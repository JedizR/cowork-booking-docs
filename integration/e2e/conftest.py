"""Shared helpers for the e2e suite.

Every call follows the contracts: purchase-public.md, purchase-payment.md and purchase-access.md.
The stack is shared and never reset, so each test makes its own Members and its own spaces
(unique names), and shared totals are asserted as before-and-after deltas.
"""
import functools
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pytest
import requests

# --- settings: dev defaults (the compose defaults) < integration/.env < the environment ---------

_DEFAULTS = {
    "PURCHASE_URL": "http://localhost:8001",
    "PAYMENT_URL": "http://localhost:8002",
    "ACCESS_URL": "http://localhost:8003",
    "PAYMENT_API_TOKEN": "dev-payment-api-token-0123456789abcdef",
    "ACCESS_API_TOKEN": "dev-access-api-token-0123456789abcdef",
    "OPERATOR_EMAIL": "operator@example.com",
    "OPERATOR_PASSWORD": "dev-operator-password",
    "STAFF_PASSWORD": "dev-staff-password",
    "E2E_OPERATOR_PASSWORD": "dev-operator-login",
}


def _settings():
    vals = dict(_DEFAULTS)
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            key, sep, value = line.partition("=")
            value = value.strip().strip("'\"")
            if sep and key.strip() in vals and value:
                vals[key.strip()] = value
    vals.update({k: os.environ[k] for k in vals if os.environ.get(k)})
    return vals


_S = _settings()
PURCHASE, PAYMENT, ACCESS = _S["PURCHASE_URL"], _S["PAYMENT_URL"], _S["ACCESS_URL"]
OPERATOR_EMAIL = _S["OPERATOR_EMAIL"]
PASSWORD = "correct-horse-battery"

CARD_OK = "4242424242424242"
CARD_DECLINE = "4000000000000002"
CARD_REFUND_FAILS = "4000000000005126"  # pays; the first refund fails, later ones succeed (PMT-R16)
TICKET_RE = r"[23456789ABCDEFGHJKMNPQRSTVWXYZ]{4}-[23456789ABCDEFGHJKMNPQRSTVWXYZ]{4}"
PRICE = 45000  # a 300 THB/h space, 3 blocks

# --- time: "day 0" is 4 days after the real Bangkok date (2026-10-05 when run on 2026-10-01) ----

BKK = timezone(timedelta(hours=7))
_DAY0 = datetime.now(BKK).date() + timedelta(days=4)


def day(n):
    return (_DAY0 + timedelta(days=n)).isoformat()


def at(n, hhmm):
    return f"{day(n)}T{hhmm}:00+07:00"


NOW = at(0, "10:00")


def same_instant(a, b):
    return datetime.fromisoformat(a) == datetime.fromisoformat(b)  # every test starts here; bookings on day 2 are 47 h ahead


def set_clock(now):
    """The same instant on all three services (PUR-R38, PMT-R20, AXS-R19); None clears it."""
    for base in (PURCHASE, PAYMENT, ACCESS):
        r = requests.post(f"{base}/_test/clock", json={"now": now}, timeout=10)
        assert r.status_code == 200, f"{base}/_test/clock -> {r.status_code}: was compose.e2e.yaml used?"


@pytest.fixture(autouse=True)
def clock():
    """Sets NOW before any login of the test; tests call clock(at(...)) to move it; reset after."""
    set_clock(NOW)
    yield set_clock
    set_clock(None)


# --- HTML: markers are data- attributes; texts are matched on the tag-free page text ------------

class _Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        self.found.append(dict(attrs))


def tags(html, /, *has, **eq):
    """Attribute dicts of every tag that has all `has` attributes and the `eq` values
    (keyword underscores mean hyphens: data_booking_reference="BK-..." )."""
    p = _Tags()
    p.feed(html)
    eq = {k.replace("_", "-"): v for k, v in eq.items()}
    return [t for t in p.found if all(h in t for h in has) and all(t.get(k) == v for k, v in eq.items())]


