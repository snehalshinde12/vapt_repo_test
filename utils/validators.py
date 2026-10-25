import re

# BUG 11 - ReDoS: nested quantifier (CWE-1333).
# A long input like "a"*40 + "!" makes this very slow.
EMAIL_PATTERN = re.compile(r"^([a-zA-Z0-9]+)+@example\.com$")


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_PATTERN.match(value))
