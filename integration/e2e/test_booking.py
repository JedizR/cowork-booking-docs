"""Book and pay, decline and retry, lost redirect, hold expiry, coverage skips collection."""
import re
from urllib.parse import urljoin, urlparse

from conftest import (CARD_DECLINE, PRICE, PURCHASE, TICKET_RE, at, attr, axs, book, booking, follow, new_member,
                      new_space, operator, pay, pay_session, payment_operator_page, same_instant, session_id,
                      set_plan, tags, text, ticket)


def test_happy_path_pur_r25_confirm_and_grant():
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    held = booking(a, ref)
    assert (held["status"], held["coverage"], held["agreed_price_satang"]) == ("held", "pay", PRICE)
    assert held["payment_url"] == pay_url and same_instant(held["hold_expires_at"], at(0, "10:15"))
    assert same_instant(pay_session(session_id(pay_url))["expires_at"], at(0, "10:13"))  # D12

    r = pay(a, pay_url)
    assert r.status_code == 303 and f"/bookings/{ref}/return?session_id=" in r.headers["Location"]
    page = follow(a, r)
    assert page.status_code == 200 and urlparse(page.url).path == f"/bookings/{ref}"

    b = booking(a, ref)
    assert (b["status"], b["payment_status"], b["payment_url"]) == ("confirmed", "paid", None)
    assert b["grant_status"] == "issued" and b["ticket_url"]
    code, status = ticket(b["ticket_url"])
    assert re.fullmatch(TICKET_RE, code) and status == "issued"
    assert axs("GET", f"/grants/{ref}").json()["ticket_code"] == code


def _decline_once(a, pay_url):
    r = pay(a, pay_url, CARD_DECLINE)
    assert r.status_code == 303 and urlparse(urljoin(pay_url, r.headers["Location"])).path == urlparse(pay_url).path
    page = follow(a, r)
    assert attr(page.text, "data-decline-code") == "generic_decline"


def test_decline_then_retry_pmt_r10():
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    _decline_once(a, pay_url)
    assert pay_session(session_id(pay_url))["status"] == "open"  # the session stays open
    assert booking(a, ref)["status"] == "held"

    r = pay(a, pay_url)  # retry on the same page
    assert r.status_code == 303 and f"/bookings/{ref}/return" in r.headers["Location"]
    assert follow(a, r).status_code == 200
    assert booking(a, ref)["status"] == "confirmed"


def test_decline_keeps_purchase_login_pur_r03():
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    _decline_once(a, pay_url)
    r = a.get(f"{PURCHASE}/bookings/mine", allow_redirects=False)  # same requests.Session, no new login
    assert r.status_code == 200 and ref in r.text


def test_lost_redirect_reconciled_on_next_read_pur_r24():
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    assert pay(a, pay_url).status_code == 303  # the tab closes: success_url is never called
    assert a.get(f"{PURCHASE}/bookings/{ref}").status_code == 200  # the next read reconciles
    b = booking(a, ref)
    assert (b["status"], b["payment_status"], b["grant_status"]) == ("confirmed", "paid", "issued")


def test_lost_redirect_reconciled_after_hold_lapsed_pur_r25(clock):
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    assert pay(a, pay_url).status_code == 303
    clock(at(0, "10:16"))  # past hold_expires_at 10:15, nothing read in between
    b = booking(a, ref)
    assert (b["status"], b["payment_status"], b["grant_status"]) == ("confirmed", "paid", "issued")  # not expired


def test_hold_expiry_frees_slot_pur_r24(clock):
    space = new_space(operator())
    a = new_member("a")
    ref, pay_url = book(a, space)
    clock(at(0, "10:16"))  # no payment; the hold ended at 10:15
    b = booking(a, ref)
    assert (b["status"], b["payment_status"]) == ("expired", "unpaid")
    assert pay_session(session_id(pay_url))["status"] == "expired"
    assert pay(a, pay_url).status_code == 409  # no late payment (PMT-R11)

    other = new_member("b")
    ref2, pay_url2 = book(other, space)  # the same space, start and blocks
    assert ref2 != ref and pay_url2
    assert booking(other, ref2)["status"] == "held"


def _assert_skipped_payment(m, ref, coverage, price, page_text):
    b = booking(m, ref)
    assert (b["status"], b["coverage"], b["agreed_price_satang"]) == ("confirmed", coverage, price)
    assert (b["payment_session_id"], b["payment_url"], b["payment_status"]) == (None, None, "not_required")
    assert b["hold_expires_at"] is None and b["grant_status"] == "issued" and b["ticket_url"]
    assert page_text in text(m.get(f"{PURCHASE}/bookings/{ref}").text)
    assert not tags(payment_operator_page(), "data-booking-reference", data_booking_reference=ref)


def test_plan_skips_payment_pur_r20():
    op = operator()
    space = new_space(op)
    b = new_member("b")
    set_plan(op, b.email)
    ref, pay_url = book(b, space)
    assert pay_url is None  # 303 straight to /bookings/<ref>
    _assert_skipped_payment(b, ref, "plan", PRICE, "Confirmed. Covered by your plan. No payment was taken.")


def test_free_skips_payment_pur_r20():
    space = new_space(operator(), rate=0)  # a Community Table: THB 0 per hour
    a = new_member("a")
    ref, pay_url = book(a, space)
    assert pay_url is None
    _assert_skipped_payment(a, ref, "free", 0, "Confirmed. This space is free. No payment was taken.")
