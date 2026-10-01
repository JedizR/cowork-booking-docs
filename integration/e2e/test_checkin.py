"""Kiosk: before, inside and after the window, wrong room, revoked, unknown code, booking reference.
Free spaces keep these tests independent of Payment: the booking is confirmed and the grant issued at once."""
from conftest import at, book, booking, cancel, kiosk, new_member, new_space, operator, scan, ticket

# day 0 12:00-13:00 (2 blocks), booked at 10:00


def _free_booking(op=None, member=None):
    space = new_space(op or operator(), rate=0)
    a = member or new_member("a")
    ref, _ = book(a, space, day_offset=0, start="12:00", blocks=2)
    b = booking(a, ref)
    assert b["grant_status"] == "issued", b
    return space, a, ref, b["ticket_url"]


def test_checkin_window_axs_r13(clock):
    space, _, _, url = _free_booking()
    code, _ = ticket(url)
    k = kiosk(space)
    clock(at(0, "11:59"))
    assert scan(k, code) == "not_open_yet"
    clock(at(0, "12:00"))
    assert scan(k, code) == "ok"
    assert ticket(url)[1] == "checked_in"
    clock(at(0, "12:30"))
    assert scan(k, code) == "ok"  # re-entry inside the window
    clock(at(0, "13:00"))  # valid_until is exclusive
    assert scan(k, code) == "closed"


def test_checkin_wrong_room_axs_r14(clock):
    op = operator()
    a = new_member("a")
    _, _, _, url = _free_booking(op, a)
    other_space, _, _, _ = _free_booking(op, a)  # a grant in a second space, so Staff can select that room
    clock(at(0, "12:00"))
    assert scan(kiosk(other_space), ticket(url)[0]) == "wrong_room"


def test_checkin_revoked_axs_r14(clock):
    space, a, ref, url = _free_booking()
    k = kiosk(space)
    shown, _ = cancel(a, ref)
    assert shown == 0  # free: "No payment was taken"
    assert ticket(url)[1] == "revoked"
    clock(at(0, "12:00"))
    assert scan(k, ticket(url)[0]) == "revoked"


def test_checkin_unknown_code_and_booking_reference_axs_r08(clock):
    space, _, ref, _ = _free_booking()
    k = kiosk(space)
    clock(at(0, "12:00"))  # inside the window, so only the code itself can refuse
    assert scan(k, "0000-0000") == "unknown_code"  # 0 is not in the code alphabet
    assert scan(k, ref) == "unknown_code"  # BK-XXXXXX as shown on the ticket
    assert scan(k, ref.replace("-", "")) == "unknown_code"
