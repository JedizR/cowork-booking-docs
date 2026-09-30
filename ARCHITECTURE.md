# Cowork Booking architecture

Three services, three repos, three databases. Only Purchase calls the other two. This page says what runs where, who owns which data, how the services talk, and how they stay consistent without a shared transaction. Rules are in RULES.md, decisions D1-D28 in DECISIONS.md, and the reasons behind each structural choice in `adr/` (ADR-0001 to ADR-0020).

## Overview

![Context map](diagrams/context-map.svg)

Example: at 2026-10-05 10:00 Member A books Meeting Room A for 2026-10-07 09:00-10:30. Purchase prices it at THB 450.00 and holds the slot as BK-7KQ2M9. Payment collects THB 450.00 on its hosted page. Purchase reads the outcome, confirms the booking and asks Access for a grant. Access issues ticket code H7K3-9QXA, which Staff scan at the kiosk on the day.

- **Purchase** "Owns price and coverage" [extraction site]: members, spaces, availability, bookings, cancellation, the dashboard (PUR-T33).
- **Payment** "Owns payment outcomes" [extraction site]: payment sessions, the hosted mock checkout, attempts, refunds (PMT-T01).
- **Access** "Owns grants and issuance" [extraction site]: grants, ticket codes, the e-ticket, the check-in kiosk (AXS-T01).

"Shared references connect the models. They do not make them one shared object." [contexts site]. The split is the course exercise: "Three services are the course exercise, not a claim that every growing business should split its application; students compare the costs and benefits with alternative boundaries and modules within a monolith." [syllabus site]. ADR-0001 records the split and compares it with modules in one monolith. Account data lives on Member in Purchase; there is no Identity service (ADR-0002).

## Services and repos

| Service | Repo | Owns | Port | Image | Database |
|---|---|---|---|---|---|
| Purchase | cowork-booking-purchase | members, spaces, availability grid, bookings, price, coverage, cancellation, dashboard | 8001 | `cowork-booking-purchase:v1.0.0` | own postgres:16, database `purchase` |
| Payment | cowork-booking-payment | payment sessions, hosted checkout, attempts, refunds, operator money page | 8002 | `cowork-booking-payment:v1.0.0` | own postgres:16, database `payment` |
| Access | cowork-booking-access | grants, ticket codes, e-ticket, check-in kiosk, scan log | 8003 | `cowork-booking-access:v1.0.0` | own postgres:16, database `access` |
| Docs | cowork-booking-docs | rules, decisions, PRD, architecture, ADRs, diagrams, contracts index, integration stack | none | none | none |

- Every app container listens on 8000; compose maps it to 8001, 8002 or 8003.
- Each service repo is seeded by copy-and-prune from the seed at 5a1cf3d, straight to three repos (ADR-0006).
- Each contract has one authoritative copy beside its provider's code: Payment holds purchase-payment, Access holds purchase-access, Purchase holds its own `openapi.yaml`. The docs repo keeps links only (ADR-0005).

## Containers and deployment

![Containers](diagrams/containers.svg)

Run each service alone from its own repo, or all three from the docs repo:

- **Per repo** `compose.yaml`: `app` (build `.`, port 8001, 8002 or 8003) and `db` (postgres:16, `pg_isready` healthcheck, named volume). Only this file publishes a DB port (5441, 5442 or 5443), so pytest on the host can reach it. Calls to a service that is not running follow the failure rules below.
- **Integration** `cowork-booking-docs/integration/compose.yaml`: builds the three services from the sibling folders, each with its own postgres:16. No DB port is published. `compose.e2e.yaml` adds only `TEST_CLOCK_ENABLED=true` (D27).

```yaml
# integration/compose.yaml (one of three pairs)
services:
  purchase-db:
    image: postgres:16
    environment: {POSTGRES_USER: purchase, POSTGRES_PASSWORD: purchase, POSTGRES_DB: purchase}
    healthcheck: {test: ["CMD-SHELL", "pg_isready -U purchase"], interval: 2s, retries: 30}
  purchase:
    build: ../../cowork-booking-purchase
    ports: ["8001:8000"]
    env_file: .env
    environment:
      DATABASE_URL: postgresql://purchase:purchase@purchase-db:5432/purchase
      PUBLIC_URL: http://localhost:8001
      PAYMENT_INTERNAL_URL: http://payment:8000
      PAYMENT_PUBLIC_URL: http://localhost:8002
      ACCESS_INTERNAL_URL: http://access:8000
      ACCESS_PUBLIC_URL: http://localhost:8003
    depends_on: {purchase-db: {condition: service_healthy}}
```

