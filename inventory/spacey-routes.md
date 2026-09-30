# Spacey routes at 5a1cf3d

Source: `cs403bkk-2026/spacey` main `5a1cf3d90e538f431625cbb959987b7bdbe3c946`, `app.py` (1053 lines). Nothing here was run. All rows are Observed Spacey behaviour, not project policy.

## Count

```
$ grep -cE '@app\.(route|get|post|put|patch|delete)' app.py
27
```

27 decorated routes, all inside `create_app()` (app.py:379-1052). No blueprints, no `before_request`, no `errorhandler`. Flask adds `HEAD` to every GET and answers `OPTIONS` itself; a wrong method gives 405 and a non-integer `<int:...>` segment gives 404.

"Auth required" means the route reads `session["user_id"]`. "Ownership check" means it limits rows to the logged-in user. `302` rows are HTML form flows. The last-but-one column is the BRIEF section 10 destination; [keep-delete.md](keep-delete.md) has the detail.

## Routes

| # | Method | Path | Auth required? | Ownership check? | Template or JSON | What it does | Status codes | app.py line | In openapi.yaml? | Section 10 destination | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GET | `/` | No | n/a | `index.html` | Lists all spaces, which are booked right now, every upcoming booking's times per space (paid or not); one booking form per space; reflects `?error=` | 200 | 413 | No (HTML) | Purchase (index) | source inspected at 5a1cf3d |
| 2 | GET | `/register` | No | n/a | `register.html` | Registration form; passes `?registered=` (unused by the template) and `?error=` | 200 | 467 | No (HTML) | Purchase | source inspected at 5a1cf3d |
| 3 | POST | `/register` | No | n/a | JSON if `is_json`, else form redirect | Creates a user via `register_user` (443): email trimmed + lower-cased, password hashed | JSON 201 / 400 / 409 ("email is already registered"); form 302 to `/register?error=...` or `/login?message=Registered!...` | 475 | Yes (JSON only) | Purchase | source inspected at 5a1cf3d |
| 4 | GET | `/login` | No | n/a | `login.html` | Login form; reflects `?error=` and `?message=` | 200 | 511 | No (HTML) | Purchase | source inspected at 5a1cf3d |
| 5 | POST | `/login` | No | n/a | JSON if `is_json`, else form redirect | `login_user` (489): same 401 for unknown email and wrong password; sets `session["user_id"]` | JSON 200 / 401; form 302 to `/login?error=...` or `/` | 519 | Yes (JSON only) | Purchase | source inspected at 5a1cf3d |
| 6 | POST | `/logout` | No | n/a | JSON if `is_json`, else redirect | Pops `user_id` from the client-side cookie session; idempotent | JSON 200 `{"status":"ok"}`; form 302 to `/` | 533 | Yes (JSON only; 302 not documented) | Purchase | source inspected at 5a1cf3d |
| 7 | GET | `/health` | No | n/a | JSON | `SELECT 1` on the shared connection; returns `revision` from `APP_REVISION` | 200 `{status:"ok", revision}` / 503 `{status:"error", error:"database unreachable"}` | 541 | Yes | All three services | source inspected at 5a1cf3d |
| 8 | GET | `/spaces` | No | n/a | JSON | Lists spaces with `available` for now or for `?start_time&end_time` (`parse_window` 154, `booked_space_ids` 170) | 200 / 400 (bad window) | 554 | Yes | Purchase | source inspected at 5a1cf3d |
| 9 | POST | `/spaces` | No | n/a | JSON | Creates a space (`name`, `capacity`, `price_cents` default 0) | 201 / 400; 500 if `capacity` or `price_cents` exceed INTEGER (not run; see flaws F9) | 570 | Yes | Purchase (operator only) | source inspected at 5a1cf3d |
| 10 | GET | `/spaces/<int:space_id>` | No | n/a | JSON | One space with `available` (same window rule) | 200 / 400 / 404 | 601 | Yes | Purchase | source inspected at 5a1cf3d |
| 11 | PATCH | `/spaces/<int:space_id>` | No | n/a | JSON | Partial update via `COALESCE`; existing bookings keep their `amount_cents` | 200 / 400 / 404 | 620 | Yes | Purchase (operator only) | source inspected at 5a1cf3d |
| 12 | DELETE | `/spaces/<int:space_id>` | No | n/a | JSON (empty body on 204) | Deletes a space unless any booking row references it | 204 / 404 / 409 ("space has bookings, cancel them first") | 663 | Yes | Purchase, reshaped to archive (D23) | source inspected at 5a1cf3d |
| 13 | GET | `/spaces/<int:space_id>/bookings` | No | No | JSON | Every booking of a space, all columns incl. `member`, `user_id`, `card_last4` | 200 / 404 | 684 | Yes | Purchase (operator only) | source inspected at 5a1cf3d |
| 14 | POST | `/spaces/<int:space_id>/bookings` | No (links `user_id` if a session exists) | n/a | JSON | Creates a booking via `book_space` (700): tz-aware ISO times, `member` default "guest", `party_size` default 1; paid at 0 if `member` is subscribed, else unpaid at `calculate_booking_price_cents` | 201 / 400 / 404 / 409 (overlap, ExclusionViolation or DeadlockDetected); 500 on INTEGER overflow | 774 | Yes | Purchase (reshaped) | source inspected at 5a1cf3d |
| 15 | POST | `/spaces/<int:space_id>/book` | No | n/a | Form redirect | Homepage form target; naive times read as Bangkok (`parse_form_time` 191); `party_size` hard-coded 1 | 302 to `/?error=...` or `/bookings/<id>/confirmation` | 795 | No (HTML) | Purchase (reshaped: date + block, D2) | source inspected at 5a1cf3d |
| 16 | GET | `/bookings/<int:booking_id>/confirmation` | No | No | `confirmation.html` / `booking_not_found.html` | Booking header, Pay form if unpaid, Unlock button if paid; renders `?code=` and `?error=` from the URL | 200 / 404 | 812 | No (HTML) | Split: Purchase booking page, Payment hosted page, Access ticket page | source inspected at 5a1cf3d |
| 17 | POST | `/bookings/<int:booking_id>/confirmation/pay` | No | No | Form redirect | `mark_booking_paid` (932) with form card fields; no `force_failure` | 302 to confirmation (with `?error=` on 400/404) | 836 | No (HTML) | Delete (Payment hosted page replaces it) | source inspected at 5a1cf3d |
| 18 | POST | `/bookings/<int:booking_id>/confirmation/unlock` | No | No | Form redirect | `issue_access_code` (970); puts the fresh code in the redirect URL | 302 to confirmation `?code=<hex>` or `?error=` | 852 | No (HTML) | Delete (Access ticket page replaces it) | source inspected at 5a1cf3d |
| 19 | GET | `/bookings/mine` | Yes (else 302 `/login`) | Yes (`WHERE b.user_id = session user_id`) | `my_bookings.html` | The logged-in user's bookings with Pay / "Get unlock code" links | 200 / 302 | 871 | No (HTML) | Purchase (My bookings) | source inspected at 5a1cf3d |
| 20 | GET | `/bookings` | No | No | JSON | Every booking in the system, all columns incl. `member`, `user_id`, `card_last4` | 200 | 891 | Yes | Purchase (operator only) | source inspected at 5a1cf3d |
| 21 | GET | `/bookings/<int:booking_id>` | No | No | JSON | One booking, all columns | 200 / 404 | 902 | Yes | Purchase (owner or operator, D17) | source inspected at 5a1cf3d |
| 22 | DELETE | `/bookings/<int:booking_id>` | No | No | JSON | Cancel = `DELETE FROM bookings ... RETURNING` (hard delete, paid or not) | 200 (deleted row) / 404 | 917 | Yes | Purchase, reshaped to status cancel (D18, D19) | source inspected at 5a1cf3d |
| 23 | POST | `/bookings/<int:booking_id>/pay` | No | No | JSON | `mark_booking_paid`; already-paid is a 200 no-op without a card; `force_failure: true` gives 402 | 200 / 400 (card) / 402 / 404 | 987 | Yes | Delete (Payment API replaces it) | source inspected at 5a1cf3d |
| 24 | POST | `/bookings/<int:booking_id>/unlock` | No | No | JSON | `issue_access_code`: new random 8-hex code each call, not stored | 200 `{booking_id, access_code}` / 402 (unpaid) / 404 | 999 | Yes | Delete (Access `POST /grants` replaces it) | source inspected at 5a1cf3d |
| 25 | POST | `/members/<name>/subscribe` | No | No | JSON | Upserts `subscriptions(member_key(name))` active; free, no provider | 200 / 400 (blank name) | 1004 | Yes | Purchase: becomes the operator's `plan_active` toggle | source inspected at 5a1cf3d |
| 26 | GET | `/metrics` | No | n/a | JSON | `compute_metrics` (283) business numbers | 200 | 1027 | Yes | Purchase (booking metrics only) | source inspected at 5a1cf3d |
| 27 | GET | `/dashboard` | No | n/a | `dashboard.html` | Same metrics plus revenue-per-space bars | 200 | 1034 | No (HTML) | Purchase (operator only, D24) | source inspected at 5a1cf3d |
| - | GET | `/static/<path:filename>` | No | n/a | file | Flask built-in; serves `static/style.css` | 200 / 404 | (Flask) | No | All three services | source inspected at 5a1cf3d |

