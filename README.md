# Cowork Booking — docs

Business rules, glossary, product and architecture docs for Cowork Booking, a co-working room booking product built as three services:

| Context | Repo | Owns |
|---|---|---|
| Purchase | `cowork-booking-purchase` | members, spaces, availability, bookings, price, coverage, cancellation |
| Payment | `cowork-booking-payment` | hosted mock checkout, payment outcomes, refunds |
| Access | `cowork-booking-access` | access grants, e-tickets, check-in kiosk |

This repo is the single home for rules and decisions. Service contracts live beside each provider's code.

## Checks

```bash
python3 scripts/check_docs.py
for f in diagrams/*.mmd; do npx -y @mermaid-js/mermaid-cli@11 -p diagrams/puppeteer.json -i "$f" -o "${f%.mmd}.svg"; done
```
