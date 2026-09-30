# Contract: Purchase public surface

| Field | Value |
|---|---|
| Provider | Purchase (`cowork-booking-purchase`), port 8001 |
| Consumers | The Member's and the Operator's browser; the e2e suite (`requests.Session`) |
| State | proposed (M2 draft). Becomes agreed at M4 sign-off (tag `contract-v1`), verified by the M6 e2e run |
| OpenAPI | [openapi/purchase.yaml](openapi/purchase.yaml) |
| Outbound calls | Purchase → Payment ([purchase-payment.md](purchase-payment.md)); Purchase → Access ([purchase-access.md](purchase-access.md)) |
| Decisions | D1-D5, D7-D11, D13-D20, D23, D24, D27, D28; ADR-0002, ADR-0004, ADR-0007, ADR-0009, ADR-0013, ADR-0014 |

## 1. Purpose and parties

Purchase is the only service a Member uses directly. It owns members, spaces, 30-minute availability, bookings, price, coverage, booking status and cancellation (PUR-T33). This contract pins every browser route, form field, flashed message and redirect, plus the JSON API, so that the browser pages, the e2e suite and the other two implementers agree on one surface.

- Account data (email, display name, password hash) lives on Member in Purchase. There is no Identity service (ADR-0002).
- Purchase sends the browser to Payment's hosted page and links Access's e-ticket. It is the only caller of the other two services (PUR-R35, ADR-0004).

## 2. Authentication and session

- **Login.** `POST /login` (form) sets the cookie `purchase_session`: signed, HttpOnly, SameSite=Lax, plus Secure when `PUBLIC_URL` starts with https (PUR-R03). The JSON API uses the same cookie. There is no JSON login in contract-v1.
- **Lifetime.** 12 h from login, whatever the activity. After that a page redirects to `/login` with the flash "Please log in again" and the API answers 401 (PUR-R03).
- **Logout.** `POST /logout` clears the cookie in that browser. A copy replayed inside the 12 h still works: an accepted trade-off (D15, ADR-0016).
- **Anonymous callers** get the login step before any lookup: 303 to `/login` with a flash (pages) or 401 (JSON) (PUR-R05, PUR-R06).
- **Ownership.** A booking and its actions are for its owner or an operator. Any other logged-in Member gets 404, the same as for an unknown reference (PUR-R05, D17).
- **Operator pages** (`/operator/*`, `/dashboard`) answer a logged-in non-operator with 404 (PUR-R06). The Member whose email equals `OPERATOR_EMAIL` becomes operator at registration or login (PUR-R04).
- **CSRF.** SameSite=Lax plus "every state change is a POST" is the mitigation. There are no CSRF tokens (PUR-R37, ADR-0009). A GET to a POST route gets 405.

The e2e suite logs in like a browser:

```http
POST /register
Content-Type: application/x-www-form-urlencoded

email=a%40example.com&display_name=Member+A&password=correct-horse
```

```http
HTTP/1.1 303 See Other
Location: /login
```

```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=a%40example.com&password=correct-horse
```

```http
HTTP/1.1 303 See Other
Location: /
Set-Cookie: purchase_session=...; HttpOnly; Path=/; SameSite=Lax
```

## 3. Conventions

- **Forms** post `application/x-www-form-urlencoded`. Every successful or refused form POST answers 303 (post, redirect, get). The outcome shows once as a flashed message on the next page (PUR-R36).
- **No text from the URL is ever shown.** `?error=`, `?message=` and `?code=` are ignored (PUR-R36).
- **JSON** requests send `Content-Type: application/json`; a body that is not a JSON object gets 400. JSON answers never redirect.
- **Times.** Pages show Bangkok time, "2026-10-07 09:00". JSON needs ISO 8601 with an offset and answers with `+07:00`; a naive time gets 400 (PUR-R07, D2).
- **Money.** Pages show "THB 450.00". JSON uses integer satang in fields ending `_satang`, with `"currency": "THB"` (PUR-R18, D1).
- **JSON errors** always have this shape. The rule rows quote only the text, which is `error.message`. Only `GET /health` keeps the seed shape, `{"status": "error", "error": "database unreachable"}` (section 4):

```json
{"error": {"code": "slot_taken", "message": "Slot just taken"}}
```

