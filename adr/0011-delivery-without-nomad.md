# ADR-0011 Delivery without Nomad; rollback redeploys the previous tag

## Status

Accepted, 2026-10-01

## Context

Example: a PR to `cowork-booking-payment` runs pytest against a postgres:16 service, then `docker build`. Nothing is pushed or deployed. To roll Payment back from a bad release to v1.0.0, check out v1.0.0 in that repo and run `docker compose up -d --build`. Purchase and Access keep running.

- The seed's `.github/workflows/delivery.yml` (117 lines) tests every PR, then on each push to main builds and pushes an image to ghcr and runs `nomad job run deploy/startup-app.nomad.hcl`. The Nomad job pins one node, sets `auto_revert true` and passes no SECRET_KEY, so deploy runs with the public default key (seed flaw F10). Source inspected at 5a1cf3d.
- The new repos have no Nomad cluster, no registry credentials and no host.
- The course: "use version control, pull-request review, continuous delivery, and rollback as coordination and safety systems;" and the grading row "Service delivered, independently deployable" [syllabus site]. Team submissions include "a second-person rollback" [syllabus site].

## Decision

- Give each service repo one workflow, `.github/workflows/ci.yml`: pytest against postgres:16, then `docker build`. No registry push, no deploy step.
- Give the docs repo `docs.yml`: `scripts/check_docs.py` and the diagram renders.
- Deploy each service alone from its own `Dockerfile` and `compose.yaml`: app on 8001, 8002 or 8003 (container port 8000), its database on 5441, 5442 or 5443. Publish every port on 127.0.0.1 only (`"127.0.0.1:8001:8000"`, `"127.0.0.1:5441:5432"`): the DB port exists only so pytest on the host can reach it. Take POSTGRES_PASSWORD from env, never user=password.
- Build all three for e2e from the docs repo's `integration/compose.yaml`, from sibling folders.
- Release with a git tag (v1.0.0). Roll back by redeploying the previous tag with that repo's compose file.
- Delete `delivery.yml` and `deploy/` before the seed commit (ADR-0006).
- Read secrets from env at run time. Refuse to start without SECRET_KEY. Commit only `.env.example`, with every secret left empty so a copied example fails fast, and never set TEST_CLOCK_ENABLED in a Dockerfile, a service `compose.yaml` or `.env.example`.

## Consequences

- Good: every PR proves the tests pass and the image builds.
- Good: no cloud credentials in any repo; anyone can run a service with `docker compose`.
- Good: rollback steps fit in a README, so a second person can do it.
- Bad: no continuous deployment and no live URL.
- Bad: no automatic revert. The Nomad job's `auto_revert` is gone; rollback is manual.
- Bad: rollback rebuilds from source. `requirements.txt` pins direct packages only, so a rebuild may pull newer transitive packages.
- Bad: rollback redeploys code, not data. A schema change must stay readable by the previous tag, or the rollback needs a database restore.

## Alternatives considered

- **Keep ghcr and Nomad.** Rejected: no cluster, no registry secrets, and a push-and-deploy on every merge.
- **Push images to ghcr without deploying.** Gives immutable images to roll back to. Deferred: needs registry write access and cleanup.
- **Kubernetes.** Not in the pinned stack.
- **One compose file for all three as the deploy unit.** Rejected: the services would no longer deploy independently.

## Rules and decisions

- Rules: PUR-R03, PMT-R19, AXS-R18 (SECRET_KEY required); PUR-R38, PMT-R20, AXS-R19 (test clock flag never in an image); PMT-R01, AXS-R04 (tokens required at start).
- Decisions: D26, D27, D28.
- Related: ADR-0006, ADR-0013, ADR-0015.

## Sources

- Spacey main 5a1cf3d: `.github/workflows/delivery.yml`, `deploy/startup-app.nomad.hcl`, seed flaw F10 (source inspected at 5a1cf3d).
- inventory/spacey-tests-infra.md sections 5 and 6 (source inspected at 5a1cf3d).
- course site [syllabus site] fetched 2026-09-30: S23, S70, S76, S96.
- Project team (D26).
