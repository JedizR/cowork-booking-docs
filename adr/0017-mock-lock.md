# ADR-0017 The lock is mocked

## Status

Accepted, 2026-10-01

## Context

Example: at 2026-10-07 09:05 Staff scans H7K3-9QXA at the Meeting Room A kiosk. The kiosk shows "ok — Door unlocked (mock)", logs the scan and sets the grant to checked_in. No door moved. The log proves a valid code was scanned at the right room inside its window. It does not prove anyone entered.

- The course keeps the lock mocked: "Proposed internal calls. Payments and locks remain mocked." and "Current-code baseline: e734fc7. No real payment or lock." [extraction site]; "No real payment or lock is connected." [contexts site].
- It separates three facts: "A stored grant does not by itself prove that a door can be opened." [extraction site] and "Payment success ≠ access provisioned ≠ a successful door opening." [contexts site].
- The syllabus pictures real locks later: "Paying members find a space, book it, pay, and enter through API-driven locks." [syllabus site].
- The seed has no lock. Unlock returns a new random code, stores nothing, and ignores the booking time (seed flaws F4 and A2; app.py:970-985). Source inspected at 5a1cf3d.

## Decision

- Mock the lock. An ok scan shows "Door unlocked (mock)" and calls nothing.
- Keep three facts apart and name them: paid (Payment), grant issued (Access), check-in ok (a scan row in Access). None implies the next.
- Store the grant as issued, checked_in or revoked. checked_in means "an ok scan was logged". Derive not yet valid, expired and no-show on read; never store them.
- Never write "entered" or "door opened" on a page or report without "(mock)".
- Build the kiosk room list from the grants' space_id and space_name, not from a door registry.

## Consequences

- Good: check-in is testable end to end, with no hardware: before, inside and after the window, wrong room, revoked, unknown code.
- Good: labels stay honest; nobody reads a scan log as an entry log.
- Bad: no evidence of physical entry. A no-show means "no ok scan", not "nobody came" (AXS-Q06).
- Bad: a real lock needs a call out of Access, which ADR-0004 and AXS-R04 forbid today. That change needs a new ADR, a lock contract, a door per space (PUR-Q06) and rules for lock failure (AXS-Q02).

## Future path to a real lock

1. Map each space to a door (PUR-Q06).
2. Add one lock client module to Access, the only place that calls the lock.
3. On an ok scan, call the lock with the door and the code; store the lock's answer on the scan, apart from the check-in result.
4. Amend ADR-0004: Access then calls the lock, and still never calls Purchase or Payment.

## Alternatives considered

- **Simulate a door** (open, closed, jammed states). Theatre: it adds states with no real evidence behind them.
- **Integrate a lock vendor's API now.** No lock, no vendor, out of scope.
- **No check-in at all.** The course expects Access to check "subject, door, time and revocation" [contexts site].

## Rules and decisions

- Rules: AXS-R04, AXS-R13, AXS-R14, AXS-R15, AXS-R16, AXS-R17.
- Terms: AXS-T05, AXS-T16, AXS-T17. Questions: PUR-Q06, AXS-Q02, AXS-Q06.
- Decisions: D20, D21.
- Diagram: seq-checkin. Related: ADR-0004, ADR-0008.

## Sources

- course site [extraction site] fetched 2026-09-30: E17, E46, E50.
- course site [contexts site] fetched 2026-09-30: C20, C29, C31.
- course site [syllabus site] fetched 2026-09-30: S08.
- Spacey main 5a1cf3d: seed flaws F4 and A2, app.py:970-985 (source inspected at 5a1cf3d).
