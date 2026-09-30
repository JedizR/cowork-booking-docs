# Business model

Cowork Booking is a marketplace for co-working rooms. Members book a whole room in 30-minute blocks, pay on a hosted checkout, and get an e-ticket for the door. The platform earns a commission on the money it keeps after refunds.

Status: draft (M2), 2026-10-01. Every figure below uses the shared example data: clock 2026-10-05 10:00 Bangkok; Meeting Room A (THB 300 per hour), Focus Pod 1 (THB 20 per hour), Board Room (THB 1,000 per hour), Community Table (free); standard booking BK-7KQ2M9, Member A, Meeting Room A, 2026-10-07 09:00-10:30, 3 blocks, party 4, THB 450.00.

## 1. Value

### For Members

- See which start blocks are free, and why the others are not, before you commit (PUR-R13).
- See the price before you pay. It is fixed at creation and never changes (PUR-R17). Example: BK-7KQ2M9 costs THB 450.00, even if the rate later rises.
- Pay on a hosted page. Only the card brand and last4 are stored (PMT-R13).
- Plan and free bookings are confirmed at once, with no card (PUR-R20).
- Get one e-ticket with one code, H7K3-9QXA, shown as text and as a QR (AXS-R05, AXS-R07).
- See the refund before you confirm a cancel (PUR-R30).

### For space hosts

- The room is never double-booked (PUR-R22). An unpaid hold frees the slot after 15 minutes (PUR-R21, PUR-R24).
- The price is agreed once and stored (PUR-R17). Payment never re-prices it (PMT-R04).
- The door opens only for the right room inside the booked time (AXS-R13, AXS-R14).
- Nothing is deleted. Cancelled and expired bookings stay on record (PUR-R28). A retired room is archived with its history (PUR-R16).

### For the platform

- A commission of 20% of net collected (D25; section 3).
- One record per fact: the booking in Purchase, the money in Payment, the grant in Access (PUR-R35, PMT-R18, AXS-R04).
- Operator metrics for bookings (PUR-R34) and money (PMT-R17).

## 2. Customers and segments

| Segment | Example | Coverage | Money collected | Rules |
|---|---|---|---|---|
| Pay-as-you-go Member | Member A (a@example.com) books Meeting Room A | pay | yes, through Payment | PUR-R19, PUR-R23 |
| Plan Member | Member B (b@example.com), plan_active set by the Operator | plan | no | PUR-R19, PUR-R20, PUR-Q02 |
| Free-space user | any Member booking the Community Table | free | no | PUR-R19, PUR-R20 |
| Space host | the owner of Meeting Room A; no account in v1, the Operator lists and edits the room | none | no payout in v1 | PUR-R15, PUR-R16, PMT-Q04 |

By room type: meeting and board rooms serve teams (party size up to capacity, PUR-R14); focus pods serve one or two people; the free Community Table brings Members in.

Internal users are not customers: the Operator runs Purchase and reads Payment's operator page (PUR-R06, PMT-R17); Staff run the check-in kiosk (AXS-R11).

## 3. Revenue

The platform is a marketplace. The source of the model is class issue #173:

