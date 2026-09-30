# Spacey tests and infrastructure at 5a1cf3d

Source: `cs403bkk-2026/spacey` main `5a1cf3d90e538f431625cbb959987b7bdbe3c946`. For the test run, the tree was exported with `git archive origin/main` into a scratch folder, and the tests ran there, not in the sources clone.

## 1. Test run on Python 3.12

| Item | Value | Evidence |
|---|---|---|
| Result | **160 passed, 0 failed, 0 skipped, 0 errors** in 10.24 s, exit code 0 | test run at 5a1cf3d |
| Python | `Python 3.12.11` (uv venv, uv 0.7.17) | test run at 5a1cf3d |
| Database | Throwaway `postgres:16` container on host port 55439; server reported `PostgreSQL 16.14 (Debian 16.14-1.pgdg13+1) on aarch64-unknown-linux-gnu`. Removed after the run (`docker rm -f`; `docker ps -a` then showed 0 matches). | test run at 5a1cf3d |
| Env | Only `DATABASE_URL=postgresql://postgres:postgres@localhost:55439/postgres`. `SECRET_KEY`, `RESET_DB_ON_START` and `APP_REVISION` unset. | test run at 5a1cf3d |
| Command | `.venv/bin/python -m pytest -q -p no:cacheprovider` (the flag only stops pytest writing `.pytest_cache`) | test run at 5a1cf3d |
| Collected per file | `tests/test_app.py`: 154, `tests/test_purchase.py`: 6 (`pytest --collect-only`) | test run at 5a1cf3d |
| Per-test run (`-rA`) | Second run, 2026-09-30 17:39 UTC (2026-10-01 00:39 Bangkok): a fresh `git archive` export of `5a1cf3d` (not the clone), a new Python 3.12.11 uv venv, the same env (only `DATABASE_URL` set), a new throwaway `postgres:16` container (server 16.14) on port 55439, removed after the run. `pytest -rA`: 160 `PASSED` lines, "160 passed in 12.93s", exit code 0. Full log: [spacey-pytest-rA-5a1cf3d.log](spacey-pytest-rA-5a1cf3d.log). | test run at 5a1cf3d |
| Race test, history | `STARTUP_LOG.md` calls the concurrency test flaky (line 492: "it's flaky and not caused by this PR"), traces it to a deadlock that gave a 500 (line 625), then says (line 834): "It already was (a deadlock now returns 409). The test passed 40 runs in a row on main." Those runs are the log's, not ours. | source inspected at 5a1cf3d |
| Race test, our runs | `test_concurrent_bookings_for_the_same_slot_only_one_succeeds` passed in both runs (its `PASSED` line is below). Not re-run to probe flakiness. | test run at 5a1cf3d |

Exact output:

```
$ .venv/bin/python --version
Python 3.12.11
$ docker exec m0-spacey-pg psql -U postgres -tAc 'select version()'
PostgreSQL 16.14 (Debian 16.14-1.pgdg13+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
$ DATABASE_URL=postgresql://postgres:postgres@localhost:55439/postgres .venv/bin/python -m pytest -q
........................................................................ [ 45%]
........................................................................ [ 90%]
................                                                         [100%]
160 passed in 10.24s
exit code: 0

$ DATABASE_URL=... .venv/bin/python -m pytest -q --collect-only | per-file counts
tests/test_app.py: 154
tests/test_purchase.py: 6
160 tests collected in 0.11s
```

Prior baseline: BRIEF section 4 reports 160 passed on Python 3.11.7. That is prior research, not re-run in M0.

Second run, per-test output (the `PASSED` lines for every test the inventory names; all 160 are in the log file):

```
$ DATABASE_URL=postgresql://postgres:postgres@localhost:55439/postgres .venv/bin/python -m pytest -rA -p no:cacheprovider
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0
collected 160 items
...
============================= 160 passed in 12.93s =============================
exit code: 0
$ grep -c '^PASSED ' spacey-pytest-rA-5a1cf3d.log
160
$ grep -E '^PASSED .*(<the 13 test_app.py tests named in the inventory>)|^PASSED .*test_purchase' spacey-pytest-rA-5a1cf3d.log
PASSED tests/test_app.py::test_book_pay_unlock_all_the_way_through_the_browser
PASSED tests/test_app.py::test_confirmation_page_shows_times_in_bangkok_time
PASSED tests/test_app.py::test_a_subscribers_booking_shows_zero_amount_on_the_confirmation_page
PASSED tests/test_app.py::test_form_times_are_read_as_bangkok_time
PASSED tests/test_app.py::test_concurrent_bookings_for_the_same_slot_only_one_succeeds
PASSED tests/test_app.py::test_cancel_booking_makes_space_available_again
PASSED tests/test_app.py::test_unlock_a_paid_booking_returns_an_access_code
PASSED tests/test_app.py::test_registering_with_a_duplicate_email_is_rejected
PASSED tests/test_app.py::test_a_guest_booking_has_no_user_id
PASSED tests/test_app.py::test_subscription_matches_the_member_name_ignoring_case_and_spaces
PASSED tests/test_app.py::test_a_subscribers_booking_adds_no_per_booking_revenue
PASSED tests/test_app.py::test_startup_fails_fast_with_a_clear_message_for_a_bad_database_url
PASSED tests/test_app.py::test_list_bookings_returns_bookings_across_all_spaces
PASSED tests/test_purchase.py::test_booking_price_examples[1500-1800-750]
PASSED tests/test_purchase.py::test_booking_price_examples[1000-1200-333]
PASSED tests/test_purchase.py::test_booking_price_examples[100-18-1]
PASSED tests/test_purchase.py::test_booking_price_examples[100-17-0]
PASSED tests/test_purchase.py::test_booking_price_examples[3600-1.9-1]
PASSED tests/test_purchase.py::test_booking_price_examples[0-3600-0]
```

