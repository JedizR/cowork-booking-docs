# ADR-0008 The e-ticket link is a bearer link

## Status

Accepted, 2026-10-01

## Context

Example: BK-7KQ2M9 is confirmed, and Access returns a ticket_url of the form `<ACCESS_PUBLIC_URL>/t/<ticket_token>`. Member A presses "View e-ticket" and sees Meeting Room A, 2026-10-07 09:00-10:30, and the code H7K3-9QXA with its QR. Member A forwards the link to a colleague. At 09:05 the colleague shows the QR at the Meeting Room A kiosk: ok. Anyone holding the link can do the same.

- The product model is a cinema e-ticket: the link or printout is the ticket, and whoever holds it gets in.
- Access holds no accounts (ADR-0002) and calls no one (ADR-0004), so it cannot check a Purchase login.
- Seed flaw F4: the access code is regenerated on every unlock and never stored, and the confirmation page renders any `?code=` value as "Your access code" (app.py:832, 970-985; templates/confirmation.html:21-22). Seed flaw F7: unlock is anonymous. Source inspected at 5a1cf3d.
- The course: Integrations / Locks "Checks subject, door, time and revocation." [contexts site]; "Proposed policy: reuse the credential for the same valid grant." [extraction site].

## Decision

- Give each grant a random 128-bit ticket token from Python's `secrets`, unique. ticket_url = ACCESS_PUBLIC_URL + `/t/<ticket_token>`.
- Make the link view-only. GET /t/<ticket_token> shows the stored ticket code, its QR, the space, the Bangkok date and time, the check-in window and the status. It has no action and shows no email and no member_ref. An unknown token gets 404.
- Send `Referrer-Policy: no-referrer` on the e-ticket.
- Show only stored values, never text from the URL.
- Let only the kiosk check in. The link cannot.
- Check door, time and revocation at the kiosk, not the subject: whoever presents the code is the guest.
- Let revocation end it. After a cancel, the page shows CANCELLED and the kiosk answers revoked.
- In Purchase, show the "View e-ticket" link only to the booking's owner or an operator (PUR-R05).

## Consequences

- Good: works like a cinema ticket. Print it, forward it to a colleague, open it on a phone at the door.
- Good: Access needs no identity data and no login page; the spoofable `?code=` of F4 is gone.
- Bad: forwarding the link forwards entry for the booking's window.
- Bad: a leaked link (shared screen, browser history, a proxy log) leaks entry. The /t/ path also appears in Access's own access log, at the same trust level as its database.
- Bad: the link cannot be rotated without revoking the grant (AXS-Q05).

## Alternatives considered

- **Member login on Access.** Rejected: Access would need accounts or an Identity service (ADR-0002).
- **A short-lived link signed by Purchase.** Rejected: a shared signing secret, or a call from Access back to Purchase (ADR-0004).
- **Show the ticket only inside Purchase.** Rejected: Purchase would store or proxy the credential, which Access owns ("Owns grants and issuance" [extraction site]).
- **Email the ticket.** No email in v1 (AXS-Q03).

## Rules and decisions

- Rules: AXS-R05, AXS-R07, AXS-R08, AXS-R09, AXS-R10, AXS-R14, AXS-R17, PUR-R05, PUR-R26.
- Terms: AXS-T08, AXS-T10, AXS-T11. Questions: AXS-Q03, AXS-Q05.
- Decisions: D17, D21, D22.
- Related: ADR-0002, ADR-0010, ADR-0016.

## Sources

- Spacey main 5a1cf3d: seed flaws F4 and F7, app.py:832 and 970-985, templates/confirmation.html:21-22 (source inspected at 5a1cf3d).
- course site [contexts site] fetched 2026-09-30: C20.
- course site [extraction site] fetched 2026-09-30: E11, E45.
- Project team (D17).