| Status | error.code | message (example) | Rule |
|---|---|---|---|
| 400 | `invalid_request` | "Time needs an offset, for example +07:00"; "Start on :00 or :30"; "Duration must be 1 to 8 blocks"; "Outside opening hours 08:00-20:00"; "Book at least 60 minutes ahead"; "Book at most 30 days ahead"; "Party size must be 1 to 6"; "Pick a date from today to 30 days ahead" | PUR-R07, PUR-R08, PUR-R09, PUR-R10, PUR-R13, PUR-R14 |
| 401 | `unauthorized` | "Please log in" | PUR-R03, PUR-R05 |
| 404 | `not_found` | "Not found" (unknown, not yours, archived space, or not an operator) | PUR-R05, PUR-R06, PUR-R16 |
| 409 | `slot_taken` | "Slot just taken" | PUR-R12, PUR-R22 |
| 409 | `held_booking_exists` | "Finish or cancel your held booking BK-7KQ2M9 first" | PUR-R39 |
| 409 | `payment_time_over` | "Time to pay has run out; you can book again after 10:15" | PUR-R40 |
| 409 | `booking_started` | "This booking has started; ask the operator" | PUR-R30 |
| 409 | `booking_ended` | "This booking has ended" | PUR-R30 |
| 409 | `hold_expired` | "This hold has already expired" | PUR-R31 |
| 503 | `payment_unreachable` | "Payment is not reachable. Please try again." | PUR-R22, PUR-R23, PUR-R31 |

## 4. Browser routes

"Member" means any logged-in Member; "Owner" means the booking's Member or an operator; "Operator" means `is_operator`. Anonymous callers of a Member, Owner or Operator route get 303 to `/login` with "Log in to book" (booking form) or "Please log in" (other pages).

