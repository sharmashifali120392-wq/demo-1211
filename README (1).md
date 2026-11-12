# Code Scanning Demo

A tiny, intentionally vulnerable Flask app to show GitHub code scanning (CodeQL) in action.

## Repo layout

```
.
├── app.py
├── requirements.txt
└── .github/
    └── workflows/
        └── codeql.yml
```

## Run the demo

1. Create a new GitHub repo (public repos get code scanning free; private repos need GitHub Advanced Security / Code Security).
2. Add `app.py`, `requirements.txt`, and put `codeql.yml` at `.github/workflows/codeql.yml`.
3. Push to `main`.
4. Open the **Actions** tab and watch the **CodeQL** workflow run (~2–4 min).
5. Open **Security → Code scanning** to see the alerts.

## Expected alerts

| Route    | Issue                       | CodeQL rule                     |
|----------|-----------------------------|---------------------------------|
| `/user`  | SQL injection               | `py/sql-injection`              |
| `/ping`  | Command injection           | `py/command-line-injection`     |
| `/read`  | Path traversal              | `py/path-injection`             |
| `/hello` | Reflected XSS               | `py/reflective-xss`             |
| `main`   | Flask debug mode            | `py/flask-debug`                |

## Show the PR experience (optional)

Make a branch, fix one bug, and open a PR — the alert will be marked fixed. Or add a new bug in a PR and CodeQL will comment on the exact line. For example, the SQL fix:

```python
rows = get_db().execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
```

> ⚠️ This code is vulnerable on purpose. Never deploy it.
