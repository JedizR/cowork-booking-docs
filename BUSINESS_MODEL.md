# Business model

Cowork Booking is a marketplace for co-working rooms. Members book a whole room in 30-minute blocks, pay on a hosted checkout, and get an e-ticket for the door. The platform earns a commission on the money it keeps after refunds. The rooms belong to hosts; who pays the Staff at each room door, the platform or the host, is an open question (PMT-Q04). The default below: the platform staffs Meeting Room A and Board Room, and Focus Pod 1 is sold only when its host staffs its door (section 6).

Status: draft (M2), 2026-10-01. The figures use the shared example data, except where a row names its own scenario: the section 3 plan example and the section 5 dashboard rows follow PUR-R34 row 1 (a Member B plan booking of Board Room 2026-10-06 13:00-15:00, 2 h, and one expired Member C booking; BK-3HT8WD is not in it), and the section 5 money row follows PMT-R17 row 1 (BK-7KQ2M9 refunded in full). The shared example data: clock 2026-10-05 10:00 Bangkok; Meeting Room A (THB 300 per hour), Focus Pod 1 (THB 20 per hour), Board Room (THB 1,000 per hour), Community Table (free); standard booking BK-7KQ2M9, Member A, Meeting Room A, 2026-10-07 09:00-10:30, 3 blocks, party 4, THB 450.00; BK-3HT8WD, Member C, Board Room 2026-10-07, 2 blocks, THB 1,000.00, paid with test card 4000000000005126, later cancelled, refund attempt 1 failed. Every THB cost figure is an assumption for the example, not a measured figure.

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
- Check-in accepts a code only for its room and its window (AXS-R13, AXS-R14). The lock is mocked, and while a revoke is pending the old code still passes (PUR-Q12).
- Nothing is deleted. Cancelled and expired bookings stay on record (PUR-R28). A retired room is archived with its history (PUR-R16).

### For the platform

- A commission of 20% of net collected (D25; section 3).
- One owner per fact: the booking in Purchase, the money in Payment, the grant in Access (PUR-R35, PMT-R18, AXS-R04). Purchase keeps follow-up copies of the answers it got (PUR-T34), which can lag behind Payment while a refund is pending.
- Operator metrics for bookings (PUR-R34) and money (PMT-R17).

## 2. Customers and segments

| Segment | Example | Coverage | Money collected | Rules |
|---|---|---|---|---|
| Pay-as-you-go Member | Member A (a@example.com) books Meeting Room A | pay | yes, through Payment | PUR-R19, PUR-R23 |
| Plan Member | Member B (b@example.com), plan_active set by the Operator | plan | no | PUR-R19, PUR-R20, PUR-Q02 |
| Free-space user | any Member booking the Community Table | free | no | PUR-R19, PUR-R20 |
| Space host | the owner of Meeting Room A; no account in v1, the Operator lists and edits the room; staffs its own door under option (e) of PMT-Q04, and by default for Focus Pod 1 (section 6) | none | no payout in v1 | PUR-R15, PUR-R16, PMT-Q04 |

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

A full refund takes the commission back to THB 0.00. The refund is sent only after the grant is revoked (PUR-R32), and it never exceeds the amount collected (PMT-R15).

Three cases make net and commission read too high: two refunds still owed, and refunds settled outside the system:

- A failed refund. Payment lists it "needs manual follow-up" (PMT-R17, PUR-R33).
- A pending refund: one that waits for its revoke (PUR-Q10), which Payment has not received, or one that got no answer from Payment (refund_status pending, PUR-T34), which Payment may or may not have stored (PMT-R14, PUR-R33 row 8). Only Purchase's all-bookings list flags it, as "Refund pending" (with "Revocation pending" while it waits for its revoke) and the time it was requested (PUR-R32). A refund that landed before its answer was lost is already in Payment's refunded total.
- A refund settled outside the system: a refund after the end (PRD section 5), or a failed refund the Operator pays by bank transfer. It never reaches Payment's refunded total, so net, commission and the weekly hand sum stay too high for good, and a failed refund paid that way keeps "Refund failed" and "needs manual follow-up". The Operator keeps a list of these, subtracts them from the weekly hand sum, and leaves them out of PRD target (2). PMT-Q02 option (b), a "settled outside" action with a totals line (reversal cost Low), is the fix once this happens.