| Method | Path | Who | Input | Success | Other outcomes | Rules |
|---|---|---|---|---|---|---|
| GET | `/health` | anyone | none | 200 `{"status": "ok", "revision": "<APP_REVISION>"}` | 503 `{"status": "error", "error": "database unreachable"}` | none (kept from the seed) |
| GET | `/register` | anyone | none | 200 sign-up form | | PUR-R01 |
| POST | `/register` | anyone | `email`, `display_name`, `password` | 303 `/login`, flash "Registered. Please log in." | 303 `/register` with "Email already registered", "Password must be at least 8 characters" or "Display name is required" | PUR-R01, PUR-R04 |
| GET | `/login` | anyone | none | 200 login form | | PUR-R02 |
| POST | `/login` | anyone | `email`, `password` | 303 `/`; the header shows the display name | 303 `/login` with "Invalid email or password" (same for unknown email and wrong password) | PUR-R02, PUR-R03, PUR-R04 |
| POST | `/logout` | anyone | none | 303 `/`, flash "Logged out"; cookie cleared | GET `/logout` gets 405 | PUR-R37 |
| GET | `/` | anyone | none | 200 non-archived spaces: name, capacity, "THB 300.00 per hour, THB 150.00 per 30 min" | | PUR-R15, PUR-R16, PUR-R18 |
| GET | `/spaces/<space_id>` | anyone | query `date` (YYYY-MM-DD, default today), `blocks` (1-8, default 1) | 200 space page: date input with min today and max today + 30, duration 1-8, the price for that duration, party size 1 to capacity, note, the start-block grid (section 6) | 404 unknown or archived space; a date outside the horizon gets 303 `/spaces/<space_id>` with "Pick a date from today to 30 days ahead"; blocks outside 1-8 get 303 with "Duration must be 1 to 8 blocks" | PUR-R08, PUR-R09, PUR-R10, PUR-R13, PUR-R14, PUR-R17, PUR-R19 |
| POST | `/spaces/<space_id>/book` | Member | `date`, `start` (HH:MM), `blocks`, `party_size`, `note` (optional) | Pay: 303 to the Payment hosted page `url`. Plan or free: 303 `/bookings/<ref>` | See section 5.3 | PUR-R05, PUR-R07 to PUR-R14, PUR-R17, PUR-R19 to PUR-R23, PUR-R39, PUR-R40 |
| GET | `/bookings/<ref>` | Owner | none | 200 booking page (section 7). Reconciles a held booking and retries pending follow-ups first | 404 not yours or unknown | PUR-R05, PUR-R24, PUR-R26, PUR-R28, PUR-R32, PUR-R33, PUR-R40 |
| GET | `/bookings/<ref>/return` | Owner | query `session_id=ps_…` (ignored) | Reconciles with the stored session id, then 303 `/bookings/<ref>`. This is the `success_url` | 404 not yours | PUR-R24, PUR-R25, PUR-R26 |
| GET | `/bookings/<ref>/cancel` | Owner | none | 200 confirm screen showing the refund (section 5.4) | 303 `/bookings/<ref>` when the booking cannot be cancelled, with the flash that a POST would get | PUR-R30, PUR-R31 |
| POST | `/bookings/<ref>/cancel` | Owner | none | 303 `/bookings/<ref>`, flash "Booking cancelled" | See section 5.4 | PUR-R30, PUR-R31, PUR-R32 |
| POST | `/bookings/<ref>/retry` | Owner | none | 303 `/bookings/<ref>` after retrying, in order: pending grant, pending revoke, pending refund. An operator caller also starts attempt+1 of a failed refund | A Member never starts attempt+1: the page keeps "Refund failed. The operator will follow up." | PUR-R26, PUR-R32, PUR-R33 |
| GET | `/bookings/mine` | Member | none | 200 upcoming and past bookings, past ones marked "Completed". Reconciles held bookings first | | PUR-R05, PUR-R24, PUR-R28 |
| GET | `/operator/bookings` | Operator | none | 200 every booking with status, Cancel, Retry (only with a pending or failed step), Reconcile (held only); "Revocation pending" flagged | 404 for a non-operator | PUR-R06, PUR-Q12 |
| POST | `/operator/bookings/<ref>/cancel` | Operator | none | 303 `/operator/bookings`, flash "Booking cancelled". Operator policy: before the end, always 100% | "This booking has ended" at or after the end | PUR-R06, PUR-R30, PUR-R32 |
| POST | `/operator/bookings/<ref>/retry` | Operator | none | 303 `/operator/bookings`. Retries pending steps; a stored failed refund gets attempt+1 | 404 for a non-operator: a Member cannot start attempt+1 | PUR-R06, PUR-R32, PUR-R33 |
| POST | `/operator/bookings/<ref>/reconcile` | Operator | none | 303 `/operator/bookings`, flash "1 confirmed, 0 expired, 0 unchanged" (counts for this booking) | "Payment is not reachable. Please try again." | PUR-R06, PUR-R24 |
| GET | `/operator/spaces` | Operator | none | 200 every space, with create, edit and archive forms | | PUR-R06, PUR-R15, PUR-R16 |
| POST | `/operator/spaces` | Operator | `name`, `capacity` (1-1000), `hourly_rate` (whole THB: 0 or 20-10000) | 303 `/operator/spaces`, flash "Space saved". Stored in satang | 303 with "Name is required", "Capacity must be a whole number from 1 to 1,000" or "Rate must be 0 or 20 to 10,000 THB per hour" | PUR-R15 |
| POST | `/operator/spaces/<space_id>` | Operator | `name`, `capacity`, `hourly_rate` | 303 `/operator/spaces`, flash "Space saved". Existing bookings keep their price and party size | Same flashes as create; 404 unknown space | PUR-R14, PUR-R15, PUR-R17 |
| POST | `/operator/spaces/<space_id>/archive` | Operator | none | 303 `/operator/spaces`, flash "Space archived" | "Cancel its upcoming bookings first" while a held or confirmed booking ends after now | PUR-R16 |
| GET | `/operator/members` | Operator | none | 200 Members with email, display name, `plan_active` and a plan button | | PUR-R06, PUR-R19 |
| POST | `/operator/members/<member_id>/plan` | Operator | none (toggle); optional `plan_active` (`true` or `false`) sets that value | 303 `/operator/members`, flash "Plan updated". With no field the POST flips the current value (the button sends no field). With `plan_active` it sets that value, so a repeat changes nothing. Only new bookings see it | 404 unknown Member or non-operator; any other `plan_active` value gets 303 with "Plan must be true or false" and no change | PUR-R06, PUR-R19 |
| GET | `/dashboard` | Operator | none | 200 last 7 Bangkok days: bookings by status, utilization "1.0%", counted members. No money | 404 for a non-operator | PUR-R06, PUR-R34 |
| POST | `/_test/clock` | e2e only | JSON `{"now": "<ISO with offset>"}` or `{"now": null}` | 200 `{"now": ...}` when `TEST_CLOCK_ENABLED` is exactly `true` | 404 otherwise; nothing stored | PUR-R38 |

