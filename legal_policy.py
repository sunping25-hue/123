"""Public policy metadata and a fail-closed intake gate. No customer data here."""
import json
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parent / 'shinox-v2-site' / 'legal-config.json'
PRIVACY_POLICY_VERSION = '2026-10-29.1'


def load_policy_state(expected_retention_days=30):
    try:
        data = json.loads(POLICY_PATH.read_text(encoding='utf-8'))
        ready = (
            data.get('reviewAccepted') is True
            and data.get('privacyVersion') == PRIVACY_POLICY_VERSION
            and bool(data.get('reviewAcceptedAt'))
            and bool(data.get('operatorLegalName'))
            and bool(data.get('rightsContactEmail'))
            and data.get('approvedDatabaseRetentionDays') == expected_retention_days
            and bool(data.get('approvedEmailRetention'))
            and bool(data.get('approvedBackupRetention'))
        )
    except (OSError, ValueError, TypeError, AttributeError):
        ready = False
    return {'ready': bool(ready), 'privacyVersion': PRIVACY_POLICY_VERSION}
