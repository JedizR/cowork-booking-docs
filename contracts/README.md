# Contracts

Cowork Booking has three service contracts. Purchase is the only caller of the other two services (ADR-0004). Each contract names one provider, who writes and maintains it, and its consumers, who review it.

| Contract | Provider | Consumer | Link | State | Evidence |
|---|---|---|---|---|---|
| purchase-payment | Payment (cowork-booking-payment) | Purchase | [CONTRACT.md](https://github.com/JedizR/cowork-booking-payment/blob/main/CONTRACT.md), [openapi.yaml](https://github.com/JedizR/cowork-booking-payment/blob/main/openapi.yaml) | agreed | Consumer-lens sign-off in REVIEW_LOG.md (M4 contract sign-off); provider tag contract-v1 |
| purchase-access | Access (cowork-booking-access) | Purchase | [CONTRACT.md](https://github.com/JedizR/cowork-booking-access/blob/main/CONTRACT.md), [openapi.yaml](https://github.com/JedizR/cowork-booking-access/blob/main/openapi.yaml) | agreed | Consumer-lens sign-off in REVIEW_LOG.md (M4 contract sign-off); provider tag contract-v1 |
| purchase-public | Purchase (cowork-booking-purchase) | Browser, e2e suite | [CONTRACT.md](https://github.com/JedizR/cowork-booking-purchase/blob/main/CONTRACT.md), [openapi.yaml](https://github.com/JedizR/cowork-booking-purchase/blob/main/openapi.yaml) | agreed | Consumer-lens sign-off in REVIEW_LOG.md (M4 contract sign-off); provider tag contract-v1 |

## Contract states

A state changes only by the step named here. Nothing else changes it.

1. **proposed**: the M2 draft (formerly in this folder). Nobody has signed it off.
2. **agreed**: in M4 a consumer-lens reviewer signs the contract off in `REVIEW_LOG.md`. Then the provider repo gets the tag `contract-v1`.
3. **verified**: in M6 the e2e suite passes against the three running services. The Evidence column then cites that run (`integration/reports/e2e.xml`).

Consumer tests that stub a provider at `payment_client.py` or `access_client.py` (M5) count as evidence toward "verified". They do not change the state.

## Where the contracts live

In M4 each contract moves beside its provider's code, as one authoritative copy (ADR-0005):

- `cowork-booking-payment/CONTRACT.md` and `openapi.yaml`: purchase-payment.
- `cowork-booking-access/CONTRACT.md` and `openapi.yaml`: purchase-access.
- `cowork-booking-purchase/CONTRACT.md` and `openapi.yaml`: purchase-public. The brief's layout names `CONTRACT.md` for Payment and Access only; Purchase gets one too, so its public contract text has a single home.

Done in M4: this index keeps links only. The Link column points at the provider repo, and the drafts that were in this folder are deleted.

## Change a contract

1. The implementer returns `CONTRACT_CHANGE_REQUEST: <repo> <section> <reason> <rule IDs>` and stops that sub-task.
2. The main agent updates `RULES.md` and `GLOSSARY.md` first, if the meaning changed.
3. The main agent updates the provider's `CONTRACT.md` and `openapi.yaml`, then tags `contract-v2`.
4. Provider and consumer are re-dispatched.
