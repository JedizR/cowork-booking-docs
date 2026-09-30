# ADR-0012 One fixed UTC+7 offset

## Status

Accepted, 2026-10-01

## Context

Example: on the form Member A picks 2026-10-07 and the 09:00 block. The server builds 2026-10-07T09:00:00+07:00 and stores it as timestamptz. Over JSON, "2026-10-07T09:00:00+07:00" is accepted and "2026-10-07T09:00:00" gets 400. Every page shows "2026-10-07 09:00".

- The seed has a fixed-offset `LOCAL_TZ` (app.py:188). Source inspected at 5a1cf3d.
- Seed flaw A7: the form reads a naive time as Bangkok time, but the JSON API rejects it (app.py:149-150 against 198-199). Seed flaw F1: any instant is accepted. Source inspected at 5a1cf3d.
- Class rules PR #9 (at 9afd71f), TIM-R01: "The two inputs do not agree what a time with no timezone means." (known conflict K7).
- The course assumes one zone: "Shared time zone assumed." [contexts site].
- Bangkok has no daylight saving, so a fixed offset is exact.
- `zoneinfo` would need a tz database, and the `tzdata` package is not in the pinned stack.

## Decision

- Use one constant in every service: UTC+7 as `timezone(timedelta(hours=7))`. No `zoneinfo`.
- Store every instant as timestamptz.
- Require ISO 8601 with an offset in JSON: Purchase's `start`, Payment's `expires_at`, Access's `valid_from` and `valid_until`. A naive time gets 400.
- Never send a time string from the form. It sends a date and a start block (`start=HH:MM`); the server builds the instant.
- Show every time as Bangkok time ("2026-10-07 09:00"). Return ISO with +07:00 in JSON.
- Count business days as Bangkok dates: opening hours, the 30-day horizon, the dashboard's 7 days, the card expiry month.

## Consequences

- Good: exact for a business in Bangkok, with no dependency.
- Good: one input means one instant on both channels; TIM-R01's conflict is gone.
- Bad: a space in another zone, or in a zone with daylight saving, needs `zoneinfo` and a zone per space.
- Bad: a Member abroad sees Bangkok time and converts in their head.

## Alternatives considered

- **`zoneinfo` with "Asia/Bangkok".** Correct everywhere, but adds a tz database dependency for no gain today.
- **UTC in the interface.** Members think in local time; every screen would need converting.
- **Naive local times** (the seed's form). Ambiguous across channels; the source of A7.

## Rules and decisions

- Rules: PUR-R07, PUR-R08, PUR-R10, PUR-R13, PUR-R34, PMT-R02, PMT-R08, AXS-R03, AXS-R13.
- Term: PUR-T08.
- Decisions: D2, D3, D5, D24.
- Related: ADR-0013.

## Sources

- Spacey main 5a1cf3d: app.py:188 `LOCAL_TZ`; seed flaws A7 and F1 (source inspected at 5a1cf3d).
- class PR #9 diff at 9afd71f: TIM-R01.
- course site [contexts site] fetched 2026-09-30: C31.
- Project team (D2).
