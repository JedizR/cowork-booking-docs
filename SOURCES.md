# Sources

Every external source this project uses. The class repos are read-only: we cloned them fresh into `${TMPDIR}/cowork-sources` (outside the mother folder) and only ran `git show/log/diff/archive`, `gh pr list/view/diff`, `gh issue view` and `gh api` GET against them.

- Fetch date for every source: **2026-09-30**.
- Re-check of the SHAs and PR heads below: 2026-10-01 (`git log` in the fresh clones and `gh pr list --state all`). Nothing had moved.
- People are named by role only (course instructor, class reviewer, class contributor, Member A/B, Operator, Staff).

## 1. Repositories and revisions

| Source | Location | Full SHA | Short | State | Used for | Evidence |
|---|---|---|---|---|---|---|
| Spacey main (seed revision) | https://github.com/cs403bkk-2026/spacey, clone `${TMPDIR}/cowork-sources/spacey` | `5a1cf3d90e538f431625cbb959987b7bdbe3c946` | `5a1cf3d` | `main` tip. Expected `5a1cf3d`: **unchanged**. Committed 2026-09-30T08:14:30Z. | Seed for all three service repos (copy-and-prune), routes, schema, helpers, tests, infra, flaws | source inspected at 5a1cf3d |
| Spacey commit bb39ee7 | same repo | `bb39ee724046ecebd5851b346f95a4ae27ec68b6` | `bb39ee7` | In `main` history (found by `git log origin/main`). Subject: "refactor: extract booking price calculation into Purchase". | Origin of `purchase.py` / `calculate_booking_price_cents` | source inspected at 5a1cf3d |
| Spacey evidence pin | same repo | `e734fc79bbb72341407f7decd7030fd47ea6a151` | `e734fc7` | Ancestor of `main` (found in `git log origin/main`). Committed 2026-09-27T15:26:56Z, "Merge pull request #177". | The revision every class rule cites. Line numbers in class rules refer to it. | source inspected at e734fc7 |
| Class rules main | https://github.com/cs403bkk-2026/spacey-business-rules, clone `${TMPDIR}/cowork-sources/spacey-business-rules` | `58a1477ac4ead3193f8083bf2838c8f461dbb4c9` | `58a1477` | `main` tip. Expected `58a1477`: **unchanged**. It is the PR #14 merge commit (2026-09-30T08:16:49Z). Holds only `README.md`, `GLOSSARY.md`, `RULES.md`. | Class glossary, rules, template; input for `ID_MAP.md` | source inspected at 58a1477 |
| Rules main: PR #1 merge | same repo | `1124404ff8ca0b977871b218ef7fb8bd28b5dff6` | `1124404` | On main. Base of PRs #3, #4 (merge-base), #10, #11, #12, #13, #15. | History | source inspected at 58a1477 |
| Rules main: PR #3 merge | same repo | `5d23e9fac0a7b05753216ab67c1c4e4fd9d6b030` | `5d23e9f` | On main | History | source inspected at 58a1477 |
| Rules main: direct push | same repo | `81e490e28d78fc1dbfcdf0d7f28e58cdda475125` | `81e490e` | On main, pushed without a PR: "Update RULES according to the template.md" | Explains template-field drift and the dropped Q-numbers | source inspected at 58a1477 |
| Rules main: seed commits | same repo | `bd1aa3107d9d899b605a951e70cd6d6485411599`, `fbdabd30f18556c436ed2acc2cc46c39a171569c`, `a200114a601fa9612a801822d366e5c1ec4b7901`, `a85379535c47e9d5f3e926e9551a2fc1f541650b` | `bd1aa31`, `fbdabd3`, `a200114`, `a853795` | On main. Course instructor's README, GLOSSARY, RULES and template. `a853795` is the merge-base of PRs #5-#9. | EX-T01, EX-T02, EX-R01, EX-R02, the rule template | source inspected at 58a1477 |

## 2. Class rules PRs

`gh pr list --state all` returns 14 PRs: #1 and #3-#15. **PR #2 does not exist**: there is no `origin/pr/2` ref, and `gh api repos/cs403bkk-2026/spacey-business-rules/issues/2` returns HTTP 404. PR heads are fetched as `origin/pr/<n>`. Every head below equals the `headRefOid` that GitHub reports.