def attr(html, key, /, **eq):
    hit = tags(html, key, **eq)
    return hit[0][key] if hit else None


def text(html):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())


# --- Purchase: members, operator, spaces, bookings ---------------------------------------------

def _login(s, email, password):
    r = s.post(f"{PURCHASE}/login", data={"email": email, "password": password}, allow_redirects=False)
    return r.status_code == 303 and urlparse(r.headers["Location"]).path != "/login"


def new_member(tag="m"):
    """A fresh Member, registered and logged in at the current test clock."""
    s = requests.Session()
    s.email = f"{tag}-{uuid.uuid4().hex}@example.com"
    r = s.post(f"{PURCHASE}/register", data={"email": s.email, "display_name": "E2E Member", "password": PASSWORD},
               allow_redirects=False)
    assert r.status_code == 303 and urlparse(r.headers["Location"]).path == "/login", r.status_code
    assert _login(s, s.email, PASSWORD)
    return s


@functools.cache
def _register_operator():
    # "Email already registered" on a reused stack is fine: the login below decides
    requests.post(f"{PURCHASE}/register", allow_redirects=False, data={
        "email": OPERATOR_EMAIL, "display_name": "Operator", "password": _S["E2E_OPERATOR_PASSWORD"]})


def operator():
    """The Operator (OPERATOR_EMAIL), logged in at the current test clock (PUR-R04)."""
    _register_operator()
    s = requests.Session()
    if not _login(s, OPERATOR_EMAIL, _S["E2E_OPERATOR_PASSWORD"]):
        pytest.exit("OPERATOR_EMAIL is registered with another password: remove the e2e volumes "
                    "(docker compose -f compose.yaml -f compose.e2e.yaml down -v)")
    return s


def new_space(op, rate=300, capacity=6):
    """A uniquely named space, so no two tests or runs share a slot. Returns its space_id."""
    name = f"E2E {uuid.uuid4().hex[:12]}"
    r = op.post(f"{PURCHASE}/operator/spaces", data={"name": name, "capacity": capacity, "hourly_rate": rate},
                allow_redirects=False)
    assert r.status_code == 303, r.status_code
    spaces = requests.get(f"{PURCHASE}/api/spaces", timeout=10).json()["spaces"]
    ids = [sp["space_id"] for sp in spaces if sp["name"] == name]
    assert ids, f"space {name} not in GET /api/spaces"
    return ids[0]


def set_plan(op, email, on=True):
    page = op.get(f"{PURCHASE}/operator/members").text
    action = attr(page, "action", data_member_email=email)
    assert action, f"no plan form for {email}"
    r = op.post(urljoin(PURCHASE, action), data={"plan_active": "true" if on else "false"}, allow_redirects=False)
    assert r.status_code == 303
    assert attr(op.get(f"{PURCHASE}/operator/members").text, "data-plan-active", data_member_email=email) == str(on).lower()


def book(s, space_id, day_offset=2, start="09:00", blocks=3, party_size=2):
    """Book by the form (PUR-R21). Returns (ref, hosted page url) for pay, (ref, None) for plan or free."""
    r = s.post(f"{PURCHASE}/spaces/{space_id}/book", allow_redirects=False, data={
        "date": day(day_offset), "start": start, "blocks": blocks, "party_size": party_size, "note": "e2e"})
    assert r.status_code == 303, r.status_code
    loc = urljoin(r.url, r.headers["Location"])
    if "/pay/" in loc:
        return pay_session(session_id(loc))["booking_reference"], loc
    m = re.fullmatch(r"/bookings/(BK-[A-Z0-9]{6})", urlparse(loc).path)
    assert m, f"booking refused, redirected to {loc}: {text(s.get(loc).text)[:300]}"
    return m.group(1), None


def booking(s, ref):
    """GET /api/bookings/<ref>. Note: it reconciles a held booking (PUR-R24)."""
    r = s.get(f"{PURCHASE}/api/bookings/{ref}")
    assert r.status_code == 200, r.status_code
    return r.json()