## 5. Booking by form: outcomes

### 5.1 The request

`POST /spaces/<space_id>/book` builds the start instant from `date` + `start` in Bangkok time (PUR-R07). The name and email come from the logged-in Member, never from a field (PUR-R05). The price and coverage are set here and never change (PUR-R17, PUR-R19). A field `amount_satang` or any other extra field is ignored.

### 5.2 Checks, in this order (PUR-R39)

1. Input (400 in JSON, a flash on the form): time, block alignment, duration, opening hours, notice, horizon, party size.
2. The Member's own lapsed holds are reconciled; then a remaining slot-blocking held booking refuses any other request (409).
3. The pre-insert sweep reconciles stale holds of the space, then the check and insert run in one transaction; the partial EXCLUDE constraint catches a race (409) (PUR-R22).

### 5.3 Results

| Case | Form answer | JSON answer (`POST /api/bookings`) | Rule |
|---|---|---|---|
| New pay booking | 303 to the hosted page `url` | 201, `status` held, `payment_url` set | PUR-R21, PUR-R23 |
| Same space and time while the hold blocks (double submit) | 303 to the same hosted page | 200, the same booking and `payment_url` | PUR-R21 |
| New plan or free booking | 303 `/bookings/<ref>`; page "Confirmed. Covered by your plan. No payment was taken." (plan) | 201, `status` confirmed, `payment_url` null | PUR-R20 |
| Input error | 303 `/spaces/<space_id>?date=…&blocks=…` with the JSON message as the flash. One flash differs: a misaligned start gets "Pick a start on the half hour" (JSON: "Start on :00 or :30") | 400 `invalid_request` | PUR-R07 to PUR-R10, PUR-R14 |
| Anonymous | 303 `/login`, "Log in to book" | 401 | PUR-R05 |
| Unknown or archived space | 404 | 404 | PUR-R16 |
| Another held booking blocks | 303 back to the space page, "Finish or cancel your held booking BK-7KQ2M9 first" | 409 `held_booking_exists` | PUR-R39 |
| Slot taken | 303 back, "Slot just taken" | 409 `slot_taken` | PUR-R12, PUR-R22 |
| Sweep needs Payment and it is unreachable | 303 back, "Payment is not reachable. Please try again." | 503 `payment_unreachable`; nothing changes | PUR-R22 |
| Session create unreachable after the insert | 303 `/bookings/<ref>`, "Payment is not reachable. Please try again."; booking held without a session | 503 `payment_unreachable` | PUR-R23, PUR-Q09 |
| Same slot after the session's `expires_at`, before `hold_expires_at` | 303 `/bookings/<ref>`, "Time to pay has run out; you can book again after 10:15" | 409 `payment_time_over`; no Payment call | PUR-R40 |

### 5.4 Cancel

`GET /bookings/<ref>/cancel` shows the refund before the person confirms (PUR-R30, PUR-R31):

| Booking | Screen text |
|---|---|
| Confirmed, pay, 24 h or more before start (or any operator cancel before the end) | "Refund THB 450.00 (100%)" |
| Confirmed, pay, under 24 h (Member) | "Refund THB 0.00 (0%)" |
| Confirmed, plan or free | "No payment was taken" |
| Held | "No payment has been taken. If your payment already went through, the refund follows the policy: THB 450.00 (100%)." |

`POST /bookings/<ref>/cancel` (and the operator route) answers:

| Case | Form answer | JSON answer (`POST /api/bookings/<ref>/cancel`) | Rule |
|---|---|---|---|
| Confirmed, allowed | 303, "Booking cancelled"; the page shows the follow-up state | 200 booking, `status` cancelled | PUR-R30, PUR-R32 |
| Held, session unpaid, inside the hold | 303, "Booking cancelled" | 200, `status` cancelled, `refund_amount_satang` 0 | PUR-R31 |
| Held, the expire answer says paid | 303, "Booking cancelled"; refund per policy | 200, `status` cancelled | PUR-R31 |
| Held, hold lapsed, unpaid | 303, "This hold has already expired" | 409 `hold_expired`; `status` is now expired | PUR-R31 |
| Held, Payment unreachable | 303, "Payment is not reachable. Please try again." | 503 `payment_unreachable`; still held | PUR-R31 |
| Member, at or after start | 303, "This booking has started; ask the operator" | 409 `booking_started` | PUR-R30 |
| Operator, at or after end | 303, "This booking has ended" | 409 `booking_ended` | PUR-R30 |
| Already cancelled (repeat) | 303, no change | 200, the stored booking; pending follow-ups retried, nothing new sent | PUR-R28, PUR-R32 |
| Not yours | 404 | 404 | PUR-R05 |