Resolved packages in the run venv (`uv pip freeze`, 2026-09-30):

```
blinker==1.9.0  certifi==2026.7.22  charset-normalizer==3.5.2  click==8.5.0  flask==3.1.2
gunicorn==23.0.0  idna==3.20  iniconfig==2.3.0  itsdangerous==2.2.0  jinja2==3.1.6
markupsafe==3.0.3  packaging==26.3  pluggy==1.6.0  psycopg==3.2.13  psycopg-binary==3.2.13
pygments==2.21.0  pytest==8.4.2  requests==2.32.3  typing-extensions==4.16.0  urllib3==2.8.0
werkzeug==3.1.9
```

## 2. Test files

| File | Lines | Tests | Style | Evidence |
|---|---:|---:|---|---|
| `tests/test_app.py` | 2078 | 154 | Flask `test_client()` against a real Postgres. JSON API and HTML pages. No fixtures (only `monkeypatch` in one test), no `conftest.py`, no markers. | source inspected at 5a1cf3d |
| `tests/test_purchase.py` | 24 | 6 | One `@pytest.mark.parametrize` unit test of `purchase.calculate_booking_price_cents`: (1500,1800,750), (1000,1200,333), (100,18,1), (100,17,0), (3600,1.9,1), (0,3600,0). Imports only `purchase`; needs no DB by itself. | source inspected at 5a1cf3d |

### Tests by area (`tests/test_app.py`, 154)

The rows are read from `tests/test_app.py`. Pass results per group are in the check table below the appendix note. The "pins" column is Observed Spacey behaviour. The last column is the BRIEF section 10 destination of the code under test (a planning hint).

| # | Area | Tests | What the tests pin | Section 10 destination | Evidence |
|---|---|---:|---|---|---|
| G1 | Homepage `/` | 9 | "free right now" / "booked right now", "$15.00 per hour", upcoming booked times, a booking form on every space, names escaped against XSS, links to register, My bookings (only when logged in) and dashboard | Purchase (index) | source inspected at 5a1cf3d |
| G2 | Booking form `POST /spaces/<id>/book` | 6 | Naive form times read as Bangkok (UTC+7). 302 to `/bookings/<id>/confirmation`. Overlap and missing times give an error message after the redirect. | Purchase | source inspected at 5a1cf3d |
| G3 | Confirmation page (+ `/pay`, `/unlock`) | 7 | Browser book, pay, unlock. "Not paid yet - total $x", then "Paid. Total: $x", then "card ending 4242". Unlock code is 8 hex chars. Unlock before paying shows an error. Unknown id gives 404. | Split: header Purchase, pay form Payment, unlock Access | source inspected at 5a1cf3d |
| G4 | Pricing and frozen amount | 7 | Hourly rate x duration, rounded half up (333 for 20 min at 1000). `amount_cents` on every booking response. A later price change does not change past amounts or revenue. | Purchase (`purchase.py`) | source inspected at 5a1cf3d |
| G5 | Spaces CRUD | 21 | Seed "Founders Desk" (capacity 1, 2500/h). Validation of create and PATCH (name, capacity int >= 1 not bool, price_cents int >= 0 not bool). DELETE 204, 409 if bookings exist, 404 unknown. All anonymous. | Purchase | source inspected at 5a1cf3d |
| G6 | Availability | 7 | `available` = free right now, or free for an optional `?start_time&end_time` window (both, tz-aware, in order). Back-to-back is free. | Purchase | source inspected at 5a1cf3d |
| G7 | Booking API | 18 | 201 with the full booking. 404 unknown space. 400 missing/inverted times or bad `party_size`. 409 on overlap. A two-connection race gives exactly one 201 and one 409. `created_at` set by the DB. Lists earliest first. All anonymous. | Purchase | source inspected at 5a1cf3d |
| G8 | Cancel `DELETE /bookings/<id>` | 2 | Cancel returns the booking, then `GET` gives **404** (hard delete) and the space is free again | Purchase (reshaped) | source inspected at 5a1cf3d |
| G9 | Mock payment `POST /bookings/<id>/pay` | 13 | Card shape checks (13-19 digits, MM/YY not before the current month, CVC 3-4 digits). Only `card_last4` kept. `force_failure` gives 402 and the booking stays unpaid. Retry works. Paying twice is a no-op and counts revenue once. | Payment (`validate_card`, regexes) | source inspected at 5a1cf3d |
| G10 | Unlock `POST /bookings/<id>/unlock` | 3 | 402 if unpaid, 200 with `access_code` if paid, 404 if unknown | Access (`issue_access_code`) | source inspected at 5a1cf3d |
| G11 | Accounts | 15 | Email normalised and unique (409). Password >= 8 chars, stored hashed. Same 401 for wrong password and unknown email. JSON and form variants. Logout idempotent. | Purchase (Member) | source inspected at 5a1cf3d |
| G12 | Account-linked bookings, My bookings | 10 | `user_id` from the session, null for guests. `/bookings/mine` redirects to `/login` when logged out and lists only the user's own bookings. | Purchase | source inspected at 5a1cf3d |
| G13 | Subscriptions (coverage) | 9 | `POST /members/<name>/subscribe` keys on the trimmed, lower-cased typed name. A subscriber's booking is paid on creation at amount 0 and adds no revenue. | Purchase (`Member.plan_active`) | source inspected at 5a1cf3d |
| G14 | Metrics JSON `/metrics` | 15 | Counts, paid/unpaid split, revenue from paid bookings, utilization over the next 7 days, repeat member rate, payment conversion, average revenue per paid booking, revenue by space. Zero-denominator cases return 0. | Purchase (booking metrics only) | source inspected at 5a1cf3d |
| G15 | Dashboard `/dashboard` | 8 | Metrics, paid/unpaid split, investor metrics, a CSS revenue bar per space, "No spaces yet.", "space booking system", "test and load-test data", link home. Anonymous. | Purchase (dashboard) | source inspected at 5a1cf3d |
| G16 | Health and startup | 4 | `/health` returns `{"revision","status":"ok"}`, or 503 "database unreachable" when the connection is closed. A bad `DATABASE_URL` gives `SystemExit` naming the URL and "docker compose up db -d". The startup `amount_cents` backfill. | All services | source inspected at 5a1cf3d |
| | **Total** | **154** | | | source inspected at 5a1cf3d |

