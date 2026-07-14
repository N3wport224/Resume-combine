#!/usr/bin/env python3
"""Heuristic ATS scorer. Extracts text with pypdfium2 and scores on standard
ATS-parseability criteria (0-100)."""
import re, sys
import pypdfium2 as pdfium

MONTHS = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{2}/\d{4}|present)"
STD_HEADINGS = ["experience", "education", "skills", "summary",
                "certification", "competenc", "profile"]

def extract(path):
    pdf = pdfium.PdfDocument(path)
    pages = len(pdf)
    txt = []
    for i in range(pages):
        txt.append(pdf[i].get_textpage().get_text_range() or "")
    return "\n".join(txt), pages

def score(path):
    text, pages = extract(path)
    low = text.lower()
    words = re.findall(r"\w+", text)
    breakdown = {}

    # 1. Machine-readable text present (20)
    breakdown["Parseable text"] = (20 if len(words) > 120 else
                                   10 if len(words) > 40 else 0, 20)

    # 2. Contact completeness: email, phone, location, linkedin (14)
    c = 0
    if re.search(r"[\w.]+@[\w.]+", text): c += 4
    if re.search(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text): c += 4
    if re.search(r"\b[A-Z][a-z]+,\s?[A-Z]{2}\b", text): c += 3
    if "linkedin" in low: c += 3
    breakdown["Contact info"] = (c, 14)

    # 3. Standard section headings (14)
    found = sum(1 for h in STD_HEADINGS if h in low)
    breakdown["Standard headings"] = (min(14, found * 3), 14)

    # 4. Dates on roles: count month/year date ranges (16)
    date_ranges = len(re.findall(MONTHS + r"[^\n]{0,20}?[-–]{1,2}\s*" + MONTHS, low))
    # also count standalone month-year tokens as fallback
    tokens = len(re.findall(r"\b(19|20)\d{2}\b", text))
    if date_ranges >= 4: d = 16
    elif date_ranges >= 2: d = 11
    elif tokens >= 4: d = 7
    elif tokens >= 1: d = 3
    else: d = 0
    breakdown["Complete dates"] = (d, 16)

    # 5. Single-column / no multi-column artifacts (14)
    col = 14
    if re.search(r"page\s+\d+\s+of\s+\d+", low): col -= 5   # export footers
    # crude two-column detector: many very short lines
    lines = [l for l in text.splitlines() if l.strip()]
    if lines:
        short = sum(1 for l in lines if len(l.strip()) < 22) / len(lines)
        if short > 0.45: col -= 6
    breakdown["Single-column layout"] = (max(0, col), 14)

    # 6. Keyword richness / skills coverage (12)
    kws = ["agile","scrum","project","data","operations","vendor","analysis",
           "management","dashboard","stakeholder","logistics","process",
           "business intelligence","excel","risk","coordination"]
    hits = sum(1 for k in kws if k in low)
    breakdown["Keyword coverage"] = (min(12, hits), 12)

    # 7. Clean encoding: penalize decorative math-bold/unicode glyphs (5)
    weird = len(re.findall(r"[\U0001D400-\U0001D7FF]", text))
    breakdown["Clean encoding"] = (0 if weird > 20 else 3 if weird > 0 else 5, 5)

    # 8. Length appropriateness 1-2 pages ideal (5)
    breakdown["Length (pages)"] = (5 if pages <= 2 else 3 if pages == 3 else 1, 5)

    total = sum(v[0] for v in breakdown.values())
    return total, pages, breakdown

if __name__ == "__main__":
    for path in sys.argv[1:]:
        total, pages, bd = score(path)
        print(f"\n=== {path}  ({pages} pages)  ->  {total}/100 ===")
        for k,(g,m) in bd.items():
            print(f"   {k:<24} {g:>2}/{m}")
