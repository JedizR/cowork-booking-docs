# Contracts

Cowork Booking has three service contracts. Purchase is the only caller of the other two services (ADR-0004). Each contract names one provider, who writes and maintains it, and its consumers, who review it.

| Contract | Provider | Consumer | Link | State | Evidence |
|---|---|---|---|---|---|
| purchase-payment | Payment (cowork-booking-payment) | Purchase | [purchase-payment.md](purchase-payment.md), [openapi/payment.yaml](openapi/payment.yaml) | proposed | M2 draft |
| purchase-access | Access (cowork-booking-access) | Purchase | [purchase-access.md](purchase-access.md), [openapi/access.yaml](openapi/access.yaml) | proposed | M2 draft |
| purchase-public | Purchase (cowork-booking-purchase) | Browser, e2e suite | [purchase-public.md](purchase-public.md), [openapi/purchase.yaml](openapi/purchase.yaml) | proposed | M2 draft |

## Contract states

A state changes only by the step named here. Nothing else changes it.

1. **proposed**: the M2 draft in this folder. Nobody has signed it off.
2. **agreed**: in M4 a consumer-lens reviewer signs the contract off in `REVIEW_LOG.md`. Then the provider repo gets the tag `contract-v1`.
3. **verified**: in M6 the e2e suite passes against the three running services. The Evidence column then cites that run (`integration/reports/e2e.xml`).

Consumer tests that stub a provider at `payment_client.py` or `access_client.py` (M5) count as evidence toward "verified". They do not change the state.

## Where the contracts live

In M4 each contract moves beside its provider's code, as one authoritative copy (ADR-0005):

- `cowork-booking-payment/CONTRACT.md` and `openapi.yaml`: purchase-payment.
- `cowork-booking-access/CONTRACT.md` and `openapi.yaml`: purchase-access.
- `cowork-booking-purchase/openapi.yaml` and its public contract: purchase-public.

After the move, this index keeps links only. The Link column then points at the provider repo, and the drafts in this folder are deleted.

## Change a contract

1. The implementer returns `CONTRACT_CHANGE_REQUEST: <repo> <section> <reason> <rule IDs>` and stops that sub-task.
2. The main agent updates `RULES.md` and `GLOSSARY.md` first, if the meaning changed.
3. The main agent updates the provider's `CONTRACT.md` and `openapi.yaml`, then tags `contract-v2`.
4. Provider and consumer are re-dispatched.
