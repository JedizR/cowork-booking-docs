# Course statements

Every course statement this project relies on, verbatim, with its page and evidence type. Course text is guidance for this project, not project policy; M1 turns what we adopt into Decided rules.

Pages were fetched with `curl -sL` on 2026-09-30 (hashes in [`../SOURCES.md`](../SOURCES.md)). Some text appears only after a click; it was read from the page's inline `<script>` and is marked "(after click)". No browser was driven.

Notation: " / " stands for a line break in the source. `"Heading": "body"` is a heading followed by its body. `[persona]` replaces a startup persona's name.

## 1. BRIEF quotes checked against the sites

Method: each BRIEF string was searched as an exact substring in the tag-stripped text (entities decoded, whitespace collapsed, inline-script strings included) of all three pages. A trailing full stop is ignored. "Paraphrase" means the BRIEF does not put the text in quotes.

| # | BRIEF § | BRIEF text | Found verbatim? | Exact site wording or note | Evidence |
|---|---|---|---|---|---|
| Q01 | 2 | "Work is graded on evidence and trade-offs, not on the volume of generated output or the polish of a demo." | yes | Identical (Evaluation and grading) | course site [syllabus site] fetched 2026-09-30 |
| Q02 | 2 | "a small, explicitly agreed change spanning the three services, with unsupported cases recorded." | yes (fragment) | "Cancellation is a small, explicitly agreed change spanning the three services, with unsupported cases recorded." | course site [syllabus site] fetched 2026-09-30 |
| Q03 | 2 | cancellation is "the course's flagship cross-service change" (paraphrase) | no | The word "flagship" is not on any page. Support: Q02; grading row "Cancellation shipped to production" 15% (tied largest team weight); outline days 8 and 13. | course site [syllabus site] fetched 2026-09-30 |
| Q04 | 3.2 | "Separate ownership, still one monolith" | yes (after click) | View label after "Proposed next step"; the default label is "Current coupling" | course site [extraction site] fetched 2026-09-30 |
| Q05 | 3.2 | the course takes a "strangler path" (paraphrase) | no (paraphrase) | Syllabus: "extract a monolith into independently deployable services using a strangler approach;" and day 4 "Extraction mechanics, strangler patterns, data ownership, and the shared database". The extraction site never uses the word. | course site [syllabus site] fetched 2026-09-30 |
| Q06 | 3.7 | "change the context to the existing 'Purchase' ... In the future can be extracted in the different context" | not a course-site quote | On no course page; the BRIEF says it is a PR review. Found in class PR #10 as "change the context to the existing \"Purchase\" and good to go" / "In the future can be extracted in the different context", written by the **course instructor** (BRIEF says "class reviewer"). See section 5. | class PR #10 discussion |
| Q07 | 3.7 | "Shared references connect the models. They do not make them one shared object." | yes | Identical | course site [contexts site] fetched 2026-09-30 |
| Q08 | 3.7 | Stores "Reservations (space, time, agreed price, coverage), Payments (booking reference, amount, outcome), Access grants (booking reference, resource, grant state)" (paraphrase) | matches in substance | "Reservations": "space · time / agreed price · coverage"; "Payments": "booking reference / amount · outcome"; "Access grants": "booking reference / resource · grant state" (hidden until "Proposed next step"). The contexts site shows different fields (see C07, C09, C11). | course site [extraction site] fetched 2026-09-30 |
| Q09 | 4 | "Owns price and coverage" | yes (after click) | Proposed view, Purchase node; default "Creates the booking" | course site [extraction site] fetched 2026-09-30 |
| Q10 | 4 | "Owns payment outcomes" | yes (after click) | Proposed view, Payments node | course site [extraction site] fetched 2026-09-30 |
| Q11 | 4 | "Owns grants and issuance" | yes (after click) | Proposed view, Access node | course site [extraction site] fetched 2026-09-30 |
| Q12 | 4 | "Collect this agreed amount" | yes | Site: "“Collect this agreed amount.”" (curly quotes, full stop) | course site [extraction site] fetched 2026-09-30 |
| Q13 | 4 | "Purchase interprets the result" | yes | Step heading | course site [extraction site] fetched 2026-09-30 |
| Q14 | 4 | "Payment or subscription coverage?" | yes | Identical | course site [extraction site] fetched 2026-09-30 |
| Q15 | 4 | "Issue an authorised grant" | yes | Site: "“Issue an authorised grant.”" | course site [extraction site] fetched 2026-09-30 |
| Q16 | 4 | "“Covered” is not always “money collected”." | yes | Identical, same curly quotes | course site [extraction site] fetched 2026-09-30 |
| Q17 | 4 | "Paid ≠ subscription-covered." | **no** (wording differs) | Site: "Units, success and failure. “Paid” ≠ subscription-covered." ("Paid" is in curly quotes). Quote the site form in docs. | course site [extraction site] fetched 2026-09-30 |
| Q18 | 4 | "Payments does not re-price the booking." | yes | Identical. On the contexts site only, not the extraction site. | course site [contexts site] fetched 2026-09-30 |
| Q19 | 4 | "Success, invalid input, failure, repeat; coverage skips collection." | yes | Under "Which examples?" | course site [extraction site] fetched 2026-09-30 |
| Q20 | 4 | "Reuse or new attempt? Agree identity and behaviour; do not assume." | yes | Under "What if repeated?" | course site [extraction site] fetched 2026-09-30 |
| Q21 | 4 | "Beside the provider’s code. Agreed with its consumer" | yes | Site ends with a full stop | course site [extraction site] fetched 2026-09-30 |
| Q22 | 4 | "Add OpenAPI for HTTP" | yes | Body: "Operations and schemas, linked to behavioural promises." | course site [extraction site] fetched 2026-09-30 |
| Q23 | 4 | "One authoritative copy" | yes (fragment) | "One authoritative copy—not two drifting copies." | course site [extraction site] fetched 2026-09-30 |
| Q24 | 4 | "Provider maintains it. Consumer reviews it. Proposed, agreed and verified are different states." | yes | Identical | course site [extraction site] fetched 2026-09-30 |
| Q25 | 4 | "reuse the credential for the same valid grant" | yes (after click) | After "Show proposed behaviour": "Proposed policy: reuse the credential for the same valid grant." Static text elsewhere: "Repeated access requests reuse a credential?" | course site [extraction site] fetched 2026-09-30 |
| Q26 | 4 | "This is a behaviour change: agree the rule, then implement and check." (paraphrase) | no (paraphrase) | Site: "This changes behaviour: agree its scope and exceptions, update the rule, then implement and check." The BRIEF drops "scope and exceptions". | course site [extraction site] fetched 2026-09-30 |
| Q27 | 4 | "A stored grant does not by itself prove that a door can be opened." | yes | Identical | course site [extraction site] fetched 2026-09-30 |
| Q28 | 4 | "Payment success ≠ access provisioned ≠ a successful door opening." | yes | Identical. Contexts site only. | course site [contexts site] fetched 2026-09-30 |
| Q29 | 4 | "The booking and successful payment remain recorded. No automatic refund is implied." | yes (after click) | After "Revoke access": "Access is revoked. The booking and successful payment remain recorded. No automatic refund is implied." | course site [contexts site] fetched 2026-09-30 |
| Q30 | 4 | The syllabus names the third team "Integrations/Locks" | yes | "Students work in three teams, one for each bounded context: Purchase, Payments, and Integrations/Locks." The contexts site writes "Integrations / Locks"; the extraction site says "Access". | course site [syllabus site] fetched 2026-09-30 |
| Q31 | 4 | teams talk over REST (paraphrase) | yes in substance | "Teams communicate between services over REST." and day 5 "Extraction: three services, REST between them, each independently deployable" | course site [syllabus site] fetched 2026-09-30 |
| Q32 | 4 | Artefacts include service contracts, ADRs, specifications and a PRD (paraphrase) | yes in substance | "service contracts, architecture decisions, technical specifications, product requirements, pull-request reviews, release records, and incident records." Grading row: "Documentation artefacts—contracts, ADRs, specifications, and PRD contribution" | course site [syllabus site] fetched 2026-09-30 |
| Q33 | 4 | "Three services are the course exercise, not a claim that every growing business should split" | yes (truncated) | Full sentence: "Three services are the course exercise, not a claim that every growing business should split its application; students compare the costs and benefits with alternative boundaries and modules within a monolith." Quote it in full. | course site [syllabus site] fetched 2026-09-30 |
| Q34 | 4 | The course target comes "from the extraction and contexts sites" | partly | Q18, Q28 and Q29 are on the contexts site; Q01, Q02 and Q30-Q33 are on the syllabus; the rest are on the extraction site | course site [extraction site] fetched 2026-09-30 |

