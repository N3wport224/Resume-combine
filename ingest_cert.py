#!/usr/bin/env python3
"""Extract certification data from a cert PDF.

Usage:  python3 ingest_cert.py path/to/cert.pdf [more.pdf ...]

Prints extracted text plus best-guess fields (issuer, issue date as MM/YYYY,
credential ID) to help populate resume_data.json -> "certifications".
For cert *images* (png/jpg), the assistant reads them directly via vision;
this script handles PDFs. Dates are normalized to MM/YYYY.
"""
import re, sys
import pypdfium2 as pdfium

MONTHS = {m: i for i, m in enumerate(
    ["january","february","march","april","may","june","july","august",
     "september","october","november","december"], 1)}
ABBR = {m[:3]: i for m, i in MONTHS.items()}

def to_mmyyyy(text):
    """Return a list of (raw, MM/YYYY) dates found in text."""
    found = []
    low = text.lower()
    # Month DD, YYYY  or  Month YYYY
    for m in re.finditer(r"\b([a-z]{3,9})\.?\s+(?:\d{1,2},?\s+)?(\d{4})\b", low):
        name, year = m.group(1), m.group(2)
        mo = MONTHS.get(name) or ABBR.get(name[:3])
        if mo:
            found.append((m.group(0), f"{mo:02d}/{year}"))
    # MM/YYYY or MM/DD/YYYY or M/D/YY
    for m in re.finditer(r"\b(\d{1,2})[/-](?:\d{1,2}[/-])?(\d{2,4})\b", text):
        mo, yr = int(m.group(1)), m.group(2)
        if 1 <= mo <= 12:
            if len(yr) == 2:
                yr = ("20" if int(yr) < 50 else "19") + yr
            found.append((m.group(0), f"{mo:02d}/{yr}"))
    # bare year fallback
    if not found:
        for m in re.finditer(r"\b(19|20)\d{2}\b", text):
            found.append((m.group(0), f"__/{m.group(0)}"))
    return found

ISSUERS = ["Scrum Alliance","Google","Coursera","IBM","Microsoft","ADP","AWS",
           "Amazon Web Services","LinkedIn","Udemy","edX","PMI","CompTIA",
           "Salesforce","Oracle","Meta","Cisco"]

def guess(text):
    low = text.lower()
    issuer = next((i for i in ISSUERS if i.lower() in low), "")
    cid = ""
    m = re.search(r"(credential|certificate|cert|id|verify|code)[^\w]{0,8}"
                  r"([A-Z0-9]{6,}|[A-Z0-9-]{8,})", text, re.I)
    if m:
        cid = m.group(2)
    dates = to_mmyyyy(text)
    return issuer, dates, cid

def extract(path):
    pdf = pdfium.PdfDocument(path)
    return "\n".join((pdf[i].get_textpage().get_text_range() or "")
                     for i in range(len(pdf)))

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print("\n" + "=" * 70)
        print("CERT FILE:", path)
        print("=" * 70)
        text = extract(path)
        print(text.strip()[:1500] or "[no extractable text - likely a scanned image; read via vision]")
        issuer, dates, cid = guess(text)
        print("\n--- BEST GUESS ---")
        print("Issuer:        ", issuer or "?")
        print("Issue date(s): ", ", ".join(f"{r} -> {n}" for r, n in dates) or "?")
        print("Credential ID: ", cid or "?")
