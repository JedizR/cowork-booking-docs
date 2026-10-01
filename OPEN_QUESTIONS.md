# Open questions

Questions that D1 to D28 do not settle, by context. Each one states where it arises, the options, the default that applies until the owner decides (M5 builds the default), the reversal cost, the owner and the class question it continues, if any. Class questions that a decision answers are in ID_MAP.md.

## Purchase

### PUR-Q01 Cleaning gap between bookings

- Question: Should a cleaning or turnover gap separate two bookings of the same space?
- Where it arises: PUR-R11 (no gap), PUR-R12 (slot-blocking check), PUR-R13 (start-block grid), PUR-R27 (check-in window values). The Access side is AXS-Q01.
- Options: (a) no gap, back-to-back allowed; (b) a fixed gap B after every booking, for example 15 min; (c) a gap set per space.
- Default that applies: No gap, 0 min (D6). Back-to-back bookings are allowed and there is no early entry (D21).
- Reversal cost: Medium. A gap changes the slot-blocking check, the EXCLUDE range, the grid and valid_from (start - min(B, 15 min)); existing back-to-back bookings would need a transition rule.
- Owner: Course instructor (business stakeholder).
- Class source: Q03 (course instructor, class rules base a853795: "A 15-minute cleaning gap is not currently an approved rule.").

### PUR-Q02 Selling plans

