# ADR-0014 Natural keys make repeats safe; no Idempotency-Key header

## Status

Accepted, 2026-10-01

## Context

Example: Purchase sends POST /payment-sessions for BK-7KQ2M9 (amount_satang 45000). Payment stores the session, but the answer is lost and Purchase times out after 5 s. Member A presses "Continue to payment" again. Purchase resumes the same held booking and repeats the call. Payment finds BK-7KQ2M9, sees the same amount and currency, and returns the same ps_ session with 200. One session, one charge.

- The course: "What if repeated?": "Reuse or new attempt? Agree identity and behaviour; do not assume." and "Which examples?": "Success, invalid input, failure, repeat; coverage skips collection." [extraction site]. For access: "Proposed policy: reuse the credential for the same valid grant." [extraction site].
- Every provider call can time out after the provider did the work (timeout=5, D28).
- Stripe-style APIs take an `Idempotency-Key` header and store each key with its first response.
- The seed has no idempotency: two pays can both pass the check (seed flaw F14, app.py:940-965), and each unlock returns a new code (F4, app.py:970-985). Source inspected at 5a1cf3d.

## Decision

Use the business key each call already carries. Enforce each one with a database UNIQUE constraint, not only an app check.

- **Payment session:** `booking_reference` is unique. A repeat with the same amount_satang and currency returns the existing session with 200, whatever its status. A different amount gets 409 and changes nothing (PMT-R03).
- **Refund:** `(payment_session_id, attempt)` is unique. A repeat returns the stored refund with 200, even a failed one. A new try is a new attempt number, and after a stored failure only the Operator starts attempt+1 (PMT-R14, PUR-R33).
- **Grant:** `booking_reference` is unique. A repeat returns the stored grant and the same ticket code with 200. A revoked reference, or a revoked tombstone, answers status revoked and never issues (AXS-R01, AXS-R02).
- **Expire and revoke:** a repeat returns the same final state (PMT-R06, AXS-R17).
- **Booking:** one held booking per Member; the same space and time resumes it (PUR-R21, PUR-R39). The booking reference is unique, and the partial EXCLUDE catches a race (PUR-R22, PUR-R29).
- Send no `Idempotency-Key` header.

## Consequences

- Good: repeats are safe across workers and restarts, because the key lives in the row.
- Good: no key store and no key expiry. Support can read the key: "BK-7KQ2M9 has one session".
- Good: double submit, repeated session create and repeated grant give no double charge and no double grant.
- Bad: a booking never gets a second payment session. After its session expires, the Member books again under a new reference.
- Bad: a repeat with other fields changed (description, URLs) silently returns the old session, by design (PMT-R03).
- Bad: Purchase must choose refund attempt numbers correctly; it stores the attempt on the booking.

## Alternatives considered

- **Idempotency-Key header with stored responses.** General, but each provider needs a key table with expiry, and Purchase must store keys too. It adds nothing when every call already names one business fact.
- **No idempotency.** The seed's state; risks a double charge.
- **Exactly-once delivery through a broker.** Not in the pinned stack.

## Rules and decisions

- Rules: PUR-R21, PUR-R22, PUR-R29, PUR-R33, PUR-R39, PMT-R03, PMT-R06, PMT-R12, PMT-R14, PMT-R15, AXS-R01, AXS-R02, AXS-R05, AXS-R17.
- Decisions: D11, D14, D19, D20, D22, D28.
- Related: ADR-0004, ADR-0005.

## Sources

- course site [extraction site] fetched 2026-09-30: E39, E40, E45.
- Spacey main 5a1cf3d: seed flaws F14 and F4 (source inspected at 5a1cf3d).
- Project team (D11, D19, D20).
