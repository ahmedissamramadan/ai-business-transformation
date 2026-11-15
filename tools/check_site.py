#!/usr/bin/env python3
"""Lint the landing pages for stray characters and unfilled tokens.

Hand-authored Arabic prose in HTML picks up the same Latin, CJK and Cyrillic
fragments that the playbooks do. This catches them, and lists the tokens that
still need a real value before the page is published.

    python3 tools/check_site.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fingerprint

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

# Latin words that legitimately appear in the pages.
ALLOWED = set("""
AI Business Transformation Integration Master Operating Playbook Egypt Gulf Edition
Version SME SMEs GDP IT AI IoT API ERP CRM HR ROI CAC CTO COO CIO CPO CFO CDO PMO ECC
PDPL ZATCA SAMA MISA Nitaqat Nitaqat ECC ABITI ABTI SAR AED QAR KWD BHD OMR USD EGP
Lead In Name Value Price Ladder Offer Offers Read More Learn More Get Started
Contact Us Book Call Message Us Why What How Who When Where Which
Business First Where It Matters Results Always
Foundation Readiness Assessment Blueprint Delivery Continuous Transformation
Partnership Diagnostic Implementation Engagement Optimization Strategy Mapping
Systems Integration Intelligent Automation Change Management Performance
Quality Management Revenue Cycle Time Product Cost Data Security Privacy
LinkedIn WhatsApp Email Document Control Reference Committee
Next Previous Home Menu Open Close
""".split())

ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
LATIN = re.compile(r"[A-Za-z][A-Za-z\.\-_/&']*")
STRAY = re.compile(
    r"[^\x00-\x7F؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿"
    r" ‌‍‎‏﻿­‪‫‬‭‮‘’“”…·©§«»№×÷≈±≥≤→←↑↓•✓—–]"
)


def check_text(text, where, problems):
    for m in LATIN.finditer(text):
        w = m.group(0)
        if w in ALLOWED or w.isupper():
            continue
        # a Latin word glued to Arabic (no space) is always a typo
        before = text[m.start() - 1] if m.start() else ""
        after = text[m.end()] if m.end() < len(text) else ""
        if ARABIC.search(before) or ARABIC.search(after):
            problems.append((where, "latin glued to arabic %r" % w,
                             " ".join(text[max(0, m.start() - 40):m.end() + 40].split())))
            continue
        # a Latin word with Arabic on both sides is also a typo
        b2 = text[max(0, m.start() - 3):m.start()]
        a2 = text[m.end():m.end() + 3]
        if ARABIC.search(b2) and ARABIC.search(a2):
            problems.append((where, "embedded latin %r" % w,
                             " ".join(text[max(0, m.start() - 40):m.end() + 40].split())))
    for m in STRAY.finditer(text):
        problems.append((where, "stray run %r" % m.group(0),
                         " ".join(text[max(0, m.start() - 40):m.end() + 30].split())))


def main():
    problems = []
    tokens = []
    files = sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("gulf/*.html"))
    if not files:
        sys.exit("no html found")
    for f in files:
        raw = f.read_text(encoding="utf-8")
        # strip tags and comments so we only judge visible text
        body = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
        body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", body)
        check_text(text, f.name, problems)
        for tok in sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", raw))):
            tokens.append((f.name, tok))

    print("files: %s" % ", ".join(f.name for f in files))
    if tokens:
        print("\nTOKENS STILL TO FILL:")
        for name, tok in tokens:
            print("  %-18s %s" % (name, tok))
    if problems:
        print("\nPROBLEMS (%d):" % len(problems))
        for where, kind, ctx in problems:
            print("  %-12s %-26s %s" % (where, kind, ctx))
        sys.exit(1)
    print("\nclean: no stray characters")

    # AI-writing fingerprints
    fhits = []
    for f in files:
        raw = f.read_text(encoding="utf-8")
        raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
        raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
        fingerprint.scan(re.sub(r"<[^>]+>", " ", raw), f.name, fhits)
    if fhits:
        print("\nFINGERPRINTS (%d):" % len(fhits))
        for label, name, ctx in fhits:
            print("  %-12s %-26s %s" % (label, name, ctx))
        sys.exit(1)
    print("clean: no fingerprints")


if __name__ == "__main__":
    main()
