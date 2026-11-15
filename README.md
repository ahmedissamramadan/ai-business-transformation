# Landing pages — AI Business Transformation & Integration

Static, Arabic-first landing pages for the practice. One design system, two
market pages, no build step and no dependencies: plain HTML, one stylesheet,
one small script.

```
index.html            Egypt market — the home page
gulf/index.html       Gulf market (Saudi Arabia led, GCC comparison)
assets/style.css      the design system, shared by both pages
assets/app.js         progressive enhancement only (scroll reveal, nav spy)
tools/check_site.py   lints the pages for stray characters and unfilled tokens
```

Open `index.html` in a browser — there is nothing to install and nothing to
build.

---

## Before you publish: three edits

Both pages carry two placeholders. Find them with:

```bash
grep -rn "{{" . --include="*.html"
```

| Token | Replace with | Appears in |
|---|---|---|
| `{{WHATSAPP}}` | your WhatsApp number in international format, no `+` and no spaces — e.g. `201001234567` | the header button, the hero CTA, the CTA band, the footer |
| `{{EMAIL}}` | your email address | the CTA band, the founder block |

Then check the LinkedIn URL, which is currently `linkedin.com/in/ahmedissamramadan`:

```bash
grep -rn "linkedin.com/in" . --include="*.html"
```

Replace it if that is not your profile.

And set the two absolute URLs that social platforms use when the page is
shared in a WhatsApp or LinkedIn message — the preview image and the link
both come from these:

```bash
grep -rn "example.com" . --include="*.html"
```

Change `og:url` and `link rel="canonical"` to your real domain. The `og:title`
and `og:description` are already written.

---

## Publishing

**GitHub Pages (free, and what your action plan calls for):**

1. Create a repository, push this folder.
2. Settings → Pages → Deploy from a branch → `main` / root.
3. The site is live at `https://<user>.github.io/<repo>/` in a minute.
4. For your own domain: add a `CNAME` file containing the domain, point a
   CNAME record at `<user>.github.io`, and enable "Enforce HTTPS".

**Any other host** — Netlify, Vercel, Cloudflare Pages: drag the folder in.
No configuration is needed; there is no build step.

**Previewing locally** before publishing:

```bash
python3 -m http.server 8000
open http://localhost:8000
```

A local server is better than opening the file directly, because the pages
load `assets/style.css` relative to their own folder.

---

## What is on the pages

| Section | Egypt | Gulf |
|---|---|---|
| Hero with the published price summary | ✓ | ✓ |
| The problem — four named failure modes | ✓ | ✓ |
| The four offers, with duration and price on each card | ✓ | ✓ |
| ABTI — the six phases | ✓ | ✓ |
| The full price ladder, plus floor / ceiling / credit rules | ✓ | ✓ |
| Sectors | 3 priority sectors | 10 sectors |
| Frameworks | evidence levels | ECC · PDPL · e-invoicing · SAMA · local content · Nitaqat |
| Who we work with, and who we don't | ✓ | ✓ |
| Frequently asked questions | 7 | 7 |
| Founder | ✓ | ✓ |
| Call to action | ✓ | ✓ |

Both pages are Arabic-primary with English secondary, and both are right to
left throughout — including the list markers, the table columns and the
section headings.

---

## Design notes

- **One stylesheet, two pages.** Change `--gold`, `--teal` or `--ink` in
  `assets/style.css` and both pages follow.
- **Progressive enhancement.** The pages read and work with JavaScript
  disabled. The script only adds scroll reveals and highlights the section
  you are reading.
- **Reduced motion is respected.** `prefers-reduced-motion` turns the
  reveals off and removes the hover lifts.
- **It prints.** There is a print stylesheet: the navigation and the calls to
  action are dropped, and the page comes out clean on A4 or Letter.
- **Shared link previews.** Open Graph tags are set for both pages, so a
  WhatsApp or LinkedIn share shows the title and description rather than a
  bare URL.

---

## What is deliberately not on the pages

**No case studies, no client logos, no statistics, no testimonials.** There
is no documented engagement yet, and inventing any of these would break the
one rule the practice runs on: nothing is claimed that cannot be evidenced.
The FAQ says this out loud, which is itself a differentiator.

When the first project is signed, add a case-study block with the client's
written permission, its baseline, the intervention and the measured result —
and change the FAQ answer that currently says there is none.

---

## Keeping the pages honest

The prices on the pages are the same prices as in the Master Operating
Playbook and the price card. When one changes, change all three:

- `AI BUSINESS TRANSFORMATION & INTEGRATION v1.1/working-set/` — the price card
- `AI BUSINESS TRANSFORMATION & INTEGRATION GCC/working-set/` — the Gulf price card
- these two pages

The footer of each page carries the date the prices were last reviewed
(12 November 2026 for Egypt, 13 November 2026 for the Gulf). Update it when
you update the prices.

---

## The linters

```bash
python3 tools/check_site.py     # stray characters + tokens still to fill
python3 tools/fingerprint.py index.html gulf/index.html   # AI-writing tells
```

`fingerprint.py` reports the markers that make machine-written copy
recognisable: an em dash used as a stylistic tic, an en dash outside a
numeric range, the "ليس … بل …" antithesis, a chain of three "ثم", and
filler phrases. Every one of them is now gone from both pages, and the check
is part of the pre-publish gate.

It reports stray Latin, CJK or Cyrillic fragments in the Arabic prose — the
same class of typo the playbook build catches — and lists the tokens still
waiting for a value. It exits non-zero if either is found, so it can sit in
a pre-publish check.

Hand-written Arabic picks these up silently: they are invisible in the source
and obvious on the page. This build caught nine of them in the Gulf page.
