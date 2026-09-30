# Inventory (M0)

What exists before we design anything: the Spacey code at `5a1cf3d`, the class rules record at `58a1477` plus its open PRs, and the three course sites. Revisions and fetch dates are in [`../SOURCES.md`](../SOURCES.md).

Everything here is **input**, not policy. Spacey behaviour is Observed. Class-rule text is what a PR says. Course text is guidance. M1 turns the parts we adopt into `GLOSSARY.md`, `RULES.md`, `ID_MAP.md` and `DECISIONS.md`.

## Files

| File | What it covers |
|---|---|
| [spacey-routes.md](spacey-routes.md) | All 27 Spacey routes (plus Flask's static route): method, path, auth, ownership, template/JSON, status codes, line |
| [spacey-schema.md](spacey-schema.md) | All 4 tables, every column and constraint, the EXCLUDE constraint, DDL order, startup behaviour |
| [spacey-app.md](spacey-app.md) | Config and env vars, DB connection, time handling, every helper, filters, metrics, templates, CSS; BRIEF section 4 Spacey facts checked |
| [spacey-tests-infra.md](spacey-tests-infra.md) | The two Python 3.12 test runs (160 passed each, exact output; per-test `PASSED` lines), tests by area, Docker, compose, gunicorn, CI, Nomad, requirements |
| [spacey-pytest-rA-5a1cf3d.log](spacey-pytest-rA-5a1cf3d.log) | Raw output of the second (`pytest -rA`) run: one `PASSED` line per test |
| [spacey-flaws.md](spacey-flaws.md) | Every BRIEF section 4 flaw with file:line evidence (Disposition "to decide in M1"), plus 15 more |
| [rules-prs.md](rules-prs.md) | Every class rules PR (#1, #3-#15): state, head, IDs defined and referenced, review points by role, known conflicts, other conflicts, the rule template |
| [class-ids.md](class-ids.md) | One table of every class term, rule and question ID found anywhere, sorted by ID. Input for `ID_MAP.md` |
| [course-statements.md](course-statements.md) | Every course statement we rely on, verbatim, and a found/not-found check of each quote in BRIEF sections 2, 3, 4 and 7 |
| [keep-delete.md](keep-delete.md) | Every Spacey file, route, table and helper, with a Purchase / Payment / Access / Delete decision per BRIEF section 10 |

## Evidence types

Every inventory row carries exactly one tag. (Legend and index tables like this one carry none.)

| Tag | Meaning | Source |
|---|---|---|
| `source inspected at <short-sha>` | Code or text read at that revision; nothing executed | BRIEF section 14 |
| `test run at <short-sha>` | Tests or code executed at that revision; output shown beside the claim | BRIEF section 14 |
| `live journey verified` | A running app was driven (not used in M0) | BRIEF section 14 |
| `class PR #n diff at <head-short-sha>` | Text of a class rules PR at its head. What the PR claims, not what is true | citation type |
| `class PR #n discussion` | Reviews, inline comments or body of a class PR. Runs claimed there are theirs, not ours | citation type |
| `course site [label] fetched 2026-09-30` | Verbatim course-page text on that date. Labels `[extraction site]`, `[contexts site]`, `[syllabus site]` map to URLs in `../SOURCES.md` | citation type |
| `class issue #n discussion` | Text of a Spacey GitHub issue (only #173, the D25 commission wording) | citation type |

BRIEF section 14 names the first three evidence kinds. We add the PR and course-site citation types because the class record and the course are text, not code. Spacey issue #82 is quoted through the class PR that cites it (`class PR #6 discussion`); issue #173 carries the issue tag.

## Policy status (BRIEF section 14)

Status is not evidence. Inventory rows describe inputs, so they carry no project status yet. M1 gives each adopted rule one of these four.

| Status | Meaning |
|---|---|
| `Observed` | Spacey behaviour, intent unresolved |
| `Decided` | Project decision (D# or ADR-#) |
| `Stakeholder-clarified` | Scoped, with source |
| `Superseded` | Replaced; links to the replacement |

The class record uses its own labels ("observed", "proposed", "stakeholder-clarified", "superseded"). They are quoted as written and mapped in M1.

## Conventions

- People are roles: "course instructor", "class reviewer", "class contributor", Member A / B / C, Operator, Staff. Square brackets in a quote, e.g. `[role]`, mark a replaced name. Branch names are not quoted.
- Course sites are cited by label (`[extraction site]`, `[contexts site]`, `[syllabus site]`). The full URLs appear once, in `../SOURCES.md`, because their hostnames contain a person's name.
- Member C / c@example.com is an added anonymised role, used only where Spacey tests or the class record need a third distinct member.
- The names scan runs from the mother folder over every repo (not committed: the list itself holds names).
- Line numbers: `app.py:NNN` means Spacey `5a1cf3d` unless the row says `e734fc7`. Class rules cite `e734fc7` lines, which differ by a few lines (for example `parse_time` is L141 at `e734fc7` and L143 at `5a1cf3d`; `issue_access_code` is L976 and L970), because `amount_for` moved to `purchase.py`.
- Money in Spacey is cents and "$". Our docs will use THB and satang (D1). Examples quoted from the class keep their original units.

## M0 gate coverage

| Gate item (BRIEF section 8) | Where | Evidence type used |
|---|---|---|
| Every PR (#1, #3-#15) | rules-prs.md sections 1 and 3-16; SOURCES.md section 2 | class PR #n diff at head (per row) |
| Every Spacey route | spacey-routes.md (27 + static) | source inspected at 5a1cf3d |
| Every Spacey table | spacey-schema.md (4 tables + EXCLUDE + extension) | source inspected at 5a1cf3d |
| Every course statement relied on | course-statements.md | course site <url> fetched 2026-09-30 (per row) |
| keep-delete per section 10 | keep-delete.md | source inspected at 5a1cf3d |
| Spacey suite re-run on 3.12 | spacey-tests-infra.md section 1 | test run at 5a1cf3d |