BRIEF section 7 quotes no course text, so it adds no row. Result: every quoted course string is on a course page except Q17 (curly quotes around "Paid" on the site) and Q06 (a PR review, not course text). Q03 and Q26 are paraphrases that differ from the site.

## 2. Extraction site — [extraction site]

Page title "Untangle before you split · Spacey". It describes itself as "Illustrative target design; not implemented services." It names the parts Purchase, Payments and Access; it never says "Integrations/Locks", "strangler", revoke, grading or cancellation. Links: the contexts site (header) and the class rules `RULES.md` (footer).

| # | Statement (verbatim) | Topic | Visible | Evidence |
|---|---|---|---|---|
| E03 | "Untangle before / you split." | strangler path | shown | course site [extraction site] fetched 2026-09-30 |
| E04 | "Separate the data and behaviour. Keep one application first." | strangler path | shown | course site [extraction site] fetched 2026-09-30 |
| E05 | View buttons "Today" and "Proposed next step"; caption "ONE APPLICATION" | one monolith | shown | course site [extraction site] fetched 2026-09-30 |
| E06 | View label (Today): "Current coupling" | ownership | shown | course site [extraction site] fetched 2026-09-30 |
| E07 | Today: "Purchase": "Creates the booking"; "Payments": "Changes booking.paid"; "Access": "Reads booking.paid" | ownership (observed) | shown | course site [extraction site] fetched 2026-09-30 |
| E08 | Today store: "Booking record": "price · paid · card_last4" / "Access code: generated, not saved" | ownership (observed) | shown | course site [extraction site] fetched 2026-09-30 |
| E09 | "Moving the helpers into new files would leave this shared-data dependency." | extraction | shown | course site [extraction site] fetched 2026-09-30 |
| E10 | View label (Proposed): "Separate ownership, still one monolith" | one monolith | after click | course site [extraction site] fetched 2026-09-30 |
| E11 | Proposed: "Purchase": "Owns price and coverage"; "Payments": "Owns payment outcomes"; "Access": "Owns grants and issuance" | ownership | after click | course site [extraction site] fetched 2026-09-30 |
| E12 | Proposed stores: "Reservations": "space · time / agreed price · coverage"; "Payments": "booking reference / amount · outcome"; "Access grants": "booking reference / resource · grant state" | stores | hidden until click | course site [extraction site] fetched 2026-09-30 |
| E13 | "New tables + extracted operations + explicit contracts. Agree migration and compatibility before switching callers." | strangler path | after click | course site [extraction site] fetched 2026-09-30 |
| E14 | "Purchase → Payments": "“Collect this agreed amount.”" | call flow | shown | course site [extraction site] fetched 2026-09-30 |
| E15 | "Purchase interprets the result": "Payment or subscription coverage?" | call flow | shown | course site [extraction site] fetched 2026-09-30 |
| E16 | "Purchase → Access": "“Issue an authorised grant.”" | call flow | shown | course site [extraction site] fetched 2026-09-30 |
| E17 | "Proposed internal calls. Payments and locks remain mocked." | call flow | shown | course site [extraction site] fetched 2026-09-30 |
| E18 | "Which repository changes?" / "Ask: did the meaning or behaviour change?" | change routing | shown | course site [extraction site] fetched 2026-09-30 |
| E19 | "Business model": "“Covered” is not always “money collected”." | coverage | shown | course site [extraction site] fetched 2026-09-30 |
| E20 | "Business model": "Repeated access requests reuse a credential?" | access policy | shown | course site [extraction site] fetched 2026-09-30 |
| E21 | "Business model" destination: "Glossary + rules + examples" | change routing | shown | course site [extraction site] fetched 2026-09-30 |
| E22 | "Implementation design": "Store payments in their own table." | ownership | shown | course site [extraction site] fetched 2026-09-30 |
| E23 | "Implementation design": "Move issuance behind an Access interface." | extraction | shown | course site [extraction site] fetched 2026-09-30 |
| E24 | "Implementation design" destination: "Architecture decision + code + migration" | change routing | shown | course site [extraction site] fetched 2026-09-30 |
| E25 | "Where does the contract live?" / "Beside the provider’s code. Agreed with its consumer." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E26 | "Now · one application" / "Contract documents": "One for Payments. / One for Access." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E27 | "Python interface + tests": "Explicit inputs, results and checked examples." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E28 | "Keep the agreement beside the code it describes." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E29 | "Later · separate services" / "Each provider’s repository": "Move its contract with it →": "Payments keeps Payments. / Access keeps Access." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E30 | "Add OpenAPI for HTTP": "Operations and schemas, linked to behavioural promises." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E31 | "One authoritative copy—not two drifting copies." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E32 | "Business rules": "Meaning + policy / in spacey-business-rules" → "Contract document": "Promises + rule-ID links / beside provider code" → "Interface + tests": "Shape + evidence / against those promises" | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E33 | "Illustrative proposal · negotiate before implementing" / "A payment boundary on one page" | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E34 | "Purchase sends": "Booking reference / Agreed amount + currency / Required mock-payment input" | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E35 | "Payments owns": "Payment record / Processing outcome / Not booking or access state" | ownership | shown | course site [extraction site] fetched 2026-09-30 |
| E36 | "Purchase receives": "Payment reference / Matching amount + outcome / Then applies booking rules" | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E37 | "What does it mean?": "Units, success and failure. “Paid” ≠ subscription-covered." | coverage | shown | course site [extraction site] fetched 2026-09-30 |
| E38 | "What can change?": "Payments writes its record; Purchase owns the reservation." | ownership | shown | course site [extraction site] fetched 2026-09-30 |
| E39 | "What if repeated?": "Reuse or new attempt? Agree identity and behaviour; do not assume." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E40 | "Which examples?": "Success, invalid input, failure, repeat; coverage skips collection." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E41 | "Provider maintains it. Consumer reviews it. Proposed, agreed and verified are different states." | contracts | shown | course site [extraction site] fetched 2026-09-30 |
| E42 | "A refactor—or a new rule?" / "Use repeated access requests to tell the difference." | access policy | shown | course site [extraction site] fetched 2026-09-30 |
| E43 | "Ask for access twice": "First request" "Credential A" → "Second request" "Credential B" | access policy | shown | course site [extraction site] fetched 2026-09-30 |
| E44 | "Observed current behaviour: each request generates a new code. Moving the code alone does not change this rule." | access policy (observed) | shown | course site [extraction site] fetched 2026-09-30 |
| E45 | "Proposed policy: reuse the credential for the same valid grant. This changes behaviour: agree its scope and exceptions, update the rule, then implement and check." (the second credential then reads "Credential A") | access policy | after click | course site [extraction site] fetched 2026-09-30 |
| E46 | "A stored grant does not by itself prove that a door can be opened." | access policy | shown | course site [extraction site] fetched 2026-09-30 |
| E47 | "Keep the evidence connected." | evidence | shown | course site [extraction site] fetched 2026-09-30 |
| E48 | "01" "Rule + example": "What should happen?"; "02" "Contract": "What can each side rely on?"; "03" "Data + code": "Who owns and changes the state?"; "04" "Check + link back": "What actually happened?" | evidence chain | shown | course site [extraction site] fetched 2026-09-30 |
| E49 | "Same behaviour? Keep the rule, update its evidence. / New behaviour? Agree the rule, then verify it." | evidence | shown | course site [extraction site] fetched 2026-09-30 |
| E50 | "Illustrative target design; not implemented services. / Current-code baseline: e734fc7. No real payment or lock." | status; evidence pin | shown | course site [extraction site] fetched 2026-09-30 |