The policy follows the caller: an operator caller gets the operator policy on either route (D18).

After a confirmed cancel the booking page shows each follow-up: "Revocation pending", "Refund pending", "Refund failed. The operator will follow up." (PUR-R32, PUR-R33). The refund is sent only after the revoke succeeded (PUR-Q10).

## 6. Start-block grid (page and JSON)

For one space, one date and one duration, the grid lists every start from 08:00 to 19:30 (24 starts). A start is available only if all its blocks are inside opening hours, past the notice period and free of slot-blocking bookings. Otherwise the first reason that applies wins: "Too soon", then "Runs past 20:00", then "Booked" (PUR-R13). The end is exclusive, so a start right at another booking's end is available (PUR-R11).

Page markup, inside the booking form that posts to `/spaces/<space_id>/book` with hidden `date` and `blocks` and the fields `party_size` and `note`:

```html
<button type="submit" name="start" value="09:00">09:00</button>
<button type="submit" name="start" value="19:00" disabled title="Runs past 20:00">19:00</button>
```

Pressing an available start is "Continue to payment" (or "Book" for plan and free coverage). The page shows the price for the chosen duration above the grid, e.g. "THB 450.00", or for Member B "THB 450.00, covered by your plan. No payment needed." (PUR-R17, PUR-R19).

The JSON form is `GET /api/spaces/<space_id>/availability?date=2026-10-07&blocks=3` (section 8.2).

## 7. Booking page

`GET /bookings/<ref>` shows status, reference, times, price, coverage, payment outcome and the e-ticket link (PUR-R05). Held bookings show "Pay by 10:13" with a countdown to the session's `expires_at`, and a "Continue to payment" button that posts the same fields to `/spaces/<space_id>/book` (PUR-R21, PUR-R40). Other lines: "Your e-ticket is being prepared" (PUR-R26), "View e-ticket" linking `ticket_url`, "Payment status unknown, refresh later" (PUR-R24), "Completed" once the end has passed (PUR-R28).

A GET may change a booking only by the idempotent sync of D13, D19 and D20: reconcile, pending grant, pending revoke, pending refund. Nothing in the request steers it (PUR-R37).

## 8. JSON API

All JSON routes use the `purchase_session` cookie. Space reads need no login.

v1 has no JSON route for operator work, plans, the dashboard or a refund retry. Test those rule rows over the form routes in section 4: plan_active with `POST /operator/members/<member_id>/plan`, the metrics with `GET /dashboard` (404 for a Member, 303 to `/login` when anonymous), and a refund retry with `POST /bookings/<ref>/retry` (a Member starts no attempt 2) or `POST /operator/bookings/<ref>/retry` (404 for a Member). An unknown `/api/...` path gets 404 `not_found` (PUR-R06, PUR-R33, PUR-R34).

### 8.1 GET /api/spaces

200 with non-archived spaces (PUR-R15, PUR-R16):

```json
{"spaces": [
  {"space_id": 1, "name": "Meeting Room A", "capacity": 6, "hourly_rate_satang": 30000, "block_price_satang": 15000, "currency": "THB"},
  {"space_id": 4, "name": "Community Table", "capacity": 8, "hourly_rate_satang": 0, "block_price_satang": 0, "currency": "THB"}
]}
```

### 8.2 GET /api/spaces/{space_id}/availability

Query `date` (YYYY-MM-DD, required) and `blocks` (1-8, required). Answers: 200 grid; 400 `invalid_request` for a date outside today to today + 30 or bad blocks; 404 unknown or archived space (PUR-R13).

```json
{"space_id": 1, "date": "2026-10-07", "blocks": 3, "price_satang": 45000, "currency": "THB",
 "starts": [
   {"start": "2026-10-07T08:00:00+07:00", "available": false, "reason": "Booked"},
   {"start": "2026-10-07T10:30:00+07:00", "available": true, "reason": null},
   {"start": "2026-10-07T19:00:00+07:00", "available": false, "reason": "Runs past 20:00"}
 ]}
```

