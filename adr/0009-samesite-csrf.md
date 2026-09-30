# ADR-0009 SameSite=Lax cookies are the CSRF mitigation

## Status

Accepted, 2026-10-01

## Context

Example: while Member A is logged in, a page on another site auto-submits a hidden form that POSTs to Purchase's /bookings/BK-7KQ2M9/cancel. The browser sends that cross-site POST without `purchase_session`, because the cookie is SameSite=Lax. Purchase sees an anonymous request and answers with the login step. Nothing is cancelled.

- Seed flaw F13: no form carries a CSRF token, no route checks one, `requirements.txt` has no CSRF library, and `SESSION_COOKIE_SAMESITE` is never set (templates/base.html:17, index.html:30-35, login.html:11-15, confirmation.html:9-19). Source inspected at 5a1cf3d.
- The stack allows one new runtime dependency, `segno` (ADR-0010). A CSRF library such as Flask-WTF is out.
- Members come back from Payment's hosted page to Purchase by a top-level GET redirect to success_url. That return must carry the login.

## Decision

- Set every session cookie HttpOnly and SameSite=Lax, plus Secure when PUBLIC_URL starts with https: `purchase_session`, `payment_session`, `access_session`.
- Run every state-changing browser action as a POST (PUR-R37): book, cancel, Retry, Reconcile, logout, archive, the plan toggle, every space edit; Pay on the hosted page (PMT-R10); the kiosk room choice and scan (AXS-R11).
- Never start an action on a GET. A GET may only run the idempotent sync that moves a booking toward an outcome already decided: reconcile, pending grant, revoke or refund (D13, D19, D20).
- Use no CSRF tokens.
- Choose Lax, not Strict: Lax sends the cookie on a top-level GET, so the Member is still logged in after the redirect back from payment. That is exactly why a GET must stay safe.

## Consequences

- Good: no dependency, no hidden field in every template, no token store. One review rule: writes are POSTs.
- Bad: SameSite works per site, not per origin. localhost:8001, 8002 and 8003 are one site, so our own services could post to each other with the cookie. Accepted: they are our code. Deploy under a domain we control, with no untrusted sibling subdomains.
- Bad: HTTP Basic credentials are not cookies, so SameSite does not cover them. Payment's /operator only reads. A forged cross-site scan at /checkin arrives without `access_session`, so it has no room and is refused ("Select the room first"). A forged room change is possible; the kiosk shows its room with every result (ADR-0016).
- Bad: it relies on the browser honouring SameSite. A very old browser would send the cookie.
- Bad: one GET that changes state by mistake would be forgeable. Code review checks PUR-R37.

## Alternatives considered

- **Synchronizer tokens with Flask-WTF.** Rejected: a new runtime dependency.
- **Hand-rolled tokens** (a secret in the session, a hidden field in each form). Works without a dependency, but adds code to every form in three services. Kept as the upgrade path.
- **Origin header check.** A few lines of defence in depth; deferred while Lax holds.
- **SameSite=Strict.** Rejected: on separate sites the return from the hosted page would arrive without the login.

## Rules and decisions

- Rules: PUR-R03, PUR-R37, PMT-R10, PMT-R19, AXS-R11, AXS-R18.
- Decisions: D13, D15, D19, D20, D28.
- Related: ADR-0016, ADR-0019.

## Sources

- Spacey main 5a1cf3d: seed flaw F13 (source inspected at 5a1cf3d).
- Project team (D15).
