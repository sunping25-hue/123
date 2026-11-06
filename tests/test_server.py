"""Integration checks use a temporary database and synthetic contact data only."""
import http.client
import json
from datetime import datetime, timedelta, timezone
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
        (cls.public / '404.html').write_text('<!doctype html><html><head><link rel="stylesheet" href="site.css"></head><body>CUSTOM 404</body></html>')
        (cls.public / 'site.css').write_text('body{color:white}')
        (Path(cls.temp.name) / 'private.txt').write_text('PRIVATE_CONTENT')
        (cls.public / 'private-link.txt').symlink_to(Path(cls.temp.name) / 'private.txt')
        cls.store = RequestStore(Path(cls.temp.name) / 'requests.sqlite3')
        cls.server = PreviewServer(('127.0.0.1', 0), cls.store, cls.public, allow_test_submissions=True)
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
        return {'name': 'Preview Test', 'email': 'preview@example.test', 'consent': True, 'privacyPolicyVersion':'2026-10-29.1', 'consentConfirmedAt':'2026-10-29T00:00:00+00:00', 'message': 'Synthetic test only'}

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
        self.assertEqual(self.post('/api/booking-requests', {**self.data(), 'preferredDate': '20990101'})[0], 400)

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

    def test_custom_404_at_nested_route_and_head(self):
        for route in ['/missing.html', '/nested/missing/path?x=1', '/private-link.txt']:
            status, headers, body = self.request('GET', route)
            self.assertEqual(status, 404)
            self.assertIn(b'CUSTOM 404', body)
            self.assertIn(b'<base href="/">', body)
            self.assertNotIn(b'PRIVATE_CONTENT', body)
            self.assertEqual(headers['Cache-Control'], 'no-store')
        status, headers, body = self.request('HEAD', '/nested/missing')
        self.assertEqual(status, 404)
        self.assertEqual(body, b'')
        self.assertGreater(int(headers['Content-Length']), 0)

    def test_head_api_and_range_and_static_cache(self):
        status, headers, body = self.request('HEAD', '/video.mp4?version=1', headers={'Range': 'bytes=2-5'})
        self.assertEqual(status, 200)
        self.assertEqual(body, b'')
        self.assertEqual(headers['Content-Length'], '10')
        self.assertNotIn('Content-Range', headers)
        self.assertEqual(headers['Cache-Control'], 'private, max-age=300')
        status, headers, body = self.request('HEAD', '/api/status?check=1')
        self.assertEqual(status, 200)
        self.assertEqual(body, b'')
        self.assertEqual(headers['Cache-Control'], 'no-store')
        self.assertEqual(self.request('GET', '/site.css')[1]['Cache-Control'], 'no-cache')
        status, headers, body = self.request('GET', '/video.mp4?version=1', headers={'Range': 'bytes=2-5'})
        self.assertEqual((status, body), (206, b'2345'))
        self.assertEqual(headers['Cache-Control'], 'private, max-age=300')

    def test_invalid_ranges_and_private_paths(self):
        for value in ['bytes=-0', 'bytes=5-2', 'bytes=-', 'bytes=a-b', 'bytes=0-1,3-4', 'bytes=' + '9' * 5000 + '-']:
            self.assertEqual(self.request('GET', '/video.mp4', headers={'Range': value})[0], 416)
        status, headers, body = self.request('GET', '/private-link.txt', headers={'Range': 'bytes=0-2'})
        self.assertEqual(status, 404)
        self.assertNotIn('Content-Range', headers)
        self.assertNotIn(b'PRIVATE_CONTENT', body)
        self.assertEqual(self.request('GET', '/video.mp4', headers={'Range': 'bytes=-99'})[2], b'0123456789')

    def test_malformed_origin_blocked(self):
        for origin in ['http://[', f'http://127.0.0.1:{self.port}/path', f'http://127.0.0.1:{self.port}?x=1', 'null']:
            self.assertEqual(self.request('POST', '/api/leads', json.dumps(self.data()),
                {'Origin': origin, 'Content-Type': 'application/json'})[0], 403)

    def test_startup_retention_purge(self):
        store_path = Path(self.temp.name) / 'retention.sqlite3'
        store = RequestStore(store_path)
        identifier = store.add('lead', self.data())
        with store.connect() as connection:
            connection.execute('INSERT INTO requests VALUES (?, ?, ?, ?)', ('old-test', 'lead',
                (datetime.now(timezone.utc) - timedelta(days=31)).isoformat(), '{}'))
        store = RequestStore(store_path)
        with store.connect() as connection:
            self.assertEqual(connection.execute('SELECT id FROM requests').fetchall(), [(identifier,)])

    def test_rate_limit(self):
        for _ in range(10):
            self.post('/api/leads', {})
        self.assertEqual(self.post('/api/leads', {})[0], 429)


if __name__ == '__main__':
    unittest.main()