A script checked the appendix against `tests/test_app.py`: `OK: 154 tests, each in exactly one group, line numbers match` (source inspected at 5a1cf3d).

| Check | Result | Evidence |
|---|---|---|
| Every appendix test name has a `PASSED` line in the `-rA` log | 154 of 154; every group G1-G16 is n/n (script output below) | test run at 5a1cf3d |
| Tests in G5, G7, G10 and G15 that call `register(client`, `login(client`, `/login`, `/register` or `session_transaction` | 0 of 50 (script output below) | source inspected at 5a1cf3d |

```
$ python3 check_groups.py spacey-tests-infra.md test_app.py spacey-pytest-rA-5a1cf3d.log
G1: 9/9 PASSED; tests that register, log in or set a session: 2
G2: 6/6 PASSED; tests that register, log in or set a session: 0
G3: 7/7 PASSED; tests that register, log in or set a session: 0
G4: 7/7 PASSED; tests that register, log in or set a session: 0
G5: 21/21 PASSED; tests that register, log in or set a session: 0
G6: 7/7 PASSED; tests that register, log in or set a session: 0
G7: 18/18 PASSED; tests that register, log in or set a session: 0
G8: 2/2 PASSED; tests that register, log in or set a session: 0
G9: 13/13 PASSED; tests that register, log in or set a session: 0
G10: 3/3 PASSED; tests that register, log in or set a session: 0
G11: 15/15 PASSED; tests that register, log in or set a session: 14
G12: 10/10 PASSED; tests that register, log in or set a session: 9
G13: 9/9 PASSED; tests that register, log in or set a session: 0
G14: 15/15 PASSED; tests that register, log in or set a session: 0
G15: 8/8 PASSED; tests that register, log in or set a session: 0
G16: 4/4 PASSED; tests that register, log in or set a session: 0
test_app.py PASSED lines: 154; appendix names with a PASSED line: 154
```

(`test_app.py` is `git show 5a1cf3d:tests/test_app.py`. The script is a scratch file, not kept. The `n/n PASSED` part reads the run log; the log-in count reads the source.)

### Tests that pin behaviour BRIEF section 4 lists as a flaw

What each test asserts is read from source. That they passed is the last row, from the `-rA` run. This is Observed Spacey behaviour, not policy.