Gaps in the numbering (E01, E02: page titles; E51: links) are statements not relied on.

## 3. Contexts site — [contexts site]

Page title "One booking. Three models." The third model is named "Integrations / Locks" (with spaces). The footer says "Illustrative models, not the current Spacey implementation." No link to the extraction site or the syllabus.

| # | Statement (verbatim) | Topic | Visible | Evidence |
|---|---|---|---|---|
| C02 | "Models → meanings → contracts" | contracts | shown | course site [contexts site] fetched 2026-09-30 |
| C03 | "One booking. Three models." | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C04 | "Same real-world story. Different questions to answer." | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C05 | "[persona] books a room" / "Member m7 · Booking b42 · 10:00–11:00" | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C06 | Card 1: "Purchase" / "What is the price of this booking?" | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C07 | Card 1 entity "Reservation · b42": "Member" "m7", "Space" "Room A", "Time" "10:00–11:00", "Agreed price" "฿300", status "Booking confirmed" | stores | shown | course site [contexts site] fetched 2026-09-30 |
| C08 | Card 2: "Payments" / "Did we collect the requested amount?" | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C09 | Card 2 entity "Payment · p17": "Booking reference" "b42", "Amount to collect" "฿300", "Currency" "THB", "Attempt" "a9", status "Payment succeeded" | stores | shown | course site [contexts site] fetched 2026-09-30 |
| C10 | Card 3: "Integrations / Locks" / "May [persona] enter this door now?" | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C11 | Card 3 entity "Access grant · g8": "Subject" "m7", "Booking reference" "b42", "Door" "A-01", "Valid window" "10:00–11:00", status "Access provisioned" | stores | shown | course site [contexts site] fetched 2026-09-30 |
| C12 | "Shared references connect the models. They do not make them one shared object." | contexts | shown | course site [contexts site] fetched 2026-09-30 |
| C13 | "Change one fact." / "Try revoking the access grant. What should happen to the payment?" (button "Revoke access") | revoke | shown | course site [contexts site] fetched 2026-09-30 |
| C14 | Status becomes "Access revoked"; text "Access is revoked. The booking and successful payment remain recorded. No automatic refund is implied." | revoke | after click | course site [contexts site] fetched 2026-09-30 |
| C15 | "Access is restored in this illustration. The payment record has not changed." (button "Restore access") | revoke | after second click | course site [contexts site] fetched 2026-09-30 |
| C16 | "Same ฿300. Different meaning." | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C17 | "Purchase defines the price. Payments collects the requested amount." | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C18 | Purchase: "Agreed price" / "฿300 for this reservation." / "Owns pricing rules and the agreed total." | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C19 | Payments: "Amount to collect" / "฿300 requested by Purchase." / "Owns collection and its outcome." | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C20 | Integrations / Locks: "No price needed" / "Needs an authorised access grant." / "Checks subject, door, time and revocation." | stored grant vs door | shown | course site [contexts site] fetched 2026-09-30 |
| C21 | "A price decision becomes a payment instruction." / "Access needs permission, not pricing rules." | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C22 | "The contract connects the meanings." | contracts | shown | course site [contexts site] fetched 2026-09-30 |
| C23 | "One pricing authority. An explicit request and result." | contracts | shown | course site [contexts site] fetched 2026-09-30 |
| C24 | Purchase endpoint: "Defines the agreed price" | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C25 | Request: "Purchase → Payments" / "Collect ฿300 THB for b42" | contracts | shown | course site [contexts site] fetched 2026-09-30 |
| C26 | "Same amount and currency." / "Payments does not re-price the booking." | contracts | shown | course site [contexts site] fetched 2026-09-30 |
| C27 | Result: "Payments → Purchase" / "p17 · succeeded · ฿300 THB" | contracts | shown | course site [contexts site] fetched 2026-09-30 |
| C28 | Payments endpoint: "Collects and reports the outcome" | ownership | shown | course site [contexts site] fetched 2026-09-30 |
| C29 | "Payment success ≠ access provisioned ≠ a successful door opening." | stored grant vs door | shown | course site [contexts site] fetched 2026-09-30 |
| C30 | Footer: "Illustrative models, not the current Spacey implementation." | status | shown | course site [contexts site] fetched 2026-09-30 |
| C31 | Footer: "Shared time zone assumed. No real payment or lock is connected." | time zone; mocks | shown | course site [contexts site] fetched 2026-09-30 |

