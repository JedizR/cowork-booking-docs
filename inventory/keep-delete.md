# Keep / delete per service

Every file in the Spacey tree at `5a1cf3d`, and every route, table and helper, mapped to the three service repos by BRIEF section 10. This is the plan for M4's copy-and-prune seed; nothing is copied in M0.

## BRIEF section 10, the rules applied

| Rule | Section 10 text (short) |
|---|---|
| R-ALL | "Every service keeps: `/health` with `revision`, the fail-fast DB connect, gunicorn query-string scrubbing, `base.html` + `style.css` (one shared look), and the `money`/`local_time` filters (adapted to THB)." |
| R-PUR | "Purchase keeps: spaces, bookings (reshaped), users → members (+`is_operator`, `plan_active`), register/login/logout/`inject_current_user`, `purchase.py`, metrics (booking metrics only), the index, my_bookings, login, register and dashboard templates, and the booking header of `confirmation.html`." |
| R-COV | "Coverage moves to Purchase: `member_key`, `is_subscribed`, the subscribe route and the subscriptions table become `Member.plan_active`." New table `test_clock`. |
| R-PMT | "Payment keeps: `validate_card` and the card regexes, and the payment form part of `confirmation.html` (it becomes the hosted page). New tables: `payment_sessions`, `payment_attempts`, `refunds`, `test_clock`. It deletes subscriptions and everything booking-related." |
| R-AXS | "Access keeps: `issue_access_code` (rewritten to persist), and the unlock part of `confirmation.html` (it becomes the ticket page). New tables: `grants`, `scans`, `test_clock`." |
| R-DEL | "Everything else is deleted and listed in `PROVENANCE.md`." |
| R-PRE | Removed before the seed commit: `STARTUP_LOG.md`, `LOAD_TEST.md`, `CONTRIBUTING.md`, `scripts/`, `deploy/` (the Nomad job) and `.github/workflows/delivery.yml`. |
| R-LAY | Service layout: `app.py`, `<domain>.py`, `clock.py`, `templates/`, `static/`, `tests/`, `openapi.yaml`, `CONTRACT.md` (Payment, Access), `PROVENANCE.md`, `README.md`, `Dockerfile`, `compose.yaml`, `gunicorn.conf.py`, `pytest.ini`, `requirements.txt`, `.github/workflows/ci.yml`. |

Cell values: **keep** = copied and kept as is (apart from scrub and branding); **adapt** = kept and changed; **part** = only the named part is kept; **-** = removed from that service in the prune commit. Delete column: **before seed** = removed from the export before the seed commit (never in any repo history); **prune** = removed by the prune commit from every service marked "-"; **all** = kept by no service. Items section 10 does not name are marked "not named" in Notes and follow R-DEL unless a layout entry (R-LAY) covers them.

Before the seed commit, every kept file is also scrubbed of persona names (BRIEF section 11; see [spacey-tests-infra.md](spacey-tests-infra.md) section 9) and of "spacey" branding on scanned surfaces (see [spacey-app.md](spacey-app.md)).

## 1. Files (28, from `git ls-tree -r --name-only origin/main`)