def book_and_pay(s, space_id, card=CARD_OK, **kw):
    ref, pay_url = book(s, space_id, **kw)
    r = pay(s, pay_url, card)
    assert r.status_code == 303 and f"/bookings/{ref}/return" in r.headers["Location"], r.status_code
    assert follow(s, r).status_code == 200
    b = booking(s, ref)
    assert (b["status"], b["payment_status"], b["grant_status"]) == ("confirmed", "paid", "issued"), b
    return ref, pay_url


def open_cancel(s, ref):
    """The confirm screen: returns (shown_refund_satang, the form's absolute action url)."""
    screen = s.get(f"{PURCHASE}/bookings/{ref}/cancel")
    assert screen.status_code == 200, screen.status_code
    shown = attr(screen.text, "value", name="shown_refund_satang")
    action = next(t["action"] for t in tags(screen.text, "action") if t["action"].endswith(f"/{ref}/cancel"))
    return int(shown), urljoin(screen.url, action)


def cancel(s, ref):
    """Cancel through the confirm screen, as a browser does (PUR-R30). Returns (shown, 303 response)."""
    shown, action = open_cancel(s, ref)
    r = s.post(action, data={"shown_refund_satang": shown}, allow_redirects=False)
    assert r.status_code == 303, r.status_code
    return shown, r


def follow(s, r):
    return s.get(urljoin(r.url, r.headers["Location"]))


# --- Payment: hosted page, API, operator page ---------------------------------------------------

def session_id(pay_url):
    return pay_url.rsplit("/pay/", 1)[1]


def pay(s, pay_url, card=CARD_OK):
    """POST the hosted page form; the 303 is returned, never followed."""
    return s.post(pay_url, data={"card_number": card, "expiry": "12/30", "cvc": "123"}, allow_redirects=False)


def pmt(method, path, **kw):
    return requests.request(method, f"{PAYMENT}{path}", timeout=10,
                            headers={"Authorization": f"Bearer {_S['PAYMENT_API_TOKEN']}"}, **kw)


def pay_session(sid):
    r = pmt("GET", f"/payment-sessions/{sid}")
    assert r.status_code == 200, r.status_code
    return r.json()


def payment_operator_page():
    r = requests.get(f"{PAYMENT}/operator", auth=("operator", _S["OPERATOR_PASSWORD"]), timeout=10)
    assert r.status_code == 200, r.status_code
    return r.text


def totals():
    html = payment_operator_page()
    return {k: int(attr(html, f"data-{k}-satang")) for k in ("collected", "refunded")}


def refund_rows(ref, html=None):
    """{attempt: status} of Payment's refund rows for one booking."""
    rows = tags(html or payment_operator_page(), "data-refund-status", data_booking_reference=ref)
    return {t["data-refund-attempt"]: t["data-refund-status"] for t in rows}


# --- Access: API, e-ticket, kiosk ---------------------------------------------------------------

def axs(method, path, **kw):
    return requests.request(method, f"{ACCESS}{path}", timeout=10,
                            headers={"Authorization": f"Bearer {_S['ACCESS_API_TOKEN']}"}, **kw)


def ticket(url):
    """(data-ticket-code, data-status) of the e-ticket page."""
    r = requests.get(url, timeout=10)
    assert r.status_code == 200, r.status_code
    return attr(r.text, "data-ticket-code"), attr(r.text, "data-status")


def kiosk(space_id):
    """A Staff kiosk with its room selected (AXS-R11)."""
    k = requests.Session()
    k.auth = ("staff", _S["STAFF_PASSWORD"])
    r = k.post(f"{ACCESS}/checkin", data={"space_id": space_id})
    assert attr(r.text, "data-selected-space-id") == str(space_id), r.status_code
    return k


def scan(k, code):
    """POST a code; the 303 lands on /checkin, where the flashed data-result shows once."""
    r = k.post(f"{ACCESS}/checkin", data={"code": code})
    assert r.status_code == 200, r.status_code
    return attr(r.text, "data-result")