> "[The platform] is a marketplace that lists spaces owned by others and earns a commission on bookings (e.g. 20% of each booking, like Booking.com's model)." (class issue #173 discussion)

We take 20% of **net collected**, not of each booking (D25). Plan and free bookings collect nothing, and refunded money is not revenue.

Formulas, as on Payment's operator page (PMT-R17):

- Collected = the sum of amount_satang over paid sessions (PMT-T13).
- Refunded = the sum of succeeded refunds (PMT-T14). A failed refund adds nothing.
- Net = collected minus refunded.
- Estimated platform commission = 20% of net, rounded half up to the satang (PMT-T16).

Host payouts are out of scope (D25). The commission is a figure on the operator page, never a transfer (PMT-Q04).

### Worked example: the standard booking and its refunds

Member A books BK-7KQ2M9 for THB 450.00 (amount_satang 45000) and pays with 4242424242424242. The rows below are alternatives, one per cancel case.

| Case | Refund | Collected | Refunded | Net | Commission |
|---|---|---|---|---|---|
| Paid, not cancelled | none | THB 450.00 | THB 0.00 | THB 450.00 | THB 90.00 |
| Member A cancels 2026-10-05 12:00 (45 h before start) | 100% (PUR-R30) | THB 450.00 | THB 450.00 | THB 0.00 | THB 0.00 |
| Member A cancels 2026-10-06 09:01 (under 24 h) | 0% (PUR-R30) | THB 450.00 | THB 0.00 | THB 450.00 | THB 90.00 |
| Operator cancels 2026-10-07 09:30 (before end) | 100% (PUR-R30) | THB 450.00 | THB 450.00 | THB 0.00 | THB 0.00 |
| Paid with 4000000000005126; Operator cancels; attempt 1 fails | 100%, failed (PMT-R16) | THB 450.00 | THB 0.00 | THB 450.00 | THB 90.00, "needs manual follow-up" |
| Same; the Operator's Retry sends attempt 2, it succeeds | 100% (PUR-R33) | THB 450.00 | THB 450.00 | THB 0.00 | THB 0.00 |

A full refund takes the commission back to THB 0.00. The refund is sent only after the grant is revoked (PUR-R32), and it never exceeds the amount collected (PMT-R15). While a refund stays failed, net and commission read too high: that is why the failed refund is listed for the Operator.

### Plan and free bookings are bookings, never revenue

The [extraction site] says it plainly: "“Covered” is not always “money collected”."

- Member B (plan) books Board Room 2026-10-06 13:00-15:00. The booking stores THB 2,000.00 (PUR-R19), is confirmed at once and never reaches Payment (PUR-R20). It adds one confirmed booking and 2 hours of utilization, and THB 0.00 of revenue (D24, PUR-R34).
- Member A books the Community Table: coverage free, price THB 0.00, no Payment call (PUR-R20).
- Neither appears in Payment's totals (PMT-R17).

## 4. Costs

| Cost | What drives it | v1 approach | Rules and decisions |
|---|---|---|---|
| Hosting | three services and three PostgreSQL 16 databases, 2 gunicorn workers each | one image and one compose file per service; no registry, no Nomad | D26, D28, ADR-0003, ADR-0011, ADR-0015 |
| Card fees | a real provider's fee per charge and refund | none: the checkout is a mock, no real money | ADR-0018, PMT-Q01 |
| Failed refunds | each failed refund needs a person | listed as "needs manual follow-up"; only the Operator starts attempt+1 | PMT-R17, PUR-R33, PMT-Q02 |
| Pending calls | Payment or Access did not answer | "refund pending", "revocation pending", "being prepared"; retried on the booking page or by Retry | PUR-R26, PUR-R32, PUR-Q12 |
| Operator time | rooms, plans, cancels, reconcile, reading two dashboards | manual screens in Purchase and Payment | PUR-R06, PUR-R16, PUR-R24, PUR-R30, D24 |
| Staff time | a person at the kiosk | one shared kiosk login per room | AXS-R11 |
| Change cost | a cross-service change touches up to three repos and two contracts | contracts beside the provider, proposed then agreed then verified | ADR-0005 |

## 5. Metrics

Bookings live in Purchase (GET /dashboard, Operator only). Money lives in Payment (GET /operator, HTTP Basic, ADR-0019). The Operator reads both (D24).

| Metric | Definition | Where | Rules and decisions | Example |
|---|---|---|---|---|
| Bookings by status | count of held, confirmed, expired and cancelled bookings in the last 7 Bangkok days, by start; Completed is derived, not a status | Purchase dashboard | PUR-R34, PUR-R28, PUR-Q11, D24 | clock 2026-10-08 10:00: confirmed 2, expired 1 |
| Utilization | confirmed booked hours ÷ (12 h × non-archived spaces × 7); plan and free hours count; shown as a percent with one decimal, rounded half up | Purchase dashboard | PUR-R34, PUR-T32, D24 | 4 spaces give 336 hours; BK-7KQ2M9 (1.5 h) plus a Member B plan booking (2 h) = 3.5 ÷ 336 = 1.0%; 42 ÷ 336 = 12.5% |
| Members | accounts with at least one confirmed booking in the period | Purchase dashboard | PUR-R34, PUR-T31, D24 | Member A with two bookings counts once |
| Collected, refunded, net, commission | the formulas in section 3; all-time totals | Payment operator page | PMT-R17, PMT-T16, PMT-Q03, D25 | collected THB 1,450.00, refunded THB 450.00, net THB 1,000.00, commission THB 200.00 |
| Failed refunds needing follow-up | failed refunds with no later succeeded attempt for the same session | Payment operator page | PMT-R17, PMT-T15, PUR-R33, PMT-Q02 | the attempt-1 refund of BK-3HT8WD shows "needs manual follow-up" until attempt 2 succeeds |

The Purchase dashboard shows no money (PUR-R34). A plan booking adds a booking, never THB 2,000.00 of revenue.

## 6. Unit economics example

Per standard booking (Meeting Room A, 3 blocks, pay):

- The Member pays THB 450.00.
- The platform's commission is THB 90.00.
- THB 360.00 is the host's share on paper. v1 pays nothing out (PMT-Q04).
- Card fees are THB 0.00, because the checkout is a mock (ADR-0018).

Commission per paid hour: Meeting Room A THB 60.00, Focus Pod 1 THB 4.00, Board Room THB 200.00, Community Table THB 0.00.

Per week, 4 rooms give 336 bookable hours (D24). If every hour were paid and never refunded, the ceiling is 84 hours × (THB 300 + THB 20 + THB 1,000) × 20% = THB 22,176.00 of commission a week.

Break-even utilization = weekly cost ÷ THB 22,176.00, for an all-pay mix spread evenly over the four rooms. Example: if hosting and Operator time cost THB 2,772.00 a week (an assumption for this example, not a measured figure), break-even is 12.5% utilization, or about 31 standard bookings a week.

Three things move the result:

- Plan and free hours raise utilization and add THB 0.00. An hour of Meeting Room A under a plan gives up as much as THB 60.00 of commission when the room would otherwise sell (PUR-R19).
- A refund of 100% (24 h or more before start, or any Operator cancel) takes the commission to THB 0.00, but the hosting and Operator time are already spent (PUR-R30).
- Each failed refund costs Operator time for a retry (PUR-R33).

## 7. Risks

| Risk | Effect | Default in v1 | Rules, questions, ADRs |
|---|---|---|---|
| Commission is an estimate with no host payouts | hosts cannot see or receive their share | display only | D25, PMT-Q04 |
| Plans are unpriced and set by hand | plan hours use rooms and earn nothing | no plan sales | D10, PUR-Q02 |
| 0% refund under 24 h | Members may complain; every Operator cancel refunds 100% and gives up the commission | policy fixed at 100% or 0% | PUR-R30, PUR-Q03 |
| A failed refund stays failed | net and commission read too high until attempt 2 succeeds | Operator follow-up | PMT-R17, PUR-R33, PMT-Q02 |
| Mock payment and mock lock | no real money moves; a stored grant is not proof a door opened | mocked by design | ADR-0017, ADR-0018, PUR-Q06, AXS-Q02 |
| Abandoned checkouts | a held slot is unsellable for up to 15 minutes | lazy expiry on the next touch | PUR-R21, PUR-R24, ADR-0007 |
| Revoke pending while the slot is rebooked | the old code can still open the room | visible pending state; refund waits for the revoke | PUR-R32, PUR-Q12 |
| Utilization read as revenue | a busy dashboard can hide low income | money shown only on Payment's page | PUR-R34, D24 |
| Three services cost more to run and change | more hosting, more coordination | accepted as the course exercise | ADR-0001, section 8 |

## 8. Three services vs modules in a monolith

The course asks us to compare the split with a monolith. Here is the same product both ways.

| Aspect | Three services (this project) | Modules in one monolith |
|---|---|---|
| Deployment | three images, three compose files; each service deploys and rolls back alone (D26, ADR-0011) | one image, one deploy; a bad change in any module rolls back the whole app |
| Data ownership | a database per service; no service reads another's database; shared references such as booking_reference, never foreign keys (ADR-0003, PUR-R35) | one database; ownership is a code-review convention; a join across modules is one line away |
| Failure modes | partial failure: Payment down gives "try again" (PUR-R31); Access down gives "being prepared" or "revocation pending" (PUR-R26, PUR-R32); a lost redirect waits for reconciliation (ADR-0007) | up or down as a whole; no timeouts between modules |
| Consistency | eventual: reconcile on touch, natural-key idempotency, stored follow-up fields (ADR-0014, PUR-R24) | one transaction can confirm the booking, record the payment and issue the grant together |
| Team autonomy | one repo per team; contracts beside the provider, proposed then agreed then verified (ADR-0005) | one repo, one main branch; module boundaries by convention |
| Cost | three services, three databases, six gunicorn workers, three CI pipelines (ADR-0015) | one service, one database, one CI pipeline |
| Testability | unit tests per service with stubbed clients, plus an e2e stack that sets one test clock on three services (ADR-0013) | one pytest run against one database covers the whole journey |
| Change effort for cancellation | policy and orchestration in Purchase (PUR-R30, PUR-R31, PUR-R32, PUR-R33), refunds in Payment (PMT-R14, PMT-R15, PMT-R16), revoke in Access (AXS-R17); two contracts; three deploys, provider first | one PR; status, refund record and revoke in one transaction; only the card provider stays outside |

What the split does buy: card data stays inside Payment (ADR-0020), a slow Access never blocks a payment, and each team can deploy on its own.

### Conclusion

The three services are the course exercise, not a recommendation for this business. The syllabus says so: "Three services are the course exercise, not a claim that every growing business should split its application; students compare the costs and benefits with alternative boundaries and modules within a monolith." ([syllabus site])

For four rooms and one Operator, modules in one monolith would be cheaper to run, simpler to keep consistent, and faster to change. The course's own path goes through "Separate ownership, still one monolith" ([extraction site]); this project goes straight to three repos (ADR-0006). We split to practise contracts, independent delivery and a cross-service change. Split for real only when separate teams, separate release cycles or a separate card-data boundary pay for the extra cost. The decision and its alternatives are in ADR-0001.

## Sources

- Commission: class issue #173 discussion (fetched 2026-10-01); D25.
- Metrics: D24; PUR-R34; PMT-R17.
- "“Covered” is not always “money collected”." and "Separate ownership, still one monolith": [extraction site], fetched 2026-09-30.
- "Three services are the course exercise ...": [syllabus site], fetched 2026-09-30.
