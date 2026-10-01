# Cowork Booking — docs

Business rules, glossary, product and architecture docs for Cowork Booking, a co-working room booking product built as three services:

| Context | Repo | Owns |
|---|---|---|
| Purchase | `cowork-booking-purchase` | members, spaces, availability, bookings, price, coverage, cancellation |
| Payment | `cowork-booking-payment` | hosted mock checkout, payment outcomes, refunds |
| Access | `cowork-booking-access` | access grants, e-tickets, check-in kiosk |

This repo is the single home for rules and decisions. Service contracts live beside each provider's code.

## Run the whole system on your machine

Needs Docker. The four repos sit side by side in one folder (this repo builds the three services from its sibling folders).

```bash
git clone git@github.com:JedizR/cowork-booking-docs.git
git clone git@github.com:JedizR/cowork-booking-purchase.git
git clone git@github.com:JedizR/cowork-booking-payment.git
git clone git@github.com:JedizR/cowork-booking-access.git
cd cowork-booking-docs/integration
docker compose -f compose.yaml up -d --build --wait
```

| What | URL | Sign-in |
|---|---|---|
| Purchase: spaces, booking, My bookings, operator pages | http://localhost:8001 | Sign up as a Member; `operator@example.com` becomes the Operator on sign-up |
| Payment: hosted checkout `/pay/<id>`, operator totals `/operator` | http://localhost:8002 | `/operator`: HTTP Basic `operator` / `OPERATOR_PASSWORD` (dev default `dev-operator-password`) |
| Access: e-tickets `/t/<token>`, kiosk `/checkin` | http://localhost:8003 | `/checkin`: HTTP Basic `staff` / `STAFF_PASSWORD` (dev default `dev-staff-password`) |

Test cards on the hosted page (any future expiry, any CVC): `4242424242424242` succeeds, `4000000000000002` declines, `4000000000005126` succeeds but its first refund fails. The door lock is mocked: an `ok` at the kiosk means the scan was accepted, not that a door opened (ADR-0017).

Stop with `docker compose -f compose.yaml down` (add `-v` to wipe the data). The e2e suite and its test clock are described in [integration/README.md](integration/README.md).

## Documents

| Read this | For |
|---|---|
| [PRD.md](PRD.md) | Problem, roles, stories and acceptance criteria, UX flows |
| [RULES.md](RULES.md), [GLOSSARY.md](GLOSSARY.md) | Business rules and terms by context |
| [DECISIONS.md](DECISIONS.md), [adr/](adr/README.md) | D1-D28 and the architecture decisions |
| [ARCHITECTURE.md](ARCHITECTURE.md), [diagrams/](diagrams/) | Services, data ownership, calls, sequences |
| [BUSINESS_MODEL.md](BUSINESS_MODEL.md) | Commission model, metrics, three services vs a monolith |
| [contracts/README.md](contracts/README.md) | The three contracts (verified), held beside each provider |
| [TRACEABILITY.md](TRACEABILITY.md) | Every rule to its passing tests or manual check |
| [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md), [REVIEW_LOG.md](REVIEW_LOG.md), [ID_MAP.md](ID_MAP.md) | Open questions with defaults, review rounds, class-ID mapping |
| [design/DESIGN.md](design/DESIGN.md), [design/preview.html](design/preview.html) | The black-and-white design system (derived from an Apple design analysis) shared by the three services |
| [SOURCES.md](SOURCES.md), [inventory/](inventory/README.md) | Where everything came from |

## Checks

```bash
python3 scripts/check_docs.py
for f in diagrams/*.mmd; do npx -y @mermaid-js/mermaid-cli@11 -p diagrams/puppeteer.json -i "$f" -o "${f%.mmd}.svg"; done
```

## Doc formats

`scripts/check_docs.py` enforces these. Keep them exact.

- **IDs.** Terms `PUR-Tnn`, rules `PUR-Rnn`, questions `PUR-Qnn`; prefixes `PUR` (Purchase), `PMT` (Payment), `AXS` (Access). Terms are defined only in `GLOSSARY.md`, rules only in `RULES.md`, questions only in `OPEN_QUESTIONS.md`. Every ID is defined once; every reference resolves.
- **Glossary row.** `| ID | Term | Context | Meaning | Counterexample | Status / source |`. Status starts with a policy status.
- **Rule.** A heading `### PUR-Rnn <title>`, then a field table `| Field | Value |` with the rows Rule, Policy status, Decision source, Implementation evidence, Terms, Candidate responsibility and dependencies, Open question, Clarification owner, Next use, then an example table `| # | Kind | Channel | Given | When | Expected result under this rule |`. Kind is `ordinary`, `boundary` or `counterexample` (all three required). Channel is `JSON`, `form` or `internal`; JSON and form outcomes get separate rows.
- **Policy status.** `Observed`, `Decided`, `Stakeholder-clarified` or `Superseded` (a superseded rule names its replacement rule ID).
- **Evidence.** `source inspected at <sha>`, `test run at <sha>`, or `live journey verified`. Never interchangeable.
- **Open question.** A heading `### PUR-Qnn <title>` whose body states the default that applies.
- **Decisions.** `| D# | Topic | Decision | Status | Rationale |`, D1–D28, Status `Decided`.
- **ID map.** `| Class ID | Class meaning / source | New ID | Disposition | Reason |`, every class ID from `inventory/class-ids.md` exactly once; disposition `kept`, `merged`, `superseded` or `rejected`.
- **ADRs.** `adr/NNNN-<slug>.md`, cited as `ADR-NNNN`.
- **PRD.** Acceptance criteria are bullets `- AC<story>.<n> …` and each cites a rule ID. Every rule appears in the PRD.
- **Contracts index.** `| Contract | Provider | Consumer | Link | State | Evidence |`, State `proposed`, `agreed` or `verified`.
- **Traceability.** `| Rule | Status | Evidence |`. Decided and Stakeholder-clarified rules cite test node IDs `` `e2e:e2e/test_x.py::test_y` `` (report `purchase`, `payment`, `access` or `e2e`, checked against `integration/reports/<report>.xml`) or `manual: <steps + result>`. Observed and Superseded rules cite the replacing rule ID or `out of scope (ADR-NNNN)`.
- **Diagrams.** Mermaid sources in `diagrams/*.mmd`, rendered to `.svg`. Every diagram has the three boxes Purchase, Payment, Access; only Member, Operator, Staff and Browser sit outside them.