## Route helpers nested in `create_app`

| Helper | app.py line | Called by routes | Evidence |
|---|---|---|---|
| `register_user(email, password)` | 443 | #3 | source inspected at 5a1cf3d |
| `login_user(email, password)` | 489 | #5 | source inspected at 5a1cf3d |
| `book_space(space_id, member, start_time, end_time, party_size)` | 700 | #14, #15 | source inspected at 5a1cf3d |
| `mark_booking_paid(booking_id, card_number, expiry, cvc, force_failure=False)` | 932 | #17, #23 | source inspected at 5a1cf3d |
| `issue_access_code(booking_id)` | 970 | #18, #24 | source inspected at 5a1cf3d |

## openapi.yaml vs code

| Item | Finding | Evidence |
|---|---|---|
| Coverage | `openapi.yaml` (732 lines, OpenAPI 3.0.3) lists 18 operations, which are the 18 JSON routes above. It says the 9 HTML routes "are not listed here" (openapi.yaml:9-12). | source inspected at 5a1cf3d |
| Form branches | POST `/register`, `/login`, `/logout` also answer HTML forms with 302; not documented. | source inspected at 5a1cf3d |
| 500s | No 500 responses documented; the code can return 500 on INTEGER overflow (flaws F9). | source inspected at 5a1cf3d |
| Persona examples | Member and email examples use a persona first name at openapi.yaml:234, 412, 420, 432, 459, 683, 723. Scrub before seeding. | source inspected at 5a1cf3d |
| Brand | `title: Spacey API` (openapi.yaml:3). Must change in every kept copy. | source inspected at 5a1cf3d |
