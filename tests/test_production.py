"""Production integration tests use synthetic data and mock SMTP; never send real mail."""
import http.client
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from server import PreviewServer, RequestStore
from production_api import (ProductionConfig, RECIPIENTS, add_lead, deliver_pending,
                            export_csv, list_leads, prepare_store, send_notification)


class ProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.tmp.name) / "site"
        cls.site.mkdir()
        (cls.site / "index.html").write_text("ShinoX test", encoding="utf-8")
        cls.store = RequestStore(Path(cls.tmp.name) / "private.sqlite3")
        cls.config = ProductionConfig({
            "SHINOX_PUBLIC_ORIGIN": "https://shinox.example.test",
            "SHINOX_SMTP_HOST": "smtp.example.test",
            "SHINOX_SMTP_PORT": "465",
            "SHINOX_SMTP_USER": "synthetic",
            "SHINOX_SMTP_PASSWORD": "not-a-real-secret",
            "SHINOX_SMTP_FROM": "noreply@example.test",
            "SHINOX_ADMIN_TOKEN": "synthetic-token-012345678901234567890123456789",
            "SHINOX_FORM_LIVE": "1",
        })
        cls.server = PreviewServer(("127.0.0.1", 0), cls.store, cls.site, production=cls.config)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp.cleanup()

    def request(self, method, path, data=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request(method, path, data, headers or {})
        response = connection.getresponse()
        result = (response.status, dict(response.getheaders()), response.read())
        connection.close()
        return result

    def data(self):
        return {"name": "Synthetic Lead", "email": "lead@example.test",
                "phone": "0912345678", "region": "Test", "consent": True, "website": "",
                "message": "Synthetic request"}

    def post(self, origin="https://shinox.example.test"):
        return self.request("POST", "/api/leads", json.dumps(self.data()),
                            {"Origin": origin, "Content-Type": "application/json"})

    def test_config_fail_closed(self):
        with self.assertRaises(ValueError):
            ProductionConfig({})
        with self.assertRaises(ValueError):
            ProductionConfig({"SHINOX_PUBLIC_ORIGIN": "http://example.test"})

    def test_status_requires_explicit_live(self):
        result = json.loads(self.request("GET", "/api/status")[2])
        self.assertEqual(result["mode"], "production")
        self.assertTrue(result["acceptingLeads"])
        self.config.live = False
        try:
            self.assertEqual(self.post()[0], 503)
        finally:
            self.config.live = True

    def test_lead_end_to_end_storage_and_email_outbox(self):
        with patch("production_api.send_notification") as mail:
            status, _, body = self.post()
            self.assertEqual(status, 201)
            result = json.loads(body)
            self.assertTrue(result["emailSent"])
            self.assertEqual(result["status"], "received")
            self.assertFalse(result["bookingConfirmed"])
            self.assertEqual(mail.call_count, 1)
        records = list_leads(self.store)
        matching = [r for r in records if r["id"] == result["requestId"]]
        self.assertEqual(len(matching), 1)
        self.assertTrue(matching[0]["emailSent"])

    def test_email_failure_does_not_lose_request(self):
        with patch("production_api.send_notification", side_effect=OSError("SMTP offline")):
            status, _, body = self.post()
            self.assertEqual(status, 201)
            result = json.loads(body)
            self.assertFalse(result["emailSent"])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT attempts FROM notifications WHERE request_id=?",
                                        (result["requestId"],)).fetchone()[0], 1)
            self.assertIsNotNone(db.execute("SELECT id FROM requests WHERE id=?",
                                            (result["requestId"],)).fetchone())

    def test_origin_and_admin_access(self):
        self.assertEqual(self.post("https://evil.example.test")[0], 403)
        self.assertEqual(self.request("GET", "/api/admin/leads")[0], 401)
        self.assertEqual(self.request("GET", "/api/admin/leads", headers={
            "Authorization": "Bearer wrong"})[0], 401)
        status, _, body = self.request("GET", "/api/admin/leads", headers={
            "Authorization": "Bearer " + self.config.admin_token})
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(body)["ok"])
        status, headers, csv = self.request("GET", "/api/admin/export.csv", headers={
            "Authorization": "Bearer " + self.config.admin_token})
        self.assertEqual(status, 200)
        self.assertIn(b"Synthetic Lead", csv)
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_csv_formula_escape(self):
        raw = export_csv([{"id": "1", "kind": "lead", "createdAt": "now",
                           "emailSent": False, "data": {"name": "=HYPERLINK(1)"}}])
        self.assertIn(b"'=HYPERLINK(1)", raw)

    def test_smtp_two_recipients_with_mock_transport(self):
        row = ("synthetic-id", "lead", "2099-01-01T00:00:00+00:00",
               json.dumps(self.data()), 0)
        class FakeSMTP:
            def __init__(self, *args, **kwargs):
                self.message = None
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def login(self, *args):
                pass
            def send_message(self, msg):
                self.message = msg
                self.asserted_recipients = msg["To"]
                return {}
        with patch("production_api.smtplib.SMTP_SSL", FakeSMTP):
            send_notification(self.config, row)
        self.assertEqual(len(RECIPIENTS), 2)


if __name__ == "__main__":
    unittest.main()
