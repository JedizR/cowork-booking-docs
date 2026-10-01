# Rules

Business rules of Cowork Booking, by context, in ID order. Each rule uses the class rule template (class rules main 58a1477): Rule, Policy status, Decision source, Implementation evidence, Terms, Candidate responsibility and dependencies, Open question, Clarification owner and Next use, then a table of examples.

Policy status is one of:

- Decided: a project decision, cited as D1 to D28 (DECISIONS.md), as an ADR, or as the row of "Disputes decided in M1" (DECISIONS.md) that reads a default more precisely (row 7 for the derived Completed state). The D number comes first where one applies. ADR-NNNN names an ADR in adr/ (index: adr/README.md).
- Stakeholder-clarified: scoped, with its source. Only PUR-R17, the booking price (course instructor, class rules PR #14 at 25ca71e, merged as 58a1477).
- Observed: seed behaviour whose intent is unresolved. No rule here is Observed; class behaviour we do not adopt is recorded in ID_MAP.md.
- Superseded: replaced, with a link to the replacing rule. No rule here is Superseded.

Clarification owner names who settles each open question the rule cites (the Owner line of that question in OPEN_QUESTIONS.md), then who owns the rule as stated. A rule with no open question names its own owner.

Implementation evidence is one of `source inspected at <sha>`, `test run at <sha>` (with output) or `live journey verified`. They are never interchangeable. At M1 every rule says "Not implemented yet (planned M5)." Where the seed app has related behaviour, the rule cites it as "Spacey: source inspected at 5a1cf3d, app.py:<line>": the source was read, not run. TRACEABILITY.md (M6) links each rule to its tests.

How to read the example table:

- # numbers the rows.
- Kind is ordinary, boundary or counterexample. Every rule has all three.
- Channel is JSON (an API call), form (a browser page: the outcome is a redirect and a flashed message, never ?error=) or internal (service logic or a service-to-service call). Where a behaviour has both a JSON API and a browser form, each gets its own row. In Payment and Access rules, calls to their JSON API (made by Purchase) are JSON rows; in Purchase rules, Purchase's outbound calls are internal rows.
- Given is the state before, When is the action, and Expected result under this rule is what must happen.
- "then" inside one row means one sequence on the same objects, in that order, and it must hold under the check orders the rules pin; a refusal comes before the action that would change the object.
- A JSON error quoted as {"error": "X"} means the body {"error": {"code": "...", "message": "X"}}. The code for each status is in the provider's contract (contracts/, section 3). Only GET /health keeps the seed shape.
- A Purchase row with channel JSON uses a route of the Purchase JSON API (cowork-booking-purchase CONTRACT.md, section 8). Sign-up, login, operator work, plans and the dashboard have no JSON route in v1, so their rows are form rows.

Example data used across the three contexts: clock 2026-10-05 10:00 Bangkok (Monday). Spaces: Meeting Room A (space_id 1, capacity 6, THB 300 per hour), Focus Pod 1 (space_id 2, capacity 2, THB 20 per hour), Board Room (space_id 3, capacity 12, THB 1,000 per hour), Community Table (space_id 4, capacity 8, THB 0 per hour). Standard booking BK-7KQ2M9: Member A, Meeting Room A, 2026-10-07 09:00-10:30 (3 blocks), party size 4, THB 450.00 (amount_satang 45000), hold_expires_at 2026-10-05 10:15, payment session expires_at 10:13, ticket code H7K3-9QXA. Member A pays by card (plan_active false); Member B has plan_active true. Other references in the rows: BK-3MZ8QT (Member B's plan booking, Meeting Room A 2026-10-07 10:30-11:30, ticket code M4TR-8WCE), BK-3HT8WD (Member C, Board Room, 2 blocks, THB 1,000.00), BK-P4W6RC (a booking cancelled before any grant exists), BK-9MZ4RC (Member A, Focus Pod 1, 1 block, THB 10.00), ps_Q7mZ3xK9vT2bN8rL4wYc1A (the standard payment session). JSON times carry the offset, for example "2026-10-07T09:00:00+07:00".

Generated IDs are examples. Tests assert the pattern (^BK-[23456789ABCDEFGHJKMNPQRSTVWXYZ]{6}$ for a booking reference, ^[23456789ABCDEFGHJKMNPQRSTVWXYZ]{4}-[23456789ABCDEFGHJKMNPQRSTVWXYZ]{4}$ for a shown ticket code, and the prefixes ps_, gr_, re_ and pa_) or stub the generator. Where a rule reads a default more precisely than D1-D28 state it, the rule cites the row in DECISIONS.md, "Disputes decided in M1".

## Purchase

### PUR-R01 Register a Member

| Field | Value |
|---|---|
| Rule | Register a Member with a unique email (trimmed, lower-cased), a non-blank display name and a password of at least 8 characters; store only a werkzeug generate_password_hash value (salted and slow, kept from the seed) and check it with check_password_hash; say plainly when the email is already registered. The trimmed email must be ASCII, at most 254 characters and match ^[^@\s]+@[^@\s]+\.[^@\s]+$ (the seed's EMAIL_RE), else 303 to /register with the flash "Enter a valid email" and nothing stored, so a look-alike address (a Cyrillic "а") cannot copy another account's email in the header. The trimmed display name must be 1 to 50 characters, each a letter, combining mark or digit (Unicode categories L, M, N), a space, or one of . ' - (so no "@", "(", ")", control or bidi characters), else "Display name must be 1 to 50 letters, digits or spaces" (a blank one gets "Display name is required"), so a display name cannot imitate the "(email)" part of the header (PUR-R02 row 4). |
| Policy status | Decided (D15, D16) |
| Decision source | Project team (D15, D16). Account data lives on Member in Purchase: Course instructor (class rules PR #10 review on bb9f346, applied in d68631f). |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:443-462 register_user trims and lower-cases the email, hashes the password and returns 409 "email is already registered"; app.py:485-486 the form redirects with that text in `?error=`. |
| Terms | PUR-T01 |
| Candidate responsibility and dependencies | Purchase (Member). No other service is involved. Registration does not log the person in. |
| Open question | PUR-Q04 (email confirmation). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q04; Project team for the rule as stated |
| Next use | Purchase OpenAPI draft and the PRD sign-up story (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | No Member has a@example.com | Submit the sign-up form with email " A@Example.com ", display name "Member A", password "correct-horse" | 303 to /login with the flash "Registered. Please log in."; Member stored with email a@example.com, is_operator false, plan_active false; only the password hash is stored |
| 2 | boundary | form | No Member has b@example.com or c@example.com | Sign up b@example.com with an 8-character password, then c@example.com with a 7-character one | First 303 to /login, registered; second 303 to /register with the flash "Password must be at least 8 characters"; c@example.com is not stored |
| 3 | counterexample | form | a@example.com is registered | Submit the sign-up form with "A@EXAMPLE.COM" | 303 to /register with the flash "Email already registered" (accepted enumeration trade-off, D16); nothing stored; the URL carries no error text |
| 4 | counterexample | form | No Member has c@example.com | Submit the sign-up form with display name "   " | 303 to /register with the flash "Display name is required"; nothing stored |
| 5 | counterexample | form | No Member has any of these addresses | Submit the sign-up form with the email "а@example.com" (a Cyrillic а), then "hello" | 303 to /register with the flash "Enter a valid email" both times; nothing stored |
| 6 | boundary | form | No Member has c@example.com | Sign up c@example.com with the display name "Member A (a@example.com)", then with a 51-character name, then with a 50-character name | The first two get 303 to /register with the flash "Display name must be 1 to 50 letters, digits or spaces" and nothing stored; the 50-character name is stored |

### PUR-R02 Log in with one uniform error

| Field | Value |
|---|---|
| Rule | Log a Member in when the email (in any case) and the password match; answer an unknown email and a wrong password with the same error. |
| Policy status | Decided (D15, D16) |
| Decision source | Project team (D15, D16) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:489-494 login_user gives the same 401 for an unknown email and a wrong password; app.py:508 stores the user id in the cookie session. |
| Terms | PUR-T01, PUR-T03 |
| Candidate responsibility and dependencies | Purchase (Member, login session). |
| Open question | PUR-Q05 (failed-login limits). |
| Clarification owner | Project team, with the course instructor, for PUR-Q05 and the rule as stated |
| Next use | Purchase OpenAPI draft (M2); Purchase tests (M5); e2e "after a decline, the Member is still logged in" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member A is registered | Submit the login form with a@example.com and the right password | 303 to /; `purchase_session` cookie set; the header shows "Member A (a@example.com)": the display name and the email |
| 2 | boundary | form | Same | Submit the login form with "A@Example.COM" and the right password | Logged in, as row 1: the email is matched lower-cased |
| 3 | counterexample | form | Member A is registered; Member C is not | Submit the login form as a@example.com with a wrong password, then as c@example.com | 303 to /login with the flash "Invalid email or password" both times; no session; no `?error=` |
| 4 | counterexample | form | Someone registered attacker@example.com with the display name "Member A" | A cross-site form logs Member A's browser in to that account (login CSRF, accepted in ADR-0016) | The header shows "Member A (attacker@example.com)": the email shows the wrong account (PUR-R01 keeps emails ASCII and display names free of "@" and brackets); an ASCII look-alike such as a@exarnple.com is not refused and can pass a quick glance (accepted, ADR-0016) |

### PUR-R03 A login session ends 12 hours after login

| Field | Value |
|---|---|
| Rule | Treat a login session as valid only while login_at <= clock.now() < login_at + 12 h, whatever the activity; clear the cookie on logout in that browser; set `purchase_session` HttpOnly and SameSite=Lax, plus Secure when PUBLIC_URL starts with https; refuse to start when SECRET_KEY is unset, empty, shorter than 32 characters or the seed's public default (ADR-0019). At login the session stores the member id, the Member's email and login_at; on every request Purchase loads that Member, and a missing row or a different email counts as an ended login (a cookie from before a database reset or restore). On the first request whose purchase_session holds an ended login, Purchase removes the member id, the email and login_at from purchase_session in that same response, keeps the kept path, and flashes "Please log in again" once; the request then runs as anonymous. A route that needs a login (the Member, Owner and Operator routes and /api/bookings*) gives the login step (303 to /login) or 401 {"error": "Please log in again"} (JSON); the public routes (/, /spaces/<id>, GET /api/spaces and /api/spaces/<id>/availability, /register, /login, /logout and /health) answer as for an anonymous visitor, and POST /login and POST /register always run. A request with no login gets "Log in to book" (booking form) or "Please log in" (other pages; JSON 401 {"error": "Please log in"}). |
| Policy status | Decided (D15) |
| Decision source | Project team (D15). SameSite=Lax is the CSRF mitigation: ADR-0009 (SameSite as the CSRF mitigation). |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:20 falls back to a public default SECRET_KEY; app.py:508 and app.py:536 write and pop the user id in the cookie, with no lifetime set anywhere. |
| Terms | PUR-T03 |
| Candidate responsibility and dependencies | Purchase. Store the login instant in the session and compare it with clock.now() on every request (D27); do not rely on Flask's session lifetime, which slides with each request and reads the real clock. Moving the test clock 12 h or more past a login, or back before it, ends that session, so the e2e helper logs every actor in again after such a move (ADR-0013). .env.example leaves SECRET_KEY empty, so a copied example fails fast (ADR-0019). The cookies `payment_session` and `access_session` belong to the other services, which set the same flags (PMT-R19, AXS-R18). Every browser action is a POST (PUR-R37). |
| Open question | None. Replay of a copied cookie after logout, inside the 12 h, is an accepted and documented trade-off (D15). |
| Clarification owner | Project team |
| Next use | ADR-0009 (SameSite as the CSRF mitigation); Purchase tests with the test clock (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member A logged in at 2026-10-05 10:00 | Open My bookings at 14:00 | Page shown; the cookie is HttpOnly and SameSite=Lax |
| 2 | boundary | form | Same | Open My bookings at 22:00 | Redirect to login with the flash "Please log in again" |
| 3 | boundary | JSON | Same; Member A made a request every minute since 10:00 | GET /api/bookings/mine at 22:00 | 401 {"error": "Please log in again"}; activity never extends the session |
| 4 | counterexample | form | Member A logged out at 11:00; a copy of the earlier cookie exists | The copy is replayed at 11:30 | Accepted until 22:00 (documented trade-off); a new login starts a new 12 h |
| 5 | counterexample | internal | SECRET_KEY is unset or empty, for example copied unchanged from .env.example | Start the Purchase service | Non-zero exit with the message "SECRET_KEY is required"; no default key is used |
| 6 | boundary | internal | PUBLIC_URL starts with https | Member A logs in | The cookie also carries Secure; with http it does not |
| 7 | counterexample | form | Member A is logged in; a page on another site holds a form that posts Cancel for BK-7KQ2M9 | Member A's browser submits that form | The browser sends no purchase_session cookie (SameSite=Lax), so Purchase answers with the login step; BK-7KQ2M9 is unchanged. Proof: a Purchase test asserts SameSite=Lax on the Set-Cookie and that the POST without the cookie gets 303 to /login; the cross-site browser behaviour is a manual check from a page on a second hostname |
| 8 | counterexample | internal | Member A logged in with the test clock at 2026-10-07 10:00; the clock is then set back to 2026-10-05 10:00 | Member A opens My bookings | Login step: login_at is after now, so the session is not valid |
| 9 | boundary | JSON | Member A is logged in on Purchase; same browser, all three services on localhost | A card is declined on /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A, then Member A gets /api/bookings/mine | 200: the decline set only Payment's own cookie; purchase_session is untouched because each service uses its own cookie name (D15) |
| 10 | boundary | form | Member A logged in at 2026-10-04 22:05 and created BK-7KQ2M9 at 10:00; the login ends at 10:05; Member A pays on the hosted page at 10:06 | The browser returns to /bookings/BK-7KQ2M9/return | 303 to /login with "Please log in again"; after logging in, 303 to /bookings/BK-7KQ2M9/return (PUR-R05), which reconciles and shows Confirmed |
| 11 | counterexample | internal | SECRET_KEY is "x", or "changeme" | Start the Purchase service | Non-zero exit with the message "SECRET_KEY must be at least 32 characters" |
| 12 | boundary | form | Member A's login ended (12 h passed) | Member A opens /login, then posts the login form with the right password | GET /login: 200 with the flash "Please log in again", no redirect, and the cookie no longer holds the member id; the POST logs in and answers 303 to the kept path, else / |
| 13 | boundary | JSON | Same | GET /api/spaces, then GET /api/spaces/1/availability?date=2026-10-07&blocks=3 | 200 both times, as for an anonymous visitor; an ended login never blocks a public route |
| 14 | counterexample | form | Member A logged in as member id 1; the Purchase database is then reset (or restored) and the Operator registers first, so the Operator now has member id 1 | Member A's browser opens My bookings with the old cookie | Login step with "Please log in again": the email stored in the session does not match the Member with id 1, so the browser is never logged in as the Operator |
| 15 | counterexample | internal | SECRET_KEY is "dev-secret-key-not-for-production", the seed's public default (33 characters) | Start the Purchase service | Non-zero exit with the message "SECRET_KEY is the public seed default" |

### PUR-R04 Promote the operator by OPERATOR_EMAIL

| Field | Value |
|---|---|
| Rule | Set `is_operator` true when the Member whose email equals OPERATOR_EMAIL (compared lower-cased) registers or logs in; no other path makes an operator, and is_operator is never removed automatically. |
| Policy status | Decided (D15) |
| Decision source | Project team (D15). The no-demotion reading and the accepted OPERATOR_EMAIL risk: DECISIONS.md, Disputes decided in M1, row 5. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:69-80 the users table has no role or operator column. |
| Terms | PUR-T01, PUR-T02 |
| Candidate responsibility and dependencies | Purchase. OPERATOR_EMAIL is a deploy setting (env var). Demotion is a manual step in v1: `UPDATE members SET is_operator = false WHERE email = '...'` on the Purchase database; the Purchase README gives the command. Change OPERATOR_EMAIL first, or the next login promotes the account again. |
| Open question | PUR-Q04 (email confirmation would close the OPERATOR_EMAIL risk). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q04; Project team for the rule as stated |
| Next use | Purchase README env list (M5); e2e operator cancel and refund retry (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | OPERATOR_EMAIL holds the Operator's address; no Member has it | The Operator submits the sign-up form with that address | 303 to /login; the stored Member has is_operator true |
| 2 | ordinary | form | The Operator registered before OPERATOR_EMAIL was set, so is_operator is false | The Operator logs in through the form | is_operator set true; operator links appear |
| 3 | boundary | form | Same | The Operator logs in with the address in upper case | Promoted (compared lower-cased) |
| 4 | counterexample | form | OPERATOR_EMAIL holds the Operator's address | Member A submits the sign-up form with a@example.com | 303 to /login; is_operator false |
| 5 | counterexample | internal | OPERATOR_EMAIL is unset | Anyone registers or logs in | Nobody is promoted |
| 6 | counterexample | internal | OPERATOR_EMAIL holds the Operator's address; nobody has registered it yet | Someone else registers that address first | That account is promoted. Accepted risk while v1 has no email confirmation (PUR-Q04); register the operator account right after first start (README quick start) |
| 7 | boundary | internal | The Operator is promoted; OPERATOR_EMAIL is then changed to another address | The Operator logs in again | is_operator stays true: it is never removed automatically; the new address is promoted when its Member registers or logs in |
| 8 | counterexample | form | The wrong account holds is_operator (it registered the OPERATOR_EMAIL address first); OPERATOR_EMAIL has been changed | The admin runs the README's manual demotion step; that account then opens /operator/bookings | 404: is_operator is false from its next request; its own bookings are unchanged |

### PUR-R05 Log in to book; see only your own bookings

| Field | Value |
|---|---|
| Rule | Require login to book and to see My bookings; show a booking and its actions only to its owning Member or an operator, and answer any other logged-in Member with 404; an anonymous request gets the login step (form) or 401 (JSON) before any lookup. The form's login step keeps a local GET path in the signed session cookie, never in the URL, and after a successful login sends the browser there (303) only if the path starts with "/", its second character is neither "/" nor "\", and it holds no control character, else to /; Purchase builds the kept path itself from the refused route (url_for plus the known date and blocks), never from a request field; it keeps only GET paths: for a refused booking POST the kept path is the space page with its date and blocks, and for a refused POST on /bookings/<ref>/... it is /bookings/<ref>. The kept path survives POST /register and is used at the next successful login. "Continue to payment" and "Book again" show only to the booking's own Member; an operator viewing another Member's booking gets no button that would book in the operator's own name. An ended login gets "Please log in again" once and is anonymous from then on, so public pages, /register and /login still answer; no login gets "Log in to book" (booking form) or "Please log in" (PUR-R03). An anonymous visitor's space page shows the pay-coverage review and cancellation terms (for a space whose rate is 0, the free review "THB 0.00" with no refund line), and its one button reads "Log in to book": the login step keeps the space page with its date and blocks, and the start, party size and note are chosen again after login. The owner's booking page shows the party size and the note, as an operator's does. |
| Policy status | Decided (D15, D17) |
| Decision source | Project team (D15, D17). The login step or 401 for anonymous callers refines D17: DECISIONS.md, Disputes decided in M1, row 1. The e-ticket URL in Access is a bearer link: ADR-0008 (bearer ticket link). |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:871-889 /bookings/mine is the only route that checks the session owner; app.py:902 and app.py:917 read and delete any booking by id for anyone. |
| Terms | PUR-T01, PUR-T02, PUR-T17 |
| Candidate responsibility and dependencies | Purchase. The booking's name and email come from the logged-in Member, never from a typed field. The e-ticket page (Access) is not covered here. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | PRD roles and stories (M2); e2e "non-owner 404 on Purchase" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member A owns BK-7KQ2M9 | Open its booking page | 200: status, reference, times, price, coverage, payment outcome, "Party of 4" and the note, "View e-ticket" link |
| 2 | ordinary | JSON | The Operator is logged in | Get BK-7KQ2M9 | 200 with the booking |
| 3 | counterexample | JSON | Member B is logged in | Get BK-7KQ2M9, then an unknown BK-2222ZZ | 404 both times, same body |
| 4 | counterexample | form | Member B is logged in | Post Cancel for BK-7KQ2M9 | 404 page; the booking is unchanged |
| 5 | counterexample | form | Nobody is logged in | Press "Log in to book" (the anonymous page's button) on Meeting Room A, 2026-10-07, 3 blocks | Redirect to login with the flash "Log in to book"; no booking created; after logging in, 303 to /spaces/1?date=2026-10-07&blocks=3 |
| 6 | counterexample | JSON | Nobody is logged in | Send a booking request, or get BK-7KQ2M9 | 401; nothing looked up or created |
| 7 | boundary | JSON | Member A is logged in; BK-7KQ2M9 is cancelled | Member A gets BK-7KQ2M9 | 200 with status cancelled: ownership does not end with the booking |
| 8 | boundary | form | Member A's login ended; BK-7KQ2M9 has a pending refund | Member A presses Retry (POST /bookings/BK-7KQ2M9/retry), logs in, or first signs up at /register and then logs in | 303 to /login with "Please log in again"; after the login, 303 to /bookings/BK-7KQ2M9 (the kept GET path), never a GET of the retry URL (405) |
| 9 | counterexample | form | BK-7KQ2M9 is held; the Operator is logged in | The Operator opens /bookings/BK-7KQ2M9 | The deadline, Cancel and Reconcile, but no "Continue to payment" and no "Book again"; a crafted POST /spaces/1/book by the Operator is an ordinary booking by the Operator under the Operator's own hold rules (PUR-R39) |
| 10 | boundary | form | Member A's login ended (its 12 h have passed) | Member A posts the booking form for Meeting Room A, 2026-10-07, 3 blocks | 303 to /login with "Please log in again", not "Log in to book"; nothing created; after the login, 303 to /spaces/1?date=2026-10-07&blocks=3 |
| 11 | counterexample | internal | The session holds the kept path "/\evil.example", or a path with a CR or LF | Member A logs in | 303 to "/": the kept path is used only if its second character is neither "/" nor "\" and it holds no control character |

### PUR-R06 Operator pages are for operators only

| Field | Value |
|---|---|
| Rule | Let only an operator create, edit and archive spaces, list all bookings with Cancel, use the operator Retry (POST /operator/bookings/<ref>/retry, the only way to start refund attempt+1 after a failed refund, PUR-R33), run Reconcile, set a Member's `plan_active` (the button sends the target value, true or false; turning a plan off flashes the Member's upcoming confirmed plan bookings, which stay plan under D10: "Plan off for b@example.com; upcoming plan bookings: BK-3MZ8QT") and see the dashboard; answer a logged-in non-operator with 404 and an anonymous caller with the login step before any lookup. These are browser pages only: v1 has no JSON route for them. A booking's owner keeps the owner's Retry of pending steps (PUR-R32). |
| Policy status | Decided (D15, D17) |
| Decision source | Project team (D15, D17). The 404 for non-operators applies D17's "everyone else gets 404" to operator pages; the login step or 401 for anonymous callers is DECISIONS.md, Disputes decided in M1, row 1. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:570, app.py:620 and app.py:663 create, edit and delete spaces for anyone; app.py:891 lists every booking to anyone; app.py:1034 shows the dashboard to anyone; app.py:1004 lets anyone subscribe any name. |
| Terms | PUR-T02, PUR-T25 |
| Candidate responsibility and dependencies | Purchase. Retry and Reconcile call Payment and Access (PUR-R24, PUR-R26, PUR-R32, PUR-R33). |
| Open question | PUR-Q02 (selling plans instead of the operator toggle). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q02; Project team for the rule as stated |
| Next use | PRD operator stories and screen list (M2); e2e operator cancel (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | The Operator is logged in | Open the all-bookings list | Every booking with its status; Cancel only on held bookings and on confirmed bookings before their end; Retry only on bookings with a pending or failed step; Reconcile only on held rows; a pending revoke is flagged "Revocation pending" (PUR-Q12); each row carries data-booking-reference and data-flags. With no booking yet: "No bookings yet" |
| 2 | ordinary | form | The Operator is logged in | Post plan_active=true for Member B on /operator/members | 303 to /operator/members with the flash "Plan on for b@example.com"; only bookings Member B creates after this get coverage plan |
| 3 | counterexample | form | Member A is logged in | Open /operator/bookings, or post the create-space form to /operator/spaces | 404 page; nothing changes |
| 4 | counterexample | form | Member A is logged in | Open the dashboard | 404 page |
| 5 | counterexample | form | Nobody is logged in | Open the dashboard, or the all-bookings list | Redirect to login with the flash "Please log in"; nothing looked up |
| 6 | counterexample | form | Member A is logged in | Member A posts plan_active=true to /operator/members/<Member A's id>/plan | 404; plan_active stays false |
| 7 | counterexample | form | Member A is logged in; BK-7KQ2M9 held | Member A posts /operator/bookings/BK-7KQ2M9/reconcile, or /operator/bookings/reconcile | 404; nothing is reconciled |
| 8 | counterexample | JSON | Member A, or nobody, is logged in | GET /api/dashboard | 404 not_found: v1 has no JSON operator route, and an unknown /api path is 404 |
| 9 | boundary | form | Member B already has plan_active true | The Operator double-clicks the button on Member B's row, which sends plan_active=false twice | First "Plan off for b@example.com"; the second post changes nothing and flashes the same; plan_active stays false |
| 10 | counterexample | form | The Operator is logged in | Post to /operator/members/<Member B's id>/plan with no field, or plan_active=yes | 303 with the flash "Plan must be true or false"; nothing changes: there is no toggle |
| 11 | ordinary | form | Member B has plan_active true and an upcoming confirmed plan booking BK-3MZ8QT | The Operator turns Member B's plan off | 303 with the flash "Plan off for b@example.com; upcoming plan bookings: BK-3MZ8QT"; BK-3MZ8QT stays plan; the Operator can cancel it from All bookings |

### PUR-R07 Times carry an offset; the form sends a date and a block

| Field | Value |
|---|---|
| Rule | Accept a JSON time only as ISO 8601 with an offset and answer a naive time with 400; build the instant on the server from the form's Bangkok date and start block; store timestamptz; show and return times in Bangkok time, a fixed UTC+7 offset. |
| Policy status | Decided (D2) |
| Decision source | Project team (D2) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:143-151 parse_time rejects a time without an offset; app.py:191-200 parse_form_time reads the same text as UTC+7; app.py:188 LOCAL_TZ is a fixed UTC+7 offset. |
| Terms | PUR-T08, PUR-T09 |
| Candidate responsibility and dependencies | Purchase. Access receives valid_from and valid_until with the +07:00 offset (PUR-R27). No tz database is needed. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Purchase OpenAPI draft (time formats) and contracts (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A is logged in | Book Meeting Room A with start "2026-10-07T09:00:00+07:00", 3 blocks | Accepted; the booking returns start "2026-10-07T09:00:00+07:00" and end "2026-10-07T10:30:00+07:00" |
| 2 | boundary | JSON | Same | Book with start "2026-10-07T02:00:00Z" | Same instant, accepted; returned as "2026-10-07T09:00:00+07:00" |
| 3 | counterexample | JSON | Same | Book with start "2026-10-07T09:00:00" (no offset) | 400 "Time needs an offset, for example +07:00" |
| 4 | ordinary | form | Same | Pick date 2026-10-07 and start block 09:00 | Server builds 2026-10-07T09:00:00+07:00; the page shows "2026-10-07 09:00" |
| 5 | counterexample | internal | The server process runs with TZ=UTC | Any of the rows above | Same results; the server's own zone is never used |

### PUR-R08 Book inside opening hours

| Field | Value |
|---|---|
| Rule | Accept a booking only if it starts at or after 08:00 and ends at or before 20:00 on the same Bangkok date, every day. |
| Policy status | Decided (D3) |
| Decision source | Project team (D3) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:712-713 book_space checks only that the end is after the start. |
| Terms | PUR-T11, PUR-T08 |
| Candidate responsibility and dependencies | Purchase. The start-block grid (PUR-R13) applies the same limits; no other service is involved. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Start-block grid (PUR-R13); utilization denominator of 12 h a day (PUR-R34); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A is logged in | Book start "2026-10-07T09:00:00+07:00", 3 blocks | Accepted |
| 2 | boundary | JSON | Same | Book start "2026-10-07T19:30:00+07:00" for 1 block, then for 2 blocks | First accepted (ends 20:00); second 400 "Outside opening hours 08:00-20:00" |
| 3 | boundary | JSON | Same | Book start "2026-10-07T08:00:00+07:00" for 1 block, then "2026-10-07T07:30:00+07:00" for 1 block | First accepted; second 400 |
| 4 | counterexample | JSON | Same | Book start "2026-10-07T23:30:00+07:00" for 2 blocks (would end 00:30 the next day) | 400; a booking never crosses midnight |
| 5 | boundary | form | Same | Post a crafted form with date 2026-10-07, block 19:30, 2 blocks | Back to the space page with the flash "Outside opening hours 08:00-20:00"; the grid itself greys that start as "Runs past 20:00" |

### PUR-R09 Start on the half hour; book 1 to 8 blocks

| Field | Value |
|---|---|
| Rule | Accept a start only at exactly :00 or :30 Bangkok time and a duration of 1 to 8 whole blocks; the end is start + blocks x 30 min and is exclusive; anything else gives 400. |
| Policy status | Decided (D4) |
| Decision source | Project team (D4) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:712-713 accepts any interval whose end is after its start; purchase.py:6-15 prices any number of seconds. |
| Terms | PUR-T09, PUR-T10 |
| Candidate responsibility and dependencies | Purchase. The price (PUR-R17) and the grid (PUR-R13) use the block count; no other service is involved. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Price calculation (PUR-R17); Purchase OpenAPI draft (M2); Purchase unit test for block alignment and duration (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A is logged in | Book start "2026-10-07T09:00:00+07:00", 3 blocks | Accepted; end "2026-10-07T10:30:00+07:00" |
| 2 | boundary | JSON | Same | Book start "2026-10-07T08:00:00+07:00" for 8 blocks, then for 9 blocks, then for 0 blocks | First accepted (end "2026-10-07T12:00:00+07:00"); the others 400 "Duration must be 1 to 8 blocks" |
| 3 | counterexample | JSON | Same | Book with start "2026-10-07T09:15:00+07:00" | 400 "Start on :00 or :30" |
| 4 | counterexample | JSON | Same | Book with start "2026-10-07T09:00:30+07:00" | 400 (seconds are not allowed) |
| 5 | ordinary | form | Same | Open Meeting Room A | Duration offered as 1 to 8 blocks (30 min to 4 h); the grid offers starts only on the half hour |
| 6 | counterexample | form | Same | Post a crafted booking form with date 2026-10-07 and block "09:15" | Back to the space page with the flash "Pick a start on the half hour"; no booking |

### PUR-R10 Book at least 60 minutes ahead and at most 30 days out

| Field | Value |
|---|---|
| Rule | Accept a start only if it is at least 60 min after `clock.now()` and its Bangkok date is at most today + 30 days. |
| Policy status | Decided (D5) |
| Decision source | Project team (D5) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:700-772 book_space never compares the start with the current time, so past bookings are accepted. |
| Terms | PUR-T12, PUR-T13, PUR-T08 |
| Candidate responsibility and dependencies | Purchase. Depends on the test clock (D27) for checks. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Date picker limits and start-block grid (PUR-R13); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Clock 2026-10-05 10:00 | Member A books start "2026-10-07T09:00:00+07:00" | Accepted |
| 2 | boundary | JSON | Same | Book start "2026-10-05T11:00:00+07:00", then "2026-10-05T10:30:00+07:00" | First accepted (exactly 60 min); second 400 "Book at least 60 minutes ahead" |
| 3 | boundary | JSON | Same | Book start "2026-11-04T09:00:00+07:00", then "2026-11-05T09:00:00+07:00" | First accepted (today + 30 days); second 400 "Book at most 30 days ahead" |
| 4 | counterexample | JSON | Same | Book start "2026-10-04T09:00:00+07:00" | 400; past starts are never accepted |
| 5 | boundary | form | Same | Open Meeting Room A | The date input has min 2026-10-05 and max 2026-11-04; a crafted date 2026-11-05 gets the flash "Pick a date from today to 30 days ahead" |
| 6 | boundary | JSON | Clock 2026-10-05 10:00:01 | Member A books start "2026-10-05T11:00:00+07:00" | 400 "Book at least 60 minutes ahead" (1 second short) |

### PUR-R11 No gap between bookings

| Field | Value |
|---|---|
| Rule | Keep no cleaning gap: a booking may start exactly when another booking of the same space ends. |
| Policy status | Decided (D6) |
| Decision source | Project team (D6). A cleaning gap is not approved; it stays an open question. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:130-135 the EXCLUDE range tstzrange(start_time, end_time) excludes its end, so back-to-back bookings pass. |
| Terms | PUR-T14, PUR-T21 |
| Candidate responsibility and dependencies | Purchase. Access gets no early entry while the buffer is 0 (PUR-R27). |
| Open question | PUR-Q01 (cleaning gap). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q01; Project team for the rule as stated |
| Next use | Slot-blocking check (PUR-R12); check-in window values (PUR-R27); Purchase test for adjacent bookings (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | BK-7KQ2M9 is confirmed for 2026-10-07 09:00-10:30; no other booking of Meeting Room A that day | Member B books Meeting Room A with start "2026-10-07T10:30:00+07:00", 2 blocks | Accepted (adjacent): this is BK-3MZ8QT, 10:30-11:30 |
| 2 | boundary | JSON | Same | Member B books start "2026-10-07T08:00:00+07:00", 2 blocks | Accepted; its end equals the other start |
| 3 | counterexample | JSON | Same | Member B books start "2026-10-07T10:00:00+07:00", 2 blocks | 409 {"error": "Slot just taken"}; 30 minutes overlap |
| 4 | boundary | form | BK-7KQ2M9 is confirmed for 2026-10-07 09:00-10:30; nothing else booked that day | Member B opens the grid for 2026-10-07, 2 blocks, and books 10:30 | 10:30 is marked available; booking it succeeds (Member B's plan booking is confirmed): no gap is kept after 10:30 |

### PUR-R12 Only slot-blocking bookings take a slot

| Field | Value |
|---|---|
| Rule | Treat a slot as taken only by a slot-blocking booking of the same space: status confirmed, or status held with `hold_expires_at` later than `clock.now()` passed as a query parameter; every availability read and the booking check use this predicate; every slot conflict answers the same, 409 {"error": "Slot just taken"} (JSON) or the flash "Slot just taken" (form), whether the pre-check or the EXCLUDE constraint finds it, except an overlapping lapsed hold the pre-insert sweep could not reconcile, which answers 503 (PUR-R22). |
| Policy status | Decided (D11) |
| Decision source | Project team (D11) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:731-737 the overlap pre-check ignores payment; app.py:130-135 the EXCLUDE constraint covers every row, so an unpaid booking blocks its slot until it is deleted. |
| Terms | PUR-T21, PUR-T20, PUR-T19 |
| Candidate responsibility and dependencies | Purchase. No SQL uses now(); `clock.now()` is a parameter (D27). The grid never offers a booked start, so a Member meets a conflict only in a race or with a crafted request; one text for both paths lets a race test assert the body. |
| Open question | PUR-Q01 (cleaning gap); PUR-Q12 (revocation pending while the slot is rebooked). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q01; Project team for PUR-Q12 and the rule as stated |
| Next use | Start-block grid (PUR-R13); insert guard (PUR-R22); e2e "hold expiry frees the slot" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | BK-7KQ2M9 is confirmed for 2026-10-07 09:00-10:30 | Member B books Meeting Room A with start "2026-10-07T10:00:00+07:00", 2 blocks | 409 {"error": "Slot just taken"} |
| 2 | ordinary | form | Same | Member B posts the booking form for 10:00-11:00 | Back to the space page with the flash "Slot just taken" |
| 3 | boundary | internal | BK-7KQ2M9 is held, `hold_expires_at` 2026-10-05 10:15 | Check the slot at 10:14, then at 10:15 | Blocking at 10:14; not blocking at 10:15 (`hold_expires_at` must be later than now) |
| 4 | counterexample | JSON | A booking for 09:00-10:30 exists with status expired, and another with status cancelled | Member B books start "2026-10-07T09:00:00+07:00", 3 blocks | Accepted; expired and cancelled bookings never block |

### PUR-R13 Show the start-block grid with reasons

| Field | Value |
|---|---|
| Rule | For a space, a date within the horizon and a duration, list every start from 08:00 to 19:30 and mark it available only if all its blocks are inside opening hours, past the notice period and free of slot-blocking bookings; grey every other start with one reason, the first that applies: "Too soon", then "Runs past 20:00", then "Booked"; answer a date outside today to today + 30 days with 400 "Pick a date from today to 30 days ahead". |
| Policy status | Decided (D4, D11) |
| Decision source | Project team (D4, D11) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:170-185 booked_space_ids answers only "booked right now" or for a free-form window; app.py:413-441 the home page shows free or booked right now and lists every upcoming booking's times (A13). |
| Terms | PUR-T15, PUR-T09, PUR-T10, PUR-T11, PUR-T12, PUR-T13, PUR-T21 |
| Candidate responsibility and dependencies | Purchase. The grid is a read: it never reconciles and never holds a slot. |
| Open question | PUR-Q01 (cleaning gap). The reason texts are UI wording and may be refined in the M2 screen list. |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q01; Project team for the reason texts and the rule as stated |
| Next use | PRD UX flow "pick a start block" (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Clock 2026-10-05 10:00; Meeting Room A has no bookings on 2026-10-07 | Member A opens Meeting Room A, date 2026-10-07, 3 blocks | 24 starts 08:00 to 19:30; 08:00 to 18:30 available; 19:00 and 19:30 greyed "Runs past 20:00" |
| 2 | ordinary | JSON | Same | Ask for the grid of space 1, date 2026-10-07, 3 blocks | 24 entries, each with start (ISO with +07:00), available true or false, and a reason when false |
| 3 | boundary | form | BK-7KQ2M9 confirmed 09:00-10:30 | Open date 2026-10-07, 2 blocks | 08:00 available (ends 09:00); 08:30, 09:00, 09:30, 10:00 greyed "Booked"; 10:30 available |
| 4 | boundary | form | Clock 2026-10-05 10:00 | Open date 2026-10-05, 1 block | 08:00 to 10:30 greyed "Too soon"; 11:00 available (exactly 60 min) |
| 5 | counterexample | JSON | BK-7KQ2M9 held with `hold_expires_at` 10:15, not yet reconciled; clock 10:16 | Ask for the grid of 2026-10-07, 3 blocks | 09:00 is available; a lapsed hold is not slot-blocking even before it is marked expired |
| 6 | counterexample | JSON | Clock 2026-10-05 10:00 | Ask for the grid of 2026-11-05 | 400 "Pick a date from today to 30 days ahead" |
| 7 | boundary | form | Clock 2026-10-05 10:00; a confirmed booking of Meeting Room A 2026-10-05 10:30-11:00 | Open date 2026-10-05, 1 block | 10:30 greyed "Too soon", not "Booked": the first reason that applies wins |
| 8 | counterexample | JSON | Clock 2026-10-05 10:00 | Ask for the grid of 2026-10-04 | 400 "Pick a date from today to 30 days ahead" |


### PUR-R14 A booking is the whole room for 1 to capacity people

| Field | Value |
|---|---|
| Rule | Sell exclusive use of the whole room; accept a party size that is a whole number from 1 to the space's capacity at creation, and a note of at most 500 characters ("Note must be at most 500 characters"); never change existing bookings when capacity is lowered later. |
| Policy status | Decided (D7) |
| Decision source | Project team (D7). Answers the course instructor's class question Q01 (class rules base a853795): what do we sell, and what happens when capacity falls. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:716-727 checks party size against capacity on the JSON path only; app.py:806 the form always sends 1; app.py:746-748 the INSERT never stores the party size. |
| Terms | PUR-T04, PUR-T05, PUR-T16 |
| Candidate responsibility and dependencies | Purchase. Capacity comes from the space (PUR-R15); party size is stored on the booking; no other service is involved. |
| Open question | None. Class question Q01 is answered by D7 (ID_MAP.md). |
| Clarification owner | Project team |
| Next use | Booking form and PRD story (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Meeting Room A, capacity 6 | Member A books the standard slot with party_size 4 | Accepted; party size 4 stored |
| 2 | ordinary | form | Same | Member A opens the booking form | Party size offered 1 to 6; Member A picks 4 and continues |
| 3 | boundary | JSON | Same | Book the standard slot with party_size 7, then 0, then 6 | 7 and 0 get 400 "Party size must be 1 to 6" and store nothing; then 6 is accepted |
| 4 | counterexample | JSON | Member B has a confirmed Board Room booking 2026-10-07 09:00-10:00 with party size 1 | Member C books Board Room with start "2026-10-07T09:30:00+07:00", 2 blocks, party_size 5 | 409 {"error": "Slot just taken"}; the whole room is taken, whatever the party size |
| 5 | counterexample | internal | BK-7KQ2M9 confirmed with party size 4 | The Operator lowers Meeting Room A capacity to 3 | BK-7KQ2M9 is unchanged and stays confirmed; new bookings need party size 1 to 3 |
| 6 | counterexample | form | Same | Post a crafted booking form with party size 7 | Back to the space page with the flash "Party size must be 1 to 6"; no booking |
| 7 | boundary | JSON | Meeting Room A, capacity 6 | Book the standard slot with a note of 501 characters, then of 500 | 501: 400 "Note must be at most 500 characters", nothing stored; 500: accepted |

### PUR-R15 Space values

| Field | Value |
|---|---|
| Rule | Give every space a non-blank name that no other non-archived space uses (compared trimmed and case-insensitive; "Name already used" otherwise), a whole-number capacity from 1 to 1,000 and an hourly rate in whole THB that is 0 or from 20 to 10,000; refuse out-of-range input with 303 back to the operator spaces page and a flashed message, never a 500. Checks run in this order and stop at the first failure: name required ("Name is required" for a blank or spaces-only name), name already used, capacity, rate; then the save. Typed values are not kept. |
| Policy status | Decided (D7, D9) |
| Decision source | Project team (D7, D9). The capacity maximum refines D7: DECISIONS.md, Disputes decided in M1, row 3. The rate range makes every block price an exact satang amount and every chargeable booking at least THB 10. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:207 and app.py:216 check only capacity at least 1 and price at least 0, with no upper bound; app.py:46-47 price_cents is INTEGER, so a huge value fails with a 500. |
| Terms | PUR-T04, PUR-T05, PUR-T06 |
| Candidate responsibility and dependencies | Purchase (operator actions, PUR-R06). A rename affects new grants only: Access keeps the space_name it was sent, so issued e-tickets keep the old name, and the kiosk label for that room changes once a grant with the new name has the greatest valid_from (within the 30-day horizon, AXS-R11). The kiosk shows the room number with every label, "Meeting Room A (room 1)", because an archived space's name can be used again (AXS-R11). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Space pages and Purchase OpenAPI draft (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | The Operator is logged in | Save "Focus Pod 1", capacity 2, rate 20 (THB) on the space form | 303 to /operator/spaces with the flash "Space saved"; stored as 2000 satang; shown as "THB 20.00 per hour, THB 10.00 per 30 min" |
| 2 | ordinary | form | Same | Save "Meeting Room A", capacity 6, rate 300 (THB) on the space form | Saved as 30000 satang; shown as "THB 300.00 per hour, THB 150.00 per 30 min" |
| 3 | boundary | form | Same | Save "Pod R0" with rate 0, "Pod R20" with 20 and "Pod R10000" with 10000 (THB), then "Pod R19" with 19 and "Pod R10001" with 10001 | The first three saved; "Pod R19" and "Pod R10001" get 303 with the flash "Rate must be 0 or 20 to 10,000 THB per hour" and nothing saved |
| 4 | counterexample | form | Same | Save a space with rate 25.50 | 303 with the flash "Rate must be 0 or 20 to 10,000 THB per hour": whole THB only; nothing saved |
| 5 | counterexample | form | Same | Save a space with capacity 0, or capacity 99999999999 | 303 to /operator/spaces with the flash "Capacity must be a whole number from 1 to 1,000"; never a 500 |
| 6 | boundary | form | Same | Save "Hall 1000" with capacity 1000, then "Hall 1001" with capacity 1001 | "Hall 1000" saved; then 303 with the flash "Capacity must be a whole number from 1 to 1,000" and "Hall 1001" not saved |
| 7 | boundary | internal | The grant for BK-7KQ2M9 is issued with space_name "Meeting Room A" | The Operator renames space 1 to "Meeting Room Alpha" | New grant requests send "Meeting Room Alpha"; the BK-7KQ2M9 e-ticket still shows "Meeting Room A"; the kiosk label for room 1 changes once a grant with the new name has the latest valid_from, which can take up to 30 days |
| 8 | counterexample | form | Meeting Room A (space_id 1) is not archived | The Operator creates a space named "meeting room a ", or renames Focus Pod 1 to "Meeting Room A" | 303 to /operator/spaces with the flash "Name already used"; nothing saved. An archived space's name can be used again, so the kiosk can list two rooms with one name, told apart by room number (AXS-R11 row 14) |
| 9 | counterexample | form | The Operator is logged in | Save a space with the name "   " (spaces only), capacity 0 and rate 19 | 303 to /operator/spaces with the flash "Name is required" only (the first failing check); nothing saved |

### PUR-R16 Archive a space; never delete it

| Field | Value |
|---|---|
| Rule | Let the operator archive a space only when it has no held or confirmed booking whose end is after `clock.now()`, and name those bookings in the refusal ("Cancel its upcoming bookings first: BK-7KQ2M9", a held one marked "(held)"); hide an archived space from browsing and booking and keep its history; never delete a space. An archived space stays archived and cannot be edited in v1: POST /operator/spaces/<id> for it gets 404, like an unknown space (PUR-Q13). The spaces admin page lists archived spaces last, marked "Archived 2026-10-07", with no edit or archive form; a repeat archive POST for an archived space (a double click or a stale page) answers 303 /operator/spaces with "Space archived" and leaves archived_at unchanged. |
| Policy status | Decided (D23) |
| Decision source | Project team (D23). Answers class question Q06 (class rules PR #5 at 0712a1c): archive instead of delete. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:663-682 deletes a space unless a booking row references it (409 "space has bookings, cancel them first"), and app.py:917-930 cancel deletes bookings, so retiring a space erases its history. |
| Terms | PUR-T04, PUR-T07, PUR-T19 |
| Candidate responsibility and dependencies | Purchase. The operator cancels upcoming bookings first (PUR-R30). Archive does not reconcile; the operator runs Reconcile first when a lapsed hold is in the way. Archive checks and sets archived_at in one transaction that holds the space row FOR UPDATE; the booking insert (PUR-R22) locks the same space row FOR SHARE and re-checks archived_at, so a booking and an archive cannot both win. |
| Open question | PUR-Q13 (unarchive a space). |
| Clarification owner | Project team |
| Next use | Operator stories (M2); utilization denominator (PUR-R34); Purchase archive tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Community Table has only past bookings | The Operator presses Archive on it at /operator/spaces | 303 to /operator/spaces with the flash "Space archived"; gone from the spaces list; its past bookings still show in My bookings and the all-bookings list |
| 2 | ordinary | JSON | Same, after row 1 | GET /api/spaces, then GET /api/spaces/4/availability?date=2026-10-07&blocks=1 | Space 4 is not listed; the availability read gets 404 |
| 3 | counterexample | form | BK-7KQ2M9 confirmed, ends 2026-10-07 10:30; clock 2026-10-05 11:00 | The Operator presses Archive on Meeting Room A | 303 to /operator/spaces with the flash "Cancel its upcoming bookings first: BK-7KQ2M9"; nothing changes |
| 4 | boundary | form | Same; clock 2026-10-07 10:30 | The Operator presses Archive on Meeting Room A | 303 with the flash "Space archived": the end is not after now |
| 5 | boundary | internal | Meeting Room A has no upcoming booking | Member B's booking insert for Meeting Room A and the Operator's archive arrive together | The space row lock orders them: either the booking commits first and the archive gets "Cancel its upcoming bookings first" naming it, or the archive commits first and the booking gets 404; never an upcoming booking in an archived space |
| 6 | counterexample | JSON | Community Table is archived | Member A books it with POST /api/bookings | 404; nothing created |
| 7 | counterexample | form | Community Table is archived | The Operator sends DELETE /operator/spaces/4 | 405; the space row stays |
| 8 | boundary | form | Community Table was archived at 2026-10-07 10:00 | The Operator presses Archive on it again from a stale page at 10:05 | 303 to /operator/spaces with the flash "Space archived"; archived_at stays 2026-10-07 10:00; the page lists it last as "Archived 2026-10-07" with no forms |

### PUR-R17 Booking price is fixed at creation

| Field | Value |
|---|---|
| Rule | For a booking not covered by a subscription (pay or free coverage: the clarified scope), set `agreed_price_satang` = round_half_up(hourly rate in satang at creation x blocks / 2) once at creation, store it and never recalculate it; Payment collects it and never re-prices it. |
| Policy status | Stakeholder-clarified (course instructor, class rules PR #14 at 25ca71e) |
| Decision source | Course instructor (class rules PR #14 at 25ca71e, merged as 58a1477): hourly rate at creation x duration, rounded half up, owned by Purchase; Payments consumes the recorded amount without recalculating it. Project team (D8) applies it to whole blocks and satang. Plan bookings are outside the clarified scope ("subscription coverage remains PAY-R01"); PUR-R19 stores their price (D8, D10). Course [contexts site]: "Payments does not re-price the booking." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, purchase.py:6-15 calculate_booking_price_cents returns (rate x seconds + 1800) // 3600, the same half-up formula over seconds. |
| Terms | PUR-T23, PUR-T06, PUR-T09, PUR-T10 |
| Candidate responsibility and dependencies | Purchase owns the calculation. Payment receives amount_satang in the session request (PUR-R23) and computes no price. Plan bookings: see PUR-R19. |
| Open question | None for the formula. Whole blocks make the class's fractional-second question moot, and D9 makes every block price an exact satang amount, so the rounding never changes a value. PUR-Q07 covers bookings without a stored price. |
| Clarification owner | Course instructor (class rules PR #14 at 25ca71e) for the formula; Project team for PUR-Q07 |
| Next use | purchase to payment contract, amount_satang (M2); Purchase unit test with these rows (M5); e2e happy path and "different amount gets 409" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Meeting Room A at THB 300 per hour | Member A books start "2026-10-07T09:00:00+07:00", 3 blocks | agreed_price_satang 45000 (30000 x 3 / 2) |
| 2 | ordinary | form | Same | Member A reaches the review step | Shows "THB 450.00" before "Continue to payment" |
| 3 | boundary | JSON | Focus Pod 1 at THB 20 per hour | Member A books 1 block | agreed_price_satang 1000 (THB 10.00, the smallest chargeable price) |
| 4 | boundary | JSON | Board Room at THB 1,000 per hour | Member A books 8 blocks | agreed_price_satang 400000 (THB 4,000.00) |
| 5 | counterexample | internal | BK-7KQ2M9 stored at 45000 | The Operator changes Meeting Room A to THB 400 per hour | BK-7KQ2M9 stays 45000; its payment session asks for 45000; nothing re-prices it |
| 6 | counterexample | JSON | Meeting Room A at THB 300 per hour | The booking request also sends "amount_satang": 100 | The field is ignored; agreed_price_satang 45000 |

### PUR-R18 Money is whole satang, shown as THB

| Field | Value |
|---|---|
| Rule | Hold every amount as an integer number of satang (BIGINT columns, JSON fields ending in _satang, currency THB); show it as "THB 1,234.50"; never use floats or another currency. |
| Policy status | Decided (D1) |
| Decision source | Project team (D1) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:395 the money filter prints "$" and cents; app.py:90 amount_cents is INTEGER, which overflows with a 500. |
| Terms | PUR-T23, PUR-T06 |
| Candidate responsibility and dependencies | Purchase. Payment uses the same units; its minimum is THB 10, which every chargeable booking meets (PUR-R15). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | `money` filter in the shared base template (M5); contracts (M2); Purchase unit test for the money filter (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | BK-7KQ2M9, price 45000 | Open the booking page | "THB 450.00" |
| 2 | ordinary | JSON | Same | Get the booking | "agreed_price_satang": 45000, "currency": "THB" |
| 3 | boundary | form | A booking priced 123450 | Open its page | "THB 1,234.50" (thousands separator, 2 decimals) |
| 4 | boundary | form | A Community Table booking, price 0 | Open its page | "THB 0.00", coverage free |
| 5 | counterexample | JSON | BK-7KQ2M9, price 45000 | Get BK-7KQ2M9 | "agreed_price_satang": 45000, an integer; never "$450.00", 450.0, 4.5e4 or "45000" |

### PUR-R19 Coverage is fixed at creation

| Field | Value |
|---|---|
| Rule | Set coverage once, when the booking is created: free when the booking price is 0, else plan when the Member's `plan_active` is true, else pay; never change it afterwards. Store the booking price for plan bookings too, with the same formula (D8, D10). |
| Policy status | Decided (D10, D8) |
| Decision source | Project team (D10; D8 for the stored price on plan bookings, which the clarified price rule PUR-R17 does not cover). Course [extraction site]: "“Covered” is not always “money collected”." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:256-267 member_key and is_subscribed match a typed name; app.py:741 and app.py:755-759 save a subscriber's booking as paid with amount 0. |
| Terms | PUR-T24, PUR-T25, PUR-T23, PUR-T01 |
| Candidate responsibility and dependencies | Purchase owns coverage; Payment never sees plan or free bookings. |
| Open question | PUR-Q08 (plan Member books a free space: the order free, then plan, is the default). PUR-Q02 (plan sales). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q02; Project team for PUR-Q08 and the rule as stated |
| Next use | Plan and free skip Payment (PUR-R20); metrics (PUR-R34); e2e "plan and free skip Payment" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A, plan_active false | Books the standard slot | coverage pay; agreed_price_satang 45000; status held |
| 2 | ordinary | JSON | Member B, plan_active true | Books Meeting Room A with start "2026-10-07T10:30:00+07:00", 2 blocks | BK-3MZ8QT: coverage plan; agreed_price_satang 30000 stored; status confirmed; nothing collected |
| 3 | boundary | JSON | Member A | Books Community Table (THB 0 per hour) for 1 block | coverage free; agreed_price_satang 0 |
| 4 | boundary | internal | Member B's plan booking exists | The Operator turns Member B's plan_active off | That booking stays plan; Member B's next booking is pay |
| 5 | counterexample | internal | Member A holds BK-7KQ2M9 (pay) | The Operator turns Member A's plan_active on at 10:05 | BK-7KQ2M9 stays pay and still needs payment; coverage is never re-read |
| 6 | ordinary | form | Member B, plan_active true | Member B reaches the review step for Meeting Room A 2026-10-07 10:30-11:30 | Shows "THB 300.00, covered by your plan. No payment needed." before Member B continues |

### PUR-R20 Plan and free bookings skip Payment

| Field | Value |
|---|---|
| Rule | Create a plan or free booking directly as confirmed, make no Payment call and never ask for a card, then request its grant. |
| Policy status | Decided (D10, D20) |
| Decision source | Project team (D10, D20). Course [extraction site]: "Success, invalid input, failure, repeat; coverage skips collection." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:953-955 always asks for a card on an unpaid booking, even at amount 0. |
| Terms | PUR-T24, PUR-T19, PUR-T17, PUR-T34 |
| Candidate responsibility and dependencies | Purchase; Access for the grant (PUR-R26). |
| Open question | PUR-Q02 (selling plans). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q02; Project team for the rule as stated |
| Next use | Contract example "coverage skips collection" (M2); e2e "plan and free skip Payment" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member B, plan_active true | Pick 10:30 on Meeting Room A, 2026-10-07, 2 blocks, and press "Book" (plan and free coverage never show "Continue to payment") | No redirect to Payment; booking page "Confirmed. Covered by your plan. No payment was taken." with the e-ticket link. For a free booking the page says "Confirmed. This space is free. No payment was taken." |
| 2 | ordinary | JSON | Member A | Book Community Table with start "2026-10-07T09:00:00+07:00", 2 blocks | 201; "status": "confirmed", "coverage": "free", "payment_url": null |
| 3 | boundary | JSON | Member A, plan_active false | Book Focus Pod 1 for 1 block (THB 10.00) | Not free: status held and a payment_url (pay coverage) |
| 4 | counterexample | internal | Member A's free Community Table booking | Look at the calls Purchase made | No call to Payment; no hold; one grant request to Access |

### PUR-R21 A hold lasts 15 minutes; the same request resumes it

| Field | Value |
|---|---|
| Rule | On "Continue to payment" for a pay booking, create a held booking with `hold_expires_at` = creation + 15 min. While that hold is slot-blocking, the same Member sending the same space, start and blocks resumes it: no second booking, the same booking reference and its payment_url. The match runs right after the shape checks and before the notice, horizon and party-size checks (PUR-R39), so a hold made exactly 60 min ahead, or one whose space capacity has since dropped, can still be resumed. A resume keeps the held booking's stored party size and note and ignores the ones sent; to change them, cancel and book again. A resume repeats POST /payment-sessions (PMT-R03): an answer paid confirms the booking (D14) and answers with the booking (form 303 /bookings/<ref>, JSON 200), never the hosted page; an answer expired before the payment deadline (an earlier held cancel reached Payment but its answer was lost) answers like the deadline (PUR-R40), with no redirect to Payment; no answer gives "Payment is not reachable. Please try again." (form 303 /bookings/<ref>, JSON 503). A Member sending the same space, start and blocks as their own confirmed booking gets that booking back: the form answers 303 to its booking page with the flash "You already booked this slot", JSON answers 200 with it; nothing new is created and no grant is requested again. Never hold a plan or free booking (PUR-R20). One held booking per Member and the check order: PUR-R39. The end of a hold that can no longer be paid: PUR-R40. |
| Policy status | Decided (D11) |
| Decision source | Project team (D11). Answers class questions Q-SLOT-1 and Q-SLOT-2 (class rules PR #6 at c18b638), with PUR-R40. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:49-117 the bookings table has no status or expiry column; app.py:745-765 inserts unpaid bookings that never lapse. |
| Terms | PUR-T20, PUR-T21, PUR-T01, PUR-T34 |
| Candidate responsibility and dependencies | Purchase. The payment session is requested after the insert commits (PUR-R23). |
| Open question | PUR-Q09 (Payment unreachable when the hold is created). |
| Clarification owner | Project team |
| Next use | Purchase hold tests (M5); e2e "double submit" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A has no held booking | Book the standard slot at 10:00 | 201; status held, hold_expires_at "2026-10-05T10:15:00+07:00", reference BK-7KQ2M9, payment_url of the hosted page |
| 2 | ordinary | form | Same | Press "Continue to payment" | Held booking created; browser sent to the Payment hosted page |
| 3 | boundary | JSON | BK-7KQ2M9 held until 10:15 | At 10:05 Member A sends the same space and time again | 200 with BK-7KQ2M9 and the same payment_url; no second booking (double submit is safe) |
| 4 | boundary | form | Same | At 10:05 Member A presses "Continue to payment" again for the same space and time | Browser sent to the same hosted page for BK-7KQ2M9; no second booking |
| 5 | boundary | JSON | BK-7KQ2M9 held with no session: POST /payment-sessions got no answer at 10:00 (PUR-Q09) | At 10:05, with Payment back, Member A sends the same space and time | 200 with BK-7KQ2M9 and the new session's payment_url |
| 6 | counterexample | JSON | Member B (plan_active true) has no held booking | At 10:00 book Meeting Room A with start "2026-10-07T10:30:00+07:00", 2 blocks | 201 BK-3MZ8QT; "status": "confirmed", "coverage": "plan", "payment_url": null; never held (PUR-R20) |
| 7 | boundary | form | Member B's plan booking BK-3MZ8QT (Meeting Room A 2026-10-07 10:30-11:30) was just confirmed | Member B's double click sends the same form again | 303 to that booking's page with the flash "You already booked this slot"; no second booking, no second grant request, never "Slot just taken" |
| 8 | boundary | JSON | BK-7KQ2M9 confirmed | Member A sends the standard booking body again | 200 with BK-7KQ2M9 as stored; nothing new created |
| 9 | boundary | form | At 10:00 Member A held Focus Pod 1 for 2026-10-05 11:00, 1 block (exactly 60 min ahead) | At 10:05 Member A presses "Continue to payment" on the booking page | 303 to the same hosted page, not "Book at least 60 minutes ahead": the resume match runs before the notice check |
| 10 | counterexample | JSON | BK-7KQ2M9 held, party size 4, note "Team planning" | At 10:05 Member A sends the same space, start and blocks with party_size 5 and another note | 200 with BK-7KQ2M9 as stored: party size 4 and the old note; nothing changes |
| 11 | boundary | form | BK-7KQ2M9 held; Member A paid it at 10:04 in another tab, and nothing in Purchase has read it | At 10:05 Member A presses "Continue to payment" on the booking page | The repeated create answers paid: BK-7KQ2M9 is confirmed (D14) and its grant requested; 303 to /bookings/BK-7KQ2M9, never the hosted page |
| 12 | counterexample | form | BK-7KQ2M9 held; at 10:04 Member A's held cancel reached Payment, which expired the session, but the answer was lost, so the hold stayed | At 10:05 Member A presses "Continue to payment" | No redirect to Payment: 303 to /bookings/BK-7KQ2M9 with "Time to pay has run out; cancel this hold or book again from 10:15"; the page shows "Time to pay has run out. Nothing was charged. Cancel this hold to book again now, or it ends at 10:15." and Cancel |
| 13 | boundary | JSON | BK-7KQ2M9 held with no session (PUR-Q09); Payment still unreachable | At 10:05 Member A sends the same space and time again | 503 {"error": "Payment is not reachable. Please try again."}; still held without a session |

### PUR-R22 Guard the booking insert against races

| Field | Value |
|---|---|
| Rule | Before inserting a booking, reconcile the stale held bookings of that space in their own short steps; then check and insert in one transaction, which first locks the Member's row and re-runs the Member's own match and the one-held-booking check (PUR-R39); let the partial EXCLUDE constraint on status held or confirmed turn a lost race into 409 (JSON) or the flashed "Slot just taken" (form), except that a violation by the Member's own matching hold answers as a resume (PUR-R39). When a lapsed held booking that overlaps the requested slot could not be reconciled (no answer, or the sweep stopped before reading it), answer 503 {"error": "Payment is not reachable. Please try again."} (JSON) or that flash (form) before the insert; when a slot-blocking booking also overlaps, 409 "Slot just taken" wins over 503. A lapsed hold that does not overlap the requested slot never blocks the insert, even when it could not be reconciled. |
| Policy status | Decided (D11, D13) |
| Decision source | Project team (D11, D13) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:130-135 the EXCLUDE constraint has no status filter; app.py:766 maps ExclusionViolation and DeadlockDetected to 409. |
| Terms | PUR-T21, PUR-T20, PUR-T26 |
| Candidate responsibility and dependencies | Purchase; Payment for the sweep (GET /payment-sessions/{id}). No HTTP call runs inside the insert transaction (PUR-R35). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Purchase tests with two concurrent inserts (M5); e2e "double submit" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 held, hold lapsed at 10:15, session unpaid | At 10:20 Member B books Meeting Room A 2026-10-07 09:00-10:30 | The sweep marks BK-7KQ2M9 expired in its own step; then Member B's insert commits; 201 |
| 2 | boundary | JSON | Meeting Room A 09:00-10:30 is free | Member A and Member B send the same slot at the same instant | One 201; the other 409 {"error": "Slot just taken"} from the EXCLUDE constraint |
| 3 | boundary | form | Same | The losing request came from the form | Space page with the flash "Slot just taken" |
| 4 | boundary | JSON | BK-7KQ2M9 held with a lapsed hold; Payment unreachable | At 10:20 Member B books the overlapping slot | 503 {"error": "Payment is not reachable. Please try again."}; nothing changes |
| 5 | boundary | form | Same | Member B posts the booking form for the overlapping slot | Space page with the flash "Payment is not reachable. Please try again."; nothing changes |
| 6 | counterexample | JSON | The only overlapping booking is cancelled | Member B books the slot | 201; the EXCLUDE constraint ignores expired and cancelled rows |
| 7 | boundary | JSON | Payment unreachable; Member C's hold on Meeting Room A 2026-10-07 09:00-10:30 lapsed at 10:15 and is unreconciled; clock 10:20 | Member B books Meeting Room A 2026-10-07 13:00, 1 block | 201: the unread lapsed hold does not overlap 13:00, so the insert proceeds |
| 8 | counterexample | JSON | Payment unreachable; a confirmed booking takes Meeting Room A 2026-10-07 09:00-10:00, and an unreconciled lapsed hold takes 10:00-10:30; clock 10:20 | Member B books Meeting Room A 2026-10-07 09:30, 2 blocks | 409 {"error": "Slot just taken"}: the confirmed booking blocks the slot whatever Payment answers, so 409 wins over 503 |


### PUR-R23 Ask Payment for a session that ends before the hold

| Field | Value |
|---|---|
| Rule | For a held pay booking, after its insert commits, call POST /payment-sessions with booking_reference, amount_satang = the booking price, currency THB, description, success_url, cancel_url and expires_at = `hold_expires_at` - 2 min; store the returned session id and send the browser to PAYMENT_PUBLIC_URL + "/pay/" + that id, never to the url in the answer (payment_url in JSON is built the same way), so a wrong Payment PUBLIC_URL cannot send a bearer link to another host or over plain http. The description holds the space name and the Bangkok time only, never the Member's name or email. If the call gets no answer, the booking stays held without a session and the Member sees "Payment is not reachable. Please try again." (503 over JSON; PUR-Q09). |
| Policy status | Decided (D12) |
| Decision source | Project team (D12). Course [extraction site]: Purchase to Payments "Collect this agreed amount." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:932-965 mark_booking_paid takes the card inside the same app; there is no payment session. |
| Terms | PUR-T20, PUR-T23, PUR-T18, PMT-T02, PMT-T06 |
| Candidate responsibility and dependencies | Purchase sends; Payment owns the session and rejects attempts at or after expires_at, so the outcome is final before the hold ends. |
| Open question | PUR-Q09 (Payment unreachable at this call). |
| Clarification owner | Project team |
| Next use | purchase to payment contract (M2); consumer tests with a stubbed payment_client.py (M5); e2e happy path and repeat session create (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 held at 10:00 | Purchase requests the session | Body: booking_reference BK-7KQ2M9, amount_satang 45000, currency THB, description "Meeting Room A, 2026-10-07 09:00-10:30", success_url "http://localhost:8001/bookings/BK-7KQ2M9/return", cancel_url "http://localhost:8001/bookings/BK-7KQ2M9", expires_at "2026-10-05T10:13:00+07:00"; the ps_ id is stored |
| 2 | ordinary | form | Same | Member A pressed "Continue to payment" | Browser redirected to the Payment hosted page url |
| 3 | boundary | internal | Same, resumed at 10:05 | Purchase repeats the request with the same body | Payment returns the existing session (200); same url; no second session |
| 4 | counterexample | internal | Member B's plan booking, or Member A's free booking | Booking created | No session request at all |
| 5 | counterexample | internal | The Operator raised the rate to THB 400 per hour after BK-7KQ2M9 was created | Purchase repeats the session request | Still amount_satang 45000; a different amount would get 409 from Payment |
| 6 | boundary | JSON | Payment unreachable at 10:00 | Member A books the standard slot | 503 {"error": "Payment is not reachable. Please try again."}; BK-7KQ2M9 stays held with no payment_session_id |
| 7 | boundary | form | Same | Member A presses "Continue to payment" | The booking page with the flash "Payment is not reachable. Please try again."; BK-7KQ2M9 stays held with no session |
| 8 | counterexample | internal | Member A's name and email are on the Member | Purchase builds the description | "Meeting Room A, 2026-10-07 09:00-10:30"; a description holding a@example.com or "Member A" is never sent |

### PUR-R24 Reconcile held bookings whenever Purchase touches them

| Field | Value |
|---|---|
| Rule | Whenever Purchase shows or acts on a held booking that has a payment session, call GET /payment-sessions/{id}. The reconcile points: the booking page and its return URL, GET /api/bookings/<ref>, My bookings (the page and GET /api/bookings/mine), the cancel confirm screen, the pre-insert sweep, the Member's own lapsed holds (PUR-R39), and the Operator's Reconcile of one booking or of all held; the POST cancel uses the expire answer in place of the GET (PUR-R31). The answer: paid goes to fulfilment, unpaid after the hold marks it expired, unpaid inside the hold changes nothing, and an unreachable Payment changes nothing. The hold has lapsed when clock.now() is at or after hold_expires_at. A held booking without a session is expired without a Payment call once its hold lapses (PUR-Q09). "Reconcile all held" and the pre-insert sweep stop calling Payment after the first read that gets no answer and count the rest unchanged (held bookings without a session are still expired on lapse), so a hung Payment costs one 5 s timeout, never a gunicorn worker timeout. In the same way, within one Reconcile request, after the first POST /grants or POST /refunds that gets no answer Purchase sends no more calls of that kind in that request (those bookings stay flagged "Being prepared" or "Refund pending" for the next retry point, and the flash adds "Access is not reachable. Please try again." or "Payment is not reachable. Please try again."); after the first read answered with any other 4xx (for example 401 from a mismatched token) it stops reading, counts the rest unchanged and adds one flash after the counts, "Payment refused the call (401): check the service settings and the Purchase log.". A Reconcile of a booking that is not held changes nothing and flashes "0 confirmed, 0 expired, 0 cancelled, 1 unchanged". |
| Policy status | Decided (D13) |
| Decision source | Project team (D13). Course [extraction site]: "Purchase interprets the result". No webhooks: ADR-0004 (Purchase-only callers), no webhooks. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:960-965 marks a booking paid in the same process; nothing reads an outcome from elsewhere. |
| Terms | PUR-T26, PUR-T20, PUR-T19, PUR-T27, PUR-T34 |
| Candidate responsibility and dependencies | Purchase; Payment GET /payment-sessions/{id}. Purchase trusts its stored session id, not the session_id in the return URL. Invariant: every paid session ends as a confirmed booking or a refund attempt. |
| Open question | PUR-Q09 (held booking without a session). |
| Clarification owner | Project team |
| Next use | ADR-0007 (lazy hold expiry and reconciliation); e2e "lost redirect reconciled" and "hold expiry frees the slot" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member A paid on the hosted page at 10:04 | The browser returns to success_url | Purchase reads its stored session: paid; the booking page shows "Confirmed" and requests the grant |
| 2 | boundary | form | Member A paid at 10:12 and closed the tab (lost redirect) | At 10:30 Member A opens My bookings | Reconciled: paid, so BK-7KQ2M9 becomes confirmed, not expired |
| 3 | boundary | JSON | Session unpaid; hold lapsed at 10:15 | At 10:20 Member A gets BK-7KQ2M9 | Reconciled first: status expired; the slot is free |
| 4 | ordinary | form | Session unpaid; clock 10:10 | Member A opens the booking page | No change; status held and "Pay by 10:13" (3 min left) |
| 5 | counterexample | form | Payment unreachable | Member A opens the booking page at 10:20 | Nothing changes (payment_outcome unchanged); the page shows held, "Payment status unknown. If you paid before 10:13, your booking will be confirmed: refresh in a minute." and Cancel, with no "Continue to payment" (past the payment deadline, PUR-R40); no error page, because a read does not need the result |
| 6 | ordinary | form | Clock 10:20; three held bookings with sessions: one paid, one unpaid with its hold lapsed at 10:15, one unpaid created at 10:10 (hold until 10:25) | The Operator presses "Reconcile all held" (POST /operator/bookings/reconcile) | 303 to /operator/bookings with the flash "1 confirmed, 1 expired, 0 cancelled, 1 unchanged"; the per-booking Reconcile on the paid one alone would flash "1 confirmed, 0 expired, 0 cancelled, 0 unchanged" |
| 7 | boundary | internal | Session unpaid; hold_expires_at 10:15 | Purchase reconciles at 10:14:59, then at 10:15:00 | 10:14:59: unchanged, held; 10:15:00: expired |
| 8 | counterexample | form | BK-7KQ2M9 held; Member C's session for BK-3HT8WD is paid | Member A opens the success_url of BK-7KQ2M9 with ?session_id= set to Member C's session id | Purchase ignores the query value and reads BK-7KQ2M9's stored ps_ id; BK-7KQ2M9 stays held; no refund is requested; Member C's booking and session are unchanged |
| 9 | boundary | internal | BK-7KQ2M9 held with no session (PUR-Q09); clock 10:15 | Purchase touches it | expired, with no Payment call: there is no session to read |
| 10 | counterexample | form | Clock 10:20; two held bookings with sessions, both lapsed; Payment unreachable | The Operator presses "Reconcile all held" | One Payment read, then no more: nothing changes; the flash says "0 confirmed, 0 expired, 0 cancelled, 2 unchanged. Payment is not reachable. Please try again." |
| 11 | boundary | form | BK-7KQ2M9 confirmed | The Operator posts /operator/bookings/BK-7KQ2M9/reconcile from a stale list | No Payment call; 303 to /operator/bookings with the flash "0 confirmed, 0 expired, 0 cancelled, 1 unchanged" |
| 12 | boundary | form | Clock 10:20; three held bookings with paid sessions; Access gives no answer | The Operator presses "Reconcile all held" | All three confirmed; the first POST /grants gets no answer and the other two are not sent, so all three keep grant_status pending ("Being prepared"); the flash "3 confirmed, 0 expired, 0 cancelled, 0 unchanged. Access is not reachable. Please try again."; the request ends well inside gunicorn's 30 s timeout |
| 13 | counterexample | form | PAYMENT_API_TOKEN in Purchase differs from the one Payment holds; clock 10:20; two held bookings with sessions | The Operator presses "Reconcile all held" | The first read gets 401 and no second read is made; the flash "0 confirmed, 0 expired, 0 cancelled, 2 unchanged. Payment refused the call (401): check the service settings and the Purchase log." |

### PUR-R25 Confirm only a matching payment

| Field | Value |
|---|---|
| Rule | Confirm a held booking, even if its hold just lapsed, only when the paid session's booking_reference, amount_satang and currency equal the booking's; on a mismatch, set the booking cancelled with reason amount_mismatch and record a full refund request (refund_status pending, refund_attempt 1, refund_requested_at = clock.now()) in the same transaction, sent right after commit; refund a paid session whose booking is already expired in full with reason slot_unavailable, recorded the same way in the transaction that stores the paid read before the call; every such full refund carries the session's own payment_session_id and booking_reference as returned by GET /payment-sessions/{id}. |
| Policy status | Decided (D14) |
| Decision source | Project team (D14). Course [extraction site]: "Purchase receives": "Payment reference / Matching amount + outcome / Then applies booking rules". |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:940-965 checks and then updates paid without an amount check and without a transaction. |
| Terms | PUR-T27, PUR-T23, PUR-T18, PUR-T28, PUR-T29 |
| Candidate responsibility and dependencies | Purchase. The real Payment cannot produce a mismatch, so the check is covered by a Purchase unit test with a stubbed payment_client.py. The refund amount is the session's collected amount. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Purchase unit test with the stub (M5); issuance (PUR-R26). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 held; session paid, BK-7KQ2M9, 45000, THB | Purchase reconciles | status confirmed; then the grant is requested |
| 2 | boundary | internal | Same, but the hold lapsed at 10:15 and the payment landed at 10:12 | Purchase reconciles at 10:20 | Still confirmed; the hold lapse does not beat a paid session |
| 3 | counterexample | internal | Stubbed session: paid, BK-7KQ2M9, amount_satang 40000, THB | Purchase reconciles | One transaction: status cancelled, reason amount_mismatch, refund request 40000; the refund is sent after commit; no grant |
| 4 | counterexample | internal | Stubbed session: paid, BK-7KQ2M9, 45000, currency USD | Purchase reconciles | Same as row 3: cancelled with amount_mismatch and a full refund |
| 5 | counterexample | internal | BK-7KQ2M9 already expired; stubbed session reports paid | Purchase reconciles | Stays expired; full refund 45000 with reason slot_unavailable |
| 6 | counterexample | internal | Stubbed session for booking BK-7KQ2M9 reports paid, booking_reference BK-3HT8WD, 45000, THB | Purchase reconciles | cancelled with reason amount_mismatch; the full refund is sent with BK-3HT8WD, the session's own reference, so Payment accepts it; no grant |

### PUR-R26 Request the grant on confirmation

| Field | Value |
|---|---|
| Rule | When a booking becomes confirmed, and only while it stays confirmed with no cancel in progress, call POST /grants with booking_reference, member_ref, space_id, space_name, valid_from and valid_until. The transaction that confirms the booking also sets grant_status pending, so a stop between that commit and the call leaves "being prepared", never a confirmed booking with no ticket and no flag (the held-cancel path of PUR-R31 confirms without a grant and cancels at once). If Access fails, keep the booking confirmed, show "being prepared" and retry at the retry points: the booking page (the page or GET /api/bookings/<ref>), the owner's Retry (POST /bookings/<ref>/retry) and the Operator's Retry. Store grant_id, ticket_url and grant_status (PUR-T34); store ticket_url only when it starts with ACCESS_PUBLIC_URL + "/t/": any other value is a config defect (PUR-R35), logged with the booking reference, and grant_status stays pending, so the page keeps "Your e-ticket is being prepared". Purchase does not call GET /grants in v1 and never derives a no-show. |
| Policy status | Decided (D20) |
| Decision source | Project team (D20). Course [extraction site]: Purchase to Access "Issue an authorised grant." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:970-985 issue_access_code makes a new random code on every call and stores nothing. |
| Terms | PUR-T17, PUR-T18, PUR-T30, PUR-T34, AXS-T02, AXS-T11 |
| Candidate responsibility and dependencies | Purchase requests; Access owns the grant and its ticket code. member_ref is the Member's id as text, never the email. POST /grants is idempotent on the booking reference. Purchase stores ticket_url, never the ticket_code from the answer, and logs neither: ticket_url is itself a bearer link (ADR-0008). |
| Open question | PUR-Q06 (real door locks). |
| Clarification owner | Course instructor (business stakeholder), with the project team, for PUR-Q06; Project team for the rule as stated |
| Next use | purchase to access contract (M2); e2e happy path and "repeat grant" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 just confirmed | Purchase requests the grant | Body: booking_reference BK-7KQ2M9, member_ref (Member A's id), space_id 1, space_name "Meeting Room A", valid_from "2026-10-07T09:00:00+07:00", valid_until "2026-10-07T10:30:00+07:00"; grant_id (gr_), ticket_url and grant_status issued are stored |
| 2 | ordinary | form | Same | Member A opens the booking page | "View e-ticket" links to the ticket_url |
| 3 | boundary | form | Access timed out during issuance | Member A opens the booking page later | Booking still confirmed; "Your e-ticket is being prepared"; issuance is retried and, once it succeeds, the link appears; one grant only |
| 4 | boundary | JSON | Same | Member A gets BK-7KQ2M9 | "status": "confirmed", "grant_status": "pending", "ticket_url": null |
| 5 | counterexample | internal | BK-7KQ2M9 is cancelled, or its cancel is in progress | A retry would run | No POST /grants |
| 6 | counterexample | internal | Access answers the grant request with status revoked (a tombstone) | Purchase stores the answer | grant_status revoked; no e-ticket link is shown |
| 7 | ordinary | form | Access timed out during issuance of BK-7KQ2M9; Access is back | The Operator presses Retry on BK-7KQ2M9 in the all-bookings list | One POST /grants; grant_status issued; Member A's booking page shows "View e-ticket"; one grant only |
| 8 | counterexample | internal | Purchase stops right after the commit that confirms BK-7KQ2M9, before POST /grants | Member A opens the booking page later | grant_status is pending (set in the confirming transaction): the page shows "Your e-ticket is being prepared" and retries the grant; the all-bookings list flags "Being prepared" |
| 9 | counterexample | internal | Access's PUBLIC_URL is wrongly set to http://evil.example, so the grant answer for BK-7KQ2M9 carries ticket_url "http://evil.example/t/q3Vt9XbLk2Rm8PzW4nHc7A" | Purchase stores the answer | ticket_url is not stored; the defect is logged with BK-7KQ2M9 (never the URL's token); grant_status stays pending and the page shows "Your e-ticket is being prepared" |

### PUR-R27 Send the check-in window as the booking time

| Field | Value |
|---|---|
| Rule | Send valid_from = start and valid_until = end, the half-open window [start, end), with no early entry while the buffer is 0; if a buffer B is ever approved, send valid_from = start - min(B, 15 min). |
| Policy status | Decided (D21) |
| Decision source | Project team (D21) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:970-985 issues a code with no time check. |
| Terms | PUR-T17, PUR-T14, PUR-T08, AXS-T12 |
| Candidate responsibility and dependencies | Purchase computes the values; Access only checks them at the kiosk and never computes a window itself. |
| Open question | PUR-Q01 (cleaning gap); PUR-Q06 (real door locks). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q01, and with the project team for PUR-Q06; Project team for the rule as stated |
| Next use | purchase to access contract (M2); e2e check-in before, inside and after the window (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9, 2026-10-07 09:00-10:30 | Purchase builds the grant request | valid_from "2026-10-07T09:00:00+07:00", valid_until "2026-10-07T10:30:00+07:00" |
| 2 | boundary | internal | Buffer 0 (today) | Same | valid_from is exactly the start, not 08:45; no early entry |
| 3 | boundary | internal | Hypothetical: a buffer of 10 min, then of 30 min, approved later | Same | valid_from 08:50; then 08:45 (capped at 15 min) |
| 4 | counterexample | form | The grant for BK-7KQ2M9 has valid_from 2026-10-07 09:00; opening hours start at 08:00 | Staff scans H7K3-9QXA at Meeting Room A at 08:59 | not_open_yet (opens 09:00): Access uses only the valid_from it was sent, never the opening hours |


### PUR-R28 Booking statuses move one way; nothing is deleted

| Field | Value |
|---|---|
| Rule | Store only the statuses held, confirmed, expired and cancelled; allow only held to confirmed, expired or cancelled, and confirmed to cancelled; never delete a booking; derive Completed (confirmed and clock.now() at or after the end) only when showing it; JSON shows it as "completed": true beside "status": "confirmed". |
| Policy status | Decided (D11, D18; Disputes decided in M1, row 7) |
| Decision source | Project team (D11, D18). Completed is derived by Purchase and never stored; no-show is derived by Access only: DECISIONS.md, Disputes decided in M1, row 7. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 cancel runs DELETE FROM bookings, so a paid booking and its revenue disappear. |
| Terms | PUR-T19, PUR-T22, PUR-T28 |
| Candidate responsibility and dependencies | Purchase. "No-show" is derived by Access only. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | State diagram (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 held | Fulfilment runs | held to confirmed |
| 2 | boundary | form | BK-7KQ2M9 confirmed; clock 2026-10-07 10:30 | Member A opens My bookings | BK-7KQ2M9 is listed under past bookings as "Completed"; stored status stays confirmed |
| 3 | counterexample | internal | BK-7KQ2M9 expired | A paid session for it is reconciled | No move to confirmed; it stays expired and is refunded (PUR-R25) |
| 4 | counterexample | JSON | BK-7KQ2M9 cancelled | Get BK-7KQ2M9 | 200 with status cancelled; the row is never deleted, so never a 404 from deletion |
| 5 | counterexample | internal | BK-7KQ2M9 cancelled | Anything tries to set it confirmed or held | Refused; cancelled is final |
| 6 | boundary | JSON | BK-7KQ2M9 confirmed | Get BK-7KQ2M9 at 2026-10-07 10:29, then at 10:30 | "status": "confirmed" both times; "completed": false, then true |

### PUR-R29 Booking reference is BK- plus 6 symbols

| Field | Value |
|---|---|
| Rule | Give every booking a reference `BK-` + 6 random symbols from 23456789ABCDEFGHJKMNPQRSTVWXYZ, unique by a database constraint and regenerated on collision; use it as the shared reference with Payment and Access. |
| Policy status | Decided (D22) |
| Decision source | Project team (D22) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:52 booking ids are SERIAL integers, easy to guess and enumerate. |
| Terms | PUR-T18 |
| Candidate responsibility and dependencies | Purchase generates it. Payment keys its session on it; Access keys its grant on it. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contracts (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A books the standard slot | Read the response | "reference": "BK-7KQ2M9" (BK- then 6 symbols from the alphabet); Payment and Access store the same value as booking_reference |
| 2 | boundary | internal | The generated reference already exists | Insert the booking | The unique constraint fires; a new reference is generated and the insert succeeds |
| 3 | counterexample | internal | Any booking | Generate references | Never 0, O, 1, I, L or U, so BK-7KQ2M0 cannot occur |
| 4 | counterexample | form | BK-7KQ2M9 confirmed | Staff types BK7KQ2M9 at the check-in kiosk | Refused as unknown_code (Access); the reference is never an entry credential |

### PUR-R30 Cancel a confirmed booking: who, when, how much

| Field | Value |
|---|---|
| Rule | Let the owning Member cancel a confirmed booking before its start, with a 100% refund at 24 h or more before start and 0% otherwise; let an operator cancel it before its end, always at 100%; refund 0 with no Payment call for plan and free bookings and say "No payment was taken"; show the refund before the person confirms. The confirm form carries the refund it showed (shown_refund_satang, integer satang): for a confirmed booking the amount on the screen, for a held one the amount its "If a payment completes first" sentence names (PUR-R31), 0 for plan and free. At the POST, before any Payment or Access call, Purchase computes the PUR-R30 amount again for that caller; if it is lower, cancel nothing and show the confirm screen again with the flash "The refund is now THB 0.00 (0%): the start is less than 24 h away. Confirm again." A missing, empty or non-integer shown_refund_satang cancels nothing and answers 303 to /bookings/<ref>/cancel with the flash "Please confirm the refund again." JSON callers send no shown amount, so no check applies. The POST runs its checks in this order on both routes: ownership (404), already cancelled or expired, started (Member) or ended (operator), the shown_refund_satang comparison, then the calls. The two shown-refund refusals ("The refund is now ... Confirm again." and "Please confirm the refund again.") answer 303 /bookings/<ref>/cancel on both routes; every other refusal answers 303 /bookings/<ref>. The confirm screen names the booking ("Cancel BK-7KQ2M9, Meeting Room A 2026-10-07 09:00-10:30", plus "Member A (a@example.com)" for an operator), its button reads "Cancel booking", and a "Keep booking" link goes back to /bookings/<ref>. From the start until the end the owner's (non-operator) booking page shows no Cancel and no refund line, only "This booking has started; ask the operator" (v1 has no contact channel in the app: door Staff phone the Operator, who is on call through opening hours). The operator policy applies to any booking, the Operator's own included (accepted). Before payment the space page's review shows, for pay coverage only, "Full refund if you cancel 24 h or more before the start; after that, no refund.", plus "Starts less than 24 h away cannot be refunded." when the grid date is today or tomorrow; plan and free show no refund line. A confirmed pay booking's page shows the owner "Cancel by 2026-10-06 09:00 for a full refund." up to the 24 h line and "No refund if you cancel: the start is less than 24 h away." after it; a plan or free one shows "You can cancel until the start.". These policy lines are for the owner; an operator viewer sees Cancel until the end and "Operator cancel: full refund until 10:30", never "ask the operator". |
| Policy status | Decided (D18) |
| Decision source | Project team (D18). The shown refund binds the POST: DECISIONS.md, Disputes decided in M1, row 10. Answers class questions Q-SLOT-4 and Q-SLOT-5 (class rules PR #6 at c18b638). Course [syllabus site]: "Cancellation is a small, explicitly agreed change spanning the three services, with unsupported cases recorded." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 anyone with the id can cancel at any time and nothing about a refund is stored. |
| Terms | PUR-T28, PUR-T29, PUR-T24, PUR-T02, PUR-T22 |
| Candidate responsibility and dependencies | Purchase decides the amount; the steps run as in PUR-R32. |
| Open question | PUR-Q03 (partial cancel, reschedule, Member cancel after start, other refund percentages). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q03; Project team for the rule as stated |
| Next use | PRD cancellation stories and unsupported cases (M2); e2e Member cancel at 24 h or more and under 24 h, operator cancel (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | BK-7KQ2M9 confirmed, pay, THB 450.00; clock 2026-10-05 11:00 | Member A presses Cancel, sees "Refund THB 450.00 (100%)", then confirms | status cancelled; refund 45000 |
| 2 | ordinary | JSON | Same | Member A cancels | 200; status cancelled, refund_amount_satang 45000 |
| 3 | boundary | JSON | Same; clock 2026-10-06 09:00 (exactly 24 h before start) | Member A cancels | refund_amount_satang 45000 (100%) |
| 4 | boundary | form | Same; clock 2026-10-06 09:01 | Member A presses Cancel | The screen shows "Refund THB 0.00 (0%)" before confirming; after confirming, cancelled with no refund call: refund_amount_satang 0, refund_status none, refund_attempt null |
| 5 | counterexample | form | Same; clock 2026-10-07 09:00 (start) | Member A opens BK-7KQ2M9 and posts Cancel | No Cancel button is shown; the post gets the flash "This booking has started; ask the operator"; nothing changes |
| 6 | boundary | JSON | Same; clock 2026-10-07 10:00 | The Operator cancels | Cancelled with refund 45000 (100%) |
| 7 | counterexample | form | Member B's plan booking, confirmed | Member B cancels 2 hours before start | Cancelled; the screen says "No payment was taken"; refund_amount_satang 0, refund_status none, refund_attempt null; no Payment call |
| 8 | counterexample | JSON | BK-7KQ2M9 confirmed; clock 2026-10-07 09:00 (start) | Member A cancels | 409 {"error": "This booking has started; ask the operator"}; nothing changes |
| 9 | boundary | form | BK-7KQ2M9 confirmed; clock 2026-10-07 10:30 (end) | The Operator presses Cancel on BK-7KQ2M9 in an all-bookings list loaded before 10:30 | No confirm screen: 303 to the booking page with the flash "This booking has ended"; nothing changes |
| 10 | boundary | form | BK-7KQ2M9 confirmed, pay | Member A opens the cancel screen at 2026-10-06 08:59 ("Refund THB 450.00 (100%)") and confirms at 09:01 | Nothing is cancelled: 303 to /bookings/BK-7KQ2M9/cancel with the flash "The refund is now THB 0.00 (0%): the start is less than 24 h away. Confirm again."; the screen now shows "Refund THB 0.00 (0%)" |
| 11 | counterexample | form | BK-7KQ2M9 confirmed, pay; clock 2026-10-05 11:00 | Member A posts the cancel form with no shown_refund_satang, or with "abc" | Nothing is cancelled and nothing is sent to Access or Payment; 303 to /bookings/BK-7KQ2M9/cancel with the flash "Please confirm the refund again." |
| 12 | boundary | form | BK-7KQ2M9 confirmed, pay | The Operator opens the confirm screen at 2026-10-07 10:29 ("Refund THB 450.00 (100%)") and confirms at 10:30 | 303 to /bookings/BK-7KQ2M9 with the flash "This booking has ended"; nothing cancelled: the end check runs before the shown-refund check |
| 13 | boundary | JSON | BK-7KQ2M9 confirmed, pay, not cancelled; clock 2026-10-07 10:30 (end) | The Operator cancels | 409 {"error": "This booking has ended"}; it is completed; nothing changes |
| 14 | ordinary | form | Clock 2026-10-05 10:00; Member A (pay) | Member A opens Meeting Room A, date 2026-10-07, 3 blocks, then date 2026-10-06 | 2026-10-07: the review shows "Full refund if you cancel 24 h or more before the start; after that, no refund."; 2026-10-06 also shows "Starts less than 24 h away cannot be refunded." |
| 15 | counterexample | form | Clock 2026-10-05 10:00; Member B (plan_active true) | Member B opens Meeting Room A, date 2026-10-07, 3 blocks | The review says "THB 450.00, covered by your plan. No payment needed." with no refund line |
| 16 | boundary | form | BK-7KQ2M9 confirmed, pay | Member A opens its page at 2026-10-06 09:00, then at 09:01 | 09:00: "Cancel by 2026-10-06 09:00 for a full refund."; 09:01: "No refund if you cancel: the start is less than 24 h away." |
| 17 | boundary | form | BK-7KQ2M9 confirmed, pay; clock 2026-10-07 09:30 | The Operator opens BK-7KQ2M9, then its cancel screen | Cancel shows, with "Operator cancel: full refund until 10:30" and no "ask the operator"; the confirm screen shows "Refund THB 450.00 (100%)" |

### PUR-R31 Cancel a held booking: expire its session first

| Field | Value |
|---|---|
| Rule | To cancel a held booking, first call POST /payment-sessions/{id}/expire (D18); it returns the session's final state, and Purchase applies it as the cancel's reconcile read (D13): if paid, confirm the booking without issuing a grant and continue as a confirmed-booking cancel (PUR-R30); if unpaid and the hold has lapsed, mark the booking expired, not cancelled; if unpaid inside the hold, set it cancelled with no refund. Refuse the cancel if Payment is unreachable. A held booking without a session is cancelled with no Payment call, or expired if its hold has lapsed (PUR-Q09). Before the person confirms, the confirm screen (GET) runs the reconcile read for the held booking (PUR-R24). Paid: the booking is confirmed (D14) and the screen shows the confirmed-booking refund (PUR-R30). Before the payment deadline (hold_expires_at - 2 min), unpaid: "We have not received a payment for this booking. Cancelling closes the payment page. If a payment completes first, the refund is" and the amount PUR-R30 would give, for example "THB 450.00 (100%).", or "THB 0.00 (0%): the start is less than 24 h away."; Payment gives no answer: "We could not check your payment just now. If a payment completes or went through, the refund is" and the same amount, never "We have not received a payment". An operator viewer always sees "THB 450.00 (100%)" there before the end. From the payment deadline, after a read that returned unpaid, no payment can complete, so the screen says only "Nothing was charged. Cancel this hold?". From the payment deadline with no answer it says "Payment status unknown. If a payment went through, the refund is THB 450.00 (100%)." (or "THB 0.00 (0%): the start is less than 24 h away."), never "Nothing was charged". With no session, at any time, it says "Payment was not started. Nothing was charged. Cancel this hold?". The held screen's form carries shown_refund_satang equal to the amount the screen names: the PUR-R30 amount for that caller where a sentence names one, 0 for "Nothing was charged. Cancel this hold?" and for no session. The PUR-R30 check runs before the expire call, so a refused cancel never expires the session and a paid session is never confirmed and then left uncancelled. A held cancel stores cancel_reason member_cancel or operator_cancel, after the caller. |
| Policy status | Decided (D13, D18) |
| Decision source | Project team (D13, D18). The refund never depends on whether Purchase had already seen the payment. The lapsed-hold tie-break between D13 and D18: DECISIONS.md, Disputes decided in M1, row 2. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 deletes the booking whether or not a payment is in flight. |
| Terms | PUR-T28, PUR-T20, PUR-T26, PUR-T29 |
| Candidate responsibility and dependencies | Purchase; Payment's expire call, which returns the final state (paid stays paid). The expire answer is the reconcile read for this cancel (PUR-R24); no separate GET is needed. |
| Open question | PUR-Q09 (held booking without a session). |
| Clarification owner | Project team |
| Next use | e2e "held cancel racing with payment" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | BK-7KQ2M9 held, session unpaid; clock 10:05 | Member A presses Cancel, sees "We have not received a payment for this booking. Cancelling closes the payment page. If a payment completes first, the refund is THB 450.00 (100%).", then confirms | Session expired at Payment; status cancelled; no refund; the slot is free |
| 2 | ordinary | JSON | Same | Member A cancels | 200; status cancelled, refund_amount_satang 0 |
| 3 | boundary | JSON | Same; Payment unreachable | Member A cancels | 503 {"error": "Payment is not reachable. Please try again."}; the booking stays held |
| 4 | boundary | form | Same; Payment unreachable | Member A presses Cancel | Booking page with the flash "Payment is not reachable. Please try again."; the booking stays held |
| 5 | boundary | internal | BK-7KQ2M9 held; Member A paid in another tab at 10:04 | Member A cancels at 10:05; expire reports paid | Confirmed without a grant, then cancelled as a confirmed booking: 24 h or more before start, so refund 45000; the revoke is still sent and Access stores a tombstone |
| 6 | counterexample | form | BK-7KQ2M9 held, hold lapsed at 10:15, session unpaid | Member A cancels at 10:20 | Expire returns expired and unpaid; the hold has lapsed, so status expired, not cancelled; the flash says "This hold has already expired"; no refund |
| 7 | counterexample | JSON | Same as row 6 | Member A cancels at 10:20 | 409 {"error": "This hold has already expired"}; status expired |
| 8 | boundary | internal | Member A holds a Focus Pod 1 booking for 2026-10-05 13:00, 1 block (THB 10.00), created at 10:00; Member A paid at 10:04 in another tab | Member A cancels at 10:05; expire reports paid | Confirmed without a grant, then cancelled as a confirmed booking under 24 h before start: refund_amount_satang 0; the revoke is sent (Access stores a tombstone); no POST /refunds |
| 9 | boundary | internal | BK-7KQ2M9 held with no session (PUR-Q09); clock 10:05 | Member A cancels | cancelled, with no expire call and no refund |
| 10 | boundary | form | BK-7KQ2M9 held; Member A paid in another tab at 10:04 | Member A presses Cancel at 10:05 | The confirm screen's reconcile read finds paid: BK-7KQ2M9 is confirmed and its grant requested; the screen shows "Refund THB 450.00 (100%)", never "We have not received a payment" |
| 11 | ordinary | form | BK-7KQ2M9 held, session unpaid; clock 10:05 | Member A confirms the held screen, which posts shown_refund_satang=45000 | The check passes (the policy gives 45000 if paid); expire answers unpaid; status cancelled with refund_amount_satang 0: an unpaid held cancel is never refused for its conditional amount |
| 12 | boundary | JSON | BK-7KQ2M9 created with POST /api/bookings at 10:00; at 10:04 Member A pays its payment_url with 4242424242424242 and allow_redirects=False, never following success_url; nothing reads the booking in Purchase | At 10:05 POST /api/bookings/BK-7KQ2M9/cancel | 200: status cancelled, refund_amount_satang 45000, refund_status succeeded, grant_status revoked, ticket_url null; Access GET /grants/BK-7KQ2M9 (token) answers status revoked with ticket_code null, a tombstone; Payment collected and refunded each rise by 45000 (the e2e procedure for "held cancel racing with payment") |
| 13 | boundary | form | Clock 2026-10-05 09:55: Member A holds Board Room 2026-10-06 10:00-11:00 (THB 1,000.00), session unpaid | Member A opens the cancel screen at 09:59 ("... the refund is THB 1,000.00 (100%).") and confirms at 10:01 | Nothing is cancelled and no expire call is made; 303 to the cancel screen with the flash "The refund is now THB 0.00 (0%): the start is less than 24 h away. Confirm again." |
| 14 | boundary | form | BK-7KQ2M9 held with no session (PUR-Q09); clock 10:05 | Member A opens the cancel screen, then confirms | The screen says "Payment was not started. Nothing was charged. Cancel this hold?" and the form carries shown_refund_satang=0; the POST makes no expire call and answers 303 /bookings/BK-7KQ2M9 with "Booking cancelled"; the same POST at 10:16 would answer "This hold has already expired" and mark it expired |
| 15 | counterexample | form | BK-7KQ2M9 held with a session; clock 10:14; Payment gives no answer to the read | Member A opens the cancel screen | "Payment status unknown. If a payment went through, the refund is THB 450.00 (100%)." with shown_refund_satang=45000; never "Nothing was charged", because a payment at 10:12 is possible |
| 16 | ordinary | form | BK-7KQ2M9 held, session unpaid; clock 10:05 | The Operator cancels it from the confirm screen | Status cancelled with cancel_reason operator_cancel; the booking page says "Cancelled by the operator before payment. Nothing was charged." |

### PUR-R32 Cancel a confirmed booking in three stored steps

| Field | Value |
|---|---|
| Rule | Cancel a confirmed booking in order: (1) commit in one transaction status cancelled, cancelled_at = clock.now(), refund amount, cancel_reason, refund_reason and grant_status revoke_pending, plus, when the amount is above 0 and coverage is pay, refund_status pending with refund_attempt 1 and refund_requested_at = clock.now(); steps 2 and 3 overwrite these with the answers, so a stop after step 1 leaves both steps flagged and retried; (2) revoke the grant; (3) once the revoke has succeeded, request the refund when the amount is above 0 and coverage is pay; store each outcome on the booking (PUR-T34); show a call that got no answer (timeout, connection error or 5xx answer, PUR-R35) as "revocation pending" or "refund pending", and retry it idempotently, revoke first, when the booking page is opened (page or GET /api/bookings/<ref>), when the owner presses Retry (POST /bookings/<ref>/retry, which repeats pending steps exactly like opening the page and never starts attempt+1, whoever calls it) or when the operator presses Retry (POST /operator/bookings/<ref>/retry). A refund that Payment answered as failed is not pending (PUR-R33). The booking page builds its refund line from stored fields only (contract purchase-public.md section 7): "THB 450.00 refunded." only when refund_status is succeeded, "Refund of THB 450.00 pending." while it is pending, "Refund failed. The operator will follow up." when it failed, and, while grant_status is revoke_pending, "Your ticket is still being cancelled; any refund follows." with no "View e-ticket"; the amount is refund_amount_satang. The Operator's list flags the same states "Revocation pending", "Refund pending" and "Refund failed". |
| Policy status | Decided (D19) |
| Decision source | Project team (D19). The refund waits for the revoke: PUR-Q10 default and DECISIONS.md, Disputes decided in M1, row 6. Course [contexts site]: "The booking and successful payment remain recorded. No automatic refund is implied." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 one DELETE with no refund and no access change. |
| Terms | PUR-T28, PUR-T29, PUR-T30, PUR-T34, AXS-T06, PMT-T12 |
| Candidate responsibility and dependencies | Purchase orchestrates; Access POST /grants/{booking_reference}/revoke (idempotent); Payment POST /refunds with attempt (repeat returns the stored result). No call runs inside the step 1 transaction. Refund reasons sent: member_cancel or operator_cancel. |
| Open question | PUR-Q10 (the refund waits for the revoke); PUR-Q12 (revocation pending while the slot is rebooked); PUR-Q03 (cancellation cases we do not support). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q03; Project team for PUR-Q10, PUR-Q12 and the rule as stated |
| Next use | Cancel sequence diagrams (M2); e2e cancel variants (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 confirmed, pay; clock 2026-10-05 11:00 | Member A cancels | Commit: cancelled, refund 45000, cancel_reason and refund_reason member_cancel, grant_status revoke_pending, refund_status pending with refund_attempt 1; then revoke: revoked; then refund attempt 1 of 45000: succeeded; all three outcomes stored |
| 2 | ordinary | JSON | Same | Member A cancels | 200; "status": "cancelled", "grant_status": "revoked", "refund_status": "succeeded", "refund_amount_satang": 45000 |
| 3 | boundary | form | Access unreachable during step 2 | Member A cancels, then reopens the booking page after Access is back | First "Cancelled.", "Refund of THB 450.00 pending." and "Your ticket is still being cancelled; any refund follows.", with no "View e-ticket": no POST /refunds yet; on reopening, the revoke is retried (revoked), then refund attempt 1 of 45000 is sent (succeeded); both stored |
| 4 | boundary | form | Payment unreachable during step 3 | The Operator presses Retry after Payment is back | Refund retried as attempt 1 (Payment returns the stored result if the first call had landed); no double refund |
| 5 | counterexample | internal | Member B's plan booking, or a 0% Member cancel | Cancel | Steps 1 and 2 only; no POST /refunds |
| 6 | counterexample | internal | Purchase stops right after step 1 commits | The booking page is opened later | The booking is cancelled with grant_status revoke_pending and refund_status pending (attempt 1), both set in step 1; the all-bookings list flags "Revocation pending" and "Refund pending", the refund counts as owed, and the retries complete them, revoke first |

### PUR-R33 Only the operator retries a failed refund

| Field | Value |
|---|---|
| Rule | When Payment returns a stored failed refund, retry nothing automatically; only the operator route POST /operator/bookings/<ref>/retry starts attempt+1 (the booking page's Retry form posts there for an operator viewer; the owner route never starts it, whoever calls it), and a repeat of the same attempt returns Payment's stored result. The operator's Retry first commits attempt n+1 with a conditional update, UPDATE bookings SET refund_attempt = n+1, refund_status = 'pending' WHERE reference = <ref> AND refund_status = 'failed' AND refund_attempt = n, where n is the value it read; if no row matches, it re-reads the booking and resends a stored pending attempt as it is, or flashes "Nothing to retry", so two Retries never send attempt n+2. It then calls POST /refunds; a call with no answer leaves "Refund pending", and the same attempt n+1 is resent on the next touch. Its flashes name the attempt: "Refund attempt <n> succeeded" or "Refund attempt <n> failed" (for example "Refund attempt 1 succeeded" when a pending attempt 1 is resent); a Retry that finds no pending or failed step flashes "Nothing to retry". |
| Policy status | Decided (D19) |
| Decision source | Project team (D19) |
| Implementation evidence | Not implemented yet (planned M5). No related behaviour in the seed app (it has no refunds). |
| Terms | PUR-T29, PUR-T30, PUR-T02, PMT-T12, PMT-T15 |
| Candidate responsibility and dependencies | Purchase; Payment keys refunds on (payment_session_id, attempt) and keeps refunded total at or below collected. Payment lists failed refunds as "needs manual follow-up". |
| Open question | None. |
| Clarification owner | Project team |
| Next use | e2e refund failure card (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member C paid BK-3HT8WD (Board Room, THB 1,000.00) with test card 4000000000005126 | Member C cancels 24 h or more before start; refund attempt 1 returns failed | Stored: refund failed, attempt 1; the page says "Refund failed. The operator will follow up."; reopening the page retries nothing |
| 2 | ordinary | form | Same | The Operator presses Retry | Refund attempt 2 of 100000: succeeded; stored; the flash "Refund attempt 2 succeeded" |
| 3 | boundary | form | Same | The Operator's Retry is sent twice, one after the other (a double click the browser sends in sequence) | The first sends attempt 2, which succeeds; the second makes no call and flashes "Nothing to retry"; total refunded stays THB 1,000.00 |
| 4 | counterexample | form | Same, after attempt 1 failed | Member C, or the Operator, posts the owner route /bookings/BK-3HT8WD/retry | 303 to /bookings/BK-3HT8WD; no attempt 2; the page keeps "Refund failed. The operator will follow up." |
| 5 | boundary | internal | Refund attempt 1 got no answer (Payment unreachable) | Member C reopens the booking page | That is pending, not failed: attempt 1 is retried |
| 6 | counterexample | form | Same, after attempt 1 failed | Member C opens the BK-3HT8WD booking page | "Refund failed. The operator will follow up."; no Retry button |
| 7 | counterexample | form | Same, after attempt 1 failed | Member C posts /operator/bookings/BK-3HT8WD/retry | 404; no attempt 2 |
| 8 | boundary | internal | Attempt 1 failed; the Operator presses Retry; Payment stores attempt 2 as succeeded but the answer is lost (timeout) | The Operator opens the BK-3HT8WD booking page | refund_attempt 2 and refund_status pending were committed before the call, so the page shows "Refund pending" and resends attempt 2; Payment returns the stored succeeded result; no attempt 3 |
| 9 | boundary | form | BK-3HT8WD refunded by attempt 2; the Operator's list is stale | The Operator presses Retry on BK-3HT8WD again | No call is made; 303 to /operator/bookings with the flash "Nothing to retry" |
| 10 | boundary | internal | Same as row 1, after attempt 1 failed | Two Operator Retry POSTs are handled at the same moment by the two workers | Only one conditional update matches; the other re-reads and resends the stored pending attempt 2; Payment stores exactly one attempt 2 and never an attempt 3; refund_status succeeded; refunded total THB 1,000.00 (a Purchase integration test with two threads) |


### PUR-R34 Dashboard metrics

| Field | Value |
|---|---|
| Rule | Show operators, for the last 7 Bangkok days: bookings by status, utilization = confirmed booked hours in non-archived spaces / (12 h x non-archived spaces x 7), counted members (accounts with at least one confirmed booking), and confirmed booked hours by coverage (pay, plan, free); count plan and free bookings as bookings and hours, never as revenue; show no money totals, which live on Payment's operator page. Use the period of PUR-Q11: from 00:00 Bangkok 6 days before today to 00:00 tomorrow; a booking belongs by its start, so a confirmed booking later today counts. Bookings by status, members and hours by coverage count every booking, archived spaces included; only utilization leaves archived spaces out, in its numerator as in its denominator (PUR-Q11). The figures use stored statuses: the dashboard does not reconcile, so a lapsed hold counts as held until something reconciles it; the page offers "Reconcile all held" (PUR-R24) to press first. Show utilization as a percent with one decimal, rounded half up. The page carries each figure in a marker, always present, 0 when empty: data-utilization (the ratio rounded half up, always 4 decimals, "0.0000"), data-members (an integer), data-status-count-<status> for held, confirmed, expired and cancelled (integers) and data-hours-<coverage> for pay, plan and free (the shortest decimal with no trailing zero: "2", "1.5", "0"). With no non-archived space the denominator is 0: utilization shows "0.0%" and data-utilization="0.0000", never a division error. v1 has no JSON route for the metrics. |
| Policy status | Decided (D24) |
| Decision source | Project team (D24). The numerator, period and stored statuses: DECISIONS.md, Disputes decided in M1, row 9. Answers class questions MET-Q01, Q-MET-1 and Q-MET-2 (class rules PR #7 at 05e90b3 and PR #8 at ce99d13). |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:295-296 counts distinct typed names as members; app.py:289-290 counts subscriber bookings as paid; app.py:306-315 utilization counts unpaid bookings over 24 h days. |
| Terms | PUR-T31, PUR-T32, PUR-T19, PUR-T24, PUR-T07 |
| Candidate responsibility and dependencies | Purchase (operator only, PUR-R06). Revenue and commission come from Payment's totals. Closure bookings (PRD section 3) are plan bookings of a closure Member, so they count as plan bookings, plan hours, utilization and a member; the Operator subtracts them by hand. |
| Open question | PUR-Q11 (which 7 days, which bookings); PUR-Q02 (plan usage if plans are sold); PUR-Q08 (plan or free label for a plan Member's free booking). |
| Clarification owner | Course instructor (business stakeholder) for PUR-Q02; Project team for PUR-Q11, PUR-Q08 and the rule as stated |
| Next use | BUSINESS_MODEL metrics by rule ID (M2); Purchase tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Clock 2026-10-08 10:00; 4 non-archived spaces; confirmed: BK-7KQ2M9 (Member A, 1.5 h, pay) and a Member B plan booking of Board Room 2026-10-06 13:00-15:00 (2 h); one expired Member C booking | The Operator opens the dashboard | Bookings: confirmed 2, expired 1; members 2; utilization 3.5 / 336 = 1.0%; confirmed hours by coverage: pay 1.5, plan 2, free 0 |
| 2 | ordinary | form | Same | The Operator opens the dashboard; the test reads its markers | data-utilization="0.0104", data-members="2", data-status-count-confirmed="2", data-status-count-expired="1", data-hours-pay="1.5", data-hours-plan="2", data-hours-free="0"; no marker and no text for money |
| 3 | boundary | form | Same, plus a cancelled Member A booking of 2 h | The Operator opens the dashboard | cancelled 1 is listed; its hours do not count in utilization |
| 4 | counterexample | form | Same | Look for revenue | None on this page; Member B's plan booking adds a booking, not THB 2,000.00 of revenue |
| 5 | counterexample | form | Member A has two confirmed bookings in the period | Count members | Member A counts once (by account) |
| 6 | boundary | internal | Clock 2026-10-08 10:00 | Count confirmed bookings starting 2026-10-02 08:00, 2026-10-01 19:30 and 2026-10-08 15:00 | The first counts; the second does not (before the period); the third counts (later today is inside the period) |
| 7 | boundary | form | As row 1, plus a confirmed Member C pay booking of Focus Pod 1 2026-10-03 10:00-12:00 (2 h); Focus Pod 1 archived on 2026-10-07 | The Operator opens the dashboard | confirmed 3, members 3, hours by coverage pay 3.5, plan 2; utilization 3.5 / (12 x 3 x 7 = 252) = 1.4% (data-utilization="0.0139"): the archived space leaves both numerator and denominator |
| 8 | counterexample | form | Clock 2026-10-05 10:20; Member A's Focus Pod 1 booking for 2026-10-05 13:00 is held, its hold lapsed unpaid at 10:15, and nothing has touched it | The Operator opens the dashboard, presses "Reconcile all held", then opens the dashboard again | First held 1: stored statuses, no reconcile on a read; then held 0, expired 1 |
| 9 | boundary | form | A fresh install: no space yet (or every space archived); only the Operator is registered | The Operator opens the dashboard | 200; utilization "0.0%", data-utilization="0.0000"; data-members="0"; every data-status-count and data-hours marker is "0"; never a 500 |

### PUR-R35 Only Purchase calls other services

| Field | Value |
|---|---|
| Rule | Reach Payment and Access only through their HTTP APIs with bearer tokens (PAYMENT_API_TOKEN, ACCESS_API_TOKEN) and timeout=5; never read another service's database; never call while a database transaction is open; treat a timeout, a connection error or a 5xx answer as "unreachable"; treat any other 4xx answer as a Purchase or config defect: log the operation, the booking reference and the status (never the token), store nothing, and handle the step like "unreachable" (pending, or "try again" where the request needs the answer), except that an operator's Retry or Reconcile flashes the status, for example "Payment refused the call (401): check the service settings and the Purchase log."; refuse to start when PAYMENT_API_TOKEN or ACCESS_API_TOKEN is unset, empty or shorter than 32 characters; Payment and Access never call Purchase. |
| Policy status | Decided (D13, D28) |
| Decision source | Project team (D13, D28). ADR-0003 (database per service); ADR-0004 (Purchase-only callers), no webhooks. Course [contexts site]: "Shared references connect the models. They do not make them one shared object." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:23-25 and app.py:387 one process shares one database connection for booking, payment and access. |
| Terms | PUR-T17, PUR-T18, PUR-T26, PUR-T33, PMT-T17, AXS-T19 |
| Candidate responsibility and dependencies | Purchase owns payment_client.py and access_client.py, the one boundary where tests stub the providers. Internal and public URLs are separate settings. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | ARCHITECTURE and ADRs (M2); consumer tests (M5); integration compose (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | BK-7KQ2M9 inserted and committed | Purchase requests the payment session | HTTP POST to PAYMENT_INTERNAL_URL with "Authorization: Bearer" and PAYMENT_API_TOKEN, timeout 5 s |
| 2 | boundary | internal | Payment would answer after 6 s | Member A cancels the held booking | The call times out at 5 s and counts as unreachable: 503 and nothing changes (PUR-R31) |
| 3 | counterexample | internal | Purchase needs a refund outcome | Read Purchase's settings | Purchase's env and compose give it one DATABASE_URL (purchase-db); a config test asserts that no Payment or Access database host appears; outcomes come only through the Payment API |
| 4 | counterexample | internal | The cancel transaction of step 1 is open | The stubbed payment_client and access_client are called | Each stub asserts that the database connection's transaction status is IDLE on every call; a call inside a transaction fails the test |
| 5 | counterexample | internal | Member A closed the tab after paying | Wait for Payment to tell Purchase | Payment never calls; the next read reconciles (PUR-R24) |
| 6 | boundary | internal | Payment answers GET /payment-sessions/{id} with 500 | Member A opens the BK-7KQ2M9 booking page | Unreachable, as for a timeout: nothing changes; "Payment status unknown, refresh later" |
| 7 | counterexample | internal | ACCESS_API_TOKEN unset or empty | Start the Purchase service | Non-zero exit with the message "ACCESS_API_TOKEN is required"; the same for PAYMENT_API_TOKEN |
| 8 | boundary | form | ACCESS_API_TOKEN in Purchase differs from the one Access holds; BK-7KQ2M9 is confirmed with grant_status pending | The Operator presses Retry | Access answers 401; 303 to /operator/bookings with the flash "Access refused the call (401): check the service settings and the Purchase log."; grant_status stays pending; the log names the operation, BK-7KQ2M9 and 401, never the token |
| 9 | boundary | internal | ACCESS_API_TOKEN is 31 characters, then 32 (the same for PAYMENT_API_TOKEN) | Start the Purchase service | 31: non-zero exit with the message "ACCESS_API_TOKEN must be at least 32 characters"; 32: it starts |

### PUR-R36 Form outcomes are flashed messages

| Field | Value |
|---|---|
| Rule | After a browser form action, redirect and show the outcome as a one-time flashed message; never show text taken from the URL (`?error=`, `?message=`, `?code=`) as a message; never write a query string to the access log (gunicorn logs the path only, kept from the seed). |
| Policy status | Decided (D28) |
| Decision source | Project team (D28) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:440, app.py:472, app.py:515-516 and app.py:832-833 render `?error=` and `?code=` text from the URL. |
| Terms | PUR-T17 |
| Candidate responsibility and dependencies | Purchase (all templates). JSON callers get a status code and a JSON body, never a redirect. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Shared base template (M5); every form row in these rules; Purchase template test that ?error=, ?message= and ?code= never render (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member B loses the race for 09:00-10:30 | The form post returns | Redirect to the space page; flash "Slot just taken" shown once |
| 2 | boundary | form | Same | Member B reloads the page | The message is gone |
| 3 | counterexample | form | Member A is logged in | Open the booking page with "?error=Refund sent" added to the URL | No message is shown; the URL text is ignored |
| 4 | ordinary | JSON | Same race, JSON caller | The request returns | 409 {"error": "Slot just taken"}; no redirect |
| 5 | counterexample | form | Member A is logged in | Open the BK-7KQ2M9 booking page with "?code=AAAA-AAAA" added to the URL | No code or message is shown; the page shows only stored values |
| 6 | counterexample | internal | Member A returns from paying | Read the access log line for GET /bookings/BK-7KQ2M9/return?session_id=ps_Q7mZ3xK9vT2bN8rL4wYc1A | Method, path /bookings/BK-7KQ2M9/return and status only; no query string, no referer |

### PUR-R37 Browser actions are POSTs; logout clears the cookie

| Field | Value |
|---|---|
| Rule | Run every state-changing browser action as a POST: book, cancel, log out, Retry, Reconcile, archive, the plan toggle and every space edit. A GET never starts one; it may only run the idempotent sync of D13, D19 and D20 (reconcile, pending grant, revoke or refund), which moves a booking only toward an outcome already decided. POST /logout clears purchase_session. |
| Policy status | Decided (D15) |
| Decision source | Project team (D15). ADR-0009 (SameSite as the CSRF mitigation): SameSite=Lax holds back the cookie only on cross-site POSTs, so this rule is what makes it a CSRF mitigation. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:533-536 logout is already a POST that pops the user id from the cookie. |
| Terms | PUR-T03, PUR-T26, PUR-T30 |
| Candidate responsibility and dependencies | Purchase (all forms and routes). Payment's Pay (PMT-R10) and the Access kiosk room choice and scan (AXS-R11) are POSTs too. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | ADR-0009 (SameSite as the CSRF mitigation); Purchase route test that every GET changes nothing except the D13, D19 and D20 sync (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Member A is logged in | Member A presses Log out (POST /logout) | purchase_session cleared; redirect to the spaces page with the flash "Logged out" |
| 2 | boundary | form | Member A is logged in; BK-7KQ2M9 confirmed | The browser sends GET /logout, GET /bookings/BK-7KQ2M9/retry or GET /operator/bookings/BK-7KQ2M9/cancel; then GET /bookings/BK-7KQ2M9/cancel | 405 for the first three; the last is 200, the confirm screen only; Member A stays logged in and BK-7KQ2M9 is unchanged |
| 3 | counterexample | JSON | No purchase_session cookie | Post Cancel for BK-7KQ2M9 | 401; BK-7KQ2M9 is unchanged |
| 4 | boundary | form | BK-7KQ2M9 held; its session was paid at 10:04 | Member A opens My bookings (a GET) at 10:06 | BK-7KQ2M9 becomes confirmed: the D13 sync is the only change a GET may make, and nothing in the request steers it |

### PUR-R38 The test clock is off unless TEST_CLOCK_ENABLED=true

| Field | Value |
|---|---|
| Rule | Read time only through clock.now(); never use SQL now() or CURRENT_TIMESTAMP in business logic (column defaults for audit timestamps such as created_at are fine). Answer POST /_test/clock with 404 unless TEST_CLOCK_ENABLED is exactly "true"; when it is, store {"now": iso-or-null} in the one-row test_clock table, where null clears the override; a "now" that is not ISO 8601 with an offset gets 400 and stores nothing (D2). With the flag off, clock.now() returns real time and never reads test_clock, even if a row still holds an override (an e2e run leaves one in the integration volumes). The override is a fixed instant: clock.now() returns exactly the stored value on every read until the next POST /_test/clock; it never advances. With the flag on, clock.now() reads the test_clock row on every call (no per-process cache), so both gunicorn workers see a new instant from the next request. Never set the flag in the Dockerfile, the service compose.yaml or .env.example. |
| Policy status | Decided (D27) |
| Decision source | Project team (D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:175, app.py:311, app.py:420 and app.py:427 read Postgres now() in business logic (seed flaw A11). |
| Terms | PUR-T08, PUR-T12, PUR-T21 |
| Candidate responsibility and dependencies | Purchase. Payment and Access have the same guard (PMT-R20, AXS-R19); the e2e suite sets the same instant on all three. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Purchase clock and guard tests (M5); e2e setup (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | TEST_CLOCK_ENABLED=true; BK-7KQ2M9 held until 10:15 | POST /_test/clock {"now": "2026-10-05T10:15:00+07:00"} | 200; clock.now() returns that instant; the grid shows 2026-10-07 09:00-10:30 free |
| 2 | boundary | JSON | TEST_CLOCK_ENABLED=true; an override is set | POST /_test/clock {"now": null} | 200; the override is cleared and clock.now() is the real time again |
| 3 | counterexample | JSON | TEST_CLOCK_ENABLED unset, "false" or "1" | POST /_test/clock {"now": "2026-10-05T10:15:00+07:00"} | 404; nothing stored; clock.now() unchanged |
| 4 | counterexample | internal | The Purchase Dockerfile, compose.yaml and .env.example | Look for TEST_CLOCK_ENABLED | Set in none of them; only the e2e compose override sets it |
| 5 | counterexample | JSON | TEST_CLOCK_ENABLED=true | POST /_test/clock {"now": "2026-10-05T10:15:00"} (no offset), or {"now": "soon"} | 400; nothing stored; clock.now() unchanged |
| 6 | counterexample | internal | An override 2026-10-05T10:15:00+07:00 is stored; Purchase restarts with TEST_CLOCK_ENABLED unset | Read the time (for example, open the grid) | Real time: clock.now() never reads test_clock while the flag is off |
| 7 | boundary | internal | TEST_CLOCK_ENABLED=true; override 2026-10-05T10:12:50+07:00 | Read clock.now() twice, 2 s apart | Both reads return 2026-10-05T10:12:50+07:00: the override never advances |
| 8 | boundary | internal | TEST_CLOCK_ENABLED=true; two Purchase app instances with their own database connections (like the two workers) share one database | Instance 1 handles POST /_test/clock {"now": "2026-10-05T10:15:00+07:00"}; then instance 2 reads clock.now() | 2026-10-05T10:15:00+07:00: clock.now() reads the row on every call, never a per-process copy (a service test) |

### PUR-R39 One held booking per Member; checks run in a fixed order

| Field | Value |
|---|---|
| Rule | Let a Member have at most one slot-blocking held booking. Reconcile the Member's own lapsed holds before this check. Refuse every request other than the same space, start and blocks (which resumes the hold, PUR-R21) until the hold resolves, plan and free requests too. Run the checks in this order: (1) the shape checks give 400: a time with an offset, the :00 or :30 start, 1 to 8 blocks, inside opening hours; (2) the Member's own lapsed holds are reconciled, then the Member's own match: a slot-blocking hold of the same space, start and blocks resumes it (PUR-R21; from the payment deadline it answers "Time to pay has run out", PUR-R40), and a confirmed booking of the same space, start and blocks answers with that booking (PUR-R21); (3) the notice, horizon, party-size and note-length checks give 400; (4) the one-held-booking check gives 409 {"error": "Finish or cancel your held booking <reference> first"} (JSON) or the same flash (form), or from that hold's payment deadline {"error": "Time to pay has run out on <reference>; cancel it, or try again from 10:15"}; (5) the slot check gives 409 "Slot just taken" (PUR-R12). A match answers with the stored booking and its stored values, so a resume is never refused by a check that the stored booking has since failed (notice, a lowered capacity). Two workers run (D28), so one Member's requests can arrive at once: the insert transaction first locks the Member's row (SELECT ... FOR UPDATE on members), then runs step (2)'s own match and step (4) again inside that transaction before the insert; on an EXCLUDE violation Purchase re-reads the Member's own slot-blocking hold of the same space, start and blocks and, when there is one, answers as a resume (form: 303 to the same hosted page; JSON: 200). |
| Policy status | Decided (D11) |
| Decision source | Project team (D11). The check order: DECISIONS.md, Disputes decided in M1, row 4. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:700-772 `book_space` checks the space, the times, the party size and overlap, then inserts, with no limit on a member's unpaid bookings. |
| Terms | PUR-T01, PUR-T20, PUR-T21, PUR-T26 |
| Candidate responsibility and dependencies | Purchase; Payment for reconciling the Member's lapsed hold (GET /payment-sessions/{id}, PUR-R24). |
| Open question | PUR-Q17 (repeated holds without paying: a Member may cancel a hold and hold the same slot again at once). |
| Clarification owner | Course instructor (business stakeholder), with the project team, for PUR-Q17; Project team for the rule as stated |
| Next use | Error list of the Purchase booking API in the contracts (M2); Purchase tests of the check order (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | BK-7KQ2M9 held until 10:15 | At 10:05 Member A sends a booking request for Focus Pod 1 | 409 {"error": "Finish or cancel your held booking BK-7KQ2M9 first"}; no new booking |
| 2 | ordinary | form | Same | At 10:05 Member A presses "Continue to payment" for Focus Pod 1 | Space page with the flash "Finish or cancel your held booking BK-7KQ2M9 first"; no new booking |
| 3 | boundary | JSON | Same | At 10:05 Member A books Community Table (free) | 409 "Finish or cancel your held booking BK-7KQ2M9 first": a plan or free request is refused too (D11) |
| 4 | boundary | JSON | BK-7KQ2M9's hold lapsed unpaid at 10:15 | At 10:20 Member A books Focus Pod 1 | BK-7KQ2M9 reconciled first and marked expired; the new booking gets 201 |
| 5 | counterexample | JSON | BK-7KQ2M9 held until 10:15 | At 10:05 Member A sends start "2026-10-07T09:15:00+07:00" for Focus Pod 1 | 400 "Start on :00 or :30", not 409: the shape checks run first |
| 6 | counterexample | JSON | BK-7KQ2M9 held until 10:15; a confirmed booking takes Board Room 2026-10-08 09:00-10:00 | At 10:05 Member A books Board Room with start "2026-10-08T09:00:00+07:00", 2 blocks | 409 "Finish or cancel your held booking BK-7KQ2M9 first", not "Slot just taken": the one-held-booking check runs before the slot check |
| 7 | boundary | JSON | At 10:00 Member A held Focus Pod 1 for 2026-10-05 11:00, 1 block | At 10:05 Member A sends the same space, start and blocks | 200 with that held booking and its payment_url, not 400 "Book at least 60 minutes ahead": the own match runs before the notice check |
| 8 | boundary | JSON | BK-7KQ2M9 held, party size 4; the Operator then lowered Meeting Room A's capacity to 3 | At 10:05 Member A sends the standard booking body again | 200 with BK-7KQ2M9 as stored (party size 4), not 400 "Party size must be 1 to 3" |
| 9 | boundary | JSON | Member A has no held booking; Meeting Room A 2026-10-07 09:00-10:30 is free | Member A sends the standard booking body twice at the same instant (a double click reaching both workers) | One booking; both answers carry the same reference and payment_url (one 201, one 200), never 409 for the Member's own hold (a two-thread Purchase integration test) |
| 10 | counterexample | JSON | Member A has no held booking | Member A sends Meeting Room A 09:00 and Board Room 13:00 on 2026-10-07 at the same instant | One 201 and one 409 {"error": "Finish or cancel your held booking <reference> first"}: never two held bookings (a two-thread Purchase integration test) |
| 11 | counterexample | form | Member A has no held booking | Member A posts the Meeting Room A booking form with no start picked | 303 back to the space page with the flash "Pick a start time"; nothing created |

### PUR-R40 A hold cannot be paid after its session expires

| Field | Value |
|---|---|
| Rule | Count down on the booking page to the payment deadline, hold_expires_at - 2 min ("Pay by 10:13"), not to hold_expires_at, the way the hosted page does (PMT-R07): the server renders "Pay by 10:13 (N min left)" with data-seconds-left computed from clock.now() (N is the whole minutes left rounded up; under 60 s it reads "less than 1 min left"); every held state before the deadline, "Payment could not be started" and "Payment status unknown" included, carries data-seconds-left and the countdown script; and a few lines of inline script count down and, at zero, hide "Continue to payment" and show "Time to pay has run out"; without script the server decides on reload. The deadline is derived for every held pay booking, with or without a session; when a session exists it equals the session's expires_at. The booking page shows the from-deadline state whenever the session reads expired, even before the deadline (PUR-R21). From the payment deadline until hold_expires_at the hold can no longer be paid: the booking page replaces the countdown and "Continue to payment" with "Time to pay has run out. Nothing was charged. Cancel this hold to book again now, or it ends at 10:15." and a Cancel button; a booking request for the same space and time sends no session request and no redirect, and answers "Time to pay has run out; cancel this hold or book again from 10:15". Until hold_expires_at the hold still blocks its slot and the Member's other requests (PUR-R39); from the payment deadline the held-booking banner, the My bookings row and the 409 for another request say "Time to pay has run out on BK-7KQ2M9; cancel it, or try again from 10:15", never "pay by". The booking page's held states apply in this order: (1) from the payment deadline "Continue to payment" is never shown; (2) "Nothing was charged" is shown only after a read returned unpaid, or when there is no session; (3) a read with no answer at or after the deadline shows "Payment status unknown. If you paid before 10:13, your booking will be confirmed: refresh in a minute." and Cancel, never "Time to pay has run out", because a payment just before the deadline may still be confirmed. |
| Policy status | Decided (D11, D12) |
| Decision source | Project team (D11, D12). The unpayable end of a hold and the countdown: DECISIONS.md, Disputes decided in M1, row 4. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:49-117 the bookings table has no status or expiry column, so there is no payment deadline. |
| Terms | PUR-T20, PUR-T21, PUR-T26, PMT-T06 |
| Candidate responsibility and dependencies | Purchase; Payment refuses attempts at or after expires_at on its own (PMT-R11). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Booking page countdown (M2 screen list); e2e "hold expiry frees the slot" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | BK-7KQ2M9 held until 10:15; its session expires_at 10:13 | At 10:05 Member A opens the booking page | "Pay by 10:13" (8 min left), not 10:15, and a "Continue to payment" button |
| 2 | boundary | form | Same | At 10:12 Member A presses "Continue to payment" | Browser sent to the Payment hosted page; the session takes attempts before 10:13 |
| 3 | boundary | JSON | BK-7KQ2M9 held until 10:15; its session expired unpaid at 10:13 | At 10:14 Member A sends the same space and time again | 409 {"error": "Time to pay has run out; cancel this hold or book again from 10:15"}; no session request; BK-7KQ2M9 stays held until 10:15 |
| 4 | boundary | form | Same | At 10:14 Member A opens the booking page, then posts the booking form for the same slot | The page shows "Time to pay has run out. Nothing was charged. Cancel this hold to book again now, or it ends at 10:15." and Cancel, with no countdown and no "Continue to payment"; the post redirects to the booking page with the flash "Time to pay has run out; cancel this hold or book again from 10:15"; no redirect to Payment |
| 5 | counterexample | JSON | Same | At 10:14 Member A books Focus Pod 1 | 409 held_booking_exists "Time to pay has run out on BK-7KQ2M9; cancel it, or try again from 10:15": the hold still blocks until 10:15 (PUR-R39) |
| 6 | boundary | JSON | Same | At 10:15 Member A sends the same space and time again | BK-7KQ2M9 reconciled first and marked expired; 201 with a new booking reference and hold_expires_at "2026-10-05T10:30:00+07:00" |
| 7 | counterexample | JSON | BK-7KQ2M9 held until 10:15 with no session: POST /payment-sessions got no answer at 10:00 (PUR-Q09) | At 10:14 Member A sends the same space and time again | 409 "Time to pay has run out; cancel this hold or book again from 10:15"; no session request: the deadline 10:13 is derived from hold_expires_at, not from a session |
| 8 | counterexample | form | BK-7KQ2M9 held until 10:15 with a session; Payment unreachable | At 10:14 Member A opens the booking page | "Payment status unknown. If you paid before 10:13, your booking will be confirmed: refresh in a minute." and Cancel; no "Continue to payment", no "Nothing was charged" and no "Time to pay has run out" (the read failed, and a payment at 10:12 is possible) |
| 9 | boundary | form | Same, Payment back; the session is unpaid | At 10:14 Member A opens the space page and My bookings | The banner and the row say "Time to pay has run out on BK-7KQ2M9; cancel it, or try again from 10:15", not "pay by 10:13" |
| 10 | boundary | form | Test clock 10:12:50; BK-7KQ2M9 held with an open session | Open the booking page in a browser and wait | manual: the page renders data-seconds-left="10"; within about 10 s "Continue to payment" is hidden and "Time to pay has run out" shows; the test clock is a fixed instant, so a reload still renders data-seconds-left="10" until the clock is set to 10:13:00 or later |

### PUR-R41 The booking page shows the ticket code, read live from Access

| Field | Value |
|---|---|
| Rule | On the owner's (or the Operator's) page of a confirmed booking whose grant is issued or checked in, show the ticket code in the XXXX-XXXX form next to the "View e-ticket" link; read it on each page view with GET /grants/{booking_reference} (bearer token, timeout 5 s, never inside a DB transaction) and never store it in Purchase; if Access does not answer, show the link and "Ticket code unavailable right now"; never show a code for a cancelled or expired booking. |
| Policy status | Decided (D17, D20) |
| Decision source | Project team (D17, D20; ADR-0021). Aligns the booking page with the course target's last step, Purchase showing the code to the Member ([journey site]), without copying Access data into Purchase (ADR-0003). |
| Implementation evidence | Not implemented yet (planned M8). |
| Terms | PUR-T17, PUR-T18, AXS-T02, AXS-T08, AXS-T11 |
| Candidate responsibility and dependencies | Purchase renders; Access owns the grant and the code (AXS-R01, AXS-R05) and answers GET /grants/{booking_reference}. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Purchase booking page; e2e happy path. |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | BK-7KQ2M9 confirmed; its grant is issued with ticket code H7K3-9QXA | Member A opens /bookings/BK-7KQ2M9 | The page shows "H7K3-9QXA" and the "View e-ticket" link; Purchase stores no ticket code |
| 2 | boundary | form | Same; Access does not answer within 5 s | Member A opens the booking page | "View e-ticket" link and "Ticket code unavailable right now"; the booking stays confirmed |
| 3 | counterexample | form | BK-7KQ2M9 cancelled; its grant is revoked | Member A opens the booking page | No ticket code is shown; the status is cancelled |
| 4 | counterexample | form | BK-7KQ2M9 confirmed | Member B (not the owner) opens /bookings/BK-7KQ2M9 | 404, no code (PUR-R05) |

## Payment

### PMT-R01 Only Purchase calls the Payment API

| Field | Value |
|---|---|
| Rule | Every Payment JSON API route (POST /payment-sessions, GET /payment-sessions/{id}, POST /payment-sessions/{id}/expire, POST /refunds) needs the header "Authorization: Bearer" followed by PAYMENT_API_TOKEN. A missing or wrong token, or the wrong scheme, gets 401 {"error": "unauthorized"} before any validation or lookup (401 before 400 or 404) and changes nothing. Payment refuses to start when PAYMENT_API_TOKEN is unset, empty or shorter than 32 characters. The hosted page, /health and the operator page do not use this token. |
| Policy status | Decided (D13; ADR-0004 (Purchase-only callers), no webhooks) |
| Decision source | Project team (ADR-0004 (Purchase-only callers), no webhooks); D13 makes Purchase the only caller |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:987-997 `POST /bookings/<int:booking_id>/pay` takes any anonymous caller and a force_failure flag. |
| Terms | PMT-T17, PMT-T02, PMT-T12 |
| Candidate responsibility and dependencies | Payment checks the token with a constant-time compare of UTF-8 bytes (hmac.compare_digest on encoded values, ADR-0019). Purchase keeps the same PAYMENT_API_TOKEN in its env and sends it on every call with timeout=5 (D28). |
| Open question | PMT-Q05 (anyone with the payment link may pay). |
| Clarification owner | Project team |
| Next use | Contract purchase→payment (M2), security section; Payment openapi.yaml securitySchemes; Payment API tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Purchase sends "Authorization: Bearer" with the right token | POST /payment-sessions with the standard body | 201 with the new session (PMT-R02) |
| 2 | counterexample | JSON | No Authorization header | POST /payment-sessions with the standard body | 401 {"error": "unauthorized"}; no session stored |
| 3 | boundary | JSON | The token with its last character changed, or the right token sent as "Basic" | GET /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A | 401 {"error": "unauthorized"}; no session data returned |
| 4 | counterexample | form | Member A's browser, no token | GET /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A at 2026-10-05 10:01 | 200, the hosted page (PMT-R07): the page is not part of the API |
| 5 | counterexample | internal | PAYMENT_API_TOKEN unset or empty | Payment starts | Non-zero exit with the message "PAYMENT_API_TOKEN is required"; an empty token never matches |
| 6 | counterexample | JSON | No Authorization header | POST /payment-sessions with amount_satang 5 (invalid) | 401 {"error": "unauthorized"}, not 400: the token is checked first |
| 7 | counterexample | JSON | Any state | GET /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A with "Authorization: Bearer é" (a non-ASCII token) | 401 {"error": "unauthorized"}, never a 500: the compare runs on UTF-8 bytes |
| 8 | boundary | internal | PAYMENT_API_TOKEN is 31 characters, then 32 | Payment starts | 31: non-zero exit with the message "PAYMENT_API_TOKEN must be at least 32 characters"; 32: it starts |

### PMT-R02 A payment session needs a valid request

| Field | Value |
|---|---|
| Rule | POST /payment-sessions accepts only: booking_reference (non-empty text), amount_satang (an integer, at least 1000 = THB 10.00), currency "THB", description (text), success_url and cancel_url (absolute http or https URLs), expires_at (ISO 8601 with an offset; for a new session it must be after clock.now()). A new valid request gets 201 with id (ps_ + secrets.token_urlsafe(16): 128 random bits, unique, because the id is the only key to the hosted page), url, status open, payment_status unpaid, amount_satang, currency, booking_reference and expires_at. Anything else gets 400 with an error that names the field, and nothing is stored; an integer outside the BIGINT range also gets 400, never a 500. |
| Policy status | Decided (D1) |
| Decision source | Project team (D1, D2, D9, D12) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:216-217 is_valid_price accepts 0 with no upper bound, and app.py:90 stores amount_cents as INTEGER (overflow gives a 500). |
| Terms | PMT-T02, PMT-T05, PMT-T06, PUR-T18 |
| Candidate responsibility and dependencies | Payment validates. Purchase sends the agreed price (D8) only for coverage pay (D10), and expires_at = hold_expires_at minus 2 min (D12). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contract purchase→payment examples "success" and "invalid input" (M2); openapi.yaml request schema; Payment API tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Clock 2026-10-05T10:00:00+07:00; no session for BK-7KQ2M9 | POST /payment-sessions with the standard body | 201 {"id": "ps_Q7mZ3xK9vT2bN8rL4wYc1A", "url": "http://localhost:8002/pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A", "status": "open", "payment_status": "unpaid", "amount_satang": 45000, "currency": "THB", "booking_reference": "BK-7KQ2M9", "expires_at": "2026-10-05T10:13:00+07:00"} |
| 2 | boundary | JSON | Member A books Focus Pod 1 for 1 block (THB 10.00), booking BK-9MZ4RC | POST with amount_satang 1000 | 201; the hosted page will show "THB 10.00" |
| 3 | boundary | JSON | No session for the reference | POST with amount_satang 999 | 400 {"error": "amount_satang must be at least 1000 (THB 10.00)"}; nothing stored |
| 4 | counterexample | JSON | A free Community Table booking (THB 0.00) | POST with amount_satang 0 | 400, same error. Purchase never sends free or plan bookings (D10), so no card form for THB 0.00 can exist |
| 5 | counterexample | JSON | No session for the reference | POST with expires_at "2026-10-05T10:13:00" (no offset) | 400 {"error": "expires_at must be ISO 8601 with an offset"} (D2) |
| 6 | counterexample | JSON | No session for the reference | POST with currency "USD", or amount_satang 450.5, or amount_satang "45000" | 400; only THB and whole satang as an integer |
| 7 | boundary | JSON | Clock 2026-10-05T10:00:00+07:00; no session for the reference | POST with expires_at "2026-10-05T10:00:00+07:00" | 400 {"error": "expires_at must be in the future"} |
| 8 | boundary | JSON | No session for the reference | POST with amount_satang 9223372036854775808 | 400 {"error": "amount_satang is out of range"}; nothing stored; never a 500 |
| 9 | counterexample | JSON | Two new sessions, for BK-7KQ2M9 and BK-3HT8WD | Compare their ids | Both match ^ps_[A-Za-z0-9_-]{22}$ and share no sequence: neither id can be guessed from the other |

### PMT-R03 One payment session per booking reference

| Field | Value |
|---|---|
| Rule | booking_reference is unique among sessions. A valid POST /payment-sessions for a reference that already has a session returns that session unchanged with 200 when amount_satang and currency match, whatever its status and whatever the other fields say. A different amount gets 409 and changes nothing. Payment never opens a second session for a reference. |
| Policy status | Decided (D11) |
| Decision source | Project team (D8, D11); Course [extraction site]: "Reuse or new attempt? Agree identity and behaviour; do not assume." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:950-951 paying an already-paid booking returns it unchanged with 200; no session object exists. |
| Terms | PMT-T02, PMT-T03, PMT-T05, PUR-T18 |
| Candidate responsibility and dependencies | Payment keeps a UNIQUE constraint on booking_reference and compares amount and currency. Purchase resends the same body when the Member presses "Continue to payment" again for the same held booking (D11). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contract purchase→payment example "repeat" (M2); e2e "repeated POST /payment-sessions with a different amount gets 409" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Standard session open | At 10:04 Purchase sends the standard body again (Member A pressed "Continue to payment" twice) | 200 with the same id, url and expires_at; no new session |
| 2 | boundary | JSON | Standard session open | Repeat with amount_satang 45000 and THB, but expires_at "2026-10-05T10:20:00+07:00" and a new description | 200 with the stored session; expires_at stays "2026-10-05T10:13:00+07:00" |
| 3 | counterexample | JSON | Standard session open | Repeat with amount_satang 30000 | 409 {"error": "BK-7KQ2M9 already has a payment session for 45000 THB"}; the session keeps 45000 |
| 4 | boundary | JSON | Standard session paid at 10:04 | Repeat with the standard body at 10:06 | 200 with status "complete", payment_status "paid"; Purchase then applies fulfilment (D14); no second charge |
| 5 | boundary | JSON | Standard session expired at 10:13, unpaid | Repeat with the standard body at 10:14 | 200 with status "expired"; no new session (a new booking gets a new reference) |

### PMT-R04 Payment collects the agreed amount as given

| Field | Value |
|---|---|
| Rule | Payment takes amount_satang from Purchase as the agreed price and never re-prices it: it holds no rates, no price rules and no coverage. The amount is fixed on the session for life. The hosted page shows it, a succeeded attempt collects exactly it, and refunds are capped by it. |
| Policy status | Decided (D8) |
| Decision source | Project team (D8), following Course instructor (class rules PR #14 at 25ca71e): "Payments consumes the recorded amount rather than recalculating it"; Course [contexts site]: "Payments does not re-price the booking." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:953-965 mark_booking_paid marks the booking paid without checking amount_cents. |
| Terms | PMT-T05, PMT-T02, PMT-T07, PMT-T13, PUR-T23 |
| Candidate responsibility and dependencies | Payment shows and collects. Purchase owns the booking price (stakeholder-clarified, class rules PR #14 at 25ca71e) and sends it. |
| Open question | None. |
| Clarification owner | Course instructor (class rules PR #14 at 25ca71e) for the price; Project team for Payment |
| Next use | Contract purchase→payment clause "Same amount and currency" (M2); the D14 fulfilment check in Purchase; Payment tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session (amount_satang 45000) | Member A opens /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A and pays with 4242424242424242 | The page shows "THB 450.00"; the succeeded attempt collects 45000; amount collected 45000 |
| 2 | boundary | form | A session with amount_satang 4000000 (a THB 10,000-per-hour space, 8 blocks: the largest possible price) | Member A opens the page | "THB 40,000.00"; a success collects 4000000 |
| 3 | boundary | JSON | After the session was created, the Operator changes Meeting Room A to THB 400 per hour in Purchase | Purchase GETs the session | amount_satang is still 45000: Payment never saw a rate and never recalculates |
| 4 | counterexample | JSON | Standard session open | Purchase repeats the create with amount_satang 40000 | 409; the session is not re-priced (PMT-R03) |
| 5 | counterexample | internal | Member B (plan_active true) books Meeting Room A | Purchase creates the booking with coverage plan | No session is created; Payment never decides coverage and never sees plan bookings (D10) |

### PMT-R05 Session states and expiry

| Field | Value |
|---|---|
| Rule | A session is open until a succeeded attempt makes it complete, or it becomes expired. It is expired from the instant clock.now() reaches expires_at, or after an expire request (PMT-R06); every read, JSON and hosted page, reports it so. complete and expired are final. payment_status is paid only when the session is complete. GET /payment-sessions/{id} returns the session in the create response shape; an unknown id gets 404. Refunds never change status or payment_status (PMT-R16). |
| Policy status | Decided (D12) |
| Decision source | Project team (D12, D13, D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:55 a boolean paid column on the booking row and no expiry, so an unpaid booking holds its slot forever. |
| Terms | PMT-T02, PMT-T03, PMT-T04, PMT-T06 |
| Candidate responsibility and dependencies | Payment derives expiry from clock.now() (D27). Purchase reads the session when it reconciles a held booking (D13) and interprets the result. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contract status table and the state diagram (M2); Purchase reconciliation tests with a stubbed payment_client.py (M5); e2e lost redirect and hold expiry (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Standard session, no attempt, clock 2026-10-05T10:05:00+07:00 | GET /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A | 200 status "open", payment_status "unpaid" |
| 2 | ordinary | JSON | Member A paid with 4242424242424242 at 10:04 | GET at 10:05 | 200 status "complete", payment_status "paid" |
| 3 | boundary | JSON | No attempt; clock 2026-10-05T10:12:59+07:00 | GET | status "open", payment_status "unpaid" |
| 4 | boundary | JSON | No attempt; clock 2026-10-05T10:13:00+07:00 | GET | status "expired", payment_status "unpaid" |
| 5 | counterexample | JSON | Member A paid at 10:04 | GET at 10:20, after expires_at | Still "complete" and "paid": expiry never undoes a payment |
| 6 | counterexample | JSON | No such session | GET /payment-sessions/ps_doesnotexist | 404 {"error": "payment session not found"} |
| 7 | boundary | form | No attempt; clock 2026-10-05 10:13:00 | Member A opens /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A | "This payment session has expired. Nothing was charged." and a "Back to your booking" link; no card form (PMT-R07) |

### PMT-R06 Expire a session on request

| Field | Value |
|---|---|
| Rule | POST /payment-sessions/{id}/expire makes an open session expired and returns its final state with 200. A complete session stays complete and paid and is returned as paid. An expired session is returned unchanged. The expire and any payment attempt lock the same session row, so exactly one of them wins. An unknown id gets 404. |
| Policy status | Decided (D18) |
| Decision source | Project team (D12, D18) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 cancel hard-deletes the booking row, paid or not; there is nothing to expire. |
| Terms | PMT-T02, PMT-T03, PMT-T04 |
| Candidate responsibility and dependencies | Payment. Purchase calls it first when a held booking is cancelled (D18): unpaid means Purchase cancels with no refund; paid means Purchase confirms, then cancels under the refund policy. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contract "expire" operation (M2); cancel sequence diagrams; e2e "held cancel racing with payment" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Standard session open, clock 10:05 | POST /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A/expire | 200 status "expired", payment_status "unpaid" |
| 2 | counterexample | form | Session expired on request at 10:05 | Member A presses Pay with 4242424242424242 at 10:06 | 409 with the expired page "This payment session has expired. Nothing was charged." and a "Back to your booking" link to cancel_url; no attempt stored; no charge |
| 3 | counterexample | JSON | Member A paid at 10:04 | Expire at 10:05 | 200 status "complete", payment_status "paid"; it stays paid |
| 4 | boundary | JSON | Session already expired | Expire again | 200 status "expired"; nothing changes |
| 5 | boundary | internal | Standard session open | A Pay with 4242424242424242 and an expire arrive at the same instant | Both lock the session row (SELECT ... FOR UPDATE): either the attempt commits first and expire returns paid, or the expire commits first and the attempt is refused with no charge. Never expired and charged |
| 6 | counterexample | JSON | No such session | POST /payment-sessions/ps_doesnotexist/expire | 404 |

### PMT-R07 The hosted page shows the session

| Field | Value |
|---|---|
| Rule | GET /pay/{id} needs no login or token. For an open session it shows the amount as "THB 450.00", the booking reference, the description, a countdown to expires_at ("Pay by 10:13"), a test-mode banner listing the test cards, a card form (number, MM/YY, CVC), "Pay" and "Back". The server renders "Pay by 10:13" with a data-seconds-left attribute, the whole seconds from clock.now() to expires_at at render time, so the test clock drives it and the browser clock is never read; a few lines of inline script count it down each second, update "N min left" (N is the whole minutes left rounded up; under 60 s "less than 1 min left") and, at zero, disable Pay and show "Time to pay has run out"; without script the static text stays, and the server check (PMT-R11) decides. Back is a link to cancel_url and changes nothing. A complete session shows "Paid" and a link to success_url?session_id={id}. An expired session shows "This payment session has expired. Nothing was charged.", a "Back to your booking" link to cancel_url and no form. An unknown id gets a 404 page. |
| Policy status | Decided (D12) |
| Decision source | Project team (D1, D2, D12) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, templates/confirmation.html:12-19 card form on the booking page (the base of this page); app.py:395 the money filter shows dollars. |
| Terms | PMT-T07, PMT-T02, PMT-T05, PMT-T06, PMT-T10 |
| Candidate responsibility and dependencies | Payment renders the page. Purchase redirects the browser to the session url (PMT-R02) and supplies success_url and cancel_url. |
| Open question | PMT-Q05 (anyone with the link may pay). |
| Clarification owner | Project team |
| Next use | UX flow and screen list (M2); Payment page tests (M5); e2e happy path (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session, clock 10:01 | Member A's browser opens /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A | "THB 450.00", "Booking BK-7KQ2M9", "Meeting Room A, 2026-10-07 09:00-10:30", "Pay by 10:13 (12 min left)", the test-mode banner with the 6 test cards, the card form, Pay and Back |
| 2 | ordinary | form | Same | Member A presses Back | The browser goes to cancel_url on Purchase; the session stays open and the same url works until 10:13 |
| 3 | boundary | form | Clock 10:13:00, unpaid | Open the page | "This payment session has expired. Nothing was charged." and a "Back to your booking" link to cancel_url; no card form |
| 4 | boundary | form | Paid at 10:04 | Open the page at 10:06 | "Paid" and a "Return to booking" link to success_url?session_id=ps_Q7mZ3xK9vT2bN8rL4wYc1A; no card form |
| 5 | counterexample | form | No such session | Open /pay/ps_doesnotexist | 404 page; no booking data shown |
| 6 | counterexample | form | Standard session open | Open /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A?error=Card+refused | No message is shown; the query value is ignored and never rendered |
| 7 | boundary | form | Test clock 10:12:50 on all three services, standard session open | Open /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A in a browser and wait | manual: the page renders data-seconds-left="10"; within about 10 s "Time to pay has run out" shows and Pay is disabled, whatever the browser's own date; the server clock stays at 10:12:50 (a fixed instant), so then set the test clock to 2026-10-05T10:13:00+07:00 on all three services: a crafted POST now gets 409 (PMT-R11) |

### PMT-R08 Card details must look valid

| Field | Value |
|---|---|
| Rule | Before any attempt, the hosted page checks the card fields in this order, after removing spaces from the number: number 13-19 digits; CVC 3 or 4 digits; expiry MM/YY with a month from 01 to 12; expiry month not before the current Bangkok month of clock.now(). The first failure is flashed on the page as plain text, never a code identifier (validate_card is kept and its codes are mapped to this text): ("Card number must be 13 to 19 digits", "CVC must be 3 or 4 digits", "Expiry must be MM/YY", "The expiry date has passed"); no attempt is stored and the session stays open. There is no Luhn or card network check (mock). "The expiry date has passed" (fix the date) differs on purpose from the expired_card decline "Your card has expired." (use another card, PMT-T09). |
| Policy status | Decided (D27; ADR-0018 (mock checkout and test cards)) |
| Decision source | Project team (ADR-0018 (mock checkout and test cards); D27 for the clock); keeps the observed check that a class contributor recorded (class rules PR #1 at 0326c8c, merged in main 58a1477) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:232-253 validate_card and its regexes (kept); app.py:250 reads datetime.now(timezone.utc) (to be replaced by clock.now()); app.py:953-955 a card is required even for amount 0. |
| Terms | PMT-T08, PMT-T07, PMT-T11 |
| Candidate responsibility and dependencies | Payment, reusing validate_card. Depends on PMT-R02 (no session below THB 10.00) and on Purchase's coverage rules PUR-R19 and PUR-R20 (free and plan bookings skip Payment, D10). |
| Open question | PMT-Q01 (what a real payment should check). |
| Clarification owner | Project team for PMT-Q01 and the rule as stated; course instructor for the scope of PMT-Q01 |
| Next use | Payment unit tests for validate_card (M5); UX error states of the hosted page (M2). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session, clock 2026-10-05 10:02 | Pay with 4242424242424242, expiry 12/28, CVC 123 | The check passes; an attempt is stored with its outcome (PMT-R09) |
| 2 | boundary | form | Clock 2026-10-05 10:02 | Pay with 4242424242424242, expiry 10/26 | Passes: October 2026 is the current month |
| 3 | boundary | form | Clock 2026-10-05 10:02 | Pay with 4242424242424242, expiry 09/26 | Flash "The expiry date has passed"; back on /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A; no attempt stored; session open |
| 4 | counterexample | form | Standard session open | Pay with 424242424242 (12 digits) | Flash "Card number must be 13 to 19 digits"; no attempt stored |
| 5 | boundary | form | Standard session open | Pay with "4242 4242 4242 4242", 12/28, 123 | Spaces are removed; the check passes |
| 6 | counterexample | internal | A free Community Table booking (THB 0.00): the class case where a card was still required for amount 0 | Member A books it | No session and no card form: Purchase confirms at once (D10), and Payment refuses amount 0 (PMT-R02) |
| 7 | boundary | form | Standard session open | Pay with 4000000000002 (13 digits), then 42424242424242424242 (20 digits) | The 13-digit number passes the check (then declines generic_decline, PMT-R09); the 20-digit one gets the flash "Card number must be 13 to 19 digits" |
| 8 | boundary | form | Standard session open | Pay with 4242424242424242, 12/28 and CVC 12345, then with CVC 1234 | 12345 gets the flash "CVC must be 3 or 4 digits" and stores nothing; then 1234 passes the check |
| 9 | counterexample | form | Standard session open | Pay with 4242424242424242, expiry 13/28, then 00/28 | Both get the flash "Expiry must be MM/YY"; no attempt stored |

### PMT-R09 Test cards decide the attempt outcome

| Field | Value |
|---|---|
| Rule | An attempt's outcome depends only on the card number: 4242424242424242 succeeded; 4000000000000002 declined(generic_decline); 4000000000009995 declined(insufficient_funds); 4000000000000069 declined(expired_card); 4000000000000119 declined(processing_error); 4000000000005126 succeeded (its first refund fails, PMT-R16). Any future expiry and any CVC. Every other number that passes PMT-R08 declines with generic_decline. No real card is charged, and no request field can force an outcome. |
| Policy status | Decided (ADR-0018 (mock checkout and test cards)) |
| Decision source | Project team (ADR-0018 (mock checkout and test cards)); D19 relies on the refund-failure card |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:957-958 "force_failure": true in a JSON body gives 402, a test hook open to any caller. |
| Terms | PMT-T10, PMT-T08, PMT-T09 |
| Candidate responsibility and dependencies | Payment. The e2e suite (M6) uses these cards; no other service depends on them. |
| Open question | PMT-Q01 (what a real payment should check). |
| Clarification owner | Project team for PMT-Q01 and the rule as stated; course instructor for the scope of PMT-Q01 |
| Next use | Test-mode banner (PMT-R07); e2e decline-then-retry and refund-failure scenarios (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session, clock 10:02 | Pay with 4242424242424242, 12/28, 123 | Attempt pa_… succeeded; session complete and paid |
| 2 | ordinary | form | Standard session open | Pay with 4000000000009995 | Attempt declined(insufficient_funds); flash "Your card has insufficient funds." |
| 3 | boundary | form | Standard session open | Pay with 4000000000000069, expiry 12/28 | Attempt declined(expired_card): a test decline, though the date is in the future |
| 4 | ordinary | form | Standard session open | Pay with 4000000000000119 | Attempt declined(processing_error); flash "An error occurred while processing your card. Try again."; session open |
| 5 | ordinary | form | Member C's session for BK-3HT8WD (100000) | Pay with 4000000000005126 | Attempt succeeded; its first refund will fail (PMT-R16) |
| 6 | counterexample | form | Standard session open | Pay with 4111111111111111 (valid-looking, not a test card) | Attempt declined(generic_decline); flash "Your card was declined." |

### PMT-R10 A decline keeps the session open; a success completes it

| Field | Value |
|---|---|
| Rule | A declined attempt is stored; the page redirects to itself (303, so a reload never re-posts the card fields) and shows the flashed reason inside an element data-decline-code="<code>"; the session stays open and unpaid for another try until expires_at. A succeeded attempt makes the session complete and paid and redirects the browser (303) to success_url?session_id={id}. Neither outcome changes a booking: Purchase reads the session and decides (D14). |
| Policy status | Decided (D12) |
| Decision source | Project team (D12, D14, D28) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:844-849 a failed pay redirects with the error text in ?error=, which the page reflects. |
| Terms | PMT-T08, PMT-T09, PMT-T03, PMT-T04, PMT-T07 |
| Candidate responsibility and dependencies | Payment. Purchase's success_url page calls GET /payment-sessions/{id} and confirms (D14); if the redirect is lost, reconciliation does the same (D13). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Sequence diagrams "book and pay" and "decline and retry" (M2); e2e decline then retry, and "after a decline the Member is still logged in on Purchase" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session, clock 10:02 | Pay with 4000000000000002 | 303 to /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A; the page then shows the flash "Your card was declined." inside data-decline-code="generic_decline"; attempt declined(generic_decline) stored; session open and unpaid |
| 2 | ordinary | form | After row 1, clock 10:03 | Pay with 4242424242424242 | Attempt succeeded; session complete and paid; 303 to success_url?session_id=ps_Q7mZ3xK9vT2bN8rL4wYc1A |
| 3 | boundary | form | Three declines between 10:02 and 10:12 | Pay with 4242424242424242 at 10:12:30 | Succeeds: there is no retry limit before expires_at |
| 4 | counterexample | JSON | After a decline at 10:02 | Purchase GETs the session | status "open", payment_status "unpaid": a decline is not a final outcome; the booking stays held in Purchase |
| 5 | counterexample | form | After a decline | Look at the browser address | /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A with no ?error= and no card data; the reason is a flashed message only (D28) |

### PMT-R11 No attempt at or after expires_at

| Field | Value |
|---|---|
| Rule | Payment refuses every payment attempt when clock.now() is at or after the session's expires_at, even if the page was loaded earlier: no attempt is stored, nothing is charged, and the POST answers 409 with the same expired page as the GET (PMT-R07): "This payment session has expired. Nothing was charged." and a "Back to your booking" link to cancel_url, so the Member is never left at a dead end. So a session's outcome is final before the booking's hold ends (expires_at is 2 minutes before hold_expires_at). |
| Policy status | Decided (D12) |
| Decision source | Project team (D12, D13, D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:932-968 mark_booking_paid has no time limit. |
| Terms | PMT-T06, PMT-T08, PMT-T03, PMT-T07 |
| Candidate responsibility and dependencies | Payment checks the time inside the attempt transaction (PMT-R12). Purchase sets expires_at (D12) and expires the booking once its hold lapses (D13). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | ADR-0004 (Purchase-only callers), no webhooks (why no webhook is needed); e2e lost redirect and hold expiry (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | boundary | form | Standard session (expires_at 10:13), unpaid | Pay with 4242424242424242 at 10:12:59 | Accepted; session complete and paid |
| 2 | boundary | form | Same, unpaid | Pay with 4242424242424242 at 10:13:00 | 409, the page "This payment session has expired. Nothing was charged." with "Back to your booking" linking cancel_url; no attempt; no charge |
| 3 | counterexample | form | Page loaded at 10:10 with the countdown running | Member A submits the card at 10:13:05 | Refused as in row 2; loading the page earlier does not extend the time |
| 4 | boundary | JSON | Same, unpaid | Purchase GETs the session at 10:14 (the hold ends 10:15) | status "expired", payment_status "unpaid": final, so no late payment can arrive after Purchase expires the booking |
| 5 | counterexample | internal | Test clock set with POST /_test/clock to "2026-10-05T10:13:00+07:00" (TEST_CLOCK_ENABLED, D27) | An attempt arrives | Refused: Payment reads time only through clock.now(), never the database now() |
| 6 | ordinary | form | Standard session (expires_at 10:13), unpaid | Pay with 4242424242424242 at 10:04 | Accepted; session complete and paid |

### PMT-R12 A session is charged at most once

| Field | Value |
|---|---|
| Rule | Each attempt runs in one transaction: SELECT the session FOR UPDATE, check it is open and before expires_at, decide the outcome, store the attempt with attempted_at = clock.now() and, on success, set complete, paid and paid_at = clock.now(). A session therefore has at most one succeeded attempt. A Pay on a complete session stores no attempt, charges nothing and sends the browser to success_url?session_id={id}. |
| Policy status | Decided (D28) |
| Decision source | Project team (D28) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:940-965 SELECT then UPDATE on an autocommit connection with no FOR UPDATE, so two pays can both pass the check. |
| Terms | PMT-T08, PMT-T02, PMT-T04, PMT-T13 |
| Candidate responsibility and dependencies | Payment (explicit transaction, D28). With one session per booking reference (PMT-R03), Purchase gets at most one charge per booking. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Payment concurrency test (M5); e2e "double submit: no double charge" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | Standard session open | One Pay with 4242424242424242 | One transaction: lock, attempt pa_… succeeded, session complete and paid, commit |
| 2 | boundary | form | Standard session open | Member A double-clicks Pay at 10:03 (two POSTs with 4242424242424242) | The first commits a succeeded attempt; the second waits on the lock, sees complete, stores nothing and redirects to success_url?session_id=ps_Q7mZ3xK9vT2bN8rL4wYc1A; on /operator exactly one row with data-booking-reference="BK-7KQ2M9" and data-attempt-result="succeeded"; collected rises by 45000, not 90000 |
| 3 | counterexample | form | Session paid at 10:03 | Member A pays again in a second tab with 4000000000005126 at 10:05 | No attempt stored; no charge; redirect to success_url |
| 4 | boundary | internal | A decline at 10:02, then a success at 10:03 | Count the attempts | Two attempts, one declined and one succeeded; one charge |

### PMT-R13 Store only the card brand and last4

| Field | Value |
|---|---|
| Rule | For each attempt Payment stores only the card brand and the last 4 digits (e.g. visa, 4242). It never stores, logs, flashes or puts in a URL the full number, the expiry or the CVC. After a form error the card fields come back empty. Access logs record the path only (query-string scrubbing kept from the seed). |
| Policy status | Decided (D28; ADR-0020 (card data handling)) |
| Decision source | Project team (ADR-0020 (card data handling)); D28 for flash() instead of ?error= |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:964 stores card_number[-4:] only; gunicorn.conf.py:1-5 logs the path without the query string. |
| Terms | PMT-T11, PMT-T08, PMT-T09 |
| Candidate responsibility and dependencies | Payment. The operator page (PMT-R17) shows only brand and last4; Purchase never receives card data. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Security lens review (M3); a Payment test that searches the database and the log output for the full number (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | Member A pays with 4242424242424242, 12/28, 123 | Read the attempt row | brand "visa", last4 "4242", outcome succeeded; no column holds the number, expiry or CVC |
| 2 | boundary | internal | Member A pays with 4000000000000002 | Read the attempt row | brand "visa", last4 "0002", decline code generic_decline; nothing more about the card |
| 3 | counterexample | form | Member A submits CVC "12" | The page comes back | Flash "CVC must be 3 or 4 digits"; the card fields are empty; the number is not in the URL, the flash cookie or the log |
| 4 | counterexample | internal | Any attempt | Read the access log line for POST /pay/ps_Q7mZ3xK9vT2bN8rL4wYc1A | Method, path and status only; no form body and no query string |
| 5 | ordinary | form | Member A paid with 4242424242424242 | Operator opens the operator page | The attempt shows "visa ending 4242"; never more digits |
| 6 | boundary | internal | Member A pays with 4000000000002 (13 digits, the shortest number PMT-R08 accepts) | Read the attempt row | brand "visa", last4 "0002", decline code generic_decline; the other 9 digits are stored nowhere |

### PMT-R14 One refund per session and attempt number

| Field | Value |
|---|---|
| Rule | POST /refunds takes payment_session_id, booking_reference, amount_satang (an integer, at least 1), reason (non-empty text from Purchase) and attempt (an integer, at least 1). (payment_session_id, attempt) is unique. A new request gets 201 with the refund (id re_…, status succeeded or failed). A repeat with the same key and amount returns the stored refund with 200 and does nothing else, even if it failed. The repeat-key check, the balance check (PMT-R15) and the insert run in one transaction after the session row is locked (FOR UPDATE), so two identical requests that arrive together get one 201 and one 200, never a 409. The refund's created_at is written from clock.now() in that transaction. The same key with a different amount gets 409. An unknown session gets 404; a booking_reference that does not match the session gets 409; bad fields get 400, and so does an integer outside its column range (amount_satang BIGINT, attempt INTEGER), never a 500. |
| Policy status | Decided (D19) |
| Decision source | Project team (D19) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 cancel deletes the booking row and records no refund. |
| Terms | PMT-T12, PMT-T02, PUR-T18 |
| Candidate responsibility and dependencies | Payment enforces the key. Purchase picks attempt: 1 for the first try, attempt+1 only when the operator retries after a stored failure (D19), and resends the same attempt after a timeout. It stores each outcome on the booking. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contract refund operation and "repeat" example (M2); e2e refund failure card (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Standard session paid (45000); Member A cancels at 2026-10-05 11:00, 46 h before start (100%, D18) | POST /refunds {"payment_session_id": "ps_Q7mZ3xK9vT2bN8rL4wYc1A", "booking_reference": "BK-7KQ2M9", "amount_satang": 45000, "reason": "member_cancel", "attempt": 1} | 201 {"id": "re_…", "status": "succeeded", "amount_satang": 45000, "attempt": 1} |
| 2 | boundary | JSON | After row 1; Purchase timed out before it read the answer | Same body again | 200 with the same re_ id and status "succeeded"; no second refund |
| 3 | counterexample | JSON | After row 1 | Same session, attempt 1, amount_satang 20000 | 409 {"error": "refund attempt 1 already exists with a different amount"}; nothing new stored |
| 4 | counterexample | JSON | Standard session paid | booking_reference "BK-3HT8WD" with ps_Q7mZ3xK9vT2bN8rL4wYc1A | 409 {"error": "booking_reference does not match the session"}; nothing stored |
| 5 | boundary | JSON | Standard session paid | attempt 0, or amount_satang 0 | 400; nothing stored |
| 6 | counterexample | JSON | No such session | payment_session_id "ps_doesnotexist" | 404 |
| 7 | boundary | JSON | Standard session paid | attempt 2147483648, or amount_satang 9223372036854775808 | 400 naming the field; nothing stored; never a 500 |
| 8 | boundary | JSON | Member C's session for BK-3HT8WD paid (100000); refund attempt 1 failed | Two identical attempt 2 requests arrive together (the Operator's double click, or the Operator's Retry racing Member C's page open) | Both lock the session row first: one gets 201 succeeded; the other waits, then gets 200 with the same re_ id; never 409 |

### PMT-R15 Refunds never exceed the amount collected

| Field | Value |
|---|---|
| Rule | A refund is accepted only if refunded total + amount_satang is at most the amount collected on its session; otherwise 409 and nothing is stored. Amount collected is amount_satang of a paid session, else 0; refunded total sums succeeded refunds only. The check and the insert run in one transaction with the session row locked (FOR UPDATE), so parallel refunds cannot overshoot. Payment accepts any amount within the balance; Purchase sends only full refunds (D18). |
| Policy status | Decided (D19) |
| Decision source | Project team (D18, D19, D28) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:298-301 revenue sums surviving booking rows, so a cancel erases it; no refund exists. |
| Terms | PMT-T12, PMT-T13, PMT-T14 |
| Candidate responsibility and dependencies | Payment. Purchase computes the refund amount (D18) and the full refunds for amount_mismatch and slot_unavailable (D14). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | e2e "the total refunded never exceeds the amount collected" (M6); Payment concurrency test (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Standard session paid: collected 45000, refunded 0 | Refund 45000, attempt 1 | 201 "succeeded"; refunded total 45000 |
| 2 | boundary | JSON | Collected 45000; a succeeded refund of 20000 | Refund 25000, attempt 2 | 201 "succeeded"; refunded total 45000, equal to collected |
| 3 | boundary | JSON | Collected 45000, refunded 45000 | Refund 1 satang, attempt 2 | 409 {"error": "refund exceeds amount collected"}; nothing stored |
| 4 | counterexample | JSON | Member C's session for BK-3HT8WD paid with 4000000000005126 (100000); refund attempt 1 failed | Refund 100000, attempt 2 | Allowed: a failed refund adds nothing to the refunded total; 201 "succeeded" |
| 5 | counterexample | JSON | Standard session expired unpaid (collected 0) | Refund 45000, attempt 1 | 409; nothing was collected |
| 6 | boundary | internal | Collected 45000, refunded 0 | Refunds of 45000 with attempts 1 and 2 arrive together | The session lock serialises them: one succeeds, the other gets 409 |

### PMT-R16 A refund outcome is final at once

| Field | Value |
|---|---|
| Rule | POST /refunds answers with the final outcome, succeeded or failed, in the same response. There is no pending state, and a stored outcome never changes. For a session paid with test card 4000000000005126 the first refund stored for that session fails and later ones succeed; for every other paid session refunds succeed. Payment recognises that card from the stored last4 5126 of the session's succeeded attempt (the only succeeding test card ending in 5126), never from a stored card number. Refunds never change the session's status or payment_status: a refunded session still reads complete and paid. |
| Policy status | Decided (D19) |
| Decision source | Project team (D19); ADR-0018 (mock checkout and test cards) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 cancel is a DELETE; no refund exists. |
| Terms | PMT-T12, PMT-T10, PMT-T15, PMT-T04 |
| Candidate responsibility and dependencies | Payment. Purchase stores the outcome on the booking. A stored failed refund shows "Refund failed. The operator will follow up.", and only the operator starts attempt+1 (D19, PUR-R33). "Refund pending" means only that Payment gave no answer, or that the refund waits for its revoke (PUR-T30). |
| Open question | PMT-Q02 (how a failed refund gets closed). |
| Clarification owner | Project team |
| Next use | e2e refund failure card (M6); the follow-up label on the operator page (PMT-R17). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Standard session paid with 4242424242424242 | Refund 45000, attempt 1 | 201 status "succeeded" in the same response |
| 2 | boundary | JSON | Member C's session for BK-3HT8WD paid with 4000000000005126 (100000) | Refund 100000, attempt 1 | 201 status "failed"; refunded total stays 0; listed as needs manual follow-up |
| 3 | ordinary | JSON | After row 2, the Operator presses Retry in Purchase | Refund 100000, attempt 2 | 201 status "succeeded"; refunded total 100000 |
| 4 | counterexample | JSON | After row 2 | Repeat attempt 1 with the same body | 200 status "failed", the stored result (PMT-R14); repeating does not retry |
| 5 | counterexample | JSON | After row 1 | GET /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A | status "complete", payment_status "paid": refunds are separate records |

### PMT-R17 Operator page shows money totals and failed refunds

| Field | Value |
|---|---|
| Rule | GET /operator needs HTTP Basic with the password OPERATOR_PASSWORD, compared in constant time; any user name is accepted; otherwise 401 with a Basic challenge. Payment refuses to start when OPERATOR_PASSWORD is unset, empty or shorter than 12 characters. The page lists sessions (booking_reference, amount, status, paid_at), attempts (booking_reference, card brand and last4 only, result, decline code, attempted_at) and refunds (booking_reference, attempt, amount, reason, status, created_at), each list in a fixed order: sessions newest paid_at first, then unpaid sessions newest created first; attempts newest attempted_at first; refunds newest created_at first; paid_at, attempted_at and created_at are written from clock.now() in the pay or refund transaction, never by a database default (D27), and shows all-time totals: collected (sum over paid sessions), refunded (sum of succeeded refunds), net = collected minus refunded, and "estimated platform commission (20% of net)", rounded half up to the satang. Each failed refund is listed as "needs manual follow-up", with "Retry it from Purchase: All bookings", until a later refund attempt for the same session succeeds. The times let the Operator sum a week by hand; v1 shows no weekly total (PMT-Q03). The page carries test markers: data-session-id and data-booking-reference on every session, attempt and refund row; data-attempt-result on each attempt row, plus data-decline-code on a declined one; data-refund-attempt and data-refund-status on each refund row; data-follow-up="<booking_reference>" only while that failed refund needs follow-up, and data-collected-satang, data-refunded-satang, data-net-satang and data-commission-satang on the totals. |
| Policy status | Decided (D25; ADR-0019 (service authentication)) |
| Decision source | Project team (D24, D25; ADR-0019 (service authentication)) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:1027-1050 /metrics and /dashboard show revenue to anyone without a login. |
| Terms | PMT-T18, PMT-T13, PMT-T14, PMT-T15, PMT-T16 |
| Candidate responsibility and dependencies | Payment. Purchase's dashboard shows booking metrics only (D24); plan and free bookings never appear here because they never reach Payment. |
| Open question | PMT-Q02 (closing a failed refund); PMT-Q03 (period of the totals); PMT-Q04 (host payouts). |
| Clarification owner | Course instructor for the scope of PMT-Q04, with the project team; Project team for PMT-Q02, PMT-Q03 and the rule as stated |
| Next use | BUSINESS_MODEL.md commission figures (M2); e2e refund failure scenario checks the follow-up label (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Paid sessions: BK-7KQ2M9 (45000, refunded 45000) and BK-3HT8WD (100000, refund attempt 1 failed) | Operator opens /operator with the right password | Collected THB 1,450.00; refunded THB 450.00; net THB 1,000.00; estimated platform commission (20% of net) THB 200.00; the BK-3HT8WD refund is marked "needs manual follow-up" (data-follow-up="BK-3HT8WD"); data-collected-satang="145000", data-refunded-satang="45000" |
| 2 | boundary | form | After row 1, refund attempt 2 for BK-3HT8WD succeeds | Operator reloads | Refunded THB 1,450.00; net THB 0.00; commission THB 0.00; no follow-up label and no data-follow-up element; among the rows with data-booking-reference="BK-3HT8WD", the refund row with data-refund-attempt="1" has data-refund-status="failed" and the row with "2" has "succeeded" |
| 3 | boundary | form | Only one paid session: Focus Pod 1, 1000 | Operator opens /operator | Collected THB 10.00; net THB 10.00; commission THB 2.00 |
| 4 | counterexample | form | Any data | Open /operator with no credentials or a wrong password | 401 with "WWW-Authenticate: Basic"; no data |
| 5 | counterexample | form | Member B's plan booking and a free Community Table booking exist in Purchase | Operator opens /operator | Neither appears or adds to any total: they never reach Payment (D10) |
| 6 | boundary | form | One paid session collected 1000; a direct API refund of 3 succeeded | Operator opens /operator | Net THB 9.97; commission 20% of 997 = 199.4 satang, rounded half up to 199: "THB 1.99" |
| 7 | counterexample | internal | OPERATOR_PASSWORD unset or empty | Payment starts | Non-zero exit with the message "OPERATOR_PASSWORD is required"; an empty Basic password never matches |
| 8 | counterexample | form | Any data | Open /operator with a Basic password holding a non-ASCII character, such as "passwörd" | 401 with "WWW-Authenticate: Basic", never a 500: the compare runs on UTF-8 bytes |
| 9 | boundary | internal | OPERATOR_PASSWORD is 11 characters, then 12 | Payment starts | 11: non-zero exit with the message "OPERATOR_PASSWORD must be at least 12 characters"; 12: it starts |

### PMT-R18 Payment calls no other service

| Field | Value |
|---|---|
| Rule | Payment makes no outbound HTTP call and reads no other service's database: no webhook to Purchase, no call to Access. It reports outcomes when Purchase asks (GET /payment-sessions/{id} and the POST responses) and sends the Member's browser back by redirect. Payment never sets or reads a booking status, a coverage or a grant. |
| Policy status | Decided (D13) |
| Decision source | Project team (D12, D13); ADR-0004 (Purchase-only callers), no webhooks; Course [extraction site]: "Purchase interprets the result" |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:960-965 payment writes paid straight onto the booking row in the one shared database. |
| Terms | PMT-T01, PMT-T02, PMT-T04 |
| Candidate responsibility and dependencies | Payment is a provider only. Purchase polls and reconciles (D13), confirms (D14) and issues grants (D20). |
| Open question | PMT-Q01 (a real provider would add inbound webhooks to Payment only). |
| Clarification owner | Project team for PMT-Q01 and the rule as stated; course instructor for the scope of PMT-Q01 |
| Next use | Context map and container diagrams (M2); Payment env and code have no other service's URL, and a Payment test checks that no outbound HTTP call is made (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session open | Member A pays with 4242424242424242 at 10:04 | The browser is redirected to success_url; Payment itself sends nothing to Purchase or Access |
| 2 | ordinary | JSON | After row 1 | Purchase GETs /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A | 200 complete and paid; Purchase confirms (D14) and calls Access (D20) |
| 3 | boundary | internal | Member A closes the tab right after paying at 10:04 (lost redirect) | Nothing reaches Purchase | The session stays complete and paid; the next Purchase read or sweep reconciles the booking to confirmed, not expired (D13) |
| 4 | counterexample | internal | Payment's configuration | Look for another service's URL or database | None: the env is DATABASE_URL, SECRET_KEY, APP_REVISION, PUBLIC_URL, PAYMENT_API_TOKEN, OPERATOR_PASSWORD, and TEST_CLOCK_ENABLED for e2e only |
| 5 | counterexample | JSON | Any session | Any Payment API response | No booking status, coverage or grant field; only session, attempt and refund data |

### PMT-R19 Cookies and SECRET_KEY

| Field | Value |
|---|---|
| Rule | Refuse to start when SECRET_KEY is unset, empty, shorter than 32 characters or the seed's public default "dev-secret-key-not-for-production" (ADR-0019). Set the payment_session cookie HttpOnly and SameSite=Lax, plus Secure when PUBLIC_URL starts with https. It carries only flashed messages for the hosted page, never card data. |
| Policy status | Decided (D15) |
| Decision source | Project team (D15). ADR-0009 (SameSite as the CSRF mitigation). |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:20 falls back to a public default SECRET_KEY. |
| Terms | PMT-T07, PMT-T11 |
| Candidate responsibility and dependencies | Payment. Purchase and Access follow the same rule for their own cookies (PUR-R03, AXS-R18). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Payment startup and cookie tests (M5); README env list (M7). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Standard session open | Member A pays with 4000000000000002 | The decline flash comes back through payment_session, HttpOnly and SameSite=Lax; the cookie holds no card data |
| 2 | boundary | internal | PUBLIC_URL starts with https | The hosted page sets payment_session | The cookie also carries Secure; with http it does not |
| 3 | counterexample | internal | SECRET_KEY unset or empty, for example copied unchanged from .env.example | Payment starts | Non-zero exit with the message "SECRET_KEY is required"; no default key is used |
| 4 | counterexample | internal | SECRET_KEY is "x" | Payment starts | Non-zero exit with the message "SECRET_KEY must be at least 32 characters" |
| 5 | counterexample | internal | SECRET_KEY is "dev-secret-key-not-for-production" (33 characters) | Payment starts | Non-zero exit with the message "SECRET_KEY is the public seed default" |

### PMT-R20 The test clock is off unless TEST_CLOCK_ENABLED=true

| Field | Value |
|---|---|
| Rule | Read time only through clock.now() (session expiry, attempts, card expiry); never use SQL now() or CURRENT_TIMESTAMP in business logic. Answer POST /_test/clock with 404 unless TEST_CLOCK_ENABLED is exactly "true"; when it is, store {"now": iso-or-null} in the one-row test_clock table, where null clears the override; a "now" that is not ISO 8601 with an offset gets 400 and stores nothing (D2). With the flag off, clock.now() returns real time and never reads test_clock, even if a row still holds an override. The override is a fixed instant: clock.now() returns exactly the stored value on every read until the next POST /_test/clock; it never advances. With the flag on, clock.now() reads the test_clock row on every call (no per-process cache), so both gunicorn workers see a new instant from the next request. Never set the flag in the Dockerfile, the service compose.yaml or .env.example. No other test hook exists. |
| Policy status | Decided (D27) |
| Decision source | Project team (D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:250 validate_card reads datetime.now(timezone.utc); app.py:957-958 a force_failure flag is a test hook open to any caller (seed flaw A6). |
| Terms | PMT-T03, PMT-T06 |
| Candidate responsibility and dependencies | Payment. Purchase and Access have the same guard (PUR-R38, AXS-R19). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Payment clock and guard tests (M5); e2e setup (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | TEST_CLOCK_ENABLED=true; standard session open | POST /_test/clock {"now": "2026-10-05T10:13:00+07:00"} | 200; GET /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A reports status "expired" |
| 2 | boundary | JSON | TEST_CLOCK_ENABLED=true; an override is set | POST /_test/clock {"now": null} | 200; the override is cleared |
| 3 | counterexample | JSON | TEST_CLOCK_ENABLED unset, "false" or "1" | POST /_test/clock {"now": "2026-10-05T10:13:00+07:00"} | 404; nothing stored; clock.now() unchanged |
| 4 | counterexample | form | Standard session open | Pay with 4242424242424242 and an added force_failure field | The field is ignored: the attempt succeeds, as the test card says (PMT-R09) |
| 5 | counterexample | internal | The Payment Dockerfile, compose.yaml and .env.example | Look for TEST_CLOCK_ENABLED | Set in none of them; only the e2e compose override sets it |
| 6 | counterexample | JSON | TEST_CLOCK_ENABLED=true | POST /_test/clock {"now": "2026-10-05T10:13:00"} (no offset) | 400; nothing stored |
| 7 | counterexample | internal | An override 2026-10-05T10:13:00+07:00 is stored; Payment restarts with TEST_CLOCK_ENABLED unset | Read the standard session | Real time decides its status: clock.now() never reads test_clock while the flag is off |
| 8 | boundary | JSON | TEST_CLOCK_ENABLED=true; override 2026-10-05T10:12:50+07:00; standard session open | GET /payment-sessions/ps_Q7mZ3xK9vT2bN8rL4wYc1A twice, 2 s apart | open both times: the override never advances, so the session expires only when the clock is set to 10:13:00 or later |
| 9 | boundary | internal | TEST_CLOCK_ENABLED=true; two Payment app instances with their own database connections (like the two workers) share one database | Instance 1 handles POST /_test/clock {"now": "2026-10-05T10:15:00+07:00"}; then instance 2 reads clock.now() | 2026-10-05T10:15:00+07:00: clock.now() reads the row on every call, never a per-process copy (a service test) |

## Access

### AXS-R01 Issue one grant per booking reference

| Field | Value |
|---|---|
| Rule | When Purchase calls POST /grants for a booking reference that has no grant, Access stores one grant in state issued with a new grant_id (gr_), ticket code and ticket token, and answers 201 with grant_id, ticket_code, ticket_url and status. Every later POST /grants for that reference answers 200 with the stored grant, unchanged, even if the body differs. |
| Policy status | Decided (D20) |
| Decision source | Project team (D20, D22); Course [extraction site]: Access "Owns grants and issuance"; "Reuse or new attempt? Agree identity and behaviour; do not assume." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:970-985 issue_access_code keeps no grant record; every unlock returns a fresh value. |
| Terms | AXS-T02, AXS-T03, AXS-T04, AXS-T08, AXS-T10, PUR-T18 |
| Candidate responsibility and dependencies | Access decides and enforces it with UNIQUE(booking_reference) and an insert that returns the existing row on conflict. Purchase calls only for a confirmed booking with no cancel in progress (D20); Access cannot check that, because it never calls Purchase. |
| Open question | AXS-Q05 (changing a grant's room or window) |
| Clarification owner | Project team, with the course instructor for cancellation scope, for AXS-Q05 and the rule as stated |
| Next use | Contract (M2) purchase→access: POST /grants success and repeat examples; e2e "repeat grant" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A's booking BK-7KQ2M9 is confirmed at 2026-10-05 10:05; no grant exists | Purchase POSTs /grants with BK-7KQ2M9, Member A's member_ref, space_id 1, space_name "Meeting Room A", valid_from 2026-10-07T09:00:00+07:00, valid_until 2026-10-07T10:30:00+07:00 | 201: grant_id gr_…, ticket_code H7K3-9QXA, ticket_url ending `/t/<ticket_token>`, status issued. One grant stored. |
| 2 | boundary | JSON | The grant for BK-7KQ2M9 exists with H7K3-9QXA | Purchase's first call timed out, so it POSTs the same body again | 200: the same grant_id, ticket_code H7K3-9QXA and ticket_url. Still one grant. |
| 3 | boundary | internal | No grant for BK-7KQ2M9 | Two identical POSTs arrive at the same instant on two workers | One grant stored; both answers carry the same grant_id and ticket code. |
| 4 | counterexample | JSON | The grant for BK-7KQ2M9 is issued for 09:00-10:30 | Purchase POSTs /grants for BK-7KQ2M9 with valid_from 2026-10-07T10:00:00+07:00 and valid_until 2026-10-07T11:30:00+07:00 | 200 with the stored grant unchanged: the window stays 09:00-10:30. A repeat never updates or re-issues (reschedule is unsupported, D18). |
| 5 | counterexample | JSON | Member B's plan booking BK-3MZ8QT is confirmed with no payment | Purchase POSTs /grants for BK-3MZ8QT | 201, the same as for a paid booking. Access receives no price, amount or coverage and does not ask for them. |

### AXS-R02 A revoked booking reference never gets a grant

| Field | Value |
|---|---|
| Rule | If Purchase revokes a booking reference that has no grant, Access stores a revoked tombstone for it. POST /grants for a reference whose grant or tombstone is revoked answers 200 with status revoked and issues nothing: no new grant, no new ticket code, no ticket token. |
| Policy status | Decided (D19, D20) |
| Decision source | Project team (D19, D20) |
| Implementation evidence | Not implemented yet (planned M5). |
| Terms | AXS-T02, AXS-T03, AXS-T06, AXS-T07, PUR-T18 |
| Candidate responsibility and dependencies | Access enforces it. It exists because a revoke can reach Access before an issue: the held-booking cancel that finds the session paid (D18: confirmed without a grant, then cancelled) and a late issuance retry racing a cancel (D19, D20). |
| Open question | AXS-Q05 (restoring a revoked grant) |
| Clarification owner | Project team, with the course instructor for cancellation scope, for AXS-Q05 and the rule as stated |
| Next use | Contract (M2) purchase→access: revoke-before-issue example; e2e "held cancel racing with payment" (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Member A cancels held booking BK-P4W6RC; Payment reports the session paid, so Purchase confirms it without a grant and cancels it (D18); no grant exists | Purchase POSTs /grants/BK-P4W6RC/revoke | 200 status revoked. A tombstone is stored with no ticket code and no ticket token. |
| 2 | ordinary | JSON | The tombstone for BK-P4W6RC exists | A late issuance retry POSTs /grants for BK-P4W6RC with a full body | 200: status revoked, ticket_code null, ticket_url null. Nothing is issued. |
| 3 | boundary | JSON | The grant for BK-7KQ2M9 (H7K3-9QXA) was revoked | Purchase POSTs /grants for BK-7KQ2M9 again | 200: the stored grant, status revoked, the old code. No new code. |
| 4 | boundary | JSON | The tombstone for BK-P4W6RC exists | An API caller holding ACCESS_API_TOKEN (contract test) GETs /grants/BK-P4W6RC | 200 status revoked, not 404. |
| 5 | counterexample | JSON | The tombstone for BK-P4W6RC exists | Purchase POSTs /grants for BK-3MZ8QT, a different booking | 201 issued as usual: a tombstone blocks only its own reference. |

### AXS-R03 A grant request carries a complete window with UTC offsets

| Field | Value |
|---|---|
| Rule | POST /grants needs booking_reference (BK- plus 6 symbols from the D22 alphabet), a non-empty member_ref, a positive integer space_id, a non-empty space_name, and valid_from and valid_until as ISO 8601 instants with a UTC offset, valid_until after valid_from. Otherwise Access answers 400 naming the field and stores nothing; a space_id outside the INTEGER range gets 400 too, never a 500. Access stores the window exactly as sent and does not check it against opening hours, blocks or buffers. |
| Policy status | Decided (D2, D21) |
| Decision source | Project team (D2, D21) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:143-151 parse_time returns None for a time with no offset, so the JSON API already rejects naive booking times. |
| Terms | AXS-T02, AXS-T12, AXS-T18, PUR-T18 |
| Candidate responsibility and dependencies | Access validates. Purchase builds valid_from and valid_until from the booking (D21) and owns opening hours (D3), blocks (D4) and any buffer (D6). The same reference format check (400) applies to the GET and revoke paths. |
| Open question | AXS-Q01 (cleaning buffer and early entry) |
| Clarification owner | Course instructor (business stakeholder) for AXS-Q01; Project team for the rule as stated |
| Next use | Contract (M2): POST /grants invalid-input examples; openapi.yaml (Access) request schema; Access API validation tests (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | No grant for BK-7KQ2M9 | POST /grants with every field and valid_from 2026-10-07T09:00:00+07:00, valid_until 2026-10-07T10:30:00+07:00 | 201; the e-ticket shows 2026-10-07 09:00-10:30. |
| 2 | boundary | JSON | No grant for BK-7KQ2M9 | The same body with valid_from 2026-10-07T02:00:00Z and valid_until 2026-10-07T03:30:00Z | 201; the same instants, shown as 2026-10-07 09:00-10:30 Bangkok. |
| 3 | counterexample | JSON | No grant for BK-7KQ2M9 | valid_from is 2026-10-07T09:00:00 (no offset) | 400 "valid_from needs a UTC offset"; nothing stored (D2). |
| 4 | boundary | JSON | No grant for BK-7KQ2M9 | valid_from and valid_until are both 2026-10-07T09:00:00+07:00 | 400 "valid_until must be after valid_from"; nothing stored. |
| 5 | counterexample | JSON | No grant | booking_reference is "7KQ2M9" (no BK- prefix) or space_name is empty | 400 naming the field; nothing stored. |
| 6 | counterexample | JSON | No grant for BK-7KQ2M9 | valid_from is 2026-10-07T08:45:00+07:00 (15 minutes before the start) | 201 with the window as sent. Access does not re-derive it; sending the start while the buffer is 0 is Purchase's duty (D21). |
| 7 | boundary | JSON | No grant for BK-7KQ2M9 | space_id 2147483648 | 400 {"error": "space_id is out of range"}; nothing stored; never a 500 |

### AXS-R04 Only Purchase calls the grant API, and Access calls no one

| Field | Value |
|---|---|
| Rule | POST /grants, GET /grants/{booking_reference} and POST /grants/{booking_reference}/revoke need the header `Authorization: Bearer <ACCESS_API_TOKEN>`. With no token, a wrong one or the wrong scheme, Access answers 401 {"error": "unauthorized"} before any validation or lookup (401 before 400 or 404) and changes nothing. Access refuses to start when ACCESS_API_TOKEN is unset, empty or shorter than 32 characters; an empty token never matches. Access makes no outbound call to Purchase, Payment or a lock. |
| Policy status | Decided (D19, D20; ADR-0004 (Purchase-only callers), no webhooks) |
| Decision source | Project team (ADR-0004 (Purchase-only callers), no webhooks); D19 and D20 name Purchase as the only caller |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:999-1002 the JSON unlock route answers anyone, with no token or session. |
| Terms | AXS-T01, AXS-T02, AXS-T19 |
| Candidate responsibility and dependencies | Access enforces it with a constant-time compare of UTF-8 bytes (ADR-0019). Only Purchase holds ACCESS_API_TOKEN. The e-ticket (bearer link, AXS-R09) and the kiosk (Staff password, AXS-R11) are not part of this API. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Contract (M2): auth section; openapi.yaml (Access) security scheme; e2e repeated requests (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | Purchase sends the correct bearer token | Purchase POSTs /grants for BK-7KQ2M9 | 201, as in AXS-R01. |
| 2 | counterexample | JSON | No Authorization header | A script POSTs /grants/BK-7KQ2M9/revoke | 401 {"error": "unauthorized"}; the grant stays issued. |
| 3 | boundary | JSON | A token that differs from ACCESS_API_TOKEN only in its last character | GET /grants/BK-7KQ2M9 | 401 {"error": "unauthorized"}; no grant data returned. |
| 4 | counterexample | internal | A grant is issued, revoked and scanned | Any Access action runs | Access sends no HTTP request to Purchase, Payment or a lock; it only answers. |
| 5 | counterexample | form | Member A's browser has no token | Member A opens the e-ticket at its ticket_url | 200: the e-ticket does not use the API token (AXS-R09). |
| 6 | boundary | JSON | The right token sent as "Basic" instead of "Bearer" | POST /grants/BK-7KQ2M9/revoke | 401 {"error": "unauthorized"}; nothing changes. |
| 7 | counterexample | internal | ACCESS_API_TOKEN unset or empty | Access starts | Non-zero exit with the message "ACCESS_API_TOKEN is required"; "Authorization: Bearer " with an empty token never matches. |
| 8 | counterexample | JSON | No Authorization header | POST /grants with booking_reference "7KQ2M9" | 401, not 400: the token is checked first. |
| 9 | counterexample | JSON | Any state | GET /grants/BK-7KQ2M9 with "Authorization: Bearer é" (a non-ASCII token) | 401 {"error": "unauthorized"}, never a 500: the compare runs on UTF-8 bytes. |
| 10 | boundary | internal | ACCESS_API_TOKEN is 31 characters, then 32 | Access starts | 31: non-zero exit with the message "ACCESS_API_TOKEN must be at least 32 characters"; 32: it starts. |

### AXS-R05 The ticket code is issued once and reused

| Field | Value |
|---|---|
| Rule | Access generates a grant's ticket code once, at issuance, stores it, and returns or shows that same code for the life of the grant: on a repeat POST /grants, on GET /grants, on the e-ticket, in the QR and at every check-in. It is never regenerated for the same grant. Revoking keeps it stored but stops it opening. |
| Policy status | Decided (D20, D22) |
| Decision source | Project team (D20 for issue-once and reuse, D22 for the code format), adopting the course's proposed policy: "Proposed policy: reuse the credential for the same valid grant. This changes behaviour: agree its scope and exceptions, update the rule, then implement and check." ([extraction site]). Class rules PR #12 (1c8ce57, unpinned) claimed this as observed implementation; the seed never stored a code (K4), so the class text is used only as a proposal, never as evidence. Supersedes the observed class PAY-R03 and PAY-T04. |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:984 generates secrets.token_hex(4) on every unlock and stores nothing (the observed behaviour this rule replaces). |
| Terms | AXS-T02, AXS-T03, AXS-T08, AXS-T09, AXS-T11 |
| Candidate responsibility and dependencies | Access decides. Scope: one grant, one code; a new booking gets a new grant and a new code. Exceptions: none; revocation disables the code (AXS-R14). |
| Open question | None. The class question on expiry (Q07) is answered by AXS-R13. |
| Clarification owner | Course instructor ([extraction site] proposed policy) and project team |
| Next use | Contract (M2): repeat examples; e2e "repeat grant" and check-in tests (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | The grant for BK-7KQ2M9 was issued with H7K3-9QXA at 2026-10-05 10:05 | On 2026-10-06 12:00 an API caller holding ACCESS_API_TOKEN (contract test) GETs /grants/BK-7KQ2M9 | 200, ticket_code H7K3-9QXA. |
| 2 | ordinary | form | The same grant | Member A opens the e-ticket twice and prints it | Every view and the printout show H7K3-9QXA and the same QR. |
| 3 | boundary | form | Member A got ok with H7K3-9QXA at 2026-10-07 09:02 | Member A comes back at 09:40 and scans again | ok; the code is still H7K3-9QXA. Re-entry does not change it. |
| 4 | counterexample | JSON | The grant for BK-7KQ2M9 exists | Purchase asks twice (repeat POST /grants) | H7K3-9QXA both times. The class-observed "200, a different code" (PAY-R03) no longer applies. |
| 5 | boundary | JSON | The grant for BK-7KQ2M9 was revoked | An API caller holding ACCESS_API_TOKEN (contract test) GETs /grants/BK-7KQ2M9 | 200, status revoked, ticket_code H7K3-9QXA still stored; the kiosk answers revoked for it. |

### AXS-R06 A ticket code is 8 unambiguous symbols and never starts with BK

| Field | Value |
|---|---|
| Rule | A ticket code is 8 symbols drawn at random from 23456789ABCDEFGHJKMNPQRSTVWXYZ, stored without a hyphen and shown XXXX-XXXX. Access discards a draw that starts with BK, and a draw that equals an existing code (UNIQUE violation), and draws again before it stores the grant. |
| Policy status | Decided (D22) |
| Decision source | Project team (D22) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:984 uses 8 lower-case hex characters, which include 0 and 1. |
| Terms | AXS-T08, PUR-T18 |
| Candidate responsibility and dependencies | Access, with a cryptographic random choice and UNIQUE(ticket_code), and a bounded number of redraws. 30 symbols to the power 8 is about 6.6 × 10^11 codes, so collisions are rare. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Access unit tests with a stubbed generator (M5); openapi.yaml (Access) pattern for ticket_code. |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | Issuance for BK-7KQ2M9 | The generator draws H7K39QXA | Stored as H7K39QXA; returned and shown as H7K3-9QXA. |
| 2 | boundary | internal | Issuance for BK-7KQ2M9 | The first draw is BKQ47MNP | Discarded and drawn again, so no code starts with BK and a hyphen-stripped booking reference (BK7KQ2M9) can never equal a code. |
| 3 | boundary | internal | M4TR-8WCE belongs to BK-3MZ8QT | The generator draws M4TR8WCE for BK-7KQ2M9 | UNIQUE violation; drawn again; BK-7KQ2M9 gets a different code. |
| 4 | counterexample | internal | Issuance for BK-7KQ2M9 | The generator draws B7KQ2M9A (starts B7, not BK) | Accepted: only the two-symbol prefix BK is excluded. |
| 5 | counterexample | internal | The old 8-hex style, for example 3f9a0c1e | Access checks whether it is a ticket code | It is not: it contains 0, 1 and lower case, which are outside the alphabet. |

### AXS-R07 The QR encodes exactly the ticket code

| Field | Value |
|---|---|
| Rule | The e-ticket shows the ticket code in large text and as a QR (inline SVG made with segno) that encodes exactly the same string, H7K3-9QXA. The QR carries no URL, token, booking reference or other data. |
| Policy status | Decided (D22) |
| Decision source | Project team (D22); ADR-0010 (segno) |
| Implementation evidence | Not implemented yet (planned M5). |
| Terms | AXS-T08, AXS-T09, AXS-T11 |
| Candidate responsibility and dependencies | Access renders it server-side; no image file and no external service. A USB QR scanner types the decoded string, then Enter, into the kiosk input. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Access template test comparing the segno payload with the code (M5); e2e check-in by typed code (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | The grant for BK-7KQ2M9, code H7K3-9QXA | Member A opens the e-ticket | Large text H7K3-9QXA and a QR that decodes to H7K3-9QXA. |
| 2 | ordinary | form | Staff at Meeting Room A; clock 2026-10-07 09:00 | Staff scans the QR with the USB scanner | The input receives H7K3-9QXA; result ok, the same as typing it. |
| 3 | boundary | form | The grant was revoked | Member A opens the e-ticket | The code and QR are still drawn, under the CANCELLED overlay; scanning them gives revoked. |
| 4 | counterexample | internal | The e-ticket for BK-7KQ2M9 is rendered | The QR payload is checked | It equals H7K3-9QXA. A payload holding the ticket_url, the ticket token or BK-7KQ2M9 breaks this rule. |

### AXS-R08 The booking reference is for support, never for entry

| Field | Value |
|---|---|
| Rule | The e-ticket shows the booking reference only in small type as "Booking ref (not for entry)". The kiosk never accepts a booking reference: after normalisation BK-7KQ2M9 becomes BK7KQ2M9, which no ticket code can equal, so the result is unknown_code, even though a grant for that reference exists. |
| Policy status | Decided (D22) |
| Decision source | Project team (D22) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:999-1002 unlocks by the numeric booking id in the URL, so the booking identifier alone yields a code. |
| Terms | AXS-T08, AXS-T11, AXS-T13, AXS-T16, PUR-T18 |
| Candidate responsibility and dependencies | Access. The booking reference is Purchase's identifier; Access keeps it as the grant key; GET /grants/{booking_reference} finds a grant by it for API token holders only. Purchase does not call GET /grants in v1 (PUR-R26). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | e2e "unknown code" check-in case (M6); e-ticket template (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | The grant for BK-7KQ2M9 | Member A opens the e-ticket | A small line "Booking ref (not for entry) BK-7KQ2M9"; the large code is H7K3-9QXA. |
| 2 | counterexample | form | Staff at Meeting Room A; clock 2026-10-07 09:10; the grant for BK-7KQ2M9 is issued | Staff types BK-7KQ2M9 | unknown_code; the scan is logged; the grant stays issued. |
| 3 | boundary | form | The same | Staff types bk7kq2m9 | Normalised to BK7KQ2M9; unknown_code. |
| 4 | ordinary | JSON | The grant for BK-7KQ2M9 is issued | An API caller holding ACCESS_API_TOKEN (contract test) GETs /grants/BK-7KQ2M9 | 200 with the status and ticket_url: the reference finds the grant through the API, never at the kiosk. |

### AXS-R09 The e-ticket link is a view-only bearer link

| Field | Value |
|---|---|
| Rule | Each grant has a random 128-bit ticket token, and ticket_url is Access's public URL plus `/t/<ticket_token>`. GET `/t/<ticket_token>` shows the e-ticket to whoever holds the link, with no login; any unknown token, well-formed or not, gives 404, never 400. The page has no action and shows no email and no member_ref. Whoever holds the link can read the code, so sharing the link shares entry for the window: the accepted bearer trade-off. The ticket token is secrets.token_urlsafe(16): 22 characters matching ^[A-Za-z0-9_-]{22}$, 128 random bits. The e-ticket response sends Referrer-Policy: no-referrer. The /t/ path also appears in the server access log; that is accepted at the same trust level as the database. |
| Policy status | Decided (D17) |
| Decision source | Project team (D17); ADR-0008 (bearer ticket link) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:812-834 the confirmation page opens for anyone by a sequential booking id. |
| Terms | AXS-T10, AXS-T11, AXS-T18 |
| Candidate responsibility and dependencies | Access generates the token (UNIQUE). Purchase shows the "View e-ticket" link only to the booking's owner or an operator (D17). |
| Open question | AXS-Q03 (sending the e-ticket by email) |
| Clarification owner | Project team |
| Next use | ADR-0008 (bearer ticket link); e2e ticket view (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | The grant for BK-7KQ2M9 | Member A follows "View e-ticket" on the Purchase booking page | 200 e-ticket; no login asked. |
| 2 | boundary | form | Member A forwards the link to Member B | Member B opens it | 200, the same page: the link is a bearer link (accepted, D17). |
| 3 | counterexample | form | Any browser | GET `/t/` with a made-up token | 404; no hint whether any ticket exists. |
| 4 | counterexample | form | Staff at Meeting Room A; clock 2026-10-07 09:10 | Staff types the ticket token from the URL into the kiosk | unknown_code: the token cannot check anyone in. |
| 5 | counterexample | form | The e-ticket is open | The page is read in full | No email, no member_ref, no check-in button, no form. |
| 6 | ordinary | form | The e-ticket for BK-7KQ2M9 | Read the e-ticket response headers | Referrer-Policy: no-referrer, so the ticket URL never leaves in a Referer header. |
| 7 | boundary | internal | The e-ticket for BK-7KQ2M9 | Read the access log line for GET /t/<ticket_token>?utm=x | Method, the /t/ path and status only: no query string and no referer (the path itself is logged, accepted). |
| 8 | counterexample | internal | Grants for BK-7KQ2M9 and BK-3MZ8QT | Compare their ticket tokens | Both match ^[A-Za-z0-9_-]{22}$ and share no sequence: neither token can be guessed from the other. |

### AXS-R10 The e-ticket shows the grant as it stands now

| Field | Value |
|---|---|
| Rule | The e-ticket shows the space name, the date and time in Bangkok, the check-in window, a status badge, the ticket code in large text with its QR, and "Booking ref (not for entry)". The badge follows the stored state and the clock: Issued, Checked in, Expired (now at or after valid_until), or Cancelled (revoked, with a CANCELLED overlay over the code and QR); when two apply, Cancelled wins over Expired, Expired over Checked in, and Checked in over Issued. The page shows only stored values, never a code taken from the URL, and prints on one page without navigation. |
| Policy status | Decided (D17, D21) |
| Decision source | Project team (D17, D21) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:832 renders a ?code= query value as the access code, so any URL can show a fake code. |
| Terms | AXS-T04, AXS-T05, AXS-T08, AXS-T09, AXS-T11, AXS-T12 |
| Candidate responsibility and dependencies | Access. Before a grant exists, Purchase shows "being prepared" (D20); Access has no page for a booking without a grant. |
| Open question | None. |
| Clarification owner | Project team |
| Next use | e-ticket template and print stylesheet (M5); Access template test for the badge and the overlay (M5); manual print check for row 5; UX flow diagram (M2). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | The grant for BK-7KQ2M9 is issued; clock 2026-10-05 11:00 | Member A opens the e-ticket | Meeting Room A; 2026-10-07 09:00-10:30; "Check-in 09:00-10:30"; badge Issued; H7K3-9QXA large with the QR; "Booking ref (not for entry) BK-7KQ2M9". |
| 2 | ordinary | form | Member A cancelled at 2026-10-05 11:00 and the grant was revoked | Member A opens the same link | 200; badge Cancelled; a CANCELLED overlay across the code and QR. |
| 3 | boundary | form | The grant is issued and never scanned; clock 2026-10-07 10:30 | Member A opens the e-ticket | Badge Expired: the window closed at 10:30. |
| 4 | counterexample | form | The grant for BK-7KQ2M9 | GET the ticket URL with ?code=AAAA-AAAA added | The page still shows H7K3-9QXA; the query value is ignored and never rendered. |
| 5 | boundary | form | The e-ticket is open | Member A prints it | manual: the print preview shows one page with the code, QR, room, date and window, and no navigation bar. |
| 6 | boundary | form | The grant for BK-7KQ2M9 was checked in at 2026-10-07 09:05; clock 10:30 | Member A opens the e-ticket | Badge Expired; data-status "checked_in" (the stored state) |
| 7 | boundary | form | The grant for BK-7KQ2M9 is revoked; clock 2026-10-07 10:30 | Member A opens the e-ticket | Badge Cancelled with the overlay, not Expired; data-status "revoked" |

### AXS-R11 The kiosk needs Staff sign-in and a selected room

| Field | Value |
|---|---|
| Rule | GET and POST /checkin need HTTP Basic with the password STAFF_PASSWORD, compared in constant time; any user name is accepted; otherwise 401 with WWW-Authenticate: Basic. Access refuses to start when STAFF_PASSWORD is unset, empty or shorter than 12 characters; an empty password never matches. Staff first selects the room, with a POST, from the space_id and space_name values in stored grants (tombstones excluded; one entry per space_id, listed by space_id ascending, labelled with the space_name of its grant with the greatest valid_from and the room number, "Meeting Room A (room 1)", because an archived space's name can be used again; a room whose space Purchase archived stays listed, accepted, because Access never asks Purchase). The kiosk shows the same label for the selected room with every result. The kiosk remembers the room in its access_session cookie until Staff changes it. A posted space_id that is not in that list gets 303 to /checkin with the flash "Unknown room", and the selection does not change. A POST with a code scans at the room stored in access_session; a space_id in the same POST is ignored. Only a POST without a code selects a room. A scan with no room selected is refused with a flashed "Select the room first". A code that is blank after normalisation (for example a scanner's double Enter) gets the flash "Enter a code", and no scan is stored. Access never asks Purchase for rooms. |
| Policy status | Decided (D15, D21; ADR-0019 (service authentication)) |
| Decision source | Project team (D15, D21; ADR-0019 (service authentication)) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:852-869 the unlock form accepts anyone, with no sign-in. |
| Terms | AXS-T02, AXS-T07, AXS-T13, AXS-T14, AXS-T15 |
| Candidate responsibility and dependencies | Access. The room lives in the access_session cookie (HttpOnly, SameSite=Lax, D15, AXS-R18), so a cross-site POST arrives without a room and is refused. Staff is not a Member and has no Purchase account. |
| Open question | AXS-Q04 (limits on failed Staff sign-ins) |
| Clarification owner | Project team |
| Next use | Kiosk template (M5); e2e check-in setup (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Grants exist for space_id 1 Meeting Room A and space_id 2 Focus Pod 1 | Staff opens /checkin with STAFF_PASSWORD and selects Meeting Room A | The kiosk shows "Meeting Room A (room 1)" and an autofocused code input. |
| 2 | boundary | form | No grant is stored yet | Staff opens /checkin | An empty room list: "No rooms yet: a room appears after its first ticket is issued". No code input. |
| 3 | counterexample | form | Board Room (space_id 3) exists in Purchase but has no grant | Staff looks for Board Room | Not listed; Access does not call Purchase for it. |
| 4 | counterexample | form | A wrong or missing password | GET /checkin | 401 with a Basic challenge; no scan stored (gunicorn's access log keeps the 401 line). |
| 5 | counterexample | form | Signed in, no room selected (or a cross-site form that arrives without the cookie) | POST /checkin with H7K3-9QXA | Flashed "Select the room first" and a redirect to /checkin; no check-in and no scan stored. |
| 6 | counterexample | internal | STAFF_PASSWORD unset or empty | Access starts | Non-zero exit with the message "STAFF_PASSWORD is required"; an empty Basic password never matches. |
| 7 | boundary | form | Signed in, Meeting Room A selected | A GET to /checkin carries another room in its query string | The selected room does not change: only a POST selects it. |
| 8 | counterexample | form | Signed in, Meeting Room A selected; no grant for space_id 3 | POST /checkin with space_id=3 and no code | 303 to /checkin with the flash "Unknown room"; Meeting Room A stays selected |
| 9 | counterexample | form | Signed in, Meeting Room A selected | POST /checkin with code "  - " (blank after normalisation) | The flash "Enter a code"; no scan stored |
| 10 | boundary | form | The kiosk browser is signed in; a page on another site holds a form that posts space_id=2 to /checkin | The kiosk browser submits it | Accepted risk (ADR-0016): the browser resends the cached Basic credentials and stores the new access_session, so the room changes to Focus Pod 1; the kiosk shows its room with every result, and the forged form cannot scan |
| 11 | counterexample | form | Signed in, no access_session (a cross-site form) | POST /checkin with space_id=1 and code=H7K3-9QXA | The flash "Select the room first"; no scan stored; the grant stays issued |
| 12 | boundary | form | Signed in, Meeting Room A selected in the cookie; a grant exists for Focus Pod 1 (space_id 2); clock 2026-10-07 09:10 | POST /checkin with space_id=2 and code=H7K3-9QXA | The scan runs at Meeting Room A (ok); the selection stays Meeting Room A |
| 13 | counterexample | form | Any state | GET /checkin with a Basic password holding a non-ASCII character | 401 with WWW-Authenticate: Basic, never a 500: the compare runs on UTF-8 bytes |
| 14 | boundary | form | Grants exist with space_name "Meeting Room A" under space_id 1 (archived in Purchase) and under space_id 5 (a new space with the same name) | Staff opens /checkin | Two entries, "Meeting Room A (room 1)" and "Meeting Room A (room 5)"; a ticket for room 5 scanned at room 1 gets wrong_room "This ticket is for Meeting Room A (room 5)" |
| 15 | boundary | internal | STAFF_PASSWORD is 11 characters, then 12 | Access starts | 11: non-zero exit with the message "STAFF_PASSWORD must be at least 12 characters"; 12: it starts. |

### AXS-R12 Kiosk input is normalised before lookup

| Field | Value |
|---|---|
| Rule | Before lookup the kiosk upper-cases the input and strips spaces and hyphens. The result must equal a stored ticket code exactly. There is no other correction (no mapping of O to 0 or similar); anything else gives unknown_code. |
| Policy status | Decided (D22) |
| Decision source | Project team (D22) |
| Implementation evidence | Not implemented yet (planned M5). |
| Terms | AXS-T08, AXS-T13, AXS-T15, AXS-T16 |
| Candidate responsibility and dependencies | Access. The D22 alphabet leaves out 0, O, 1, I, L and U, so look-alike symbols never need mapping. |
| Open question | AXS-Q04 (limits on repeated unknown codes). |
| Clarification owner | Project team |
| Next use | Access unit test for the normaliser (M5). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Staff at Meeting Room A; clock 2026-10-07 09:00 | The scanner types H7K3-9QXA | Normalised H7K39QXA; it matches; ok. |
| 2 | boundary | form | The same | Staff types " h7k3 9qxa " | Normalised H7K39QXA; it matches; ok. |
| 3 | boundary | form | The same | Staff types H7K3-9QX (7 symbols) | unknown_code. |
| 4 | counterexample | form | The same | Staff types H7K3-9OXA (letter O in place of Q) | unknown_code; the kiosk does not guess look-alike symbols. |

### AXS-R13 A code opens only inside its check-in window

| Field | Value |
|---|---|
| Rule | For a matching grant that is not revoked, scanned at its own room, the kiosk answers ok "Door unlocked (mock)" when valid_from ≤ now < valid_until, where now is clock.now(). Before valid_from it answers not_open_yet with the opening time (HH:MM on the same Bangkok date, otherwise YYYY-MM-DD HH:MM). At or after valid_until it answers closed with the closing time, in the same format ("Check-in closed at 10:30"). Re-entry inside the window is allowed: every scan inside it is ok. |
| Policy status | Decided (D21) |
| Decision source | Project team (D21, D6, D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:970-985 issue_access_code returns a code for a paid booking at any time; there is no window. |
| Terms | AXS-T12, AXS-T13, AXS-T16, AXS-T17 |
| Candidate responsibility and dependencies | Access checks; Purchase sets the window (D21). Time comes only from clock.now() (D27), so e2e tests can set the instant. |
| Open question | AXS-Q01 (cleaning buffer and early entry); AXS-Q02 (real door-lock integration); AXS-Q07 (order of the kiosk checks); PUR-Q12 (a pending revoke leaves the old code opening) |
| Clarification owner | Course instructor (business stakeholder) for AXS-Q01; course instructor (Integrations/Locks scope) and project team for AXS-Q02; Project team for AXS-Q07, PUR-Q12 and the rule as stated |
| Next use | e2e check-in before, inside and after the window (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | boundary | form | Staff at Meeting Room A; the grant for BK-7KQ2M9 (window 2026-10-07 09:00-10:30); clock 2026-10-07 09:00 | Staff scans H7K3-9QXA | ok "Door unlocked (mock)". |
| 2 | boundary | form | The same; clock 2026-10-07 08:59 | Staff scans H7K3-9QXA | not_open_yet (opens 09:00). |
| 3 | boundary | form | The same; clock 2026-10-07 10:30; Member B's grant BK-3MZ8QT (M4TR-8WCE) for Meeting Room A opens at 10:30 | Staff scans H7K3-9QXA, then M4TR-8WCE | closed for H7K3-9QXA; ok for M4TR-8WCE. Adjacent bookings hand over at 10:30. |
| 4 | ordinary | form | Member A got ok at 09:05 | Staff scans H7K3-9QXA again at 09:40 | ok again (re-entry). |
| 5 | counterexample | form | The same grant; clock 2026-10-05 10:00 | Staff scans H7K3-9QXA | not_open_yet (opens 2026-10-07 09:00). No early entry while the buffer is 0 (D6, D21). |
| 6 | counterexample | form | The same grant; clock 2026-10-08 09:00 | Staff scans H7K3-9QXA | closed "Check-in closed at 2026-10-07 10:30". The code does not open after the booking ends (class Q07); the grant stays stored. |

### AXS-R14 Check-in rejects unknown, revoked and wrong-room codes before it checks the time

| Field | Value |
|---|---|
| Rule | The kiosk decides in this order and stops at the first answer: unknown_code "Code not recognised" (no stored ticket code equals the normalised input), revoked (the grant is revoked), wrong_room (the grant's space_id is not the selected room; the reason names the ticket's room with its room number), then the window (AXS-R13). Each result is shown large with its reason after a redirect to /checkin, carried by a flashed message, never by a query string. |
| Policy status | Decided (D21) |
| Decision source | Project team (D21 for the window, D28 for flashed results); the order of the checks is the default of AXS-Q07 |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:980-983 checks only that the booking exists (404) and is paid (402). |
| Terms | AXS-T06, AXS-T13, AXS-T16 |
| Candidate responsibility and dependencies | Access. The order puts the most decisive answer first, so a cancelled ticket says revoked wherever it is scanned. The kiosk checks room, time and revocation, never identity: the subject is whoever presents the ticket code, because the ticket is a bearer credential (D17; ADR-0008 (bearer ticket link)). |
| Open question | AXS-Q07 (order of the kiosk checks); AXS-Q02 (real door-lock integration) |
| Clarification owner | Course instructor (Integrations/Locks scope) and project team for AXS-Q02; Project team for AXS-Q07 and the rule as stated |
| Next use | e2e wrong room, revoked and unknown code cases (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | A grant exists for Board Room (BK-3HT8WD), so Staff can select it; Staff at Board Room (space_id 3); the grant for BK-7KQ2M9 is issued for Meeting Room A; clock 2026-10-07 09:10 | Staff scans H7K3-9QXA | wrong_room "This ticket is for Meeting Room A (room 1)". |
| 2 | ordinary | form | Staff at Meeting Room A; the grant for BK-7KQ2M9 was revoked at 2026-10-05 11:00; clock 2026-10-07 09:10 | Staff scans H7K3-9QXA | revoked "This ticket was cancelled". |
| 3 | boundary | form | As row 1, Staff at Board Room; the grant for BK-7KQ2M9 is revoked; clock 2026-10-07 09:10 | Staff scans H7K3-9QXA | revoked: revocation is checked before the room. |
| 4 | boundary | form | As row 1, Staff at Board Room; the grant for BK-7KQ2M9 is issued; clock 2026-10-07 08:00 | Staff scans H7K3-9QXA | wrong_room, not not_open_yet: the room is checked before the time. |
| 5 | counterexample | form | Staff at Meeting Room A; clock 2026-10-07 09:10 | Staff scans Z9Z9-Z9Z9 (no such code) | unknown_code "Code not recognised"; nothing else is revealed. |
| 6 | counterexample | form | Staff at Meeting Room A | Open /checkin?error=ok | No result is shown; the query value is ignored and never rendered. |

### AXS-R15 Every scan is logged and the kiosk shows the last 10

| Field | Value |
|---|---|
| Rule | Access stores every scan with the time (clock.now()), the selected room, the normalised input, the result and the matched grant, if any. The kiosk shows the last 10 scans at the selected room, newest first (by scan time, then by scan id, both descending, because a frozen test clock gives equal times), with the code masked to its last 4 symbols (••••-9QXA) and the time as HH:MM for today's scans, YYYY-MM-DD HH:MM for older ones; the full normalised input stays only in the scans table. Older scans stay stored. |
| Policy status | Decided (D21, D27) |
| Decision source | Project team (D21, D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, gunicorn.conf.py:1-5 logs request paths without the query string because the code travelled as ?code=; no unlock is recorded anywhere. |
| Terms | AXS-T05, AXS-T13, AXS-T15, AXS-T16, AXS-T17 |
| Candidate responsibility and dependencies | Access (a scans table). The log feeds the derived no-show (AXS-R16) and support questions. It records scans, never door openings. |
| Open question | AXS-Q04 (limits on repeated unknown codes) |
| Clarification owner | Project team |
| Next use | e2e check-in assertions (M6); scans table in the data model diagram (M2). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Staff at Meeting Room A; clock 2026-10-07 09:05 | Staff scans H7K3-9QXA | ok; the list gains "09:05 ••••-9QXA ok" at the top. |
| 2 | boundary | form | 10 scans are already listed | An 11th scan | The newest 10 are listed; the oldest drops off the screen but stays stored. |
| 3 | counterexample | form | Staff at Meeting Room A | Staff types BK-7KQ2M9 | The unknown_code scan is logged too, with input BK7KQ2M9 and no grant; the kiosk shows it as ••••-Q2M9. |
| 4 | boundary | form | Scans exist at Board Room and at Meeting Room A | Staff at Meeting Room A views the kiosk | Only Meeting Room A scans are listed. |
| 5 | counterexample | internal | An ok scan is stored | The stored row is read | It records result ok, not "door opened": the lock is mocked. |
| 6 | counterexample | form | Staff at Meeting Room A; 10 scans listed | Anyone reads the kiosk screen | No full ticket code is shown; the full input is only in the scans table. |
| 7 | boundary | form | Clock 2026-10-08 08:05; the last scan at Meeting Room A was H7K3-9QXA at 2026-10-07 09:05 | Staff views the kiosk | The row reads "2026-10-07 09:05 ••••-9QXA ok": a scan from another day shows its date. |

### AXS-R16 A grant is issued, checked in or revoked, and the rest is derived

| Field | Value |
|---|---|
| Rule | A grant is stored in one of three states: issued (at issuance), checked_in (at its first ok scan) and revoked (at revoke, from issued or checked_in; final). Nothing else changes the state. Not yet valid, expired and no-show are derived on read from clock.now(), the window and the state, and are never stored; GET /grants reports the derived value as "condition" (not_yet_valid, expired or no_show; null otherwise) beside the stored "status". checked_in means an ok scan was recorded, not that a door opened. |
| Policy status | Decided (D19, D21) |
| Decision source | Project team (D19, D21, D27); Course [extraction site]: "A stored grant does not by itself prove that a door can be opened."; Course [contexts site]: "Payment success ≠ access provisioned ≠ a successful door opening." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:970-985 keeps no access state at all. |
| Terms | AXS-T02, AXS-T04, AXS-T05, AXS-T06, AXS-T15, AXS-T17 |
| Candidate responsibility and dependencies | Access. Purchase keeps only its own record of issuance and revocation on the booking (PUR-T34); it never derives no-show and does not call GET /grants in v1. |
| Open question | AXS-Q06 (what a no-show changes); AXS-Q02 (real door-lock integration) |
| Clarification owner | Course instructor (Integrations/Locks scope) and project team for AXS-Q02; Project team, with the course instructor (business stakeholder), for AXS-Q06; Project team for the rule as stated |
| Next use | State diagram, Access (Grant) composite (M2); e2e check-in and cancel tests (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | internal | The grant for BK-7KQ2M9 is issued | The first ok scan at 2026-10-07 09:02 | State checked_in. |
| 2 | boundary | internal | The grant is checked_in | Another ok scan at 09:40 | State stays checked_in; the scan is logged. |
| 3 | ordinary | JSON | The grant is checked_in; the Operator cancels at 2026-10-07 09:30, before the end (D18) | Purchase POSTs /grants/BK-7KQ2M9/revoke | 200 status revoked; a scan at 09:35 answers revoked. |
| 4 | boundary | JSON | The grant is issued and never scanned; clock 2026-10-07 10:30 | An API caller holding ACCESS_API_TOKEN (contract test) GETs /grants/BK-7KQ2M9 | 200 "status": "issued", "condition": "no_show" (derived). Nothing is written. |
| 5 | counterexample | internal | The grant is revoked | Any later POST /grants, scan or clock change | The state stays revoked; it never returns to issued or checked_in. |
| 6 | counterexample | JSON | The grant is checked_in | An API caller holding ACCESS_API_TOKEN (contract test) GETs /grants/BK-7KQ2M9 | status checked_in, which proves an ok scan, not a door opening: the lock is mocked. |

### AXS-R17 Revoke is idempotent and changes nothing outside Access

| Field | Value |
|---|---|
| Rule | POST /grants/{booking_reference}/revoke sets the grant to revoked and answers 200 with status revoked; repeating it answers the same and changes nothing. Revoking an unknown reference stores a revoked tombstone (AXS-R02). Revoke calls no other service: "The booking and successful payment remain recorded. No automatic refund is implied." |
| Policy status | Decided (D19) |
| Decision source | Project team (D18, D19); Course [contexts site]: "Access is revoked. The booking and successful payment remain recorded. No automatic refund is implied." |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:917-930 cancel hard-deletes the booking row; there is no revoke. |
| Terms | AXS-T02, AXS-T04, AXS-T06, AXS-T07, AXS-T11 |
| Candidate responsibility and dependencies | Access revokes. Purchase decides when (D19 step 2, retried idempotently on the booking page or GET /api/bookings/<ref>, by the owner's Retry or by the Operator's Retry, PUR-R26, PUR-R32) and whether a refund follows (D18, D19). |
| Open question | AXS-Q05 (restoring a revoked grant) |
| Clarification owner | Project team, with the course instructor for cancellation scope, for AXS-Q05; Course instructor ([contexts site]) and project team for the rule as stated |
| Next use | Contract (M2) revoke examples; e2e Member cancel and operator cancel, each revoking the grant (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | The grant for BK-7KQ2M9 is issued; Member A cancels at 2026-10-05 11:00, at least 24 h before the start (100% refund, D18) | Purchase POSTs /grants/BK-7KQ2M9/revoke | 200 status revoked. The refund is between Purchase and Payment; Access calls neither. |
| 2 | boundary | JSON | The grant is already revoked | Purchase retries the revoke after a timeout | 200 status revoked; revoked_at unchanged; nothing else changes. |
| 3 | ordinary | form | The grant is revoked | Member A opens the e-ticket | Badge Cancelled with the CANCELLED overlay. |
| 4 | boundary | JSON | No grant for BK-P4W6RC | Purchase POSTs /grants/BK-P4W6RC/revoke | 200 status revoked; a tombstone is stored. |
| 5 | counterexample | JSON | Member A cancels at 2026-10-06 10:00, under 24 h before the start (0% refund, D18) | Purchase revokes BK-7KQ2M9 | 200 status revoked, exactly as with a 100% refund: Access neither knows nor changes the refund. |

### AXS-R18 Cookies and SECRET_KEY

| Field | Value |
|---|---|
| Rule | Refuse to start when SECRET_KEY is unset, empty, shorter than 32 characters or the seed's public default "dev-secret-key-not-for-production" (ADR-0019). Set the access_session cookie HttpOnly and SameSite=Lax, plus Secure when PUBLIC_URL starts with https. It holds only the selected kiosk room and flashed results, and lasts until the browser closes or Staff changes the room. |
| Policy status | Decided (D15) |
| Decision source | Project team (D15). ADR-0009 (SameSite as the CSRF mitigation). |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:20 falls back to a public default SECRET_KEY. |
| Terms | AXS-T13, AXS-T15 |
| Candidate responsibility and dependencies | Access. The kiosk's CSRF defence (AXS-R11) depends on SameSite. Purchase and Payment follow the same rule for their own cookies (PUR-R03, PMT-R19). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Access startup and cookie tests (M5); README env list (M7). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | form | Staff is signed in | Staff selects Meeting Room A | access_session is set HttpOnly and SameSite=Lax; it holds the room and nothing about any grant. |
| 2 | boundary | internal | PUBLIC_URL starts with https | Staff selects a room | The cookie also carries Secure; with http it does not. |
| 3 | counterexample | internal | SECRET_KEY unset or empty, for example copied unchanged from .env.example | Access starts | Non-zero exit with the message "SECRET_KEY is required"; no default key is used. |
| 4 | counterexample | internal | SECRET_KEY is "x" | Access starts | Non-zero exit with the message "SECRET_KEY must be at least 32 characters". |
| 5 | counterexample | internal | SECRET_KEY is "dev-secret-key-not-for-production" (33 characters) | Access starts | Non-zero exit with the message "SECRET_KEY is the public seed default". |

### AXS-R19 The test clock is off unless TEST_CLOCK_ENABLED=true

| Field | Value |
|---|---|
| Rule | Read time only through clock.now() (check-in window, derived conditions, scan times); never use SQL now() or CURRENT_TIMESTAMP in business logic. Answer POST /_test/clock with 404 unless TEST_CLOCK_ENABLED is exactly "true"; when it is, store {"now": iso-or-null} in the one-row test_clock table, where null clears the override; a "now" that is not ISO 8601 with an offset gets 400 and stores nothing (D2). With the flag off, clock.now() returns real time and never reads test_clock, even if a row still holds an override. The override is a fixed instant: clock.now() returns exactly the stored value on every read until the next POST /_test/clock; it never advances. With the flag on, clock.now() reads the test_clock row on every call (no per-process cache), so both gunicorn workers see a new instant from the next request. Never set the flag in the Dockerfile, the service compose.yaml or .env.example. |
| Policy status | Decided (D27) |
| Decision source | Project team (D27) |
| Implementation evidence | Not implemented yet (planned M5). Spacey: source inspected at 5a1cf3d, app.py:970-985 issue_access_code has no time check and no clock. |
| Terms | AXS-T05, AXS-T12, AXS-T15 |
| Candidate responsibility and dependencies | Access. Purchase and Payment have the same guard (PUR-R38, PMT-R20). |
| Open question | None. |
| Clarification owner | Project team |
| Next use | Access clock and guard tests (M5); e2e check-in tests set the instant (M6). |

| # | Kind | Channel | Given | When | Expected result under this rule |
|---|---|---|---|---|---|
| 1 | ordinary | JSON | TEST_CLOCK_ENABLED=true; the grant for BK-7KQ2M9 is issued | POST /_test/clock {"now": "2026-10-07T09:00:00+07:00"} | 200; a scan of H7K3-9QXA at Meeting Room A then answers ok. |
| 2 | boundary | JSON | TEST_CLOCK_ENABLED=true; an override is set | POST /_test/clock {"now": null} | 200; the override is cleared. |
| 3 | counterexample | JSON | TEST_CLOCK_ENABLED unset, "false" or "1" | POST /_test/clock {"now": "2026-10-07T09:00:00+07:00"} | 404; nothing stored; scans still use the real time. |
| 4 | counterexample | internal | The Access Dockerfile, compose.yaml and .env.example | Look for TEST_CLOCK_ENABLED | Set in none of them; only the e2e compose override sets it. |
| 5 | counterexample | JSON | TEST_CLOCK_ENABLED=true | POST /_test/clock {"now": "2026-10-07T09:00:00"} (no offset) | 400; nothing stored. |
| 6 | counterexample | internal | An override 2026-10-07T09:00:00+07:00 is stored; Access restarts with TEST_CLOCK_ENABLED unset | Staff scans H7K3-9QXA | The window is checked against real time: clock.now() never reads test_clock while the flag is off. |
| 7 | boundary | form | TEST_CLOCK_ENABLED=true; override 2026-10-07T10:29:59+07:00; the grant for BK-7KQ2M9 is issued | Staff scans H7K3-9QXA twice, 2 s apart | ok both times: the override never advances past valid_until 10:30 |
| 8 | boundary | internal | TEST_CLOCK_ENABLED=true; two Access app instances with their own database connections (like the two workers) share one database | Instance 1 handles POST /_test/clock {"now": "2026-10-05T10:15:00+07:00"}; then instance 2 reads clock.now() | 2026-10-05T10:15:00+07:00: clock.now() reads the row on every call, never a per-process copy (a service test) |