| PR | Title | State | Head (full) | Head (short) | Created (UTC) | Merged (UTC) / merge commit | Used for | Evidence |
|---|---|---|---|---|---|---|---|---|
| #1 | Add payment glossary terms and rules | MERGED | `0326c8cedeb049ab67c2a9618747c502646b8a36` | `0326c8c` | 2026-09-29 13:26 | 2026-09-30 02:15:48 / `1124404` | PAY-T01..T04, PAY-R01..R03 | class PR #1 diff at 0326c8c |
| #3 | docs(glossary,rules): add Guest / Account-linked booking terms and EX-R04 | MERGED | `6752b24d4fa923ed9a7277250467cceb3d786252` | `6752b24` | 2026-09-29 13:52 | 2026-09-30 06:41:45 / `5d23e9f` | EX-T08, EX-T09, EX-R04 | class PR #3 diff at 6752b24 |
| #4 | Document booking prices, rounding and stored amounts | OPEN | `9478b3e9221650948d44eab228cf2291cebec54c` | `9478b3e` | 2026-09-29 14:21 | - | PRC-T01, PRC-T02 "Booking amount", PRC-R01, PRC-R02 | class PR #4 diff at 9478b3e |
| #5 | Add Space deletion constraint rule (EX-R05) | OPEN | `0712a1c3ae8c47b7b765e4c4fbc0a90bec222f2c` | `0712a1c` | 2026-09-29 16:02 | - | EX-R05 | class PR #5 diff at 0712a1c |
| #6 | Add SLOT glossary terms and rules: unpaid bookings hold slots; cancellation frees them | OPEN | `c18b6381d6c0e31a15b91806682890d9fb74f160` | `c18b638` | 2026-09-29 16:44 | - | SLOT-T01..T03, SLOT-R01, SLOT-R02 | class PR #6 diff at c18b638 |
| #7 | [Add] Add term counted member and count rules | OPEN | `05e90b3f8d45404d65c518e20159bc13c23954a8` | `05e90b3` | 2026-09-29 17:15 | - | MET-T01, MET-R01 | class PR #7 diff at 05e90b3 |
| #8 | Add dashboard metrics terms and rules | OPEN | `ce99d137cb42d948bb1672804c49c45f71eaa5c8` | `ce99d13` | 2026-09-29 17:24 | - | MET-T01, MET-T02, MET-R01, MET-R02 | class PR #8 diff at ce99d13 |
| #9 | Time Glossary and Rule | OPEN | `9afd71faae3f1b7a570ee1d27d1744cec2aa885b` | `9afd71f` | 2026-09-29 18:32 | - | TIM-T01, TIM-T02, TIM-R01 | class PR #9 diff at 9afd71f |
| #10 | Add account and login-session terms and rules | OPEN | `d68631f137de32fa3b574904f5a93659a146c76e` | `d68631f` | 2026-09-30 02:25 | - | ACC-T01, ACC-T02, ACC-R01, ACC-R02; Member-in-Purchase review | class PR #10 diff at d68631f |
| #11 | Add party size and capacity rule | OPEN | `7cf2656874afc49667e77eef5c6b40c7f90d7b5e` | `7cf2656` | 2026-09-30 05:34 | - | BOOK-T01, BOOK-T02, BOOK-R01 (rename of EX-R01) | class PR #11 diff at 7cf2656 |
| #12 | Access code is generated once and stored | OPEN | `1c8ce57c7c3bd2f73e2571fdd4047c5480bd2d9c` | `1c8ce57` | 2026-09-30 06:55 | - | PAY-R04 | class PR #12 diff at 1c8ce57 |
| #13 | Add space availability terms and rules | OPEN | `c8a302ff5947952838319795568acd31c2464b09` | `c8a302f` | 2026-09-30 07:58 | - | AVL-T01, AVL-T02, AVL-R01, AVL-R02 (first version) | class PR #13 diff at c8a302f |
| #14 | Clarify booking price and Purchase calculation ownership | MERGED | `25ca71e0379a30dfa64953e4de75a57027b4a726` | `25ca71e` | 2026-09-30 08:02 | 2026-09-30 08:16:49 / `58a1477` | PRC-T02 "Booking price", the stakeholder-clarified booking-price rule | class PR #14 diff at 25ca71e |
| #15 | Add availability search glossary terms and rules | OPEN | `9e4971ac9b17965ce5b1e4dd42efc6282a6666f8` | `9e4971a` | 2026-09-30 08:13 | - | AVL-T01, AVL-T02, AVL-R01, AVL-R02 (base for ID_MAP) | class PR #15 diff at 9e4971a |

All open PRs target `main`. Branch names are not recorded here, because some contain personal names.

## 3. Course sites

Fetched with `curl -sL` on 2026-09-30. Text shown only after a click was read from the page's inline script, not from a running browser.

