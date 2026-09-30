# ADR-0016 Accepted security trade-offs

## Status

Accepted, 2026-10-01

## Context

Example: Member A logs in on a shared computer at 2026-10-05 10:00 and logs out at 12:00. Someone who copied the `purchase_session` cookie at 11:00 can still use it until 22:00, 12 hours after login. We accept that, and we say so.

The seed had many security holes (inventory/spacey-flaws.md, source inspected at 5a1cf3d). Most are fixed by D1-D28. Five are only narrowed. For each, the fix costs more than v1 can justify: an email service, server-side sessions, named staff accounts, or a real card processor. The course asks for honesty over polish: "Record unknown or unhandled cases honestly." and "Work is graded on evidence and trade-offs, not on the volume of generated output or the polish of a demo." [syllabus site].

## Decision

Accept these five trade-offs. Document each in the PRD and the service READMEs.

| # | Trade-off we accept | Seed flaw it answers | What someone can do | What limits it | Rules and decisions |
|---|---|---|---|---|---|
| 1 | Logout replay inside 12 h | F10: sessions never expire, logout only clears that browser, the default SECRET_KEY is used in deploy (app.py:20, 386, 508, 536) | Reuse a copied cookie until 12 h after login, even after logout | Absolute 12 h expiry; SECRET_KEY required, fail fast; HttpOnly; Secure over https | PUR-R03, D15 |
| 2 | Registration enumeration | F11: registration reveals whether an email exists (app.py:461-462, 485-486) | Learn whether an email has an account by trying to register it | Login keeps one uniform error; hiding it would need a confirmation email, and v1 sends none | PUR-R01, PUR-R02, PUR-Q04, D16 |
| 3 | Bearer ticket link | F4: the code is never stored and any ?code= value is shown (app.py:832, 970-985); F7: unlock is anonymous | Whoever gets the /t/ link can read the code and check in during the window | 128-bit token; view-only; no email shown; no-referrer; revoke ends it; Purchase shows the link only to the owner or an operator (ADR-0008) | AXS-R09, PUR-R05, D17 |
| 4 | HTTP Basic for the Payment operator page and the Access kiosk | F7: space admin and unlock are anonymous (app.py:570-599, 620-682, 852-869); F8: the revenue dashboard is public (app.py:1027-1050) | Anyone who learns OPERATOR_PASSWORD or STAFF_PASSWORD gets in; passwords are shared, with no per-person audit, no lockout and no logout | Constant-time compare; refuse to start without the password; https in production; every scan is logged (ADR-0019) | PMT-R17, AXS-R11, AXS-R15, AXS-Q04 |
| 5 | Mock card data | F16: a 0-amount booking still asks for a card (app.py:953-955); A6: the force_failure test hook is live (app.py:957-958, 995) | Pay any session with a test card; anyone with a /pay/ link can pay that session; no real money moves | Documented test cards only; amounts come from Purchase; only brand and last4 stored (ADR-0018, ADR-0020) | PMT-R08, PMT-R09, PMT-R13, PMT-Q05 |

Also accepted, smaller:

- The first person to register the OPERATOR_EMAIL address becomes the Operator (PUR-R04). Register it right after first start.
- No failed-login limit (PUR-Q05) and no kiosk lockout (AXS-Q04). Every scan is logged.
- Our three services share one site for SameSite purposes (ADR-0009).
- A revoke that got no answer leaves the old code working until Retry succeeds (PUR-Q12).

## Consequences

- Good: v1 ships without an email service, a session store, staff accounts or a card processor, and each gap is written down with its limit.
- Bad: each row is a real exposure. Revisit a row when its trigger arrives: public deployment (1, 4), email (2, 3), real money (5), a real lock (3).

## Alternatives considered

- **Server-side sessions with revocation** (row 1): a session table and a lookup per request.
- **Confirmation email** (row 2): needs an email service and a pending-account state (PUR-Q04).
- **Member login on the e-ticket** (row 3): needs identity in Access (ADR-0002).
- **Named Staff and operator accounts** (row 4): needs an Identity context (ADR-0002).
- **A real processor in test mode** (row 5): external keys, network and webhooks (ADR-0018).

## Rules and decisions

- Rules: PUR-R01, PUR-R02, PUR-R03, PUR-R04, PUR-R05, PMT-R08, PMT-R09, PMT-R13, PMT-R17, AXS-R09, AXS-R11, AXS-R15.
- Questions: PUR-Q04, PUR-Q05, PUR-Q12, PMT-Q05, AXS-Q04.
- Decisions: D15, D16, D17.
- Related: ADR-0008, ADR-0009, ADR-0018, ADR-0019, ADR-0020.

## Sources

- Spacey main 5a1cf3d: seed flaws F4, F7, F8, F10, F11, F16, A6 (source inspected at 5a1cf3d).
- class PR #10 diff at d68631f: Q-ACC-1, Q-ACC-3.
- course site [syllabus site] fetched 2026-09-30: S80, S112.
