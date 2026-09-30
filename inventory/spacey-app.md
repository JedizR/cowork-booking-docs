# Spacey application structure at 5a1cf3d

Config, connection handling, time handling, every helper, Jinja filters, metrics, templates and CSS. Nothing here was run unless the row says "test run". All rows are Observed Spacey behaviour.

## BRIEF section 4 Spacey facts, checked

| BRIEF claim | Result | Where | Evidence |
|---|---|---|---|
| "160 tests passed on Python 3.11.7. Re-run in M0 on 3.12." | On 3.12.11: 160 passed (154 in `tests/test_app.py`, 6 in `tests/test_purchase.py`), in two runs. The 3.11.7 figure is BRIEF prior research, not re-run. | [spacey-tests-infra.md](spacey-tests-infra.md) section 1 | test run at 5a1cf3d |
| `app.py` holds almost everything | Confirmed: config, DDL, helpers and all 27 routes in 1053 lines | this file | source inspected at 5a1cf3d |
| `purchase.py` holds `calculate_booking_price_cents` | Confirmed: 15 lines, that function only; added by `bb39ee7` | purchase.py:6-15 | source inspected at 5a1cf3d |
| Tables `spaces`, `bookings` (`paid` and `card_last4` on the row), `subscriptions` keyed by typed name, `users` | Confirmed | [spacey-schema.md](spacey-schema.md) | source inspected at 5a1cf3d |
| btree_gist `no_overlapping_bookings` EXCLUDE | Confirmed | app.py:122-139 | source inspected at 5a1cf3d |
| One shared autocommit connection | Confirmed | app.py:25, 387 | source inspected at 5a1cf3d |
| DDL runs at every start | Confirmed (and at import) | app.py:23-140, 1053 | source inspected at 5a1cf3d |
| 1 gunicorn sync worker | Confirmed: no `-w` in Dockerfile, no `workers` in gunicorn.conf.py, so gunicorn's default of 1 applies. `LOAD_TEST.md` wrongly says the Dockerfile uses `-w 2`. | Dockerfile:17, gunicorn.conf.py | source inspected at 5a1cf3d |
| Dockerfile `python:3.12-slim` | Confirmed | Dockerfile:1 | source inspected at 5a1cf3d |
| CI `.github/workflows/delivery.yml`: pytest, then ghcr build, then Nomad deploy | Confirmed (build and deploy on push to main only) | [spacey-tests-infra.md](spacey-tests-infra.md) section 5 | source inspected at 5a1cf3d |

## Files