| Site | URL | HTTP | Bytes | sha256 | Headers | Used for | Evidence |
|---|---|---|---|---|---|---|---|
| [extraction site] Extraction ("Untangle before you split") | https://cs403bkk-extraction.quick.prokopov.me/ | 200 | 14725 | `0be1c694c763a5f250f94bf14caa1b625edf30df26b2c3ad3fc99049ca02085d` | ETag `"510dbb078ecada0891476699906a9c9d"`, Last-Modified Wed, 30 Sep 2026 02:48:37 GMT | Course target: ownership, call flow, contracts, access-credential policy | course site [extraction site] fetched 2026-09-30 |
| [contexts site] Contexts ("One booking. Three models.") | https://cs403bkk-contexts.quick.prokopov.me/ | 200 | 9691 | `67f9899fe1cdef0e9d4ccef95b7f77e071b883f44b5301e57774f247a0adb3b8` | HEAD returns 405, so no ETag or Last-Modified | Shared references, re-pricing, revoke, "Integrations / Locks" | course site [contexts site] fetched 2026-09-30 |
| [syllabus site] Syllabus | https://cs403bkk.quick.prokopov.me/ | 200 | 19461 | `e3286484fa8088ab7f520a645249f3f888f4d50939e23bf3746f29b881e32307` | ETag `65436f1b3949aacf3b8d00b75f5773c6`, Last-Modified Mon, 14 Sep 2026 12:17:29 GMT | Teams, REST, artefacts, grading, cancellation, three services vs monolith | course site [syllabus site] fetched 2026-09-30 |

Links between the sites: the extraction page links to the contexts page and to the class rules `RULES.md`. The contexts page links to neither of the others. No root page links to the syllabus (deeper pages were not crawled).

## 4. Other class records cited

| Record | Where | State | Used for | Evidence |
|---|---|---|---|---|
| Spacey issue #82, as linked by a class reviewer on rules PR #6 | `gh api repos/cs403bkk-2026/spacey-business-rules/pulls/6/reviews` (review 5362641240) | Review APPROVED; PR #6 OPEN | Cancel hard-delete flaw (spacey-flaws.md F5). Review text: "We have an open issue for this (#82 - \"Cancelling a paid booking should leave a record\"). Maybe link it so it stays visible?" | class PR #6 discussion |
| Spacey PR #196 "Extract booking price calculation into Purchase" | cited in rules PR #14 body | merged 2026-09-30 08:14 UTC as `5a1cf3d` | Where `purchase.py` came from | class PR #14 discussion |

Spacey issue #173 (OPEN, created 2026-09-24, fetched 2026-10-01 with `gh issue view 173 -R cs403bkk-2026/spacey`), source of the D25 commission wording. Verbatim: "Spacey is a marketplace that lists spaces owned by others and earns a commission on bookings (e.g. 20% of each booking, like Booking.com's model)." Evidence type: `class issue #173 discussion` (added citation type for Spacey issues).

## 5. Local runs done in M0

| Run | Revision | Environment | Result | Evidence |
|---|---|---|---|---|
| Spacey pytest suite | 5a1cf3d (`git archive` export, not the clone) | Python 3.12.11 (uv venv), throwaway `postgres:16` container (server 16.14), removed after the run | 160 passed, exit 0 (output in `inventory/spacey-tests-infra.md`) | test run at 5a1cf3d |
| Spacey pytest suite, per-test (`pytest -rA`) | 5a1cf3d (fresh `git archive` export) | Python 3.12.11 (uv venv), new throwaway `postgres:16` container (server 16.14), removed after the run; 2026-09-30 17:39 UTC | 160 `PASSED` lines, "160 passed in 12.93s", exit 0 (log `inventory/spacey-pytest-rA-5a1cf3d.log`; named-test lines in `inventory/spacey-tests-infra.md` section 1) | test run at 5a1cf3d |
| `amount_for` arithmetic on the three PR #14 examples | e734fc7 (function read with `git show`) | stdlib Python, no DB | 750, 333, 1 (output in `inventory/rules-prs.md`) | test run at e734fc7 |
| `parse_time` / `parse_window` on the six PR #15 AVL-R02 rows | e734fc7 (functions copied into a scratch script) | Python 3.11.7, no DB, no HTTP | all six rows reproduce (output in `inventory/rules-prs.md`) | test run at e734fc7 |

No live journey was driven in M0. Nothing in the inventory is tagged "live journey verified".

## 6. Evidence-type legend

Every inventory row carries exactly one of these tags. They are never interchangeable.

| Tag | Meaning |
|---|---|
| `source inspected at <short-sha>` | We read the code or text at that revision. Nothing was executed. |
| `test run at <short-sha>` | We executed tests or code from that revision. The output is shown next to the claim. |
| `live journey verified` | We drove a running app. (Not used in M0.) |
| `class PR #n diff at <head-short-sha>` | The text of a class rules PR at its head. It says what the PR claims, not what is true. |
| `class PR #n discussion` | Reviews, inline comments or the body of a class rules PR. Run results claimed there are the PR author's or reviewer's, not ours. |
| `course site [label] fetched 2026-09-30` | Verbatim text of a course page on that date; labels map to the URLs in the course-sites table above. |
| `class issue #n discussion` | Text of a Spacey GitHub issue (only #173). |

Policy status is separate from evidence. Everything in `inventory/` is either Observed Spacey behaviour, class-record text or course guidance. None of it is project policy until M1 decides it.