```bash
# from the mother folder; frees ports 8001-8003
for s in purchase payment access; do (cd cowork-booking-$s && docker compose down); done
cd cowork-booking-docs/integration && docker compose -f compose.yaml -f compose.e2e.yaml up -d --build --wait
```

- Server-to-server calls use the internal URL (`http://payment:8000`); the browser uses the public one (`http://localhost:8002/pay/ps_...`).
- Browsers share cookies across ports on one host, so each service has its own cookie name (D15).
- The apps do not wait for each other: Purchase calls Payment and Access only when a request needs them.

## Data ownership

![Data model](diagrams/data-model.svg)

A service reads and writes only its own database (ADR-0003; PUR-R35, PMT-R18, AXS-R04). Foreign keys exist only inside one database. A value from another service is a plain column, never a foreign key. Column names below are a guide for M5; the contracts pin only the JSON field names.

| Service | Table | Main columns |
|---|---|---|
| Purchase | members | id, email (unique, lower-cased), display_name, password_hash, is_operator, plan_active |
| Purchase | spaces | id, name, capacity, hourly_rate_satang (BIGINT), archived_at |
| Purchase | bookings | reference (unique, BK-), member_id, space_id, start_time, end_time, blocks, party_size, note, agreed_price_satang (BIGINT), coverage, status, hold_expires_at, payment_session_id, payment_outcome, cancel_reason, refund_amount_satang, refund_reason, refund_status, refund_attempt, grant_id, grant_status, ticket_url (PUR-T17, PUR-T34). The booking JSON field `payment_status` is this `payment_outcome` (not_required, unpaid, paid); it is not Payment's own payment_status (PMT-T04), which has no not_required |
| Payment | payment_sessions | id (ps_), booking_reference (unique), amount_satang (BIGINT), currency, description, success_url, cancel_url, expires_at, status, payment_status |
| Payment | payment_attempts | id (pa_), session_id, card_brand, card_last4, outcome, decline_code (PMT-R13) |
| Payment | refunds | id (re_), payment_session_id, booking_reference, amount_satang, reason, attempt, status; unique (payment_session_id, attempt) (PMT-R14) |
| Access | grants | id (gr_), booking_reference (unique), member_ref, space_id, space_name, valid_from, valid_until, ticket_code (unique), ticket_token (unique), status, revoked_at (timestamptz, null until the first revoke; a repeat revoke keeps it); a tombstone has no code, token or space (AXS-T07) |
| Access | scans | id, scanned_at, space_id (selected room), input (normalised), result, grant_id (AXS-R15) |
| All three | test_clock | one row: the override instant or null (D27) |

Purchase also keeps the seed's race guard, now partial, so expired and cancelled rows never block (PUR-R22):

```sql
ALTER TABLE bookings ADD CONSTRAINT bookings_no_overlap
  EXCLUDE USING gist (space_id WITH =, tstzrange(start_time, end_time) WITH &&)
  WHERE (status IN ('held', 'confirmed'));
```

Cross-service references (values only):

| Value | Minted by | Stored by | Used for |
|---|---|---|---|
| booking_reference BK-7KQ2M9 | Purchase (PUR-R29) | Payment sessions and refunds, Access grants | natural key for session create, grant and revoke |
| payment_session_id ps_... | Payment | Purchase bookings | reconcile, expire, refund |
| amount_satang 45000 | Purchase (agreed price, PUR-R17) | Payment sessions | collected as given, never re-priced (PMT-R04) |
| grant_id gr_..., ticket_url | Access | Purchase bookings | "View e-ticket" link |
| member_ref, space_id, space_name, valid_from, valid_until | Purchase | Access grants, copies as sent | e-ticket, kiosk room list, window check (AXS-R03) |

Payment never receives an email or a name: the description holds the space and the Bangkok time only (PUR-R23). Access stores member_ref as an opaque value and never shows it (AXS-T18).

## Service-to-service calls

Only Purchase calls. Payment and Access call no one: no webhooks, no callbacks (ADR-0004; PUR-R35, PMT-R18, AXS-R04). The Member's browser moves between services by redirect.

```python
# payment_client.py in Purchase; access_client.py is the same shape
r = requests.get(f"{PAYMENT_INTERNAL_URL}/payment-sessions/{session_id}",
                 headers={"Authorization": f"Bearer {PAYMENT_API_TOKEN}"}, timeout=5)
```

