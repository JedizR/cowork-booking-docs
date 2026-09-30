# ADR-0006 Seed three repos by copy-and-prune

## Status

Accepted, 2026-10-01

## Context

Example: the Payment repo starts as the seed app at 5a1cf3d, minus the files deleted before the seed. Its second commit removes bookings, spaces, members, the dashboard and the unlock route. It keeps `validate_card` and the card regexes, the fail-fast database connect, `/health`, `base.html`, `style.css`, the `money` filter and the query-string scrubbing, and adds `PROVENANCE.md` and `ci.yml`.

- Project rule: reuse the seed; do not start from scratch.
- The course takes a strangler path. [syllabus site]: "extract a monolith into independently deployable services using a strangler approach;" and day 4, "Extraction mechanics, strangler patterns, data ownership, and the shared database". [extraction site]: "Untangle before / you split." and "Separate the data and behaviour. Keep one application first." Its proposed step is labelled "Separate ownership, still one monolith", then "New tables + extracted operations + explicit contracts. Agree migration and compatibility before switching callers."
- Our situation differs: no production traffic, no live users, no data to keep. No booking data is migrated (PUR-Q07). The strangler's main benefit, keeping a live system working while callers switch, has nothing to protect here.

## Decision

Go straight to three repos by copy-and-prune from the seed revision 5a1cf3d. For each service:

1. Export the seed with `git archive`. Delete `STARTUP_LOG.md`, `LOAD_TEST.md`, `CONTRIBUTING.md`, `scripts/`, `deploy/` and `.github/workflows/delivery.yml` before anything is committed.
2. Replace persona names with Member A and Member B.
3. Commit `chore: seed from cs403bkk-2026/spacey@<full-sha>`.
4. Commit `refactor: prune to <service> context`, with `PROVENANCE.md` (every removed file, route and table; every seed flaw fixed or out of scope, citing a rule or ADR) and the new `ci.yml`.
5. Push only then, so no history ever holds `delivery.yml`.

Skip the "Separate ownership, still one monolith" step. The keep/delete plan is `inventory/keep-delete.md`.

| Step | Course strangler path | Our copy-and-prune |
|---|---|---|
| Start | One app; split its tables and operations inside it | Three copies of the app |
| Middle | "Separate ownership, still one monolith"; callers switch one at a time; old and new run side by side | None; each copy is pruned to one context at once |
| Data | Move rows out of shared tables; agree compatibility | A fresh database per service; nothing migrated |
| Risk it manages | Breaking a live journey | None live; the risks are dead code and drift |
| Safety evidence | Each step stays deployable | Seed tests kept per service, then new tests per rule |

## Consequences

- Good: three deployable repos in one step, each with the seed's tested parts: fail-fast connect, card validation, the btree_gist exclusion pattern, filters, one shared look.
- Good: `PROVENANCE.md` ties every kept line to 5a1cf3d, and no history holds personal names or the push-and-deploy pipeline.
- Bad: no git history from the seed; blame stops at the seed commit, which cites the SHA.
- Bad: three copies of shared code (`base.html`, `style.css`, the `money` filter, `clock.py`) can drift.
- Bad: we never practise the strangler's switch-over, which the course teaches. We say so plainly.
- Bad: pruning can leave dead code. A reviewer checks each `PROVENANCE.md` against `inventory/keep-delete.md`.

## Alternatives considered

- **The course's strangler path.** Right when live traffic and data must survive. Rejected here: nothing is live, and each step would be a monolith release we then throw away.
- **Rewrite from scratch.** Rejected: the project rule is reuse, and it loses tested code.
- **Fork with full history, then prune.** Rejected: the history holds personal names, `STARTUP_LOG.md` and a pipeline that pushes and deploys; rewriting it means rewriting history we did not create.
- **One repo with three service folders.** Rejected: the course asks for one independently deployable service per team.

## Rules and decisions

- Rules kept from the seed: PUR-R17 (`purchase.py` price), PUR-R22 (exclusion constraint), PMT-R08 (`validate_card`), PMT-R13 (log scrubbing), AXS-R05 (`issue_access_code`, rewritten to persist).
- Question: PUR-Q07.
- Decisions: D8, D26.
- Related: ADR-0001, ADR-0003, ADR-0011.

## Sources

- Spacey main 5a1cf3d, including bb39ee7 "extract booking price calculation into Purchase" (source inspected at 5a1cf3d).
- course site [extraction site] fetched 2026-09-30: E03, E04, E10, E13.
- course site [syllabus site] fetched 2026-09-30: S11, S22, S93.
- inventory/keep-delete.md (source inspected at 5a1cf3d).
