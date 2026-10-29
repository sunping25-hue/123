#!/usr/bin/env python3
"""Start ShinoX behind Render's HTTPS reverse proxy; forms stay disabled by default."""
from __future__ import annotations
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
db = os.environ.get("SHINOX_DB_PATH", "")
if not db or not Path(db).is_absolute():
    raise SystemExit("SHINOX_DB_PATH must be an absolute private persistent disk path")
port = int(os.environ.get("PORT", "10000"))
if not 1 <= port <= 65535:
    raise SystemExit("Invalid PORT")
os.execv(sys.executable, [sys.executable, str(ROOT / "server.py"),
                          "--production", "--host", "0.0.0.0",
                          "--port", str(port), "--db", db])
