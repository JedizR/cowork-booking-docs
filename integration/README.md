# Integration stack and e2e suite

`compose.yaml` builds Purchase, Payment and Access from the sibling repos (`../../cowork-booking-purchase`,
`../../cowork-booking-payment`, `../../cowork-booking-access`), each with its own postgres:16. No database port is
published. Every variable has a dev default, so no `.env` file is needed; copy `.env.example` to `.env` to change one.

| Service | URL | Health |
|---|---|---|
| Purchase | http://localhost:8001 | `/health` |
| Payment | http://localhost:8002 | `/health` |
| Access | http://localhost:8003 | `/health` |

## Normal run (no test clock)

```bash
for s in purchase payment access; do (cd ../../cowork-booking-$s && docker compose down); done  # frees ports 8001-8003
docker compose up -d --build --wait
```

## e2e run

`compose.e2e.yaml` only sets `TEST_CLOCK_ENABLED=true` on the three apps, which opens `POST /_test/clock` (D27).
Use it for the e2e run only. Run from this folder:

```bash
for s in purchase payment access; do (cd ../../cowork-booking-$s && docker compose down); done
docker compose -f compose.yaml -f compose.e2e.yaml up -d --build --wait
uv venv -p 3.12 .venv && uv pip install -p .venv/bin/python -r e2e/requirements.txt
.venv/bin/python -m pytest e2e -q --junitxml=reports/e2e.xml
docker compose -f compose.yaml -f compose.e2e.yaml down -v
```

How the suite works:

- It reads `PURCHASE_URL`, `PAYMENT_URL`, `ACCESS_URL`, `PAYMENT_API_TOKEN`, `ACCESS_API_TOKEN`, `OPERATOR_EMAIL`,
  `OPERATOR_PASSWORD`, `STAFF_PASSWORD` and `E2E_OPERATOR_PASSWORD` from the environment, else from `.env`, else
  the same dev defaults as compose.
- Each test sets the same test-clock instant on all three services before any login (day 0 10:00 Bangkok, where
  day 0 is 4 days after the real date) and clears it afterwards.
- Each test registers fresh Members (`a-<uuid>@example.com`) and has the Operator create its own uniquely named
  spaces, so tests never share a slot and the suite passes when run twice against the same stack.
- Shared figures (Payment totals) are asserted as before-and-after deltas; Payment and Purchase operator rows are
  scoped by `data-booking-reference`.
- The suite registers `OPERATOR_EMAIL` with `E2E_OPERATOR_PASSWORD`, or logs in if it is already registered. Never
  register `OPERATOR_EMAIL` by hand on the e2e stack. If the login fails, the run stops: remove the volumes with
  `docker compose -f compose.yaml -f compose.e2e.yaml down -v`.
- "Held cancel racing with payment" pays with `allow_redirects=False` and reads nothing in Purchase before the
  cancel, because every Purchase read reconciles (purchase-public.md section 11).
