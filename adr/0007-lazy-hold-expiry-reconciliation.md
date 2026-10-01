# ADR-0007 Lazy hold expiry and reconciliation

## Status

Accepted, 2026-10-01

## Context

Example: at 2026-10-05 10:00 Member A presses "Continue to payment" for Meeting Room A, 2026-10-07 09:00-10:30. BK-7KQ2M9 is held; hold_expires_at is 10:15; the session's expires_at is 10:13. Member A never pays.

- No job runs at 10:15.
- At 10:16 Member B opens the grid. The slot-blocking predicate, `confirmed OR (held AND hold_expires_at > :now)`, already treats 09:00-10:30 as free.
- Member B books it. The pre-insert sweep calls GET /payment-sessions/ps_..., sees unpaid, marks BK-7KQ2M9 expired, and then Member B's insert runs.

Seed flaw F3: an unpaid row blocks its slot forever. The INSERT stores `paid = false` (app.py:745-765), the exclusion constraint covers every row (app.py:130-135), and no column records a hold or an expiry (source inspected at 5a1cf3d). Class rules PR #6 (at c18b638) made that a rule, SLOT-R01 "An unpaid booking holds its slot until it is cancelled", and asked "for how long before it is released (for example, a payment deadline)?".

Constraints: gunicorn with 2 workers, no scheduler, no broker (ADR-0015). Only Purchase calls other services (ADR-0004).

## Decision

- Never trust a stored held status alone. Every availability read and the booking check use the slot-blocking predicate with `:now` = `clock.now()` passed as a parameter (PUR-R12).
- Let the stored status catch up when touched. At the reconcile points of PUR-R24 (the booking page and its return URL, GET /api/bookings/<ref>, My bookings (the page and GET /api/bookings/mine), the cancel confirm screen, the pre-insert sweep, the Member's own lapsed holds (PUR-R39), and the Operator's Reconcile of one booking or of all held), Purchase calls GET /payment-sessions/<id> for a held booking; the POST cancel uses expire in place of the GET (PUR-R31):
  - paid: fulfilment, even after the hold lapsed (PUR-R25);
  - unpaid, hold lapsed: expired;
  - unpaid, inside the hold: no change;
  - Payment unreachable: no change.
- Reconcile the space's stale holds before an insert, in their own short steps, then check and insert in one transaction. The partial EXCLUDE on held and confirmed rows turns a lost race into "Slot just taken" (PUR-R22).
- Let Payment close its side on its own clock: a session is expired from expires_at (PMT-R05, PMT-R11).
- Run no background job, cron or thread.

## Consequences

- Good: no extra process and nothing to schedule. Tests move time with the test clock (ADR-0013).
- Good: a payment that lands never loses the booking. Paid goes to confirmed, even when the Member closed the tab (seq-lost-redirect).
- Bad: the stored status lags. A lapsed hold still reads held in the database, and in bookings by status on the dashboard (PUR-R34), until something touches it. The Operator's Reconcile fixes it by hand.
- Bad: while Payment is down, a stale hold cannot be resolved, so a conflicting insert gets 503 (D13). Member A's lapsed, unpaid hold can then block Member B until Payment answers.
- Bad: each touch costs one Payment round trip, bounded by timeout=5.

## Alternatives considered

- **Background sweeper** (thread or cron). Rejected: another process to run and monitor; it would read the real clock unless wired to `clock.now()`; two workers would run it twice.
- **pg_cron in the database.** Not in the pinned stack.
- **Expire in SQL without asking Payment.** Rejected: it would expire a booking whose payment already landed, the lost-redirect case.
- **Payment webhooks.** See ADR-0004.
- **No expiry.** The seed's behaviour, F3.

## Rules and decisions

- Rules: PUR-R12, PUR-R21, PUR-R22, PUR-R24, PUR-R25, PUR-R31, PUR-R34, PUR-R39, PUR-R40, PMT-R05, PMT-R11.
- Terms: PUR-T20, PUR-T21, PUR-T26. Question: PUR-Q09.
- Decisions: D11, D12, D13, D14, D27.
- Diagram: seq-hold-expiry. Related: ADR-0004, ADR-0013.

## Sources

- Spacey main 5a1cf3d: seed flaw F3, app.py:130-135 and 745-765 (source inspected at 5a1cf3d).
- class PR #6 diff at c18b638: SLOT-R01, Q-SLOT-2.
- Project team (D11, D12, D13).
