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
- Default that applies: free when the price is 0, else plan when plan_active is true, else pay. Both skip Payment; only the label and plan-usage figures differ. D10 names both conditions but not their order.
- Reversal cost: Low. A label and a metric filter.
- Owner: Project team.
- Class source: none.

### PUR-Q09 Payment unreachable when the hold is created

- Question: What happens to a held booking when POST /payment-sessions fails or times out, so the booking has no payment session?
- Where it arises: PUR-R21 (hold), PUR-R23 (session request), PUR-R24 (reconciliation), PUR-R31 (held cancel).
- Options: (a) keep it held and retry on "Continue to payment"; (b) cancel it at once; (c) keep retrying in the background.
- Default that applies: (a), for a timeout or connection error (PUR-R35): the booking stays held without a session, and "Continue to payment" for the same space and time repeats the request (PUR-R21, PUR-R23). Without a session it is expired on lapse or cancelled on cancel with no Payment call (PUR-R24, PUR-R31), and from expires_at no session is requested (PUR-R40).
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
- Default that applies: (a): today and the 6 dates before it, with each booking counted by its start; PUR-R34 gives the bounds, the rounding and the examples.
- Reversal cost: Low. Query bounds only.
- Owner: Project team.
- Class source: none (the counting questions MET-Q01, Q-MET-1 and Q-MET-2 are answered by D24).

### PUR-Q12 Revocation pending while the slot is rebooked

- Question: Step 1 of a confirmed cancel frees the slot. If the revoke in step 2 got no answer, Access still answers ok for the old ticket code. If another Member books the freed slot, the kiosk admits both parties. What should prevent that?
- Where it arises: PUR-R32 (rows 3 and 6), PUR-R12 (a cancelled booking is not slot-blocking), AXS-R13 (the old code still opens).
- Options: (a) accept the risk and make the pending revoke visible; (b) also retry the pending revokes of that space in the pre-insert sweep (PUR-R22); (c) keep the slot blocked until the revoke succeeds, which changes the D11 predicate.
- Default that applies: (a), as D19 stands. The Operator's all-bookings list flags "Revocation pending", and a pending revoke is retried on the booking page or by the Operator's Retry (PUR-R32). The refund waits for the revoke (PUR-Q10), so no money moves while the old code still opens.
- Reversal cost: Low for (b): one more step in the sweep. Medium for (c): the slot-blocking predicate, the EXCLUDE constraint and the grid change.
- Owner: Project team.
- Class source: none.

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
- Where it arises: PMT-R16, PMT-R17; D19 (only the operator starts attempt+1).
- Options: (a) only a later succeeded refund attempt clears the label; (b) a "settled outside" action on the Payment operator page, with a note; (c) automatic retries by Payment.
- Default that applies: (a). The label "needs manual follow-up" stays until a later refund attempt for the same session succeeds (the Operator's Retry in Purchase sends attempt+1, D19). Payment has no manual settle action and never retries on its own.
- Reversal cost: Low. (b) adds one column, one button and a "settled outside" line in the totals.
- Owner: Project team (business owner lens).
- Class source: none.

### PMT-Q03 Which period do the money totals cover?

- Question: Should the totals on Payment's operator page use the same "last 7 Bangkok days" period as Purchase's dashboard?
- Where it arises: PMT-R17; D24 sets the period for booking metrics and says money totals are on Payment's page, but gives the totals no period.
- Options: (a) all time; (b) the last 7 Bangkok days, by payment time and refund time; (c) a date filter.
- Default that applies: (a). All-time totals since the first record. D24's 7-day period applies to Purchase's booking metrics only.
- Reversal cost: Low: one filter and a label.
- Owner: Project team.
- Class source: none.

### PMT-Q04 Who pays hosts, and when is commission earned?

- Question: The marketplace earns a 20% commission (D25). Should Payment record host payouts? Is commission earned when the Member pays or when the booking ends?
- Where it arises: PMT-R17, PMT-T16.
- Options: (a) an estimate only; (b) a payouts ledger in Payment; (c) a separate payouts context.
- Default that applies: (a). "Estimated platform commission (20% of net)" is display only. Host payouts are out of scope (D25). Nothing is paid out and no ledger exists.
- Reversal cost: High for (b) or (c): new tables, a money-out flow, a new contract and new totals.
- Owner: Course instructor for scope; Project team.
- Class source: none.

### PMT-Q05 May anyone with the payment link pay?

- Question: The hosted page /pay/{id} works without a login. Anyone who has the link sees the amount and booking reference and can pay. Is that acceptable?
- Where it arises: PMT-R07, PMT-R01, PMT-T02.
- Options: (a) a bearer link with an unguessable session ID; (b) a short-lived signed token from Purchase in the URL; (c) a login on Payment.
- Default that applies: (a), like a hosted checkout link. The session ID carries 128 random bits, reaches only the Member's browser by redirect, and stops taking payments at expires_at (13 minutes after creation at most). Paying someone else's session only pays their booking. Payment has no Member accounts (account data lives on Member in Purchase).
- Reversal cost: Low for (b): Purchase adds a token and Payment checks it. High for (c): Payment would need accounts.
- Owner: Project team (security lens).
- Class source: none.

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