Three of the 24 entries, with BK-7KQ2M9 confirmed 09:00-10:30: 08:00 to 10:00 are Booked (3 blocks from 08:00 run to 09:30), 10:30 is free (the end is exclusive), 19:00 and 19:30 run past 20:00. The real answer always has 24 entries (the full example is in `openapi/purchase.yaml`). The grid is a read: it never reconciles and never holds a slot (PUR-R13).

### 8.3 POST /api/bookings

Request:

| Field | Type | Required | Constraints | Rule |
|---|---|---|---|---|
| `space_id` | integer | yes | A non-archived space, else 404 | PUR-R16 |
| `start` | string | yes | ISO 8601 with an offset; exactly :00 or :30 Bangkok time, no seconds; at least 60 min after now; date at most today + 30; inside 08:00-20:00 with the end. It may equal another booking's end: no gap is kept | PUR-R07, PUR-R08, PUR-R09, PUR-R10, PUR-R11 |
| `blocks` | integer | yes | 1 to 8 | PUR-R09 |
| `party_size` | integer | yes | 1 to the space's capacity | PUR-R14 |
| `note` | string | no | Free text for the Member and the operator | |

Responses: 201 new booking; 200 resumed hold (same Member, space, start and blocks); 400; 401; 404; 409 `held_booking_exists`, `slot_taken` or `payment_time_over`; 503 `payment_unreachable` (section 5.3).

Idempotency: no header. A repeat of the same space and time by the same Member resumes the slot-blocking hold, with the same reference and `payment_url` (PUR-R21, ADR-0014). A plan or free booking is confirmed at once, so a repeat of it gets 409 `slot_taken`.

### 8.4 GET /api/bookings/{ref}

Owner only. 200 booking object; 401 anonymous; 404 not yours or unknown (same body). Reconciles a held booking and retries pending follow-ups first, like the page (PUR-R05, PUR-R24).

### 8.5 GET /api/bookings/mine

Member only. 200 `{"bookings": [<booking object>, ...]}`, ordered by start. Reconciles held bookings first (PUR-R24, PUR-R28).

### 8.6 POST /api/bookings/{ref}/cancel

Owner only. Empty body or `{}`. Answers in section 5.4.

### 8.7 Booking object

The pinned fields, plus `completed`, `currency`, `note`, `payment_url` and `refund_reason`, which the rules need (PUR-R18, PUR-R28, PUR-T34).

| Field | Type | Values | Rule |
|---|---|---|---|
| `reference` | string | `BK-7KQ2M9` | PUR-R29 |
| `status` | string | `held`, `confirmed`, `expired`, `cancelled` | PUR-R28 |
| `completed` | boolean | true when confirmed and now is at or after the end | PUR-R28 |
| `space_id`, `space_name` | integer, string | 1, "Meeting Room A" | |
| `start`, `end` | string | ISO, `+07:00`; the end is exclusive | PUR-R07, PUR-R09 |
| `blocks`, `party_size` | integer | 3, 4 | PUR-R09, PUR-R14 |
| `note` | string or null | as sent | |
| `agreed_price_satang` | integer | 45000 | PUR-R17 |
| `currency` | string | `THB` | PUR-R18 |
| `coverage` | string | `pay`, `plan`, `free` | PUR-R19 |
| `hold_expires_at` | string or null | set for held pay bookings | PUR-R21 |
| `payment_session_id` | string or null | `ps_…` | PUR-R23 |
| `payment_url` | string or null | the hosted page; only while held with a session | PUR-R23 |
| `payment_status` | string | `not_required` (plan, free), `unpaid`, `paid`: the last payment status Purchase read. This is PUR-T34 payment_outcome under its JSON name; Payment's own payment_status (PMT-T04) has no `not_required` | PUR-R24, PUR-T34 |
| `cancel_reason` | string or null | `member_cancel`, `operator_cancel`, `amount_mismatch` | PUR-R25, PUR-R32 |
| `refund_reason` | string or null | the same, or `slot_unavailable` | PUR-R25, PUR-R32 |
| `refund_amount_satang` | integer or null | null until cancel; then 0 or the full price | PUR-R30 |
| `refund_status` | string | `none`, `pending`, `succeeded`, `failed` | PUR-R32, PUR-R33 |
| `refund_attempt` | integer or null | 1, 2, … | PUR-R33 |
| `grant_status` | string | `not_requested`, `pending`, `issued`, `revoke_pending`, `revoked` | PUR-R26, PUR-R32 |
| `ticket_url` | string or null | the Access e-ticket link, once issued | PUR-R26 |

