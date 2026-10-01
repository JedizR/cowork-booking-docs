# ADR-0010 segno draws the ticket QR

## Status

Accepted, 2026-10-01

## Context

Example: the e-ticket for BK-7KQ2M9 shows H7K3-9QXA in large text and a QR that decodes to exactly "H7K3-9QXA". A USB QR scanner at the kiosk types those 9 characters and Enter. The kiosk normalises them to H7K39QXA and finds the grant.

- The e-ticket needs a QR: two forms of one credential, like a cinema ticket.
- The stack is pinned: Python 3.12, Flask 3.1.2, gunicorn 23.0.0, psycopg[binary] 3.2.13, requests 2.32.3, pytest 8.4.2. The only new runtime dependency allowed is the pure-Python QR library `segno`, in Access.
- The seed has no QR. Its access code is plain text and never stored (seed flaw F4; app.py:970-985; source inspected at 5a1cf3d).
- A QR encoder needs error correction, masking and version selection. That is not a few lines.

## Decision

- Add `segno` to Access's `requirements.txt`, pinned with `==` like every other package. Purchase and Payment do not get it.
- Render the QR on the server as inline SVG inside the e-ticket HTML. No image file, no external QR service, no client JavaScript.
- Encode exactly the displayed ticket code, `XXXX-XXXX`, and nothing else: no URL, no ticket token, no booking reference.
- Keep both forms: the large text and the QR carry the same credential, so a Member can read it out if the scanner fails.
- Keep Jinja autoescape on in every template of all three services. segno's SVG, built from the stored ticket code, is the only output marked safe (`Markup` or the `safe` filter); free text such as display_name, note, space_name and description is always escaped.

## Consequences

- Good: pure Python with no other package, so it installs in the slim image with nothing to compile.
- Good: SVG stays sharp when the ticket is printed.
- Good: the code never leaves Access for a third party.
- Bad: one more package to pin, watch and update, in one service.
- Bad: any phone camera can read the QR. Accepted: the same code is printed beside it (ADR-0008).

## Alternatives considered

- **Another QR package.** Rejected: the project allows exactly one new runtime dependency, and `segno` needs no other package.
- **A hand-written encoder.** Hundreds of lines of error-prone code for one picture.
- **A JavaScript QR library from a CDN.** An external script, no server-side test, and a print that depends on the browser.
- **An external QR image API.** Sends every ticket code to a third party.
- **Text only.** The kiosk accepts typed codes, but the e-ticket is meant for a scanner.

## Rules and decisions

- Rules: AXS-R06, AXS-R07, AXS-R10, AXS-R12.
- Terms: AXS-T08, AXS-T09.
- Decisions: D22.
- Related: ADR-0008.

## Sources

- Spacey main 5a1cf3d: `requirements.txt` (5 entries) and seed flaw F4, app.py:970-985 (source inspected at 5a1cf3d).
- inventory/keep-delete.md: Access adapts `requirements.txt` to add `segno` (source inspected at 5a1cf3d).
- Project team (D22).
