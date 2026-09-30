# Spacey schema at 5a1cf3d

All DDL lives in `app.py`. No database was inspected; notes marked "not run" are PostgreSQL semantics read from the DDL. The test suite does create this schema on a real Postgres 16 and passes (see [spacey-tests-infra.md](spacey-tests-infra.md)), which shows the DDL applies cleanly, but no row below was checked against a live catalog.

## Where DDL runs

| What | Where | Behaviour | Evidence |
|---|---|---|---|
| All DDL + backfill | `get_connection()` app.py:23-140 | Runs on the one autocommit connection right after connect, in a fixed order, every time it is called. Each statement commits alone: no wrapping transaction, no migration/version table. | source inspected at 5a1cf3d |
| Caller | `create_app()` app.py:387 `app.db = get_connection(database_url)` | Every app construction. | source inspected at 5a1cf3d |
| Import side effect | app.py:1053 `app = create_app()` | Importing `app` (gunicorn `app:app`, and the tests) connects and runs all DDL at import time. | source inspected at 5a1cf3d |
| Opt-in wipe | `reset_tables()` app.py:359-367 | `TRUNCATE bookings, spaces, subscriptions, users RESTART IDENTITY CASCADE` when `RESET_DB_ON_START=true` (app.py:383) or `create_app(reset_on_start=True)`. | source inspected at 5a1cf3d |
| Seed | `seed_starter_space()` app.py:369-377 | If `spaces` is empty, inserts `("Founders Desk", 1, 2500)`; comment says "$25.00 per hour". Runs on every start (app.py:390). | source inspected at 5a1cf3d |
| Connect failure | app.py:24-34 | `psycopg.OperationalError` becomes `SystemExit` with the URL and a `docker compose up db -d` hint (fail fast). | source inspected at 5a1cf3d |

## DDL in execution order

| Order | app.py lines | Statement | Evidence |
|---|---|---|---|
| 1 | 36-44 | `CREATE TABLE IF NOT EXISTS spaces (...)` | source inspected at 5a1cf3d |
| 2 | 45-48 | `ALTER TABLE spaces ADD COLUMN IF NOT EXISTS price_cents INTEGER NOT NULL DEFAULT 0` | source inspected at 5a1cf3d |
| 3 | 49-58 | `CREATE TABLE IF NOT EXISTS bookings (...)` | source inspected at 5a1cf3d |
| 4 | 59-68 | `CREATE TABLE IF NOT EXISTS subscriptions (...)` | source inspected at 5a1cf3d |
| 5 | 69-80 | `CREATE TABLE IF NOT EXISTS users (...)` | source inspected at 5a1cf3d |
| 6 | 83-87 | `ALTER TABLE bookings ADD COLUMN IF NOT EXISTS start_time TIMESTAMPTZ, ADD COLUMN IF NOT EXISTS end_time TIMESTAMPTZ` | source inspected at 5a1cf3d |
| 7 | 88-91 | `ALTER TABLE bookings ADD COLUMN IF NOT EXISTS amount_cents INTEGER` | source inspected at 5a1cf3d |
| 8 | 92-98 | `ALTER TABLE bookings ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users (id)` | source inspected at 5a1cf3d |
| 9 | 99-103 | `ALTER TABLE bookings ADD COLUMN IF NOT EXISTS card_last4 TEXT` | source inspected at 5a1cf3d |
| 10 | 104-111 | `ALTER TABLE bookings ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()` | source inspected at 5a1cf3d |
| 11 (DML) | 112-117 | `UPDATE bookings SET amount_cents = s.price_cents FROM spaces s WHERE s.id = bookings.space_id AND bookings.amount_cents IS NULL` (backfill on every start; uses the current rate, not the duration) | source inspected at 5a1cf3d |
| 12 | 122 | `CREATE EXTENSION IF NOT EXISTS btree_gist` | source inspected at 5a1cf3d |
| 13 | 123-139 | `DO $$ ... IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'no_overlapping_bookings') THEN ALTER TABLE bookings ADD CONSTRAINT no_overlapping_bookings EXCLUDE USING gist (space_id WITH =, tstzrange(start_time, end_time) WITH &&); END IF; END $$;` | source inspected at 5a1cf3d |

`grep -niE 'create index|check \(|on delete' app.py` returns nothing: no explicit index, no CHECK, no ON DELETE clause.

## Tables

### spaces

| Column | Type | Default | Constraints | Added at | Evidence |
|---|---|---|---|---|---|
| id | SERIAL (INTEGER + sequence) | nextval | PRIMARY KEY | app.py:39 | source inspected at 5a1cf3d |
| name | TEXT | none | NOT NULL | app.py:40 | source inspected at 5a1cf3d |
| capacity | INTEGER | none | NOT NULL; `>= 1` only in app (`is_valid_capacity` 207), no upper bound | app.py:41 | source inspected at 5a1cf3d |
| price_cents | INTEGER | 0 | NOT NULL; `>= 0` only in app (`is_valid_price` 216), no upper bound. Meaning: hourly rate in cents (openapi.yaml:667-670; purchase.py:6-15) | app.py:46-47 (ALTER) | source inspected at 5a1cf3d |

### bookings

