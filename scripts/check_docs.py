#!/usr/bin/env python3
"""Mechanical docs checks (stdlib only). Runs locally and in docs CI.

Checks whatever exists, so it works from M0 onward: diagrams, ID definitions
and references, rule templates and examples, statuses, decisions, the ID map,
PRD coverage, ADR references, contract states and traceability.
Formats are described in README.md ("Doc formats").
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTEXTS = ("Purchase", "Payment", "Access")
ACTORS = ("Member", "Operator", "Staff", "Browser")
NEW_ID = re.compile(r"\b(?:PUR|PMT|AXS)-[TRQ]\d{2}\b")
RULE_ID = re.compile(r"\b(?:PUR|PMT|AXS)-R\d{2}\b")
CLASS_ID = re.compile(r"^(?:[A-Z]{2,6}-[A-Z]?\d{2}|Q-[A-Z]+-\d+|Q\d{2})$")
POLICY = ("Observed", "Decided", "Stakeholder-clarified", "Superseded")
RULE_FIELDS = ("Rule", "Policy status", "Decision source", "Implementation evidence", "Terms",
               "Candidate responsibility and dependencies", "Open question", "Clarification owner", "Next use")
KINDS = ("ordinary", "boundary", "counterexample")
CHANNELS = ("JSON", "form", "internal")
DISPOSITIONS = ("kept", "merged", "superseded", "rejected")
CONTRACT_STATES = ("proposed", "agreed", "verified")
REPORTS = ("purchase", "payment", "access", "e2e")
NODE = re.compile(r"`(purchase|payment|access|e2e):([^`\s]+?\.py)::([^`\s]+)`")

errors = []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def read(name):
    p = ROOT / name
    return p.read_text() if p.exists() else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def rows(text):
    """Table rows as cell lists, separator rows skipped."""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and not re.fullmatch(r"\|[\s:|-]+\|", s):
            yield cells(s)


def bare(cell):
    return cell.strip("`* ")


def sections(text, pattern):
    """Split text into {id: body} at headings matching pattern (group 1 = id)."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(pattern, line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif re.match(r"#{1,3}\s", line):
            cur = None
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def md_files():
    skip = {".git", "node_modules", ".venv", "drafts"}
    return [p for p in ROOT.rglob("*.md") if not skip & set(p.relative_to(ROOT).parts)]


# ---------------------------------------------------------------- diagrams
def check_diagrams():
    n = 0
    for path in sorted((ROOT / "diagrams").glob("*.mmd")):
        n += 1
        text = path.read_text()
        lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("%%")]
        if lines and lines[0].startswith("sequenceDiagram"):
            boxes, inside, count = [], None, 0
            for l in lines[1:]:
                if l.startswith("box "):
                    inside, count = l, 0
                elif inside and l == "end":
                    boxes.append((inside, count))
                    inside = None
                elif re.match(r"(participant|actor)\s", l):
                    if inside:
                        count += 1
                    elif not any(a in l for a in ACTORS):
                        err(path.name, f"participant outside the three boxes: {l}")
            for label, c in boxes:
                if c == 0:
                    err(path.name, f"empty box (mermaid drops it): {label}")
            for ctx in CONTEXTS:
                if not any(re.search(rf"\b{ctx}\b", b) for b, _ in boxes):
                    err(path.name, f"missing box {ctx}")
        else:
            for ctx in CONTEXTS:
                if not re.search(rf"^\s*(subgraph|state)\s+\"?{ctx}\b", text, re.M):
                    err(path.name, f"missing {ctx} box")
    return n


# ---------------------------------------------------------- ID definitions
DEF_FILES = {"GLOSSARY.md": "T", "RULES.md": "R", "OPEN_QUESTIONS.md": "Q"}


def collect_definitions():
    defs = {}
    for name, kind in DEF_FILES.items():
        text = read(name)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            m = re.match(r"#{2,4}\s+((?:PUR|PMT|AXS)-[TRQ]\d{2})\b", line)
            if not m and line.strip().startswith("|"):
                m = re.fullmatch(r"((?:PUR|PMT|AXS)-[TRQ]\d{2})", bare(cells(line)[0]))
            if m:
                ident = m.group(1)
                defs.setdefault(ident, []).append(f"{name}:{i}")
                if ident[4] != kind:
                    err(f"{name}:{i}", f"{ident} is not a {kind} ID")
    for ident, locs in defs.items():
        if len(locs) > 1:
            err(ident, "defined more than once: " + ", ".join(locs))
    return defs


def check_references(defs):
    for path in md_files():
        for i, line in enumerate(path.read_text().splitlines(), 1):
            for ident in NEW_ID.findall(line):
                if ident not in defs:
                    err(f"{path.relative_to(ROOT)}:{i}", f"{ident} referenced but not defined")


