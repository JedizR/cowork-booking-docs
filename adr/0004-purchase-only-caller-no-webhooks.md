# ADR-0004 Only Purchase calls other services; no webhooks

## Status

Accepted, 2026-10-01

## Context

Example (lost redirect): at 2026-10-05 10:05 Member A pays BK-7KQ2M9 with 4242 4242 4242 4242 and closes the tab before the redirect. Nobody tells Purchase. At 10:20 Member A opens My bookings. Purchase calls GET /payment-sessions/ps_..., sees paid, confirms the booking (not expired, although the hold lapsed at 10:15) and calls POST /grants.

The course call flow runs one way: "Purchase → Payments": "“Collect this agreed amount.”", then "Purchase interprets the result", then "Purchase → Access": "“Issue an authorised grant.”" [extraction site]. Payments owns "Payment record / Processing outcome / Not booking or access state" [extraction site].

A Stripe-style checkout sends a webhook when a session completes, because a real processor can settle late. Ours cannot: Payment refuses every attempt at or after expires_at, and expires_at is hold_expires_at − 2 min (D12, PMT-R11). Every payment outcome is final 2 minutes before the hold ends. Nothing arrives late, so nothing needs pushing.

## Decision

- Only Purchase calls another service, over HTTP/JSON with a bearer token (ADR-0019) and timeout=5.
  - Purchase → Payment: POST /payment-sessions, GET /payment-sessions/<id>, POST /payment-sessions/<id>/expire, POST /refunds.
  - Purchase → Access: POST /grants, POST /grants/<booking_reference>/revoke. GET /grants/<booking_reference> exists for tests; Purchase does not call it in v1 (PUR-R26).
- Payment and Access call no one. They answer. Payment sends the Member's browser back by a redirect to success_url?session_id=ps_..., or by the Back link to cancel_url.
- Defer Stripe-style webhooks. Purchase pulls the outcome whenever it touches a held booking (D13, ADR-0007).
- Never call while a database transaction is open.
- Treat a timeout, a connection error or a 5xx answer as unreachable: change nothing; answer a request that needs the result with 503 (JSON) or a flashed "try again" (form).

## Consequences

- Good: trust runs one way. Only the providers check tokens; Purchase has no inbound machine endpoint to sign, verify or retry.
- Good: no cycles. A provider never waits on Purchase, so one slow service cannot deadlock another.
- Good: the invariant holds without push: every paid session ends as a confirmed booking or a refund attempt (D13, D14).
- Bad: Purchase orchestrates everything. If Purchase is down, nothing moves.
- Bad: a paid booking stays stored as held until something touches it. After hold_expires_at the grid can show its slot as free; the pre-insert sweep (PUR-R22) then confirms it, and the second Member gets "Slot just taken", never a double booking. The Operator's Reconcile covers rows nobody touches.
- Bad: while Payment is down, a held cancel (PUR-R31) and a conflicting insert get 503.

## Alternatives considered

- **Payment webhook to Purchase.** Rejected for v1: it needs an inbound endpoint on Purchase, request signing, retries and a second trust direction, and adds nothing while D12 holds. Revisit with a real processor (PMT-Q01); webhooks would then arrive at Payment only.
- **Payment calls Access on success.** Rejected: Payment would need booking policy (coverage, cancel in progress), which it must not own.
- **A message broker.** Not in the pinned stack.

## Rules and decisions

- Rules: PUR-R22, PUR-R24, PUR-R25, PUR-R26, PUR-R31, PUR-R32, PUR-R35, PUR-R40, PMT-R01, PMT-R06, PMT-R10, PMT-R11, PMT-R18, AXS-R04, AXS-R17.
- Question: PMT-Q01.
- Decisions: D12, D13, D14, D18, D19, D20, D28.
- Diagrams: seq-book-pay, seq-lost-redirect. Related: ADR-0007, ADR-0019.

## Sources

- course site [extraction site] fetched 2026-09-30: E14, E15, E16, E17, E35.
- course site [syllabus site] fetched 2026-09-30: S63 "Teams communicate between services over REST."
- Project team (D12, D13).
