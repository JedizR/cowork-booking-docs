# ADR-0013 One test clock, off by default

## Status

Accepted, 2026-10-01

## Context

Example: the hold-expiry e2e test creates BK-7KQ2M9 at 2026-10-05T10:00:00+07:00. Then it posts `{"now": "2026-10-05T10:15:00+07:00"}` to `/_test/clock` on all three services. Member B's grid shows 2026-10-07 09:00-10:30 as free. No sleep, no 15-minute wait.

- Seed flaw A11: business logic reads Postgres `now()` and `datetime.now` (app.py:175, 250, 311, 420, 427). Source inspected at 5a1cf3d.
- The seed's own tests carry dated time bombs: a test card expiring "12/30" and a booking on 2030-01-01 (tests/test_app.py:21 and 68). Source inspected at 5a1cf3d.
- Our rules depend on time: the 60-minute notice and 30-day horizon (D5), the 15-minute hold (D11), session expiry 2 minutes earlier (D12), the 24-hour refund cut-off (D18), the check-in window (D21).
- The e2e suite drives three running containers, so an in-process time freezer cannot reach them.
- The course: "Test the split: integration failures, boundary trade-offs and a change-management policy" [syllabus site].

## Decision

- Add `clock.py` to every service. `clock.now()` is the only source of time.
- Pass `clock.now()` into SQL as a parameter. Never use `now()` or `CURRENT_TIMESTAMP` in business logic; audit-only defaults are fine, but a time that a rule or a weekly sum reads (paid_at, attempted_at, refunds.created_at, refund_requested_at) is written from `clock.now()` (ARCHITECTURE.md, Data ownership).
- Add a one-row `test_clock` table to every service's database.
- Serve `POST /_test/clock {"now": "<ISO with offset>" or null}` with 200 `{"now": ...}` only when TEST_CLOCK_ENABLED is exactly "true". Otherwise answer 404. `null` clears the override.
- When the flag is off, `clock.now()` returns real time and never reads the table.
- The override is a fixed instant: `clock.now()` returns exactly the stored value on every read until the next `POST /_test/clock`; it never advances. With the flag on, `clock.now()` reads the `test_clock` row on every call, never a per-process cache, so both gunicorn workers (ADR-0015) see a new instant from the next request. Boundary tests (10:12:59 against 10:13:00, exactly 24 h) then give the same answer on every run, and a test that needs time to pass sets the next instant.
- Set the flag only in `integration/compose.e2e.yaml`. Never in a Dockerfile, a service `compose.yaml` or `.env.example`.
- Set the same instant on all three services in every e2e step.

## Consequences

- Good: every time rule is testable across services, fast and repeatable.
- Good: service unit tests use the same override.
- Bad: one more table, route and guard in each service.
- Bad: a flag set by mistake in production would let anyone move time: lapse holds, open check-in early. The exact-"true" check and the e2e-only override are the guard.
- Bad: three clocks can disagree if a test forgets one. One e2e helper sets all three.
- Bad: moving the clock 12 h or more past a login, or back before it, ends that Purchase session (PUR-R03). The e2e helper logs every actor in again after each such move.
- A "now" without an offset, or not a time at all, gets 400 and changes nothing (D2).

## Alternatives considered

- **freezegun or time-machine.** New dependencies, and in-process only: they cannot move time inside three running containers.
- **A fake time in an env var.** Needs a restart for every step.
- **Real sleeps.** 15-minute waits; flaky.
- **SQL `now()`.** The seed's behaviour; cannot be moved.

## Rules and decisions

- Rules: PUR-R38, PMT-R20, AXS-R19, PUR-R10, PUR-R12, PUR-R30, PMT-R05, PMT-R08, PMT-R11, AXS-R13, AXS-R16.
- Decisions: D5, D11, D12, D18, D21, D27.
- Related: ADR-0007, ADR-0011, ADR-0012.

## Sources

- Spacey main 5a1cf3d: seed flaw A11; tests/test_app.py:21 and 68 (source inspected at 5a1cf3d).
- course site [syllabus site] fetched 2026-09-30: S95.
- Project team (D27).