# ------------------------------------------------------------------ rules
def check_rules():
    text = read("RULES.md")
    if text is None:
        return {}
    statuses = {}
    for ident, body in sections(text, r"#{2,4}\s+((?:PUR|PMT|AXS)-R\d{2})\b").items():
        fields, kinds, examples = {}, set(), 0
        for c in rows(body):
            if len(c) >= 2 and c[0] in RULE_FIELDS:
                fields[c[0]] = c[1]
            elif c[0].isdigit():
                if len(c) != 6:
                    err(ident, f"example row {c[0]} needs 6 cells (# | Kind | Channel | Given | When | Expected result under this rule)")
                    continue
                examples += 1
                if c[1] not in KINDS:
                    err(ident, f"example {c[0]} kind '{c[1]}' not in {KINDS}")
                if c[2] not in CHANNELS:
                    err(ident, f"example {c[0]} channel '{c[2]}' not in {CHANNELS}")
                kinds.add(c[1])
        for f in RULE_FIELDS:
            if not fields.get(f):
                err(ident, f"missing field '{f}'")
        status = fields.get("Policy status", "")
        word = next((p for p in POLICY if status.startswith(p)), None)
        if not word:
            err(ident, f"policy status '{status}' not in {POLICY}")
        elif word == "Superseded" and not RULE_ID.search(status.replace(ident, "")):
            err(ident, "Superseded needs a replacement rule ID")
        statuses[ident] = word
        if examples < 3:
            err(ident, f"only {examples} example rows (need >= 3)")
        for k in KINDS:
            if k not in kinds:
                err(ident, f"no '{k}' example row")
    return statuses


def check_glossary():
    text = read("GLOSSARY.md")
    if text is None:
        return 0
    n = 0
    for c in rows(text):
        if NEW_ID.fullmatch(bare(c[0])):
            n += 1
            if len(c) != 6:
                err(c[0], "glossary row needs 6 cells (ID | Term | Context | Meaning | Counterexample | Status / source)")
            elif not c[5].startswith(POLICY):
                err(c[0], f"status '{c[5]}' not in {POLICY}")
            elif not c[4] or c[4] in ("-", "—"):
                err(c[0], "missing counterexample")
    return n


def check_questions():
    text = read("OPEN_QUESTIONS.md")
    if text is None:
        return 0
    qs = sections(text, r"#{2,4}\s+((?:PUR|PMT|AXS)-Q\d{2})\b")
    for ident, body in qs.items():
        if "default" not in body.lower():
            err(ident, "open question has no default that applies")
    return len(qs)


def check_decisions():
    text = read("DECISIONS.md")
    if text is None:
        return set()
    found = {}
    for c in rows(text):
        m = re.fullmatch(r"D(\d+)", bare(c[0]))
        if m:
            found.setdefault(int(m.group(1)), []).append(c)
    for d in range(1, 29):
        if d not in found:
            err("DECISIONS.md", f"D{d} missing")
    for d, cs in found.items():
        if len(cs) > 1:
            err("DECISIONS.md", f"D{d} listed {len(cs)} times")
        if len(cs[0]) < 5 or not cs[0][3].startswith("Decided"):
            err("DECISIONS.md", f"D{d} needs 5 cells with Status 'Decided'")
    for path in md_files():
        for ref in re.findall(r"(?<![\w-])D(\d{1,2})\b(?![-.]\d)", path.read_text()):
            if int(ref) not in found:
                err(str(path.relative_to(ROOT)), f"D{ref} referenced but not in DECISIONS.md")
    return set(found)