| # | Path | Lines | Purchase | Payment | Access | Delete | Basis | Notes | Evidence |
|---|---|---:|---|---|---|---|---|---|---|
| 1 | `.dockerignore` | 6 | keep | keep | keep | - | not named | Section 10's layout lists no dotfiles; not on the delete list. Kept as build hygiene; confirm in M4. | source inspected at 5a1cf3d |
| 2 | `.github/workflows/delivery.yml` | 117 | - | - | - | **before seed** | R-PRE | Pushes to ghcr and deploys to Nomad. Replaced by a new `ci.yml` (D26). | source inspected at 5a1cf3d |
| 3 | `.gitignore` | 7 | keep | keep | keep | - | not named | Already ignores `.env` (needed for "Commit only `.env.example` files"). Confirm in M4. | source inspected at 5a1cf3d |
| 4 | `CONTRIBUTING.md` | 15 | - | - | - | **before seed** | R-PRE | | source inspected at 5a1cf3d |
| 5 | `Dockerfile` | 17 | adapt | adapt | adapt | - | R-LAY | Copy list changes per service; workers move to `gunicorn.conf.py` (D28) | source inspected at 5a1cf3d |
| 6 | `LOAD_TEST.md` | 38 | - | - | - | **before seed** | R-PRE | | source inspected at 5a1cf3d |
| 7 | `README.md` | 127 | adapt | adapt | adapt | - | R-LAY | Rewritten per service (quick start, env, ports); remove "spacey" DB URLs | source inspected at 5a1cf3d |
| 8 | `STARTUP_LOG.md` | 1399 | - | - | - | **before seed** | R-PRE | Contains personal names and a live hostname | source inspected at 5a1cf3d |
| 9 | `app.py` | 1053 | part | part | part | prune | R-PUR, R-PMT, R-AXS | Split by the route, table and helper rows below | source inspected at 5a1cf3d |
| 10 | `compose.yaml` | 23 | adapt | adapt | adapt | - | R-LAY | DB host ports 5441 / 5442 / 5443; app 8001 / 8002 / 8003; no "spacey" DB names; healthcheck | source inspected at 5a1cf3d |
| 11 | `deploy/startup-app.nomad.hcl` | 96 | - | - | - | **before seed** | R-PRE | No Nomad (D26) | source inspected at 5a1cf3d |
| 12 | `gunicorn.conf.py` | 5 | keep | keep | keep | - | R-ALL | Query-string scrubbing; add `workers = 2` (D28) | source inspected at 5a1cf3d |
| 13 | `openapi.yaml` | 732 | adapt | adapt | adapt | - | R-LAY | Purchase: prune to its own ops. Payment and Access: file kept, content replaced by the section 5.2 / 5.3 APIs. Title and persona examples change. | source inspected at 5a1cf3d |
| 14 | `purchase.py` | 15 | adapt | - | - | prune | R-PUR | Price in satang by whole blocks (D8) | source inspected at 5a1cf3d |
| 15 | `pytest.ini` | 3 | keep | keep | keep | - | R-LAY | | source inspected at 5a1cf3d |
| 16 | `requirements.txt` | 4 | keep | keep | adapt | - | R-LAY | Access adds `segno` (the only new runtime dependency) | source inspected at 5a1cf3d |
| 17 | `scripts/load_test.py` | 59 | - | - | - | **before seed** | R-PRE | | source inspected at 5a1cf3d |
| 18 | `static/style.css` | 162 | keep | keep | keep | - | R-ALL | One shared look | source inspected at 5a1cf3d |
| 19 | `templates/base.html` | 24 | adapt | adapt | adapt | - | R-ALL | New title and brand; nav per service | source inspected at 5a1cf3d |
| 20 | `templates/booking_not_found.html` | 5 | - | - | - | all | R-DEL (not named) | Purchase may re-create a 404 page for D17; decide in M4 | source inspected at 5a1cf3d |
| 21 | `templates/confirmation.html` | 27 | part (booking header) | part (payment form, becomes hosted page) | part (unlock part, becomes ticket page) | prune | R-PUR, R-PMT, R-AXS | Parts by line in section 5 | source inspected at 5a1cf3d |
| 22 | `templates/dashboard.html` | 32 | adapt | - | - | prune | R-PUR | Operator-only; booking metrics only (D24) | source inspected at 5a1cf3d |
| 23 | `templates/index.html` | 39 | adapt | - | - | prune | R-PUR | New date/duration/block flow (5.1) | source inspected at 5a1cf3d |
| 24 | `templates/login.html` | 17 | keep | - | - | prune | R-PUR | `flash()` instead of `?error=` (D28) | source inspected at 5a1cf3d |
| 25 | `templates/my_bookings.html` | 19 | adapt | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 26 | `templates/register.html` | 14 | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 27 | `tests/test_app.py` | 2078 | part | part | part | prune | R-LAY | Split by test area in section 6 | source inspected at 5a1cf3d |
| 28 | `tests/test_purchase.py` | 24 | adapt | - | - | prune | R-PUR | Follows `purchase.py` | source inspected at 5a1cf3d |

