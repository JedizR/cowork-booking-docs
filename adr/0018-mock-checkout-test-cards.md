# ADR-0018 Hosted mock checkout with test cards

## Status

Accepted, 2026-10-01

## Context

Example: Member A presses "Continue to payment" for BK-7KQ2M9. Purchase redirects the browser to Payment's /pay/ps_... The page shows "THB 450.00", BK-7KQ2M9, "Pay by 10:13" and a test-mode banner. Member A enters 4000 0000 0000 0002: the page shows generic_decline, and the session stays open. Member A enters 4242 4242 4242 4242, 12/30, CVC 123: paid, and the browser goes back to /bookings/BK-7KQ2M9/return?session_id=ps_...

- No real money moves: "No real payment or lock." [extraction site]; "No real payment or lock is connected." [contexts site].
- The call is "“Collect this agreed amount.”", and "Purchase sends": "Booking reference / Agreed amount + currency / Required mock-payment input" [extraction site].
- The product model is a hosted checkout page, like Stripe Checkout, much simpler.
- In the seed the card form sits on the booking confirmation page and pays the booking row (templates/confirmation.html:12-19). `validate_card` and its regexes check the fields. A 0-amount booking still asks for a card (seed flaw F16). The pay check-then-update is not atomic (F14). A `force_failure` test hook is open to any JSON caller (A6; app.py:957-958, 995). Source inspected at 5a1cf3d.

## Decision

- Host the checkout in Payment at GET and POST /pay/<id>. Purchase never shows a card field and never receives card data.
- Purchase creates the session with the agreed amount (Payment never re-prices), sends the browser there, and reads the session on return (D14).
- Check card fields with the seed's `validate_card` order (PMT-R08). Then let the card number alone decide the outcome. Any future expiry, any CVC:

| Card | Outcome |
|---|---|
| 4242424242424242 | succeeded |
| 4000000000000002 | declined, generic_decline |
| 4000000000009995 | declined, insufficient_funds |
| 4000000000000069 | declined, expired_card |
| 4000000000000119 | declined, processing_error |
| 4000000000005126 | succeeded; its first refund fails, later refunds succeed |
| any other valid-looking number | declined, generic_decline |

- List these cards in a test-mode banner on every hosted page.
- Keep the session open after a decline, for a retry, until expires_at. Refuse every attempt at or after expires_at (PMT-R11).
- Run each attempt in one transaction with `SELECT ... FOR UPDATE`, so a session is charged at most once (PMT-R12).
- Refuse amounts below THB 10.00 (PMT-R02). Plan and free bookings never reach Payment (PUR-R20).
- Remove `force_failure`. The only test hook left is the clock (ADR-0013).

## Consequences

- Good: e2e can drive every outcome: success, each decline, a refund failure and the Operator's retry.
- Good: a realistic journey (redirect out, redirect back, lost redirect) with no processor account, no keys and no card-industry scope.
- Bad: no Luhn check, no network authorisation, no 3-D Secure, no chargebacks (PMT-Q01).
- Bad: anyone holding a /pay/ link can pay that session (PMT-Q05).
- Bad: the refund-failure card is recognised by the stored last4 5126 (PMT-R16). That works only while no other succeeding test card ends in 5126.

## Alternatives considered

- **A real processor in test mode.** External account, keys, network access and webhooks (ADR-0004). Out of scope.
- **Card form inside Purchase.** Purchase would handle card data, and collection belongs to Payment.
- **Keep the force_failure flag.** A hidden test hook in production (seed flaw A6).
- **Always succeed.** Declines and refund failures could not be tested.

## Rules and decisions

- Rules: PMT-R02, PMT-R04, PMT-R07, PMT-R08, PMT-R09, PMT-R10, PMT-R11, PMT-R12, PMT-R16, PUR-R20, PUR-R23.
- Terms: PMT-T07, PMT-T09, PMT-T10. Questions: PMT-Q01, PMT-Q05.
- Decisions: D1, D12, D14.
- Diagrams: seq-book-pay, seq-decline-retry, seq-refund-retry. Related: ADR-0016, ADR-0020.

## Sources

- course site [extraction site] fetched 2026-09-30: E14, E34, E50.
- course site [contexts site] fetched 2026-09-30: C31.
- Spacey main 5a1cf3d: templates/confirmation.html:12-19; seed flaws F14, F16, A6 (source inspected at 5a1cf3d).
- Project team (D12, D14).
