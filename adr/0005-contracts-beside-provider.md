# ADR-0005 Contracts live beside the provider's code

## Status

Accepted, 2026-10-01

## Context

Example: Purchase relies on this promise: "POST /payment-sessions for BK-7KQ2M9 with amount_satang 45000, sent twice, returns the same ps_ session with 200; sent with 40000, it gets 409". The promise is Payment's to keep (PMT-R03). So it lives in `cowork-booking-payment`, beside the code and tests that keep it.

The course says where: "Where does the contract live?" / "Beside the provider’s code. Agreed with its consumer." and "Payments keeps Payments. / Access keeps Access." [extraction site]. It asks for "Add OpenAPI for HTTP": "Operations and schemas, linked to behavioural promises." and "One authoritative copy—not two drifting copies." It names the states: "Provider maintains it. Consumer reviews it. Proposed, agreed and verified are different states." It names the examples: "Success, invalid input, failure, repeat; coverage skips collection." [extraction site].

The seed has one `openapi.yaml` (732 lines, 18 operations, OpenAPI 3.0.3) for the whole app (source inspected at 5a1cf3d), from the syllabus requirement for "a version-controlled minimal OpenAPI contract" [syllabus site].

## Decision

- Keep one authoritative copy of each contract, in the provider's repo:
  - purchase→payment: `CONTRACT.md` and `openapi.yaml` in `cowork-booking-payment`.
  - purchase→access: `CONTRACT.md` and `openapi.yaml` in `cowork-booking-access`.
  - Purchase's own browser and JSON API: `openapi.yaml` in `cowork-booking-purchase`.
- Keep links only in the docs repo: `contracts/README.md`, one row per contract. The M2 drafts sit in the docs repo until M4 moves them; after the move the docs repo holds no copy.
- Write promises and examples, and link rule IDs. Meaning stays in RULES.md. Every contract has the five course examples: success, invalid input, failure, repeat, coverage skips collection.
- Move a contract through three states, and let nothing else change a state:
  - proposed: the M2 draft;
  - agreed: a consumer-lens reviewer signs off in REVIEW_LOG.md, and the provider repo is tagged `contract-v1`;
  - verified: the M6 e2e run is cited.
- Stub providers in consumer tests at one boundary (`payment_client.py`, `access_client.py`), using the contract examples. Those tests are evidence toward verified; they do not change the state.
- Change a contract in this order: the consumer asks, rules and glossary change first if meaning changed, then the provider's contract, then a `contract-v2` tag, then both sides implement.

## Consequences

- Good: one place to read each promise, next to the code and tests that keep it.
- Good: the state tells a reader how far to trust it.
- Bad: a consumer reads a document in another repo, and cross-repo links can break. The index row carries the link and the state.
- Bad: a rule change touches two repos in a fixed order, which is slower than editing one file.

## Alternatives considered

- **Central contracts in the docs repo.** Rejected: they drift from the code; "One authoritative copy—not two drifting copies." [extraction site].
- **Consumer-driven contract tests** (a Pact-style broker). New tooling and a new service; not in the stack.
- **A shared schema package.** Couples the release of three services.

## Rules and decisions

- Rules: PUR-R23, PUR-R26, PUR-R35, PMT-R01, PMT-R02, PMT-R03, PMT-R06, PMT-R14, AXS-R01, AXS-R02, AXS-R03, AXS-R04, AXS-R17.
- Decisions: D12, D14, D20, D26.
- Related: ADR-0004, ADR-0014, ADR-0019.

## Sources

- course site [extraction site] fetched 2026-09-30: E25, E29, E30, E31, E40, E41.
- course site [syllabus site] fetched 2026-09-30: S109.
- Spacey main 5a1cf3d: `openapi.yaml` (source inspected at 5a1cf3d).
- Project team (D26).