- Question: Should Members buy a plan (price, term, renewal, cancellation) instead of the Operator switching `plan_active` by hand?
- Where it arises: PUR-R06 (plan toggle), PUR-R19 (coverage), PUR-R20 (plan skips Payment), PUR-R34 (metrics).
- Options: (a) no plan sales, operator toggle only; (b) a monthly plan paid through Payment; (c) prepaid hour bundles.
- Default that applies: No plan sales in v1 (D10). The Operator sets `plan_active`; it has no price and no end date; turning it off never changes existing bookings.
- Reversal cost: High. A plan product needs its own price, a recurring payment flow in Payment and a rule for what a plan covers (hours, spaces).
- Owner: Course instructor (business stakeholder).
- Class source: no question ID. PAY-T03 (class rules main 58a1477, PR #1): "No price, no end date, no way to cancel. It is unclear what it covers."; PAY-R01: "What does a subscription cover, and can it end?"

### PUR-Q03 Cancellation cases we do not support

- Question: Should Purchase support partial cancel, reschedule, a Member cancel after start, or refunds other than 0% and 100%?
- Where it arises: PUR-R30 (cancel policy), PUR-R32 (cancel steps).
- Options: (a) unsupported, recorded in the PRD; (b) reschedule as cancel plus a new booking; (c) pro-rata refunds.
- Default that applies: Unsupported (D18). The Member cancels the whole booking before start (100% at 24 h or more before start, else 0%) or asks the Operator, who may cancel before end at 100%.
- Reversal cost: Medium to high. Partial refunds change the refund contract with Payment; reschedule needs price and coverage rules for the new time.
- Owner: Course instructor (business stakeholder).
- Class source: none.

### PUR-Q04 Email confirmation

- Question: Must a Member confirm their email before they can book?
- Where it arises: PUR-R01 (registration), PUR-R04 (operator promotion: whoever registers OPERATOR_EMAIL first).
- Options: (a) no confirmation; (b) confirm by an emailed link before the first booking.
- Default that applies: No email confirmation in v1; a new Member can log in and book at once. Purchase sends no email. The password rule stays "at least 8 characters" (D15).
- Reversal cost: Medium. It needs a mail service, a token table and an unconfirmed state on Member. It also closes an accepted risk: until then, whoever registers the OPERATOR_EMAIL address first is promoted (PUR-R04).
- Owner: Course instructor (business stakeholder).
- Class source: Q-ACC-2, second half (class rules PR #10, head d68631f). The first half (password policy) is settled by D15.

### PUR-Q05 Failed-login limits

- Question: Should Purchase slow down or lock logins after repeated failures?
- Where it arises: PUR-R02 (login). The kiosk side is AXS-Q04.
- Options: (a) no limit; (b) a per-email delay after 5 failures; (c) a per-address rate limit in front of the service.
- Default that applies: No limit in v1; the uniform error stays (D16). Recorded as a known risk.
- Reversal cost: Low. A counter and a check in login; no contract changes.
- Owner: Project team, with the course instructor.
- Class source: Q-ACC-4, first half (class rules PR #10, head d68631f). The second half (booking under another member name) is settled: the booking takes the logged-in Member (D15, PUR-R05).

### PUR-Q06 Real door locks

- Question: When a real lock replaces the mock, which door does each space map to, and what must Purchase send?
- Where it arises: PUR-R26 (grant request), PUR-R27 (window values). The Access side is AXS-Q02.
- Options: (a) keep the mock and send space_id and space_name only; (b) store a door id per space in Purchase and send it; (c) Access keeps its own space-to-door map.
- Default that applies: The lock stays mocked (course [extraction site]: "Proposed internal calls. Payments and locks remain mocked."). Purchase sends space_id, space_name, valid_from and valid_until; a stored grant is not proof that a door opened.
- Reversal cost: Medium. A new field in the grant request and a new version of the Access contract.
- Owner: Course instructor (business stakeholder), with the project team.
- Class source: none (Q07 on class rules PR #12 at 1c8ce57, about code expiry, belongs to Access).

### PUR-Q07 Bookings without a stored price

- Question: How is a booking recorded when its price was never stored?
- Where it arises: PUR-R17 (booking price).
- Options: (a) migrate no legacy bookings, so every booking stores its price at creation; (b) migrate seed-app bookings and fill missing prices.
- Default that applies: No booking data is migrated from the seed app. `agreed_price_satang` is required on every booking. The seed app's startup backfill is removed (Spacey: source inspected at 5a1cf3d, app.py:112-117 fills a missing amount with the current hourly rate, ignoring the duration).
- Reversal cost: Low now; high once real bookings exist.
- Owner: Project team.
- Class source: PRC-Q02, second half (class rules PR #4, head 9478b3e). The first half (fixed at booking or at payment) is answered by class rules PR #14 at 25ca71e and D8.

### PUR-Q08 A plan Member books a free space

- Question: Member B (plan_active true) books Community Table (price 0). Is the coverage plan or free?
- Where it arises: PUR-R19 (coverage), PUR-R34 (metrics).
- Options: (a) free whenever the price is 0; (b) plan whenever plan_active is true.
- Default that applies: free when the price is 0, else plan when plan_active is true, else pay. Both skip Payment; only the label and the dashboard's confirmed hours by coverage (PUR-R34: free, not plan) differ. D10 names both conditions but not their order.
- Reversal cost: Low. A label and a metric filter.
- Owner: Project team.
- Class source: none.

### PUR-Q09 Payment unreachable when the hold is created

- Question: What happens to a held booking when POST /payment-sessions fails or times out, so the booking has no payment session?
- Where it arises: PUR-R21 (hold), PUR-R23 (session request), PUR-R24 (reconciliation), PUR-R31 (held cancel).
- Options: (a) keep it held and retry on "Continue to payment"; (b) cancel it at once; (c) keep retrying in the background.
- Default that applies: (a), for a timeout, a connection error or a 5xx answer (PUR-R35): the booking stays held without a session, and "Continue to payment" for the same space and time repeats the request (PUR-R21, PUR-R23). The booking page shows "Payment could not be started. Pay by 10:13" with "Continue to payment" and Cancel. Without a session it is expired on lapse or cancelled on cancel with no Payment call (PUR-R24, PUR-R31), and from the payment deadline (hold_expires_at - 2 min, derived even without a session) no session is requested (PUR-R40).
- Reversal cost: Low.
- Owner: Project team.
- Class source: none.

### PUR-Q10 Does the refund wait for the revoke?

- Question: In a confirmed-booking cancel, should step 3 (refund) wait until step 2 (revoke) has succeeded?
- Where it arises: PUR-R32 (cancel steps).
- Options: (a) run step 3 even when step 2 failed and retry each on its own; (b) hold the refund until the grant is revoked.
- Default that applies: (b): the refund is sent only after the revoke has succeeded, and a retry runs the revoke first (PUR-R32; DECISIONS.md, Disputes decided in M1, row 6). Trade-off: while Access is down, the Member waits for the money.
- Reversal cost: Low. (a) only drops the wait in the retry step.
- Owner: Project team.
- Class source: none.

### PUR-Q11 Which 7 days the dashboard counts

- Question: Which days and which bookings make up "the last 7 Bangkok days"?
- Where it arises: PUR-R34 (metrics).
- Options: (a) today and the 6 dates before it, bookings counted by start; (b) the 7 full dates before today; (c) bookings counted by creation time.
- Default that applies: (a): today and the 6 dates before it, with each booking counted by its start; PUR-R34 gives the bounds, the rounding and the examples. Archived spaces: D24's denominator counts non-archived spaces, so the utilization numerator counts confirmed hours in non-archived spaces only; bookings by status, members and hours by coverage count every booking, archived spaces included. A lapsed hold counts as held until something reconciles it; the dashboard does not reconcile.
- Reversal cost: Low. Query bounds only.
- Owner: Project team.
- Class source: none (the counting questions MET-Q01, Q-MET-1 and Q-MET-2 are answered by D24).

### PUR-Q12 Revocation pending while the slot is rebooked

- Question: Step 1 of a confirmed cancel frees the slot. If the revoke in step 2 got no answer, Access still answers ok for the old ticket code. If another Member books the freed slot, the kiosk admits both parties. What should prevent that?
- Where it arises: PUR-R32 (rows 3 and 6), PUR-R12 (a cancelled booking is not slot-blocking), AXS-R13 (the old code still opens).
- Options: (a) accept the risk and make the pending revoke visible; (b) also retry the pending revokes of that space in the pre-insert sweep (PUR-R22); (c) keep the slot blocked until the revoke succeeds, which changes the D11 predicate; (d) a "Retry all pending" button on the all-bookings list that works like "Reconcile all held" and stops after the first call with no answer.
- Default that applies: (a), as D19 stands. The Operator's all-bookings list flags "Revocation pending", and a pending revoke is retried on the booking page (or GET /api/bookings/<ref>), by the owner's Retry or by the Operator's Retry (PUR-R26, PUR-R32). The refund waits for the revoke (PUR-Q10), so no money moves while the old code still opens.
- Reversal cost: Low for (b): one more step in the sweep. Medium for (c): the slot-blocking predicate, the EXCLUDE constraint and the grid change. Low for (d): one route and one button; v1 has none, so the Operator presses Retry per flagged row in a daily routine (BUSINESS_MODEL.md section 4).
- Owner: Project team.
- Class source: none.

### PUR-Q13 Unarchive a space

- Question: An Operator who archives the wrong space has no way back. Should an archived space be restorable, and may it be edited?
- Where it arises: PUR-R16 (archive), PUR-R15 (space values), PUR-R34 (utilization counts non-archived spaces); AXS-R11 (the kiosk lists rooms from grants).
- Options: (a) no unarchive: create a new space; (b) POST /operator/spaces/<id>/unarchive clears archived_at; (c) let the Operator edit an archived space and unarchive it.
- Default that applies: (a). Archive is one-way in v1 and an archived space cannot be edited (POST /operator/spaces/<id> gets 404). The workaround is a new space with a new space_id: its history starts empty, the dashboard counts the two spaces apart, and the kiosk lists both rooms once the new one has a grant, told apart by room number, "Meeting Room A (room 1)" and "Meeting Room A (room 5)" (AXS-R11).
- Reversal cost: Low for (b): one route, one button and the archived-space tests.
- Owner: Project team.
- Class source: none.

### PUR-Q14 Receipts, tax invoices and VAT

- Question: Should a Member get a receipt or a tax invoice, and do prices include VAT?
- Where it arises: PUR-R17 (booking price), PUR-R18 (money display); PMT-R17 (money totals).
- Options: (a) no receipt: the booking page shows the price paid; (b) a printable receipt page in Purchase; (c) tax invoices with a VAT breakdown and the host's details.
- Default that applies: (a). The price is final and shown with no tax breakdown; v1 issues no receipt or tax invoice.
- Reversal cost: Medium for (b); high for (c), which needs host tax details, invoice numbering and a VAT rule.
- Owner: Course instructor (business stakeholder).
- Class source: none.

### PUR-Q15 Limits on confirmed plan and free bookings per Member

- Question: Should a Member's upcoming confirmed plan and free bookings be limited, so that one Member cannot take every opening hour of a room for the next 30 days at no cost?
- Where it arises: PUR-R39 (it limits held bookings only), PUR-R19 and PUR-R20 (plan and free bookings are confirmed at once, whole-room use, D7), PUR-R10 (the 30-day horizon), PUR-R34 (the dashboard counts bookings by start in the last 7 days, so future hoarding does not show there); BUSINESS_MODEL.md section 7.
- Options: (a) no limit; the Operator watches upcoming rows; (b) a cap on a Member's upcoming confirmed plan and free hours (for example 10 hours in the next 30 days), checked in the PUR-R39 order; (c) a cap per space per day.
- Default that applies: (a), no limit in v1. The Operator scans upcoming plan and free rows in the all-bookings list and cancels hoarded ones (an Operator cancel refunds 0 for plan and free, PUR-R30). Turning plan_active off stops only new plan bookings; existing ones stay (PUR-R19).
- Reversal cost: Low: one count in the PUR-R39 check order, one message and its tests.
- Owner: Course instructor (business stakeholder), with the project team.
- Class source: none.

### PUR-Q16 Password change, reset and account erasure

- Question: How does a Member change a leaked password or recover a forgotten one, and can a Member have the account erased?
- Where it arises: PUR-R01 (registration), PUR-R02 (login), PUR-R03 (a copied session lasts until its 12 h end); ADR-0002 (password reset is an extraction trigger), ADR-0016.
- Options: (a) none in v1; (b) the Operator sets a one-time password; (c) an emailed reset link, which needs the mail service of PUR-Q04; (d) on request, overwrite email and display_name with placeholders and keep the booking rows.
- Default that applies: (a). No password change, no reset and no erasure in v1. A Member who forgets the password registers again with another email; the Operator cannot reset a password; a leaked password stays valid. Bookings keep member_id; Payment and Access hold no email or name (PUR-R23, AXS-T18), so erasure would touch Purchase only. Recorded in the PRD "Not in v1" table and ADR-0016.
- Reversal cost: Low for (b) or (d): one operator form or one update. Medium for (c): a mail service, a token table and an expiry.
- Owner: Course instructor (business stakeholder), with the project team (security lens).
- Class source: ACC-T01 boundary (class rules PR #10, head d68631f): "At this revision there is no email confirmation, password change, password reset or account deletion." Email confirmation continues as PUR-Q04.

### PUR-Q17 Repeated holds without paying

- Question: PUR-R39 allows one held booking per Member, but a Member may cancel a hold, or let it lapse, and hold the same slot again at once. Sign-up needs no email confirmation (PUR-Q04) and has no rate limit (PUR-Q05). Should repeated holds be limited, so that one script or a few free accounts cannot keep a paid room's best slots held without paying?
- Where it arises: PUR-R21 and PUR-R39 (one held booking, 15 minutes each), PUR-R31 (a held cancel frees the slot at once), PUR-R01 (free sign-up); BUSINESS_MODEL.md section 7; ADR-0016; DECISIONS.md seed flaw F3.
- Options: (a) no limit; the Operator watches held rows; (b) at most N held bookings per Member per Bangkok day; (c) no new hold of the same slot by the same Member until the old hold_expires_at; (d) a sign-up rate limit, or email confirmation (PUR-Q04).
- Default that applies: (a), accepted in v1. A held slot is unsellable for 15 minutes per hold, and without limit while the same Member or several accounts keep holding it again. The Operator sees held rows in All bookings (with "held, pay by 10:13") and can cancel them. Trigger to revisit: public deployment.
- Reversal cost: Low for (b) or (c): one count or one lookup in the PUR-R39 check order, one message and its tests. Medium for (d).
- Owner: Course instructor (business stakeholder), with the project team (security lens).
- Class source: none.

### PUR-Q18 M3 round 5: Under the default, Staff stand only at the Meeting Room A and Board Ro

- Question: Under the default, Staff stand only at the Meeting Room A and Board Room doors. Section 6 says a room without Staff cannot let anyone in. Two spaces are still listed and bookable: (a) The Community Table has no Staff and no kiosk under the default (it is staffed only in the non-default 4-kiosk row). A free booking there gets an e-ticket that nobody checks and that cannot get the Member in. Section 2 relies on this space as the channel that brings Members in. (b) Focus Pod 1 'is not sold' when its host does not staff it, but v1 has no way to stop selling a space except the one-way archive (PUR-R16, PUR-Q13). If it stays listed, a Member can pay THB 10.00 or more for a door nobody opens, which forces an Operator 100% cancel and more Operator time. The default's utilization figures (28.0%, '56%') also use 336 h, which assumes all 4 spaces stay listed. If the unstaffed spaces are archived, the denominator is 168 h, and 94 h is 56.0%, not 28.0%.
- Where it arises: BUSINESS_MODEL.md; PRD.md; OPEN_QUESTIONS.md, BUSINESS_MODEL.md header (line 3), section 2 'the free Community Table brings Members in' (line 40), section 4 Staff time (line 101), section 6 lines 137-139 ('a room without Staff cannot let anyone in while the lock is a mock'), 149 (Focus Pod 1 'otherwise it is not sold'), 155 (default row, 28.0% utilization over 336 h), 157; PRD.md section 1 (line 22); OPEN_QUESTIONS.md PMT-Q04 default (line 214); RULES.md PUR-R16 and OPEN_QUESTIONS PUR-Q13 (archive is one-way).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Say in BUSINESS_MODEL section 6 (and copy it to the PRD section 1 target and the PMT-Q04 default) what happens to each unstaffed space under the default. Pick one rule for each. Community Table: give it the default's third kiosk (target THB 16,372.00), make it an open table inside a staffed area with no kiosk check (say so in section 2 and the PRD), or leave it out of v1 and drop the 'brings Members in' claim. Focus Pod 1: without host Staff it is not created, or it is archived before launch, and a new space is created if a host later staffs it (PUR-Q13). Then recompute the utilization percentages over the spaces that are actually listed.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, major).

### PUR-Q19 M3 round 5: The 0% rule for a cancel under 24 h has an undefined exit that the doc

- Question: The 0% rule for a cancel under 24 h has an undefined exit that the docs point Members to. A Member who cancels at 08:00 gets THB 0.00. The same Member who 'asks the operator', after the start through door Staff or any outside channel, can only get an Operator cancel, and under D18 that is always 100%. No document says when the Operator should agree. The section 3 worked example shows an Operator cancel at 09:30 as an ordinary case. So whether the 0% rule holds depends on unwritten judgement. Each Operator cancel gives up the full 20% commission and the host's 80%, and the dashboard and Payment's page do not separate these refunds from refunds caused by venue faults.
- Where it arises: PRD.md; OPEN_QUESTIONS.md; BUSINESS_MODEL.md, PRD.md section 5 Unsupported row 'Member cancel after the start: Ask the Operator, who may cancel before the end at 100%' (line 524), section 3 support row (line 84), AC13.3 (line 270); OPEN_QUESTIONS.md PUR-Q03 default (line 32: 'or asks the Operator, who may cancel before end at 100%'); BUSINESS_MODEL.md section 3 worked example row 'Operator cancels 2026-10-07 09:30' (line 70), section 7 risk '0% refund under 24 h' (line 179); RULES.md PUR-R30.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Do not change D18. Add Operator cancel criteria to PRD section 5 (that row and AC13.3), the PUR-Q03 default and a BUSINESS_MODEL section 7 risk row. The Operator cancels a paid booking only when the room could not be delivered: room unusable, closure, a door or Staff failure, or a double entry from a pending revoke. A Member's change of plans is refused, so the Member policy (100% at 24 h or more, else 0%) holds. Reword the unsupported row to 'No refund after the start; the Operator cancels (100%) only when the room could not be used.' Optionally add PUR-Q03 option (d), an Operator cancel at the Member policy, with default none.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, major).

### PUR-Q20 M3 round 5: The split's extra cost is about THB 900.00 a week: THB 152.00 of hosti

- Question: The split's extra cost is about THB 900.00 a week: THB 152.00 of hosting plus 3 Operator hours, THB 750.00. That is 'small' only against the default THB 12,172.00. Under the host-staffed alternative the doc also costs (THB 3,772.00), it is about 24% of the platform's weekly cost. At THB 7,972.00 it is about 11%. That equals about 10 standard Meeting Room A bookings a week (THB 900.00 / THB 90.00). The Cost row also lists only the hosting difference and omits the THB 750.00 of Operator time that the conclusion counts.
- Where it arises: BUSINESS_MODEL.md, Section 8 table row 'Cost' (line 199) and Conclusion (line 209: 'The running-cost difference is small next to THB 12,172.00 of weekly cost').
- Options: (a) keep the current text; (b) apply the reviewer's fix: Give the figure in the Cost row ('about THB 900.00 a week: THB 152.00 hosting plus THB 750.00 Operator time'). In the conclusion, state it against each staffing case: about 7% of THB 12,172.00, about 11% of THB 7,972.00, and about 24% of THB 3,772.00, or about 10 standard bookings a week. Drop 'small' or limit it to the default.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, minor).

### PUR-Q21 M3 round 5: The members example mixes two scenarios. In the named scenario (PUR-R3

- Question: The members example mixes two scenarios. In the named scenario (PUR-R34 row 1), Member A has one booking (BK-7KQ2M9), and the result is members 2, confirmed 2. 'Member A with two bookings counts once' comes from PUR-R34 row 5, a different scenario. AC20.2 appends it to the row 1 example, and the BUSINESS_MODEL header says every section 5 dashboard row follows row 1.
- Where it arises: PRD.md; BUSINESS_MODEL.md, PRD.md AC20.2 (line 347, last sentence 'Member A with two bookings counts once'); BUSINESS_MODEL.md section 5 Members row example (line 119) against the header (line 5: 'the section 5 dashboard rows follow PUR-R34 row 1').
- Options: (a) keep the current text; (b) apply the reviewer's fix: In AC20.2, start the last sentence with 'Separately (PUR-R34 row 5):'. In BUSINESS_MODEL section 5 use the row 1 figure ('members 2: Member A and Member B'), or mark the example as PUR-R34 row 5.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, minor).

### PUR-Q22 M3 round 5: The Operator procedures use wording that an Operator cannot follow. 'C

- Question: The Operator procedures use wording that an Operator cannot follow. 'Clear both lists' does not say which lists, and a failed refund's 'needs manual follow-up' label cannot be cleared except by a successful attempt 2. The adjusted-commission step tells a person to match rows by data-booking-reference, which is an HTML test marker and not something visible on the page.
- Where it arises: BUSINESS_MODEL.md, Section 3 paragraph 'Before reading commission' (line 82: 'Then clear both lists.'); section 5 'Refunds owed' row (line 122: 'whose data-booking-reference has no succeeded refund row').
- Options: (a) keep the current text; (b) apply the reviewer's fix: Line 82: 'Then work through Payment's "needs manual follow-up" rows and Purchase's "Refund failed" rows: press Retry in All bookings on each one'. Line 122: 'whose booking reference has no succeeded refund row on Payment's page'.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, minor).

### PUR-Q23 M3 round 5: Nothing tells a Member that the Operator cancelled their booking. v1 h

- Question: Nothing tells a Member that the Operator cancelled their booking. v1 has no email, and the 'Email' row covers only confirmations and tickets. The Operator cancels in several documented flows: a room closure (all affected bookings), hoarded plan rows, an 'undo by mistake', and any request. In each one the Member learns only by opening the booking page. Most Members find out at the door, when Staff read 'This ticket was cancelled'. A printed e-ticket or saved /t/ link from before the cancel still looks valid on paper. The closure row even tells the Operator to cancel at 100% and say nothing. No rule, AC, open question or unsupported-case row records this, so the Member-facing outcome of the required 'operator cancel' case is undefined.
- Where it arises: PRD.md, Section 3 'Not in v1' table: 'Email' row (line 69), 'Close a room for a day' row (line 87), 'Limits on confirmed plan and free bookings' row (line 85); section 5 Unsupported row 'Undo a cancel' (line 531); US16 AC16.2-AC16.5 (lines 305-308). Also contracts/purchase-public.md section 7 Cancelled line 1 'Cancelled by the operator.' (line 234).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Add a 'Not in v1' row named 'Telling a Member about an Operator cancel'. Its text: 'No message in the app or by email. Before cancelling, the Operator contacts the Member outside the app at the email shown in All bookings and on the confirm screen. The booking page and My bookings then show "Cancelled by the operator." with the refund line.' Add 'tell each affected Member first' to the closure row and the hoarding row. Add AC16.7 citing PUR-R30 and PUR-R32: 'Member A sees the cancel only on the booking page and in My bookings: "Cancelled by the operator." and "THB 450.00 refunded."'. Record a new open question (for example PUR-Q18 'Notify a Member of an Operator cancel'), default 'manual contact by the Operator', owner Course instructor. No rule text changes.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, major).

### PUR-Q24 M3 round 5: 'Upcoming' is defined as 'end after now, any status'. Cancelled bookin

- Question: 'Upcoming' is defined as 'end after now, any status'. Cancelled bookings and expired holds with a future date therefore sit among the Member's upcoming visits, in start order. After a few lapsed or cancelled holds (hold cycling is allowed, PUR-Q17), the upcoming list mixes dead rows with real ones. A Member scanning it for 'where do I go next' can take a cancelled booking for a live one.
- Where it arises: PRD.md, US12 AC12.1 (line 259) and section 6 'My bookings' row (line 551); contracts/purchase-public.md section 4 GET /bookings/mine (line 104); contracts/openapi/purchase.yaml myBookingsPage (lines 626-633).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Define Upcoming as held or confirmed with end after now. List cancelled and expired bookings under Past, or in a third group 'Cancelled and expired', by start descending. Change AC12.1, the PRD row, the contract row and myBookingsPage. Keep the GET /api/bookings/mine order as it is.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PUR-Q25 M3 round 5: The Member's own Retry reuses the Operator's flash texts. The Member's

- Question: The Member's own Retry reuses the Operator's flash texts. The Member's page says 'Your ticket is still being cancelled; any refund follows.' Pressing Retry then flashes 'Grant revoked', 'Refund attempt 1 succeeded' or 'Access is not reachable. Please try again.'. 'Grant', 'attempt 1' and 'Access' (the service name) are internal terms that round 3 #4 removed from the Member's page. A Member cannot tell from them what happened to the ticket or the money.
- Where it arises: contracts/purchase-public.md, Section 4 row POST /bookings/<ref>/retry (line 103); PRD.md section 6 Booking row ('with the flashes of the operator Retry', line 548); contracts/openapi/purchase.yaml retryByForm (lines 775-781).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Give the owner route its own flashes: 'Your e-ticket is ready', 'Your ticket is cancelled', 'THB 450.00 refunded', 'Refund of THB 450.00 pending', 'The ticket service is not reachable. Please try again.', 'Payment is not reachable. Please try again.' and 'Nothing to retry'. Keep the operator route's flashes as they are. Update the contract row, the PRD Booking row and retryByForm. The page lines stay the same.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PUR-Q26 M3 round 5: The confirm screen shows only the refund amount. Three things are miss

- Question: The confirm screen shows only the refund amount. Three things are missing. (1) The consequences: the e-ticket stops working, the slot goes back on sale, and the cancel cannot be undone (PRD section 5 records 'Undo a cancel' as unsupported). (2) The reason for 0%: the screen reads only 'Refund THB 0.00 (0%)'. (3) Any notice when the held booking's reconcile read finds a payment. A Member who opened Cancel to drop what they thought was an unpaid hold is shown 'Refund THB 450.00 (100%)'. Nothing tells them the payment went through and the booking is now confirmed with a ticket, so they may cancel a booking they meant to keep.
- Where it arises: contracts/purchase-public.md, Section 5.4 confirm-screen table (lines 154-165); RULES.md PUR-R31 rule ('Paid: the booking is confirmed (D14) and the screen shows the confirmed-booking refund', line 775) and row 10; PRD.md AC13.1, AC13.2, AC13.5 (lines 268-272) and section 6 Cancel row (line 550).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Under the refund line, for confirmed bookings, add: 'Your e-ticket will stop working and the slot will be released. This cannot be undone.' Make the 0% text 'Refund THB 0.00 (0%): the start is less than 24 h away.'; the old string stays a prefix, so markers and tests still match. When the held read finds paid, put this line before the refund: 'Your payment of THB 450.00 went through: BK-7KQ2M9 is confirmed.' Copy all three into PUR-R31 (row 10), AC13.1, AC13.5, the PRD Cancel row and cancelConfirmPage.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PUR-Q27 M3 round 5: For today and tomorrow the review adds 'Starts less than 24 h away can

- Question: For today and tomorrow the review adds 'Starts less than 24 h away cannot be refunded.'. The grid has a radio for every start but one review line, so the Member cannot tell which starts this covers. On 2026-10-05 at 10:00, a 2026-10-06 start at 09:30 is non-refundable from the moment it is paid, while one at 10:30 is refundable for 30 more minutes. The sentence is true but leaves the Member to do the date arithmetic.
- Where it arises: PRD.md, US5 AC5.5 (line 179) and section 6 'Space and grid' row (line 547); contracts/purchase-public.md section 6 (line 204); RULES.md PUR-R30 rule text and row 14 (lines 741, 766); contracts/openapi/purchase.yaml spacePage.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Render the cut-off from clock.now(): 'Starts before 2026-10-06 10:00 cannot be refunded.' (now + 24 h, Bangkok). Update AC5.5, PUR-R30 row 14 (2026-10-06 shows 'Starts before 2026-10-06 10:00 cannot be refunded.'), contract section 6 and spacePage.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PUR-Q28 M3 round 5: A refused booking form redirects to /spaces/<id>?date&blocks, and a re

- Question: A refused booking form redirects to /spaces/<id>?date&blocks, and a refused sign-up redirects to /register. Both drop everything the Member typed: start, party size and note, or email and display name. A pasted 600-character note is lost completely after 'Note must be at most 500 characters'. 'Pick a start time' costs the Member the party size and note too. Nothing sets a default party size, so a Member who skips that field gets 'Party size must be 1 to 6' and loses the rest of the form.
- Where it arises: contracts/purchase-public.md, Section 5.3 'Input error' row (line 141) and section 6 (lines 194-204); RULES.md PUR-R14 (note at most 500), PUR-R39 row 11 ('Pick a start time'); PRD.md AC1.2, AC4.1; contracts/openapi/purchase.yaml bookByForm, register.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Let the browser catch these errors first and keep the server checks. Use textarea maxlength="500" for the note and a party-size select of 1 to capacity with 1 preselected. Put required on the start radios. On the sign-up form use type=email required, required on display_name, and minlength="8" on the password. List these attributes in contract section 6 and the register row as UI-only. The OpenAPI form schemas stay free of constraints (round 4 #25).
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PUR-Q29 M3 round 5: Still unresolved from rounds 2 and 4: the price or coverage can change

- Question: Still unresolved from rounds 2 and 4: the price or coverage can change between the review and the POST, and the Member gets no message. It has no question ID yet, though round 5 is the last round. The harm is smaller than 'expensive' implies, and nobody has recorded that. A pay booking always shows its amount on the hosted page before any charge, and Back plus Cancel recover. A plan-to-pay switch lands on the card form instead of confirming silently. A lower price or a pay-to-plan switch only helps the Member.
- Where it arises: REVIEW_LOG.md, Round 2 #30 (line 138) and round 4 #28 (line 275), both 'open'; contracts/purchase-public.md 5.1 (line 123) and section 6 (line 204); RULES.md PUR-R17, PUR-R19.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Close it cheaply. Add an open question (for example PUR-Q19 'Price or coverage changes between review and booking') with default (a): no shown_price check in v1, for the reasons above. Residual: a Member reviewed 'No payment needed' and meets a card form, and recovers with Back, then Cancel. Reversal cost: Medium (shown_price_satang and shown_coverage on the booking form). Mark round 4 #28 as moved.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PUR-Q30 M3 round 5: D14 is Decided: a paid session whose booking is already expired gets a

- Question: D14 is Decided: a paid session whose booking is already expired gets a full refund with reason slot_unavailable. AC18.2 puts this under the Operator's Reconcile, and PUR-R25 row 5 says 'Purchase reconciles' an expired booking. But no route ever reads the session of an expired booking. PUR-R24 reconciles only held bookings. The contract and the OpenAPI say a Reconcile of a booking that is not held makes no call and flashes '0 confirmed, 0 expired, 0 cancelled, 1 unchanged'. Reconcile also shows only on held rows. So the branch can fire only inside one reconcile of a held row that is found already expired at commit, for example a two-worker race or a Purchase/Payment clock skew of more than the 2-minute margin. If that race does not happen, the paid session stays collected with no refund. The booking page then tells the Member 'Not paid in time ... nothing was charged', and that breaks the D13 invariant that every paid session ends as a confirmed booking or a refund attempt. An Operator who finds the case by joining Payment's session list with All bookings has no button to settle it. A builder who follows the contract will fail AC18.2, and a tester cannot reach AC18.2 through any route.
- Where it arises: PRD.md, AC18.2 (line 328, US18 Reconcile); RULES.md PUR-R24 Rule (line 596) and PUR-R25 Rule (line 626) and row 5 (line 642); contracts/purchase-public.md section 4 POST /operator/bookings/<ref>/reconcile (line 108) and section 7 row 'Expired, a payment landed after the hold' (line 226); contracts/openapi/purchase.yaml operatorReconcile (line 864); DECISIONS.md D14.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Option (a), recommended: allow the per-booking Reconcile on an expired booking that has a payment_session_id and refund_status none. It reads GET /payment-sessions/{id}. If the session is paid, it records and sends the slot_unavailable refund as PUR-R25 says (refund_requested_at set, flags 'Refund pending' or 'Refund failed'), and the booking stays expired. The flash counts it as unchanged plus the refund flash ('Refund attempt 1 succeeded'). Show Reconcile on such expired rows (contract section 4 and line 105, operatorBookings, PUR-R06 row 1, PRD AC16.1). Add a PUR-R24 row (expired, paid stub, refund 45000 slot_unavailable) and update operatorReconcile and AC18.2. Option (b): state in PUR-R24 and PUR-R25 that the branch runs only when the fulfilment transaction re-reads the row FOR UPDATE and finds it expired. Rewrite the Given of PUR-R25 row 5 as that race and reword or move AC18.2 out of US18. Record the residual case (clock skew, no concurrent read) as an open question, with a manual check for the Operator: a paid session on Payment's page whose booking is expired in All bookings.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, major).

### PUR-Q31 M3 round 5: The Operator sees 'Cancelled 2026-10-05 11:00' (cancelled_at) on every

- Question: The Operator sees 'Cancelled 2026-10-05 11:00' (cancelled_at) on every cancelled row and on the booking page, and ARCHITECTURE says it is 'written in the cancel transaction'. Only PUR-R32 (confirmed cancel) sets cancelled_at = clock.now(). A held cancel (PUR-R31, member_cancel or operator_cancel) and an amount_mismatch cancel (PUR-R25) set status cancelled and say nothing about cancelled_at. A builder who follows the rules leaves it null, so those rows show no cancel time. That is the dispute evidence that round-4 #31 added the column for.
- Where it arises: RULES.md, PUR-R31 Rule (line 775) and PUR-R25 Rule (line 626), against PUR-R32 step (1) (line 808); contracts/purchase-public.md section 4 GET /operator/bookings (line 105) and section 7 (line 212); ARCHITECTURE.md bookings row (line 99).
- Options: (a) keep the current text; (b) apply the reviewer's fix: In the PUR-R31 and PUR-R25 rule text, write cancelled_at = clock.now() in the transaction that sets status cancelled. Add it to the expected result of PUR-R31 row 1 and PUR-R25 row 3. Alternatively, state where cancelled_at is null and what the Operator's list then shows.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q32 M3 round 5: Three gaps on the all-bookings page. (1) A held row between the paymen

- Question: Three gaps on the all-bookings page. (1) A held row between the payment deadline and hold_expires_at, for example at 10:14, can only read 'held, pay by 10:13', a deadline that has already passed. The booking page in the same state says 'Time to pay has run out'. (2) The sort is 'flagged ones first (those with a refund owed by oldest Refund requested time), then newest start first'. It does not say whether rows with a refund owed come before other flagged rows ('Being prepared', 'Revocation pending' alone), or how those other rows are ordered. A test that asserts 'listed first' (seq-refund-retry) can break. (3) Per-booking Reconcile with no answer from Payment flashes only 'Payment is not reachable. Please try again.' in the contract, while PUR-R24 row 10 gives Reconcile all held the counts plus that text. The exact flash is ambiguous.
- Where it arises: contracts/purchase-public.md, Section 4 GET /operator/bookings (line 105) and POST /operator/bookings/<ref>/reconcile (line 108); PRD.md AC16.1 (line 304), AC18.4 (line 330), section 6 All bookings row (line 552); contracts/openapi/purchase.yaml operatorBookings and operatorReconcile.
- Options: (a) keep the current text; (b) apply the reviewer's fix: (1) Add the status label 'held, time to pay ran out 10:13 (hold ends 10:15)' for that interval, in the contract, PRD AC16.1, section 6 and operatorBookings. (2) Pin the order: rows with a refund owed first, by refund_requested_at ascending; then the other flagged rows, newest start first; then unflagged rows, newest start first. (3) Pin the per-booking flash as '0 confirmed, 0 expired, 0 cancelled, 1 unchanged. Payment is not reachable. Please try again.', in the contract, operatorReconcile and AC18.4.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q33 M3 round 5: Still unresolved from round 3 #27. The kept path after login is define

- Question: Still unresolved from round 3 #27. The kept path after login is defined only for a refused booking POST and for POSTs on /bookings/<ref>/.... Take an Operator whose 12 h login ends while working: they press Retry, Reconcile, Reconcile all held, Cancel on the operator route, Archive, Save space or a plan button. Each gets 'Please log in again', and after login the Operator lands on '/', away from the list they were working through. A builder has no rule for which path to keep.
- Where it arises: RULES.md, PUR-R05 Rule (line 137); contracts/purchase-public.md section 2 'Anonymous callers' (line 23); REVIEW_LOG.md round 3 #27 (left open; round 4 #34 fixed only the return_to half).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Extend the PUR-R05 rule and contract section 2 as follows. A refused POST on /operator/bookings/<ref>/... keeps /bookings/<ref> when return_to=booking, else /operator/bookings. POST /operator/bookings/reconcile keeps /dashboard when return_to=dashboard, else /operator/bookings. /operator/spaces/... keeps /operator/spaces, and /operator/members/... keeps /operator/members. Add one PUR-R05 row: the Operator's login ended, they press Retry in All bookings, log in, and get a 303 to /operator/bookings.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q34 M3 round 5: The contract has the operator cancel, retry and reconcile forms carry

- Question: The contract has the operator cancel, retry and reconcile forms carry a hidden return_to, and GET /bookings/<ref>/cancel reads ?return_to=booking. The OpenAPI mentions return_to only in description prose. It declares no query parameter on cancelConfirmPage, no return_to field in CancelForm, and no request body at all on operatorRetry and operatorReconcile. Only operatorReconcileAll declares it. A client or contract test generated from the OpenAPI never sends return_to, so the 'answer comes back to the booking page' behaviour is untested. Also, the confirm screen's 'Keep booking' link always goes to /bookings/<ref>, even when the Operator opened the screen from the all-bookings list.
- Where it arises: contracts/openapi/purchase.yaml, cancelConfirmPage (lines 713-760, no return_to query parameter); requestBodies.CancelForm (line 1146, no return_to); operatorRetry (line 837) and operatorReconcile (line 859), no requestBody; against contracts/purchase-public.md section 4 lines 101 and 106-108.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Declare the query parameter return_to (string, 'booking'; anything else means the list) on cancelConfirmPage. Add an OperatorCancelForm (shown_refund_satang plus return_to), or add return_to to CancelForm and mark it operator-only. Add an application/x-www-form-urlencoded requestBody with return_to to operatorRetry and operatorReconcile. In contract section 4 and 5.4, make 'Keep booking' go to /operator/bookings when an operator opened the screen without return_to=booking.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q35 M3 round 5: The docs say v1 has no JSON route for operator work and that operator

- Question: The docs say v1 has no JSON route for operator work and that operator pages are browser-only. But POST /api/bookings/<ref>/cancel is 'Owner only', where Owner includes an operator, and the policy follows the caller. So an operator can cancel any Member's booking over JSON at 100%, with no shown-refund check, and PUR-R30 rows 6 and 13 test exactly that. GET /api/bookings/<ref> is also open to the operator (PUR-R05 row 2). A builder reading AC14.3 could block operators on /api/*, and a reviewer reading PUR-R30 would expect them allowed.
- Where it arises: PRD.md, AC14.3 (line 289); RULES.md intro (line 27) and PUR-R06 Rule (line 165, 'v1 has no JSON route for them'); contracts/purchase-public.md section 8 (line 253) and 8.6 (line 307); against RULES.md PUR-R30 rows 6 and 13 (lines 758, 765) and purchase.yaml /api/bookings/{ref}/cancel ('the caller's role decides the policy').
- Options: (a) keep the current text; (b) apply the reviewer's fix: Reword AC14.3, the RULES intro, PUR-R06 and contract section 8 to: 'v1 has no JSON route for operator-only work (spaces, plans, Retry, Reconcile, dashboard); an operator may read any booking with GET /api/bookings/<ref> and cancel any booking with POST /api/bookings/<ref>/cancel under the operator policy, with no shown-refund check (PUR-R30 rows 6 and 13)'. Cite it from US16.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q36 M3 round 5: The only recovery the docs give for a forgotten password is 'register

- Question: The only recovery the docs give for a forgotten password is 'register again with another email'. For the Operator that does not restore operator rights, because promotion follows OPERATOR_EMAIL. The Operator is the only person who can cancel a started booking, start refund attempt 2, Reconcile or set plans, so a lost Operator password stops all operator work. The recovery path exists in pieces (PUR-R04 rows 7-8, the README demotion step) but is never stated.
- Where it arises: PRD.md, Section 3 'Not in v1' row 'Password change or reset' (line 81); OPEN_QUESTIONS.md PUR-Q16 default (line 162); RULES.md PUR-R04 (lines 112-131).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Add the Operator path to the PRD row and the PUR-Q16 default. Register a new address, set OPERATOR_EMAIL to it and restart Purchase, then log in with the new address, which is promoted (PUR-R04 row 7). Then run the README demotion for the old account, because is_operator is never removed automatically and the old password would keep operator rights (PUR-R04 row 8).
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q37 M3 round 5: Archive is one POST from the spaces admin list, sitting beside the edi

- Question: Archive is one POST from the spaces admin list, sitting beside the edit forms, with no confirmation, and it is one-way (PUR-Q13: no unarchive, no edit). A mis-click on the wrong row, for example a space with only past bookings, removes the room from booking at once. The only workaround is a new space with a new space_id: a new kiosk room number, history split across two spaces and the dashboard counting them apart. Cancel, which can be undone by booking again, has a confirm screen; archive, which cannot be undone, has none.
- Where it arises: RULES.md, PUR-R16 Rule (line 401); PRD.md AC15.4 (line 298) and section 6 Spaces admin row (line 553); contracts/purchase-public.md section 4 POST /operator/spaces/<space_id>/archive (line 113).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Add a confirm step. GET /operator/spaces/<id>/archive shows 'Archive Meeting Room A (room 1)? This cannot be undone: the space leaves the spaces list and cannot be edited or restored.' with an 'Archive space' button that posts to the existing route, and a 'Keep space' link. Add a PRD AC under US15, a contract section 4 row and a purchase.yaml path. The archive rules themselves do not change.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q38 M3 round 5: There is no recorded answer for a Member who cancelled at 0% (under 24

- Question: There is no recorded answer for a Member who cancelled at 0% (under 24 h) and then asks the Operator for the money back, for example because the room was unusable. The Operator cannot act: a repeat cancel answers 'This booking is already cancelled', and the operator's 100% policy applies only to a cancel the Operator makes. The table records 'Refund after the end' and 'Refunds other than 0% or 100%', but not a full refund of a booking already cancelled at 0%. This is a common support request, and the docs give the Operator no path for it.
- Where it arises: PRD.md, Section 5 'Unsupported cases (recorded)' table (lines 520-531); OPEN_QUESTIONS.md PUR-Q03.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Add a row: 'Refund a booking the Member already cancelled at 0% / Settle outside the system; the Operator lists it and subtracts it from the weekly sum by hand (BUSINESS_MODEL.md section 3); the booking keeps refund_amount_satang 0 / PUR-Q03'. Add the case to the PUR-Q03 options.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### PUR-Q39 M3 round 5: The one state diagram shows Payment's refund outcome and Access's gran

- Question: The one state diagram shows Payment's refund outcome and Access's grant state, but not the Purchase follow-up states that drive every Operator flag and Retry. These are grant_status (not_requested, pending, issued, revoke_pending, revoked) and refund_status (none, pending, succeeded, failed), including the operator-only transition from failed back to pending with attempt n+1. The Operator's recovery loop (being prepared, Revocation pending, Refund pending, Refund failed, then Retry) appears only in prose and in seq-refund-retry. A builder or tester has no single picture of which transitions Retry may make and who may make them.
- Where it arises: diagrams/states.mmd, Purchase / Booking composite (lines 4-19).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Inside the Purchase box, add a 'Follow-up on a booking' composite. grant_status: not_requested to pending (confirm), pending to issued (POST /grants answered), issued or pending to revoke_pending (cancel step 1), revoke_pending to revoked (Retry or page open). refund_status: none to pending (cancel step 1, amount_mismatch, slot_unavailable), pending to succeeded or failed, failed to pending with attempt n+1 (operator Retry only, PUR-R33). Label each state with its flag text. Re-render the SVG.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

## Payment

### PMT-Q01 What should a real payment check?

- Question: Payment is a mock. If a real card provider is added, which checks replace the syntax check and the test-card table (Luhn, card network authorisation, 3-D Secure, fraud rules, chargebacks), and do webhooks come back?
- Where it arises: PMT-R08, PMT-R09, PMT-R18.
- Options: (a) keep the mock; (b) a real provider behind the same session API, with its webhooks received by Payment only; (c) Purchase talks to the provider directly.
- Default that applies: (a). No real money moves. The syntax check (PMT-R08) and the test-card table (PMT-R09) decide every outcome; every other valid-looking number declines. Webhooks stay deferred, because Payment refuses attempts at or after expires_at (D12) and Purchase reconciles (D13).
- Reversal cost: Medium. (b) changes the attempt code inside Payment; the purchase→payment contract, statuses and IDs stay. Chargebacks would add a new money-out path and new totals.
- Owner: Project team; course instructor for scope.
- Class source: PAY-R02 open question ("What should a real payment check?"), class rules main 58a1477 (PR #1). Its first half ("a booking with amount 0 still starts unpaid and needs a card ... Should it?") is settled by D10 and D1: free and plan bookings skip Payment, and Payment refuses amounts below THB 10.00 (PMT-R02).

### PMT-Q02 How does a failed refund get closed?

- Question: Should the Operator be able to mark a failed refund as settled outside the system (for example, by bank transfer)? Should retries stop after repeated failures?
- Where it arises: PMT-R16, PMT-R17; D19 (only the operator starts attempt+1); BUSINESS_MODEL.md section 3 (a refund settled outside the system never reaches Payment's totals, so its label and the PRD section 1 target (2) never clear).
- Options: (a) only a later succeeded refund attempt clears the label; (b) a "settled outside" action on the Payment operator page, with a note; (c) automatic retries by Payment.
- Default that applies: (a). The label "needs manual follow-up" stays until a later refund attempt for the same session succeeds (the Operator's Retry in Purchase sends attempt+1, D19). Payment has no manual settle action and never retries on its own.
- Reversal cost: Low. (b) adds one column, one button and a "settled outside" line in the totals.
- Owner: Project team (business owner lens).
- Class source: none.

### PMT-Q03 Which period do the money totals cover?

- Question: Should the totals on Payment's operator page use the same "last 7 Bangkok days" period as Purchase's dashboard?
- Where it arises: PMT-R17; D24 sets the period for booking metrics and says money totals are on Payment's page, but gives the totals no period.
- Options: (a) all time; (b) the last 7 Bangkok days, by payment time and refund time; (c) a date filter.
- Default that applies: (a). All-time totals since the first record. D24's 7-day period applies to Purchase's booking metrics only. v1 therefore shows no weekly commission; the session and refund lists show paid_at and the refund's created_at (both from clock.now()), so the Operator can sum a week by hand on a cash basis: collected by paid_at minus succeeded refunds by created_at (PMT-R17, BUSINESS_MODEL.md sections 5 and 6). Cash leads use by up to 30 days, because Members pay up to 30 days ahead (PUR-R10), so the success test uses the 4 full weeks that start 30 days or more after launch.
- Reversal cost: Low: one filter and a label.
- Owner: Project team.
- Class source: none.

### PMT-Q04 Who pays hosts, and when is commission earned?

- Question: The marketplace earns a 20% commission (D25). Should Payment record host payouts? Is commission earned when the Member pays or when the booking ends? Who employs the Staff at each room door: the platform, from its 20%, or each host, from its 80%?
- Where it arises: PMT-R17, PMT-T16; AXS-R11 (a kiosk and Staff per room door while the lock is a mock); BUSINESS_MODEL.md sections 4 and 6 and the PRD section 1 success test.
- Options: (a) an estimate only; (b) a payouts ledger in Payment; (c) a separate payouts context. For Staff: (d) the platform runs the venue and pays Staff at every staffed door; (e) each host staffs its own door from its 80% share.
- Default that applies: (a). "Estimated platform commission (20% of net)" is display only. Host payouts are out of scope (D25). Nothing is paid out and no ledger exists. The figure is 20% of net collected to date, including bookings that have not started; it is not earned until the booking ends, because an Operator cancel can still refund 100% before the end (PUR-R30). For Staff, (d) for Meeting Room A and Board Room: the platform pays their door Staff; Focus Pod 1 is sold only when its host staffs its door ((e) for that room), because its best weekly commission, THB 336.00, never covers a THB 4,200.00 door. The v1 success test is then THB 12,172.00 of weekly commission, which at an equal-hours mix needs 47 of each staffed room's 84 weekly hours (56%); under (e) for every room it is THB 3,772.00 (BUSINESS_MODEL.md section 6).
- Reversal cost: High for (b) or (c): new tables, a money-out flow, a new contract and new totals. None in code for (d) or (e): only the business model's cost row and the success target change.
- Owner: Course instructor for scope; Project team.
- Class source: none.

### PMT-Q05 May anyone with the payment link pay?

- Question: The hosted page /pay/{id} works without a login. Anyone who has the link sees the amount and booking reference and can pay. Is that acceptable?
- Where it arises: PMT-R07, PMT-R01, PMT-T02.
- Options: (a) a bearer link with an unguessable session ID; (b) a short-lived signed token from Purchase in the URL; (c) a login on Payment.
- Default that applies: (a), like a hosted checkout link. The session ID carries 128 random bits and stops taking payments at expires_at (13 minutes after creation at most). It reaches the Member's browser by redirect, Purchase's booking row and the owner's booking JSON (payment_session_id, payment_url), Payment's operator page (data-session-id) and Payment's access log (the /pay/<id> and /payment-sessions/<id> paths), all at the trust level of those services' databases (accepted, like the /t/ path). Paying someone else's session only pays their booking. Payment has no Member accounts (account data lives on Member in Purchase).
- Reversal cost: Low for (b): Purchase adds a token and Payment checks it. High for (c): Payment would need accounts.
- Owner: Project team (security lens).
- Class source: none.

### PMT-Q06 M3 round 5: The only money target cannot measure a business result in v1. Target (

- Question: The only money target cannot measure a business result in v1. Target (1) asks for weekly net commission of at least THB 12,172.00 in 4 weeks that start 30 days after 'launch', summed from Payment's lists. In v1, Payment is a mock (PMT-Q01 default (a)). The hosted page shows every Member a banner that lists the test cards, and 'No real money moves' (AC7.10). So any Member can produce 'collected' money by typing 4242424242424242, and the commission figure is test money. The costs it is compared with are real: Staff THB 8,400.00, the Operator THB 3,500.00 and hosting. A staffed 4-week run with mock payments takes real costs and no real revenue, so the test can pass or fail without saying anything about viability. 'Launch' is also never defined.
- Where it arises: PRD.md; BUSINESS_MODEL.md; OPEN_QUESTIONS.md, PRD.md section 1 Goal, target (1) (line 22); BUSINESS_MODEL.md section 6 'The v1 success test' (line 161) and section 7 risk 'Mock payment and mock lock' (line 182); OPEN_QUESTIONS.md PMT-Q03 and PMT-Q04 defaults (lines 204, 214). Against PRD section 3 'Real payments' (line 67), AC7.1 (test-card banner), AC7.10, BUSINESS_MODEL section 4 'Card fees' (line 97), ADR-0018.
- Options: (a) keep the current text; (b) apply the reviewer's fix: In PRD section 1 target (1), BUSINESS_MODEL section 6 and the PMT-Q03/PMT-Q04 defaults: define 'launch' as the first day a real provider collects money (PMT-Q01 option (b)), and say that target (1) applies only from then. Give v1, while the checkout is a mock, a target it can measure. Example: in the all-bookings list, confirmed pay-coverage hours per staffed room by start week, at or above the break-even hours (47 h each for Meeting Room A and Board Room at the default). Alternatively, state that v1 has no business success test, only target (2) and the e2e suite. Add 'success target needs real payments' to the section 7 mock-payment risk row.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, major).

### PMT-Q07 M3 round 5: The default staffing breaks the rule the doc uses to exclude Focus Pod

- Question: The default staffing breaks the rule the doc uses to exclude Focus Pod 1. Focus Pod 1 is excluded because its door never pays for itself. Meeting Room A's door pays for itself only from 70 of 84 h (83%). But the default target assumes 47 h in each room (56%), and the doc admits even 56% is unproven. At that mix, Meeting Room A earns THB 2,820.00 (47 h x THB 60.00) against its THB 4,200.00 door, which loses THB 1,380.00 a week. Board Room covers the gap, and the default only just passes (THB 12,220.00 against THB 12,172.00). Option (e) for Meeting Room A, which the doc already lists, costs less: the host staffs it from its 80% (THB 240.00 an hour, so it covers its door from 17.5 h), and the platform staffs only Board Room. Platform cost is then THB 7,972.00, break-even at an equal mix is 31 h in each room (37%), and the same 47/47 week gives a surplus of THB 4,248.00 instead of THB 48.00. The success target is therefore set by a default that the doc's own figures show is the more expensive choice.
- Where it arises: BUSINESS_MODEL.md; PRD.md; OPEN_QUESTIONS.md, BUSINESS_MODEL.md section 6 contribution table row 'Meeting Room A' (line 145), default (line 149), break-even row 'Board Room and Meeting Room A equally' (line 155), success test (line 161); PRD.md section 1 target (1) (line 22); OPEN_QUESTIONS.md PMT-Q04 default (line 214). Residual of round 4 #1.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Use the same rule for every door: the platform staffs a door only where that room's commission covers the door at the assumed occupancy. Either make the default 'platform staffs Board Room; Meeting Room A and Focus Pod 1 hosts staff their own doors' (target THB 7,972.00; 31 h in each room at an equal mix, or 40 h of Board Room alone), or keep the current default and state why the platform takes on Meeting Room A's door, and that the door loses money below 70 h a week. Update section 6, the PRD section 1 target and the PMT-Q04 default to match.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, major).

### PMT-Q08 M3 round 5: The host-staffed option for Focus Pod 1 is presented as possible, but

- Question: The host-staffed option for Focus Pod 1 is presented as possible, but it can never pay. The host's best share is 84 h x THB 20.00 x 80% = THB 1,344.00 a week, and the room's whole gross is THB 1,680.00, both far below a THB 4,200.00 door. At THB 20 an hour the room's rate is lower than the THB 50.00 hourly Staff wage. No host would staff it, so 'sold only when its host staffs its door' in practice means 'never sold while a door needs Staff'.
- Where it arises: BUSINESS_MODEL.md; PRD.md; OPEN_QUESTIONS.md, BUSINESS_MODEL.md header (line 3), section 4 Staff time (line 101: 'Focus Pod 1 is sold only when its host staffs its door from its 80% share'), section 6 (line 149); PRD.md section 1 (line 22); OPEN_QUESTIONS.md PMT-Q04 default (line 214).
- Options: (a) keep the current text; (b) apply the reviewer's fix: State it in section 6 and PMT-Q04: at THB 20 an hour, Focus Pod 1 cannot carry a dedicated door for anyone (host's best THB 1,344.00, gross THB 1,680.00, against THB 4,200.00). It becomes viable only with the shared front-desk kiosk, a real lock (AXS-Q02), or a much higher rate. Under the default it is not listed in v1.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, business-owner lens, minor).

### PMT-Q09 M3 round 5: The screen table puts flashes on the wrong screen and leaves some out

- Question: The screen table puts flashes on the wrong screen and leaves some out. (1) The Space and grid row lists 'You already booked this slot', but that flash lands on the booking page (303 /bookings/<ref>, contract 5.3). (2) The same row omits the input-error flashes that do land there: 'Party size must be 1 to 6', 'Pick a start on the half hour', 'Outside opening hours 08:00-20:00', 'Book at least 60 minutes ahead', 'Book at most 30 days ahead', 'Note must be at most 500 characters', 'Pick a date from today to 30 days ahead', 'Duration must be 1 to 8 blocks'. It also omits the from-deadline 409 flash, which it lists only as banner text. (3) The Booking row lists none of the flashes that land on it: 'You already booked this slot', 'Time to pay has run out; cancel this hold or book again from 10:15', 'Payment is not reachable. Please try again.', 'Booking cancelled', 'This hold has already expired', 'This booking is already cancelled'. (4) The Hosted checkout row has no state for a card-field error (a flash with no data-decline-code) or for the countdown reaching zero ('Time to pay has run out', Pay disabled). A template builder working from this table would miss them.
- Where it arises: PRD.md, Section 6 Purchase table: 'Space and grid' row States (line 547), 'Booking' row (line 548); Payment table 'Hosted checkout' row States (line 561).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Move 'You already booked this slot' to the Booking row and add the listed booking-page flashes there. Add the input-error flashes and 'Time to pay has run out on BK-7KQ2M9; cancel it, or try again from 10:15' to the Space and grid row. Add to the Hosted checkout states: 'card-field error: 303 back, the message flashed with no data-decline-code, no attempt', and 'at zero: "Time to pay has run out", Pay disabled'.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, member-ux lens, minor).

### PMT-Q10 M3 round 5: The Payment operator page has no empty state and no rule that its tota

- Question: The Payment operator page has no empty state and no rule that its totals markers always exist. With no session yet (a fresh Payment database in the Payment repo's own tests, or the first e2e read), nothing says whether the page shows THB 0.00 or omits the totals. The e2e harness asserts totals as before-and-after deltas and needs a 'before' value. The Purchase dashboard pins 'always present, 0 when empty' for its markers, but data-collected-satang, data-refunded-satang, data-net-satang and data-commission-satang do not. The PRD Operator page row also lists no 401 state and no empty state.
- Where it arises: RULES.md, PMT-R17 Rule and rows (lines 1411-1431); contracts/purchase-payment.md 4.7 (line 223) and section 8 totals row; contracts/openapi/payment.yaml operatorPage; PRD.md section 6 Payment Operator page row (line 562).
- Options: (a) keep the current text; (b) apply the reviewer's fix: In PMT-R17, purchase-payment.md 4.7 and section 8, and payment.yaml, add: 'With no session: "No payments yet"; collected, refunded, net and commission THB 0.00; the four data-*-satang markers are always present, "0" when empty'. Add a PMT-R17 boundary row for an empty database. In the PRD row add '401 with a Basic challenge' and the empty state.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

## Access

### AXS-Q01 Cleaning buffer and early entry

- Question: Should rooms have a cleaning gap between bookings, and may a Member enter before the start?
- Where it arises: AXS-R13 (check-in window), AXS-R03 (Access stores the window as sent); D6 (buffer), D21 (early-entry formula). The Purchase side is PUR-Q01.
- Options: (a) no buffer and no early entry; (b) a buffer B, with Purchase sending valid_from = start − min(B, 15 min); (c) a fixed early-entry allowance without a buffer.
- Default that applies: Default is buffer 0 (D6) and the window [start, end), so no early entry (D21). Access needs no change for option (b), because it only checks the valid_from it receives.
- Reversal cost: None for Access. Medium for Purchase (availability and valid_from).
- Owner: Course instructor (business stakeholder); Purchase sets the buffer.
- Class source: Q03 (turnover time, course instructor, base a853795), in ID_MAP.md; continued as PUR-Q01.

### AXS-Q02 Real door-lock integration

- Question: Should an ok check-in open a real door lock, and what happens when the lock fails?
- Where it arises: AXS-R13 and AXS-R14 (the ok result), AXS-R16 (checked_in), AXS-T17 (mock lock); course [extraction site] "Payments and locks remain mocked."; course [syllabus site] "enter through API-driven locks". The Purchase side (what Purchase sends) is PUR-Q06.
- Options: (a) keep the mock; (b) on ok, Access calls a lock API for the room and records the lock outcome apart from the scan; (c) each lock pulls the valid codes for its room.
- Default that applies: Default is the mock. ok shows "Door unlocked (mock)"; no call leaves Access; a stored grant or an ok scan is not evidence that a door opened.
- Reversal cost: High. Access would start making outbound calls (today it calls no one), need a room-to-lock mapping, a lock outcome field, failure handling and a new ADR.
- Owner: Course instructor (Integrations/Locks scope) and project team.
- Class source: PAY-R04 Next use "door-lock integration design" (class rules PR #12, 1c8ce57); PAY-T04 "mocked lock integration" (class rules PR #1, 0326c8c).

### AXS-Q03 Sending the e-ticket by email

- Question: Should the Member get the e-ticket or a booking confirmation by email?
- Where it arises: AXS-R09 (bearer ticket link), AXS-T18 (Access holds no email).
- Options: (a) no email: the Member opens the ticket from the Purchase booking page; (b) Purchase emails the ticket_url; (c) Access emails the ticket, which needs the email address that Access does not hold.
- Default that applies: Default is no email in v1. The Member reaches the ticket through "View e-ticket" on the booking page and My bookings. The ticket shows no email.
- Reversal cost: Medium: an email sender, a template and a privacy decision. Option (c) also changes the purchase→access contract.
- Owner: Project team.
- Class source: Q-ACC-2 asks whether an email must be confirmed (ID_MAP.md; its email half continues as PUR-Q04); no Access question.

### AXS-Q04 Limits on failed Staff sign-ins and repeated unknown codes

- Question: Should the kiosk lock out after failed STAFF_PASSWORD attempts, or slow down after many unknown_code scans?
- Where it arises: AXS-R11 (Staff sign-in), AXS-R12 (normalisation), AXS-R15 (scan log). Member logins are PUR-Q05.
- Options: (a) no limits; (b) lock out after N failed sign-ins; (c) slow down after N unknown_code scans per room per minute.
- Default that applies: Default is no limits in v1. One shared STAFF_PASSWORD, compared in constant time. Every scan is logged, so a guessing run is visible, and there are about 6.6 × 10^11 possible codes.
- Reversal cost: Low: a counter and a message.
- Owner: Project team (security lens in M3).
- Class source: none. Related: Q-ACC-4 (Member failed logins, class rules PR #10 at d68631f) continues as PUR-Q05 (ID_MAP.md).

### AXS-Q05 Changing a grant, restoring a revoked one, or revoking alone

- Question: Can a grant's room or window change, can a revoked grant be restored, or can access be revoked while the booking stays confirmed (the course's "Revoke access" case)?
- Where it arises: AXS-R01 (a repeat returns the stored grant unchanged), AXS-R02 and AXS-R17 (revoked is final); D18 (unsupported cases); the [contexts site] illustration offers "Revoke access" and "Restore access".
- Options: (a) unsupported: cancel and book again; (b) an update call that changes the window or room and keeps the code; (c) an un-revoke call; (d) a Purchase action that revokes access and keeps the booking confirmed.
- Default that applies: Default is unsupported, as D18 records (no reschedule, no partial cancel). A repeat POST /grants returns the stored grant unchanged, revoked is final, and a new booking gets a new booking reference, grant and code. Revoking access alone, with the booking kept confirmed, is unsupported: Purchase revokes only inside a cancel (D19) or after a paid held cancel (D18), so to stop entry the booking is cancelled under D18.
- Reversal cost: Medium: a new endpoint, a new state transition, contract v2 and Purchase changes.
- Owner: Project team with the course instructor (cancellation scope).
- Class source: None.

### AXS-Q06 What a no-show changes

- Question: Should a no-show have any consequence: release the room early, a fee, a smaller refund, or a dashboard metric?
- Where it arises: AXS-T05 (derived grant condition), AXS-R16 (grant states).
- Options: (a) none: derived and shown only; (b) release the rest of the slot after N minutes without a check-in; (c) count no-shows on the Operator dashboard.
- Default that applies: Default is no consequence. Access derives no-show on read and stores nothing; the booking stays confirmed; the refund does not change; the D24 metrics leave it out; a Member cancel after the start stays unsupported (D18).
- Reversal cost: Medium to high. Releasing a slot needs Access to tell Purchase, which breaks "Access never calls anyone"; a metric needs Purchase to read it from Access.
- Owner: Project team, with the course instructor (business stakeholder).
- Class source: None.

### AXS-Q07 Order of the kiosk checks

- Question: When a scan fails more than one check, which answer does the kiosk give?
- Where it arises: AXS-R14 (check order), AXS-R13 (window). D21 and the kiosk design list the checks (code, room, window and revocation) but set no order.
- Options: (a) unknown_code, revoked, wrong_room, then the window; (b) unknown_code, wrong_room, revoked, then the window, so a scan at another room never reveals that a ticket was cancelled; (c) unknown_code, then the window first.
- Default that applies: (a). A cancelled ticket answers revoked wherever it is scanned, so Staff can tell the holder at once. Trade-off: Staff at any room learn that a code belongs to a cancelled booking.
- Reversal cost: Low: the order of four checks and their tests.
- Owner: Project team.
- Class source: none.

### AXS-Q08 M3 round 5: The kiosk and the e-ticket both live in Access. If Access is down, or

- Question: The kiosk and the e-ticket both live in Access. If Access is down, or the kiosk browser cannot reach it, during opening hours, Staff cannot check any code and Members cannot open /t/ tickets. No doc defines what Staff do then. The lock is a mock, so Staff will improvise: they admit on a screenshot or turn paying Members away, and no scan is logged. BUSINESS_MODEL section 8 also misleads: an Access outage is absorbed only at issuance ('being prepared'). At the door it stops every check-in. The PRD records neither the case nor a recovery path, and no open question covers it.
- Where it arises: BUSINESS_MODEL.md, Section 8 'Failure modes' row (line 196: 'only an Access outage is absorbed ("being prepared")'); PRD.md section 3 'Not in v1' table (lines 63-89) and section 6 Kiosk row (line 569); contracts/purchase-access.md section 4.6 (lines 153-180); OPEN_QUESTIONS.md Access section (no question).
- Options: (a) keep the current text; (b) apply the reviewer's fix: Add a PRD section 3 'Not in v1' row, 'Check-in while Access or the kiosk is down'. Staff phone the Operator, who is already on call (BUSINESS_MODEL section 4). The Operator finds the booking in All bookings by the reference the Member reads from Purchase's booking page, which stays up. The Operator confirms the room, the time, status confirmed and no 'Revocation pending'. Staff then admit by hand, and nothing is logged in Access. Record this as a new AXS-Q08 with options: (a) manual admit through the Operator (the default); (b) a printed per-room day list taken from All bookings; (c) no entry. Correct the BUSINESS_MODEL section 8 cell to: 'an Access outage is absorbed at booking time ("being prepared"); at the door it stops every check-in and every e-ticket view until Access is back'.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, major).

### AXS-Q09 M3 round 5: The kiosk page when rooms exist but none is selected (first open, or a

- Question: The kiosk page when rooms exist but none is selected (first open, or after the browser restarts, since access_session lasts until the browser closes) is undefined. The docs do not say whether the code input shows, or which scans the 'last 10 scans at that room' list shows when there is no room. Builders will differ: one shows a code input that always answers 'Select the room first', another shows scans from every room. AXS-R15 limits the list to the selected room, so a list across rooms would also widen what an unattended kiosk reveals.
- Where it arises: contracts/purchase-access.md, Section 4.6 GET /checkin (line 157); RULES.md AXS-R11 Rule (line 1739) and AXS-R15 Rule (line 1838); contracts/openapi/access.yaml showKiosk.
- Options: (a) keep the current text; (b) apply the reviewer's fix: Pin it in AXS-R11, 4.6 and showKiosk: 'Rooms exist, none selected: the room picker with "Select your room", no code input and no scan list; data-selected-space-id absent'. Add an AXS-R11 boundary row: Staff opens /checkin in a new browser, sees the picker only, then selects Meeting Room A and sees the code input and the last 10 scans.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).

### AXS-Q10 M3 round 5: The PRD screen list has drifted from the contract. All bookings omits

- Question: The PRD screen list has drifted from the contract. All bookings omits the 'Cancelled 2026-10-05 11:00' (cancelled_at) column that contract line 105 gives a cancelled row. Spaces admin says only 'Create, edit, archive' and omits the room-number label 'Meeting Room A (room 1)' that contract line 110 gives so the Operator can match the kiosk. The Kiosk states list 'No room selected' but not the flash 'Select the room first', which AXS-R11, AC23.3 and 4.6 require. A tester working from the PRD screen list misses these.
- Where it arises: PRD.md, Section 6 Purchase rows 'All bookings' (line 552) and 'Spaces admin' (line 553); Access row 'Kiosk' (line 569).
- Options: (a) keep the current text; (b) apply the reviewer's fix: All bookings row: add 'a cancelled row shows "Cancelled 2026-10-05 11:00"'. Spaces admin row: add 'each space labelled with its room number, "Meeting Room A (room 1)", as the kiosk shows it'. Kiosk row: add the flash 'Select the room first'.
- Default that applies: The current text stands until the project team decides; the implementation follows the current rules and contracts.
- Reversal cost: Low to medium; a docs change plus the matching code and test change.
- Owner: Project team.
- Class source: none (M3 round 5, operator-staff lens, minor).