Every call follows the same three steps:

1. Commit what Purchase has decided, if anything (for example: held, or cancelled with its refund amount).
2. Make the HTTP call with no transaction open, `timeout=5`. A timeout, a connection error or a 5xx answer means "unreachable" (PUR-R35), the same definition as in the three contracts.
3. In a new short transaction, lock the booking row (`SELECT ... FOR UPDATE`), check it is still in the state the call assumed, and store the answer. If another worker got there first, drop the answer.

| Call | Purchase sends it when | On an answer | On no answer |
|---|---|---|---|
| POST /payment-sessions | right after the held insert commits (PUR-R23) | 201, or 200 for a repeat: store payment_session_id, 303 the browser to `url` | the booking stays held without a session; flash "Payment is not reachable. Please try again." or JSON 503; "Continue to payment" repeats the call (PUR-Q09). A 400 or 409 is a Purchase defect, not "unreachable" |
| GET /payment-sessions/{id} | at every reconcile point: booking page, return URL, My bookings, cancel, pre-insert sweep, the Operator's Reconcile (PUR-R24) | paid: fulfil (PUR-R25); unpaid after the hold: expired; unpaid inside the hold: no change | no change; the page says "Payment status unknown, refresh later"; a conflicting insert gets 503 or a flashed "try again" (D13) |
| POST /payment-sessions/{id}/expire | the Member or Operator cancels a held booking (PUR-R31) | unpaid: cancelled, or expired if the hold had lapsed; paid: confirm without a grant, then cancel as confirmed | the cancel is refused with 503 or a flashed "try again"; nothing changes |
| POST /refunds | cancel step 3, after the revoke succeeded (PUR-R32); the full refunds amount_mismatch and slot_unavailable (PUR-R25) | store succeeded or failed with refund_attempt; after failed, only the Operator's Retry sends attempt+1 (PUR-R33) | refund_status pending, "refund pending"; the retry sends the same attempt, so a lost answer never pays twice (PMT-R14) |
| POST /grants | the booking becomes confirmed, and only while it stays confirmed with no cancel in progress (PUR-R26) | store grant_id, ticket_url, grant_status issued | grant_status pending, ticket "being prepared"; retried on the booking page or by the Operator's Retry (D20) |
| POST /grants/{booking_reference}/revoke | cancel step 2 (PUR-R32) | grant_status revoked; an unknown reference becomes a revoked tombstone (AXS-R02) | grant_status revoke_pending, "revocation pending"; the refund waits (PUR-Q10); the retry revokes first |

- Purchase never calls GET /grants in v1 (PUR-R26).
- Every JSON error in all three services is `{"error": {"code": "...", "message": "..."}}`. RULES.md rows quote only the message: `{"error": "Slot just taken"}` means `{"error": {"code": "slot_taken", "message": "Slot just taken"}}`. Only `GET /health` keeps the seed shape.
- Retries are safe because every write has a natural key: booking_reference for a session, a grant and a revoke; (payment_session_id, attempt) for a refund (ADR-0014; PMT-R03, PMT-R14, AXS-R01, AXS-R17).
- Consumer tests stub the provider at one module, `payment_client.py` or `access_client.py`, using the contract examples.

## Consistency and reconciliation

There is no distributed transaction. Each service commits its own facts. Purchase pulls the answers it needs and moves its booking toward the outcome they decide: "Purchase interprets the result" [extraction site].

- **Hold (D11).** A booking is slot-blocking when it is confirmed, or held with `hold_expires_at > :now`, where `:now` is `clock.now()` passed as a parameter (PUR-R12). A lapsed hold stays `held` in the table until something touches it, so the pre-insert sweep reconciles the space's stale holds before the insert, and the partial EXCLUDE catches the rest (PUR-R22). One held booking per Member (PUR-R39). From 10:13 to 10:15 the hold can no longer be paid, but still blocks (PUR-R40).
- **Session expiry (D12).** `expires_at = hold_expires_at - 2 min` (10:15 hold, 10:13 session). Payment refuses attempts from expires_at on (PMT-R11), so its answer is final before the hold ends. That is why a lost redirect needs no webhook (ADR-0004).
- **Reconciliation (D13).** Lazy, on touch, with no background job (ADR-0007; PUR-R24). A GET may run this sync because it only moves a booking toward an outcome already decided (PUR-R37).
- **Fulfilment (D14).** Confirm only when the session's booking_reference, amount_satang and currency equal the booking's (PUR-R25).
- **Cancel (D18, D19).** A held cancel expires the session first, so pay and cancel cannot both win (PMT-R06). A confirmed cancel runs three stored steps: commit, revoke, refund (PUR-R32).
- **Issuance (D20).** Grant on confirmation; a failure leaves the booking confirmed with a ticket "being prepared".