def check_adr_refs():
    have = {p.name[:4] for p in (ROOT / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")}
    for path in md_files():
        for ref in re.findall(r"\bADR-(\d+)\b", path.read_text()):
            if ref.zfill(4) not in have or len(ref) != 4:
                err(str(path.relative_to(ROOT)), f"ADR-{ref} has no adr/{ref.zfill(4)}-*.md (use 4 digits)")
    return len(have)


def check_id_map(defs):
    text, inv = read("ID_MAP.md"), read("inventory/class-ids.md")
    if text is None:
        return 0
    seen = {}
    for c in rows(text):
        ident = bare(c[0])
        if not CLASS_ID.match(ident):
            continue
        if ident.split("-")[0] in ("PUR", "PMT", "AXS"):
            err("ID_MAP.md", f"class ID {ident} uses a project prefix")
        seen[ident] = seen.get(ident, 0) + 1
        if len(c) != 5:
            err(ident, "ID_MAP row needs 5 cells (Class ID | Class meaning / source | New ID | Disposition | Reason)")
            continue
        if c[3] not in DISPOSITIONS:
            err(ident, f"disposition '{c[3]}' not in {DISPOSITIONS}")
        if c[3] != "rejected" and not NEW_ID.search(c[2]):
            err(ident, f"disposition {c[3]} needs a new ID")
        if not c[4]:
            err(ident, "missing reason")
    for ident, n in seen.items():
        if n > 1:
            err("ID_MAP.md", f"{ident} listed {n} times")
    if inv is not None:
        class_ids = {bare(c[0]) for c in rows(inv) if CLASS_ID.match(bare(c[0]))}
        for ident in sorted(class_ids - set(seen)):
            err("ID_MAP.md", f"class ID {ident} (inventory/class-ids.md) not mapped")
        for ident in sorted(set(seen) - class_ids):
            err("ID_MAP.md", f"{ident} not in inventory/class-ids.md")
    return len(seen)


def check_prd(statuses):
    text = read("PRD.md")
    if text is None:
        return 0
    acs = 0
    cover = {}  # rule -> stories whose criteria cite it
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"\s*[-*]\s+\**AC\d+(\.\d+)?\b", line):
            acs += 1
            if not RULE_ID.search(line):
                err(f"PRD.md:{i}", "acceptance criterion cites no rule ID")
            story = int(re.search(r"AC(\d+)", line).group(1))
            for ident in RULE_ID.findall(line):
                cover.setdefault(ident, set()).add(story)
    # The rule coverage table (section 4.4) must match the criteria's citations.
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"\|\s*((?:PUR|PMT|AXS)-R\d{2})\s[^|]*\|([^|]*)\|\s*$", line)
        if m:
            listed = {int(n) for n in re.findall(r"US(\d+)", m.group(2))}
            if listed != cover.get(m.group(1), set()):
                want = ", ".join(f"US{n}" for n in sorted(cover.get(m.group(1), set())))
                err(f"PRD.md:{i}", f"coverage row {m.group(1)} should list {want or 'no story'}")
    cited = set(RULE_ID.findall(text))
    for ident in statuses:
        if ident not in cited:
            err("PRD.md", f"rule {ident} not reachable from any story")
    return acs


def check_contracts():
    text = read("contracts/README.md")
    if text is None:
        return 0
    n = 0
    for c in rows(text):
        if len(c) >= 5 and c[0] not in ("Contract",):
            n += 1
            if bare(c[4]).split()[0].lower() not in CONTRACT_STATES:
                err("contracts/README.md", f"state '{c[4]}' not in {CONTRACT_STATES}")
    return n


# ----------------------------------------------------------- traceability
def load_reports():
    results = {}
    for name in REPORTS:
        p = ROOT / "integration" / "reports" / f"{name}.xml"
        if not p.exists():
            continue
        for tc in ET.parse(p).getroot().iter("testcase"):
            bad = any(ch.tag in ("failure", "error", "skipped") for ch in tc)
            results[(name, tc.get("classname"), tc.get("name"))] = not bad
    return results


def check_traceability(statuses):
    text = read("TRACEABILITY.md")
    if text is None:
        return 0
    results = load_reports()
    rows_by_id = {}
    for c in rows(text):
        ident = bare(c[0])
        if RULE_ID.fullmatch(ident):
            rows_by_id[ident] = " | ".join(c[1:])
    nodes = 0
    for ident, status in statuses.items():
        ev = rows_by_id.get(ident)
        if ev is None:
            err("TRACEABILITY.md", f"{ident} has no row")
            continue
        if status in ("Decided", "Stakeholder-clarified"):
            found = NODE.findall(ev)
            if not found and "manual:" not in ev:
                err(ident, "Decided/Stakeholder-clarified rule needs test node IDs or 'manual: <steps + result>'")
            for report, path, rest in found:
                nodes += 1
                parts = rest.split("::")
                classname = ".".join([path[:-3].replace("/", ".")] + parts[:-1])
                ok = results.get((report, classname, parts[-1]))
                if ok is None:
                    err(ident, f"{report}:{path}::{rest} not in integration/reports/{report}.xml")
                elif not ok:
                    err(ident, f"{report}:{path}::{rest} failed, errored or skipped")
        elif not RULE_ID.search(ev) and "out of scope (ADR-" not in ev:
            err(ident, f"{status} rule needs its replacing rule ID or 'out of scope (ADR-n)'")
    for ident in rows_by_id:
        if ident not in statuses:
            err("TRACEABILITY.md", f"{ident} is not a rule in RULES.md")
    return nodes


def main():
    diagrams = check_diagrams()
    defs = collect_definitions()
    check_references(defs)
    statuses = check_rules()
    terms = check_glossary()
    questions = check_questions()
    decisions = check_decisions()
    adrs = check_adr_refs()
    mapped = check_id_map(defs)
    acs = check_prd(statuses)
    contracts = check_contracts()
    nodes = check_traceability(statuses)
    for e in errors:
        print("ERROR", e)
    print(f"check_docs: diagrams={diagrams} terms={terms} rules={len(statuses)} questions={questions} "
          f"decisions={len(decisions)} adrs={adrs} class_ids_mapped={mapped} acceptance_criteria={acs} "
          f"contracts={contracts} trace_nodes={nodes} -> {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
