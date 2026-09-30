# Spacey flaws at 5a1cf3d

The 16 flaws come from BRIEF section 4 ("Spacey flaws, confirmed by probe"). The probe was prior research; M0 did not re-run it. This file points at the code that causes each flaw and, where they exist, at passing tests or class records that show it. All of it is Observed Spacey behaviour, not project policy.

Each flaw must end up fixed or declared out of scope in `PROVENANCE.md`, citing a rule or ADR (BRIEF section 15 checklist). The Disposition column is filled in M1.

"Not run" marks a consequence read from code, not observed.

## BRIEF section 4 flaws

| ID | Flaw (BRIEF wording) | Code that causes it (file:line) | How | Disposition | Evidence |
|---|---|---|---|---|---|
| F1 | Free-form times | app.py:143-151 `parse_time`; app.py:191-200 `parse_form_time`; app.py:712-713 (only check: end after start); templates/index.html:32-33 (`datetime-local`, no `step`); purchase.py:14 (prices any second count) | Any instant is accepted: no 30-minute grid, no opening hours, no minimum or maximum length | to decide in M1 | source inspected at 5a1cf3d |
| F2 | Past bookings accepted | app.py:700-772 `book_space` (no compare with now); app.py:777-784 and 800-804 (callers only check parsing) | No "start in the future" rule on the JSON or the form path | to decide in M1 | source inspected at 5a1cf3d |
| F3 | Unpaid holds block the slot forever | app.py:745-765 (INSERT with `paid = subscribed`, so False for most); app.py:731-737 (overlap pre-check ignores `paid`); app.py:130-135 (EXCLUDE covers every row); app.py:49-117 (no status, hold or expiry column); app.py:170-185 and 418-428 (availability counts unpaid rows) | An unpaid row is a permanent reservation. Nothing expires it; only DELETE frees it. | to decide in M1 | source inspected at 5a1cf3d |
| F4 | The access code is regenerated on every unlock, never stored, and a spoofable `?code=` value is rendered | app.py:984 `access_code = secrets.token_hex(4)` with no INSERT (970-985); app.py:863-868 (redirect puts the code in the URL); app.py:832 `code=request.args.get("code")`; templates/confirmation.html:21-22 (renders it as "Your access code"); gunicorn.conf.py:1-3 (comment: "the door access code arrives as ?code=...") | Each unlock returns a new random code that nothing can verify. Any `?code=anything` on the confirmation URL shows as a real code, even on an unpaid booking. | to decide in M1 | source inspected at 5a1cf3d |
| F5 | Cancel hard-deletes the booking and erases revenue | app.py:917-930 `DELETE FROM bookings WHERE id = %s RETURNING ...`; app.py:298-301 and 337-343 (revenue sums surviving rows only); openapi.yaml:302-304 ("Deletes the booking outright, whether or not it was paid") | A paid booking disappears with its amount and `card_last4`; no refund, no cancelled state, no audit | to decide in M1 | source inspected at 5a1cf3d |
| F6 | A free subscription keyed by typed name makes bookings paid at amount 0 | app.py:62-67 (`subscriptions.member TEXT PRIMARY KEY`); app.py:1004-1025 (anonymous, free upsert for any `<name>`); app.py:256-267 `member_key`, `is_subscribed`; app.py:741, 755, 758-759 (`paid = subscribed`, amount 0 if subscribed); app.py:788, 799 (member is whatever the caller types) | Anyone can subscribe any name, then book as that name for free. Coverage is stored as `paid = TRUE`, so metrics count it as a payment (289-290, 325-329). | to decide in M1 | source inspected at 5a1cf3d |
| F7 | No ownership checks. GET /bookings, unlock and space CRUD are anonymous | app.py:891-900 (`GET /bookings`, all rows incl. `member`, `user_id`, `card_last4`); 902-915; 917-930; 987-997; 999-1002; 812-834; 836-850; 852-869; 684-698; 570-599; 620-661; 663-682; 1004-1025. Only app.py:876-877 and 884-885 (`/bookings/mine`) read the session. app.py:73-78 (`users` has no role column) | No route checks that the caller owns the booking or is an operator. Ids are SERIAL (39, 52), so they are easy to enumerate. | to decide in M1 | source inspected at 5a1cf3d |
| F8 | Public dashboard | app.py:1034-1050 `/dashboard`; app.py:1027-1032 `/metrics`; templates/base.html:12 (nav link "Business metrics" for every visitor) | Revenue, conversion and per-space revenue are open to anyone | to decide in M1 | source inspected at 5a1cf3d |
| F9 | INTEGER amount overflow gives a 500 | app.py:90 (`amount_cents INTEGER`); app.py:46-47 (`price_cents INTEGER`); app.py:216-217 `is_valid_price` (no upper bound); purchase.py:14-15 (unbounded Python int); app.py:745-769 (only `DeadlockDetected`/`ExclusionViolation` caught) | A large rate or long booking yields an amount above 2^31-1; Postgres rejects the INSERT with an uncaught error, so Flask returns 500. Sibling paths (not run): `POST/PATCH /spaces` with a huge `price_cents` or `capacity` (41, 207-213, 591-596, 650-658). | to decide in M1 | source inspected at 5a1cf3d |
| F10 | Sessions never expire. A logout cookie can be replayed. The default SECRET_KEY is used in deploy | app.py:20 (default `dev-secret-key-not-for-production`); app.py:386 `app.secret_key = SECRET_KEY`; app.py:508 (login writes `user_id` into the client cookie); app.py:536 (logout only pops it from this client's cookie); no session lifetime config anywhere; deploy/startup-app.nomad.hcl:56-63 and compose.yaml:15-17 (no `SECRET_KEY`) | Flask's signed-cookie session has no server-side state, so a copied pre-logout cookie still works. Spacey sets no lifetime of its own (Flask's own default bound was not checked against the pinned Flask 3.1.2). Deploy runs with the public default key. | to decide in M1 | source inspected at 5a1cf3d |
| F11 | Registration reveals whether an email exists | app.py:461-462 (409 "email is already registered"); app.py:485-486 (form redirects with that text) | Contrasts with login, which hides it on purpose (app.py:492-494) | to decide in M1 | source inspected at 5a1cf3d |
| F12 | `?error=` text is reflected into pages | app.py:440, 472, 515-516, 832-833; templates/index.html:5-7, register.html:5-7, login.html:5-10 (also `?message=`), confirmation.html:21-25 (also `?code=`) | Any text in the URL shows as a site message. Jinja autoescape (comment app.py:392-393) stops script injection, not fake messages. | to decide in M1 | source inspected at 5a1cf3d |
| F13 | No CSRF tokens on POST forms | templates/base.html:17 (logout); index.html:30-35 (book); login.html:11-15; register.html:8-12; confirmation.html:9-11 (unlock) and 14-19 (pay); requirements.txt (no CSRF library); no `SESSION_COOKIE_SAMESITE` set | No form carries a token and no route checks one | to decide in M1 | source inspected at 5a1cf3d |
| F14 | The pay check-then-update is not atomic | app.py:940-946 (SELECT), 950 (`if row["paid"]`), 960-965 (`UPDATE ... WHERE id = %s`, no `AND NOT paid`, no `FOR UPDATE`); app.py:25 (autocommit, so no transaction) | Two concurrent pays both pass the check; the second overwrites `card_last4` (not run) | to decide in M1 | source inspected at 5a1cf3d |
| F15 | The form has no party size field | templates/index.html:30-35 (fields: member, start_time, end_time only); app.py:806 (`book_space(..., 1)` hard-coded) | The capacity check (app.py:715-727) is reachable only through JSON. Even there the value is checked, then discarded: no party_size column; INSERT app.py:746-748 (see [spacey-schema.md](spacey-schema.md)) | to decide in M1 | source inspected at 5a1cf3d |
| F16 | A 0-amount booking still asks for a card | templates/confirmation.html:12-19 (card form whenever `not booking.paid`, no amount test); app.py:953-955 (`validate_card` always required when unpaid); app.py:47, 217, 575 (price 0 allowed and the default) | A booking on a 0-rate space is created unpaid at 0, and the member must enter a card to "pay" 0 | to decide in M1 | source inspected at 5a1cf3d |

## Other evidence for the section 4 flaws

One row per piece of evidence. Class-record run claims belong to the PR author or reviewer, not to us.

| Flaw | What shows it | Evidence |
|---|---|---|
| F2 | `test_form_times_are_read_as_bangkok_time` (303) and `test_confirmation_page_shows_times_in_bangkok_time` (179) book 2026-09-25 09:00 Bangkok; 14 lines of `tests/test_app.py` call `slot(-1, 1)` (starts an hour before collection) | source inspected at 5a1cf3d |
| F2 | Both named tests `PASSED` in the `-rA` run (lines in [spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |
| F2 | SLOT-R01 past-slot row: a class reviewer "Tried a past unpaid booking (1 Sep 09:00–10:00): it's accepted, and a second booking for the same slot gets 409." | class PR #6 discussion |
| F3 | SLOT-R01 "An unpaid booking holds its slot until it is cancelled" (author runs, two approvals) | class PR #6 diff at c18b638 |
| F4 | `test_book_pay_unlock_all_the_way_through_the_browser` (132) only checks `len(code) == 8`; no test calls `/unlock` twice, so none checks reuse | source inspected at 5a1cf3d |
| F4 | `test_book_pay_unlock_all_the_way_through_the_browser` `PASSED` in the `-rA` run (line in [spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |
| F4 | PAY-R03 row "A paid booking that already unlocked once \| Unlock again \| 200, a different code †" and PAY-T04 "It is not saved, so asking again gives a new code." | source inspected at 58a1477 |
| F4 | Extraction site: "Observed current behaviour: each request generates a new code." | course site [extraction site] fetched 2026-09-30 |
| F5 | `test_cancel_booking_makes_space_available_again` (664) asserts `GET /bookings/<id>` gives 404 after cancel | source inspected at 5a1cf3d |
| F5 | `test_cancel_booking_makes_space_available_again` `PASSED` in the `-rA` run (line in [spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |
| F5 | SLOT-R02 "Cancelling deletes a booking and frees its slot"; a card-paid booking is deleted and "nothing about a refund is stored" | class PR #6 diff at c18b638 |
| F5 | A class reviewer on rules PR #6 (review, APPROVED) links Spacey issue #82: "We have an open issue for this (#82 - \"Cancelling a paid booking should leave a record\"). Maybe link it so it stays visible?" | class PR #6 discussion |
| F6 | `test_subscription_matches_the_member_name_ignoring_case_and_spaces` (1327) asserts `paid is True` for two spellings of the subscribed name; `test_a_subscribers_booking_adds_no_per_booking_revenue` (1341) asserts `paid_bookings == 1` and `revenue_cents == 0` | source inspected at 5a1cf3d |
| F6 | Both tests `PASSED` in the `-rA` run (lines in [spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |
| F6 | PAY-R01 "A subscriber's booking starts as paid" (observed) | source inspected at 58a1477 |
| F7 | EX-R04 records that only `/bookings/mine` checks ownership (observed; intent unresolved) | source inspected at 58a1477 |
| F7 | No test in G5, G7, G10 or G15 registers, logs in or sets a session (0 of 50; check in [spacey-tests-infra.md](spacey-tests-infra.md) section 2) | source inspected at 5a1cf3d |
| F7 | All 50 tests of G5, G7, G10 and G15 `PASSED` in the `-rA` run (21/21, 18/18, 3/3, 8/8; check in [spacey-tests-infra.md](spacey-tests-infra.md) section 2) | test run at 5a1cf3d |
| F8 | No dashboard test (G15, 8 tests) registers, logs in or sets a session | source inspected at 5a1cf3d |
| F8 | All 8 G15 tests `PASSED` in the `-rA` run (check in [spacey-tests-infra.md](spacey-tests-infra.md) section 2) | test run at 5a1cf3d |
| F9 | A class reviewer: "I ran a 100-year booking at 2500 cents/hour: HTTP 500 \"integer out of range\", nothing stored." | class PR #4 discussion |
| F10 | ACC-R02 records no expiry and browser-only logout; Q-ACC-3 "should logout end the session everywhere, so a copied cookie stops working? Should sessions expire?" | class PR #10 diff at d68631f |
| F11 | ACC-R01 Q-ACC-1: registration "does reveal it. Is that acceptable?" | class PR #10 diff at d68631f |
| F11 | `test_registering_with_a_duplicate_email_is_rejected` (971) asserts 409 and `{"error": "email is already registered"}` for a second sign-up with the same email in another case | source inspected at 5a1cf3d |
| F11 | `test_registering_with_a_duplicate_email_is_rejected` `PASSED` in the `-rA` run (line in [spacey-tests-infra.md](spacey-tests-infra.md) section 1) | test run at 5a1cf3d |
| F15 | BOOK-R01 open question: "The HTML form submits 1 and does not ask for the actual group size" | class PR #11 diff at 7cf2656 |
| F16 | A class reviewer: "I also ran paying the zero-amount booking with no card: 400 \"card_number must be 13-19 digits\", still unpaid." | class PR #4 discussion |
| F16 | PAY-R02 row "unpaid booking, amount 0 \| pay with no card \| Card details are still required †"; reviewer: "IDK let's say it's intended feature for now." | class PR #1 discussion |

## Additional flaws (not in BRIEF section 4)

| ID | Flaw | Code (file:line) | How | Disposition | Evidence |
|---|---|---|---|---|---|
| A1 | Pay racing cancel can crash with a 500 (not run) | app.py:960-968 | If the row is deleted between the SELECT (940) and the UPDATE, `cur.fetchone()` returns None and `booking_to_json(None)` raises | to decide in M1 | source inspected at 5a1cf3d |
| A2 | Unlock ignores the booking time | app.py:970-985 | A code is issued for a past or far-future paid booking at any time; no check-in window | to decide in M1 | source inspected at 5a1cf3d |
| A3 | Subscribing "guest" makes every anonymous booking free | app.py:788, 799 (blank member becomes "guest"); app.py:1004-1019 | `POST /members/guest/subscribe` turns on coverage for all guest bookings. Consequence of F6. | to decide in M1 | source inspected at 5a1cf3d |
| A4 | Booking identity is split: free-text `member` vs account `user_id` | app.py:54, 96-97, 743, 799 | A logged-in user can book under any typed name; coverage follows the name, My bookings follows `user_id` | to decide in M1 | source inspected at 5a1cf3d |
| A5 | Metrics conflate coverage with payment and count names, not people | app.py:289-290, 295, 317-323, 325-329 | Subscriber bookings count as "paid" at 0; "members" and repeat rate count distinct typed strings (MET-R01, MET-R02) | to decide in M1 | source inspected at 5a1cf3d |
| A6 | Test hook `force_failure` is live in production | app.py:957-958, 995 | Any JSON caller can force a 402 | to decide in M1 | source inspected at 5a1cf3d |
| A7 | Naive time: the form accepts it, JSON rejects it | app.py:149-150 vs 198-199 | The same input means Bangkok time on the form and is an error on the API (TIM-R01 conflict) | to decide in M1 | source inspected at 5a1cf3d |
| A8 | One shared connection, no reconnect, DDL at import | app.py:25, 387, 1053 | Every request shares one autocommit connection; if it drops, all requests fail until restart | to decide in M1 | source inspected at 5a1cf3d |
| A9 | JSON `member` is not type- or blank-checked | app.py:788 | `""`, `"   "` or a non-string reaches the INSERT (745-765); blank strings are stored; a non-string likely gives a DB error and a 500 (not run) | to decide in M1 | source inspected at 5a1cf3d |
| A10 | Money is shown in dollars | app.py:395 (`$` and /100); app.py:376 comment "$25.00 per hour" | The target uses THB (D1) | to decide in M1 | source inspected at 5a1cf3d |
| A11 | No injectable clock | app.py:175, 250, 311, 420, 427 | "Now" comes from Postgres `now()` and `datetime.now`; tests cannot move time (needed for holds, the cancel cut-off and the check-in window, D27) | to decide in M1 | source inspected at 5a1cf3d |
| A12 | Nullable booking times inside the EXCLUDE range (not run) | app.py:85-86, 134 | A NULL bound makes `tstzrange` unbounded, which would block the whole space; the app never writes NULL today | to decide in M1 | source inspected at 5a1cf3d |
| A13 | Homepage lists the timing of every upcoming booking, paid or not, to anonymous visitors | app.py:425-431; templates/index.html:19-29 | Low severity; names are not shown | to decide in M1 | source inspected at 5a1cf3d |
| A14 | Space deletion needs all bookings cancelled, and cancel hard-deletes them, so retiring a space erases its revenue history | app.py:663-682, 917-930 | EX-R05 and SLOT-R02 agree; together they erase history. PR #5 Q06 asks for "archived" or "inactive" instead. | to decide in M1 | source inspected at 5a1cf3d |
| A15 | Startup backfill fills a NULL amount with the current hourly rate, ignoring duration | app.py:112-117 | A historical 3-hour row at rate 1500 becomes 1500, not 4500 (PRC-R02 example) | to decide in M1 | source inspected at 5a1cf3d |