| BRIEF flaw | Test(s) that assert it | Evidence |
|---|---|---|
| Cancel hard-deletes the booking | `test_cancel_booking_makes_space_available_again` (664) asserts that `GET /bookings/<id>` gives 404 after cancel | source inspected at 5a1cf3d |
| Past bookings accepted | `test_confirmation_page_shows_times_in_bangkok_time` (179) and `test_form_times_are_read_as_bangkok_time` (303) book 2026-09-25 09:00 Bangkok, before the run date; 14 lines call `slot(-1, 1)`, which starts an hour before collection time | source inspected at 5a1cf3d |
| Free subscription keyed by typed name, paid at amount 0 | `test_a_subscribers_booking_shows_zero_amount_on_the_confirmation_page` (293); `test_subscription_matches_the_member_name_ignoring_case_and_spaces` (1327) asserts `paid is True` for two spellings of the subscribed name; `test_a_subscribers_booking_adds_no_per_booking_revenue` (1341) asserts `paid_bookings == 1` and `revenue_cents == 0` | source inspected at 5a1cf3d |
| Access code regenerated, not stored | `test_book_pay_unlock_all_the_way_through_the_browser` (132) only checks `len(code) == 8`; no test calls `/unlock` twice, so none checks reuse | source inspected at 5a1cf3d |
| No ownership checks | No test in G5, G7, G10 or G15 registers, logs in or sets a session (0 of 50, check in section 2), e.g. `test_list_bookings_returns_bookings_across_all_spaces` (1911), `test_unlock_a_paid_booking_returns_an_access_code` (924) | source inspected at 5a1cf3d |
| Guest bookings (free-text `member`) | `test_a_guest_booking_has_no_user_id` (1146) | source inspected at 5a1cf3d |
| Form has no party size field; 0-amount asks for a card | No test covers either | source inspected at 5a1cf3d |
| Every test named in this table | `PASSED` in the `-rA` run (lines in section 1); all 50 tests of G5, G7, G10 and G15 also passed (check in section 2) | test run at 5a1cf3d |

### Time bombs in the suite

| Where | What breaks later | Evidence |
|---|---|---|
| `VALID_CARD` expiry `"12/30"` (line 21) | Every pay test fails from January 2031 | source inspected at 5a1cf3d |
| `test_homepage_lists_the_upcoming_booked_times_of_a_space` (68) books 2030-01-01 10:00-11:00 Bangkok | The homepage lists only bookings with `end_time > now()`, so it fails after 2030-01-01 04:00 UTC | source inspected at 5a1cf3d |
| `NOW = datetime.now(timezone.utc)` at import (line 8) | All `slot()` times are relative to collection time; a very slow run shifts the "right now" checks | source inspected at 5a1cf3d |

## 3. How the tests set up the database

| Step | Detail | Evidence |
|---|---|---|
| Finding the DB | `DATABASE_URL` is read at import (app.py:14-16). `app.py:1053` has a module-level `app = create_app()`, so importing it in `tests/test_app.py` connects and runs DDL during collection. With no DB, even `--collect-only` fails. | source inspected at 5a1cf3d |
| Per test | Each test calls `make_client()` = `create_app(reset_on_start=True).test_client()`. No fixtures, no teardown. | source inspected at 5a1cf3d |
| DDL | All DDL runs on every `create_app` call (see [spacey-schema.md](spacey-schema.md)). | source inspected at 5a1cf3d |
| Reset | `reset_tables`: `TRUNCATE ... RESTART IDENTITY CASCADE`. Tests rely on ids restarting at 1 (e.g. `/bookings/1`, `/spaces/2`). | source inspected at 5a1cf3d |
| Seed | `seed_starter_space` inserts ("Founders Desk", 1, 2500) when `spaces` is empty | source inspected at 5a1cf3d |
| Second connection | The race test, the password-hash test and the backfill test open a second `create_app(reset_on_start=False)` on the same DB. The race test uses two threads and a `threading.Barrier`. | source inspected at 5a1cf3d |
| Failure cases | `app.db.close()` for the 503 health check; `postgresql://spacey:spacey@localhost:1/spacey` for fail-fast | source inspected at 5a1cf3d |
| Privileges | `CREATE EXTENSION btree_gist` needs a role that may create extensions (superuser `postgres` locally, `spacey` in CI) | source inspected at 5a1cf3d |
| Isolation | Order-independent because of the TRUNCATE; not safe in parallel (one shared DB, no xdist) | source inspected at 5a1cf3d |
| `RESET_DB_ON_START` | Not needed by the tests (they pass `reset_on_start=True`); affects only the module-level `app` and the deployed app | source inspected at 5a1cf3d |

## 4. Container, compose, gunicorn

