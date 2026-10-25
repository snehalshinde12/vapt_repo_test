# Answer key (for YOU, to compare with the scan report)

## A. Code bugs planted (SAST: Semgrep / Bandit)
| # | File | Bug | CWE | Should be found? |
|---|------|-----|-----|------------------|
| 1 | app.py | Hardcoded secrets/passwords | 798 / 259 | Yes |
| 2 | app.py `/user` | SQL injection (string +) | 89 | Yes |
| 3 | app.py `/login` | MD5 hash | 327 | Yes |
| 3b | app.py `/login` | SQL injection (f-string) | 89 | Yes |
| 4 | app.py `/ping` | Command injection, shell=True | 78 | Yes |
| 5 | app.py `/calc` | eval() | 95 | Yes |
| 6 | app.py `/load` | pickle.loads | 502 | Yes |
| 7 | app.py `/config` | yaml.load without SafeLoader | 502 | Yes |
| 8 | app.py `/file` | Path traversal | 22 | Maybe (Semgrep) |
| 9 | app.py `/fetch` | verify=False (TLS off) | 295 | Yes |
| 9b | app.py `/fetch` | SSRF | 918 | Maybe |
| 10 | app.py bottom | debug=True, host 0.0.0.0 | 489 / 605 | Yes |
| 11 | utils/validators.py | ReDoS regex | 1333 | Maybe (goes to gVisor sandbox) |
| 12 | utils/crypto_helpers.py | random for token | 330 | Yes (Bandit) |
| 13 | utils/crypto_helpers.py | SHA1 | 327 | Yes |

## B. Vulnerable libraries (OSV-Scanner on requirements.txt)
Flask 0.12.2, Werkzeug 0.14.1, Jinja2 2.10, requests 2.19.1,
urllib3 1.24.1, PyYAML 5.3, Pillow 8.1.0
-> Every one of these should show known CVEs. Expect MANY findings (dozens).

## C. What must NOT happen (false positives)
- NOTHING from `utils/safe_code.py`
- NOTHING from `tests/test_dummy.py` (the assert)

## D. Secrets safety check (very important)
- The fake AWS key `AKIAIOSFODNN7EXAMPLE` and `wJalrXUt...` must NOT appear in full
  in the PDF / HTML / Markdown / JSON. Only first 4 + last 4 chars is OK.
- Gitleaks is NOT built yet, so a "Gitleaks" finding is not expected.
  Hardcoded passwords should still come from Semgrep/Bandit.

## E. Report honesty checks
- Footer shows the tools that REALLY ran, with real versions.
- If OSV-Scanner fails, the report must say "Failed tools" and be marked incomplete.
- Report must never say "clean scan" for this repo.
- Each finding shows scanner name, file, line, and evidence.
- Severity counts in the summary = number of findings listed.

## F. Pipeline checks
- Verification: ReDoS finding -> sandbox (gVisor) / others -> static verifier.
  Look for CONFIRMED / FALSE_POSITIVE / NEEDS_REVIEW labels.
- PR / commit (Bug #3 fix): lists ONLY really-fixed items. SQL injection must go
  to "Requires Manual Review" (the rule engine never auto-fixes CWE-89).
- Duplicate findings (same bug reported by Semgrep and Bandit) should be merged.
