"""Production-only ShinoX lead operations. No credentials or customer data in Git."""
from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
import hmac
import io
import json
import os
from pathlib import Path
import smtplib
import ssl
from urllib.parse import urlsplit

RECIPIENTS = ("shinox.car.washer@gmail.com", "sunping25@gmail.com")
MAX_ATTEMPTS = 12


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class ProductionConfig:
    """Fail closed: every required secret, domain and durable DB must be explicit."""

    def __init__(self, environ=None):
        env = os.environ if environ is None else environ
        self.origin = env.get("SHINOX_PUBLIC_ORIGIN", "").rstrip("/")
        url = urlsplit(self.origin)
        if url.scheme != "https" or not url.netloc or url.username or url.password or url.path or url.query or url.fragment:
            raise ValueError("SHINOX_PUBLIC_ORIGIN must be an exact HTTPS origin")
        self.smtp_host = env.get("SHINOX_SMTP_HOST", "")
        self.smtp_port = int(env.get("SHINOX_SMTP_PORT", "465"))
        self.smtp_user = env.get("SHINOX_SMTP_USER", "")
        self.smtp_password = env.get("SHINOX_SMTP_PASSWORD", "")
        self.smtp_from = env.get("SHINOX_SMTP_FROM", "")
        self.admin_token = env.get("SHINOX_ADMIN_TOKEN", "")
        self.live = env.get("SHINOX_FORM_LIVE", "0") == "1"
        if not all((self.smtp_host, self.smtp_user, self.smtp_password, self.smtp_from)):
            raise ValueError("SMTP configuration is incomplete")
        if len(self.admin_token) < 32:
            raise ValueError("SHINOX_ADMIN_TOKEN must be at least 32 characters")
        if self.smtp_port not in (465, 587):
            raise ValueError("SMTP port must be 465 (TLS) or 587 (STARTTLS)")

    def authorized(self, header):
        prefix = "Bearer "
        return bool(header.startswith(prefix) and hmac.compare_digest(
            header[len(prefix):].encode("utf-8"), self.admin_token.encode("utf-8")))


def prepare_store(store):
    with store.connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS notifications (
            request_id TEXT PRIMARY KEY,
            attempts INTEGER NOT NULL DEFAULT 0,
            next_attempt TEXT NOT NULL,
            sent_at TEXT,
            FOREIGN KEY(request_id) REFERENCES requests(id)
        )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_requests_created ON requests(created_at)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_notify_pending ON notifications(sent_at, next_attempt)")
        db.execute("DELETE FROM notifications WHERE request_id NOT IN (SELECT id FROM requests)")


def add_lead(store, kind, payload):
    """Insert request and notification outbox entry in one SQLite transaction."""
    import uuid
    identifier = str(uuid.uuid4())
    with store.connect() as db:
        db.execute("INSERT INTO requests (id,kind,created_at,payload) VALUES (?,?,?,?)",
                   (identifier, kind, utc_now(), json.dumps(payload, ensure_ascii=False)))
        db.execute("INSERT INTO notifications (request_id,next_attempt) VALUES (?,?)",
                   (identifier, utc_now()))
    return identifier


def pending(store, request_id=None, limit=20):
    with store.connect() as db:
        if request_id:
            rows = db.execute("""SELECT r.id,r.kind,r.created_at,r.payload,n.attempts
                FROM requests r JOIN notifications n ON n.request_id=r.id
                WHERE r.id=? AND n.sent_at IS NULL AND n.attempts<?""",
                (request_id, MAX_ATTEMPTS)).fetchall()
        else:
            rows = db.execute("""SELECT r.id,r.kind,r.created_at,r.payload,n.attempts
                FROM requests r JOIN notifications n ON n.request_id=r.id
                WHERE n.sent_at IS NULL AND n.attempts<? AND n.next_attempt<=?
                ORDER BY r.created_at LIMIT ?""", (MAX_ATTEMPTS, utc_now(), limit)).fetchall()
    return rows


def send_notification(config, row):
    identifier, kind, created, payload_json, _ = row
    data = json.loads(payload_json)
    msg = EmailMessage()
    msg["Subject"] = ("[ShinoX 展示洽詢] " if kind == "booking-request" else "[ShinoX 新客戶詢問] ") + identifier[:8]
    msg["From"] = config.smtp_from
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Reply-To"] = data["email"] if data.get("email") else config.smtp_from
    keys = ("name", "phone", "email", "region", "subject", "message",
            "location", "preferredDate", "preferredTime")
    labels = ("姓名", "電話", "Email", "地區", "主題", "需求說明",
              "展示地點", "偏好日期", "偏好時段")
    lines = ["ShinoX 官網新詢問", "案件編號：" + identifier, "收件時間 UTC：" + created,
             "類型：" + kind, ""]
    lines.extend(label + "：" + str(data.get(key, "")) for key, label in zip(keys, labels) if data.get(key))
    lines.append("\n此信件包含個人資料，請勿轉寄給無關人員。")
    msg.set_content("\n".join(lines))
    context = ssl.create_default_context()
    if config.smtp_port == 465:
        with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, timeout=12, context=context) as smtp:
            smtp.login(config.smtp_user, config.smtp_password)
            refused = smtp.send_message(msg)
    else:
        with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=12) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(config.smtp_user, config.smtp_password)
            refused = smtp.send_message(msg)
    if refused:
        raise RuntimeError("Some recipients were rejected")


def deliver_pending(store, config, request_id=None):
    """Never lose a saved lead because SMTP is unavailable; retry with backoff."""
    delivered = False
    for row in pending(store, request_id):
        identifier, _, _, _, attempts = row
        try:
            send_notification(config, row)
        except (OSError, smtplib.SMTPException, RuntimeError, ValueError):
            delay = min(3600, 60 * 2 ** min(attempts, 6))
            next_time = (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat()
            with store.connect() as db:
                db.execute("""UPDATE notifications SET attempts=attempts+1,next_attempt=?
                    WHERE request_id=? AND sent_at IS NULL""", (next_time, identifier))
        else:
            with store.connect() as db:
                db.execute("UPDATE notifications SET sent_at=? WHERE request_id=?",
                           (utc_now(), identifier))
            if identifier == request_id:
                delivered = True
    return delivered


def list_leads(store, limit=100):
    limit = max(1, min(int(limit), 200))
    with store.connect() as db:
        rows = db.execute("""SELECT r.id,r.kind,r.created_at,r.payload,n.sent_at,n.attempts
            FROM requests r LEFT JOIN notifications n ON n.request_id=r.id
            ORDER BY r.created_at DESC LIMIT ?""", (limit,)).fetchall()
    return [{"id": ident, "kind": kind, "createdAt": created,
             "data": json.loads(payload), "emailSent": bool(sent),
             "notificationAttempts": attempts or 0}
            for ident, kind, created, payload, sent, attempts in rows]


def export_csv(records):
    columns = ("id", "kind", "createdAt", "emailSent", "name", "phone", "email",
               "region", "subject", "message", "location", "preferredDate", "preferredTime")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    for record in records:
        data = record["data"]
        values = [record.get(key, data.get(key, "")) for key in columns]
        # Prevent spreadsheet formula execution on CSV import.
        writer.writerow(["'" + v if isinstance(v, str) and v.lstrip().startswith(("=", "+", "-", "@")) else v
                         for v in values])
    return output.getvalue().encode("utf-8-sig")