| File | Summary | Evidence |
|---|---|---|
| `Dockerfile` (17 lines) | `FROM python:3.12-slim`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`, `WORKDIR /app`, `pip install --no-cache-dir -r requirements.txt` (so pytest and requests are in the runtime image). Copies `app.py purchase.py gunicorn.conf.py templates/ static/`, not tests and not `openapi.yaml`. `EXPOSE 8000`. `CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]`. No `-w`, so **1 sync worker**. No `USER` (runs as root). No `HEALTHCHECK`. | source inspected at 5a1cf3d |
| `gunicorn.conf.py` (5 lines) | Picked up from the working directory. `accesslog = "-"` ("so it reaches Loki"). `access_log_format` uses `%(U)s` (path without query string) and leaves out the referer, because "the door access code arrives as ?code=...". No workers, threads or timeout. | source inspected at 5a1cf3d |
| `compose.yaml` (23 lines) | `db`: `postgres:16`, user/password/db `spacey`, host `5433:5432`, named volume `db-data`. `app`: `build: .`, `APP_REVISION=compose`, `DATABASE_URL=postgresql://spacey:spacey@db:5432/spacey`, ports `8000:8000`, `depends_on: [db]` with no health condition and no restart policy (the app can exit on fail-fast if the DB is slow). No `SECRET_KEY`. | source inspected at 5a1cf3d |
| `.dockerignore` | `.git .github .venv __pycache__ .pytest_cache *.pyc` | source inspected at 5a1cf3d |
| `.gitignore` | `.env .venv/ __pycache__/ .pytest_cache/ *.py[cod] .DS_Store source/` | source inspected at 5a1cf3d |
| `pytest.ini` | `pythonpath = .` and `testpaths = tests` (added so plain `pytest` stops collecting `scripts/load_test.py`) | source inspected at 5a1cf3d |

## 5. CI: `.github/workflows/delivery.yml` (117 lines)

Triggers: `pull_request` (any branch) and `push` to `main`. Permissions: `contents: read`, `packages: write`. Env: `IMAGE: ghcr.io/${{ github.repository }}:${{ github.sha }}`.

| Job | When | Steps | Evidence |
|---|---|---|---|
| `test` | every PR and push | Service `postgres:16` (user/password/db `spacey`, port 5432, `pg_isready -U spacey` every 5 s, 5 retries). checkout@v4, setup-python@v5 "3.12" with pip cache, `pip install -r requirements.txt`, `pytest` with `DATABASE_URL=postgresql://spacey:spacey@localhost:5432/spacey`. | source inspected at 5a1cf3d |
| `build` | push only, needs `test` | checkout, `docker/login-action@v3` to `ghcr.io` with `GITHUB_TOKEN`, `docker/build-push-action@v6` `push: true`, tag `${IMAGE}`. PRs never build. | source inspected at 5a1cf3d |
| `deploy` | push only, `vars.DEPLOY_ENABLED == 'true'`, needs `build` | Concurrency group `spacey-production`, no cancel. `hashicorp/setup-nomad@main`. Freshness check: deploy only if main is still `GITHUB_SHA`, else "Skipping superseded revision". `nomad job run -detach -namespace=startup ... deploy/startup-app.nomad.hcl` with secrets `NOMAD_ADDR`, `NOMAD_TOKEN`. Verify: poll `https://$APP_HOSTNAME/health` up to 36 x 5 s until `.revision` equals the SHA. | source inspected at 5a1cf3d |

BRIEF section 10 deletes this file before the seed; D26 replaces it with `ci.yml` (pytest + `docker build`, no push).

## 6. Deploy: `deploy/startup-app.nomad.hcl` (96 lines)

| Part | Setting | Evidence |
|---|---|---|
| Variables | `image`, `hostname`, `revision` (strings from CI) | source inspected at 5a1cf3d |
| Job | `job "spacey"`, datacenter `cs403bkk`, namespace `startup`, `type = "service"` | source inspected at 5a1cf3d |
| Group `web` | `count = 1`, pinned to one Nomad node by constraint | source inspected at 5a1cf3d |
| Update | `max_parallel 1`, `health_check "checks"`, `min_healthy_time 10s`, `healthy_deadline 3m`, `progress_deadline 5m`, `auto_revert true` | source inspected at 5a1cf3d |
| Restart | 3 attempts per 5 m, 10 s delay, `mode "fail"` | source inspected at 5a1cf3d |
| Network | dynamic port `http` to 8000 | source inspected at 5a1cf3d |
| Secrets | `DATABASE_URL` rendered from Nomad variable `nomad/jobs/spacey` into `secrets/runtime.env`, `change_mode "restart"`. **No `SECRET_KEY`**, so deploy uses the public dev default (BRIEF flaw). | source inspected at 5a1cf3d |
| Resources | `cpu 300`, `memory 256` | source inspected at 5a1cf3d |
| Service | `provider "nomad"`, Traefik tags (`Host(<hostname>)`, `websecure`, TLS `letsencrypt`), HTTP check `/health` every 10 s, timeout 2 s | source inspected at 5a1cf3d |

BRIEF section 10 deletes this file before the seed; D26 drops Nomad.

## 7. Scripts and docs