| File | Lines | Role | Evidence |
|---|---|---|---|
| app.py | 1053 | Config, DDL, helpers, all 27 routes, `app = create_app()` at 1053 | source inspected at 5a1cf3d |
| purchase.py | 15 | `calculate_booking_price_cents` only (from `bb39ee7` "extract booking price calculation into Purchase", merged by `5a1cf3d`) | source inspected at 5a1cf3d |
| openapi.yaml | 732 | JSON API contract, 18 operations, OpenAPI 3.0.3 | source inspected at 5a1cf3d |
| templates/*.html | 8 files, 177 lines | Jinja pages, all extend `base.html` | source inspected at 5a1cf3d |
| static/style.css | 162 | One stylesheet, CSS variables on `:root` | source inspected at 5a1cf3d |
| gunicorn.conf.py | 5 | Access log to stdout, path without query string | source inspected at 5a1cf3d |
| Dockerfile | 17 | `python:3.12-slim`; copies app.py, purchase.py, gunicorn.conf.py, templates, static; `CMD gunicorn --bind 0.0.0.0:8000 app:app` | source inspected at 5a1cf3d |

The full file list (28 files) is in [keep-delete.md](keep-delete.md).

## Config and env vars

| Name | Read at | Default | Used for | Evidence |
|---|---|---|---|---|
| `DATABASE_URL` | app.py:14-16 (at import) | `postgresql://spacey:spacey@localhost:5432/spacey` | `create_app(database_url=DATABASE_URL)` (380) | source inspected at 5a1cf3d |
| `SECRET_KEY` | app.py:20 | `dev-secret-key-not-for-production` | `app.secret_key` (386), signs the cookie session | source inspected at 5a1cf3d |
| `RESET_DB_ON_START` | app.py:383 | `"false"` (true only if the lower-cased value is `"true"`) | `reset_tables` (359) | source inspected at 5a1cf3d |
| `APP_REVISION` | app.py:551 | `"local"` | `/health` `revision` | source inspected at 5a1cf3d |
| Gunicorn workers | not set (Dockerfile:17, gunicorn.conf.py) | gunicorn default: 1 sync worker | Serving | source inspected at 5a1cf3d |
| Gunicorn access log | gunicorn.conf.py:4-5 | `accesslog = "-"`; format uses `%(U)s` (path without query) and drops the referer, because "the door access code arrives as ?code=..." | Query-string scrubbing, kept by every service (BRIEF section 10) | source inspected at 5a1cf3d |
| compose.yaml | compose.yaml:1-23 | db `postgres:16` on host 5433; app `APP_REVISION=compose`, `DATABASE_URL=...@db:5432/...`; no `SECRET_KEY` | Local stack | source inspected at 5a1cf3d |
| Nomad job | deploy/startup-app.nomad.hcl:56-67 | Sets only `APP_REVISION` and `DATABASE_URL`; no `SECRET_KEY` | Deploy | source inspected at 5a1cf3d |

No other Flask config is set: no `PERMANENT_SESSION_LIFETIME`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`, `MAX_CONTENT_LENGTH`. The app default `DATABASE_URL` uses port 5432, while compose publishes the DB on host port 5433.

## DB connection handling

| Aspect | Code | Behaviour | Evidence |
|---|---|---|---|
| Connection | `get_connection` app.py:23-25 | One `psycopg.connect(..., row_factory=dict_row, autocommit=True)` per app | source inspected at 5a1cf3d |
| Sharing | app.py:387 `app.db` | Every route uses `with app.db.cursor() as cur:`; no pool, no per-request connection | source inspected at 5a1cf3d |
| Transactions | none | Autocommit: every statement commits alone; no `BEGIN`, no `SELECT ... FOR UPDATE` anywhere | source inspected at 5a1cf3d |
| Fail fast | app.py:26-34 | `OperationalError` at start becomes `SystemExit` with a clear message | source inspected at 5a1cf3d |
| Fail fast, test | `test_startup_fails_fast_with_a_clear_message_for_a_bad_database_url` expects `SystemExit` naming the URL and "docker compose up db -d" | tests/test_app.py:1607 | source inspected at 5a1cf3d |
| Fail fast, run | That test `PASSED` in the `-rA` run | [spacey-tests-infra.md](spacey-tests-infra.md) section 1 | test run at 5a1cf3d |
| Reconnect | none | A dropped connection is never re-opened; `/health` (541-552) returns 503 on `psycopg.Error` | source inspected at 5a1cf3d |
| Errors mapped | app.py:8, 461, 766 | Only `UniqueViolation` (register) and `ExclusionViolation` / `DeadlockDetected` (booking insert) are caught | source inspected at 5a1cf3d |

## Time handling

| Item | Behaviour | Evidence |
|---|---|---|
| `LOCAL_TZ` (app.py:188) | `timezone(timedelta(hours=7))`, fixed UTC+7 ("Bangkok, no daylight saving"); no `zoneinfo` | source inspected at 5a1cf3d |
| JSON input | `parse_time` (143-151) needs an explicit offset; returns None for a naive time | source inspected at 5a1cf3d |
| Form input | `parse_form_time` (191-200) treats a naive time as `LOCAL_TZ` | source inspected at 5a1cf3d |
| Form input, test | `test_form_times_are_read_as_bangkok_time` (303) asserts that form input 2026-09-25T09:00 comes back as `2026-09-25T02:00:00+00:00` | source inspected at 5a1cf3d |
| Form input, run | That test `PASSED` in the `-rA` run ([spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |
| JSON output | UTC ISO strings (`booking_to_json` 275-281) | source inspected at 5a1cf3d |
| HTML output | Bangkok via the `local_time` filter | source inspected at 5a1cf3d |
| "Now" | Postgres `now()` in SQL (175, 311, 420, 427) and `datetime.now(timezone.utc)` in `validate_card` (250). No injectable clock (needed by D27). | source inspected at 5a1cf3d |

## Module-level helpers (app.py)

| Helper | Line | One-line behaviour | Evidence |
|---|---|---|---|
| `get_connection(database_url)` | 23 | Connect (fail fast), run all DDL, return the connection | source inspected at 5a1cf3d |
| `parse_time(value)` | 143 | ISO 8601 via `datetime.fromisoformat`; None if invalid or naive | source inspected at 5a1cf3d |
| `parse_window(args)` | 154 | `?start_time&end_time` to `(window, error)`; both or neither; end after start | source inspected at 5a1cf3d |
| `booked_space_ids(cur, window)` | 170 | Space ids with any booking overlapping the window, or overlapping `now()` if no window; ignores `paid` | source inspected at 5a1cf3d |
| `LOCAL_TZ` | 188 | Fixed UTC+7 | source inspected at 5a1cf3d |
| `parse_form_time(value)` | 191 | Like `parse_time`, but naive becomes `LOCAL_TZ` | source inspected at 5a1cf3d |
| `is_valid_name(name)` | 203 | Non-blank string (used for spaces only, not booking `member`) | source inspected at 5a1cf3d |
| `is_valid_capacity(capacity)` | 207 | int, not bool, >= 1; no upper bound | source inspected at 5a1cf3d |
| `is_valid_price(price)` | 216 | int, not bool, >= 0; no upper bound | source inspected at 5a1cf3d |
| `EMAIL_RE` | 221 | `^[^@\s]+@[^@\s]+\.[^@\s]+$` | source inspected at 5a1cf3d |
| `is_valid_email(email)` | 224 | String matching `EMAIL_RE` after strip | source inspected at 5a1cf3d |
| `is_valid_password(password)` | 228 | String, length >= 8 | source inspected at 5a1cf3d |
| `CARD_NUMBER_RE` | 232 | `^\d{13,19}$` | source inspected at 5a1cf3d |
| `CVC_RE` | 233 | `^\d{3,4}$` | source inspected at 5a1cf3d |
| `EXPIRY_RE` | 234 | `^(0[1-9]\|1[0-2])/(\d{2})$` | source inspected at 5a1cf3d |
| `validate_card(card_number, expiry, cvc)` | 237 | Returns the first error in order: number, cvc, expiry format, expired (vs current UTC month); else None. No Luhn check. | source inspected at 5a1cf3d |
| `member_key(name)` | 256 | `name.strip().lower()` | source inspected at 5a1cf3d |
| `is_subscribed(cur, member)` | 260 | True if an active `subscriptions` row has `member_key(member)`; False for non-strings | source inspected at 5a1cf3d |
| `local_time(value)` | 270 | Bangkok `YYYY-MM-DD HH:MM` | source inspected at 5a1cf3d |
| `booking_to_json(row)` | 275 | Row dict with `start_time`, `end_time`, `created_at` as UTC ISO strings | source inspected at 5a1cf3d |
| `compute_metrics(cur)` | 283 | Returns the metric fields below | source inspected at 5a1cf3d |
| `reset_tables(conn)` | 359 | TRUNCATE all four tables, restart ids | source inspected at 5a1cf3d |
| `seed_starter_space(conn)` | 369 | Insert "Founders Desk" (capacity 1, 2500 cents/h) if there are no spaces | source inspected at 5a1cf3d |
| `create_app(database_url, reset_on_start)` | 379 | Build the Flask app, connect, optional reset, seed, filters, routes | source inspected at 5a1cf3d |
| `app` | 1053 | Module-level `create_app()` | source inspected at 5a1cf3d |

## Helpers nested in `create_app`

| Helper | Line | One-line behaviour | Evidence |
|---|---|---|---|
| `register_user(email, password)` | 443 | Validate, lower-case email, hash password, INSERT; 409 on duplicate email | source inspected at 5a1cf3d |
| `login_user(email, password)` | 489 | Same 401 for unknown email or wrong password; sets `session["user_id"]` | source inspected at 5a1cf3d |
| `inject_current_user` | 398-411 | `@app.context_processor`: adds `current_user_email` to every template; pops a stale `user_id` if the user row is gone | source inspected at 5a1cf3d |
| `book_space(...)` | 700 | Space exists, end > start, party size 1..capacity, overlap pre-check, subscription check, INSERT (paid = subscribed; amount 0 if subscribed, else prorated), `user_id` from session | source inspected at 5a1cf3d |
| `mark_booking_paid(...)` | 932 | SELECT booking; already paid gives a 200 no-op; `validate_card`; `force_failure` gives 402; UPDATE `paid=TRUE, card_last4` | source inspected at 5a1cf3d |
| `issue_access_code(booking_id)` | 970 | 404, or 402 unless paid; returns `secrets.token_hex(4)`; stores nothing | source inspected at 5a1cf3d |

## purchase.py

| Helper | Line | One-line behaviour | Evidence |
|---|---|---|---|
| `calculate_booking_price_cents(hourly_rate_cents, start_time, end_time)` | purchase.py:6-15 | `seconds = int((end - start).total_seconds())`; returns `(rate * seconds + 1800) // 3600`: hourly rate prorated, half cent rounded up. Docstring: "The caller supplies a validated interval and handles subscription coverage." | source inspected at 5a1cf3d |
| same, test | tests/test_purchase.py | One parametrized test; rows (rate, seconds, expected): (1500,1800,750), (1000,1200,333), (100,18,1), (100,17,0), (3600,1.9,1), (0,3600,0) | source inspected at 5a1cf3d |
| same, run | tests/test_purchase.py | `test_booking_price_examples[1500-1800-750]`, `[1000-1200-333]`, `[100-18-1]`, `[100-17-0]`, `[3600-1.9-1]`, `[0-3600-0]`: each `PASSED` in the `-rA` run ([spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |

## Jinja filters and autoescape

| Name | Defined / registered | Behaviour | Evidence |
|---|---|---|---|
| `local_time` | def 270-272, registered 394 | `value.astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M")` | source inspected at 5a1cf3d |
| `money` | lambda at 395 | `f"${cents / 100:.2f}"`: dollars, 2 decimals. The target needs THB (D1). | source inspected at 5a1cf3d |
| `percent` | lambda at 396 | `f"{share * 100:.1f}%"` (dashboard only) | source inspected at 5a1cf3d |
| Autoescape | comment at 392-393 | Jinja default autoescape for `.html`; no `\|safe` in any template | source inspected at 5a1cf3d |

## Metrics (`compute_metrics`, app.py:283-357)

| Field | Query / formula | Line | Evidence |
|---|---|---|---|
| spaces | `COUNT(*) FROM spaces` | 284-285 | source inspected at 5a1cf3d |
| bookings, paid_bookings, unpaid_bookings | `COUNT(*)`, `FILTER (WHERE paid)`, `FILTER (WHERE NOT paid)` | 287-293 | source inspected at 5a1cf3d |
| members | `COUNT(DISTINCT member)` (free-text names, exact match) | 295-296 | source inspected at 5a1cf3d |
| revenue_cents | `SUM(amount_cents) WHERE paid` (surviving rows only) | 298-301 | source inspected at 5a1cf3d |
| utilization | booked hours in the next 7 days (clipped) / (spaces x 7 x 24); counts unpaid too | 306-315 | source inspected at 5a1cf3d |
| repeat_member_rate | members with > 1 booking / members | 317-323 | source inspected at 5a1cf3d |
| payment_conversion | paid / total (subscriber bookings count as paid) | 325-329 | source inspected at 5a1cf3d |
| avg_revenue_cents_per_paid_booking | `round(revenue / paid)` | 331-335 | source inspected at 5a1cf3d |
| revenue_by_space | per space `SUM(amount_cents) FILTER (WHERE paid)`, LEFT JOIN | 337-343 | source inspected at 5a1cf3d |
| dashboard bars | width = revenue / top revenue x 100 | 1039-1048 | source inspected at 5a1cf3d |

## Templates

| Template | Rendered by (route, app.py line) | Context vars | Forms (method to action) | Evidence |
|---|---|---|---|---|
| base.html (24 lines) | Parent of all | `current_user_email` | POST `/logout` (line 17); nav link "Business metrics" for every visitor (12) | source inspected at 5a1cf3d |
| index.html (39) | GET `/` (435) | `spaces`, `booked_ids`, `upcoming`, `error` | POST `/spaces/<id>/book` with `member`, `start_time`, `end_time` (`datetime-local`, no `step`); no party size (30-35) | source inspected at 5a1cf3d |
| register.html (14) | GET `/register` (469) | `registered` (unused), `error` | POST `/register` (8-12) | source inspected at 5a1cf3d |
| login.html (17) | GET `/login` (513) | `error`, `message` | POST `/login` (11-15) | source inspected at 5a1cf3d |
| confirmation.html (27) | GET `/bookings/<id>/confirmation` (829) | `booking`, `code`, `error` | POST `.../confirmation/unlock` (9-11); POST `.../confirmation/pay` (14-19) | source inspected at 5a1cf3d |
| booking_not_found.html (5) | GET `/bookings/<id>/confirmation` 404 (827) | none | none | source inspected at 5a1cf3d |
| my_bookings.html (19) | GET `/bookings/mine` (889) | `bookings` | none (links to confirmation) | source inspected at 5a1cf3d |
| dashboard.html (32) | GET `/dashboard` (1050) | `metrics`, `bars` | none; inline `style="width: N%"` (24) | source inspected at 5a1cf3d |

### confirmation.html parts

| Part | Lines | Content | BRIEF section 10 destination | Evidence |
|---|---|---|---|---|
| Booking header | 1-6, 26 | Title `Booking #id`, `h1`, `space_name for member`, start/end with `local_time` "(Bangkok time)", back link | Purchase | source inspected at 5a1cf3d |
| Paid status line | 7-8 | "Paid. Total: amount (card ending last4)" | Status to Purchase; card detail to Payment | source inspected at 5a1cf3d |
| Unlock button | 9-11 | POST `/bookings/<id>/confirmation/unlock` | Access (ticket page) | source inspected at 5a1cf3d |
| Payment form | 12-19 | "Not paid yet - total ..., pay to get your access code."; inputs `card_number`, `expiry`, `cvc`; POST `.../confirmation/pay` | Payment (hosted page) | source inspected at 5a1cf3d |
| Access code display | 21-22 | `{% if code %}` "Your access code: <strong>{{ code }}</strong>" from `?code=` | Access (ticket page), rewritten to show the stored code | source inspected at 5a1cf3d |
| Error message | 23-24 | `{% elif error %}` `<p class="message">` from `?error=` | Replaced by `flash()` (D28) | source inspected at 5a1cf3d |

## static/style.css

| Item | Lines | Note | Evidence |
|---|---|---|---|
| Tokens | 4-12 | `--ink --muted --line --accent --ok --busy --bg`; light only, no dark mode, no media queries | source inspected at 5a1cf3d |
| Layout | 14-36 | `body` max-width 52rem, system font | source inspected at 5a1cf3d |
| Nav | 38-63 | `.site-nav`, `.brand`, `.spacer`, inline logout form | source inspected at 5a1cf3d |
| Messages | 65-76 | `.message`, `.hint` | source inspected at 5a1cf3d |
| Lists / status | 78-100 | `.list`, `.status-free`, `.status-busy` | source inspected at 5a1cf3d |
| Forms | 102-130 | `form` flex-wrap, `input`, `button` | source inspected at 5a1cf3d |
| Dashboard | 132-162 | `.cards`, `.bar-row`, `.bar-label`, `.bar`; `.bar-value` (dashboard.html:25) has no rule | source inspected at 5a1cf3d |

## "spacey" strings on surfaces the section 15 branding scan checks

Files deleted before the seed are not listed.

| File:line | String | Evidence |
|---|---|---|
| templates/base.html:6, :11 | `<title>Spacey - ...`, nav brand `Spacey` | source inspected at 5a1cf3d |
| templates/dashboard.html:4, :5 | `<h1>Spacey - Business Metrics</h1>`, "Spacey is a space booking system ..." | source inspected at 5a1cf3d |
| openapi.yaml:3 | `title: Spacey API` | source inspected at 5a1cf3d |
| compose.yaml:5-7, :17 | DB user, password and name `spacey`, and `DATABASE_URL` | source inspected at 5a1cf3d |
| app.py:15 | default `DATABASE_URL` | source inspected at 5a1cf3d |
| tests/test_app.py:1608 | `bad_url = "postgresql://spacey:spacey@localhost:1/spacey"` (the scan's `'*.py'` pathspec matches `tests/`) | source inspected at 5a1cf3d |
| README.md:19, :20, :53 | `DATABASE_URL` examples | source inspected at 5a1cf3d |