## 9. Examples

Standard data: clock 2026-10-05 10:00 Bangkok; Member A logged in (cookie `purchase_session`); Meeting Room A, space_id 1, THB 300 per hour.

### 9.1 Success

```http
POST /api/bookings
Cookie: purchase_session=...
Content-Type: application/json

{"space_id": 1, "start": "2026-10-07T09:00:00+07:00", "blocks": 3, "party_size": 4, "note": "Team planning"}
```

```http
HTTP/1.1 201 Created

{"reference": "BK-7KQ2M9", "status": "held", "completed": false, "space_id": 1,
 "space_name": "Meeting Room A", "start": "2026-10-07T09:00:00+07:00",
 "end": "2026-10-07T10:30:00+07:00", "blocks": 3, "party_size": 4, "note": "Team planning",
 "agreed_price_satang": 45000, "currency": "THB", "coverage": "pay",
 "hold_expires_at": "2026-10-05T10:15:00+07:00",
 "payment_session_id": "ps_Q7mZ3xK9vT2bN8rL4wYc1A",
 "payment_url": "http://localhost:8002/pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A",
 "payment_status": "unpaid", "cancel_reason": null, "refund_reason": null,
 "refund_amount_satang": null, "refund_status": "none", "refund_attempt": null,
 "grant_status": "not_requested", "ticket_url": null}
```

After Member A pays and the browser returns, `GET /api/bookings/BK-7KQ2M9` shows `"status": "confirmed"`, `"payment_status": "paid"`, `"payment_url": null`, `"grant_status": "issued"` and `"ticket_url": "http://localhost:8003/t/q3Vt9XbLk2Rm8PzW4nHc7A"`.

### 9.2 Invalid input

```http
POST /api/bookings

{"space_id": 1, "start": "2026-10-07T09:00:00", "blocks": 3, "party_size": 4}
```

```http
HTTP/1.1 400 Bad Request

{"error": {"code": "invalid_request", "message": "Time needs an offset, for example +07:00"}}
```

A misaligned start `2026-10-07T09:15:00+07:00` gets "Start on :00 or :30". `2026-10-07T19:30:00+07:00` for 2 blocks gets "Outside opening hours 08:00-20:00". The same post from the form redirects back to the space page with the message as a flash, except the misaligned start, whose flash is "Pick a start on the half hour" (PUR-R09).

### 9.3 Failure

Member B asks for 10:00-11:00 while BK-7KQ2M9 is confirmed for 09:00-10:30 (PUR-R12):

```http
HTTP/1.1 409 Conflict

{"error": {"code": "slot_taken", "message": "Slot just taken"}}
```

Payment does not answer within 5 s when the session is created (PUR-R23):

```http
HTTP/1.1 503 Service Unavailable

{"error": {"code": "payment_unreachable", "message": "Payment is not reachable. Please try again."}}
```

BK-7KQ2M9 stays held with no `payment_session_id`. The same request later resumes it and creates the session.

Member A cancels 2026-10-07 at 09:00, the start (PUR-R30):

```http
HTTP/1.1 409 Conflict

{"error": {"code": "booking_started", "message": "This booking has started; ask the operator"}}
```

### 9.4 Repeat

At 10:05 Member A sends the 9.1 body again (double submit, PUR-R21):

```http
HTTP/1.1 200 OK

{"reference": "BK-7KQ2M9", "status": "held", "completed": false, "space_id": 1,
 "space_name": "Meeting Room A", "start": "2026-10-07T09:00:00+07:00",
 "end": "2026-10-07T10:30:00+07:00", "blocks": 3, "party_size": 4, "note": "Team planning",
 "agreed_price_satang": 45000, "currency": "THB", "coverage": "pay",
 "hold_expires_at": "2026-10-05T10:15:00+07:00",
 "payment_session_id": "ps_Q7mZ3xK9vT2bN8rL4wYc1A",
 "payment_url": "http://localhost:8002/pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A",
 "payment_status": "unpaid", "cancel_reason": null, "refund_reason": null,
 "refund_amount_satang": null, "refund_status": "none", "refund_attempt": null,
 "grant_status": "not_requested", "ticket_url": null}
```