New files per service (not in Spacey): `clock.py`, `PROVENANCE.md`, `.github/workflows/ci.yml` (all); `CONTRACT.md` (Payment, Access); `.env.example` (all).

## 2. Routes (27 + static)

| # | Method | Path | Purchase | Payment | Access | Delete | Basis | Notes | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | GET | `/` | adapt | - | - | prune | R-PUR (index) | | source inspected at 5a1cf3d |
| 2 | GET | `/register` | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 3 | POST | `/register` | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 4 | GET | `/login` | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 5 | POST | `/login` | adapt | - | - | prune | R-PUR | Operator promotion by `OPERATOR_EMAIL`; 12 h session (D15) | source inspected at 5a1cf3d |
| 6 | POST | `/logout` | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 7 | GET | `/health` | keep | keep | keep | - | R-ALL | | source inspected at 5a1cf3d |
| 8 | GET | `/spaces` | adapt | - | - | prune | R-PUR | Hide archived spaces (D23) | source inspected at 5a1cf3d |
| 9 | POST | `/spaces` | adapt | - | - | prune | R-PUR | Operator only; rate rules (D9) | source inspected at 5a1cf3d |
| 10 | GET | `/spaces/<id>` | adapt | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| 11 | PATCH | `/spaces/<id>` | adapt | - | - | prune | R-PUR | Operator only | source inspected at 5a1cf3d |
| 12 | DELETE | `/spaces/<id>` | adapt | - | - | prune | R-PUR | Becomes archive (D23); never deletes a space with bookings | source inspected at 5a1cf3d |
| 13 | GET | `/spaces/<id>/bookings` | adapt | - | - | prune | R-PUR | Operator only | source inspected at 5a1cf3d |
| 14 | POST | `/spaces/<id>/bookings` | adapt | - | - | prune | R-PUR (bookings reshaped) | Blocks, notice, hold, coverage (D2-D11) | source inspected at 5a1cf3d |
| 15 | POST | `/spaces/<id>/book` | adapt | - | - | prune | R-PUR (bookings reshaped) | Date + block + party size form (D2, 5.1) | source inspected at 5a1cf3d |
| 16 | GET | `/bookings/<id>/confirmation` | part (booking page) | part (hosted page `GET /pay/{id}`) | part (ticket page `GET /t/<token>`) | prune | R-PUR, R-PMT, R-AXS | Split with `confirmation.html` | source inspected at 5a1cf3d |
| 17 | POST | `/bookings/<id>/confirmation/pay` | - | - | - | all | R-PMT ("deletes ... everything booking-related") | The hosted page's own POST replaces it | source inspected at 5a1cf3d |
| 18 | POST | `/bookings/<id>/confirmation/unlock` | - | - | - | all | R-DEL | Issuance moves to `POST /grants` | source inspected at 5a1cf3d |
| 19 | GET | `/bookings/mine` | adapt | - | - | prune | R-PUR (my_bookings) | Upcoming and past; cancel with refund preview | source inspected at 5a1cf3d |
| 20 | GET | `/bookings` | adapt | - | - | prune | R-PUR | Operator only (flaw F7) | source inspected at 5a1cf3d |
| 21 | GET | `/bookings/<id>` | adapt | - | - | prune | R-PUR | Owner or operator; others 404 (D17) | source inspected at 5a1cf3d |
| 22 | DELETE | `/bookings/<id>` | adapt | - | - | prune | R-PUR (bookings reshaped) | Status cancel, never hard delete (D18, D19) | source inspected at 5a1cf3d |
| 23 | POST | `/bookings/<id>/pay` | - | - | - | all | R-PMT (booking-related) | Replaced by `POST /payment-sessions` and the hosted page | source inspected at 5a1cf3d |
| 24 | POST | `/bookings/<id>/unlock` | - | - | - | all | R-DEL | Replaced by Access `POST /grants` | source inspected at 5a1cf3d |
| 25 | POST | `/members/<name>/subscribe` | adapt | - | - | prune | R-COV | Becomes the operator's `plan_active` toggle | source inspected at 5a1cf3d |
| 26 | GET | `/metrics` | adapt | - | - | prune | R-PUR (booking metrics only) | Revenue totals move to Payment's operator page (D24) | source inspected at 5a1cf3d |
| 27 | GET | `/dashboard` | adapt | - | - | prune | R-PUR | Operator only (flaw F8) | source inspected at 5a1cf3d |
| - | GET | `/static/<path>` | keep | keep | keep | - | R-ALL | Flask built-in | source inspected at 5a1cf3d |

