"""Cancel variants: Member >= 24 h and < 24 h, held cancel racing payment, operator, refund failure card."""
from urllib.parse import urlparse

from conftest import (CARD_REFUND_FAILS, PRICE, PURCHASE, at, axs, book, book_and_pay, booking, cancel,
                      new_member, new_space, open_cancel, operator, pay, payment_operator_page, pmt, refund_rows,
                      session_id, tags, text, ticket, totals)


def test_member_cancel_24h_or_more_full_refund_pur_r30():
    space = new_space(operator())
    a = new_member("a")
    ref, _ = book_and_pay(a, space)  # day 2 09:00, 47 h ahead
    ticket_url = booking(a, ref)["ticket_url"]
    before = totals()
    shown, r = cancel(a, ref)
    assert shown == PRICE and urlparse(r.headers["Location"]).path == f"/bookings/{ref}"
    b = booking(a, ref)
    assert (b["status"], b["cancel_reason"], b["refund_amount_satang"]) == ("cancelled", "member_cancel", PRICE)
    assert (b["refund_status"], b["refund_attempt"], b["grant_status"]) == ("succeeded", 1, "revoked")
    assert ticket(ticket_url)[1] == "revoked"
    assert totals()["refunded"] - before["refunded"] == PRICE


def test_member_cancel_under_24h_no_refund_pur_r30():
    space = new_space(operator())
    a = new_member("a")
    ref, _ = book_and_pay(a, space, day_offset=1)  # day 1 09:00, 23 h ahead
    ticket_url = booking(a, ref)["ticket_url"]
    before = totals()
    shown, _ = cancel(a, ref)
    assert shown == 0
    b = booking(a, ref)
    assert (b["status"], b["refund_amount_satang"], b["refund_status"]) == ("cancelled", 0, "none")
    assert b["grant_status"] == "revoked"
    assert ticket(ticket_url)[1] == "revoked"
    assert totals()["refunded"] == before["refunded"]  # no POST /refunds


def test_held_cancel_racing_payment_json_pur_r31():
    """purchase-public.md section 11 / PUR-R31 row 12: nothing reads the booking in Purchase before the cancel."""
    space = new_space(operator())
    a = new_member("a")
    r = a.post(f"{PURCHASE}/api/bookings", json={"space_id": space, "start": at(2, "09:00"), "blocks": 3,
                                                "party_size": 2})
    assert r.status_code == 201, r.status_code
    ref, pay_url = r.json()["reference"], r.json()["payment_url"]
    before = totals()
    assert pay(a, pay_url).status_code == 303  # success_url never followed

    r = a.post(f"{PURCHASE}/api/bookings/{ref}/cancel", json={})
    assert r.status_code == 200, r.status_code
    b = r.json()
    assert (b["status"], b["refund_amount_satang"], b["refund_status"]) == ("cancelled", PRICE, "succeeded")
    assert (b["grant_status"], b["ticket_url"]) == ("revoked", None)  # never confirmed-without-refund
    g = axs("GET", f"/grants/{ref}").json()
    assert (g["status"], g["ticket_code"]) == ("revoked", None)  # a tombstone
    after = totals()
    assert (after["collected"] - before["collected"], after["refunded"] - before["refunded"]) == (PRICE, PRICE)


def test_held_cancel_racing_payment_form_pur_r31():
    """The form variant: the confirm screen is opened while unpaid, then the Member pays, then confirms."""
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    shown, action = open_cancel(a, ref)
    assert shown == PRICE  # "If a payment completes first, the refund is THB 450.00 (100%)."
    assert pay(a, pay_url).status_code == 303
    r = a.post(action, data={"shown_refund_satang": shown}, allow_redirects=False)
    assert r.status_code == 303 and urlparse(r.headers["Location"]).path == f"/bookings/{ref}"
    b = booking(a, ref)
    assert (b["status"], b["cancel_reason"], b["refund_amount_satang"]) == ("cancelled", "member_cancel", PRICE)
    assert (b["refund_status"], b["grant_status"]) == ("succeeded", "revoked")


def test_operator_cancel_always_full_refund_pur_r30():
    op = operator()
    space = new_space(op)
    a = new_member("a")
    ref, _ = book_and_pay(a, space, day_offset=1)  # under 24 h: a Member would get 0%
    shown, r = cancel(op, ref)
    assert shown == PRICE and urlparse(r.headers["Location"]).path == "/operator/bookings"
    b = booking(a, ref)
    assert (b["status"], b["cancel_reason"], b["refund_amount_satang"]) == ("cancelled", "operator_cancel", PRICE)
    assert (b["refund_status"], b["grant_status"]) == ("succeeded", "revoked")


def test_refund_failure_card_operator_retry_pur_r33():
    op = operator()
    space = new_space(op)
    c = new_member("c")
    before = totals()
    ref, pay_url = book_and_pay(c, space, card=CARD_REFUND_FAILS)
    shown, _ = cancel(c, ref)
    assert shown == PRICE
    b = booking(c, ref)
    assert (b["status"], b["refund_status"], b["refund_attempt"]) == ("cancelled", "failed", 1)
    assert "Refund failed. The operator will follow up." in text(c.get(f"{PURCHASE}/bookings/{ref}").text)

    html = payment_operator_page()
    assert tags(html, "data-follow-up", data_follow_up=ref) and "needs manual follow-up" in text(html)
    assert refund_rows(ref, html) == {"1": "failed"}
    flags = tags(op.get(f"{PURCHASE}/operator/bookings").text, "data-flags", data_booking_reference=ref)
    assert "refund_failed" in flags[0]["data-flags"].split()

    # Only the Operator starts attempt 2
    assert c.post(f"{PURCHASE}/bookings/{ref}/retry", allow_redirects=False).status_code == 303
    assert c.post(f"{PURCHASE}/operator/bookings/{ref}/retry", allow_redirects=False).status_code == 404
    assert (booking(c, ref)["refund_status"], booking(c, ref)["refund_attempt"]) == ("failed", 1)

    assert "Refund attempt 2 succeeded" in text(op.post(f"{PURCHASE}/operator/bookings/{ref}/retry").text)
    assert "Nothing to retry" in text(op.post(f"{PURCHASE}/operator/bookings/{ref}/retry").text)
    b = booking(c, ref)
    assert (b["refund_status"], b["refund_attempt"]) == ("succeeded", 2)

    html = payment_operator_page()
    assert not tags(html, "data-follow-up", data_follow_up=ref)
    assert refund_rows(ref, html) == {"1": "failed", "2": "succeeded"}
    # The refunded total never exceeds the amount collected (PMT-R15)
    over = pmt("POST", "/refunds", json={"payment_session_id": session_id(pay_url), "booking_reference": ref,
                                        "amount_satang": 1, "reason": "operator_cancel", "attempt": 3})
    assert over.status_code == 409 and over.json()["error"]["code"] == "refund_exceeds_collected"
    after = totals()
    assert (after["collected"] - before["collected"], after["refunded"] - before["refunded"]) == (PRICE, PRICE)