No second booking and no second session: Payment returns the stored session for the same reference (PMT-R03).

At 10:05 Member A asks for Focus Pod 1 instead (PUR-R39):

```http
HTTP/1.1 409 Conflict

{"error": {"code": "held_booking_exists", "message": "Finish or cancel your held booking BK-7KQ2M9 first"}}
```

Cancel twice: the second `POST /api/bookings/BK-7KQ2M9/cancel` answers 200 with the stored cancelled booking. No second revoke or refund is started; only pending steps are retried.

### 9.5 Coverage skips collection

**No call is made to Payment.** Member B (plan_active true) books (PUR-R19, PUR-R20):

```http
POST /api/bookings

{"space_id": 1, "start": "2026-10-07T11:30:00+07:00", "blocks": 3, "party_size": 2}
```

```http
HTTP/1.1 201 Created

{"reference": "BK-5QW8XN", "status": "confirmed", "completed": false, "space_id": 1,
 "space_name": "Meeting Room A", "start": "2026-10-07T11:30:00+07:00",
 "end": "2026-10-07T13:00:00+07:00", "blocks": 3, "party_size": 2, "note": null,
 "agreed_price_satang": 45000, "currency": "THB", "coverage": "plan",
 "hold_expires_at": null, "payment_session_id": null, "payment_url": null,
 "payment_status": "not_required", "cancel_reason": null, "refund_reason": null,
 "refund_amount_satang": null, "refund_status": "none", "refund_attempt": null,
 "grant_status": "issued", "ticket_url": "http://localhost:8003/t/Nb4Rk8Tq2Wm6Xc9Pz3Hv7L"}
```

The price is stored but never collected. The only outbound call was POST /grants to Access. A Community Table booking (THB 0 per hour) gets `"coverage": "free"`, `"agreed_price_satang": 0` and the same shape. A later cancel refunds 0, calls only Access to revoke, and says "No payment was taken" (PUR-R30).

## 10. Timeouts and retries (outbound)

Purchase is the only caller (PUR-R35, ADR-0004):

- Every call to Payment or Access uses `timeout=5` seconds, a bearer token, and the internal URL.
- A timeout, a connection error or a 5xx answer means "unreachable". No result is stored.
- No call runs while a database transaction is open. Purchase commits, calls, then stores the answer in a new short transaction.
- One attempt per call inside a request. No loops or sleeps. The next touch retries: booking page, My bookings, `GET /api/bookings/<ref>`, the pre-insert sweep, Retry and Reconcile.
- What the Member sees:
  - A read that cannot reach Payment changes nothing and shows "Payment status unknown, refresh later".
  - A request that needs Payment's answer (the conflicting insert, a held cancel, session create) gets 503 or the flash "Payment is not reachable. Please try again.".
  - Access unreachable during issuance: "Your e-ticket is being prepared". During a revoke: "Revocation pending", and the refund waits.

## 11. Test-observable markers

| Where | Marker |
|---|---|
| `GET /spaces/<space_id>` | `<button name="start" value="HH:MM">`; unavailable ones have `disabled` and a `title` with the reason |
| Every Purchase page | Flashed messages appear as text in the body once; tests match the text |
| Booking state | Tests read `GET /api/bookings/<ref>` with the same cookie; Purchase pages carry no data- markers in contract-v1 |
| Payment hosted page | `data-decline-code` ([purchase-payment.md](purchase-payment.md), section 8) |
| Access e-ticket and kiosk | `data-ticket-code`, `data-status`, `data-result` ([purchase-access.md](purchase-access.md), section 8) |

Test hooks: `POST /_test/clock` on all three services, 404 unless `TEST_CLOCK_ENABLED=true` (PUR-R38, PMT-R20, AXS-R19). The e2e suite sets the same instant on all three.

## 12. Versioning

- This draft is state proposed. At M4 a consumer-lens reviewer (browser and e2e) signs it off in `REVIEW_LOG.md`; then `cowork-booking-purchase` is tagged `contract-v1`, and the text moves beside the Purchase code with its `openapi.yaml` (ADR-0005).
- Any change after `contract-v1`, even an added field, goes through a CONTRACT_CHANGE_REQUEST and the tag `contract-v2`.
- Paths carry no version prefix. Consumers ignore JSON fields they do not know.