## 3. Tables and DB objects

| Object | Purchase | Payment | Access | Delete | Basis | Notes | Evidence |
|---|---|---|---|---|---|---|---|
| `spaces` | adapt | - | - | prune | R-PUR | Rate in satang, BIGINT (D1, D9); `archived_at` (D23) | source inspected at 5a1cf3d |
| `bookings` | adapt | - | - | prune | R-PUR (reshaped) | `paid` and `card_last4` leave the row; add status, reference, hold, coverage, cancel/refund and grant fields (5.1) | source inspected at 5a1cf3d |
| `subscriptions` | - | - | - | all | R-COV | Becomes `members.plan_active` | source inspected at 5a1cf3d |
| `users` | adapt | - | - | prune | R-PUR | Becomes `members` (+ display name, `is_operator`, `plan_active`) | source inspected at 5a1cf3d |
| `no_overlapping_bookings` EXCLUDE | adapt | - | - | prune | R-PUR (bookings) | Partial: `WHERE status IN ('held','confirmed')` (D11) | source inspected at 5a1cf3d |
| `btree_gist` extension | keep | - | - | prune | R-PUR (bookings) | Needed by the EXCLUDE | source inspected at 5a1cf3d |
| Startup `amount_cents` backfill | - | - | - | all | R-DEL | No historical NULL rows in a new DB | source inspected at 5a1cf3d |

New tables planned by section 10 (not in Spacey, so no evidence row): Purchase `test_clock`; Payment `payment_sessions`, `payment_attempts`, `refunds`, `test_clock`; Access `grants`, `scans`, `test_clock`.

## 4. Helpers, filters and config

