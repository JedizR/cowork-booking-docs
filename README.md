# Cowork Booking — docs

Business rules, glossary, product and architecture docs for Cowork Booking, a co-working room booking product built as three services:

| Context | Repo | Owns |
|---|---|---|
| Purchase | `cowork-booking-purchase` | members, spaces, availability, bookings, price, coverage, cancellation |
| Payment | `cowork-booking-payment` | hosted mock checkout, payment outcomes, refunds |
| Access | `cowork-booking-access` | access grants, e-tickets, check-in kiosk |

This repo is the single home for rules and decisions. Service contracts live beside each provider's code.

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
