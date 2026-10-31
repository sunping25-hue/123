"""Policy gates use synthetic fixtures only and never open actual intake."""
import http.client,json,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from legal_policy import load_policy_state
from server import PreviewServer,RequestStore

class PolicyTests(unittest.TestCase):
    def test_published_policy_is_not_accepted(self):
        self.assertFalse(load_policy_state()['ready'])

    def test_acceptance_flag_alone_cannot_open_intake(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'policy.json';p.write_text(json.dumps({'reviewAccepted':True,'privacyVersion':'2026-10-29.1'}))
            with patch('legal_policy.POLICY_PATH',p):self.assertFalse(load_policy_state()['ready'])

    def test_default_preview_rejects_both_intake_routes_without_storage(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=RequestStore(Path(tmp)/'db.sqlite3');server=PreviewServer(('127.0.0.1',0),store,tmp)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                for path in ['/api/leads','/api/booking-requests']:
                    connection=http.client.HTTPConnection('127.0.0.1',server.server_port)
                    connection.request('POST',path,b'{}',{'Content-Type':'application/json'})
                    response=connection.getresponse();self.assertEqual(response.status,503);response.read();connection.close()
                with store.connect() as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM requests').fetchone()[0],0)
            finally:server.shutdown();server.server_close()
