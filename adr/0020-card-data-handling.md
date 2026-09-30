# ADR-0020 Card data handling

## Status

Accepted, 2026-10-01

## Context

Example: Member A pays BK-7KQ2M9 with 4242 4242 4242 4242, 12/30, CVC 123. Payment stores one attempt row: brand visa, last4 4242, outcome succeeded. The access log line shows `POST /pay/ps_...` and the status, with no query string and no body. The operator page shows visa and 4242. Nothing else about the card exists anywhere.

- The page is a mock, but a Member may still type a real card number. Treat every card field as real.
- In the seed, card_last4 sits on the booking row beside price and paid: "Booking record": "price · paid · card_last4" [extraction site]. GET /bookings returns it to anyone (seed flaw F7, app.py:891-900), and cancel deletes it (F5). Source inspected at 5a1cf3d.
- The seed's `gunicorn.conf.py` logs the path without the query string and drops the referer, because "the door access code arrives as ?code=..." (gunicorn.conf.py:4-5). Source inspected at 5a1cf3d.
- The seed reflects `?error=` text into pages (F12). Source inspected at 5a1cf3d.

## Decision

- Store only the card brand and last4, on the payment attempt row in Payment.
- Never store, log, flash or put in a URL the full number, the expiry or the CVC.
- Send card fields only in the POST body of /pay/<id>, never in a query string.
- After a validation error or a decline, show the form with empty card fields.
- Keep the seed's gunicorn access-log format (path without query string, no referer) in all three services.
- Log no request bodies. Put no form data into exception messages or flashed text.
- Keep card data inside Payment. Purchase gets the payment status and amount; Access gets nothing about payment.
- Show only brand and last4 on the operator page.
- Check it in tests: after a paid attempt, no stored column holds the full number or the CVC.

## Consequences

- Good: a leak of Payment's database or of any log exposes no usable card.
- Good: card data never crosses a service boundary.
- Good: the refund-failure test card is recognised by its stored last4, 5126, without keeping the number (PMT-R16).
- Bad: no card fingerprint. Two cards with the same brand and last4 look the same.
- Bad: support sees only brand and last4 when a Member asks about a payment.
- Bad: this is not a card-industry compliance claim. A real processor would tokenise the card in the browser (PMT-Q01).

## Alternatives considered

- **Store nothing about the card.** The Operator could not match attempts, and the refund-failure card could not be recognised.
- **Store the full number, encrypted.** Key management and compliance scope, for no use in a mock.
- **Tokenise through a real processor.** Out of scope (ADR-0018).
- **Log full requests for debugging.** Would leak card data into logs.

## Rules and decisions

- Rules: PMT-R08, PMT-R13, PMT-R16, PMT-R17, PMT-R19, PUR-R36.
- Terms: PMT-T08, PMT-T11. Question: PMT-Q01.
- Decisions: D28.
- Related: ADR-0016, ADR-0018.

## Sources

- course site [extraction site] fetched 2026-09-30: E08.
- Spacey main 5a1cf3d: gunicorn.conf.py:4-5; seed flaws F5, F7, F12 (source inspected at 5a1cf3d).
- Project team (D28).
