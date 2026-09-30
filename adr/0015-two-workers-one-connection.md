# ADR-0015 Two gunicorn workers, one database connection each

## Status

Accepted, 2026-10-01

## Context

Example: worker 1 waits up to 5 s for Payment on Member A's "Continue to payment". Worker 2 still serves Member B's grid. A third request waits in gunicorn's queue until a worker is free.

- Seed flaw A8: one shared autocommit connection for the whole app, no reconnect, DDL at import (app.py:25, 387, 1053). Source inspected at 5a1cf3d.
- The seed runs 1 sync worker: no `-w` in the Dockerfile (line 17) and no `workers` in `gunicorn.conf.py`. `LOAD_TEST.md` claims `-w 2`, wrongly. Source inspected at 5a1cf3d.
- Seed flaw F14: the pay check-then-update runs without a transaction (app.py:940-965). Source inspected at 5a1cf3d.
- Services now call each other with timeout=5, so a single worker would freeze on one slow provider.
- A pool, `psycopg_pool`, would be a new runtime dependency; the stack allows only `segno` (ADR-0010).

## Decision

- Set `workers = 2` (sync) in `gunicorn.conf.py` in every service.
- Open one psycopg connection per worker at start, keep it, and fail fast when the database is unreachable.
- Wrap booking insert, fulfilment, pay attempt and refund (and step 1 of a cancel) in explicit transactions. Lock the deciding row with `SELECT ... FOR UPDATE` where one row decides the outcome.
- Never make an HTTP call inside an open transaction. Give every outbound call timeout=5.
- Put a `# ponytail:` comment on the connection code naming the ceiling (2 concurrent requests per service, no reconnect) and the upgrade path (`psycopg_pool`).
- Run the start-up DDL under a Postgres advisory lock, so the two workers do not race on it.

## Consequences

- Good: two requests at once per service, and one slow provider call no longer stalls everything.
- Good: each worker is its own process with its own connection, so one request's transaction cannot leak into another's.
- Good: no new dependency.
- Bad: the ceiling is 2 concurrent requests per service. Two slow provider calls stall a service for up to 5 s.
- Bad: a dropped connection breaks that worker until restart. `/health` reports 503; reconnect is out of scope.
- Bad: two connections per service, not one, against each database.

## Alternatives considered

- **`psycopg_pool`.** The upgrade path when load needs it. Not now: a new dependency.
- **A connection per request.** No dependency and a simpler reconnect story, but a connect on every request, and the fail-fast start check moves.
- **More workers or threads.** More connections for no measured need; thread workers need thread-safe connection handling.
- **Async workers (gevent).** A new dependency.
- **One worker.** The seed's setup; stalls on every provider call.

## Rules and decisions

- Rules: PUR-R22, PUR-R25, PUR-R32, PUR-R35, PMT-R06, PMT-R12, PMT-R15.
- Decisions: D13, D28.
- Related: ADR-0004, ADR-0011.

## Sources

- Spacey main 5a1cf3d: seed flaws A8 and F14; Dockerfile:17; `gunicorn.conf.py` (source inspected at 5a1cf3d).
- inventory/spacey-app.md, "DB connection handling" (source inspected at 5a1cf3d).
- Project team (D28).
