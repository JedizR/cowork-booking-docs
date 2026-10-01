---
version: 1.0
name: Cowork-Booking-design-system
description: A quiet black-and-white product UI for booking rooms by the half hour. White canvas, parchment and near-black surfaces, Inter type with tight display tracking, one solid ink pill as the action, and status shown by fill (solid, outline, grey) plus words, never by hue. Every state, message and next action comes from the business rules (cowork-booking-docs/RULES.md). Adapted from an analysis of Apple's web design.

colors:
  black: "#000000"            # global nav, kiosk bar, kiosk "ok" result
  ink: "#1d1d1f"              # all text on light; the one action fill; selected states
  ink-hover: "#333336"        # hover on ink fills
  ink-80: "#333336"           # secondary text on grey fills
  muted: "#6e6e73"            # muted text: 5.07:1 on white, 4.66:1 on parchment
  muted-48: "#7a7a7a"         # disabled text and >= 18px text only (4.29:1)
  field-border: "#86868b"     # edges of inputs and controls: 3.62:1 non-text contrast
  fill-strong: "#d2d2d7"
  fill: "#e8e8ed"             # grey status fill, tracks, disabled buttons
  hairline: "#e0e0e0"         # card, table and list borders
  divider-soft: "#f0f0f0"     # row dividers
  canvas: "#ffffff"
  parchment: "#f5f5f7"        # alternate surface, summaries, flashes, footer
  pearl: "#fafafc"            # hover rows, quiet fills
  tile-dark: "#1d1d1f"        # inverse sections and strong alerts
  tile-dark-2: "#272729"      # a second dark tile stacked under the first
  on-dark: "#ffffff"
  on-dark-muted: "#a1a1a6"    # 6.54:1 on #1d1d1f
  frost: "rgba(245,245,247,0.8)"   # sticky bars, with backdrop blur
  frost-line: "rgba(0,0,0,0.08)"

typography:
  family: "Inter (Google Fonts, opsz 14..32, weights 300/400/600/700; never 500)"
  hero:          {fontSize: 56px, fontWeight: 600, lineHeight: 1.07, letterSpacing: -0.025em}
  display:       {fontSize: 40px, fontWeight: 600, lineHeight: 1.10, letterSpacing: -0.022em}
  title:         {fontSize: 34px, fontWeight: 600, lineHeight: 1.12, letterSpacing: -0.022em}
  heading:       {fontSize: 24px, fontWeight: 600, lineHeight: 1.20, letterSpacing: -0.018em}
  tagline:       {fontSize: 21px, fontWeight: 600, lineHeight: 1.19, letterSpacing: -0.012em}
  lead:          {fontSize: 21px, fontWeight: 400, lineHeight: 1.38, letterSpacing: -0.012em}
  body:          {fontSize: 17px, fontWeight: 400, lineHeight: 1.44, letterSpacing: -0.01em}
  body-strong:   {fontSize: 17px, fontWeight: 600, lineHeight: 1.24, letterSpacing: -0.01em}
  callout:       {fontSize: 15px, fontWeight: 400, lineHeight: 1.40, letterSpacing: -0.01em}
  button:        {fontSize: 15px, fontWeight: 600, lineHeight: 1.20, letterSpacing: -0.01em}
  button-large:  {fontSize: 17px, fontWeight: 600, lineHeight: 1.20}
  caption:       {fontSize: 14px, fontWeight: 400, lineHeight: 1.43}
  caption-strong: {fontSize: 14px, fontWeight: 600, lineHeight: 1.29}
  fine-print:    {fontSize: 12px, fontWeight: 400, lineHeight: 1.33, letterSpacing: 0}
  eyebrow:       {fontSize: 12px, fontWeight: 600, letterSpacing: 0.06em, textTransform: uppercase}
  numbers:       {fontVariantNumeric: tabular-nums, use: "money, times, counts; not codes or ISO dates"}

rounded: {none: 0px, xs: 5px, sm: 8px, md: 11px, lg: 18px, pill: 9999px, full: 50%}

spacing: {sp-1: 4px, sp-2: 8px, sp-3: 12px, sp-4: 17px, sp-5: 24px, sp-6: 32px, sp-7: 48px, sp-8: 80px}

layout:
  width-app: 1120px
  width-form: 720px
  width-narrow: 440px
  gutter: {desktop: 24px, phone: 16px}
  nav-height: 52px
  control-height: 44px
  control-height-compact: 36px
  breakpoints: {small-desktop: 1068px, tablet: 833px, phone: 640px, small-phone: 419px}

motion: {duration: 160ms, easing: "cubic-bezier(0.25,0.1,0.25,1)", press: "transform: scale(0.97)"}
focus: {outline: "2px solid #000", offset: 2px, onDark: "2px solid #fff"}

components:
  topnav:            {backgroundColor: black, textColor: on-dark-muted, activeText: on-dark, height: 52px, typography: caption}
  subnav:            {backgroundColor: frost, backdropFilter: "saturate(180%) blur(20px)", height: 52px, title: tagline, sticky: top}
  button-primary:    {backgroundColor: ink, textColor: on-dark, typography: button, rounded: pill, padding: 10px 22px, minHeight: 44px}
  button-secondary:  {backgroundColor: transparent, textColor: ink, border: 1px solid ink, rounded: pill, padding: 10px 22px}
  button-neutral:    {backgroundColor: parchment, textColor: ink, rounded: pill}
  button-ghost:      {backgroundColor: transparent, textColor: ink, hover: parchment, rounded: pill}
  button-utility:    {typography: caption, rounded: sm, padding: 7px 15px, minHeight: 36px (44px on touch)}
  button-large:      {typography: button-large, padding: 14px 28px, minHeight: 52px}
  field:             {backgroundColor: canvas, border: 1px solid field-border, rounded: md, padding: 10px 14px, minHeight: 44px, typography: body}
  search:            {rounded: pill, border: "1px solid rgba(0,0,0,0.16)", paddingLeft: 44px}
  card:              {backgroundColor: canvas, border: 1px solid hairline, rounded: lg, padding: 24px, shadow: none}
  summary:           {backgroundColor: parchment, rounded: lg, padding: 24px}
  stat:              {backgroundColor: canvas, border: 1px solid hairline, rounded: lg, value: title + tabular-nums}
  space-card-cover:  {rounded: lg, aspectRatio: "4/3 (16/9 on phones)", surfaces: [parchment, tile-dark, canvas+hairline]}
  chip:              {backgroundColor: canvas, border: 1px solid hairline, rounded: pill, padding: 7px 16px, typography: caption}
  chip-selected:     {backgroundColor: ink, textColor: on-dark}
  badge-solid:       {backgroundColor: ink, textColor: on-dark, rounded: pill, height: 24px, typography: "12px/600"}
  badge-outline:     {backgroundColor: canvas, border: 1px solid ink, textColor: ink}
  badge-muted:       {backgroundColor: fill, textColor: ink-80}
  badge-attention:   {border: 1.5px solid ink, icon: "! in an ink disc"}
  flash:             {backgroundColor: parchment, rounded: md, padding: 13px 17px, typography: callout}
  flash-error:       {backgroundColor: canvas, border: 2px solid ink, fontWeight: 600}
  alert:             {border: 1px solid hairline, rounded: lg, padding: 17px 24px}
  alert-strong:      {backgroundColor: tile-dark, textColor: on-dark}
  table:             {container: "1px hairline, rounded lg", header: "12px/600 muted", rowDivider: divider-soft, rowHover: pearl}
  timeline-slot:     {height: "40px (48px on touch)", gutter: 60px, free: canvas, booked: "parchment + 8px hatch", unavailable: pearl, preview: fill, selected: ink}
  calendar-day:      {size: "44px circle", available: "ink 600", selected: "ink fill", today: "4px dot", disabled: "muted-48 400"}
  sticky-bar:        {backgroundColor: frost, backdropFilter: "saturate(180%) blur(20px)", minHeight: 64px, position: sticky bottom}
  ticket:            {backgroundColor: canvas, border: 1px solid hairline, rounded: lg, maxWidth: 400px, notch: 24px, code: "40px/700"}
  kiosk-input:       {height: 96px, border: 2px solid ink, rounded: lg, typography: "48px/600, letter-spacing 0.1em"}
  kiosk-result-ok:   {backgroundColor: black, textColor: on-dark, rounded: lg}
  kiosk-result-refusal: {backgroundColor: canvas, border: 3px solid ink, rounded: lg}
  footer:            {backgroundColor: parchment, textColor: muted, typography: fine-print, padding: "32px 0 48px"}