C01 (site label) and C32 (an off-site reading link) are not relied on. The contexts site never uses the word "coverage"; its Reservation card has no coverage field.

### Contexts site vs BRIEF wording

| Item | BRIEF | Contexts site | Evidence |
|---|---|---|---|
| Third context name | "Access" | "Integrations / Locks" (the syllabus writes "Integrations/Locks") | course site [contexts site] fetched 2026-09-30 |
| Reservation fields | space, time, agreed price, coverage | "Member", "Space", "Time", "Agreed price"; no coverage | course site [contexts site] fetched 2026-09-30 |
| Payment fields | booking reference, amount, outcome | "Booking reference", "Amount to collect", "Currency", "Attempt", status "Payment succeeded" | course site [contexts site] fetched 2026-09-30 |
| Access grant fields | booking reference, resource, grant state | "Subject", "Booking reference", "Door", "Valid window", status "Access provisioned" / "Access revoked" | course site [contexts site] fetched 2026-09-30 |

## 4. Syllabus — [syllabus site]

The syllabus names no instructor or student. Its notice says "Updated 14 September 2026." while its footer says "updated 1 September 2026". Numbers are M0 labels over the whole page (S01-S116); gaps are statements this project does not rely on.

| # | Statement (verbatim) | Anchor | Topic | Evidence |
|---|---|---|---|---|
| S04 | "15-day intensive · 28 September – 16 October 2026 · examinations included" | / | dates | course site [syllabus site] fetched 2026-09-30 |
| S07 | "A startup rents bookable rooms and workbenches." | #2-abstract | domain | course site [syllabus site] fetched 2026-09-30 |
| S08 | "Paying members find a space, book it, pay, and enter through API-driven locks." | #2-abstract | member journey | course site [syllabus site] fetched 2026-09-30 |
| S11 | "Students normally start with the monolithic application developed by the three prep students." | #2-abstract | starting system | course site [syllabus site] fetched 2026-09-30 |
| S12 | "The selected starting revision and its actual provenance are identified at handover." | #2-abstract | provenance | course site [syllabus site] fetched 2026-09-30 |
| S13 | "They maintain one member journey while discovering the domain, negotiating responsibilities and extracting three independently deployable services." | #2-abstract | three services | course site [syllabus site] fetched 2026-09-30 |
| S15 | "Cancellation is a small, explicitly agreed change spanning the three services, with unsupported cases recorded." | #2-abstract | cancellation | course site [syllabus site] fetched 2026-09-30 |
| S16 | "The central question is why: what problem does an engineering practice solve, why choose it over an alternative, and what evidence shows that it helped?" | #2-abstract | evidence and trade-offs | course site [syllabus site] fetched 2026-09-30 |
| S20 | "explain why shared language and bounded contexts help resolve business-rule and ownership questions in a running system;" | #3-learning-highlights | glossary; contexts | course site [syllabus site] fetched 2026-09-30 |
| S21 | "design service boundaries, interface contracts, data ownership, and architecture decisions across teams;" | #3-learning-highlights | contracts; ADRs | course site [syllabus site] fetched 2026-09-30 |
| S22 | "extract a monolith into independently deployable services using a strangler approach;" | #3-learning-highlights | strangler path | course site [syllabus site] fetched 2026-09-30 |
| S23 | "use version control, pull-request review, continuous delivery, and rollback as coordination and safety systems;" | #3-learning-highlights | Git, PRs, CD, rollback | course site [syllabus site] fetched 2026-09-30 |
| S27 | "deliver a change spanning three services under operational pressure;" | #3-learning-highlights | cancellation | course site [syllabus site] fetched 2026-09-30 |
| S29 | "justify practices and service boundaries using observed benefits, costs, alternatives and uncertainty." | #3-learning-highlights | trade-offs | course site [syllabus site] fetched 2026-09-30 |
| S47 | "Merged code, deployed software and a solved user problem are different outcomes." | #6-methodology | evidence vs status | course site [syllabus site] fetched 2026-09-30 |
| S48 | "Simulated feedback is labelled and working software alone is not claimed as proof of customer value." | #6-methodology | evidence vs status | course site [syllabus site] fetched 2026-09-30 |
| S61 | "Three services are the course exercise, not a claim that every growing business should split its application; students compare the costs and benefits with alternative boundaries and modules within a monolith." | #6-methodology | services vs monolith modules | course site [syllabus site] fetched 2026-09-30 |
| S62 | "Students work in three teams, one for each bounded context: Purchase, Payments, and Integrations/Locks." | #6-methodology | context names | course site [syllabus site] fetched 2026-09-30 |
| S63 | "Teams communicate between services over REST." | #6-methodology | REST | course site [syllabus site] fetched 2026-09-30 |
| S65 | "Course artefacts are created in the tools where engineering work happens: service contracts, architecture decisions, technical specifications, product requirements, pull-request reviews, release records, and incident records." | #6-methodology | artefacts | course site [syllabus site] fetched 2026-09-30 |
| S66 | "Use short documents for a concrete decision, contract or handover, linking existing evidence instead of duplicating it." | #6-methodology | doc style | course site [syllabus site] fetched 2026-09-30 |
| S70 | "The team submissions cover a service boundary, independent deployment, a second-person rollback, and a specification linked to an implemented and verified change." | #7-evaluation-and-grading | deliverables | course site [syllabus site] fetched 2026-09-30 |
| S76 | Grading table: "Service delivered, independently deployable" "10%" "Team" | #7-evaluation-and-grading | grading | course site [syllabus site] fetched 2026-09-30 |
| S77 | Grading table: "Cancellation shipped to production" "15%" "Team" | #7-evaluation-and-grading | grading; cancellation | course site [syllabus site] fetched 2026-09-30 |
| S78 | Grading table: "Documentation artefacts—contracts, ADRs, specifications, and PRD contribution" "15%" "Team" | #7-evaluation-and-grading | grading; artefacts | course site [syllabus site] fetched 2026-09-30 |
| S80 | "Work is graded on evidence and trade-offs, not on the volume of generated output or the polish of a demo." | #7-evaluation-and-grading | grading | course site [syllabus site] fetched 2026-09-30 |
| S81 | "For a practice or boundary, explain the problem encountered, the alternatives, the reason for the choice and its observed consequences." | #7-evaluation-and-grading | ADR shape | course site [syllabus site] fetched 2026-09-30 |
| S82 | "Supported findings that a practice did not help are legitimate." | #7-evaluation-and-grading | evidence | course site [syllabus site] fetched 2026-09-30 |
| S83 | "AI tools are permitted throughout; no usage percentage or attestation is required." | #7-evaluation-and-grading | AI use | course site [syllabus site] fetched 2026-09-30 |
| S84 | "Students remain accountable for work under their name and may be asked to explain its decisions, trade-offs and verification." | #7-evaluation-and-grading | accountability | course site [syllabus site] fetched 2026-09-30 |
| S92 | "3 · Wed 30 Sep" "Boundary design, interface contracts, and the architecture decision to split" | #8-outline | schedule | course site [syllabus site] fetched 2026-09-30 |
| S93 | "4 · Thu 1 Oct" "Extraction mechanics, strangler patterns, data ownership, and the shared database" | #8-outline | strangler path | course site [syllabus site] fetched 2026-09-30 |
| S94 | "5 · Fri 2 Oct" "Extraction: three services, REST between them, each independently deployable" | #8-outline | REST; three services | course site [syllabus site] fetched 2026-09-30 |
| S95 | "6 · Mon 5 Oct" "Test the split: integration failures, boundary trade-offs and a change-management policy" | #8-outline | integration tests | course site [syllabus site] fetched 2026-09-30 |
| S96 | "7 · Tue 6 Oct" "Release safety, real rollback, on-call, severity, and incident command" | #8-outline | rollback | course site [syllabus site] fetched 2026-09-30 |
| S97 | "8 · Wed 7 Oct" "Cancellation product requirements under an operational interruption" | #8-outline | cancellation; PRD | course site [syllabus site] fetched 2026-09-30 |
| S102 | "13 · Wed 14 Oct" "Cancellation ships to production under change-management discipline" | #8-outline | cancellation | course site [syllabus site] fetched 2026-09-30 |
| S109 | "Required by 25 September:" "a version-controlled minimal OpenAPI contract (YAML or JSON) describing the deployed system's core booking flows: finding a space, creating a booking, and retrieving its confirmation or status, including the payment or subscription and lock access operations needed for that journey." | #9-supplementary-2-ects-component | OpenAPI (origin of Spacey's `openapi.yaml`) | course site [syllabus site] fetched 2026-09-30 |
| S111 | "Validate the document and have another person follow it against the deployed build; record the build commit, contract revision, validation result and observed requests and responses using synthetic data and no credentials." | #9-supplementary-2-ects-component | evidence pinned to a revision | course site [syllabus site] fetched 2026-09-30 |
| S112 | "Record unknown or unhandled cases honestly." | #9-supplementary-2-ects-component | open questions | course site [syllabus site] fetched 2026-09-30 |

