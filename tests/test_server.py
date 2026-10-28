"""Integration checks use a temporary database and synthetic contact data only."""
import http.client
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from server import PreviewServer, RequestStore, validate_request


class PreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.public = Path(cls.temp.name) / 'site'
        cls.public.mkdir()
        (cls.public / 'video.mp4').write_bytes(b'0123456789')
        cls.store = RequestStore(Path(cls.temp.name) / 'requests.sqlite3')
        cls.server = PreviewServer(('127.0.0.1', 0), cls.store, cls.public)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.temp.cleanup()

    def setUp(self):
        self.server.attempts.clear()

    def request(self, method, route, body=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.port)
        connection.request(method, route, body, headers or {})
        response = connection.getresponse()
        data = response.read()
        result = response.status, dict(response.getheaders()), data
        connection.close()
        return result

    def post(self, route, payload, origin=True):
        headers = {'Content-Type': 'application/json'}
        if origin:
            headers['Origin'] = f'http://127.0.0.1:{self.port}'
        return self.request('POST', route, json.dumps(payload), headers)

    def data(self):
        return {'name': 'Preview Test', 'email': 'preview@example.test', 'consent': True, 'message': 'Synthetic test only'}

    def test_request_persists_and_does_not_claim_delivery(self):
        status, _, body = self.post('/api/leads', self.data())
        record = json.loads(body)
        self.assertEqual(status, 201)
        self.assertFalse(record['emailSent'])
        self.assertEqual(record['status'], 'received_locally')
        with self.store.connect() as connection:
            self.assertEqual(connection.execute('SELECT kind FROM requests WHERE id=?', (record['requestId'],)).fetchone()[0], 'lead')

    def test_booking_is_request_not_confirmation(self):
        status, _, body = self.post('/api/booking-requests', {**self.data(), 'preferredDate': '2099-01-01', 'preferredTime': '請電話討論'})
        self.assertEqual(status, 201)
        self.assertFalse(json.loads(body)['bookingConfirmed'])
        self.assertIn('尚未確認', json.loads(body)['message'])

    def test_validation_and_consent(self):
        for payload in [{}, {**self.data(), 'consent': False}, {**self.data(), 'email': 'broken'}, {**self.data(), 'name': ['invalid']}, {**self.data(), 'website': 'bot'}]:
            self.assertEqual(self.post('/api/leads', payload)[0], 400)
        self.assertEqual(self.post('/api/booking-requests', {**self.data(), 'preferredDate': '2000-01-01'})[0], 400)

    def test_cross_origin_and_missing_origin_blocked(self):
        self.assertEqual(self.post('/api/leads', self.data(), origin=False)[0], 403)
        self.assertEqual(self.request('POST', '/api/leads', '{}', {'Origin': 'https://elsewhere.example', 'Content-Type': 'application/json'})[0], 403)

    def test_byte_ranges(self):
        for value, expected in [('bytes=2-5', b'2345'), ('bytes=-3', b'789'), ('bytes=8-', b'89')]:
            status, headers, body = self.request('GET', '/video.mp4', headers={'Range': value})
            self.assertEqual(status, 206)
            self.assertEqual(body, expected)
            self.assertIn('Content-Range', headers)
        self.assertEqual(self.request('GET', '/video.mp4', headers={'Range': 'bytes=99-'})[0], 416)

    def test_no_directory_listing_or_private_api(self):
        self.assertEqual(self.request('GET', '/')[0], 404)
        self.assertEqual(self.request('GET', '/api/leads')[0], 404)
        self.assertEqual(json.loads(self.request('GET', '/api/status')[2])['bookingConfirmation'], False)

    def test_rate_limit(self):
        for _ in range(10):
            self.post('/api/leads', {})
        self.assertEqual(self.post('/api/leads', {})[0], 429)


if __name__ == '__main__':
    unittest.main()
