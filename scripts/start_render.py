#!/usr/bin/env python3
"""Render entrypoint: website-only by default, forms strictly disabled."""
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
stage = os.environ.get("SHINOX_DEPLOY_STAGE", "preview")
if stage not in ("preview", "production"):
    raise SystemExit("SHINOX_DEPLOY_STAGE must be preview or production")
args = [sys.executable, str(ROOT / "server.py"), "--host", "0.0.0.0",
        "--port", str(port), "--db", db]
if stage == "production":
    args.insert(2, "--production")
else:
    if os.environ.get("SHINOX_FORM_LIVE", "0") != "0":
        raise SystemExit("Preview stage requires SHINOX_FORM_LIVE=0")
os.execv(sys.executable, args)