| Item | Where | Purchase | Payment | Access | Delete | Basis | Notes | Evidence |
|---|---|---|---|---|---|---|---|---|
| `get_connection` | app.py:23 | adapt | adapt | adapt | - | R-ALL (fail-fast DB connect) | Each service runs only its own DDL | source inspected at 5a1cf3d |
| `parse_time` | app.py:143 | keep | - | - | prune | R-PUR (bookings) | JSON times need an offset (D2). Not named for Payment/Access; they may need an ISO parser for `expires_at` / `valid_from` (M4). | source inspected at 5a1cf3d |
| `parse_window` | app.py:154 | adapt | - | - | prune | R-PUR (spaces) | | source inspected at 5a1cf3d |
| `booked_space_ids` | app.py:170 | adapt | - | - | prune | R-PUR (bookings) | Uses the slot-blocking predicate with `clock.now()` (D11, D27) | source inspected at 5a1cf3d |
| `LOCAL_TZ` | app.py:188 | keep | keep | keep | - | R-ALL (needed by `local_time`) | Fixed UTC+7 (D2) | source inspected at 5a1cf3d |
| `parse_form_time` | app.py:191 | adapt | - | - | prune | R-PUR (bookings) | Form sends date + block; the server builds the instant (D2) | source inspected at 5a1cf3d |
| `is_valid_name` | app.py:203 | keep | - | - | prune | R-PUR (spaces) | | source inspected at 5a1cf3d |
| `is_valid_capacity` | app.py:207 | keep | - | - | prune | R-PUR (spaces) | | source inspected at 5a1cf3d |
| `is_valid_price` | app.py:216 | adapt | - | - | prune | R-PUR (spaces) | 0 or 20-10,000 THB per hour (D9) | source inspected at 5a1cf3d |
| `EMAIL_RE`, `is_valid_email`, `is_valid_password` | app.py:221-230 | keep | - | - | prune | R-PUR (register) | | source inspected at 5a1cf3d |
| `CARD_NUMBER_RE`, `CVC_RE`, `EXPIRY_RE` | app.py:232-234 | - | keep | - | prune | R-PMT | | source inspected at 5a1cf3d |
| `validate_card` | app.py:237 | - | adapt | - | prune | R-PMT | Uses `clock.now()`; test-card outcomes (5.2) | source inspected at 5a1cf3d |
| `member_key` | app.py:256 | - | - | - | all | R-COV | Replaced by `Member.plan_active` | source inspected at 5a1cf3d |
| `is_subscribed` | app.py:260 | - | - | - | all | R-COV | Replaced by `Member.plan_active` | source inspected at 5a1cf3d |
| `local_time` filter | app.py:270, 394 | keep | keep | keep | - | R-ALL | | source inspected at 5a1cf3d |
| `booking_to_json` | app.py:275 | adapt | - | - | prune | R-PUR (bookings) | | source inspected at 5a1cf3d |
| `compute_metrics` | app.py:283 | adapt | - | - | prune | R-PUR (booking metrics only) | D24; no revenue | source inspected at 5a1cf3d |
| `reset_tables` | app.py:359 | - | - | - | all | R-DEL (not named) | Each service's tests will need a reset of their own tables; decide in M4 | source inspected at 5a1cf3d |
| `seed_starter_space` | app.py:369 | adapt | - | - | prune | R-PUR (spaces) | Not named on its own; part of spaces. THB rate. | source inspected at 5a1cf3d |
| `create_app` | app.py:379 | adapt | adapt | adapt | - | R-ALL | App factory in every service | source inspected at 5a1cf3d |
| `money` filter | app.py:395 | adapt | adapt | adapt | - | R-ALL | "THB 1,234.50" (D1) | source inspected at 5a1cf3d |
| `percent` filter | app.py:396 | keep | - | - | prune | R-PUR (dashboard) | | source inspected at 5a1cf3d |
| `inject_current_user` | app.py:398 | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| `register_user` | app.py:443 | keep | - | - | prune | R-PUR | | source inspected at 5a1cf3d |
| `login_user` | app.py:489 | adapt | - | - | prune | R-PUR | Operator promotion (D15) | source inspected at 5a1cf3d |
| `book_space` | app.py:700 | adapt | - | - | prune | R-PUR (bookings reshaped) | | source inspected at 5a1cf3d |
| `mark_booking_paid` | app.py:932 | - | - | - | all | R-PMT ("everything booking-related") | Payment writes attempts on sessions instead | source inspected at 5a1cf3d |
| `issue_access_code` | app.py:970 | - | - | adapt | prune | R-AXS | Rewritten to persist; issued once, reused (5.3) | source inspected at 5a1cf3d |
| `app` (module level) | app.py:1053 | keep | keep | keep | - | R-ALL | `gunicorn app:app` | source inspected at 5a1cf3d |
| `calculate_booking_price_cents` | purchase.py:6 | adapt | - | - | prune | R-PUR | Satang and whole blocks (D8) | source inspected at 5a1cf3d |
| `DATABASE_URL` | app.py:14 | keep | keep | keep | - | R-ALL (env list) | Default must not say "spacey" | source inspected at 5a1cf3d |
| `SECRET_KEY` | app.py:20 | adapt | adapt | adapt | - | env list | Required, fail fast; no default (D15) | source inspected at 5a1cf3d |
| `RESET_DB_ON_START` | app.py:383 | - | - | - | all | R-DEL (not in the env list) | | source inspected at 5a1cf3d |
| `APP_REVISION` | app.py:551 | keep | keep | keep | - | R-ALL (`/health` revision) | | source inspected at 5a1cf3d |

## 5. `confirmation.html` parts

