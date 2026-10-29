#!/usr/bin/env python3
"""ShinoX review/production service. Intake is closed until policy acceptance."""
from __future__ import annotations
import argparse
import secrets
from collections import defaultdict, deque
from datetime import date, datetime, timedelta, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import sqlite3
import threading
import time
from urllib.parse import urlsplit
import uuid
from legal_policy import PRIVACY_POLICY_VERSION, load_policy_state
from production_api import (ProductionConfig, prepare_store, add_lead, deliver_pending,
                            list_leads, export_csv)

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'shinox-v2-site'
MAX_BODY = 16_384
RETENTION_DAYS = 30


def validate_request(payload, booking=False):
    if not isinstance(payload, dict):
        raise ValueError('請提供有效表單資料。')
    if payload.get('website'):
        raise ValueError('無法接受此申請，請改用電話聯絡。')
    if payload.get('consent') is not True:
        raise ValueError('請閱讀並同意個資使用說明。')
    if payload.get('privacyPolicyVersion') != PRIVACY_POLICY_VERSION:
        raise ValueError('隱私權政策版本已更新，請重新載入頁面並確認。')
    try:
        confirmed = datetime.fromisoformat(payload.get('consentConfirmedAt', ''))
        if confirmed.tzinfo is None:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError('請重新確認本次諮詢的資料使用同意。') from None
    limits = {'name': 80, 'phone': 30, 'email': 254, 'region': 100,
              'subject': 160, 'message': 3000}
    if booking:
        limits.update(location=160, preferredDate=10, preferredTime=100)
    clean = {}
    for key, limit in limits.items():
        value = payload.get(key, '')
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError('欄位內容過長或格式不正確。')
        clean[key] = value.strip()
    if not clean['name']:
        raise ValueError('請填寫姓名。')
    if not clean['phone'] and not clean['email']:
        raise ValueError('請提供電話或 Email，方便後續聯絡。')
    if clean['phone'] and not re.fullmatch(r'[+\d()\s.-]{7,30}', clean['phone']):
        raise ValueError('請檢查電話格式。')
    if clean['email'] and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', clean['email']):
        raise ValueError('請檢查 Email 格式。')
    if booking and clean.get('preferredDate'):
        try:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', clean['preferredDate']):
                raise ValueError
            requested = date.fromisoformat(clean['preferredDate'])
        except ValueError:
            raise ValueError('請選擇有效日期。') from None
        # Taiwan is the service location. Avoid rejecting tomorrow across time zones.
        taiwan_today = datetime.now(timezone(timedelta(hours=8))).date()
        if requested < taiwan_today:
            raise ValueError('希望日期不得早於今天。')
    clean['consent'] = True
    clean['consentVersion'] = PRIVACY_POLICY_VERSION
    clean['privacyPolicyVersion'] = PRIVACY_POLICY_VERSION
    clean['consentConfirmedAt'] = confirmed.astimezone(timezone.utc).isoformat()
    clean['consentRecordedAt'] = datetime.now(timezone.utc).isoformat()
    return clean


class RequestStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS requests '
                '(id TEXT PRIMARY KEY, kind TEXT NOT NULL, created_at TEXT NOT NULL, payload TEXT NOT NULL)')
            cutoff = (datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)).isoformat()
            connection.execute('DELETE FROM requests WHERE created_at < ?', (cutoff,))
        os.chmod(self.path, 0o600)

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def add(self, kind, payload):
        identifier = str(uuid.uuid4())
        with self.connect() as connection:
            connection.execute('INSERT INTO requests VALUES (?, ?, ?, ?)',
                (identifier, kind, datetime.now(timezone.utc).isoformat(), json.dumps(payload, ensure_ascii=False)))
        return identifier


class PreviewServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, store, directory=SITE, production=None, *, allow_test_submissions=False):
        self.store = store
        self.production = production
        self.legal = load_policy_state(RETENTION_DAYS)
        self.allow_test_submissions = allow_test_submissions
        if production is not None:
            prepare_store(store)
        self.attempts = defaultdict(deque)
        self.rate_lock = threading.Lock()
        super().__init__(address, partial(Handler, directory=str(directory)))

    def rate_allowed(self, client):
        now = time.monotonic()
        with self.rate_lock:
            # Bound inactive limiter memory during long preview sessions.
            if len(self.attempts) > 1000:
                self.attempts = defaultdict(deque, {key: queue for key, queue in self.attempts.items()
                    if queue and queue[-1] > now - 600})
            queue = self.attempts[client]
            while queue and queue[0] < now - 600:
                queue.popleft()
            if len(queue) >= 10:
                return False
            queue.append(now)
            return True


