# Class rules record: main and PRs #1, #3-#15

Repo `cs403bkk-2026/spacey-business-rules`, main `58a1477` (includes merged PRs #1, #3, #14). PR #2 does not exist. Spacey evidence pin `e734fc7`; Spacey seed `5a1cf3d`. Full SHAs are in [`../SOURCES.md`](../SOURCES.md).

Read-only commands only: `gh pr list/view/diff`, `gh api .../pulls/<n>/comments` (GET), `git show/log/diff` in the fresh clone. Trial merges (`git merge-file`, `patch --dry-run`) ran on scratch copies, never in the clone.

Conventions:
- People are roles. `[role]` or `[Member A]` inside a quote marks a replaced name. Example people in rule tables become Member A / B / C.
- "As written" columns repeat the PR text. They are the PR's claim, not project policy and not verified fact.
- Run results that a PR author or reviewer claims are theirs. We did not re-run them unless a row says "test run".
- Line numbers inside quotes (e.g. "L745-L771") are `e734fc7` lines, as the PRs cite them.

## 1. Summary

What each PR head contains. "Branched from" is the newest commit of `origin/main` found in `git log origin/pr/<n>`. The trial merge is our `git merge-file` of the PR head onto main tip `58a1477`, on scratch copies of `git show` blobs; the number is conflict hunks per file.

| PR | Title | Head | Branched from | Files (+/-) | Trial merge onto main (ours) | Evidence |
|---|---|---|---|---|---|---|
| #1 | "Add payment glossary terms and rules" | `0326c8c` | `a853795` | GLOSSARY +11, RULES +51 | n/a (merged) | class PR #1 diff at 0326c8c |
| #3 | "docs(glossary,rules): add Guest / Account-linked booking terms and EX-R04" | `6752b24` | `1124404` | GLOSSARY +3 -1, RULES +16 | n/a (merged) | class PR #3 diff at 6752b24 |
| #4 | "Document booking prices, rounding and stored amounts" | `9478b3e` | `1124404` | GLOSSARY +9, RULES +46 | clean; gives two `PRC-T02` rows | class PR #4 diff at 9478b3e |
| #5 | "Add Space deletion constraint rule (EX-R05)" | `0712a1c` | `a853795` | RULES +22 | 1 conflict (RULES) | class PR #5 diff at 0712a1c |
| #6 | "Add SLOT glossary terms and rules: unpaid bookings hold slots; cancellation frees them" | `c18b638` | `a853795` | GLOSSARY +10, RULES +54 | 2 conflicts (GLOSSARY 1, RULES 1) | class PR #6 diff at c18b638 |
| #7 | "[Add] Add term counted member and count rules" | `05e90b3` | `a853795` | GLOSSARY +8, RULES +30 | 2 conflicts (GLOSSARY 1, RULES 1) | class PR #7 diff at 05e90b3 |
| #8 | "Add dashboard metrics terms and rules" | `ce99d13` | `a853795` | GLOSSARY +2, RULES +35 | 2 conflicts (GLOSSARY 1, RULES 1) | class PR #8 diff at ce99d13 |
| #9 | "Time Glossary and Rule" | `9afd71f` | `a853795` | GLOSSARY +11 -4, RULES +34 -16 | 2 conflicts (GLOSSARY 1, RULES 1) | class PR #9 diff at 9afd71f |
| #10 | "Add account and login-session terms and rules" | `d68631f` | `1124404` | GLOSSARY +9, RULES +65 | clean | class PR #10 diff at d68631f |
| #11 | "Add party size and capacity rule" | `7cf2656` | `1124404` | GLOSSARY +11 -2, README +1 -1, RULES +17 -16 | 1 conflict (RULES) | class PR #11 diff at 7cf2656 |
| #12 | "Access code is generated once and stored" | `1c8ce57` | `1124404` | RULES +29 | clean | class PR #12 diff at 1c8ce57 |
| #13 | "Add space availability terms and rules" | `c8a302f` | `1124404` | GLOSSARY +9, RULES +26 | clean onto main; conflicts with #15 (GLOSSARY 1, RULES 1) | class PR #13 diff at c8a302f |
| #14 | "Clarify booking price and Purchase calculation ownership" | `25ca71e` | `81e490e` | GLOSSARY +8 -1, RULES +36 | n/a (merged) | class PR #14 diff at 25ca71e |
| #15 | "Add availability search glossary terms and rules" | `9e4971a` | `1124404` | GLOSSARY +10, RULES +43 | clean onto main; conflicts with #13 | class PR #15 diff at 9e4971a |

State, reviews and GitHub's mergeable flag, from `gh pr view`, `gh pr list` and `gh api .../pulls/<n>/reviews`, `.../pulls/<n>/comments`, `.../issues/<n>/comments` (GET) on 2026-10-01; states unchanged since 2026-09-30. The merge commits of #1, #3 and #14 on main are in section 18.

| PR | State | Reviews | GitHub mergeable | Evidence |
|---|---|---|---|---|
| #1 | MERGED 2026-09-30 02:15:48 UTC | one class reviewer: CHANGES_REQUESTED twice, then APPROVED; 3 inline comments | - | class PR #1 discussion |
| #3 | MERGED 2026-09-30 06:41:45 UTC | two class reviewers: COMMENTED once each; 2 inline and 1 conversation comment (one of them) | - | class PR #3 discussion |
| #4 | OPEN | one class reviewer: APPROVED twice; 1 conversation comment by the author | MERGEABLE | class PR #4 discussion |
| #5 | OPEN | none | CONFLICTING | class PR #5 discussion |
| #6 | OPEN | class reviewer 1: APPROVED and COMMENTED (7 inline), both on `afb5b9f`; class reviewer 2: APPROVED on `c18b638` | CONFLICTING | class PR #6 discussion |
| #7 | OPEN | none | CONFLICTING | class PR #7 discussion |
| #8 | OPEN | one class reviewer: COMMENTED (empty) + 1 inline; the author: COMMENTED (empty) + 1 inline reply | CONFLICTING | class PR #8 discussion |
| #9 | OPEN | 1 conversation comment | CONFLICTING | class PR #9 discussion |
| #10 | OPEN | class reviewer: CHANGES_REQUESTED + 2 inline; the author: 2 x COMMENTED (empty) with 2 inline replies; course instructor: CHANGES_REQUESTED on `bb9f346`; no re-review after the last push | MERGEABLE | class PR #10 discussion |
| #11 | OPEN | course instructor: CHANGES_REQUESTED (empty body) + 1 inline, on head `7cf2656`; no push since, so unaddressed | CONFLICTING | class PR #11 discussion |
| #12 | OPEN | none | MERGEABLE | class PR #12 discussion |
| #13 | OPEN | none; empty body | MERGEABLE | class PR #13 discussion |
| #14 | MERGED 2026-09-30 08:16:49 UTC | class reviewer: APPROVED (no text) | - | class PR #14 discussion |
| #15 | OPEN | none; empty body | MERGEABLE | class PR #15 discussion |

## 2. Main at 58a1477

### Timeline

| Time (UTC) | Commit | What | Evidence |
|---|---|---|---|
| 2026-09-29 08:35-08:39 | `bd1aa31`..`a853795` | Course instructor creates README, GLOSSARY, RULES (EX-T01, EX-T02, EX-R01, EX-R02, template) | source inspected at 58a1477 |
| 2026-09-30 02:15 | `1124404` | PR #1 merged | source inspected at 58a1477 |
| 2026-09-30 06:41 | `5d23e9f` | PR #3 merged | source inspected at 58a1477 |
| 2026-09-30 06:59 | `81e490e` | Direct push, no PR: "Update RULES according to the template.md". Renames rule fields of EX-R01, EX-R02, PAY-R01..R03, EX-R04 to template names; adds Policy status and Next use to PAY-R01..R03; turns "Question Q01/Q03/Q05" into "Open question". | source inspected at 58a1477 |
| 2026-09-30 08:14 | Spacey `5a1cf3d` | Spacey PR #196 "Extract booking price calculation into Purchase" merged (cited by PR #14) | class PR #14 discussion |
| 2026-09-30 08:16 | `58a1477` | PR #14 merged | source inspected at 58a1477 |

Main holds only `GLOSSARY.md`, `README.md`, `RULES.md` in every ref. The README links `DOMAIN_MODEL.md` ("begin with the glossary and EX-R01/EX-R03"), `CHANGE_EXAMPLE.md` and `RULE_TEMPLATE.md`, and anchors such as `DOMAIN_MODEL.md#6-booking-cancellation-journey`. None of these files exists in any ref (source inspected at 58a1477).

### IDs on main

| ID | Kind | Title on main | Context on main | Policy status as written | Added by | Evidence |
|---|---|---|---|---|---|---|
| EX-T01 | term | Member | Shared journey | "working proposals" (table header) | course instructor | source inspected at 58a1477 |
| EX-T02 | term | Space | Purchase | "working proposals" | course instructor | source inspected at 58a1477 |
| EX-T08 | term | Guest | Shared journey | "working proposals" | PR #3 | source inspected at 58a1477 |
| EX-T09 | term | Account-linked booking | Shared journey | "working proposals" | PR #3 | source inspected at 58a1477 |
| PRC-T02 | term | Booking price | Purchase | linked to the stakeholder-clarified booking-price rule | PR #14 | source inspected at 58a1477 |
| PAY-T01..T04 | term | Paid; Member name; Subscription; Access code | (no Context column in the PAY- table) | "**observed implementation**" | PR #1 | source inspected at 58a1477 |
| EX-R01 | rule | Party size within capacity | - | "proposed; exclusive-space/group-booking interpretation needs stakeholder confirmation." | course instructor | source inspected at 58a1477 |
| EX-R02 | rule | Valid interval and no overlap | - | "observed; intended turnover policy unresolved" | course instructor | source inspected at 58a1477 |
| PAY-R01 | rule | A subscriber's booking starts as paid | - | "observed." | PR #1 | source inspected at 58a1477 |
| PAY-R02 | rule | Payment requires syntactically valid card details | - | "observed." | PR #1 | source inspected at 58a1477 |
| PAY-R03 | rule | An access code needs only a paid booking | - | "observed." | PR #1 | source inspected at 58a1477 |
| EX-R04 | rule | Guest vs. account-linked booking is decided once, at creation | - | "observed; whether non-owner access on those other endpoints is intended is unresolved." | PR #3 | source inspected at 58a1477 |
| (no ID) | rule | "Booking price — Purchase rule clarification" | Purchase | "stakeholder-clarified for this calculation and its Purchase ownership by [course instructor], 30 September 2026" | PR #14 | source inspected at 58a1477 |

Referenced on main but defined nowhere: EX-T03 and EX-T04 (via "EX-T02–EX-T04" in EX-R02), EX-T06 and EX-T07 (EX-R01 "EX-T02, EX-T06, EX-T07"), EX-R03 (README). PRC-R01 is referenced on main but defined only in open PR #4 (source inspected at 58a1477).

EX-R01 and EX-R02 on main cite evidence under the repo's old name `cs403bkk-2026/startup-app/blob/e734fc7...`; a GET of `repos/cs403bkk-2026/startup-app` returns `cs403bkk-2026/spacey` (renamed). All PRs cite `cs403bkk-2026/spacey` (source inspected at 58a1477).

## 3. PR #1 — payment terms and rules (merged)

Body, as written: "all describing what the Spacey code does today. No new policy is adopted." / "All statements are **observed implementation** at Spacey commit `e734fc7`" / "Related tests were read but **not run**." (class PR #1 discussion)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| PAY-T01 | term | Paid | Yes/no mark on a booking; yes after card payment, or at once for a subscriber. "So "paid" does not always mean money was taken." | "observed implementation" (section header) | none | "source inspection unless stated" at `e734fc79...` | none (PR body, numbered question 1: "**Is "paid" the right word?**") | class PR #1 diff at 0326c8c |
| PAY-T02 | term | Member name | Typed name on a booking; empty becomes `"guest"`; trimmed and lower-cased for subscription lookup. "Not a login." | observed implementation | none | app.py L794 (API), L805 (form), L262-L273 at `e734fc7` | none (PR body, numbered question 3: "**Member name.** It is typed text, not a login.") | class PR #1 diff at 0326c8c |
| PAY-T03 | term | Subscription | "A record saying a name is subscribed", created by `POST /members/<name>/subscribe`; mocked | observed implementation | none | app.py L1010-L1031 at `e734fc7` | "No price, no end date, no way to cancel. It is unclear what it covers." | class PR #1 diff at 0326c8c |
| PAY-T04 | term | Access code | "A random 8-character code given when a paid booking is unlocked"; "mocked lock integration" | observed implementation | none | app.py L990-L991 at `e734fc7` | Boundary: "It is not saved, so asking again gives a new code." | class PR #1 diff at 0326c8c |
| PAY-R01 | rule | A subscriber's booking starts as paid | Active subscription for the name at creation gives paid, amount 0, no card; else unpaid. Checked only at creation. | head: "Statement (observed implementation)"; main: "observed." | none | `is_subscribed` L266-L273, `book_space` L745-L771; tests L1302-L1339 "read, not run" | "Should subscriptions depend on a real account? What does a subscription cover, and can it end?" Next use: "subscription and booking contract; account model decision." | class PR #1 diff at 0326c8c |
| PAY-R02 | rule | head: "Paying needs a card that looks valid"; main: "Payment requires syntactically valid card details" | Card 13-19 digits, CVC 3-4, expiry MM/YY not past; mocked; last 4 stored; paying a paid booking returns it unchanged with no card check | head: "Statement (observed implementation)"; main: "observed." | none | `validate_card` L243-L259, `mark_booking_paid` L938-L974. Author: "**Run by me:** `validate_card` on its own (copied out of `app.py`, no database)". Tests L689-L830 "read, not run". | "a booking with amount 0 still starts unpaid and needs a card (not tested). Should it? What should a real payment check?" Next use: "payment API contract and future payment-provider integration." | class PR #1 diff at 0326c8c |
| PAY-R03 | rule | An access code needs only a paid booking | Unlock returns a new random code if the booking exists and is paid; 402 unpaid; 404 unknown; no owner or time check | head: "Statement (observed implementation)"; main: "observed." | none | `issue_access_code` L976-L991 "(it reads only the booking's `id` and `paid`)"; tests L913-L935 "read, not run" | main: "what additional conditions, if any, should be required before an access code is issued (booking time, booking owner, previous issuance)?" Next use: "access-control contract and authorization requirements." | class PR #1 diff at 0326c8c |

Key example rows (Member A subscribed, Member B not):

| Rule | Given | When | Result as written | Evidence |
|---|---|---|---|---|
| PAY-R01 | Member B has an unpaid booking | Member B subscribes afterwards | "That booking stays unpaid (subscription is checked only at creation)" | class PR #1 diff at 0326c8c |
| PAY-R01 | "guest" is subscribed | booking with no name | "Paid, amount 0 (the name becomes "guest") †" († = read, not run) | class PR #1 diff at 0326c8c |
| PAY-R02 | an already-paid booking | pay again, no card | "200, returned unchanged" | class PR #1 diff at 0326c8c |
| PAY-R02 | unpaid booking, amount 0 | pay with no card | "Card details are still required †" | class PR #1 diff at 0326c8c |
| PAY-R03 | paid booking unlocked once | unlock again | "200, a different code †" | class PR #1 diff at 0326c8c |
| PAY-R03 | paid booking that ended last week | unlock | "200, a code †" | class PR #1 diff at 0326c8c |

### IDs referenced, not defined here

| ID | Where | Defined elsewhere | Evidence |
|---|---|---|---|
| EX-T01 | PAY-T02 "Compare EX-T01" | main (course instructor) | class PR #1 diff at 0326c8c |

### Review points by role

| Role | Point | Verbatim | Evidence |
|---|---|---|---|
| class reviewer (CHANGES_REQUESTED) | Example format | "Rewrite Example/Boundary in RULES.md. Use a Given/When/Result table so a reader can predict outcomes without parsing sentences." | class PR #1 discussion |
| class reviewer (inline, PAY-R02 amount-0 row) | 0-amount still needs a card; treated as intended "for now" (a reviewer's opinion, not a stakeholder decision) | "The code in [`mark_booking_paid`](.../e734fc79.../app.py#L938-L974) shows that we check only card exists. It doesn't check amount at all. IDK let's say it's intended feature for now." | class PR #1 discussion |
| class reviewer (inline, PAY-R03) | Ambiguous "code" (access code vs HTTP status); suggestion applied on main | "`code` here means "access code" (your PAY-T04 in GLOSSARY.md). Worth renaming/clarifying in the text" | class PR #1 discussion |
| class reviewer (inline, PAY-R03 repeat-unlock row) | Codes are not stored | "Well, the code isn't stored in the first place. I don't even know how they compare the unlock code. it just regenerate every time we post the unlock api." | class PR #1 discussion |
| class reviewer | Pinned evidence: both inline comments link permalinks at `e734fc79bbb72341407f7decd7030fd47ea6a151` | (links) | class PR #1 discussion |
| class reviewer (APPROVED) | Approval | "LGTM" | class PR #1 discussion |

Not raised in #1: account-data ownership, contexts, time zones, separate JSON/form rows.

## 4. PR #3 — Guest and account-linked booking (merged)

Body: "Cited tests were **read, not executed** ... Labelled as source inspection throughout, not a runtime pass." (class PR #3 discussion)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| EX-T08 | term (context "Shared journey") | Guest | "Booking made with no session logged in at creation; `user_id` stays NULL forever." | section: "working proposals unless explicitly linked to a stakeholder clarification" | none | none on the row | Boundary: "guest status is about session state, not the name." | class PR #3 diff at 6752b24 |
| EX-T09 | term (context "Shared journey") | Account-linked booking | "A booking whose `user_id` was set from the session at creation, pointing at `users(id)`." | as EX-T08 | none | none on the row | Boundary: "Only `/bookings/mine` and creation check it; every other booking endpoint works for anyone holding the booking_id." | class PR #3 diff at 6752b24 |
| EX-R04 | rule | Guest vs. account-linked booking is decided once, at creation | `user_id` from the session at creation, never backfilled; only `/bookings/mine` checks ownership; get-by-id, pay, unlock, cancel, list-by-space work for anyone with the id | "observed; whether non-owner access on those other endpoints is intended is unresolved." | none; question owner "business stakeholder" | `user_id` app.py L745-L771, `/bookings/mine` L877-L895 at `e734fc79...`; "Source inspection, not a runtime pass."; tests L1134-L1153 "read, not executed" | head "Question Q05" (number dropped on main): "is it intended that only `/bookings/mine` gates by ownership while pay/cancel/unlock/get-by-id don't check who's asking? Should a guest booking ever become claimable after registering/logging in?" | class PR #3 diff at 6752b24 |

### IDs referenced, not defined here

| ID | Where | Defined elsewhere | Evidence |
|---|---|---|---|
| EX-T01 | EX-R04 Terms | main | class PR #3 diff at 6752b24 |
| Q05 | EX-R04 question label | label only; dropped on main by `81e490e` | class PR #3 diff at 6752b24 |

Numbering: #3 starts at EX-T08, skipping EX-T03..T07.

### Review points by role

| Role | Point | Verbatim | Outcome | Evidence |
|---|---|---|---|---|
| class reviewer (PR comment) | Ownership: add an account-linked row | "table only shows a guest booking being readable by anyone. Could you also add a row for an account-linked booking? A person who isn't logged in can still read it, and they'd see the owner's user_id too." | Addressed in `385985f` | class PR #3 discussion |
| class reviewer (inline, GLOSSARY) | EX-T09 duplicates EX-R04 | "The EX-T09 description repeats what EX-R04 already says. Maybe just say "see EX-R04" instead of writing it out twice so it easier to keep this two in sync in the future." | Not addressed | class PR #3 discussion |
| class reviewer | Approval-style comments; formal state COMMENTED | "NIce work" / "Nice catch overall" | - | class PR #3 discussion |

## 5. PR #4 — booking prices, rounding, stored amounts (open)

Body: "All claims are labelled **observed implementation** at Spacey revision `e734fc79bbb72341407f7decd7030fd47ea6a151`, with permanent source links. Intended business policy remains unresolved." / "Merge review would confirm an accurate record, not approve a pricing policy." (class PR #4 discussion)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| PRC-T01 | term | Hourly rate | A space's `price_cents`: "a non-negative whole number of cents per hour". "Omitted on space creation, it defaults to 0". | "These definitions describe **observed implementation** at Spacey revision `e734fc7…`. Intended pricing policy remains unresolved." | not written | app.py L201-L206, L222-L223, L576-L605, L938-L974 at `e734fc7` | Boundary: "A zero-rate booking can still be unpaid and require card details." | class PR #4 diff at 9478b3e |
| PRC-T02 | term | **Booking amount** | "A booking's stored total, `amount_cents`, calculated when it is created. A member with an active subscription gets amount 0 instead". | as PRC-T01 | not written | app.py L745-L771 at `e734fc7` | Boundary: "does not prove money was collected" | class PR #4 diff at 9478b3e |
| PRC-R01 | rule | Booking amounts follow duration and cent rounding | Amount = hourly rate x duration; duration truncated to whole seconds; rounded to the nearest cent, half up; only for a member without an active subscription at creation | "observed; intent unresolved. No agreed minimum charge or billing increment is established by this record." | missing | `amount_for` L201-L206, creation L745-L771, input paths L780-L816. Author ran `amount_for` extracted by AST under "Python 3.14.7; eight assertions passed". Tests L208-L251 "read, not run". | "**Question PRC-Q01:** should a positive-duration booking have a minimum charge or minimum billable duration? Should fractional seconds be discarded? What maximum rate or duration should be accepted before the stored amount overflows? Clarification owner: instructor / business stakeholder; decision unresolved." | class PR #4 diff at 9478b3e |
| PRC-R02 | rule | A later rate change preserves stored booking amounts | Stored at creation; a later rate change or the mocked payment does not recalculate; exception: startup backfill fills NULL amounts with the current `price_cents`, ignoring duration | "observed; whether the price should be fixed at booking or payment remains unresolved." | missing | L745-L771, L626-L667, L938-L974; exception L110-L115; examples "traced through source, not executed" | "**Question PRC-Q02:** should the booking-time amount remain fixed until payment? How should historical bookings with unknown amounts be recorded…? Clarification owner: instructor / business stakeholder; decision unresolved." | class PR #4 diff at 9478b3e |
| PRC-Q01, PRC-Q02 | question | (see PRC-R01, PRC-R02) | as above | - | - | - | - | class PR #4 diff at 9478b3e |

PRC-R01 rows (cents): 1500 x 1 h = 1500; rate 0 x 1 h = 0 "the booking still starts unpaid without a subscription"; 1500 x 3 h = 4500; 1500 x 30 m = 750; 1000 x 20 m = 333; 1 x 30 m = 1 ("half a cent rounds up"); 1 x 29 m 59 s = 0 ("positive duration can round to zero"); 3600 x 1.9 s = 1 ("fractional seconds are discarded first"). Storage boundary: 100-year booking at 2500 cents/h gave HTTP 500 "integer out of range" (reported by a class reviewer). No separate JSON and form rows: "Both JSON and browser bookings use the shared booking helper." (class PR #4 diff at 9478b3e)

### IDs referenced, not defined here

| ID | Defined elsewhere | Evidence |
|---|---|---|
| EX-T01, EX-T02, PAY-T01..T04 | main | class PR #4 diff at 9478b3e |

### Review points by role

| Role | Point | Verbatim | Evidence |
|---|---|---|---|
| class reviewer (APPROVED at `fbd8365`) | Zero-rate boundary | "PRC-T01: price_cents defaults to 0 when omitted (app.py L581). I ran it: a booking there gets amount_cents 0 but paid false, so it still needs a card. Worth adding as a boundary." | class PR #4 discussion |
| same | INTEGER overflow / max duration | "PRC-R01: amount_cents is a Postgres INTEGER (app.py L86-89) and there's no max duration check. I ran a 100-year booking at 2500 cents/hour: HTTP 500 \"integer out of range\", nothing stored. A one-line limit or open question is enough." | class PR #4 discussion |
| same | Reviewer's own runs | "What I verified: ran the full suite at e734fc7 (154 passed) and every PRC-R01 and PRC-R02 example through the real routes on Postgres and all matched your tables." | class PR #4 discussion |
| class contributor (author) | Did not repeat route/DB runs | "I checked the new zero-rate calculation with the pinned helper but did not repeat your route/database checks." | class PR #4 discussion |
| class reviewer (APPROVED at `9478b3e`) | Recheck; zero amount still needs a card | "Rechecked 9478b3e: the zero-rate row, card-details note and overflow boundary all match what I ran. I also ran paying the zero-amount booking with no card: 400 \"card_number must be 13-19 digits\", still unpaid." | class PR #4 discussion |

Not discussed on #4: ownership, contexts (no Context column), account data, stored codes, time zones.

## 6. PR #5 — space deletion (open)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| EX-R05 | rule | Spaces with existing bookings cannot be deleted | "A space cannot be deleted if it has any associated bookings; all such bookings must be cancelled first." | "observed; intended space retirement policy unresolved." | "unresolved." | "Source inspection of `delete_space` function in `app.py`." **No SHA, no link.** | "**Open question Q06:** How should the business handle removing a space that is no longer active but has historical bookings? The current deletion rule requires cancelling past bookings, which would destroy historical revenue records. Do we need an \"archived\" or \"inactive\" status instead of hard deletion?" Owner: "business stakeholder." | class PR #5 diff at 0712a1c |
| Q06 | question | (see EX-R05) | as above | - | - | - | - | class PR #5 diff at 0712a1c |

Other fields: Terms "EX-T02 (Space)"; Candidate responsibility "Space Management / Inventory"; Next use "Space inventory management design." Rows: no bookings, "Pass (Space is deleted)"; upcoming booking, "Reject (Error: cancel them first)"; past completed bookings, "Reject (Error: cancel them first)". No HTTP codes, no JSON/form split. (class PR #5 diff at 0712a1c)

Our cross-check: `delete_space` (L670-L688 at `e734fc7`; the 409 message is L683) returns 404 when the space is missing, 409 `"space has bookings, cancel them first"` when any booking row exists, else 204 (source inspected at e734fc7).

At Spacey main the function is L664-L682 and the 409 message is app.py:677; the body is identical to the `e734fc7` one (source inspected at 5a1cf3d).

### IDs referenced, not defined here

| ID | Defined elsewhere | Evidence |
|---|---|---|
| EX-T02 | main | class PR #5 diff at 0712a1c |

### Review points by role

| Role | Point | Verbatim | Evidence |
|---|---|---|---|
| class contributor (author, body) | No reviewer | "**🚩 Reviewer Needed:** I do not have a review partner for this PR yet." | class PR #5 discussion |
| author (body) | Question number differs from the diff (body Q07, diff Q06) | "Q07 in EX-R05: How do we \"retire\" a space…" | class PR #5 discussion |
| author (body) | Evidence kind | "Source inspection of `app.py` (`delete_space` function). Labelled as observed implementation. I did not execute a runtime pass." | class PR #5 discussion |

## 7. PR #6 — unpaid bookings hold slots; cancellation frees them (open)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| SLOT-T01 | term (context Purchase) | Unpaid booking | "A booking saved with `paid = false`. Every new booking starts this way unless the member name has an active subscription… It stays unpaid until a card payment succeeds or it is cancelled." Boundary: "**A subscriber's booking is never unpaid** (see PAY-T01 in open PR #1)." | "**observed implementation** at Spacey revision `e734fc7…`. They are not approved business policy." | not written | app.py L745-L771 at `e734fc7` | none | class PR #6 diff at c18b638 |
| SLOT-T02 | term (context Purchase) | Held slot | "The time interval of one space that an existing booking blocks… **whether the existing booking is paid or not**." Adjacent intervals are not held. | same | not written | points to SLOT-R01/R02 | none | class PR #6 diff at c18b638 |
| SLOT-T03 | term (context Purchase) | Cancellation | "`DELETE /bookings/<id>`: the booking row is permanently deleted… It is the only business operation that releases a held slot." "Only available through the JSON API; the web pages have no cancel button." | same | not written | app.py L365-L373, L388-L395 at `e734fc7` | none | class PR #6 diff at c18b638 |
| SLOT-R01 | rule | An unpaid booking holds its slot until it is cancelled | Overlap check and `no_overlapping_bookings` ignore `paid`; no expiry, no payment deadline | "Observed; intent unresolved." | not written; candidate owner "Purchase; depends on the payment decision (Payment)." | L735-L743, L116-L137, L168-L183, L923-L936, L365-L373, L388-L395, L987-L988. Author: full suite "**run** at `e734fc7` on 29 Sep 2026: 154 passed"; runtime check on a local Flask dev server, PostgreSQL 16, "All times are 2 Oct 2026, +07:00." | "**Question Q-SLOT-1:** should an unpaid booking hold a slot at all, or only a paid one?" "**Question Q-SLOT-2:** if it should, for how long before it is released (for example, a payment deadline)? What happens to a booking that was never paid when its time arrives?" "**Question Q-SLOT-3:** who may release an abandoned booking? Today, anyone who knows its id (see SLOT-R02)." Owner: "business stakeholder (instructor)". | class PR #6 diff at c18b638 |
| SLOT-R02 | rule | Cancelling deletes a booking and frees its slot | `DELETE /bookings/<id>` hard-deletes and returns the booking; slot free at once; no login, ownership or paid check; no refund recorded; JSON API only | "Observed; intent unresolved." | not written; candidate owner "Purchase; refund consequences belong to Payment." | `cancel_booking` L923-L936; tests L664-L687 "**run** as part of the 154-test suite" | "**Question Q-SLOT-4:** when a paid booking is cancelled, should the member get a refund, and should the cancellation be kept on record?" "**Question Q-SLOT-5:** who is allowed to cancel: the member, the account owner, staff, or anyone with the id?" | class PR #6 diff at c18b638 |
| Q-SLOT-1..Q-SLOT-5 | question | (see SLOT-R01, SLOT-R02) | as above | - | - | - | - | class PR #6 diff at c18b638 |

SLOT-R01 rows (author's ✓ = run): Member A books 10:00–12:00 unpaid, 201, `amount_cents: 3000`; Member B books 11:00–12:00, 409 "space is already booked for that time"; availability 11:00–12:00 `false`; Member A unlocks, 402; booking aged 30 days, still 409; past slot (1 Sep, booked 29 Sep) Member A 201 and Member B 409; **browser form row** "(form times read as +07:00)", redirected with "space is already booked for that time"; adjacent 12:00–13:00, 201; after cancel, rebooking 201. SLOT-R02 rows: anonymous `DELETE` 200 then gone; card-paid booking deleted, then `GET` 404, "nothing about a refund is stored"; `DELETE /bookings/999` "† 404". (class PR #6 diff at c18b638)

### IDs referenced, not defined here

| ID | Defined elsewhere | Note | Evidence |
|---|---|---|---|
| EX-T02, EX-R02 | main | EX-R02 cites EX-T02–EX-T04 (T03/T04 undefined) | class PR #6 diff at c18b638 |
| PAY-T01 | main (PR #1) | #6 still says "open PR #1" | class PR #6 diff at c18b638 |
| EX-T09 | main (PR #3) | #6 still says "open PR #3" | class PR #6 diff at c18b638 |

### Review points by role

| Role | On | Verbatim | Adopted at `c18b638`? | Evidence |
|---|---|---|---|---|
| class reviewer 1 (APPROVED at `afb5b9f`) | whole PR | "Checked the code links at e734fc7 and re-ran all the examples locally; everything matched. Left a few small suggestions. Approving." | n/a | class PR #6 discussion |
| class reviewer 1 (inline) | SLOT-T01 subscriber wording | "Tried this: [a member] booked first, then subscribed, and the booking stayed unpaid. So maybe \"a booking made while subscribed starts paid\"?" | **No** | class PR #6 discussion |
| class reviewer 1 (inline) | SLOT-T03 "only operation" | "RESET_DB_ON_START=true also wipes bookings (TRUNCATE, app.py L371). Maybe \"the only API operation\"?" | Yes | class PR #6 discussion |
| class reviewer 1 (inline) | Past bookings | "Tried a past unpaid booking (1 Sep 09:00–10:00): it's accepted, and a second booking for the same slot gets 409. So nothing happens when the time passes, and it keeps blocking. Maybe add it as a row?" | Yes | class PR #6 discussion |
| class reviewer 1 (inline) | **Separate form row** | "I ran the browser flow too: [Member B]'s overlapping form booking gets redirected with \"space is already booked\". So this part can be ✓." | Yes | class PR #6 discussion |
| class reviewer 1 (inline) | Link terms | "PAY-T01 and EX-T09 are still in open PRs #1 and #3. Maybe link them?" | Yes (now stale) | class PR #6 discussion |
| class reviewer 1 (inline) | Evidence marker | "This test ran in the 154-test suite, and I got 404 too. Should be ✓ instead of †?" | **No** | class PR #6 discussion |
| class reviewer 1 (inline) | No expiry | "Searched the repo for cron/schedule/expire; I only found card expiry, so this looks right." | n/a | class PR #6 discussion |
| class reviewer 2 (APPROVED at `c18b638`) | Overlap check | "I checked the overlap query in book_space() - it doesn't filter on paid, so an unpaid booking does block the slot. Source inspection only, not run." | n/a | class PR #6 discussion |
| class reviewer 2 | Paid cancel keeps a record | "should cancelling a paid booking work the same as cancelling an unpaid one? Right now both are hard-deleted. We have an open issue for this (#82 - \"Cancelling a paid booking should leave a record\"). Maybe link it so it stays visible?" | **No** | class PR #6 discussion |

## 8. PR #7 — counted member (open)

Body: "This PR records observed behaviour only; it does not decide business policy." (class PR #7 discussion)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| MET-T01 | term (context "Reporting") | Counted member | One distinct `member` text, exactly as stored, across all bookings; the "Members" figure on `/metrics` and `/dashboard`; base of the repeat member rate | "**Observed implementation** at Spacey revision `e734fc79...`"; "What the business means by "member" in its metrics is unresolved" | not stated | app.py L301-L302, L262-L263 at `e734fc7` | defers to MET-R01 | class PR #7 diff at 05e90b3 |
| MET-R01 | rule | Metrics count members by exact name text | `members` counts distinct `member` strings across all bookings, compared exactly ("case, spaces and spelling all count"); paid and unpaid; ignores `user_id`. Repeat rate = members with > 1 booking / members. | "observed; what a "member" should mean for business reporting is unresolved." | none; "Clarification owner: business stakeholder / instructor; decision unresolved." | L301-L302, L323-L329, L794, L805, L750-L771, L262-L273; dashboard.html L13-L16. Tests "read, not run". "Nothing was executed for this record" | "**MET-Q01:** what should "Members" on the investor dashboard count: people, accounts, paying customers, or typed names? Should all guest bookings count as one member? Should the metric match names the same way subscriptions do (trimmed, case ignored), so one person is not counted twice?" | class PR #7 diff at 05e90b3 |
| MET-Q01 | question | (see MET-R01) | as above | - | - | - | - | class PR #7 diff at 05e90b3 |

MET-R01 rows (names replaced; † = inferred from source): API bookings by Member A (x2) and Member B, members 2, repeat 0.5; subscribed Member A books as `"member a"` and `"  MEMBER A "`, both paid by one subscription but members 2 †; form bookings `"  member a  "` and `"member a"`, members 1 "because the form trims spaces" †; three form bookings with a blank name, members 1 (all "guest") †; API `"member": ""`, "Counted as a member with an empty name, separate from `"guest"`" †; one account books under two spellings, members 2 †; an unpaid booking still counts †. Separate JSON and form rows exist. (class PR #7 diff at 05e90b3)

### IDs referenced, not defined here

| ID | Defined elsewhere | Evidence |
|---|---|---|
| EX-T01 | main | class PR #7 diff at 05e90b3 |

### Review points by role

| Role | Point | Evidence |
|---|---|---|
| (none) | No reviews, no conversation or inline comments | class PR #7 discussion |
| class contributor (author, body) | Asks a named class reviewer: "Does the SQL support "compared exactly"?", "Can you predict each table row from the rule?", "Try a spelling or guest case I haven't listed." | class PR #7 discussion |
| author (body) | "I checked the existing glossary, rules and open PRs; there are no other MET- entries." PR #8 opened 9 minutes later with the same IDs. | class PR #7 discussion |

## 9. PR #8 — dashboard metrics (open)

Body: "Observed implementation, not policy." The glossary rows are appended to main's "Glossary v0.1" table, whose header calls its rows "working proposals". (class PR #8 discussion)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| MET-T01 | term (context "Reporting") | Counted member | "A distinct `member` text on bookings, compared exactly; shown as `members` on `/metrics` and `/dashboard`." Boundary: "Not a person or account". | none in row | not stated | none in row | none | class PR #8 diff at ce99d13 |
| MET-T02 | term (context "Reporting") | Paid booking (metrics) | "A booking with `paid = true`, paid by card or by an active subscription at $0." Boundary: "A subscriber's $0 booking counts as paid but adds no revenue." | none in row | not stated | none in row | none | class PR #8 diff at ce99d13 |
| MET-R01 | rule | Metrics count members by exact name text | "`members` counts distinct `member` texts on bookings, compared exactly (case and spaces matter). Subscriptions, by contrast, match names ignoring case and spaces." | "observed; what "member" should mean in reports is unresolved." | not stated | L301-L302, L323-L329 at `e734fc7`. Author: "✓ = run on 30 Sep 2026 (Flask test client, local PostgreSQL 16)"; no output attached | "Q-MET-1: should reports count people or accounts rather than typed names? Owner: business stakeholder." | class PR #8 diff at ce99d13 |
| MET-R02 | rule | A subscriber's booking counts as paid with zero revenue | "a subscriber's booking is saved as paid with amount 0, so metrics count it as a paid booking. It never lowers payment conversion (it raises it when other bookings are unpaid) and lowers average revenue per paid booking without adding revenue." | "observed; whether subscriber bookings belong in these metrics is unresolved." | not stated | L745-L770, L293-L299, L331-L341. Author: "✓ = run on 30 Sep 2026, same setup."; no output attached | "Q-MET-2: should payment conversion and average revenue exclude subscriber bookings? Owner: business stakeholder." | class PR #8 diff at ce99d13 |
| Q-MET-1, Q-MET-2 | question | (see MET-R01, MET-R02) | as above | - | - | - | - | class PR #8 diff at ce99d13 |

Rows (✓ as written): `member a`, `member a`, members 1, repeat 100%; `Member a`, `member a`, members 2, repeat 0%; no member twice, members 1 (`guest`); $25/h, 1 h: Member A card, paid 1, revenue $25, conversion 100%, avg $25; + Member B subscriber, paid 2, revenue $25, conversion 100%, avg $12.50; Member A card + Member C unpaid, conversion 50%; all three, paid 2, conversion 66.7%, avg $12.50. Rows do not say JSON or form. (class PR #8 diff at ce99d13)

### IDs referenced, not defined here

| ID | Defined elsewhere | Evidence |
|---|---|---|
| EX-T01 | main | class PR #8 diff at ce99d13 |

### Review points by role

| Role | Point | Verbatim | Evidence |
|---|---|---|---|
| class reviewer (the #7 author), inline | Conversion arithmetic | "Conversion is paid / total ([L331–335](...e734fc7.../app.py#L331-L335)). In your second row, adding [Member B]'s subscriber booking takes conversion from 100% (1/1) to 100% (2/2), so nothing rises. A subscriber booking can never lower conversion." | class PR #8 discussion |
| class contributor (author) | Fix applied in `ce99d13` | "good catch thankss!!!" / "I reworded to "never lowers conversion" and added a row with an unpaid booking" | class PR #8 discussion |
| (reviews) | 2 reviews, both COMMENTED with empty body, on `22f45bf`; no approval | - | class PR #8 discussion |

## 10. PR #9 — time terms and rule (open)

Empty body. Besides the TIM- content, #9 re-pads the markdown tables of the v0.1 glossary, EX-R01, EX-R02 and the template; with whitespace normalised, that reformat changes no content (class PR #9 diff at 9afd71f).

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| TIM-T01 | term (context Purchase) | Client time | "The clock time the user picks, such as 09:00. The form sends the numbers only, with no timezone." Boundary: "This is not the laptop's timezone. The browser does not send that." | none at head | not stated | none | none | class PR #9 diff at 9afd71f |
| TIM-T02 | term (context Purchase) | Server time | "The UTC time the server stores and returns from the API. Pages show that same moment in Bangkok." Boundary: "Server time is not the machine clock. 09:00 client time from the form is stored as 02:00 UTC." | none at head | not stated | none | none | class PR #9 diff at 9afd71f |
| TIM-R01 | rule | The form turns client time into Bangkok; the API does not | The form reads a naive time as Bangkok (UTC+7) and stores UTC; the JSON API rejects the same string. "Storing UTC is fine. The two inputs do not agree what a time with no timezone means." | none at head | not stated ("Ask the instructor.") | "Seen on main in [app.py](https://github.com/cs403bkk-2026/spacey/blob/main/app.py) (`parse_form_time`, `parse_time`). I ran those two functions. I did not run the tests." **Unpinned.** | "should the API also treat a missing timezone as Bangkok, like the form? Ask the instructor." | class PR #9 diff at 9afd71f |

TIM-R01 rows (separate form and JSON rows): `2026-09-25T09:00` form, "client time 09:00, stored as 02:00 server time (UTC)"; same via JSON API, "rejected, no timezone"; `2026-09-25T09:00:00Z` JSON, "server time 09:00 UTC, page shows 16:00 Bangkok". History: at `bb5133c` the terms were "Naive datetime" and "Instant", the glossary said "This is observed behaviour, not an approved policy.", and the question offered "or should the form stop guessing UTC+7?"; `9afd71f` removed all three. (class PR #9 diff at 9afd71f)

Our check: `parse_time` (L141-L149) returns None when `tzinfo is None`; `parse_form_time` (L189-L198) does `replace(tzinfo=LOCAL_TZ)` (source inspected at e734fc7).

At Spacey main both bodies are unchanged: `parse_time` app.py:143-151, `parse_form_time` app.py:191-200 (source inspected at 5a1cf3d).

### IDs referenced, not defined here

None beyond TIM-T01/T02. The unchanged EX-R01 context still lists "EX-T02, EX-T06, EX-T07" (class PR #9 diff at 9afd71f).

### Review points by role

| Role | Point | Verbatim | Evidence |
|---|---|---|---|
| class reviewer (conversation comment) | Time zones, JSON vs form | "The examples match the implementation: the form interprets a datetime without an offset as Bangkok time, while the API rejects one without an offset. I inspected the source; I did not run the test suite." | class PR #9 discussion |
| class reviewer | **Pinned evidence** | "The rule currently links to app.py on main, which can change. Please pin the evidence link to the revision you inspected, with line anchors, so readers can verify the behaviour against an identifiable version." Not addressed at head. | class PR #9 discussion |

## 11. PR #10 — accounts and login sessions (open)

Commits `cbfe9d4`, `bb9f346` ("Separate JSON and form results in ACC-R01 and ACC-R02"), `d68631f` ("Use the existing Purchase context for ACC- terms and rules"). Glossary status line: "Status: **observed implementation** at Spacey `e734fc79bbb72341407f7decd7030fd47ea6a151`, not approved policy." (class PR #10 diff at d68631f)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| ACC-T01 | term (context Purchase; "Identity" before `d68631f`) | Account | Registered email (trimmed, lower-cased, unique) plus a password hash; not the typed member name | section status line | none | `users` L67-L78, `is_subscribed` L262-L273 at `e734fc7` | Boundary: "At this revision there is no email confirmation, password change, password reset or account deletion." | class PR #10 diff at d68631f |
| ACC-T02 | term (context Purchase; "Identity" before `d68631f`) | Login session | Account id in Flask's signed session cookie after login; enables "Logged in as", account-linked bookings, `/bookings/mine` | section status line | none | login L495-L515, signing key L15-L18 | Boundary: "The app keeps no server-side list of sessions: logout removes the id from that browser only, and the app sets no expiry on the cookie (ACC-R02)." | class PR #10 diff at d68631f |
| ACC-R01 | rule | Registering creates an account keyed by its email | `POST /register` validates email shape and password length >= 8, stores trimmed lower-case email and a hash, does not log in. JSON: 201/400/409. Form: always 302. | "observed; intent unresolved." | "unresolved. Implementation history only: Spacey issue #121 asked for these checks. Its parent issue #120 is still open and also plans email confirmation, which is not built. A backlog issue is not a business decision." | "Source inspected at `e734fc7`" (L226-L235, L449-L471, L481-L493). Author: registration tests "run ... (154 passed, 30 Sep 2026)"; ✓ rows "run ... through Flask's test client against PostgreSQL 16" | "Open question Q-ACC-1: ... Registration reports \"email is already registered\" (JSON: 409; form: shown after the redirect), which does reveal it. Is that acceptable?" "Open question Q-ACC-2: is \"at least 8 characters, any characters\" the intended password policy? Must an email be confirmed (as #120 plans) before the account can be used?" | class PR #10 diff at d68631f |
| ACC-R02 | rule | Login starts a cookie session; logout clears it in that browser only | Email matched case-insensitively, password exactly; identical error for wrong password and unknown email; logout pops the id; no failed-login limit. JSON: 200/401, logout 200. Form: always 302. | "observed; intent unresolved." | "unresolved. Implementation history: #122 asked for login and logout with the identical error. The startup log notes no \"remember me\", no expiry beyond Flask's default, and no rate limiting" | "Source inspected at `e734fc7`" (L15-L18, L404-L417, L495-L515, L525-L545, L748-L749, L877-L883); login/logout tests "in the same 154-test run" | "Open question Q-ACC-3: should logout end the session everywhere, so a copied cookie stops working? Should sessions expire?" "Open question Q-ACC-4: should failed logins be limited? Should a logged-in member be able to book under a different member name?" Uncertainty: the default `SECRET_KEY` "is a known public value". | class PR #10 diff at d68631f |
| Q-ACC-1..Q-ACC-4 | question | (see ACC-R01, ACC-R02) | as above | - | - | - | - | class PR #10 diff at d68631f |

Other fields: ACC-R01 "Candidate responsibility and dependencies: Purchase; depends on the email-confirmation decision in #120." ACC-R02 "Candidate responsibility and dependencies: Purchase. Who may pay, cancel or unlock a booking is not covered here." Clarification owner (both): "business stakeholder (instructor)". (class PR #10 diff at d68631f)

Our spot-check at the seed: duplicate email 409 at app.py:462; form redirect with the error text at app.py:486; `len(password) >= 8` at app.py:229; default key at app.py:20; login stores the id at app.py:508, logout pops it at app.py:536 (source inspected at 5a1cf3d).

### IDs referenced, not defined here

| ID | Defined elsewhere | Evidence |
|---|---|---|
| EX-T01 | main | class PR #10 diff at d68631f |
| Spacey issues #120, #121, #122 | Spacey issue tracker (not rule IDs) | class PR #10 diff at d68631f |

### Review points by role

| When (UTC) | Role | Point | Verbatim | Evidence |
|---|---|---|---|---|
| 02:47 | class reviewer (CHANGES_REQUESTED on `cbfe9d4`) | Evidence scope | "I did not run the Flask routes, PostgreSQL, or the full suite myself, so the 154-pass/runtime results remain the author's reported checks." / "Two status-code claims need the JSON/form scope corrected before this record is accurate; the open policy questions can stay." | class PR #10 discussion |
| 02:47 | class reviewer (inline, ACC-R01) | **Separate JSON and form rows** | "That is true for JSON, but the form redirects with HTTP 302 to `/register?error=...` for a duplicate or validation error" ... "Please scope the 400/409 table rows to JSON requests and describe the form's redirect. This lets readers predict both paths." | class PR #10 discussion |
| 02:47 | class reviewer (inline, ACC-R02) | **Separate JSON and form rows** | "The identical 401 response for wrong/unknown credentials is the JSON route's result. The login form turns that failure into an HTTP 302 redirect to `/login?error=...`" ... "Please distinguish these paths in the rule, as ACC-R01 does after correction." | class PR #10 discussion |
| 03:30 | class contributor (author) | Fixed in `bb9f346` | "Agreed. ... Fixed." | class PR #10 discussion |
| 06:23 | course instructor (CHANGES_REQUESTED on `bb9f346`) | **Account data in Purchase, not a new Identity context** | "change the context to the existing \"Purchase\" and good to go" / "In the future can be extracted in the different context" | class PR #10 discussion |
| 06:25 | class contributor (author) | Applied in `d68631f` (Identity to Purchase); no re-review after | - | class PR #10 diff at d68631f |

The course instructor role is inferred from the reviewing account, which also reviewed #11 and which main RULES names as the stakeholder for the booking-price rule. No course page confirms it (class PR #10 discussion).

## 12. PR #11 — party size and capacity (open)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| BOOK-T01 | term (context "Booking") | Party size | Number of people on a booking; a positive whole number not above capacity | "These terms describe booking concepts and the observed implementation at revision `e734fc7`." | none | L720-L734; form L801-L821 at `e734fc7` | Boundary: "The HTML form supplies 1 and does not ask for the actual group size" | class PR #11 diff at 7cf2656 |
| BOOK-T02 | term (context "Booking") | Capacity | Positive whole-number capacity recorded for a space | same | none | creation check L583-L590; L729-L734 | none | class PR #11 diff at 7cf2656 |
| BOOK-R01 | rule (renames main EX-R01) | Party size within space capacity | Reject a booking whose party size exceeds capacity or is not a positive whole number | "observed implementation; this record does not establish a separate stakeholder policy decision." | "no separate stakeholder decision recorded." | "source inspected at revision `e734fc7`" (L706-L744, L780-L821); over-capacity test L1872-L1885 "inspected, not run" | "does the party size supplied to a booking represent every person who will use the space? The HTML form submits 1 and does not ask for the actual group size, so this check is only meaningful when the booking request receives the group's actual size." | class PR #11 diff at 7cf2656 |

Rows: capacity 15 / party 20, reject 400; 15/15, pass; 15/0, reject; group on the HTML form, form sends 1. Other fields: "Candidate responsibility and dependencies: booking; ..."; "Clarification owner: business stakeholder / instructor."; "Next use: verify the booking flow captures the intended group size and retain this rule as a booking contract check." (class PR #11 diff at 7cf2656)

Our spot-check at the seed: size check app.py:716-727; JSON default `body.get("party_size", 1)` app.py:791; form `book_space(..., 1)` app.py:806 (source inspected at 5a1cf3d).

### IDs referenced, not defined here

| ID | Status | Evidence |
|---|---|---|
| EX-R03 | Defined nowhere; #11 keeps it in README ("begin with the glossary and BOOK-R01/EX-R03") | class PR #11 diff at 7cf2656 |
| EX-T03, EX-T04 | Defined nowhere; left in EX-R02 Terms | class PR #11 diff at 7cf2656 |

### Review points by role

| Role | Point | Verbatim | Evidence |
|---|---|---|---|
| course instructor (CHANGES_REQUESTED, empty body, inline on BOOK-T01) | Context ownership | "Use Purchase context instead of the Booking" — not addressed (no commit after `7cf2656`) | class PR #11 discussion |

## 13. PR #12 — access code stored (open)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| PAY-R04 | rule | An access code is generated once and stored | Claims the first unlock stores an 8-hex code in `bookings.access_code` and later unlocks return the same code | "observed; whether the code should expire at booking end is unresolved (see Q07)." | "unresolved." | "source inspected at current main: `issue_access_code`" linked to `spacey/blob/main/app.py`. **No SHA.** Claims "on first call `access_code` is NULL, a code is generated with `secrets.token_hex(4)` and saved; on subsequent calls the stored value is returned directly." | "Open question Q07: should the access code become invalid after the booking's end time? The current implementation stores the code permanently and returns it regardless of when the unlock request is made. Whether door access should be time-limited is a business policy question, not a code question." | class PR #12 diff at 1c8ce57 |
| Q07 | question | (see PAY-R04) | as above | - | - | - | - | class PR #12 diff at 1c8ce57 |

Other fields: first field is "Statement (observed implementation)"; "Terms: PAY-T01, PAY-T04."; "Candidate responsibility and dependencies: Access / Door."; "Next use: door-lock integration design; entry verification (the distinction between \"receiving a code\" and \"using it to enter\" is not yet implemented)." (class PR #12 diff at 1c8ce57)

### IDs referenced, not defined here

| ID | Defined elsewhere | Evidence |
|---|---|---|
| PAY-R03, PAY-T01, PAY-T04 | main | class PR #12 diff at 1c8ce57 |

### Review points by role

| Role | Point | Evidence |
|---|---|---|
| (none) | No reviews, no comments (`gh api .../pulls/12/comments` returned `[]`). Body premise: "PAY-R03 (already in the file) flagged \"should a code be issued once and remembered?\" as an open question. PAY-R04 answers that - the code in the current main branch does store it." | class PR #12 discussion |

## 14. PR #13 — space availability, first version (open)

Glossary intro: "Both terms are **observed implementation** at commit `e734fc79bbb72341407f7decd7030fd47ea6a151`, from reading the source." (class PR #13 diff at c8a302f)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| AVL-T01 | term | Available | "A yes/no on a space: no booking overlaps the time you asked about". Boundary: "Capacity is ignored: one small booking makes a big room "unavailable"." | "observed implementation" (intro) | none | app.py L560-L574 (`list_spaces`) at `e734fc7` | none | class PR #13 diff at c8a302f |
| AVL-T02 | term | Time window | "Optional `start_time` and `end_time` on `GET /spaces`. Without them, the check is "right now"". Boundary: "Giving only one of the two times returns 400." | "observed implementation" (intro) | none | app.py L152-L165 (`parse_window`) | none | class PR #13 diff at c8a302f |
| AVL-R01 | rule | With no time given, "available" means free right now | "if no time window is given, a space is available unless a booking is running at this moment. A space booked for later today still shows as available." | "Statement (observed implementation)" | none | "source read, not run, at `e734fc7`:" `booked_space_ids` L168-L183 | "should "available" mean free today instead of free right now?" | class PR #13 diff at c8a302f |
| AVL-R02 | rule | Any booking blocks the whole space | "any overlapping booking makes the space unavailable, even an unpaid one or a booking for one person in a large room." | "Statement (observed implementation)" | none | "source read, not run, at `e734fc7`:" `list_spaces` L560-L574 | "do we sell the whole room or single seats? (see Q01)" | class PR #13 diff at c8a302f |

Rows: booked 15:00–16:00, checked at 10:00 with no times, "Available"; checking 15:00–16:00, "Not available"; 16:00–17:00, "Available (touching is fine, like EX-R02)"; "Room with capacity 10, one unpaid booking for 1 person now", "Not available". No time zone stated. (class PR #13 diff at c8a302f)

### IDs referenced, not defined here

| ID | Status | Evidence |
|---|---|---|
| EX-T02, EX-R02 | main | class PR #13 diff at c8a302f |
| Q01 | **Dangling on main.** At `1124404`, Q01 was EX-R01's question ("what do we sell: exclusive space, group booking or shared seats? ..."); `81e490e` removed the label | class PR #13 diff at c8a302f |

### Review points by role

| Role | Point | Evidence |
|---|---|---|
| (none) | No reviews, comments or inline comments; empty body (REST `comments: 0`, `review_comments: 0`) | class PR #13 discussion |

## 15. PR #14 — booking price clarification (merged)

Opened from the course instructor's account; commits by a separate non-personal identity; approved (no text) and merged by a class reviewer. Body: "clarify that Purchase owns its calculation: creation-time hourly rate × duration, rounded half up to cents for bookings without subscription coverage." / "This follows [course instructor]'s 30 September clarification and request for PRs." / "It adds the requested business term and scoped intent without introducing a competing rule identifier." / "Application evidence is pinned source inspection, not a deployment claim." Links Spacey PR #196. (class PR #14 discussion)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| PRC-T02 | term (context Purchase) | Booking price | "Monetary amount assigned to a particular booking. Purchase owns its calculation" | via the rule below | via the rule below | none on the row | Boundary: "Distinct from the space's hourly rate; does not mean that payment has occurred." Note: "Booking price names the same concept as **PRC-T02 Booking amount** in [PR #4]... these are not two different amounts. Integrate this clarification with PRC-T02 when that contribution merges." | class PR #14 diff at 25ca71e |
| (no ID) | rule | "Booking price — Purchase rule clarification" | "for a booking not covered by a subscription, Purchase calculates its booking price using the space's hourly rate at booking creation multiplied by the booked duration, rounded to the nearest whole cent; half cents round up." | "stakeholder-clarified for this calculation and its Purchase ownership by [course instructor], 30 September 2026; submitted here for review." | course instructor as stakeholder, 30 Sep 2026 (inside Policy status; no separate field) | `amount_for` app.py L201-L206 at `e734fc79...`: "first truncates elapsed duration to whole seconds. The initial module extraction preserves that arithmetic." / "This evidence is source inspection at the linked revision, not a deployed check." | Scope: "This clarification does not settle minimum charges, future billing increments, maximum durations or historical missing amounts raised in PR #4." Next use: "Payments consumes the recorded amount rather than recalculating it from a current hourly rate. Check both browser and JSON booking entry points after extraction." | class PR #14 diff at 25ca71e |

Worked examples as written ($): 30 min at $15.00/h = $7.50; 20 min at $10.00/h = $3.33; 18 s at $1.00/h = $0.01 "(half a cent rounds up)" (class PR #14 diff at 25ca71e).

Our arithmetic check: `amount_for` (L201-L206, read with `git show e734fc7:app.py`) executed on the three examples. Evidence: test run at e734fc7.

```
1500 0:30:00 -> 750
1000 0:20:00 -> 333
100 0:00:18 -> 1
```

All three match. Spacey main `purchase.py` `calculate_booking_price_cents` uses the same formula `(hourly_rate_cents * seconds + 1800) // 3600` (source inspected at 5a1cf3d).

### IDs referenced, not defined here

| ID | Where | Defined elsewhere | Evidence |
|---|---|---|---|
| PRC-R01 | "clarifies the intended rule behind PRC-R01 in [a class contributor]'s pricing PR #4" / "Consolidate this clarification into PRC-R01 when merging both." | open PR #4 only | class PR #14 diff at 25ca71e |
| "hourly rate" (PRC-T01 in #4) | Terms: "PRC-T02 Booking price and hourly rate" | open PR #4 only | class PR #14 diff at 25ca71e |
| PAY-R01 | "subscription coverage remains PAY-R01" | main | class PR #14 diff at 25ca71e |

### Review points by role

| Role | Point | Evidence |
|---|---|---|
| class reviewer | One APPROVED review with no text; no PR or inline comments. Pricing ownership and "Payments consumes the recorded amount" are the author's statements, not a reviewer's. | class PR #14 discussion |

## 16. PR #15 — availability search (open; base for AVL-)

Glossary intro: "Both terms are **observed implementation** at commit `e734fc79bbb72341407f7decd7030fd47ea6a151`. Evidence is source inspection unless stated." (class PR #15 diff at 9e4971a)

### IDs defined

| ID | Kind | Title | One-line meaning | Policy status as written | Decision source as written | Implementation evidence as written | Open question as written | Evidence |
|---|---|---|---|---|---|---|---|---|
| AVL-T01 | term | Available | Flag on `GET /spaces` and `GET /spaces/<id>`; `true` when no booking overlaps the availability window; with no window, "no booking is running right now". Boundary: "It is not a promise that booking will work. It does not check party size against capacity (see EX-R01) and does not hold the slot. ... both kinds of booking make a space unavailable." | "observed implementation" (intro) | none | L560-L574, L607-L624, L168-L183 at `e734fc7` | none | class PR #15 diff at 9e4971a |
| AVL-T02 | term | Availability window | Optional `start_time`/`end_time`; "Both must be given, both need a timezone, and the end must be after the start." Boundary: "If neither is given, the window is "right now", not "today" or "any time". A window in the past is accepted (see AVL-R02). The home page never uses a window: it only shows "free right now" / "booked right now"." | "observed implementation" (intro) | none | `parse_window` L152-L165 | none | class PR #15 diff at 9e4971a |
| AVL-R01 | rule | A space is available if no booking overlaps the window | Overlap uses the same test as EX-R02; with no window, "is a booking running at this moment?"; any booking counts, paid or unpaid; party size and capacity not checked | "Statement (observed implementation)" | none | `booked_space_ids` L168-L183 ("the SQL reads only `space_id`, `start_time` and `end_time`, not `paid` or party size"), `list_spaces`, `get_space`, home page L419-L447, index.html L14-L18. "Tests were read, not run": L594-L612, L1769-L1814 | "does "available" mean "free for the whole window" or "free for part of it"? Should a search take party size into account...? Should unpaid bookings (which may never be paid, see SLOT-R01 in open PR) block searches? Should the home page offer a time search too?" | class PR #15 diff at 9e4971a |
| AVL-R02 | rule | An availability window must be complete, in order and have a timezone | Both or neither; ISO 8601 with offset; end after start; otherwise 400, no spaces returned; no future or length rule | "Statement (observed implementation)" | none | `parse_time`, `parse_window` L141-L165; test L1816-L1837 "read, not run"; contributor's "**Run by me:** `parse_time` and `parse_window` on their own ... with Python 3." | "a naive time is rejected here but read as Bangkok time on the booking form (see TIM-R01 in open PR). Should search and booking read times the same way? Should searching the past be allowed? The error for a missing timezone says the two values "must be given together", which is confusing when both were given." | class PR #15 diff at 9e4971a |

AVL-R01 has 7 rows (Room A, capacity 4, booking 10:00–11:00 Bangkok on 1 Oct; three marked †). AVL-R02 has 6 rows, all ✓ (contributor's standalone run). JSON only; no form rows. (class PR #15 diff at 9e4971a)

Our run of the six AVL-R02 rows: `parse_time` and `parse_window` (L141-L165 at `e734fc7`) copied into a scratch script, Python 3.11.7, no DB, no HTTP. All six reproduce (output below). Evidence: test run at e734fc7.

The HTTP 400 in the PR's rows comes from reading `list_spaces` (it returns 400 with the `parse_window` error), not from running it (source inspected at e734fc7).

```
no values      -> (None, None)
both +07:00    -> ((datetime(2026,10,1,10,0,tz=+07:00), datetime(2026,10,1,11,0,tz=+07:00)), None)
only start     -> (None, 'start_time and end_time must be given together (ISO 8601 with timezone, e.g. 2026-09-25T09:00:00Z)')
no timezone    -> (None, 'start_time and end_time must be given together (ISO 8601 with timezone, e.g. 2026-09-25T09:00:00Z)')
start == end   -> (None, 'end_time must be after start_time')
past window    -> ((datetime(2020,1,1,10,0,tz=UTC), datetime(2020,1,1,11,0,tz=UTC)), None)
```

(Datetime reprs shortened; the raw output shows `tzinfo=datetime.timezone(datetime.timedelta(seconds=25200))` and `tzinfo=datetime.timezone.utc`.)

### IDs referenced, not defined here

| ID | Status | Evidence |
|---|---|---|
| EX-T02, EX-R02, PAY-T01 | main | class PR #15 diff at 9e4971a |
| EX-R01 | main; renamed BOOK-R01 in #11 | class PR #15 diff at 9e4971a |
| SLOT-R01 | open PR #6 only | class PR #15 diff at 9e4971a |
| TIM-T01, TIM-R01 | open PR #9 only | class PR #15 diff at 9e4971a |

### Review points by role

| Role | Point | Evidence |
|---|---|---|
| (none) | No reviews, comments or inline comments; empty body | class PR #15 discussion |

## 17. Known conflicts (BRIEF section 4)

Each must be resolved in `ID_MAP.md` (M1). Verdicts below are facts; resolutions are M1's.

| # | BRIEF item | Verdict | Detail | Evidence |
|---|---|---|---|---|
| K1 | "AVL-* IDs clash between #13 and #15. Take #15 as the base." | Confirmed | All four IDs clash. AVL-T01: same concept, #15 is a superset. AVL-T02: "Time window" vs "Availability window", same concept. AVL-R01: #13's "no window means free right now" is a sub-clause of #15's. AVL-R02: **different meanings under one ID** ("Any booking blocks the whole space" in #13 vs "An availability window must be complete, in order and have a timezone" in #15); #13's AVL-R02 content is inside #15 AVL-R01. Carry over from #13: the question "should "available" mean free today instead of free right now?", the "Room with capacity 10, one unpaid booking for 1 person now" row, and the whole-room-or-seats question (re-pointed from the dangling Q01 to the EX-R01 question). The two PRs also conflict as text. | class PR #15 diff at 9e4971a |
| K1b | (same) | #13 side | #13 definitions as quoted in section 14 | class PR #13 diff at c8a302f |
| K2 | "MET-T01 and MET-R01 are duplicated in #7 and #8." | Confirmed | Same IDs, same titles, same core meaning, no contradiction. They differ in depth, question IDs (MET-Q01 vs Q-MET-1), evidence (#7 "Nothing was executed"; #8 claims runs with no output), placement and candidate owner. MET-T02 and MET-R02 exist only in #8. | class PR #8 diff at ce99d13 |
| K2b | (same) | #7 side | #7 definitions as quoted in section 8 | class PR #7 diff at 05e90b3 |
| K3 | "PRC-T02 is \"Booking amount\" in #4 but \"Booking price\" on main." | Confirmed; a name clash, not a meaning clash | #4: "PRC-T02 Booking amount \| A booking's stored total, `amount_cents` ...". Main: "PRC-T02 Booking price \| Purchase \| Monetary amount assigned to a particular booking." Main says "these are not two different amounts". A trial merge of #4 onto main gives two `PRC-T02` rows. Main GLOSSARY section 1 diagram still says "Booking amount". | class PR #4 diff at 9478b3e |
| K4 | "PAY-R04 (#12, stored code) contradicts the code and PAY-R03." | Confirmed | At the pin, `issue_access_code` (L976-L991) reads only `id, paid`, then `access_code = secrets.token_hex(4)  # mocked lock integration` (L990), and writes nothing. No `access_code` column in the DDL. | source inspected at e734fc7 |
| K4c | (same) | Spacey main side | `issue_access_code` app.py:970-985 has the same body (token line 984); no `access_code` column in the DDL. `git log --all -G 'access_code (TEXT\|VARCHAR)\|SET access_code\|access_code IS NULL'` over the Spacey clone returns nothing, so no fetched revision ever stored it. | source inspected at 5a1cf3d |
| K4b | (same) | Class side | PAY-R03 row "Unlock again \| 200, a different code †"; PAY-T04 "It is not saved, so asking again gives a new code." PAY-R04 cites unpinned `blob/main`. Its described behaviour matches the course's *proposed* Access policy ("reuse the credential for the same valid grant"), so it can be used as a proposal, never as observed evidence. | class PR #12 diff at 1c8ce57 |
| K5 | "SLOT-T01's subscriber wording contradicts PAY-R01." | Confirmed | SLOT-T01: "A subscriber's booking is never unpaid". PAY-R01 row: a member who subscribes after booking keeps an unpaid booking ("subscription is checked only at creation"). Class reviewer 1 raised it inline on `afb5b9f`; not fixed at `c18b638`. `is_subscribed` is evaluated only inside the INSERT. | class PR #6 diff at c18b638 |
| K6 | "#11 renames EX-R01 to BOOK-R01." | Confirmed, and meaning changes too | "## EX-R01 — Party size within capacity" becomes "## BOOK-R01 — Party size within space capacity"; README EX-R01 becomes BOOK-R01. Status moves from main's "proposed; exclusive-space/group-booking interpretation needs stakeholder confirmation." to "observed implementation"; examples move from capacity 4 (incl. a 2.5 reject) to capacity 15; main's question "what do we sell: exclusive space, group booking or shared seats? What about already-made bookings if capacity falls?" is dropped; Terms EX-T02, EX-T06, EX-T07 become BOOK-T01, BOOK-T02. Main README: "Do not silently replace established course identifiers with them." | class PR #11 diff at 7cf2656 |
| K7 | "TIM-R01: the form reads naive time as Bangkok time, but the API rejects it." | Confirmed, and it reaches search too | At the pin, `parse_form_time` (L189-L198) sets `LOCAL_TZ`; `parse_time` (L141-L149) returns None for naive input; `parse_window` uses `parse_time`, so `GET /spaces` also rejects naive times (as #15 AVL-R02 shows). | source inspected at e734fc7 |
| K7c | (same) | Spacey main side | Both functions unchanged at `5a1cf3d`: `parse_time` app.py:143-151, `parse_form_time` app.py:191-200. | source inspected at 5a1cf3d |
| K7d | (same) | Class discussion | A class reviewer on #9: "The examples match the implementation: the form interprets a datetime without an offset as Bangkok time, while the API rejects one without an offset. I inspected the source; I did not run the test suite." | class PR #9 discussion |
| K7b | (same) | Class side | TIM-R01 rows: form `2026-09-25T09:00` stored as 02:00 UTC; JSON "rejected, no timezone" | class PR #9 diff at 9afd71f |
| K8 | "EX-T03, T04, T06, T07 and EX-R03 are referenced but never defined." | Confirmed | Main EX-R01 cites "EX-T02, EX-T06, EX-T07"; EX-R02 cites "EX-T02–EX-T04"; README cites "EX-R01/EX-R03". No main or PR head defines any of them (grep of GLOSSARY/RULES/README in all refs). #11 drops the EX-T06/T07 references (implying BOOK-T01/T02 replace them) but keeps EX-R03 and EX-T03/T04. EX-T05 is never referenced at all. | source inspected at 58a1477 |

## 18. Other BRIEF section 4 facts about the class record

| BRIEF claim | Verdict | Detail | Evidence |
|---|---|---|---|
| Main includes merged #1, #3, #14 | Confirmed | Merge commits on `origin/main`: `1124404` "Merge pull request #1", `5d23e9f` "Merge pull request #3", `58a1477` "Merge pull request #14" (`git log --merges origin/main`) | source inspected at 58a1477 |
| "The only stakeholder-clarified rule is booking price: rate at creation × duration, rounded half up; Purchase owns it, and Payments consumes it without re-pricing." | Confirmed | Only rule on main with that status. Quote: "Payments consumes the recorded amount rather than recalculating it from a current hourly rate." It has no stable ID. | class PR #14 diff at 25ca71e |
| Template fields: Rule, Policy status, Decision source, Implementation evidence, Terms, Candidate responsibility, Given/When/Expected table, Open question, Clarification owner, Next use | Confirmed, with two exact names | The field is "Candidate responsibility and dependencies"; the table's third column is "Expected result under this rule". See section 20. | source inspected at 58a1477 |
| "Reviewers asked for separate JSON and browser/form outcome rows" | Confirmed (not in #1, #3, #14) | #10: a class reviewer asked to "scope the 400/409 table rows to JSON requests and describe the form's redirect" (CHANGES_REQUESTED; fixed in `bb9f346`). #6: a class reviewer ran the browser flow and the form row was added. #14's author wrote "Check both browser and JSON booking entry points after extraction". | class PR #10 discussion |
| "... and for evidence pinned to a revision" | Confirmed | #9: "Please pin the evidence link to the revision you inspected, with line anchors". #1 reviewer's comments use pinned permalinks. Main README: "All implementation evidence here comes from source inspection at `e734fc7...`". | class PR #9 discussion |
| BRIEF 3.7: "the class reviewer's comment on rules PR #10, \"change the context to the existing 'Purchase' ... In the future can be extracted in the different context\"" | Confirmed, one correction | Exact text: "change the context to the existing \"Purchase\" and good to go" / "In the future can be extracted in the different context" (double quotes). The reviewing account is the **course instructor**, not a class reviewer. Review state CHANGES_REQUESTED on `bb9f346`; applied in `d68631f`. | class PR #10 discussion |

The open state of #4-#13 and #15 is in section 1, second table, one row per PR tagged `class PR #n discussion`.

## 19. Other conflicts found

| # | Conflict | Detail | Evidence |
|---|---|---|---|
| O1 | Booking-price rule has no ID | The template heading is "`<stable ID> — <business rule name>`". #14 defers to PRC-R01, which exists only in open #4. `ID_MAP.md` must assign one. | class PR #14 diff at 25ca71e |
| O2 | PRC-R01 status stale against main | #4 says "observed; intent unresolved"; main (#14) makes the same calculation stakeholder-clarified and says "Consolidate this clarification into PRC-R01 when merging both." PRC-Q01 stays open (minimum charge, increments, max duration, historical NULLs). | class PR #4 diff at 9478b3e |
| O3 | PRC-Q02 partly answered on main | Main fixes the price at creation and says Payments does not recalculate; the historical NULL-amount half is still open. | source inspected at 58a1477 |
| O4 | `PAY-` prefix spans three contexts | PAY-T02 Member name and PAY-T03 Subscription are Purchase concerns (coverage); PAY-T04, PAY-R03, PAY-R04 are Access concerns. The PAY- glossary table has no Context column. | source inspected at 58a1477 |
| O5 | Contexts outside the three | "Shared journey" (main EX-T01, EX-T08, EX-T09), "Identity" (#10 before the fix), "Booking" (#11, unfixed after the instructor's review), "Reporting" (#7, #8), "Space Management / Inventory" (#5), "Access / Door" (#12). BRIEF 3.7 allows three contexts; section 10 keeps metrics in Purchase. | class PR #11 discussion |
| O6 | Direct push without review | `81e490e` reformatted PR #1 and #3 rules on main with no PR; numbered questions Q01, Q03, Q05 lost their numbers, leaving #13's "(see Q01)" dangling. No question register exists. | source inspected at 58a1477 |
| O7 | Question-ID styles differ | Q01..Q07 (base, #3, #5, #12), PRC-Q01/Q02 (#4), Q-SLOT-1..5 (#6), MET-Q01 (#7), Q-MET-1/2 (#8), Q-ACC-1..4 (#10), unnumbered on main and in #9/#11/#13/#15. PR #5's body says Q07 while its diff says Q06; #12 defines a different Q07. | class PR #5 diff at 0712a1c |
| O8 | Status vocabularies differ | README: "Observed; intent unresolved", "Proposed", "Stakeholder-clarified, scoped", "Superseded". Template: "observed / proposed / stakeholder-clarified / superseded". BRIEF has no "Proposed" and adds "Decided". EX-R01 is "proposed". #8 glossary rows sit under "working proposals" while its body says observed. #9 has no status at head. | source inspected at 58a1477 |
| O9 | Unpinned evidence | EX-R05 (#5) has no revision or link; TIM-R01 (#9) and PAY-R04 (#12) link `blob/main`. Every other PR pins `e734fc7`. | class PR #12 diff at 1c8ce57 |
| O10 | Old repo name in main evidence | EX-R01/EX-R02 link `cs403bkk-2026/startup-app/...` (renamed to `spacey`). #11 fixes it for BOOK-R01 only. | source inspected at 58a1477 |
| O11 | EX-T09 duplicates EX-R04 | Reviewer asked for "see EX-R04"; not done | class PR #3 discussion |
| O12 | EX-R05 x SLOT-R02 erase history | Deleting a space needs all bookings cancelled; cancel hard-deletes, paid ones included; so retiring a space erases revenue history. PR #5 Q06 and the #82 reference on #6 both point at it. | class PR #6 diff at c18b638 |
| O13 | "Held slot" meaning | SLOT-T02 "held" = any existing booking, paid or unpaid. Our target uses `held` as an unpaid booking status (D11). Give the two meanings different names. | class PR #6 diff at c18b638 |
| O14 | MET-T02 duplicates PAY-T01; MET-R02 restates part of PAY-R01; MET-T01 sits beside PAY-T02 | Meanings agree; #7/#8 predate or do not cite the PAY- entries | class PR #8 diff at ce99d13 |
| O15 | ACC-T01/T02 (Purchase) vs EX-T01/T08/T09 ("Shared journey") | Meanings agree; overlap to merge, not a contradiction | class PR #10 diff at d68631f |
| O16 | #11 rewrites the Glossary v0.1 intro | New text "Definitions below are working vocabulary, not approved business policy." would mislabel stakeholder-clarified PRC-T02 now in that table | class PR #11 diff at 7cf2656 |
| O17 | Glossary section numbering | "## 4." is claimed by #11 (renumbered PAY-), #13 (AVL) and #15 (AVL) | class PR #11 diff at 7cf2656 |
| O18 | TIM terms renamed inside #9 | "Naive datetime"/"Instant" became "Client time"/"Server time"; "Server time" needs its "not the machine clock" disclaimer | class PR #9 diff at 9afd71f |
| O19 | #9 overlaps #11 as text | #9 re-pads the EX-R01 table; #11 replaces it. No semantic clash. | class PR #9 diff at 9afd71f |
| O20 | Stale "open PR" links | #6 calls #1 and #3 open (both merged); #15 calls #6 and #9 "open PR" (still true) | class PR #6 diff at c18b638 |
| O21 | Template drift in #13 and #15 | Both branched before `81e490e` and use the old names ("Statement (observed implementation)", "Evidence", "Question", "Uncertainty / questions", "Examples and boundaries"); no Policy status, Decision source, Candidate responsibility, Clarification owner or Next use | class PR #15 diff at 9e4971a |
| O22 | #15 AVL-T02 accuracy | Says the home page "only shows" free/booked right now; it also lists upcoming booked intervals | source inspected at e734fc7 |
| O23 | Units | #4 uses cents; #8 and #14 use "$"; our docs use THB and satang (D1). The formula is currency-neutral. | class PR #14 diff at 25ca71e |
| O24 | Missing README targets | `DOMAIN_MODEL.md`, `CHANGE_EXAMPLE.md`, `RULE_TEMPLATE.md` (and their cancellation anchors) exist in no ref | source inspected at 58a1477 |
| O25 | Review suggestions not adopted in #6 | † vs ✓ on the 404 row; linking Spacey issue #82 | class PR #6 discussion |
| O26 | Formatting slips on main | PAY-R01 "**Open question::**", PAY-R03 "**Rule** unlock" (no colon), trailing spaces after "observed." Matters only for a parser. | source inspected at 58a1477 |

## 20. Class rule template (exact field names)

From main `RULES.md` "## Template" (added by the course instructor in `a200114`; identical at `a853795`, `1124404` and `58a1477`).

| Element | Exact text | Evidence |
|---|---|---|
| Heading | `### <stable ID> — <business rule name>` | source inspected at 58a1477 |
| `Rule` | "<one precise sentence; include its scope>" | source inspected at 58a1477 |
| `Policy status` | "<observed / proposed / stakeholder-clarified / superseded>" | source inspected at 58a1477 |
| `Decision source` | "<actual stakeholder, date, reference; or unresolved>" | source inspected at 58a1477 |
| `Implementation evidence` | "<source / tests / live check; exact revision and limits>" | source inspected at 58a1477 |
| `Terms` | "<glossary IDs>" | source inspected at 58a1477 |
| `Candidate responsibility and dependencies` | "<who decides; facts required>" | source inspected at 58a1477 |
| Table | `Given` / `When` / `Expected result under this rule`; rows `<ordinary case>`, `<boundary case>`, `<counterexample>` | source inspected at 58a1477 |
| `Open question` | "<specific uncertainty>" | source inspected at 58a1477 |
| `Clarification owner` | "<actual name, once agreed>" | source inspected at 58a1477 |
| `Next use` | "<contract / check / decision that depends on this>" | source inspected at 58a1477 |
| Term template | "**term · context · meaning · counterexample · status/source**" | source inspected at 58a1477 |
| Glossary columns | Section 2: `ID / term \| Context \| Working meaning \| Counterexample / boundary`. PAY- section, #13, #15: `ID / term \| Meaning (as implemented) \| Boundary / counterexample` | source inspected at 58a1477 |
| README evidence kinds | "source inspected, test run at a revision, or live journey verified at a deployed revision. None is interchangeable with another." | source inspected at 58a1477 |

### Template fields used per PR

| PR | Deviations from the template | Evidence |
|---|---|---|
| #1 (main) | Rule, Policy status, Terms, Implementation evidence, "Examples and boundaries" (`Given \| When \| Result`), Open question, Next use; no Decision source, Candidate responsibility or Clarification owner | source inspected at 58a1477 |
| #3 (main) | Rule, Policy status, Terms, table, Open question (owner inline), "Evidence" | source inspected at 58a1477 |
| #4 | "Statement (observed implementation)", "Policy", "Evidence" + "Checks and limits", "Question PRC-Q0n"; no Decision source, Candidate responsibility, Next use | class PR #4 diff at 9478b3e |
| #5 | All fields, exact table header; "Open question Q06" | class PR #5 diff at 0712a1c |
| #6 | "Statement (observed implementation)", three "Evidence —" lines, "Candidate owner", "Given / When / Result (✓ = run[, † = read only])", "Question Q-SLOT-n" + "Uncertainty"; no Decision source, Next use | class PR #6 diff at c18b638 |
| #7 | "Observed rule", "Policy", "Evidence", "Candidate owner", "Question MET-Q01", extra "How names are stored"; no Decision source, Next use | class PR #7 diff at 05e90b3 |
| #8 | "Observed rule", "Policy", "Evidence", two-column tables, "Question Q-MET-n"; no Decision source, Candidate responsibility, Next use | class PR #8 diff at ce99d13 |
| #9 | Prose rule, no status, unpinned evidence, Given/When/Result, "Question"; no Decision source, Candidate responsibility, Next use | class PR #9 diff at 9afd71f |
| #10 | "Rule (observed implementation)", "Result (✓ = run)", "Open question Q-ACC-n", extra "Uncertainty"; otherwise complete | class PR #10 diff at d68631f |
| #11 | All fields, exact names, exact table header | class PR #11 diff at 7cf2656 |
| #12 | "Statement (observed implementation)", "Open question Q07"; otherwise complete | class PR #12 diff at 1c8ce57 |
| #13 | Old names: "Statement (observed implementation)", "Evidence", "Question" | class PR #13 diff at c8a302f |
| #14 (main) | Rule, Policy status (with decision source inside), Terms, "Relationship to existing work", a price table, Implementation evidence, "Scope", Next use | source inspected at 58a1477 |
| #15 | Old names: "Statement (observed implementation)", "Evidence", "Examples and boundaries", "Uncertainty / questions" | class PR #15 diff at 9e4971a |