Invariant: every paid session ends as a confirmed booking or a refund attempt (D13).

| A paid session meets | Purchase does | Ends as |
|---|---|---|
| a held booking with the same reference, amount and currency | confirm, then POST /grants | confirmed booking |
| a held booking with a different amount or currency | cancelled with amount_mismatch and a full refund, sent after commit | refund attempt |
| a booking already expired | full refund with slot_unavailable | refund attempt |
| a held cancel whose expire answers paid | confirm without a grant, then cancel as confirmed (PUR-R30) | confirmed booking, then cancelled with the policy refund |

A held booking that nobody touches stays held until the Operator's Reconcile or the next sweep of its space closes it (the D13 trade-off).

Flows:

- Book and pay: held, session, hosted page, return, confirm, grant. ![Book and pay](diagrams/seq-book-pay.svg)
- Decline and retry: the session stays open; the Member retries on the same page (PMT-R10). ![Decline and retry](diagrams/seq-decline-retry.svg)
- Lost redirect: the next touch finds paid and confirms, even after the hold lapsed. ![Lost redirect](diagrams/seq-lost-redirect.svg)
- Hold expiry: unpaid after 10:15 becomes expired; the slot is free. ![Hold expiry](diagrams/seq-hold-expiry.svg)
- Coverage skips collection: plan and free bookings confirm at once, with no Payment call (PUR-R20). ![Coverage](diagrams/seq-coverage.svg)
- Cancel a held booking: expire first (PUR-R31). ![Cancel held](diagrams/seq-cancel-held.svg)
- Cancel a confirmed booking: commit, revoke, refund (PUR-R32). ![Cancel confirmed](diagrams/seq-cancel-confirmed.svg)
- Refund failure and the Operator's attempt 2 (PUR-R33, PMT-R16). ![Refund retry](diagrams/seq-refund-retry.svg)
- Check-in: code, room, window, revocation (AXS-R13, AXS-R14). ok shows "Door unlocked (mock)": the lock is mocked, and "Payment success ≠ access provisioned ≠ a successful door opening." [contexts site] (ADR-0017). ![Check-in](diagrams/seq-checkin.svg)

## States

![States](diagrams/states.svg)

| Context | Record | Stored states | Derived, never stored |
|---|---|---|---|
| Purchase | Booking | held to confirmed, expired or cancelled; confirmed to cancelled (PUR-R28) | Completed (confirmed, end passed) |
| Purchase | Follow-up fields | grant_status not_requested, pending, issued, revoke_pending or revoked; payment_outcome not_required, unpaid or paid; refund_status none, pending, succeeded or failed (PUR-T34) | none |
| Payment | Session | open to complete or expired; payment_status unpaid or paid (PMT-R05) | none |
| Payment | Attempt, Refund | attempt succeeded or declined(code); refund succeeded or failed (PMT-R16) | "needs manual follow-up" (PMT-T15) |
| Access | Grant | issued to checked_in; revoked from either (AXS-R16) | not_yet_valid, expired, no_show |

## Security