| Column | Type | Default | Constraints | Added at | Evidence |
|---|---|---|---|---|---|
| id | SERIAL | nextval | PRIMARY KEY (sequential, easy to enumerate) | app.py:52 | source inspected at 5a1cf3d |
| space_id | INTEGER | none | NOT NULL, `REFERENCES spaces (id)` (no ON DELETE, so NO ACTION) | app.py:53 | source inspected at 5a1cf3d |
| member | TEXT | none | NOT NULL; free text typed by the booker, "guest" if blank | app.py:54 | source inspected at 5a1cf3d |
| paid | BOOLEAN | none | NOT NULL; TRUE after card payment or at creation for a subscriber | app.py:55 | source inspected at 5a1cf3d |
| start_time | TIMESTAMPTZ | none | nullable | app.py:85 (ALTER) | source inspected at 5a1cf3d |
| end_time | TIMESTAMPTZ | none | nullable; no DB `CHECK end_time > start_time` | app.py:86 (ALTER) | source inspected at 5a1cf3d |
| amount_cents | INTEGER | none | nullable; backfilled from `spaces.price_cents` for NULL rows (app.py:113-117) | app.py:90 (ALTER) | source inspected at 5a1cf3d |
| user_id | INTEGER | none | nullable, `REFERENCES users (id)`; NULL = guest | app.py:96-97 (ALTER) | source inspected at 5a1cf3d |
| card_last4 | TEXT | none | nullable; NULL until paid by card | app.py:102 (ALTER) | source inspected at 5a1cf3d |
| created_at | TIMESTAMPTZ | now() | NOT NULL | app.py:109-110 (ALTER) | source inspected at 5a1cf3d |
| (constraint) `no_overlapping_bookings` | EXCLUDE USING gist | n/a | `space_id WITH =`, `tstzrange(start_time, end_time) WITH &&`; applies to every row, paid or unpaid; no status filter (there is no status column) | app.py:130-135 | source inspected at 5a1cf3d |

| Not stored | Why | Evidence |
|---|---|---|
| party_size | Accepted and checked on the JSON path, never stored: `book_space` validates it (app.py:715-727; JSON default 1 at app.py:791, form hard-codes 1 at app.py:806), but `bookings` has no party_size column and the INSERT (app.py:746-748) lists only space_id, member, paid, start_time, end_time, amount_cents and user_id, so the value is discarded | source inspected at 5a1cf3d |

Notes (not run): `tstzrange` default bounds are `[)`, so back-to-back bookings do not clash (matches the app comment at 729-730 and what `test_back_to_back_bookings_are_allowed` asserts; that test passed in the [spacey-tests-infra.md](spacey-tests-infra.md) section 1 runs). A row with NULL `start_time` or `end_time` would give an unbounded range that overlaps everything on that space; the app never inserts NULLs, but the columns allow it.

### subscriptions

| Column | Type | Default | Constraints | Added at | Evidence |
|---|---|---|---|---|---|
| member | TEXT | none | PRIMARY KEY; value is `member_key(name)` = trimmed lower-case typed name | app.py:63 | source inspected at 5a1cf3d |
| active | BOOLEAN | TRUE | NOT NULL; no code path ever sets it FALSE | app.py:64 | source inspected at 5a1cf3d |
| started_at | TIMESTAMPTZ | now() | NOT NULL; unchanged on re-subscribe | app.py:65 | source inspected at 5a1cf3d |

No link to `users`. No price, plan or end date.

### users

| Column | Type | Default | Constraints | Added at | Evidence |
|---|---|---|---|---|---|
| id | SERIAL | nextval | PRIMARY KEY | app.py:74 | source inspected at 5a1cf3d |
| email | TEXT | none | NOT NULL UNIQUE (stored trimmed lower-case by the app, app.py:451) | app.py:75 | source inspected at 5a1cf3d |
| password_hash | TEXT | none | NOT NULL; werkzeug `generate_password_hash` | app.py:76 | source inspected at 5a1cf3d |
| created_at | TIMESTAMPTZ | now() | NOT NULL | app.py:77 | source inspected at 5a1cf3d |

No display name, no role or operator flag, no session table.

## Indexes and extensions

| Object | Kind | Source | Evidence |
|---|---|---|---|
| btree_gist | Extension (needs a role allowed to create extensions) | app.py:122 | source inspected at 5a1cf3d |
| spaces, bookings, users, subscriptions primary keys | Implicit unique btree indexes | app.py:39, 52, 63, 74 | source inspected at 5a1cf3d |
| users.email | Implicit unique btree index from UNIQUE | app.py:75 | source inspected at 5a1cf3d |
| no_overlapping_bookings | GiST index backing the EXCLUDE constraint | app.py:130-135 | source inspected at 5a1cf3d |
| bookings.user_id, bookings.created_at | No index (queried at app.py:884 and by metrics) | n/a | source inspected at 5a1cf3d |

## Columns that are missing for the target (for M1/M4)

| Missing in Spacey | Needed by | Evidence |
|---|---|---|
| Booking status, hold expiry, booking reference, coverage, cancel/refund fields | BRIEF 5.1 Booking (D10, D11, D18, D19, D22) | source inspected at 5a1cf3d |
| Booking party_size | BRIEF 5.1 Booking ("party size"; D7 "Party size 1..capacity") | source inspected at 5a1cf3d |
| Member display name, `is_operator`, `plan_active` | BRIEF 5.1 Member (D15) | source inspected at 5a1cf3d |
| Space `archived_at` | D23 | source inspected at 5a1cf3d |
| Any stored access code or grant | BRIEF 5.3 (Access) | source inspected at 5a1cf3d |
| BIGINT money | D1 (flaw F9) | source inspected at 5a1cf3d |
| `test_clock` table | D27 | source inspected at 5a1cf3d |
