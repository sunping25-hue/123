#!/usr/bin/env python3
"""Offline backup of the ShinoX private SQLite database to a restricted directory."""
from __future__ import annotations
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
import sys

def main():
    source = os.environ.get("SHINOX_DB_PATH")
    destination = os.environ.get("SHINOX_BACKUP_DIR")
    if not source or not destination:
        raise SystemExit("Set SHINOX_DB_PATH and SHINOX_BACKUP_DIR to private persistent directories")
    src = Path(source).resolve()
    backup_dir = Path(destination).resolve()
    if not src.is_file() or backup_dir == src.parent:
        raise SystemExit("Source DB missing or backup directory must be separate")
    backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(backup_dir, 0o700)
    target = backup_dir / ("shinox-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".sqlite3")
    with sqlite3.connect(src) as origin, sqlite3.connect(target) as output:
        origin.backup(output)
        if output.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            target.unlink(missing_ok=True)
            raise SystemExit("Backup integrity check failed")
    os.chmod(target, 0o600)
    print("Backup created: " + str(target) + " (contains personal data; protect and rotate separately)")

if __name__ == "__main__":
    main()
