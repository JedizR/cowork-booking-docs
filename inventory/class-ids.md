# Class IDs

Every term, rule and question ID found anywhere in the class rules record: main `58a1477`, the base commits `a853795` and `1124404`, every PR head (#1, #3-#15) and every PR body. This is the input for `ID_MAP.md` (M1), which must list each of these exactly once.

How it was found: `git show <ref>:{GLOSSARY,RULES,README}.md` for every ref, grepped for `(EX|PAY|PRC|SLOT|MET|TIM|ACC|BOOK|AVL)-[TRQ]\d{2}`, `Q-[A-Z]+-\d+` and `Q\d{1,2}`; plus `gh pr view <n> --json body` for every PR. Ranges such as "EX-T02–EX-T04" were expanded by hand.

Sorted by ID in ASCII order. The one unnumbered rule is listed last. "Defined in" lists every place that defines the ID. Titles are as written; where two sources disagree, both are given. Totals: 27 terms, 22 rules (21 numbered plus the unnumbered booking-price rule), 19 question labels; 68 rows.

| ID | Kind | Title (as written) | Defined in | Referenced-only? | Notes | Evidence |
|---|---|---|---|---|---|---|
| ACC-R01 | rule | Registering creates an account keyed by its email | PR #10 | no | Context Purchase after the course instructor's review (was "Identity"). Q-ACC-1 is registration enumeration (flaw F11). | class PR #10 diff at d68631f |
| ACC-R02 | rule | Login starts a cookie session; logout clears it in that browser only | PR #10 | no | No expiry, browser-only logout (flaw F10) | class PR #10 diff at d68631f |
| ACC-T01 | term | Account | PR #10 | no | Overlaps EX-T01, EX-T09 ("Shared journey" on main) | class PR #10 diff at d68631f |
| ACC-T02 | term | Login session | PR #10 | no | | class PR #10 diff at d68631f |
| AVL-R01 | rule | #15: "A space is available if no booking overlaps the window"; #13: "With no time given, "available" means free right now" | PR #13, PR #15 | no | Clash K1; #13's meaning is a sub-clause of #15's. Take #15 as the base. | class PR #15 diff at 9e4971a |
| AVL-R02 | rule | #15: "An availability window must be complete, in order and have a timezone"; #13: "Any booking blocks the whole space" | PR #13, PR #15 | no | Clash K1: **different meanings under one ID**. #13's content lives inside #15 AVL-R01. Referenced by #15 AVL-T02. | class PR #15 diff at 9e4971a |
| AVL-T01 | term | Available | PR #13, PR #15 | no | Clash K1: same concept; #15 is a superset | class PR #15 diff at 9e4971a |
| AVL-T02 | term | #15: "Availability window"; #13: "Time window" | PR #13, PR #15 | no | Clash K1: same concept, different name | class PR #15 diff at 9e4971a |
| BOOK-R01 | rule | Party size within space capacity | PR #11 | no | Renames main EX-R01 and changes its status and examples (K6). Referenced in #11's README. | class PR #11 diff at 7cf2656 |
| BOOK-T01 | term | Party size | PR #11 | no | Context "Booking"; the course instructor asked for "Purchase" (unaddressed). Implicitly replaces EX-T06/T07. | class PR #11 diff at 7cf2656 |
| BOOK-T02 | term | Capacity | PR #11 | no | Context "Booking" | class PR #11 diff at 7cf2656 |
| EX-R01 | rule | Party size within capacity | main (course instructor, `a853795`) | no | Status "proposed". Referenced by README, #15 AVL-T01. Renamed to BOOK-R01 by #11 (K6). Evidence links use the old repo name. | source inspected at 58a1477 |
| EX-R02 | rule | Valid interval and no overlap | main (course instructor, `a853795`) | no | Status "observed; intended turnover policy unresolved". Referenced by #6, #13, #15. | source inspected at 58a1477 |
| EX-R03 | rule | (never defined) | none | **yes** | Referenced by main README "EX-R01/EX-R03" and by #11's README (K8). Probably lived in the missing `DOMAIN_MODEL.md`. | source inspected at 58a1477 |
| EX-R04 | rule | Guest vs. account-linked booking is decided once, at creation | main (PR #3) | no | Only `/bookings/mine` checks ownership (flaw F7) | source inspected at 58a1477 |
| EX-R05 | rule | Spaces with existing bookings cannot be deleted | PR #5 | no | Evidence unpinned; context "Space Management / Inventory"; skips EX-R03 | class PR #5 diff at 0712a1c |
| EX-T01 | term | Member | main (course instructor, `fbdabd3`) | no | Context "Shared journey". Referenced by #1, #3, #7, #8, #10. | source inspected at 58a1477 |
| EX-T02 | term | Space | main (course instructor, `fbdabd3`) | no | Context "Purchase". Referenced by #4, #5, #6, #13, #15. | source inspected at 58a1477 |
| EX-T03 | term | (never defined) | none | **yes** | Only inside the range "EX-T02–EX-T04" in main EX-R02 Terms (K8) | source inspected at 58a1477 |
| EX-T04 | term | (never defined) | none | **yes** | Main EX-R02 Terms "EX-T02–EX-T04" (K8) | source inspected at 58a1477 |
| EX-T06 | term | (never defined) | none | **yes** | Main EX-R01 Terms "EX-T02, EX-T06, EX-T07"; dropped by #11 (K8) | source inspected at 58a1477 |
| EX-T07 | term | (never defined) | none | **yes** | Same as EX-T06 (K8) | source inspected at 58a1477 |
| EX-T08 | term | Guest | main (PR #3) | no | Context "Shared journey" | source inspected at 58a1477 |
| EX-T09 | term | Account-linked booking | main (PR #3) | no | Duplicates EX-R04 (reviewer point, unaddressed). Referenced by #6. | source inspected at 58a1477 |
| MET-Q01 | question | What should "Members" on the investor dashboard count? | PR #7 | no | Same question as Q-MET-1 | class PR #7 diff at 05e90b3 |
| MET-R01 | rule | Metrics count members by exact name text | PR #7, PR #8 | no | Duplicate K2; same title and meaning | class PR #8 diff at ce99d13 |
| MET-R02 | rule | A subscriber's booking counts as paid with zero revenue | PR #8 | no | Restates part of PAY-R01 | class PR #8 diff at ce99d13 |
| MET-T01 | term | Counted member | PR #7, PR #8 | no | Duplicate K2; context "Reporting" (not one of the three) | class PR #8 diff at ce99d13 |
| MET-T02 | term | Paid booking (metrics) | PR #8 | no | Duplicates PAY-T01 | class PR #8 diff at ce99d13 |
| PAY-R01 | rule | A subscriber's booking starts as paid | main (PR #1) | no | Contradicted by SLOT-T01 wording (K5). Referenced by #14. | source inspected at 58a1477 |
| PAY-R02 | rule | Payment requires syntactically valid card details (head: "Paying needs a card that looks valid") | main (PR #1) | no | Amount-0 row: card still required (flaw F16) | source inspected at 58a1477 |
| PAY-R03 | rule | An access code needs only a paid booking | main (PR #1) | no | Contradicted by PAY-R04 (K4). Referenced by #12. | source inspected at 58a1477 |
| PAY-R04 | rule | An access code is generated once and stored | PR #12 | no | Contradicts the code and PAY-R03 (K4); unpinned; matches the course's *proposed* policy | class PR #12 diff at 1c8ce57 |
| PAY-T01 | term | Paid | main (PR #1) | no | Referenced by #6, #12, #15 | source inspected at 58a1477 |
| PAY-T02 | term | Member name | main (PR #1) | no | A Purchase concern under a PAY- prefix | source inspected at 58a1477 |
| PAY-T03 | term | Subscription | main (PR #1) | no | Coverage; Purchase concern | source inspected at 58a1477 |
| PAY-T04 | term | Access code | main (PR #1) | no | Access concern; "It is not saved". Referenced by #12. | source inspected at 58a1477 |
| PRC-Q01 | question | Minimum charge / fractional seconds / maximum rate or duration | PR #4 | no | Still open on main (#14 scope note) | class PR #4 diff at 9478b3e |
| PRC-Q02 | question | Fixed at booking or payment? Historical unknown amounts? | PR #4 | no | First half answered on main by #14 | class PR #4 diff at 9478b3e |
| PRC-R01 | rule | Booking amounts follow duration and cent rounding | PR #4 | no | Referenced on main by #14 ("Consolidate this clarification into PRC-R01"); status "observed" is stale against main (O2) | class PR #4 diff at 9478b3e |
| PRC-R02 | rule | A later rate change preserves stored booking amounts | PR #4 | no | | class PR #4 diff at 9478b3e |
| PRC-T01 | term | Hourly rate | PR #4 | no | Main #14 refers to "hourly rate" without an ID | class PR #4 diff at 9478b3e |
| PRC-T02 | term | main: "Booking price"; PR #4: "Booking amount" | main (PR #14), PR #4 | no | Clash K3 (same concept, two titles) | source inspected at 58a1477 |
| Q-ACC-1 | question | Registration reveals an existing email: acceptable? | PR #10 | no | Also in the #10 body | class PR #10 diff at d68631f |
| Q-ACC-2 | question | Password policy; must email be confirmed? | PR #10 | no | | class PR #10 diff at d68631f |
| Q-ACC-3 | question | Should logout end the session everywhere? Should sessions expire? | PR #10 | no | | class PR #10 diff at d68631f |
| Q-ACC-4 | question | Limit failed logins? Book under another member name? | PR #10 | no | Not in the #10 body | class PR #10 diff at d68631f |
| Q-MET-1 | question | Count people or accounts rather than typed names? | PR #8 | no | Same question as MET-Q01 | class PR #8 diff at ce99d13 |
| Q-MET-2 | question | Exclude subscriber bookings from conversion and average revenue? | PR #8 | no | | class PR #8 diff at ce99d13 |
| Q-SLOT-1 | question | Should an unpaid booking hold a slot at all? | PR #6 | no | | class PR #6 diff at c18b638 |
| Q-SLOT-2 | question | For how long before release (payment deadline)? | PR #6 | no | | class PR #6 diff at c18b638 |
| Q-SLOT-3 | question | Who may release an abandoned booking? | PR #6 | no | | class PR #6 diff at c18b638 |
| Q-SLOT-4 | question | Refund and record on a paid cancel? | PR #6 | no | | class PR #6 diff at c18b638 |
| Q-SLOT-5 | question | Who may cancel? | PR #6 | no | | class PR #6 diff at c18b638 |
| Q01 | question | EX-R01's question: "what do we sell: exclusive space, group booking or shared seats? What about already-made bookings if capacity falls?" | base `a853795` (course instructor) | no | Label removed on main by `81e490e` (text kept as "Open question"). Referenced by #13 AVL-R02 "(see Q01)", now dangling. | source inspected at a853795 |
| Q03 | question | EX-R02's question: "does the business require turnover time? ... A 15-minute cleaning gap is not currently an approved rule." | base `a853795` (course instructor) | no | Label removed on main by `81e490e` | source inspected at a853795 |
| Q05 | question | EX-R04's ownership question | PR #3 head (and body) | no | Label removed on main by `81e490e` | class PR #3 diff at 6752b24 |
| Q06 | question | EX-R05's space-retirement / archive question | PR #5 | no | PR #5's body calls the same question "Q07" | class PR #5 diff at 0712a1c |
| Q07 | question | PR #12: should the access code become invalid after the booking's end time? | PR #12 (and PR #5 body, for a different question) | no | **Same label, two questions**: #12 (access-code expiry) and the #5 body (space retirement) | class PR #12 diff at 1c8ce57 |
| SLOT-R01 | rule | An unpaid booking holds its slot until it is cancelled | PR #6 | no | Referenced by #15 | class PR #6 diff at c18b638 |
| SLOT-R02 | rule | Cancelling deletes a booking and frees its slot | PR #6 | no | Hard delete (flaw F5) | class PR #6 diff at c18b638 |
| SLOT-T01 | term | Unpaid booking | PR #6 | no | "A subscriber's booking is never unpaid" contradicts PAY-R01 (K5) | class PR #6 diff at c18b638 |
| SLOT-T02 | term | Held slot | PR #6 | no | "Held" means any booking, paid or not; clashes with our `held` status (O13) | class PR #6 diff at c18b638 |
| SLOT-T03 | term | Cancellation | PR #6 | no | Hard delete; JSON API only | class PR #6 diff at c18b638 |
| TIM-R01 | rule | The form turns client time into Bangkok; the API does not | PR #9 | no | Conflict K7; unpinned evidence; referenced by #15 | class PR #9 diff at 9afd71f |
| TIM-T01 | term | Client time (was "Naive datetime" at `bb5133c`) | PR #9 | no | Referenced by #15 | class PR #9 diff at 9afd71f |
| TIM-T02 | term | Server time (was "Instant" at `bb5133c`) | PR #9 | no | | class PR #9 diff at 9afd71f |
| (no ID) | rule | Booking price — Purchase rule clarification | main (PR #14) | no | The only stakeholder-clarified rule; needs a stable ID (O1); #14 points at PRC-R01 | source inspected at 58a1477 |

## Not IDs

| Label | Where | Why it is not listed above | Evidence |
|---|---|---|---|
| EX-T05 | nowhere | Never referenced in any ref or body; the numbering gap is between EX-T04 and EX-T06 | source inspected at 58a1477 |
| PR #1 body questions 1-5 | PR #1 body | A numbered list ("1. **Is "paid" the right word?**" ...), not ID labels | class PR #1 discussion |
| Spacey issue #82 | PR #6 review | Issue number, not a rule ID | class PR #6 discussion |
| Spacey issues #120, #121, #122 | PR #10 ACC-R01 / ACC-R02 decision sources | Issue numbers, not rule IDs | class PR #10 diff at d68631f |

Spacey issue #173 is cited by BRIEF D25; not inventory evidence.