The syllabus never names an `Access` context; the second context is "Payments" (plural). It gives no dates for team submissions ("Detailed briefs and exact submission arrangements will be issued separately."). It sets no rules on tool versions, repo layout, branch conventions or AI attribution.

## 5. Non-course texts the BRIEF quotes

| BRIEF § | Text | Finding | Evidence |
|---|---|---|---|
| 3.7 | "change the context to the existing 'Purchase' ... In the future can be extracted in the different context" | Found, with double quotes: "change the context to the existing \"Purchase\" and good to go" / "In the future can be extracted in the different context". Review state CHANGES_REQUESTED on `bb9f346`, applied in `d68631f`. Written from the course instructor's account, not a class reviewer's. | class PR #10 discussion |
| 4 | "Booking amount" / "Booking price" | Class record, not course text; see [rules-prs.md](rules-prs.md) K3 | class PR #4 diff at 9478b3e |

Spacey issue #173 (OPEN, created 2026-09-24, fetched 2026-10-01 with `gh issue view 173 -R cs403bkk-2026/spacey`), source of the D25 commission wording. Verbatim: "Spacey is a marketplace that lists spaces owned by others and earns a commission on bookings (e.g. 20% of each booking, like Booking.com's model)." Evidence type: `class issue #173 discussion` (added citation type for Spacey issues).