---

# Cowork Booking design system

Files: `style.css` (the one shared stylesheet), `preview.html` (every component and state, open it in a browser), this document.
Use: copy `style.css` into each service's `static/style.css` and link it from `base.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

The stylesheet imports Inter itself; the preconnect lines only make it faster. Class names in this document are stable: templates may rely on them.

## 1. Overview and principles

1. **UX first, and the rules decide the UX.** Every screen state, every message and every next action comes from `cowork-booking-docs/RULES.md` and the screen table in `PRD.md` section 6. If a rule names a text ("Slot just taken", "Pay by 10:13 (12 min left)"), show that text. If a rule says a button does not exist in a state (no Cancel after the start, no "Continue to payment" from the payment deadline), do not show it. Do not show a disabled button for an action the rule removes.
2. **One action per screen.** Each screen has at most one `.btn-primary`. Everything else is secondary, neutral, ghost or a link. If two actions feel equal, the screen is doing two jobs.
3. **Choose on the thing itself.** People pick time on a visual day (the timeline), dates on a month, party size with a stepper. No "pick a duration, then pick from a list of starts".
4. **Show the consequence before the commitment.** Price, refund and deadline are visible before the button that commits to them (PUR-R17, PUR-R30, PUR-R40).
5. **Plain language.** Short sentences, sentence case, one date-and-time form everywhere: "Sat 3 Oct · 09:00–11:00" (en dash, no seconds, no ISO, the range in one `.nowrap` span so it never breaks), a moment in a sentence as "Fri 2 Oct, 09:00", money as `THB 1,234.50`. No codes, no jargon, no exclamation marks. Name the thing and what to do next.
6. **Black and white.** Status is fill plus words: solid ink = done or valid; outline = waiting; grey = ended; outline with "!" = needs a person. Never use colour.
7. **Quiet chrome.** No shadows, no gradients for decoration, no borders where a surface change does the job. Whitespace is the divider.

## 2. Colors

Ink on white. The only action colour is ink (`#1d1d1f`); pure black is for the global nav, the kiosk bar and the kiosk "ok" result. Links are ink and underlined (1 px, 2 px on hover); the underline, not a hue, marks a link.

| Token | Hex | Use | Contrast |
|---|---|---|---|
| `--ink` | #1d1d1f | text, primary fill, selected | 16.8:1 on white |
| `--muted` | #6e6e73 | secondary text | 5.07 white, 4.66 parchment, 4.86 pearl |
| `--muted-48` | #7a7a7a | disabled text, text >= 18 px only | 4.29 white (fails AA for small text) |
| `--field-border` | #86868b | input, stepper, switch-off edges | 3.62 white (WCAG 1.4.11) |
| `--ink-80` | #333336 | text on `--fill` (badges, segmented) | 10.3 on #e8e8ed |
| `--on-dark-muted` | #a1a1a6 | secondary text on dark | 6.54 on #1d1d1f, 8.16 on black |
| `--hairline` / `--divider-soft` | #e0e0e0 / #f0f0f0 | decorative borders and row lines | decorative only |
| `--canvas` / `--parchment` / `--pearl` | #fff / #f5f5f7 / #fafafc | surfaces | |
| `--fill` / `--fill-strong` | #e8e8ed / #d2d2d7 | grey status, tracks, hatch | |
| `--tile-dark` / `--tile-dark-2` | #1d1d1f / #272729 | inverse tiles, `.alert-strong` | |

Do not put `--muted` text on `--fill` (4.15:1); use `--ink-80` there.

## 3. Typography

Inter, weights 300 / 400 / 600 / 700, never 500. `font-optical-sizing: auto` uses Inter Display shapes at large sizes.

| Role | Class | Size / weight / line-height / tracking |
|---|---|---|
| Hero (landing only) | `.hero-title` | 56 / 600 / 1.07 / −0.025em |
| Display (amounts, kiosk result) | `.display` | 40 / 600 / 1.10 / −0.022em |
| Page title | `h1`, `.page-title`, `.h1` | 34 / 600 / 1.12 / −0.022em |
| Section heading | `h2`, `.h2` | 24 / 600 / 1.20 / −0.018em |
| Tagline, card group title | `h3`, `.h3`, `.section-title` | 21 / 600 / 1.19 / −0.012em |
| Lead | `.lead` | 21 / 400 / 1.38, muted |
| Body | `body` | 17 / 400 / 1.44 / −0.01em |
| Callout (tables, lists, dense UI) | — | 15 / 400 / 1.40 |
| Caption | `.caption`, `.help` | 14 / 400 / 1.43 |
| Fine print | `.fine` | 12 / 400 / 1.33, muted, tracking 0 |
| Eyebrow | `.eyebrow` | 12 / 600, uppercase, +0.06em |

Rules: headlines at 600, never 700 (700 is for the ticket code, the kiosk result and the brand mark). Negative tracking only at 14 px and up. `.num` (tabular figures) on money, times and counts so columns line up; not on codes (`H7K3-9QXA`, `BK-7KQ2M9`) or ISO dates, because Inter's tabular hyphen is wide. Ticket codes use plain figures with +0.04em tracking.

## 4. Layout

- Spacing scale 4 / 8 / 12 / 17 / 24 / 32 / 48 / 80 (`--sp-1` … `--sp-8`). Card padding 24. Section gap 48. Page top padding 48, bottom 80.
- Widths: `.container` 1120 px (app pages, tables, dashboards), `.container.container-form` 720 px (booking page, cancel, forms), `.container.container-narrow` 440 px (log in, sign up). Gutter 24 px, 16 px on phones.
- Page skeleton:

```html
<header class="topnav">…</header>
<div class="subnav">…</div>               <!-- only where a section has tabs -->
<main class="page"><div class="container">
  <a class="back-link" href="/">All spaces</a>
  <header class="page-header">
    <div><p class="eyebrow">…</p><h1 class="page-title">…</h1><p class="page-subtitle">…</p></div>
    <div class="page-actions">…</div>
  </header>
  <ul class="flashes">…</ul>
  …
</div></main>
<footer class="footer"><div class="container footer-inner">…</div></footer>
```

- Primitives: `.stack` (vertical rhythm, 24 px; `.stack-sm` 12, `.stack-lg` 48), `.cluster` (wrapping row, 12 px gap), `.grid-2`, `.grid-3`, `.grid-4` (collapse 4→2 at 1068, 3→2 at 833, all→1 at 640; `.grid-4` stays 2 on phones), `.split` (main + 360 px aside, stacks at 833), `.section` / `.section-header` / `.section-title`, `.tile` / `.tile-parchment` / `.tile-dark` (full-bleed bands, radius 0, 80 px padding).

## 5. Elevation

Flat. No `box-shadow` anywhere in the system: not on cards, buttons, menus or text. Depth comes from:

1. Surface change: white → parchment → near-black.
2. A 1 px hairline on cards, tables and lists.
3. Frosted sticky bars (`.subnav`, `.sticky-bar`): parchment at 80 % with `backdrop-filter: saturate(180%) blur(20px)`, falling back to solid parchment.

## 6. Shapes

| Radius | Use |
|---|---|
| pill 9999 px | every action button, chips, search, badges, countdown, segmented control |
| 18 px (`--r-lg`) | cards, stats, summaries, tables, lists, alerts, tickets, kiosk input and results, space-card covers |
| 11 px (`--r-md`) | inputs, field groups, flashes, date tiles, timeline range ends |
| 8 px (`--r-sm`) | `.btn-utility` compact actions, ticket stamp |
| 50 % | `.btn-icon`, stepper buttons, calendar days, status icons |
| 0 | full-bleed tiles, the top and sub navs |

Press state on every pressable thing: `transform: scale(0.97)` (0.94 for small round controls, 0.99 for cards). Focus: `outline: 2px solid #000; outline-offset: 2px` (white on dark surfaces). Touch targets are at least 44 × 44 px; compact controls grow to 44 px under `(pointer: coarse)`.

## 7. Components

Each entry: purpose · anatomy · states · do / don't.

### App shell

