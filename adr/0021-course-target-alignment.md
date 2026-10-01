# ADR-0021 Alignment with the course's "ready for splitting" target

Status: Accepted, 2026-10-01

## Context

The course published a journey page ([journey site], fetched 2026-10-01) with two views of one successful, non-subscription booking:

- "1 · EXISTING STATE": "The application does everything". "Payment state lives on booking. Access code is not saved."
- "2 · PROPOSED, READY FOR SPLITTING": "Each responsibility has an owner": Purchase ("Booking, price, eligibility"), Payments ("Mock collection, payment records"), Access ("Mock issuance, grant records"). "Still one application. Ordinary function calls, explicit inputs/results, owned data access. Separate services and deployment cycles come next." Its sequence: Member books; Purchase saves the booking and agreed price; Member pays; Purchase asks Payments to "Collect agreed amount for booking reference"; Payments saves the outcome and returns "Payment reference and outcome"; Purchase updates booking eligibility; Member asks for the code; Purchase checks eligibility and sends an "Authorised issuance request"; Access saves the grant and returns "Grant reference and code"; Purchase shows the code. "Each module owns its records. No reading another module's tables."
- "Ready means checked: ownership is enforced, migrations preserve known facts, and the existing journey plus failure/retry cases still work."

## Decision

Keep our design. It realises the target's ownership and call direction and takes its stated next step (separate services, REST, independent releases). Record the deliberate differences:

| Target step | Cowork Booking | Why |
|---|---|---|
| Purchase coordinates; only Purchase calls the others | Same (ADR-0004) | Course target |
| Purchase saves booking and agreed price | Same (PUR-R17, D8) | Stakeholder-clarified price rule |
| Member pays through Purchase; Purchase sends mock payment details to Payments | Member pays on Payment's hosted checkout; Purchase sends booking reference, agreed amount and currency only (PMT-R02, PUR-R23) | Hosted checkout (ADR-0018): card details never pass through Purchase (ADR-0020) |
| Payments returns payment reference and outcome; Purchase updates eligibility | Purchase reads the session (GET /payment-sessions/{id}) and confirms only on a full match (PUR-R25, D14); reconciliation covers a lost answer (PUR-R24, ADR-0007) | Same meaning; the read also recovers a recorded payment whose booking update failed |
| Code issued when the Member asks for it | Grant requested at confirmation (PUR-R26, D20); the code is reused for the same grant (AXS-R05) | The grant meaning was agreed before implementation, as the target asks |
| Purchase shows the code | The booking page shows the code read live from Access (PUR-R41) and links the Access e-ticket (AXS-R09) | No copy of Access data in Purchase (ADR-0003) |
| Subscription coverage bypasses a new payment | Plan and free bookings skip Payment (PUR-R20) | Course target |
| Still one deployment | Three services, three repos, database per service (ADR-0001, ADR-0003) | The target's "next" step, taken directly (ADR-0006) |
| Migrations preserve known facts | No data is migrated; each service starts with an empty database (ADR-0006, PUR-Q07). Nothing historical is invented | No production data to keep |

## Consequences

- Good: the journey and its failure and retry cases are covered by the e2e suite (TRACEABILITY.md); ownership is enforced by separate databases, not by convention.
- Bad: the hosted checkout adds one browser redirect the target does not have; the booking page makes one extra read from Access per view.

## Alternatives considered

- Pay through Purchase as in the target: rejected; card data would cross Purchase, against ADR-0020 and BRIEF-mandated hosted checkout.
- Issue the code only on request: rejected; D20 issues at confirmation so the e-ticket is ready, and AXS-R05 makes repeat views reuse the same code.

## Rules and decisions

PUR-R17, PUR-R20, PUR-R23, PUR-R24, PUR-R25, PUR-R26, PUR-R41, PMT-R02, AXS-R05, AXS-R09; D8, D13, D14, D20.

## Sources

[journey site] (course journey page and its extraction studio page, fetched 2026-10-01; see SOURCES.md).
