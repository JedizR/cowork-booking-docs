# ADR-0019 Service authentication

## Status

Accepted, 2026-10-01

## Context

Example: Purchase calls POST /grants on Access with `Authorization: Bearer <ACCESS_API_TOKEN>` and gets the grant. The same request from curl with no header gets 401 and stores nothing. Staff opens /checkin; the browser asks for a user name and password; Staff types `staff` and the STAFF_PASSWORD. The Operator opens Payment's /operator with `operator` and the OPERATOR_PASSWORD. Members log in on Purchase only.

- Seed flaw F7: no route checks who is asking; space admin and unlock are anonymous. F8: the revenue dashboard is public. F10: deploy runs with the public default SECRET_KEY (app.py:20). Source inspected at 5a1cf3d.
- There is no Identity service (ADR-0002), so Payment and Access cannot check a Purchase login.
- Only Purchase calls other services (ADR-0004), so machine trust runs one way.
- The integration stack publishes ports on localhost, so the network is not a trust boundary.
- No new dependency: no JWT library.

## Decision

| Caller and surface | Mechanism | Secret | On failure |
|---|---|---|---|
| Purchase to Payment API (/payment-sessions, /refunds) | Bearer token header | PAYMENT_API_TOKEN | 401 before any validation or lookup |
| Purchase to Access API (/grants) | Bearer token header | ACCESS_API_TOKEN | 401 before any validation or lookup |
| Members and the Operator on Purchase pages and JSON API | Cookie login, `purchase_session`, 12 h | Password hash; SECRET_KEY signs the cookie | Login step (form) or 401 (JSON); 404 to a non-owner |
| Operator on Payment /operator | HTTP Basic, user `operator` | OPERATOR_PASSWORD | 401 with a Basic challenge |
| Staff on Access /checkin | HTTP Basic, user `staff` | STAFF_PASSWORD | 401 |
| Link holder on /pay/<id> and /t/<ticket_token> | The unguessable id in the URL | None | 404 for an unknown id |

- Compare every secret in constant time. For HTTP Basic only the password is checked; the user names are what the READMEs tell people to type.
- Refuse to start when a token or password is unset or empty.
- Let tokens flow one way: Purchase holds both; each provider holds only its own.
- Keep secrets in env. Commit only `.env.example`, with placeholders.
- Leave /health open. /_test/clock answers 404 unless the test flag is on (ADR-0013).

## Consequences

- Good: no dependency, and every failure case is a simple 401 test.
- Good: a leaked Access token cannot touch Payment, and neither token can act as a Member.
- Bad: static tokens. Rotating one means redeploying the provider and Purchase together; calls in between get 401, and Purchase shows its pending or "try again" states.
- Bad: no per-person identity for Staff or the Operator on Payment and Access, and HTTP Basic has no logout (ADR-0016).
- Bad: over plain HTTP these secrets travel in clear. Use https outside localhost (PUBLIC_URL).
- Bad: the Operator has two logins, Purchase and Payment.

## Alternatives considered

- **Mutual TLS.** Certificates and infrastructure for three local containers.
- **JWTs signed by Purchase.** A library or hand-written crypto, plus key distribution.
- **OAuth client credentials.** Needs an authorisation server, a fourth service.
- **Trust the Docker network.** Rejected: ports are published on localhost.
- **Purchase's login cookie on Payment and Access.** Shares SECRET_KEY across services and couples them.

## Rules and decisions

- Rules: PMT-R01, AXS-R04, PMT-R17, AXS-R11, PUR-R02, PUR-R03, PUR-R04, PUR-R05, PUR-R06, PUR-R35, PMT-R07, AXS-R09.
- Terms: PUR-T02, PMT-T17, AXS-T14, AXS-T19.
- Decisions: D13, D15, D17, D28.
- Related: ADR-0002, ADR-0004, ADR-0009, ADR-0016.

## Sources

- Spacey main 5a1cf3d: seed flaws F7, F8, F10 (source inspected at 5a1cf3d).
- class PR #10 discussion: account data on Member in Purchase (course instructor).
- Project team (D15, D17).