**`.topnav`** — the global bar on every page of a service. Anatomy: `.topnav > .topnav-inner > .brand (.brand-mark + name) + nav.topnav-links (a, a[aria-current="page"]) + .topnav-right (.topnav-user + form > button.topnav-btn)`. Black, 52 px, links 14 px muted-on-dark, the current one white on a 14 % white pill. At ≤ 833 px the links move to a second, horizontally scrolling row. Do show who is logged in: the bar holds the avatar and the display name only (truncated on phones); the account menu under it says "Member A" with "a@example.com", links My bookings, and ends with Log out as a real `.btn.btn-secondary.btn-utility` in a POST form (PUR-R37). Don't put page actions here.
Logged out: links Spaces (in the first row on a tablet; on a phone ≤ 640 px the brand, which links home, stands for it); right cluster "Log in" (`.topnav-btn`) and "Sign up". Under 420 px the bar shows the first name only. `.subnav` tabs on a phone (≤ 640 px) fill the row with `space-between` and an 8 px minimum gap; under 420 px they drop to 13 px and hide a decorative `aria-hidden` arrow, so the five operator tabs fit at 375 px. Operator: an "Operator" menu with the same five short names as the operator tabs and page titles: Dashboard, Bookings, Spaces, Members and "Payments ↗" (Payment's `/operator`).

**`.subnav`** — sticky frosted bar for a section with tabs. The operator section uses the same five short labels in Purchase and Payment: Dashboard / Bookings / Spaces / Members / Payments. Anatomy: `.subnav > .subnav-inner > .subnav-title + nav.tabs`. The current tab has `aria-current="page"`. The title hides on phones, the tab gap drops to 17 px, and the row scrolls sideways: a few lines of script scroll the current tab to the middle on load, so the page you are on is always in view.

**`.page`, `.container`, `.page-header`, `.page-title`, `.page-subtitle`, `.page-actions`, `.back-link`, `.eyebrow`** — see Layout. One `.page-header` per page. The eyebrow holds a reference or category (`BK-7KQ2M9`). `.back-link` adds a left arrow; use it for the parent ("All spaces", "My bookings").

**`.footer`** — parchment, 12 px. `.footer-inner` holds a line ("Times in Bangkok (UTC+7) · prices in THB") and `.footer-links`.

### Buttons

Purpose: start an action. Anatomy: `<button class="btn btn-primary">` or `<a class="btn …">`.

| Class | Look | Use |
|---|---|---|
| `.btn.btn-primary` | ink pill, white text | the one action of the screen: "Continue to payment", "Book", "Pay THB 450.00", "Check in", "Sign up" |
| `.btn.btn-secondary` | outline pill | the alternative: "Keep booking", "Cancel booking" on the booking page, "Reconcile all held" |
| `.btn` | parchment pill | neutral actions next to content: "View e-ticket" in lists |
| `.btn.btn-ghost` | no fill until hover | "Back", low-stakes exits; never next to a bordered or filled button, where it reads as text |
| `.btn-utility` (+ any of the above) | 8 px rect, 14 px, 36 px tall | table row actions, always with chrome: `.btn.btn-secondary.btn-utility` for Retry, Reconcile, Cancel, Edit, Archive… |
| `.btn-lg` | 52 px, 17 px | the checkout Pay button, the sticky bar, the kiosk |
| `.btn-block` | full width | forms ≤ 440 px wide, phones |
| `.btn-icon` | 44 px circle | month arrows, close |

States: hover (ink → #333336; others → grey fill), active (scale 0.97), focus-visible (2 px ring), disabled (`disabled`, `aria-disabled="true"` or `.is-disabled`: grey fill, #7a7a7a text, no press). On `.tile-dark` and `.alert-strong` the primary turns white and the secondary turns white-outlined.
Do: label with the verb and object the rule names ("Continue to payment", "Cancel booking", "Log in to book"). Don't: two primaries on one screen; red or "danger" buttons; icon-only buttons without `aria-label`; a disabled button where the rule says the action does not exist.

### Forms

Purpose: collect input with the label always visible. Anatomy:

```html
<div class="field">
  <label for="email">Email</label>
  <input id="email" type="email" autocomplete="email">
  <p class="help">We never show your email to other members.</p>
</div>
<div class="field has-error">
  <label for="name">Display name</label>
  <input id="name" aria-invalid="true" aria-describedby="name-error">
  <p class="error" id="name-error">Display name must be 1 to 50 letters, digits or spaces</p>
</div>
```

- `.field` wraps `label` + one control + optional `.help` / `.error`. `.label` styles a non-`label` heading for a group; `.optional` marks optional fields ("Note · optional").
- Controls inside `.field` (input, select, textarea) and `.input` get the field look: 44 px, 11 px radius, #86868b border, 17 px text (17 px also stops iOS zoom). Hover: ink border. Focus: 2 px ring. Disabled: parchment, grey text. Error: 2 px ink border plus `.error` text with an "!" disc.
- `.form-row` puts two fields side by side (stacks at 640). `.form-actions` is the button row under a form.
- `.search`: pill input with a magnifier.
- `.field-group` + `.field-group-row`: inputs that share one outline (card number over MM/YY and CVC).
- `.stepper` (`.stepper-btn` − / number input / `.stepper-btn` +) for party size 1 to capacity (PUR-R14); disable − at 1 and + at capacity; the input stays typeable. A few lines of script move the value.
- `.switch` (`<label class="switch"><input type="checkbox" role="switch"><span class="switch-track"></span>Label</label>`): the plan toggle. Off = grey track, on = ink track. The label says the state ("Plan on for b@example.com"). Because the toggle is a POST (PUR-R37), wrap it in a form that submits on change, or use two buttons.
- `.segmented` (radios or links with `aria-current`): two to four views of the same list (Upcoming / Past). Selected = ink.
- `.check`: checkbox or radio with its label, 44 px row; native control in ink (`accent-color`).
Do: one message per field, in the rule's words; keep the field order the rule checks in (PUR-R15, PMT-R08) so the first error is at the top. Keep typed values only where the rule allows (space edits are not kept, PUR-R15; card fields come back empty, PMT-R13). Don't: placeholders as labels; red; inline validation that contradicts the server.

### Cards

- **`.card`** — white, hairline, 18 px, 24 px padding. Parts: `.card-header` (`.card-title` + `.card-meta`), `.card-footer` (actions on a divider). `.card-parchment` swaps to parchment with no border. `.card-hover` (on an `a.card`): ink border on hover, slight press.
- **`.space-card`** (Spaces page, Airbnb-style grid inside `.grid-3`). Anatomy: `a.space-card > .space-card-cover (.space-card-top: .space-card-room + .badge; .space-card-mark: <b>6</b><span>people</span>) + .space-card-body (.space-card-row: .space-card-title + .space-card-price; .space-card-meta)`. The cover is typographic, not a photo: capacity is the big number. Covers alternate parchment / dark / outlined by position; force one with `.is-dark` or `.is-outline`. Price: "THB 300 / h" and "THB 150 per 30 min" (PRD: per hour and per 30 min); a rate of 0 shows "Free". Archived spaces never appear (PUR-R16). Empty: `.empty` "No spaces to book yet."
- **`.stat`** — KPI tile: `.stat-label`, `.stat-value` (34 px tabular; a `small` unit inside), `.stat-meta`, optional `progress.progress`.
- **`.summary`** — parchment order summary: `.summary-title`, `.summary-row` (label left, value right), `.summary-total`, `.fine` for terms. Used beside the picker, on the booking and cancel pages and in checkout.

### Chips

`.chip` (pill, hairline, 14 px) for quick picks and filters; `.chip-selected`, `[aria-pressed="true"]`, `[aria-current]` or a checked inner input = ink fill. `.chip-muted` = non-interactive fact ("Room 1", "Up to 6 people"). Group in `.chip-row`. Don't use chips as primary actions.

### Badges and the status map

`.badge` + one of `.badge-solid`, `.badge-outline`, `.badge-muted`, `.badge-attention`. Always words, sentence case, 12 px / 600.

| Object (rule) | Solid · done or valid | Outline · waiting | Grey · ended | Attention · needs a person |
|---|---|---|---|---|
| Booking (PUR-R28) | Confirmed | Held · pay by 10:13 | Completed, Expired, Cancelled | Refund failed, Payment status unknown |
| Ticket / grant (AXS-R10, AXS-R16) | Issued, Checked in | Being prepared | Expired, Cancelled | Revocation pending |
| Payment session (PMT-R05) | Paid | Open | Expired | — |
| Attempt (PMT-R10) | Succeeded | — | Declined | — |
| Refund (PMT-R16, PUR-R32) | Refunded | Refund pending | No refund | Refund failed |
| Kiosk scan (AXS-R13, AXS-R14) | Door unlocked | Opens at 09:00, Wrong room | Check-in closed, Code not recognised, Cancelled | — |
| Space (PUR-R16) | Free now | — | Archived 2026-10-07, Booked now | — |

Completed is derived (confirmed and now ≥ end) and shown only on read (PUR-R28). The e-ticket badge follows the precedence Cancelled > Expired > Checked in > Issued (AXS-R10).

### Flashes and alerts

- **`.flash`** — the one-time outcome after a form redirect (PUR-R36). Render the session's flashes inside `ul.flashes` at the top of the page content. Anatomy: `li.flash > span.flash-icon + span(text)`; an optional link or `.btn` sits at the right. Variants: `.flash-success` (check: "Confirmed. Paid THB 450.00.", "Space saved"), plain `.flash` (info "i": "Please log in again"), `.flash-error` (white with 2 px ink border, "!": "Slot just taken", "Your card was declined."). Use `role="alert"` on errors and `role="status"` on the others. Never build a flash from URL text (PUR-R36).
- **`.alert`** — persistent state of the thing on the page, not the outcome of the last click: "Your e-ticket is being prepared", "Payment status unknown, refresh later. …". Anatomy: `.alert > .alert-icon + .alert-title + .alert-body + .alert-actions`.
- **`.alert-strong`** — inverse (near-black) for the one state that blocks everything else: the held-booking banner on the space page and My bookings ("You have a held booking BK-7KQ2M9, Meeting Room A 2026-10-07 09:00–10:30: pay by 10:13 or cancel it", PUR-R39) and the failed-refund notice on Payment's operator page. At most one per page.
- **`.test-banner`** — dashed box on the hosted payment page listing the test cards (PMT-R07). Inner `ul > li > code + span`.

### Tables

Anatomy: `div.table-wrap > table.table` (the wrap gives the hairline frame, the 18 px radius and horizontal scroll on narrow screens). `th` 12 px / 600 muted; `td` 15 px, no wrap by default (`td.wrap` allows wrapping, e.g. notes). Links in a table use one style, `a.cell-title` (600 ink, underline on hover): booking references, "1 upcoming". `table.table-link` makes that link cover its row, so the whole row opens the record (buttons and other links in the row stay clickable); use it on every table of bookings, on both services. `.col-num` right-aligns money and counts with tabular figures; put it on the `th` too. `.cell-sub` adds a second muted line (email under name, time under space, coverage under status). `.row-actions` right-aligns compact actions (`.btn-utility`). `tr.is-flagged` adds an ink bar on the left for rows that need a person; sort them first (All bookings: flagged first, refunds owed oldest first). Empty table: replace with `.empty`, never an empty grid.
`table.table.table-stack`: on phones (≤ 640 px) each row becomes a card instead of scrolling sideways. Line 1: the first cell, then `td.cell-status` and `td.col-num`; line 2: the other cells; line 3: `td.row-actions`. `.cell-label` adds the word a hidden header gave ("Attempt 2"). Use it on every operator table whose actions or status would otherwise sit off-screen.

### Lists

`ul.list > li.list-item` with `.date-tile` (`.date-tile-month`, `.date-tile-day`), a middle block (`.list-item-title` with a link that makes the whole row clickable, `.list-item-meta`) and `.list-item-aside` (badge + one action). `.is-past` quiets the row. Used for My bookings (upcoming by start ascending, past by start descending, PRD) and the kiosk's last scans on phones.

### Key-value

`dl.dl` with direct `dt`/`dd` pairs: muted labels left, values right, soft dividers. For booking details, payment details, member details.

### Tabs, segmented, steps

- **`.tabs`**: links or buttons, `aria-current="page"` (links) or `aria-selected="true"` (tab buttons) = ink text with a 2 px underline. Scrolls sideways on phones.
- **`.steps`**: `ol.steps > li(.is-done | .is-current[aria-current="step"]) > .steps-label + .steps-meta`. The booking journey is Held → Paid → Confirmed → Ticket ready. Plan and free bookings skip Paid (PUR-R20): show three steps, Confirmed → Ticket ready. "Ticket ready" stays current with meta "Preparing" while the grant is pending (PUR-R26).

### Progress and countdown

- **`progress.progress`**: native `<progress>`, 6 px ink bar on a grey track, with text content for old browsers.
- **`.countdown`**: pill with a live dot: `<span class="countdown" data-seconds-left="720">Pay by 10:13 <span class="countdown-left">12 min left</span></span>`. The server renders the text and `data-seconds-left` from `clock.now()`; a few lines of script count down once a second and rewrite "N min left" (N rounded up; under 60 s "less than 1 min left") (PUR-R40, PMT-R07). `.is-urgent` (inverse) from 2 min left; `.is-over` (grey, no pulse) when the deadline has passed and the page says "Time to pay has run out". At zero the script hides "Continue to payment" (booking page) or disables Pay (hosted page); the server still decides.

### Empty state

`.empty > .empty-icon(svg) + h3.empty-title + p.empty-text + one action`. Copy from the PRD: "No bookings yet" + "Browse spaces"; "No spaces to book yet."; "No spaces yet. Create one below."; "No rooms yet" (kiosk). Say what will appear here and the one next step.

## 8. Patterns

### 8.1 Booking range picker (space page, Purchase)

The core change. The person sees the day and selects a range on it, like a calendar app: no duration menu, no list of starts.

Layout: `.picker` grid. Desktop: left column `.picker-date` (month `.cal` in a card) above `.picker-details` (party size, note); right column `.picker-time` (the timeline). Phones (≤ 833 px): date, then time, then details. Under the picker a `.sticky-bar` keeps the choice, the price and the one button in view. Above the picker: `.back-link` "All spaces", the title, and `.chip-muted` facts (room number, "Up to 6 people", "THB 300 per hour").

Markup:

```html
<div class="timeline" role="group" aria-labelledby="tl-title">
  <div class="timeline-head">
    <h2 class="timeline-title" id="tl-title">Wednesday 7 October</h2>
    <p class="timeline-hint">Tap a start, then an end · 30 min to 4 h</p>
  </div>
  <div class="timeline-slots">
    <button type="button" class="slot is-unavailable" disabled aria-label="08:00 to 08:30, too soon">
      <span class="slot-time">08:00</span><span class="slot-body"><span class="slot-reason">Too soon</span></span></button>
    <button type="button" class="slot is-selected is-range-start" aria-pressed="true" data-hint="Start 09:00">
      <span class="slot-time">09:00</span><span class="slot-body"><span class="slot-label">09:00–10:30</span><span class="slot-sub">1 h 30 min</span></span></button>
    <button type="button" class="slot is-selected is-in-range" aria-pressed="true">…09:30…</button>
    <button type="button" class="slot is-selected is-range-end" aria-pressed="true">…10:00…</button>
    <button type="button" class="slot is-booked" disabled aria-label="12:00 to 12:30, booked">
      <span class="slot-time">12:00</span><span class="slot-body"><span class="slot-reason">Booked</span></span></button>
    …
    <div class="timeline-end" aria-hidden="true"><span class="slot-time">20:00</span><span class="slot-body"></span></div>
  </div>
</div>
<div class="timeline-legend" aria-hidden="true">…</div>
<input type="hidden" name="date"> <input type="hidden" name="start"> <input type="hidden" name="blocks">
```

Rules that shape it:

| Rule | In the picker |
|---|---|
| PUR-R08 opening hours 08:00–20:00 | 24 rows, 08:00 to 19:30, closed by the `.timeline-end` 20:00 line. A range can never run past 20:00, so "Runs past 20:00" never shows; a crafted post still gets the flash "Outside opening hours 08:00-20:00". |
| PUR-R09 start on :00 / :30; 1 to 8 blocks | Each row is one 30-min block. A range is 1 to 8 contiguous blocks (30 min to 4 h). The hint says so. |
| PUR-R10 ≥ 60 min ahead, ≤ 30 days out | Calendar: days before today and after today + 30 are disabled. Timeline: blocks starting before now + 60 min are `.is-unavailable` "Too soon". |
| PUR-R12 / R13 slot-blocking bookings | Blocks overlapping a confirmed or live held booking are `.is-booked` "Booked". The first reason that applies wins ("Too soon" before "Booked"). The reason shows once per run; every row keeps it in its `aria-label`. |
| PUR-R07 the form sends a date and a block | The selection fills hidden `date`, `start` (HH:MM) and `blocks`; the server contract is unchanged. |
| PUR-R17, R18 price fixed at creation, THB | The sticky bar shows `round_half_up(rate_satang × blocks / 2)` as "THB 450.00" live; the server computes the stored price. |
| PUR-R19, R20 coverage | The button is "Continue to payment" (pay), "Book" (plan or free, no Payment step); logged out it is "Log in to book" (AC1.8). Plan: the bar meta says "Covered by your plan"; free: "Free · no payment". |
| PUR-R30 refund terms | For pay: "Full refund if you cancel 24 h or more before the start; after that, no refund." in the summary, plus "Starts less than 24 h away cannot be refunded." for today and tomorrow. |
| PUR-R14 whole room, 1 to capacity | `.stepper` 1…capacity, help "You book the whole room, for 1 to 6 people." Note optional, ≤ 500 characters. |
| PUR-R39 one held booking | While the Member has a live hold, an `.alert-strong` banner sits above the picker with "Continue to payment" and Cancel; the picker stays readable. |
| PUR-R12 race | "Slot just taken" comes back as a `.flash-error` above the picker with the timeline re-read. |

Interaction (reference script in `preview.html`):

Two taps, like check-in and check-out or a round-trip flight: the first sets the start, the second the end. There is no duration menu (only the no-script fallback has one).

1. Tap a free block: it becomes the start and a 30-min range is already valid (`.is-selected.is-range-start.is-range-end`); the bar says "Now tap an end time, or keep 30 min".
2. While choosing the end, hovering a later free block previews the range (`.is-preview`, last row `.is-preview-end` "Until 10:30 · 1 h 30 min") if every block in between is free and the range is ≤ 8 blocks.
3. Tap that block: the range is set (start row shows "09:00–10:30" and the duration; middle rows `.is-in-range`; last row `.is-range-end`). Tap the start again to keep 30 min.
4. A second tap is never silently reinterpreted. Earlier than the start: it becomes the new start. Past a booked or too-soon block: a new range starts there and the bar says why next to the summary, "New range from 15:30 — 14:00–15:00 is booked". Beyond 4 h: the range keeps its start and ends at the 4 h mark, "Ends at 13:00 — 4 h is the longest booking". Tapping a free block when a range is complete starts a new range. The note shows in ink with an "i" under the bar's summary (`.sticky-bar-hint.is-info`) until the next tap.
5. The Member's own booking is booked for everyone (hatched) with an ink edge, labelled "Yours · BK-7KQ2M9", and is a link to its booking page; the legend adds "Yours" when the day has one. While the Member has a live hold (PUR-R39) the whole timeline is read-only (free rows are disabled), the Details card and the bar are not shown, and the hold banner is the one action.
6. Each free row carries `data-hint` ("Start 09:30" or "End 11:00") on the `.slot` button, shown on hover and keyboard focus. On touch (`pointer: coarse`) every free row shows its hint in muted text, so a phone user sees what the first and the second tap do.
7. Looks: free = an outlined cell (1 px `--fill-strong`, 8 px radius) with a pointer cursor, that reads as tappable time; hover and keyboard focus fill it parchment; a press fills it ink at once (`:active`, `touch-action: manipulation`), before the click lands; too soon = dotted parchment with muted times; booked = hatched; preview = flat grey; selected = one ink bar. The legend uses the same fills.
8. Keyboard: Tab reaches the timeline (one roving tab stop: the start, or the first free block); Up and Down move between free blocks, Home and End jump to the first and last; Enter or Space picks the start, then the end; Escape clears. Focus leaving the timeline drops any preview, so the bar always shows what the form sends.
9. Changing the date (calendar) reloads the timeline for that date and keeps party size and note.

States: nothing selected → bar title "Choose a time", meta "THB 150 per 30 min", button disabled; range selected → title "Wed 7 Oct · 09:00–10:30", meta "1 h 30 min · THB 450.00 · Party of 2", button enabled and booking at once (no review step: the party size is in the bar, the Details card sits beside the timeline on a desktop and under it on a phone); on a phone (≤ 640 px) Clear sits beside the summary as a small outline button and one muted line shows the hint while there is one, else the refund terms, so the bar stays short; no free block on the date → replace the timeline with `.empty` "No free time on this date" / "Every half hour is booked or too soon. Try another date." and a `.btn-secondary` for the next day.

Without script: render each free block as `<a class="slot" href="?date=2026-10-07&start=09:00">`, and, once a start is in the query, later reachable blocks as `?…&start=09:00&blocks=3`; the server re-renders the selection (a GET only reads, PUR-R37). With script, the same links are intercepted. Use the same element for every slot.

The sticky bar never hides what has focus: `html:has(.sticky-bar)` sets `scroll-padding-bottom` (the script keeps it at the bar's live height), so Tab and any scroll-into-view stop above it, and the bar sits in flow after the picker, so the Details card is always reachable.

Accessibility: each slot is a button with `aria-pressed` and an `aria-label` "09:00 to 09:30, free|booked|too soon|selected"; booked and too-soon slots are `disabled` (or `aria-disabled="true"` on links). The timeline is a `role="group"` labelled by the date heading.

### 8.2 Checkout (hosted payment page, Payment)

`.checkout` split, Stripe-style, with no global `.topnav`: the merchant row is the header, so the brand shows once. Left `.checkout-summary` (parchment): `.back-link` "Back to booking" (to cancel_url), `.checkout-merchant` (brand mark + "Cowork Booking"), `.checkout-label` "Booking BK-7KQ2M9", `.checkout-amount` "THB 450.00", a white `.summary` (space, Bangkok time, total due), then the `.countdown` "Pay by 10:13 · 12 min left" and fine print "Leaving keeps this payment open. You can come back and pay until 10:13." (PMT-R07 row 2). Right `.checkout-form`: `h2` "Pay with card", `.test-banner` with the test cards, the decline `.flash-error` when present (`data-decline-code`), `.field-group` (card number; MM/YY and CVC), `.btn-primary.btn-lg.btn-block` "Pay THB 450.00", fine print "Cowork stores only the card brand and last 4 digits."
States (PMT-R07 to R11): open; declined (flash with the reason, form empty, still open); card format errors under the field group in check order ("Card number must be 13 to 19 digits", …), the failing input with a 2 px ink edge and the group's dividers kept, plus "For your security, enter the card details again." after a server check (fields come back empty, PMT-R13); time over (countdown at zero): the form is replaced by the end panel "Time to pay has run out" with "Back to your booking"; paid ("Paid" + "Return to booking"); expired: no form, `.empty`-style panel "This payment session has expired. Nothing was charged." with "Back to your booking". Stacks on phones, summary first.

### 8.3 Booking page and confirmation (Purchase)

`.container-form`. Flashes first, then `.page-header` (eyebrow = reference, title in plain words, subtitle = space and Bangkok time, status badge in the actions slot), then `.steps`, then `.split`: a `.card` with `.dl` (space, when, check-in, party "Party of 4", note, payment "THB 450.00 paid · Visa •••• 4242", coverage) and a `.card-footer` with the one action, and a `.summary` aside with the cancellation terms worked out to a real time ("so until Tue 6 Oct, 09:00").
Say the state once. Titles by state: confirmed "You're booked." (the card says "Confirmed. Paid THB 450.00.", plan "Confirmed. Covered by your plan. No payment was taken.", free "Confirmed. This space is free. No payment was taken."); held "Finish paying by 10:13" with the countdown and "Continue to payment" (primary) + Cancel (secondary). Ended bookings (completed, expired, cancelled) title the room, show no badge and no tracker, and leave the state to one status card: cancelled "Cancelled." with the cancel time under it, then the money line and ticket line built from stored fields (AC13.12), so a cancel reads as the flash plus that card. Money aside: pay shows the price and "Total"; plan shows "Covered by your plan · no payment" with the agreed price as a footnote, free "Free · no payment"; neither ever shows a Total or "You pay THB 0.00". The held-state texts after the deadline and when Payment gives no answer come word for word from the PRD booking-page row; use `.alert` for them and remove buttons the rule removes. "View e-ticket" opens the ticket in a new tab; while the grant is pending show `.alert` "Your e-ticket is being prepared" instead. After the start: no Cancel, `.help` "This booking has started; ask the operator".

### 8.4 Cancel confirm (Purchase)

`.container-form`. Title "Cancel BK-7KQ2M9, Meeting Room A, Wed 7 Oct · 09:00–10:30", then a `.meta` row: duration, party, and the Member for an operator. A `.summary` with the refund line the rule computes ("Refund THB 450.00 (100%)", "Refund THB 0.00 (0%)", "No payment was taken", or the held-booking sentences). Then `.form-actions`: `.btn-primary` "Cancel booking" and `.btn-secondary` "Keep booking". The form carries `shown_refund_satang`. Never one-click cancel from a list (AC16.5).

### 8.5 E-ticket (Access)

Page body `.ticket-page` (parchment, centred), no navigation (AXS-R10). `article.ticket[data-status]`: `.ticket-top` (`.ticket-head`: eyebrow "Cowork · E-ticket", `h1.ticket-title` room name, status badge; `dl.ticket-meta` Date, Time, Check-in `.is-wide`), `.ticket-divider` (perforation with two notches; set `--ticket-cutout` to the page colour behind the ticket), `.ticket-body` (`.ticket-qr` with the segno SVG, `.ticket-code` "H7K3-9QXA" with `data-ticket-code`, `.ticket-hint`), `.ticket-ref` "Booking ref (not for entry)" + reference in fine print (AXS-R08). `.ticket.is-cancelled` fades the code and QR and shows `.ticket-stamp` "Cancelled" across them. Optional `.ticket-actions` with "Print ticket". Prints on one page: chrome hidden, black border, colours exact.

### 8.6 Kiosk (Access, Staff)

`body.kiosk`: `.kiosk-bar` (black: brand "Check-in", `.kiosk-room` "Room: **Meeting Room A (room 1)**", "Change room" `.topnav-btn`), `.kiosk-main` with `form.kiosk-form` (`.kiosk-label` "Enter the ticket code", `input.kiosk-input` autofocus, `autocomplete="off"`, `autocapitalize="characters"`, placeholder "XXXX-XXXX"; `.btn-primary.btn-lg.btn-block` "Check in"), the result, then `.kiosk-log` (last 10 scans, `.table`, masked codes `••••-9QXA`, HH:MM today else YYYY-MM-DD HH:MM; AXS-R15).
Result `div.kiosk-result[data-result][role="status"] > .kiosk-result-icon + .kiosk-result-title + .kiosk-result-reason`. `ok` → `.is-ok` (solid black, white check): "Door unlocked (mock)". Refusals → white with 3 px ink border and a cross, in the rule's order (AXS-R14): `unknown_code` "Code not recognised", `revoked` "Ticket cancelled", `wrong_room` "Wrong room" + "This ticket is for Focus Booth (room 2).", `not_open_yet` "Not open yet" + "Opens at 09:00", `closed` "Check-in closed at 10:30". No room selected: the room picker (`.field` select + primary "Use this room") replaces the form; "No rooms yet" is an `.empty`.

### 8.7 Dashboards (Purchase operator, Payment operator)

Operator pages sit under a `.subnav` with tabs. `.page-header` with the period ("Last 7 days, Thu 1 Oct to Wed 7 Oct (Bangkok)") and one secondary action ("Reconcile all held"). Then `.grid-4` of `.stat` tiles, then `.grid-2` of cards with `.bar-chart`, then tables.
- Purchase dashboard (PUR-R34): it leads with the day, never with a wall of zeros. Header: "Dashboard" and a `.meta` line with the date, the Bangkok time and, when nothing is flagged, "Nothing needs you right now". When something needs a person: one `.alert` ("2 bookings need a person", the counts by flag, a "Review" button). Then `.grid-2`: "Today" (the day's bookings by time, badges Now / Done / Held) and "Coming up" (the next bookings after today, grouped by day), each with a one-line empty state. Then "Last 7 days" with the period ("Fri 25 Sep to Thu 1 Oct · by start date, Bangkok", D24) over the `.stat` tiles: Bookings (by status in meta), Utilization % with a `progress`, Members who booked, Confirmed hours; every tile always shows its figure (0, "0.0%" with an empty `progress`, "0 h"), and a tile with nothing to count says why in its `.stat-meta` ("No booking started in these 7 days"). When nothing is booked today, "Today" is one full-width line ("No bookings today. Next: …") above "Coming up", never half a row of blank. Then "Bookings by status" bars (solid for confirmed and held, `.bar-muted` for expired and cancelled) and "Confirmed hours by coverage" (pay, plan, free), only when there is something to chart. No money: a fine-print line links to Payments.
- Payment operator (PMT-R17): stats Collected, Refunded, Net, Estimated commission (`.num`); `.alert-strong` for failed refunds "needs manual follow-up. Retry it from Purchase: All bookings"; tables for sessions, attempts (brand and last4 only), refunds.
- `.bar-chart` anatomy: `ul.bar-chart > li.bar-row > .bar-label + .bar-track > .bar[style="--value: 62%"] + .bar-value`. The value is always printed; the bar only supports it.

### 8.8 Empty states

Every list and table has one (see Components). Copy names what is missing and gives one next step. The timeline's empty state offers the next day.

### 8.9 Errors and flashes

- Form outcome after a POST: one `.flash` at the top (PUR-R36). Refusals use `.flash-error`, `role="alert"`.
- Field problems: `.field.has-error` + `.error` text under the field, `aria-invalid` and `aria-describedby`. Show the first failing check in rule order; don't pre-validate rules the server owns.
- Races and conflicts ("Slot just taken", "Time to pay has run out on BK-7KQ2M9; cancel it, or try again from 10:15"): `.flash-error` and the page re-read so the person sees the current state.
- Not found / no access: `.empty` with eyebrow "404", "This page does not exist", one way back. Operator pages answer a Member with this 404 (PUR-R06).

### 8.10 Countdown

See Components. One countdown per page, next to the action it limits (booking page header, checkout summary, My bookings row as a badge "Pay by 10:13"). Never count to `hold_expires_at`; count to the payment deadline, `hold_expires_at − 2 min` (PUR-R40).

## 9. Accessibility

- Contrast: all text ≥ 4.5:1 (table in section 2); control edges ≥ 3:1 (`--field-border`). Status never relies on fill alone: every badge, slot and result has words.
- Focus: visible 2 px ring with 2 px offset on every interactive element, white on dark; never removed for keyboard users.
- Targets ≥ 44 px; compact controls grow under `(pointer: coarse)`; timeline rows become 48 px on touch.
- Semantics: native buttons, links and inputs; labels tied with `for`; `aria-current` for nav and tabs; `aria-pressed` for slots, chips and calendar days; `role="switch"` on the plan toggle; `role="status"` on flashes and kiosk results, `role="alert"` on refusals; `.visually-hidden` for labels that are only visual elsewhere (table action headers).
- Live content: the countdown updates its text once a second but announce only the minute change (`aria-live="polite"` on a hidden copy, if at all); the kiosk result gets focus or `role="status"` after the redirect.
- Motion: transitions are short; `prefers-reduced-motion` removes them and the pulse. `forced-colors` adds outlines to selected states and strikes through booked slots.
- Language and time: `lang="en"`, Bangkok times everywhere with the zone stated once in the footer.

## 10. Responsive

| Width | Change |
|---|---|
| ≥ 1069 px | Desktop: 1120 px content, `.grid-4` four across. |
| ≤ 1068 px | Hero 48 px; `.grid-4` two across. |
| ≤ 833 px | Top-nav links move to a scrolling second row; `.grid-3` two across; `.split`, `.picker` and `.checkout` stack (picker order date → time → details; checkout summary first); hero 40, title 30. |
| ≤ 640 px | Phone: gutter 16; `.grid-2`/`.grid-3` one column; `.form-row` stacks; page header stacks; subnav title hides; space covers go 16:9; sticky-bar button goes full width under the summary; alert actions move under the text; kiosk bar wraps the room onto its own line; kiosk input 34 px; title 28. |
| ≤ 419 px | Small phone: the user name truncates harder. |
| pointer: coarse | 44 px minimum on utility buttons, chips, nav buttons, stepper; 48 px timeline rows. |

Tables scroll sideways inside `.table-wrap` unless they are `.table-stack` (cards on phones); never let the page scroll sideways. Short pages: `body` is a flex column and `main` grows, so the footer always sits at the bottom of the window.

## 11. Utilities

`.meta` (a row of facts with a dot in the gap: "Today · 09:00–11:00 · BK-7KQ2M9"; the row wraps without ever starting a line with "·", because the dot of a line's first item falls in a clipped strip; items are plain spans, so wrap a badge in a span; the rule sits last in style.css so its offset wins over `.page-subtitle` and `.list-item-meta`), `.muted` (muted text), `.num` (tabular figures), `.mono` (monospace for technical ids such as `ps_…`), `.nowrap`, `.caption`, `.fine`, `.eyebrow`, `.lead`, `.display`, `.hero-title`, `.h1`–`.h4`, `.divider`, `.visually-hidden`, `.no-print`, `form.inline`. Print: `@media print` hides the navs, footer, sticky bar, flashes, buttons and `.no-print`, and keeps tickets on one page with exact colours.

## 12. Class index

Shell: `topnav topnav-inner brand brand-mark topnav-links is-active topnav-right topnav-user topnav-btn subnav subnav-inner subnav-title page container container-form container-narrow page-header page-title page-subtitle page-actions back-link section section-header section-title tile tile-parchment tile-dark footer footer-inner footer-links`
Layout: `stack stack-sm stack-lg cluster grid-2 grid-3 grid-4 split`
Buttons: `btn btn-primary btn-secondary btn-ghost btn-utility btn-lg btn-block btn-icon is-disabled`
Forms: `field label optional input search help error has-error form-row form-actions check field-group field-group-row stepper stepper-btn switch switch-track segmented`
Cards: `card card-parchment card-hover card-header card-title card-meta card-footer space-card space-card-cover space-card-top space-card-room space-card-mark space-card-body space-card-row space-card-title space-card-price space-card-meta is-dark is-outline stat stat-label stat-value stat-meta summary summary-title summary-row summary-total`
Chips and badges: `chip-row chip chip-selected chip-muted badge badge-solid badge-outline badge-muted badge-attention`
Messages: `flashes flash flash-icon flash-success flash-error alert alert-icon alert-title alert-body alert-actions alert-strong test-banner`
Data: `table-wrap table col-num cell-sub row-actions wrap is-flagged list list-item list-item-title list-item-meta list-item-aside date-tile date-tile-month date-tile-day is-past dl tabs empty empty-icon empty-title empty-text progress countdown countdown-left is-urgent is-over steps steps-label steps-meta is-done is-current bar-chart bar-row bar-label bar-track bar bar-muted bar-value`
Calendar: `cal cal-header cal-title cal-nav cal-grid cal-dow cal-day is-today is-selected is-outside`
Range picker: `picker picker-date picker-time picker-details timeline timeline-head timeline-title timeline-hint timeline-slots slot slot-time slot-body slot-label slot-sub slot-reason is-booked is-unavailable is-selected is-in-range is-range-start is-range-end is-preview is-preview-end timeline-end timeline-legend legend-item legend-swatch sticky-bar sticky-bar-inner sticky-bar-summary sticky-bar-title sticky-bar-meta sticky-bar-actions`
Checkout: `checkout checkout-summary checkout-form checkout-merchant checkout-label checkout-amount`
Ticket: `ticket-page ticket ticket-top ticket-head ticket-title ticket-meta is-wide ticket-divider ticket-body ticket-qr ticket-code ticket-hint ticket-ref ticket-stamp is-cancelled ticket-actions`
Kiosk: `kiosk kiosk-bar kiosk-bar-inner kiosk-room kiosk-main kiosk-form kiosk-label kiosk-input kiosk-result is-ok kiosk-result-icon kiosk-result-title kiosk-result-reason kiosk-log`
Utilities: `meta muted num mono nowrap caption fine eyebrow lead display hero-title h1 h2 h3 h4 divider visually-hidden no-print inline`

## 13. Derived from

This system adapts the Apple web design analysis in `drafts/design-input/DESIGN-apple.md`: its surfaces (white, parchment #f5f5f7, pearl #fafafc, near-black tiles #1d1d1f / #272729), hairlines (#e0e0e0, #f0f0f0), ink #1d1d1f, the spacing scale 4/8/12/17/24/32/48/80, the radius grammar (pill actions, 8 px utility, 11 px fields and capsules, 18 px cards, 0 tiles), body at 17 px, headlines at 600 with negative tracking, the weight ladder without 500, no shadows on chrome, frosted sticky bars, the press-scale state, the black global nav with a frosted sub-nav, and the 833 / 640 px collapse points.

Deliberate deviations:

1. **Black and white instead of Action Blue.** Apple's single accent #0066cc (focus #0071e3, on-dark #2997ff) becomes ink: the primary is a solid ink pill, the secondary an ink-outlined pill, links are ink and underlined, the focus ring is black (white on dark). Selected chips are solid ink instead of a 2 px blue border.
2. **Inter instead of SF Pro.** Inter with optical sizing; body tracking −0.01em instead of −0.374 px and line-height 1.44 instead of 1.47 (Inter's taller x-height), as the analysis suggests. The `"ss03"` and `"cv11"` features are not set: the Google-served Inter showed no change for them in our renders, and cv11's single-storey "a" moves away from SF Pro. Tabular figures are used for money, times and counts only, not for codes or ISO dates (Inter's tabular hyphen is wide).
3. **Status by fill.** Apple has no status system; this one adds solid / outline / grey / attention badges, flashes and alerts so state never depends on hue.
4. **Accessible greys.** Muted text is #6e6e73 (5.07:1), not #7a7a7a (4.29:1, kept for disabled text only); input edges are #86868b to meet 3:1; #e8e8ed and #d2d2d7 are added for grey fills.
5. **No imagery, so no product shadow.** The one drop-shadow Apple keeps for photography is dropped; space cards use a typographic cover tile (capacity as the hero number).
6. **App density.** A 15 px callout size for tables and lists; 14 px nav links (not 12 px) and a 52 px global nav (not 44 px) for legibility and touch; content width 1120 px (between the analysis's 980 and 1440); breakpoints reduced to 1068 / 833 / 640 / 419.
7. **Press scale 0.97** instead of 0.95: app controls are pressed often and sit close together.
8. **One functional texture.** Booked time on the timeline uses a fine diagonal hatch, a state texture rather than decoration, so booked, too-soon and free stay distinct without colour.
