"""SAFE code. A good scanner should report NOTHING here (tests false positives)."""
import hashlib
import secrets
import sqlite3
import subprocess


def get_user_safe(conn: sqlite3.Connection, name: str):
    # Parameterized query - safe
    return conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()


def ping_safe(host: str) -> bytes:
    # List arguments, no shell - safe
    return subprocess.check_output(["ping", "-c", "1", host], shell=False)


def make_token_safe() -> str:
    return secrets.token_hex(16)


def checksum_safe(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