| File | Summary | Evidence |
|---|---|---|
| `scripts/load_test.py` (59) | `ThreadPoolExecutor`; `GET {url}/spaces` N times (defaults `--url http://127.0.0.1:5000 --requests 200 --concurrency 5`) with `requests`, `timeout=10`. Prints latency stats and throughput. The only user of `requests`. Deleted before the seed. | source inspected at 5a1cf3d |
| `LOAD_TEST.md` (38) | Laptop run, 200 requests: concurrency 5, 0 failures, 2.2 ms median, ~1932 req/s; concurrency 50, 0 failures, 21.1 ms median, ~2047 req/s. Says "App run with `gunicorn -w 2` (2 sync workers) - the same worker count used by the Dockerfile", but the Dockerfile sets no `-w` (default 1). Deleted before the seed. | source inspected at 5a1cf3d |
| `README.md` (127) | Quick start (venv, `docker compose up db -d`, `DATABASE_URL=...localhost:5433/spacey pytest`, `flask --app app run --port 5001`), config table for 4 env vars, HTML and JSON route tables. "Direct pushes to `main` are blocked." "This repository is public." | source inspected at 5a1cf3d |
| `CONTRIBUTING.md` (15) | Branch per change, PR, no direct push to `main`, explain what/why/how checked, review each other, never commit secrets or `.env`; a blocker-report format. Deleted before the seed. | source inspected at 5a1cf3d |
| `STARTUP_LOG.md` (1399) | Day-by-day team log with PR links. Suite grew from 4 tests (day 2) to 154 (day 11, PR #160). Records the flaky race test (a deadlock gave a 500, fixed by catching `DeadlockDetected`, app.py:766). Contains personal names and a live hostname. Deleted before the seed. | source inspected at 5a1cf3d |

## 8. Requirements (`requirements.txt`, 5 entries, no final newline)

| Package | Pin | Note | Evidence |
|---|---|---|---|
| Flask | `==3.1.2` | web framework | source inspected at 5a1cf3d |
| gunicorn | `==23.0.0` | WSGI server | source inspected at 5a1cf3d |
| pytest | `==8.4.2` | installed into the runtime image too (no dev/runtime split) | source inspected at 5a1cf3d |
| psycopg[binary] | `==3.2.13` | Postgres driver | source inspected at 5a1cf3d |
| requests | `==2.32.3` | File comment: "only used by scripts/load_test.py, not the app itself". BRIEF reuses it for service-to-service HTTP. | source inspected at 5a1cf3d |

Transitive versions are not pinned (no lock file); the set resolved on 2026-09-30 is in section 1. A later install may differ.

## 9. Personal names in the tree

Names are not written here. The M0 scan labels them P1-P5; the names themselves are kept only outside the repo, for the seed scrub (BRIEF section 11).

| Label | Role in the tree | STARTUP_LOG.md | tests/test_app.py | openapi.yaml | Evidence |
|---|---|---:|---:|---:|---|
| P1 | Startup persona ("business owner"); default member name and email in tests | 74 lines | 116 lines | 7 lines | source inspected at 5a1cf3d |
| P2 | Startup persona; second member name and email in tests | 49 | 31 | 0 | source inspected at 5a1cf3d |
| P3 | Startup persona; third member name in tests | 55 | 3 | 0 | source inspected at 5a1cf3d |
| P4 | Appears to be the course instructor | 7 | 0 | 0 | source inspected at 5a1cf3d |
| P5 | Named in BRIEF section 11; 0 hits at 5a1cf3d | 0 | 0 | 0 | source inspected at 5a1cf3d |

| Pattern in kept files | Where | Scrub note | Evidence |
|---|---|---|---|
| `"member": "<P1>"` / `"<P2>"` / `"<P3>"` (79 / 28 / 3 uses) | tests/test_app.py | Replace with Member A / Member B; P3 needs a third value (e.g. "member-c") | source inspected at 5a1cf3d |
| `<p1>@example.com` (21), `<p2>@example.com` (2) | tests/test_app.py; openapi.yaml 459, 723 | Replace with a@example.com / b@example.com | source inspected at 5a1cf3d |
| Mixed case `<P1>@Example.com` | tests/test_app.py 950, 977, 1046 | Tests email normalisation; keep the mixed case, e.g. `A@Example.com` | source inspected at 5a1cf3d |
| `/members/<p1>/subscribe` and case/space variants | tests/test_app.py 296, 1277-1357 | Tests name matching; the subscribe route is removed anyway | source inspected at 5a1cf3d |
| Comments naming a member | tests/test_app.py 1219, 1463 | Comments only | source inspected at 5a1cf3d |
| `example: <p1>` and prose | openapi.yaml 234, 412, 420, 432, 683 | OpenAPI examples | source inspected at 5a1cf3d |

No GitHub handles (`@handle`, `github.com/<user>`) appear in any file at 5a1cf3d. The attribution pattern of BRIEF section 15 has 0 hits in the tree; a tool name appears only in `STARTUP_LOG.md`, which is deleted before the seed (source inspected at 5a1cf3d).

## Appendix: all 154 `test_app.py` functions by area (line numbers)

Evidence for the whole appendix (names, line numbers, grouping): source inspected at 5a1cf3d. All passed in the section 1 run; each name has a `PASSED` line in the `-rA` log (check table in section 2).

- **G1 Homepage (9):** test_homepage_lists_spaces_with_availability 23, test_homepage_shows_a_booking_form_for_every_space 56, test_homepage_lists_the_upcoming_booked_times_of_a_space 68, test_homepage_says_when_a_space_has_no_bookings_coming_up 84, test_homepage_shows_the_price_as_an_hourly_rate 253, test_homepage_escapes_space_names 340, test_homepage_links_to_register 1031, test_homepage_links_to_my_bookings_only_when_logged_in 1264, test_homepage_links_to_dashboard 2063
- **G2 Booking form (6):** test_can_book_a_later_slot_while_the_space_is_booked_right_now 91, test_booking_an_overlapping_slot_shows_the_already_booked_message 102, test_booking_through_the_form_makes_the_space_unavailable 113, test_form_times_are_read_as_bangkok_time 303, test_form_booking_a_taken_slot_shows_the_error 320, test_form_without_times_shows_an_error 332
- **G3 Confirmation page (7):** test_book_pay_unlock_all_the_way_through_the_browser 132, test_confirmation_page_unlock_without_paying_shows_the_error 161, test_confirmation_page_for_unknown_booking_returns_404 171, test_confirmation_page_shows_times_in_bangkok_time 179, test_confirmation_page_shows_the_total_before_and_after_paying 195, test_confirmation_page_pay_form_has_card_fields_and_shows_last4_once_paid 788, test_confirmation_page_pay_with_an_invalid_card_shows_the_error 802
- **G4 Pricing (7):** test_three_hours_cost_three_times_one_hour 208, test_half_an_hour_costs_half_the_hourly_rate 225, test_an_uneven_duration_is_rounded_to_whole_cents 238, test_booking_responses_include_the_amount_charged 264, test_a_price_change_after_booking_does_not_change_the_amount_shown 282, test_revenue_stays_the_same_when_the_space_price_changes_later 1544, test_changing_a_price_with_patch_only_affects_later_bookings 2004
- **G5 Spaces CRUD (21):** test_list_spaces_returns_the_seed_space 365, test_create_space_adds_a_new_space 383, test_create_space_with_a_price_stores_it 407, test_create_space_with_negative_price_is_rejected 423, test_create_space_with_a_boolean_price_is_rejected 436, test_create_space_without_capacity_is_rejected 450, test_create_space_with_empty_name_is_rejected 458, test_create_space_with_invalid_capacity_is_rejected 467, test_create_space_trims_spaces_around_the_name 483, test_delete_unbooked_space_removes_it 1716, test_delete_space_with_bookings_is_rejected 1728, test_delete_unknown_space_returns_404 1739, test_get_space_returns_its_data 1747, test_get_unknown_space_returns_404 1761, test_update_space_name_shows_up_in_list 1935, test_update_space_capacity_only_keeps_the_name 1951, test_update_space_keeps_its_bookings 1960, test_update_space_price_shows_up_in_list 1970, test_update_space_name_only_keeps_the_price 1993, test_update_unknown_space_returns_404 2027, test_update_space_with_invalid_values_is_rejected 2035
- **G6 Availability (7):** test_space_booked_right_now_shows_as_unavailable 594, test_space_booked_only_later_is_still_available_now 604, test_list_spaces_for_a_time_window_reflects_bookings_in_that_window 1769, test_availability_window_replaces_the_right_now_check 1782, test_availability_window_touching_a_booking_is_still_free 1792, test_get_space_for_a_time_window_reflects_bookings_in_that_window 1805, test_availability_window_must_have_both_times_in_order 1816
- **G7 Booking API (18):** test_create_booking_for_existing_space_succeeds 493, test_create_booking_for_unknown_space_returns_404 514, test_create_booking_without_times_is_rejected 525, test_create_booking_ending_before_it_starts_is_rejected 535, test_overlapping_booking_is_rejected 545, test_concurrent_bookings_for_the_same_slot_only_one_succeeds 556, test_back_to_back_bookings_are_allowed 584, test_find_booking_returns_the_booking 614, test_booking_records_when_it_was_made 636, test_find_unknown_booking_returns_404 656, test_list_bookings_for_a_space_returns_all_of_them 1839, test_list_bookings_for_space_without_bookings_is_empty 1856, test_list_bookings_for_unknown_space_returns_404 1864, test_booking_more_people_than_capacity_is_rejected 1872, test_booking_up_to_capacity_is_allowed 1887, test_booking_with_invalid_party_size_is_rejected 1898, test_list_bookings_returns_bookings_across_all_spaces 1911, test_list_bookings_when_there_are_none_is_empty 1927
- **G8 Cancel (2):** test_cancel_booking_makes_space_available_again 664, test_cancel_unknown_booking_returns_404 681
- **G9 Mock payment (13):** test_pay_flips_a_booking_to_paid 689, test_paying_twice_is_still_paid 702, test_pay_unknown_booking_returns_404 714, test_paying_with_a_valid_card_succeeds_and_shows_only_last4 722, test_paying_with_a_missing_card_field_is_rejected_and_leaves_it_unpaid 737, test_paying_with_a_badly_formatted_card_is_rejected 752, test_paying_with_an_expired_card_is_rejected 774, test_paying_an_already_paid_booking_again_is_still_a_no_op 814, test_failed_payment_leaves_the_booking_unpaid_and_unlock_returns_402 828, test_failed_payment_brings_in_no_revenue_and_can_be_retried 846, test_forcing_a_failure_on_an_unknown_booking_returns_404 872, test_forcing_a_failure_on_a_paid_booking_leaves_it_paid 880, test_paying_twice_only_counts_revenue_once 894
- **G10 Unlock (3):** test_unlock_before_paying_is_rejected 913, test_unlock_a_paid_booking_returns_an_access_code 924, test_unlock_unknown_booking_returns_404 938
- **G11 Accounts (15):** test_registering_creates_an_account 946, test_registering_does_not_store_the_plain_password 959, test_registering_with_a_duplicate_email_is_rejected 971, test_registering_with_a_bad_email_is_rejected 983, test_registering_with_a_short_password_is_rejected 994, test_register_form_creates_an_account_and_redirects_with_a_message 1010, test_register_form_with_invalid_input_shows_the_error 1021, test_login_with_the_right_password_succeeds 1041, test_login_with_the_wrong_password_is_rejected 1052, test_login_with_an_unknown_email_gives_the_identical_error 1063, test_logout_ends_the_session 1079, test_logout_when_not_logged_in_is_a_no_op 1091, test_login_form_logs_in_and_redirects_to_the_homepage 1098, test_login_form_with_wrong_password_shows_the_error 1110, test_logout_button_on_the_homepage_actually_logs_out 1121
- **G12 Account-linked bookings (10):** test_a_booking_made_while_logged_in_is_linked_to_the_account 1134, test_a_guest_booking_has_no_user_id 1146, test_logging_out_before_booking_leaves_it_unlinked 1155, test_a_form_booking_while_logged_in_is_linked_to_the_account 1167, test_user_id_stays_on_the_booking_through_pay_and_list 1176, test_logged_out_visitors_are_sent_to_the_login_page 1193, test_my_bookings_page_lists_only_the_logged_in_users_bookings 1201, test_my_bookings_page_shows_space_time_price_and_paid_status 1221, test_my_bookings_link_to_the_confirmation_page_for_the_unlock_code 1243, test_my_bookings_page_when_there_are_none_says_so 1255
- **G13 Subscriptions (9):** test_a_subscribers_booking_shows_zero_amount_on_the_confirmation_page 293, test_subscribing_returns_an_active_subscription 1274, test_subscribing_twice_keeps_the_original_start 1285, test_a_blank_member_name_cannot_subscribe 1294, test_a_subscribed_members_booking_is_paid_on_creation 1302, test_a_member_without_a_subscription_still_pays_once 1315, test_subscription_matches_the_member_name_ignoring_case_and_spaces 1327, test_a_subscribers_booking_adds_no_per_booking_revenue 1341, test_form_booking_by_a_subscriber_is_paid 1355
- **G14 Metrics JSON (15):** test_metrics_reports_spaces_bookings_and_members 1363, test_metrics_splits_paid_and_unpaid_bookings 1381, test_metrics_with_no_bookings_reports_zero_for_each_count 1396, test_metrics_reports_revenue_from_paid_bookings 1405, test_utilization_over_the_next_7_days 1426, test_utilization_ignores_bookings_outside_the_next_7_days 1436, test_utilization_is_zero_with_no_spaces 1444, test_repeat_member_rate 1453, test_repeat_member_rate_is_zero_with_no_bookings 1465, test_payment_conversion 1472, test_payment_conversion_is_zero_with_no_bookings 1484, test_average_revenue_per_paid_booking 1491, test_average_revenue_per_paid_booking_is_zero_with_no_paid_bookings 1509, test_revenue_by_space 1516, test_revenue_by_space_includes_a_space_with_no_bookings 1535
- **G15 Dashboard (8):** test_dashboard_shows_current_metrics 1617, test_dashboard_shows_paid_and_unpaid_bookings_separately 1638, test_dashboard_with_no_bookings_shows_zero_paid_and_unpaid 1657, test_dashboard_describes_the_product_and_notes_the_data_source 1665, test_dashboard_shows_the_new_investor_metrics 1673, test_dashboard_shows_a_revenue_bar_for_each_space 1691, test_dashboard_with_no_spaces_shows_no_bar_chart_crash 1707, test_dashboard_links_back_to_homepage 2072
- **G16 Health and startup (4):** test_health_reports_running_revision 353, test_startup_fills_in_the_amount_on_bookings_made_before_the_column_existed 1570, test_health_reports_error_when_database_is_unreachable 1594, test_startup_fails_fast_with_a_clear_message_for_a_bad_database_url 1607