| Topic | What we do | Source |
|---|---|---|
| Login session | Signed `purchase_session` cookie, 12 h from login whatever the activity. Logout clears it in that browser; a copied cookie still works until the 12 h end (accepted) | PUR-R03, D15, ADR-0016 |
| Cookies | `purchase_session`, `payment_session`, `access_session`: HttpOnly and SameSite=Lax; Secure when PUBLIC_URL starts with https | PUR-R03, PMT-R19, AXS-R18 |
| CSRF | SameSite=Lax instead of tokens. Every state change is a POST; a GET runs only the idempotent sync | PUR-R37, ADR-0009 |
| SECRET_KEY | Required in all three. Unset or empty: the process exits at start | PUR-R03, PMT-R19, AXS-R18 |
| Service tokens | `Authorization: Bearer` with PAYMENT_API_TOKEN or ACCESS_API_TOKEN. Missing, wrong or another scheme: 401 before any validation or lookup. Payment and Access refuse to start without their token. Compare with `hmac.compare_digest` | PMT-R01, AXS-R04, ADR-0019 |
| HTTP Basic | Payment GET /operator checks OPERATOR_PASSWORD; the Access kiosk checks STAFF_PASSWORD; constant-time compare; only the password is checked (the e2e suite sends user operator or staff) | PMT-R17, AXS-R11, ADR-0019 |
| Ownership | Booking pages and actions for the owner or an operator, else 404; anonymous callers get the login step or 401 before any lookup. Operator pages 404 to non-operators | PUR-R05, PUR-R06, D17 |
| Card data | Store only brand and last4. Never store, log, flash or put in a URL the number, expiry or CVC; the card form posts in the body | PMT-R13, ADR-0020, ADR-0018 |
| Hosted page | GET /pay/{id} needs no login; the 128-bit random session id is the link | PMT-R07, PMT-Q05 |
| Ticket link | `/t/<ticket_token>`, 128-bit, view-only, no email; `Referrer-Policy: no-referrer`. Whoever holds the link holds entry for the window | AXS-R09, ADR-0008 |
| Messages | Flask `flash()` only; never render text from `?error=`, `?message=` or `?code=` | PUR-R36, PMT-R10, AXS-R14, D28 |
| Access log | gunicorn logs the path without the query string and without the referer (kept from the seed), so `?session_id=` never reaches the log; the `/t/` path is logged (accepted) | PMT-R13, AXS-R09 |
| Accepted trade-offs | Logout replay inside 12 h, registration enumeration, bearer ticket link, HTTP Basic, mock card data | D16, ADR-0016 |

## Time and the test clock

- **One fixed offset (D2).** Bangkok is UTC+7 with no daylight saving, so a fixed `timezone(timedelta(hours=7))` is exact and needs no tzdata (ADR-0012). Store timestamptz. JSON needs an offset: `"2026-10-07T09:00:00+07:00"` is accepted, `"2026-10-07T09:00:00"` gets 400. The form sends a date and a block; the server builds the instant (PUR-R07, PMT-R02, AXS-R03).
- **One clock (D27).** Every service reads time only through `clock.now()`. SQL gets it as a parameter, never `now()` or `CURRENT_TIMESTAMP` in business logic; `created_at` defaults are fine (ADR-0013; PUR-R38, PMT-R20, AXS-R19).
- **Test override.** With `TEST_CLOCK_ENABLED=true` (only in `compose.e2e.yaml`), `POST /_test/clock` stores an instant in the one-row `test_clock` table; `null` clears it. Otherwise the route answers 404. The e2e suite sets the same instant on all three services:

```bash
for p in 8001 8002 8003; do
  curl -s -X POST localhost:$p/_test/clock -H 'Content-Type: application/json' -d '{"now": "2026-10-05T10:15:00+07:00"}'
done   # Member A's unpaid hold on BK-7KQ2M9 has now lapsed on every service
```

## Runtime

| Part | Version | Where | Note |
|---|---|---|---|
| Python | 3.12 | all | `python:3.12-slim` image |
| Flask with Jinja | 3.1.2 | all | server-rendered pages and JSON |
| gunicorn | 23.0.0 | all | `workers = 2` in `gunicorn.conf.py`; no `preload_app`, so each worker opens its own connection (ADR-0015) |
| psycopg[binary] | 3.2.13 | all | one connection per worker; explicit transactions for booking, fulfilment, pay and refund (D28) |
| PostgreSQL | 16 | one per service | btree_gist for the Purchase EXCLUDE |
| requests | 2.32.3 | Purchase calls | `timeout=5` on every call |
| segno | pinned in M5 | Access only | QR as inline SVG; pure Python; the only new runtime dependency (ADR-0010) |
| pytest | 8.4.2 | tooling | per-service CI and the e2e suite |

```python
# gunicorn.conf.py (all three)
workers = 2  # ponytail: 2 workers x 1 DB connection is the ceiling; psycopg_pool is the upgrade path
accesslog = "-"  # access_log_format uses %(U)s: path only, no query string, no referer
```

- Each service keeps from the seed: `/health` with `revision` (503 when the DB is down), the fail-fast DB connect, the query-string scrubbing, `base.html` with `style.css`, and the `money` and `local_time` filters in THB.
- Tables are created at start with `CREATE ... IF NOT EXISTS`; there is no migration tool in v1.
- Not used: an ORM, an SPA framework, a message broker, Kubernetes, a service mesh or an API gateway. The browser reaches each service on its own port.