class Handler(SimpleHTTPRequestHandler):
    server_version = 'ShinoXPreview/1.0'

    def log_message(self, format, *args):
        # Never print request bodies, query strings, or contact details.
        print('%s %s' % (self.command, urlsplit(self.path).path), flush=True)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        if not any(header.lower().startswith(b'cache-control:') for header in self._headers_buffer):
            self.send_header('Cache-Control', getattr(self, '_static_cache', 'no-store'))
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        # Render the real public error page without exposing filesystem details.
        if code == 404:
            public = Path(self.directory).resolve()
            page = (public / '404.html').resolve()
            if page.is_relative_to(public) and page.is_file():
                content = page.read_text(encoding='utf-8')
                # Relative CSS, logos and links must resolve at nested missing routes too.
                content = re.sub(r'<head\b[^>]*>', lambda match: match.group() + '<base href="/">', content, count=1, flags=re.I)
                body = content.encode('utf-8')
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(body)
                return
        return super().send_error(code, message, explain)

    def json_response(self, code, body):
        content = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(content)

    def do_GET(self):
        route = urlsplit(self.path).path
        if route == '/api/status':
            config = self.server.production
            if config:
                return self.json_response(200, {'mode': 'production', 'persistence': True,
                    'emailConfigured': True, 'acceptingLeads': config.live and self.server.legal['ready'],
                    'legalReviewAccepted': self.server.legal['ready'],
                    'privacyPolicyVersion': PRIVACY_POLICY_VERSION,
                    'bookingConfirmation': False, 'retentionDays': RETENTION_DAYS,
                    'retentionPurge': 'every_60_seconds'})
            return self.json_response(200, {'mode': 'local-preview', 'persistence': True,
                'emailConfigured': False, 'acceptingLeads': False, 'bookingConfirmation': False,
                'legalReviewAccepted': False, 'privacyPolicyVersion': PRIVACY_POLICY_VERSION,
                'retentionDays': RETENTION_DAYS, 'retentionPurge': 'on_startup'})
        if route in ('/api/admin/leads', '/api/admin/export.csv'):
            config = self.server.production
            if not config or not config.authorized(self.headers.get('Authorization', '')):
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Bearer realm="ShinoX admin"')
                self.send_header('Content-Length', '0')
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                return
            records = list_leads(self.server.store, 200)
            if route == '/api/admin/leads':
                return self.json_response(200, {'ok': True, 'records': records})
            data = export_csv(records)
            self.send_response(200)
            self.send_header('Content-Type', 'text/csv; charset=utf-8')
            self.send_header('Content-Disposition', 'attachment; filename="shinox-leads.csv"')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(data)
            return
        if route.startswith('/api/'):
            return self.json_response(404, {'ok': False, 'message': '找不到此服務。'})
        return super().do_GET()

    def do_HEAD(self):
        if urlsplit(self.path).path.startswith('/api/'):
            return self.do_GET()
        return super().do_HEAD()

    def do_POST(self):
        route = urlsplit(self.path).path
        if route not in ('/api/leads', '/api/booking-requests'):
            return self.json_response(404, {'ok': False, 'message': '找不到此服務。'})
        config = self.server.production
        if ((config is not None and not (config.live and self.server.legal['ready']))
                or (config is None and not self.server.allow_test_submissions)):
            return self.json_response(503, {'ok': False, 'message': '表單尚未正式開放，請先使用電話或 Email。'})
        origin = self.headers.get('Origin', '')
        try:
            parsed = urlsplit(origin)
            valid_origin = (parsed.scheme in ('http', 'https') and bool(parsed.netloc)
                and not parsed.username and not parsed.password
                and not parsed.path and not parsed.query and not parsed.fragment)
        except ValueError:
            valid_origin = False
            parsed = urlsplit('')
        extras = {item.strip() for item in os.environ.get('SHINOX_ALLOWED_ORIGINS', '').split(',') if item.strip()}
        # Host is the browser-visible host; additional reverse proxy origins must be explicit.
        same_origin = valid_origin and parsed.netloc == self.headers.get('Host')
        if config is not None:
            origin_allowed = valid_origin and origin == config.origin
        else:
            origin_allowed = valid_origin and (same_origin or origin in extras)
        if not origin_allowed:
            return self.json_response(403, {'ok': False, 'message': '請從本站頁面送出表單。'})
        if not self.server.rate_allowed(self.client_address[0]):
            return self.json_response(429, {'ok': False, 'message': '送出次數過多，請稍後再試或電話聯絡。'})
        if self.headers.get_content_type() != 'application/json':
            return self.json_response(415, {'ok': False, 'message': '請使用 JSON 格式送出。'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            return self.json_response(413, {'ok': False, 'message': '表單內容大小不正確。'})
        try:
            payload = json.loads(self.rfile.read(length))
            booking = route == '/api/booking-requests'
            clean = validate_request(payload, booking)
        except (ValueError, UnicodeError) as error:
            message = str(error) if not isinstance(error, (json.JSONDecodeError, UnicodeError)) else '表單資料格式不正確。'
            return self.json_response(400, {'ok': False, 'message': message})
        try:
            kind = 'booking-request' if booking else 'lead'
            identifier = (add_lead(self.server.store, kind, clean) if config is not None
                          else self.server.store.add(kind, clean))
        except sqlite3.Error:
            return self.json_response(503, {'ok': False, 'message': '暫時無法儲存，請改用電話或 Email 聯絡。'})
        if config is not None:
            emailed = deliver_pending(self.server.store, config, identifier)
            message = ('展示洽詢已收到，展示地點與時段仍須專人確認。' if booking
                       else '您的設備與建場洽詢已收到，我們會盡快與您聯絡。')
            return self.json_response(201, {'ok': True, 'requestId': identifier,
                'status': 'received', 'emailSent': emailed, 'bookingConfirmed': False,
                'message': message})
        message = ('展示洽詢已儲存於本機預覽；尚未確認地點、日期或時段，也未通知業務。請電話聯絡完成安排。'
                   if booking else '詢問已儲存於本機預覽；尚未寄送或通知業務。請使用電話或 Email 完成聯絡。')
        return self.json_response(201, {'ok': True, 'requestId': identifier,
            'status': 'received_locally', 'emailSent': False, 'bookingConfirmed': False, 'message': message})

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_head(self):
        # Restrict symlinks and static access to the intended public site directory.
        resolved = Path(self.translate_path(self.path)).resolve()
        public = Path(self.directory).resolve()
        if not resolved.is_relative_to(public):
            self.send_error(404)
            return None
        self._static_cache = 'private, max-age=300' if resolved.suffix.lower() == '.mp4' else 'no-cache'
        # Range has meaning only for GET; HEAD describes the full representation.
        if self.command != 'GET' or not self.headers.get('Range') or not resolved.is_file():
            return super().send_head()
        size = resolved.stat().st_size
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers['Range'].strip())
        if not match or not any(match.groups()) or any(len(part) > 20 for part in match.groups()):
            return self.range_error(size)
        first, last = match.groups()
        if not first:
            suffix = int(last)
            if suffix == 0:
                return self.range_error(size)
            start, end = max(0, size - suffix), size - 1
        else:
            start, end = int(first), min(int(last), size - 1) if last else size - 1
        if start >= size or start > end:
            return self.range_error(size)
        file = resolved.open('rb')
        file.seek(start)
        self._range_remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(resolved)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self._range_remaining))
        self.end_headers()
        return file

    def range_error(self, size):
        self.send_response(416)
        self.send_header('Content-Range', f'bytes */{size}')
        self.send_header('Content-Length', '0')
        self.end_headers()
        return None

    def copyfile(self, source, outputfile):
        remaining = getattr(self, '_range_remaining', None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        try:
            while remaining:
                block = source.read(min(64 * 1024, remaining))
                if not block:
                    break
                outputfile.write(block)
                remaining -= len(block)
        finally:
            del self._range_remaining


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3003)
    parser.add_argument('--db', default=str(ROOT.parent / 'work' / 'shinox-runtime' / 'requests.sqlite3'))
    parser.add_argument('--production', action='store_true',
                        help='Require HTTPS reverse proxy, durable private DB and SMTP secrets')
    args = parser.parse_args()
    config = ProductionConfig() if args.production else None
    db_path = Path(args.db).resolve()
    if config is not None:
        if db_path.is_relative_to(SITE.resolve()) or db_path.is_relative_to(ROOT.resolve()):
            parser.error('Production DB must live outside the repository and public site')
        if not os.environ.get('SHINOX_DB_PATH') or db_path != Path(os.environ['SHINOX_DB_PATH']).resolve():
            parser.error('Set SHINOX_DB_PATH to an explicit persistent-volume path and pass it as --db')
    store = RequestStore(db_path)
    server = PreviewServer((args.host, args.port), store, production=config)
    if config:
        def notification_worker():
            while True:
                try:
                    if config.live and server.legal['ready']:
                        deliver_pending(store, config)
                    cutoff = (datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)).isoformat()
                    with store.connect() as db:
                        db.execute('DELETE FROM requests WHERE created_at < ?', (cutoff,))
                        db.execute('DELETE FROM notifications WHERE request_id NOT IN (SELECT id FROM requests)')
                except (OSError, sqlite3.Error):
                    pass  # Never log contact data or SMTP secrets.
                time.sleep(60)
        threading.Thread(target=notification_worker, daemon=True).start()
    print(('ShinoX production service: live=' + str(config.live) if config
           else 'ShinoX local review: no email or booking confirmation'), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
