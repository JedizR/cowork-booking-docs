# ADR-0002 Account data on Member in Purchase, no Identity context

## Status

Accepted, 2026-10-01

## Context

Example: a@example.com registers on Purchase as Member A (display name, password of at least 8 characters). Member A logs in, books BK-7KQ2M9 and sees My bookings. The Operator turns on Member B's `plan_active`. Every one of these facts sits on one row: Member, in Purchase.

- Class rules PR #10 first put the account terms (ACC-T01 Account, ACC-T02 Login session, ACC-R01, ACC-R02) in a new "Identity" context. The course instructor reviewed it (CHANGES_REQUESTED on bb9f346): "change the context to the existing \"Purchase\" and good to go" / "In the future can be extracted in the different context". The author applied it in d68631f.
- The seed keeps accounts in a `users` table beside bookings, with no role column (app.py:73-78), and lets a logged-in user book under any typed name (seed flaws A4 and A9; coverage keyed by that name, F6). Sessions never expire (F10). Source inspected at 5a1cf3d.
- Best practice puts identity (credentials, sessions, password policy, roles) in its own generic context, shared by every product and kept apart from purchasing.

## Decision

- **This is a deliberate deviation from best practice.** We follow the course instructor's request on class rules PR #10 and record it here as a deviation, not as a recommendation.
- Keep account data on Member in Purchase: email (unique, lower-cased), display_name, password hash, `is_operator`, `plan_active`.
- Purchase runs register, login, logout and the 12-hour session in the `purchase_session` cookie (PUR-R01, PUR-R02, PUR-R03).
- Build no Identity context and no fourth service.
- Payment and Access hold no accounts. Access gets only an opaque `member_ref` (AXS-T18). Payment gets only a `booking_reference`.
- Keep the seam narrow: bookings refer to a member by id only, and account code stays apart from booking code inside Purchase.

## Future extraction path to an Identity context

1. Trigger: email confirmation (PUR-Q04), failed-login limits (PUR-Q05), password reset, named Staff and operator logins, or a second product that needs the same login.
2. Create an Identity service with its own database. Copy email, display_name and password hash, keyed by the same member id.
3. Move register, login, logout and the session to Identity. Purchase accepts Identity's session or token and keeps the member id as a reference.
4. Move `is_operator` to Identity as a role. Keep `plan_active` in Purchase: coverage is Purchase's ("Owns price and coverage" [extraction site]).
5. Leave Payment and Access unchanged: they never see account data, and `member_ref` keeps its value.
6. Replace HTTP Basic on the Payment operator page and the Access kiosk with Identity logins (ADR-0019).
7. Drop the account columns from Purchase one release after the switch. Every Member logs in again once.

## Consequences

- Good: three services, not four. One login, one cookie, one place to promote the operator (PUR-R04).
- Good: coverage reads `plan_active` on the same row as the login, with no call (PUR-R19).
- Bad: Purchase's database holds password hashes beside bookings, so one breach exposes both.
- Bad: a login change ships with booking changes, and Payment and Access cannot reuse the Member login. Their staff pages use HTTP Basic (ADR-0016, ADR-0019).
- Bad: extraction later needs a data copy and a session handover.

## Alternatives considered

- **Identity context and service now.** Best practice. Rejected: the course instructor asked for Purchase, and v1 has no email, no SSO and no second product to share it.
- **External identity provider (OAuth).** A new dependency and an outside service; not in the pinned stack.
- **Account copies in each service.** Three password stores; rejected.

## Rules and decisions

- Rules: PUR-R01, PUR-R02, PUR-R03, PUR-R04, PUR-R05, PUR-R06, PUR-R19, AXS-R03, AXS-R09.
- Terms: PUR-T01, PUR-T02, PUR-T03, AXS-T18. Questions: PUR-Q04, PUR-Q05, PMT-Q05.
- Decisions: D10, D15, D16, D17.
- Related: ADR-0001, ADR-0016, ADR-0019.

## Sources

- Course instructor, class rules PR #10 review on bb9f346, applied in d68631f (class PR #10 discussion).
- class PR #10 diff at d68631f: ACC-T01, ACC-T02, ACC-R01, ACC-R02, Q-ACC-1 to Q-ACC-4.
- Spacey main 5a1cf3d: app.py:73-78 `users`; seed flaws A4, A9, F6, F10 (source inspected at 5a1cf3d).
- course site [extraction site] fetched 2026-09-30: E11.