Before reading commission, press Retry on every "Refund pending" row: a refund that already landed comes back as its stored result (PMT-R14) and its flag clears. Then clear both lists. Commission is also not earned until a booking ends: the figure includes bookings that have not started, and an Operator cancel can still refund 100% before the end (PUR-R30, PMT-Q04).

### Plan and free bookings are bookings, never revenue

The [extraction site] says it plainly: "“Covered” is not always “money collected”."

- Member B (plan) books Board Room 2026-10-06 13:00-15:00. The booking stores THB 2,000.00 (PUR-R19), is confirmed at once and never reaches Payment (PUR-R20). It adds one confirmed booking and 2 hours of utilization, and THB 0.00 of revenue (D24, PUR-R34).
- Member A books the Community Table: coverage free, price THB 0.00, no Payment call (PUR-R20).
- Neither appears in Payment's totals (PMT-R17).

## 4. Costs

| Cost | What drives it | v1 approach | Assumed weekly figure | Rules and decisions |
|---|---|---|---|---|
| Hosting | three services and three PostgreSQL 16 databases, 2 gunicorn workers each | one image and one compose file per service; no registry, no Nomad | THB 272.00 for all three (assumption) | D26, D28, ADR-0003, ADR-0011, ADR-0015 |
| Card fees | a real provider's fee per charge and refund | none: the checkout is a mock, no real money | THB 0.00 | ADR-0018, PMT-Q01 |
| Failed refunds | each failed refund needs a person | listed as "needs manual follow-up"; only the Operator starts attempt+1 | in Operator time | PMT-R17, PUR-R33, PMT-Q02 |
| Pending calls | Payment or Access did not answer | "refund pending", "revocation pending", "being prepared"; retried on the booking page (or GET /api/bookings/<ref>), by the owner's Retry or by the Operator's Retry | in Operator time | PUR-R26, PUR-R32, PUR-Q12 |
| Operator time | rooms, plans, cancels, reconcile, reading two dashboards; the routine: daily, open the all-bookings list and press Retry on each flagged row (v1 has no "Retry all pending", PUR-Q12 option (d); a pending revoke or refund moves only when its page is opened or someone presses Retry); weekly, sum commission by hand (PMT-Q03) and scan upcoming plan and free rows for hoarding (PUR-Q15; the closure Member's rows are not hoarding, section 5); on call by phone through all 84 opening hours, because only the Operator can cancel or refund a started booking (PUR-R30) and door Staff have no Purchase account (AXS-R11), so door Staff phone the Operator | manual screens in Purchase and Payment; a phone at each staffed door | 10 h at THB 250.00 = THB 2,500.00, plus an on-call allowance of THB 1,000.00 for the opening hours: THB 3,500.00 (assumption) | PUR-R06, PUR-R16, PUR-R24, PUR-R30, PUR-R32, D24 |
| Staff time | a person at each staffed room door for the whole opening day, because the lock is a mock and a kiosk checks scans against one selected room (AXS-R11, wrong_room) | one kiosk and one Staff member per room door; one shared STAFF_PASSWORD. Assumption (PMT-Q04 default): the platform runs the venue and pays the Staff at Meeting Room A and Board Room from its 20%; Focus Pod 1 is sold only when its host staffs its door from its 80% share, because its commission never covers a door (section 6); if each host staffs its own door, this row is THB 0.00 for the platform | 84 h at THB 50.00 = THB 4,200.00 per kiosk (assumption): THB 8,400.00 for Meeting Room A and Board Room (the default), THB 12,600.00 for the three paid rooms, THB 16,800.00 with the Community Table | AXS-R11, ADR-0017, AXS-Q02, PMT-Q04 |
| Change cost | a cross-service change touches up to three repos and two contracts | contracts beside the provider, proposed then agreed then verified | not counted | ADR-0005 |

With a real provider, the fee on a charge is usually kept when the charge is refunded, so a 100% refund would cost the platform that fee instead of taking the commission to THB 0.00 (PMT-Q01). A fixed per-charge fee would also exceed the THB 2.00 commission on a 1-block Focus Pod booking (THB 10.00), so D9's THB 10 minimum is a technical minimum, not an economic one: a minimum booking value or passing the fee on would be needed (PMT-Q01). D9 does not change.

## 5. Metrics

Bookings live in Purchase (GET /dashboard, Operator only). Money lives in Payment (GET /operator, HTTP Basic, ADR-0019). The Operator reads both (D24).

The booking figures use stored statuses: a lapsed hold counts as held until something reconciles it. Press "Reconcile all held" before reading them (PUR-R24, PUR-R34).

Closure bookings (PRD section 3, "Close a room for a day or for repairs") are confirmed plan bookings of a dedicated closure Member, display name "Room closed": they count as plan bookings, plan hours, utilization and one member. Subtract them by hand when reading the dashboard, and leave them out of the hoarding scan. Closures can be booked at most 30 days ahead (PUR-R10).

| Metric | Definition | Where | Rules and decisions | Example |
|---|---|---|---|---|
| Bookings by status | count of held, confirmed, expired and cancelled bookings in the last 7 Bangkok days, by start; Completed is derived, not a status | Purchase dashboard | PUR-R34, PUR-R28, PUR-Q11, D24 | clock 2026-10-08 10:00: confirmed 2, expired 1 |
| Utilization | confirmed booked hours in non-archived spaces ÷ (12 h × non-archived spaces × 7); plan and free hours count, Community Table hours included; shown as a percent with one decimal, rounded half up | Purchase dashboard | PUR-R34, PUR-T32, PUR-Q11, D24 | 4 spaces give 336 hours; BK-7KQ2M9 (1.5 h) plus a Member B plan booking (2 h) = 3.5 ÷ 336 = 1.0% |
| Confirmed hours by coverage | confirmed booked hours split into pay, plan and free: hours, not money, so allowed on the dashboard (D24) | Purchase dashboard | PUR-R34, PUR-Q08 | pay 1.5 h, plan 2 h, free 0 h |
| Members | accounts with at least one confirmed booking in the period | Purchase dashboard | PUR-R34, PUR-T31, D24 | Member A with two bookings counts once |
| Collected, refunded, net, commission | the formulas in section 3; all-time totals. v1 cannot show a weekly commission; the lists show paid_at and the refund's created_at, both written from clock.now(), so a week can be summed by hand on a cash basis: collected by paid_at in the week minus succeeded refunds by created_at in the week. Commission is not earned until a booking ends (section 3): cash differs from earned by every payment for a booking in a later week and every refund of a payment from an earlier week. Members pay up to 30 days ahead (PUR-R10), so cash leads use by up to 30 days; section 6 compares the cash figure with the weekly cost only in weeks that start 30 days or more after launch | Payment operator page | PMT-R17, PMT-T16, PMT-Q03, D25 | BK-7KQ2M9 refunded in full plus BK-3HT8WD with its refund failed: collected THB 1,450.00, refunded THB 450.00, net THB 1,000.00, commission THB 200.00 |
| Failed refunds needing follow-up | failed refunds with no later succeeded attempt for the same session | Payment operator page | PMT-R17, PMT-T15, PUR-R33, PMT-Q02 | the attempt-1 refund of BK-3HT8WD shows "needs manual follow-up" until attempt 2 succeeds |
| Refunds owed | bookings with refund_status pending or failed: the "Refund pending" and "Refund failed" flags, listed first, oldest "Refund requested" time (refund_requested_at) first. "Revocation pending" alone owes no money (a 0% Member cancel, or a plan or free cancel); a refund that waits for its revoke also shows "Refund pending". The amount owed on a flagged row is its refund_amount_satang: the price for a Member or Operator cancel, the collected amount for an amount_mismatch (PUR-R25). Press Retry on each "Refund pending" row first; then adjust only for rows still flagged whose data-booking-reference has no succeeded refund row on Payment's page: adjusted commission = Payment's commission minus 20% of those amounts | Purchase all-bookings list | PUR-R32, PUR-R33, PUR-T34, PMT-R14 | a cancel whose revoke got no answer shows "Revocation pending" and "Refund pending"; its THB 450.00 refund waits and Payment's page has no refund row for it, so adjusted commission is THB 90.00 below Payment's figure |

The Purchase dashboard shows no money (PUR-R34). A plan booking adds a booking, never THB 2,000.00 of revenue.

## 6. Unit economics example

Per standard booking (Meeting Room A, 3 blocks, pay):

- The Member pays THB 450.00.
- The platform's commission is THB 90.00.
- THB 360.00 is the host's share on paper. v1 pays nothing out (PMT-Q04), and no page shows the share per room: Payment's session list names no space, so the per-host split is a manual join of Payment's sessions with Purchase's all-bookings list by booking reference (PRD section 3).
- Card fees are THB 0.00, because the checkout is a mock (ADR-0018).

Commission per paid hour: Meeting Room A THB 60.00, Focus Pod 1 THB 4.00, Board Room THB 200.00. The Community Table never has a paid hour.

Per week the four rooms give 336 bookable hours (D24), but only 252 of them can be sold: 3 paid rooms × 84 hours. The Community Table's 84 hours earn nothing, and utilization counts them anyway. If every sellable hour were paid and never refunded, the ceiling is 84 hours × (THB 300 + THB 20 + THB 1,000) × 20% = THB 22,176.00 of commission a week.

Break-even is a commission figure: weekly net commission = weekly cost. The weekly costs are the assumptions of section 4: hosting THB 272.00 and Operator time THB 3,500.00 (the on-call allowance included) make THB 3,772.00 before any Staff. The staffing model is one kiosk and one Staff member at each sold room's door: a kiosk checks every scan against one selected room (AXS-R11), Staff are the person at the room door (PRD section 2), and a room without Staff cannot let anyone in while the lock is a mock. So the kiosks follow the rooms sold. Who pays that Staff is an assumption (PMT-Q04).

Each room against its own door, with all 84 hours sold and never refunded:

| Room | Best weekly commission | Door Staff | Contribution |
|---|---|---|---|
| Meeting Room A | THB 5,040.00 | THB 4,200.00 | +THB 840.00; covers its door only from 70 of 84 h (83%) |
| Focus Pod 1 | THB 336.00 | THB 4,200.00 | -THB 3,864.00 at best; never covers its door |
| Board Room | THB 16,800.00 | THB 4,200.00 | +THB 12,600.00; covers its door from 21 h |

So the platform never pays Staff at Focus Pod 1. The default: the platform staffs Meeting Room A and Board Room from its 20% (PMT-Q04 option (d)), and Focus Pod 1 is sold only when its host staffs its door from its 80% share (option (e) for that room); otherwise it is not sold. Its commission, at most THB 336.00 a week, then adds to the platform's figure at no Staff cost. The alternative is that each host staffs its own door, which leaves the platform only hosting and Operator time.

| Rooms sold (commission an hour) | Hosts staff their doors: THB 3,772.00 | Platform staffs each sold room |
|---|---|---|
| Meeting Room A only (THB 60.00; THB 90.00 a standard booking) | 42 standard bookings (63 h), 18.8% utilization | 1 kiosk, THB 7,972.00: not reachable; all 84 h give THB 5,040.00 |
| Board Room only (THB 200.00) | 19 h, 5.7% utilization | 1 kiosk, THB 7,972.00: 40 h of 84 (48%), 11.9% utilization |
| Board Room and Meeting Room A equally (THB 260.00 for one hour of each) | 15 h in each room, 8.9% utilization | 2 kiosks, THB 12,172.00 (the default): 47 h in each room (56%), 28.0% utilization |
| All three paid rooms equally (THB 264.00 for one hour of each) | 14.5 h in each room, 12.9% utilization | 3 kiosks, THB 16,372.00: 62.5 h in each room (74%), 55.8% utilization; not the default, because the Focus Pod 1 door loses money |
| All three paid rooms, plus Staff at the Community Table | n/a (no Staff cost) | 4 kiosks, THB 20,572.00: 78 h in each paid room (93%), 69.6% utilization |

A single front-desk kiosk for all rooms would cost less: Staff select each guest's room with one POST (AXS-R11) and then scan, and wrong_room still refuses a ticket for another room. With one Staff member the weekly cost is THB 7,972.00, which needs 30.5 h in each paid room at an equal mix. It is not the default: once a guest is past the desk, nothing stops them entering another room while the lock is a mock.

The v1 success test (PRD section 1) is this: in each of the 4 full Bangkok weeks (Monday to Sunday) that start 30 days or more after launch, weekly net commission, summed by hand from Payment's lists on a cash basis (section 5), at or above the cost of the staffing in force. Members pay up to 30 days ahead (PUR-R10), so in the first 30 days advance payments pile up before their use or their refund, and cash runs ahead of use; those weeks are left out. Under the default, with Staff at Meeting Room A and Board Room, the target is THB 12,172.00, 55% of the THB 22,176.00 ceiling. At an equal-hours mix that is 47 h in each of the two staffed rooms (56% of their 84 weekly hours), never refunded; other mixes pass too, for example Board Room alone at 61 h. Nothing in these docs shows that 56% is attainable; it is the assumption to test first. If hosts staff their own doors, the target is THB 3,772.00, about 3.2 times lower.

So the room mix and the staffing, not utilization, decide break-even. Staff is the largest cost by far while the lock is a mock and a person must stand at each door. A real lock (AXS-Q02) would save up to THB 8,400.00 a week in Staff under the default (THB 16,800.00 with every door staffed), against the unpriced cost of the locks, the integration and their upkeep (AXS-Q02 rates its reversal cost High): that saving is the business case to price for AXS-Q02.

Three things move the result:

- Plan and free hours raise utilization and add THB 0.00. An hour of Meeting Room A under a plan gives up as much as THB 60.00 of commission when the room would otherwise sell (PUR-R19).
- A refund of 100% (24 h or more before start, or any Operator cancel) takes the commission to THB 0.00, but the hosting, Operator and Staff time are already spent (PUR-R30).
- Each failed or pending refund costs Operator time (PUR-R32, PUR-R33).

## 7. Risks

| Risk | Effect | Default in v1 | Rules, questions, ADRs |
|---|---|---|---|
| Commission is an estimate with no host payouts | hosts cannot see or receive their share | display only | D25, PMT-Q04 |
| Plans are unpriced and set by hand | plan hours use rooms and earn nothing | no plan sales | D10, PUR-Q02 |
| Plan Members can book paid rooms without limit and cancel at no cost | paid demand is blocked; hosts earn nothing for plan hours | the Operator scans upcoming plan and free rows in the all-bookings list and cancels hoarded ones (Operator cancel, refund 0); the closure Member's rows are closures, not hoarding (section 5). The dashboard cannot show it: it counts bookings by start in the last 7 days, and a plan booking 30 days out shows nothing until its day. Turning plan_active off stops only new plan bookings | PUR-R19, PUR-R34, PUR-Q02, PUR-Q15 |
| One Member books the free Community Table for every opening hour of the next 30 days | the free channel that brings Members in is locked out, at no cost to that Member: PUR-R39 limits only held bookings, and a free booking is confirmed at once and is whole-room use (D7) | the same Operator scan and cancel; no limit in v1 | PUR-R20, PUR-R39, PUR-Q15 |
| 0% refund under 24 h | Members may complain; every Operator cancel refunds 100% and gives up the commission | policy fixed at 100% or 0% | PUR-R30, PUR-Q03 |
| A refund owed stays unpaid | net and commission read too high: a failed refund until attempt 2 succeeds, a pending one until its revoke and refund land; pending ones show only in Purchase | Operator follow-up of both lists, Retry first | PMT-R17, PUR-R32, PUR-R33, PMT-Q02 |
| A refund is settled outside the system | Payment's totals never see it: net, commission and the weekly hand sum stay too high for good; a failed refund paid that way keeps "needs manual follow-up" and "Refund failed", so PRD target (2) could never pass again | the Operator keeps a list, subtracts it from the weekly sum and leaves those rows out of target (2); PMT-Q02 option (b) is the fix | PMT-R17, PUR-R33, PMT-Q02, PUR-Q03 |
| Mock payment and mock lock | no real money moves; a stored grant is not proof a door opened | mocked by design | ADR-0017, ADR-0018, PUR-Q06, AXS-Q02 |
| Abandoned checkouts and hold cycling | a held slot is unsellable for 15 minutes per hold, and without limit if the same Member, or several free accounts, keep holding it again (sign-up is free, PUR-Q04, PUR-Q05) | lazy expiry on the next touch; accepted in v1: the Operator sees held rows in All bookings and can cancel them | PUR-R21, PUR-R24, PUR-R39, PUR-Q17, ADR-0007, ADR-0016 |
| Revoke pending while the slot is rebooked | the old code can still open the room | visible pending state; refund waits for the revoke | PUR-R32, PUR-Q12 |
| Utilization read as revenue | a busy dashboard can hide low income | money shown only on Payment's page | PUR-R34, D24 |
| Three services cost more to run and change | more hosting, more coordination | accepted as the course exercise | ADR-0001, section 8 |

## 8. Three services vs modules in a monolith

The course asks us to compare the split with a monolith. Here is the same product both ways.

| Aspect | Three services (this project) | Modules in one monolith |
|---|---|---|
| Deployment | three images, three compose files; each service deploys and rolls back alone (D26, ADR-0011) | one image, one deploy; a bad change in any module rolls back the whole app |
| Data ownership | a database per service; no service reads another's database; shared references such as booking_reference, never foreign keys (ADR-0003, PUR-R35) | one database; ownership is a code-review convention; a join across modules is one line away |
| Failure modes | partial failure: Payment down gives "try again" (PUR-R31); Access down gives "being prepared" or "revocation pending" (PUR-R26, PUR-R32); a lost redirect waits for reconciliation (ADR-0007). The paid journey needs Purchase and Payment both up; only an Access outage is absorbed ("being prepared"). The split also creates the pending-revoke risk: the old code opens while a revoke waits (PUR-Q12) | up or down as a whole; no timeouts between modules; one transaction revokes and refunds together |
| Consistency | eventual: reconcile on touch, natural-key idempotency, stored follow-up fields (ADR-0014, PUR-R24) | one transaction can confirm the booking, record the payment and issue the grant together |
| Team autonomy | one repo per team; contracts beside the provider, proposed then agreed then verified (ADR-0005) | one repo, one main branch; module boundaries by convention |
| Cost | three services, three databases, six gunicorn workers, three CI pipelines (ADR-0015); hosting THB 272.00 a week (section 4) | one service, one database, one CI pipeline; hosting about THB 120.00 a week (assumption) |
| Testability | unit tests per service with stubbed clients, plus an e2e stack that sets one test clock on three services (ADR-0013) | one pytest run against one database covers the whole journey |
| Change effort for cancellation | policy and orchestration in Purchase (PUR-R30, PUR-R31, PUR-R32, PUR-R33), refunds in Payment (PMT-R14, PMT-R15, PMT-R16), revoke in Access (AXS-R17); two contracts; three deploys, provider first | one PR; status, refund record and revoke in one transaction; only the card provider stays outside |

What the split does buy: card data stays inside Payment (ADR-0020), Payment's hosted page keeps working while Access is slow (though Purchase waits up to 5 s per Access call on its 2 workers, so a hanging Access can delay "Continue to payment", ADR-0015), and each team can deploy and roll back on its own. The clear rule homes (Payment never re-prices, revoke never refunds) come from the context boundaries, which modules in one monolith would give too (ADR-0001).

### Conclusion

The three services are the course exercise, not a recommendation for this business. The syllabus says so: "Three services are the course exercise, not a claim that every growing business should split its application; students compare the costs and benefits with alternative boundaries and modules within a monolith." ([syllabus site])

For four rooms and one Operator, modules in one monolith would be cheaper to run, simpler to keep consistent, and faster to change. The running-cost difference is small next to THB 12,172.00 of weekly cost: about THB 150.00 of hosting, plus the Operator work that exists only because of the split: the Retry of pending grants, revokes and refunds, Reconcile for lost redirects, reading two operator pages with two sign-ins, and the manual join of Payment's sessions with Purchase's bookings for the host share. We assume that is 3 of the 10 Operator hours a week, THB 750.00 (assumption); a monolith revokes and refunds in one transaction and reports money by room with one query. Staff time does not change with the architecture. The split's other real costs are the cross-repo change effort and the pending states it creates (PUR-Q12). The course's own path goes through "Separate ownership, still one monolith" ([extraction site]); this project goes straight to three repos (ADR-0006). We split to practise contracts, independent delivery and a cross-service change. Split for real only when separate teams, separate release cycles or a separate card-data boundary pay for the extra cost. The decision and its alternatives are in ADR-0001.

## Sources

- Commission: class issue #173 discussion (fetched 2026-10-01); D25.
- Metrics: D24; PUR-R34; PMT-R17.
- "“Covered” is not always “money collected”." and "Separate ownership, still one monolith": [extraction site], fetched 2026-09-30.
- "Three services are the course exercise ...": [syllabus site], fetched 2026-09-30.