## Delivery and rollback

Each service is delivered on its own (D26, ADR-0011). The course grades "Service delivered, independently deployable" and asks teams to "use version control, pull-request review, continuous delivery, and rollback as coordination and safety systems;" [syllabus site].

- **CI per service** (`.github/workflows/ci.yml`): pytest against a postgres:16 service container, then `docker build`. No registry push, no deploy.
- **Docs CI** (`.github/workflows/docs.yml`): `python3 scripts/check_docs.py`, then renders every `diagrams/*.mmd` with mermaid-cli.
- **Deploy**: `git checkout v1.0.0 && docker compose up -d --build` in that service's repo. The DB volume stays.
- **Rollback**: redeploy the previous tag the same way. Keep schema changes additive (new tables, new nullable columns), so the previous tag still starts on the newer schema.
- **Contract changes**: tag the provider `contract-v1`, `contract-v2`; keep a change backward compatible and deploy the provider before the consumer.
- **Removed**: the seed's pipeline pushed to a registry and deployed to Nomad on every push to main (Spacey: source inspected at 5a1cf3d, `.github/workflows/delivery.yml`, `deploy/startup-app.nomad.hcl`). Both are deleted before the seed commit. There is no auto-revert; rollback is a manual redeploy.

## Environment variables

Commit only `.env.example` files. Never set `TEST_CLOCK_ENABLED` in a Dockerfile or `.env.example`.

| All services | Example (integration stack) | Purpose |
|---|---|---|
| DATABASE_URL | `postgresql://purchase:purchase@purchase-db:5432/purchase` | own database only; fail fast when unreachable |
| SECRET_KEY | a long random string | required; signs the cookie and flashes |
| APP_REVISION | the git SHA | shown by GET /health |
| PUBLIC_URL | `http://localhost:8001` | the service's browser-facing base URL; Secure cookie when https; each service builds its own links from it (Purchase success_url and cancel_url, the Payment hosted-page url, the Access ticket_url) |
| TEST_CLOCK_ENABLED | `true` in `compose.e2e.yaml` only | enables POST /_test/clock |

| Purchase | Example | Purpose |
|---|---|---|
| PAYMENT_INTERNAL_URL | `http://payment:8000` | server-to-server calls to Payment |
| PAYMENT_PUBLIC_URL | `http://localhost:8002` | browser links to Payment pages |
| PAYMENT_API_TOKEN | shared secret | bearer token on every Payment call |
| ACCESS_INTERNAL_URL | `http://access:8000` | server-to-server calls to Access |
| ACCESS_PUBLIC_URL | `http://localhost:8003` | browser links to Access pages |
| ACCESS_API_TOKEN | shared secret | bearer token on every Access call |
| OPERATOR_EMAIL | `operator@example.com` | the Member with this email becomes the Operator (PUR-R04) |

| Payment | Example | Purpose |
|---|---|---|
| PAYMENT_API_TOKEN | same value as in Purchase | required; checks the bearer token |
| OPERATOR_PASSWORD | shared secret | required; HTTP Basic for GET /operator |

| Access | Example | Purpose |
|---|---|---|
| ACCESS_API_TOKEN | same value as in Purchase | required; checks the bearer token |
| STAFF_PASSWORD | shared secret | required; HTTP Basic for the kiosk |

## Repository layout

```
cowork-booking-docs/  README.md SOURCES.md GLOSSARY.md RULES.md ID_MAP.md DECISIONS.md OPEN_QUESTIONS.md PRD.md
                      BUSINESS_MODEL.md ARCHITECTURE.md adr/ diagrams/ contracts/README.md (links to provider copies)
                      REVIEW_LOG.md TRACEABILITY.md inventory/ scripts/check_docs.py
                      integration/{compose.yaml,compose.e2e.yaml,.env.example,e2e/,README.md} .github/workflows/docs.yml
cowork-booking-<svc>/ app.py (or a small package past ~600 lines) <domain>.py clock.py templates/ static/ tests/
                      openapi.yaml CONTRACT.md (Payment, Access) PROVENANCE.md README.md Dockerfile compose.yaml
                      gunicorn.conf.py pytest.ini requirements.txt .github/workflows/ci.yml
```

`<domain>.py` is `purchase.py`, `payment.py` or `access.py`. Purchase adds `payment_client.py` and `access_client.py`, the one boundary its tests stub.
