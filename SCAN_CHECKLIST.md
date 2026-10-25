# Quick checklist after you scan

1. Push this folder to a NEW GitHub repo (public or private with PAT).
2. Scan it from your tool (chatbot -> GitHub scan).
3. Fill this table:

| Check | Result (Yes / No) |
|-------|-------------------|
| Scan finished without crash | |
| Footer lists tools + real versions | |
| OSV-Scanner worked (CVE findings for 7 libraries) | |
| Semgrep findings for app.py | |
| Bandit findings for app.py | |
| SQL injection found (2 places) | |
| Command injection found | |
| eval, pickle, yaml.load found | |
| Weak hash + weak random found | |
| debug=True found | |
| ReDoS found / verified | |
| Nothing reported in utils/safe_code.py | |
| Fake AWS key is hidden/redacted in all formats | |
| PDF, HTML, MD, JSON all show the same findings | |
| Not marked "clean scan" | |
| PR lists only fixed items; SQLi in manual review | |
