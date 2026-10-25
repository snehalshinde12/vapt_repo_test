import hashlib
import random


def make_token():
    # BUG 12 - Weak random for a security token (CWE-330)
    return str(random.random())


def file_checksum(data: bytes) -> str:
    # BUG 13 - SHA1 is weak (CWE-327)
    return hashlib.sha1(data).hexdigest()