| Part | Lines | Purchase | Payment | Access | Delete | Notes | Evidence |
|---|---|---|---|---|---|---|---|
| Booking header | 1-6, 26 | keep | - | - | prune | Booking page | source inspected at 5a1cf3d |
| Paid status line | 7-8 | part (status) | part (card last4) | - | prune | Payment stores only brand and last4 | source inspected at 5a1cf3d |
| Unlock button | 9-11 | - | - | adapt | prune | Ticket page | source inspected at 5a1cf3d |
| Payment form | 12-19 | - | adapt | - | prune | Hosted page `GET /pay/{id}` | source inspected at 5a1cf3d |
| Access code display (`?code=`) | 21-22 | - | - | adapt | prune | Shows the stored ticket code, never a query value (flaw F4) | source inspected at 5a1cf3d |
| Error message (`?error=`) | 23-24 | - | - | - | all | `flash()` instead (D28, flaw F12) | source inspected at 5a1cf3d |

## 6. Tests (`tests/test_app.py` areas)

The tests follow the code they cover. Tests that pin a flaw's behaviour (e.g. hard-delete cancel) are rewritten to the new rule, not kept as is.

| Area | Tests | Purchase | Payment | Access | Delete | Notes | Evidence |
|---|---:|---|---|---|---|---|---|
| G1 Homepage | 9 | adapt | - | - | prune | | source inspected at 5a1cf3d |
| G2 Booking form | 6 | adapt | - | - | prune | New form | source inspected at 5a1cf3d |
| G3 Confirmation page | 7 | part | part | part | prune | Split like the template | source inspected at 5a1cf3d |
| G4 Pricing | 7 | adapt | - | - | prune | | source inspected at 5a1cf3d |
| G5 Spaces CRUD | 21 | adapt | - | - | prune | Operator auth; archive | source inspected at 5a1cf3d |
| G6 Availability | 7 | adapt | - | - | prune | | source inspected at 5a1cf3d |
| G7 Booking API | 18 | adapt | - | - | prune | Keep the two-connection race test | source inspected at 5a1cf3d |
| G8 Cancel | 2 | adapt | - | - | prune | Hard delete becomes status cancel | source inspected at 5a1cf3d |
| G9 Mock payment | 13 | - | adapt | - | prune | Card validation only | source inspected at 5a1cf3d |
| G10 Unlock | 3 | - | - | adapt | prune | Stored grant | source inspected at 5a1cf3d |
| G11 Accounts | 15 | keep | - | - | prune | | source inspected at 5a1cf3d |
| G12 Account-linked bookings | 10 | adapt | - | - | prune | Guests can no longer book (D15) | source inspected at 5a1cf3d |
| G13 Subscriptions | 9 | adapt | - | - | prune | Become `plan_active` tests | source inspected at 5a1cf3d |
| G14 Metrics JSON | 15 | adapt | - | - | prune | D24 definitions | source inspected at 5a1cf3d |
| G15 Dashboard | 8 | adapt | - | - | prune | Operator only | source inspected at 5a1cf3d |
| G16 Health and startup | 4 | adapt | adapt | adapt | - | Backfill test goes (no backfill) | source inspected at 5a1cf3d |
| `tests/test_purchase.py` | 6 | adapt | - | - | prune | | source inspected at 5a1cf3d |

## 7. Deleted-before-seed list (for `PROVENANCE.md`)

| Path | Why | Evidence |
|---|---|---|
| `STARTUP_LOG.md` | Team log with personal names; not product code | source inspected at 5a1cf3d |
| `LOAD_TEST.md` | One-off load-test notes | source inspected at 5a1cf3d |
| `CONTRIBUTING.md` | Old team process | source inspected at 5a1cf3d |
| `scripts/` (`scripts/load_test.py`) | Load-test script | source inspected at 5a1cf3d |
| `deploy/` (`deploy/startup-app.nomad.hcl`) | Nomad job; no Nomad (D26) | source inspected at 5a1cf3d |
| `.github/workflows/delivery.yml` | Pushes to ghcr and deploys to Nomad on every push to main | source inspected at 5a1cf3d |
