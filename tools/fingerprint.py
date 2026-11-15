#!/usr/bin/env python3
"""Detect AI-writing fingerprints in Arabic prose.

The tells that give machine-written copy away, in the order they matter:

  em-dash      " — "  used as a stylistic tic; the single loudest marker
  en-dash      " – "  outside numeric ranges, where it means the same thing
  double-neg   dropped: idiomatic Arabic uses "لا ... لا" freely
  contrast     "ليس ... بل ..." / "لا ... بل ..."
  triad        "ثم ... ثم ..." inside one sentence
  filler       "بشكل", "إلى حد كبير", "في المقابل", "من الجيد أن"

Usage:
    python3 fingerprint.py file.html [more files...]
    python3 fingerprint.py --text "some arabic prose"
"""
import pathlib
import re
import sys

EM_DASH = "\u2014"
EN_DASH = "\u2013"

PATTERNS = [
    ("em-dash", re.compile(EM_DASH)),
    ("en-dash", re.compile(r"(?<![\d])" + EN_DASH + r"(?![\d])")),
    ("contrast", re.compile(r"\b(ليس|ليست|لا|ليسوا)\b[^.]{0,80}?\bبل\b")),
    ("triad", re.compile(r"\bثم\b[^.]{0,200}?\bثم\b[^.]{0,200}?\bثم\b")),
    ("filler", re.compile(r"(بشكل كبير|إلى حد كبير|في المقابل|من الجيد أن|لا بد من الإشارة)")),
]

# Words that are part of the domain vocabulary, not a stylistic tic.
DOMAIN_OK = set()


def scan(text, label, hits):
    for name, pat in PATTERNS:
        for m in pat.finditer(text):
            ctx = " ".join(text[max(0, m.start() - 45):m.end() + 45].split())
            hits.append((label, name, ctx))
    return hits


def scan_file(path):
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", raw)
    hits = []
    scan(text, pathlib.Path(path).name, hits)
    return hits


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    hits = []
    if sys.argv[1] == "--text":
        scan(sys.argv[2], "text", hits)
    else:
        for f in sys.argv[1:]:
            hits.extend(scan_file(f))
    if not hits:
        print("clean: no fingerprints")
        return 0
    counts = {}
    for label, name, ctx in hits:
        counts[name] = counts.get(name, 0) + 1
    print("FINGERPRINTS (%d):" % len(hits))
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("  %-12s %d" % (name, n))
    print()
    for label, name, ctx in hits:
        print("  [%s] %s\n      %s" % (label, name, ctx))
    return 1


if __name__ == "__main__":
    sys.exit(main())
