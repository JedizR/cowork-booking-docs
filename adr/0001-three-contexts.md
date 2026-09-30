# ADR-0001 Three contexts, three services

## Status

Accepted, 2026-10-01

## Context

Example: Member A books Meeting Room A on 2026-10-07 09:00-10:30 (BK-7KQ2M9, THB 450.00). Three questions follow, and each has one owner:

- What is the price, and is it covered? Purchase.
- Did we collect THB 450.00? Payment.
- May the holder of H7K3-9QXA enter Meeting Room A now? Access.

In the seed one app and one booking row answer all three. The [extraction site] "Today" view shows it: "Booking record": "price · paid · card_last4" / "Access code: generated, not saved", with "Payments": "Changes booking.paid" and "Access": "Reads booking.paid". Seed flaws F4 (code never stored), F5 (cancel deletes the revenue) and F6 (coverage stored as paid) come from that sharing (source inspected at 5a1cf3d).

The course target splits ownership: Purchase "Owns price and coverage", Payments "Owns payment outcomes", Access "Owns grants and issuance" [extraction site]. [contexts site]: "Shared references connect the models. They do not make them one shared object." [syllabus site]: "Students work in three teams, one for each bounded context: Purchase, Payments, and Integrations/Locks." and "Teams communicate between services over REST."

The syllabus also warns: "Three services are the course exercise, not a claim that every growing business should split its application; students compare the costs and benefits with alternative boundaries and modules within a monolith." [syllabus site]. So compare, and say plainly what the split costs.

## Decision

- Build three bounded contexts, each its own service, repo and database: Purchase (`cowork-booking-purchase`, port 8001), Payment (`cowork-booking-payment`, 8002), Access (`cowork-booking-access`, 8003).
- Purchase owns members, spaces, availability, bookings, price, coverage and cancellation. Payment owns payment sessions, attempts and refunds. Access owns grants, ticket codes, scans and the kiosk.
- Connect them by shared references only: `booking_reference` (BK-7KQ2M9), `payment_session_id` (ps_...), `grant_id` (gr_...), `member_ref`. No shared object, no shared table (ADR-0003).
- Add no fourth context. Account data stays on Member in Purchase (ADR-0002).
- Write "Payment" and "Access". The course writes "Payments" and "Integrations/Locks" (PMT-T01, AXS-T01).

Three services against modules in one monolith:

| Concern | Three services (chosen) | Modules in one monolith |
|---|---|---|
| Ownership | One repo, database and deploy per team | One package per team, one repo, one deploy |
| Calls | HTTP/JSON, bearer token, timeout=5; a call can fail | In-process calls; no timeout, no 503 |
| Consistency | Reconciliation across databases (D13) and stored pending states (D19) | One transaction can cover booking, payment and grant |
| Deploy and rollback | Per service (D26) | All or nothing |
| Tests | Unit tests per service plus an e2e stack of 3 apps and 3 databases | One pytest run |
| Running cost | 3 images, 3 databases, 2 API tokens, 2 contracts | Lowest |

## Consequences

- Good: each rule has one home. Payment cannot re-price (PMT-R04). Revoking a grant never refunds (AXS-R17). Coverage never looks like money (PUR-R19).
- Good: each service ships and rolls back alone, which the course grades ("Service delivered, independently deployable" [syllabus site]).
- Bad: failure modes a monolith never has. A grant can be "being prepared" (PUR-R26), a revoke or refund can be pending (PUR-R32), and a cancel can get 503 while Payment is down (PUR-R31).
- Bad: more code: two HTTP clients, two contracts, an e2e stack, three copies of the shared look. For a v1 business this size, modules in one monolith would be simpler. We split because the course exercise is the split.

## Alternatives considered

- **Modules in one monolith** ("Separate ownership, still one monolith" [extraction site]). Cheapest, one transaction. Not chosen: the exercise and the grading ask for three independently deployable services. It stays the fallback: `payment_client.py` and `access_client.py` are the only seams, so merging back is a local change.
- **Two services** (Access inside Purchase). The credential rules (AXS-R05, AXS-R14) would sit beside booking code again, as in the seed.
- **Four contexts with Identity.** See ADR-0002.

## Rules and decisions

- Rules: PUR-R17, PUR-R19, PUR-R26, PUR-R29, PUR-R32, PUR-R35, PMT-R04, PMT-R18, AXS-R04, AXS-R17.
- Terms: PUR-T33, PMT-T01, AXS-T01.
- Decisions: D8, D10, D13, D19, D20, D24, D26.
- Related: ADR-0002, ADR-0003, ADR-0004.

## Sources

- course site [extraction site] fetched 2026-09-30: statements E07, E08, E11 in inventory/course-statements.md.
- course site [contexts site] fetched 2026-09-30: C03, C12.
- course site [syllabus site] fetched 2026-09-30: S61, S62, S63, S76.
- Spacey main 5a1cf3d, seed flaws F4, F5, F6 (source inspected at 5a1cf3d).
- Project team (D13, D26).
