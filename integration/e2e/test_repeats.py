"""Ownership and repeated requests: non-owner 404, double submit, repeat session create, repeat grant,
pay twice, cancel twice."""
from conftest import (PRICE, PURCHASE, axs, book, book_and_pay, booking, cancel, follow, new_member, new_space,
                      operator, pay, pay_session, payment_operator_page, pmt, refund_rows, session_id, tags, text,
                      ticket, totals)


def test_non_owner_gets_404_pur_r05():
    space = new_space(operator())
    a, b = new_member("a"), new_member("b")
    ref, _ = book(a, space)
    assert b.get(f"{PURCHASE}/bookings/{ref}").status_code == 404
    r = b.get(f"{PURCHASE}/api/bookings/{ref}")
    assert r.status_code == 404 and r.json()["error"]["code"] == "not_found"
    assert b.post(f"{PURCHASE}/api/bookings/{ref}/cancel", json={}).status_code == 404
    assert booking(a, ref)["status"] == "held"


def test_double_submit_resumes_hold_pur_r21():
    op = operator()
    space, free_space = new_space(op), new_space(op, rate=0)
    a = new_member("a")
    first = book(a, space)
    assert book(a, space) == first  # the same reference and the same hosted page
    mine = a.get(f"{PURCHASE}/api/bookings/mine").json()["bookings"]
    assert [m["reference"] for m in mine] == [first[0]]

    b = new_member("b")  # a confirmed (free) double submit answers with that booking
    ref, _ = book(b, free_space)
    assert book(b, free_space) == (ref, None)
    assert [m["reference"] for m in b.get(f"{PURCHASE}/api/bookings/mine").json()["bookings"]] == [ref]


def test_repeat_payment_session_pmt_r03():
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    sid = session_id(pay_url)
    s = pay_session(sid)
    body = {"booking_reference": ref, "amount_satang": s["amount_satang"], "currency": "THB",
            "description": "e2e repeat", "success_url": f"{PURCHASE}/bookings/{ref}/return",
            "cancel_url": f"{PURCHASE}/bookings/{ref}", "expires_at": s["expires_at"]}
    r = pmt("POST", "/payment-sessions", json={**body, "amount_satang": s["amount_satang"] - 15000})
    assert r.status_code == 409 and r.json()["error"]["code"] == "session_conflict"
    r = pmt("POST", "/payment-sessions", json=body)
    assert r.status_code == 200 and r.json()["id"] == sid
    assert pay_session(sid)["amount_satang"] == PRICE


def test_repeat_grant_same_code_axs_r01():
    space = new_space(operator(), rate=0)
    a = new_member("a")
    ref, _ = book(a, space)
    b = booking(a, ref)
    stored = axs("GET", f"/grants/{ref}").json()
    body = {"booking_reference": ref, "member_ref": "e2e-repeat", "space_id": b["space_id"],
            "space_name": b["space_name"], "valid_from": b["start"], "valid_until": b["end"]}
    for _ in range(2):
        r = axs("POST", "/grants", json=body)
        assert r.status_code == 200
        assert (r.json()["grant_id"], r.json()["ticket_code"]) == (stored["grant_id"], stored["ticket_code"])
    assert ticket(b["ticket_url"])[0] == stored["ticket_code"]


def test_pay_twice_charges_once_pmt_r12():
    space = new_space(operator())
    a = new_member("a")
    before = totals()
    ref, pay_url = book(a, space)
    first = pay(a, pay_url)
    second = pay(a, pay_url)  # the session is complete: no attempt, no charge
    assert first.status_code == second.status_code == 303
    assert second.headers["Location"] == first.headers["Location"]
    attempts = tags(payment_operator_page(), "data-attempt-result", data_booking_reference=ref)
    assert [t["data-attempt-result"] for t in attempts] == ["succeeded"]
    assert totals()["collected"] - before["collected"] == PRICE
    assert follow(a, second).status_code == 200 and booking(a, ref)["status"] == "confirmed"


def test_cancel_twice_refunds_once_pmt_r14():
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book_and_pay(a, space)
    before = totals()
    cancel(a, ref)
    r = a.post(f"{PURCHASE}/bookings/{ref}/cancel", data={"shown_refund_satang": PRICE})
    assert "This booking is already cancelled" in text(r.text)
    r = a.post(f"{PURCHASE}/api/bookings/{ref}/cancel", json={})
    assert r.status_code == 200 and (r.json()["refund_status"], r.json()["refund_attempt"]) == ("succeeded", 1)
    repeat = pmt("POST", "/refunds", json={"payment_session_id": session_id(pay_url), "booking_reference": ref,
                                          "amount_satang": PRICE, "reason": "member_cancel", "attempt": 1})
    assert repeat.status_code == 200 and repeat.json()["status"] == "succeeded"  # the stored result
    assert refund_rows(ref) == {"1": "succeeded"}
    assert totals()["refunded"] - before["refunded"] == PRICE