## Added 2026-10-01: journey site

| Statement (verbatim) | Topic | Evidence |
|---|---|---|
| "1 · EXISTING STATE" / "The application does everything" / "Payment state lives on booking. Access code is not saved." | Starting point | course site [journey site] fetched 2026-10-01 |
| "2 · PROPOSED, READY FOR SPLITTING" / "Each responsibility has an owner" | Target | course site [journey site] fetched 2026-10-01 |
| "Still one application. Ordinary function calls, explicit inputs/results, owned data access. Separate services and deployment cycles come next." | Target and next step | course site [journey site] fetched 2026-10-01 |
| "Collect agreed amount for booking reference" / "Payment reference and outcome" / "Authorised issuance request" / "Grant reference and code" | Calls in the target sequence | course site [journey site] fetched 2026-10-01 |
| "Each module owns its records. No reading another module's tables." | Data ownership | course site [journey site] fetched 2026-10-01 |
| "Ready means checked: ownership is enforced, migrations preserve known facts, and the existing journey plus failure/retry cases still work. Moving functions alone is not enough." | Definition of ready | course site [journey site] fetched 2026-10-01 |
| "Agree Access grant semantics before implementation: persistence alone does not prescribe code reuse, expiry or revocation." | Grant semantics | course site [journey site] fetched 2026-10-01 |
| "Failure and retry handling, including a recorded payment followed by a failed booking update, remain part of the contract and checks" | Failure cases | course site [journey site] fetched 2026-10-01 |
| "Purchase skips a new collection for already-paid or subscription-covered bookings." | Coverage | course site [journey site] fetched 2026-10-01 |
| "Frontend owns the screen. Backend owns the decisions." | Frontend boundary | course site [journey site] fetched 2026-10-01 |
| "Do not invent historical payments or old access codes." | Migration | course site [journey site] fetched 2026-10-01 |
