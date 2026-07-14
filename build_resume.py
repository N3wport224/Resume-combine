#!/usr/bin/env python3
"""Generate an ATS-optimized, single-column PDF resume from resume_data.json.

All dates render as MM/YYYY (or 'Present'). Certifications display their issue
date in (MM/YYYY) whenever the data provides one.
"""
import json, html, sys
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

DATA = sys.argv[1] if len(sys.argv) > 1 else "resume_data.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "Andrew_Perez_Master_Resume.pdf"

NAVY = HexColor("#1a2a4a")
GREY = HexColor("#333333")

S = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=20,
                           textColor=NAVY, spaceAfter=2, alignment=TA_LEFT, leading=23),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9.5,
                              textColor=GREY, spaceAfter=8, leading=13),
    "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11.5,
                              textColor=NAVY, spaceBefore=9, spaceAfter=2, leading=14),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10.5,
                           textColor=GREY, spaceBefore=5, spaceAfter=0, leading=13),
    "meta": ParagraphStyle("meta", fontName="Helvetica-Oblique", fontSize=9,
                           textColor=GREY, spaceAfter=2, leading=12),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.5,
                           textColor=GREY, spaceAfter=3, leading=13),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5,
                             textColor=GREY, leftIndent=12, bulletIndent=2,
                             spaceAfter=2, leading=12.5),
}

def esc(t):
    return html.escape(str(t)).replace("&amp;", "&amp;")  # keep entities safe

def E(t):  # escape for reportlab mini-html
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def hr():
    return HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceBefore=1, spaceAfter=4)

def daterange(start, end):
    parts = [p for p in [start, end] if p]
    return "&nbsp;&ndash;&nbsp;".join(E(p) for p in parts)

def meta_line(loc, start, end):
    dr = daterange(start, end)
    if loc and dr:
        return f"{E(loc)}&nbsp; |&nbsp; {dr}"
    return E(loc) if loc else dr

with open(DATA) as f:
    d = json.load(f)

story = []
story.append(Paragraph(E(d["name"]), S["name"]))
c = d["contact"]
contact_bits = [c.get("location"), c.get("phone"), c.get("email"), c.get("linkedin")]
story.append(Paragraph("&nbsp; |&nbsp; ".join(E(b) for b in contact_bits if b), S["contact"]))

def section(title):
    story.append(Paragraph(title.upper(), S["section"]))
    story.append(hr())

def bullet(t):
    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{E(t)}", S["bullet"]))

# Summary
section("Professional Summary")
story.append(Paragraph(E(d["summary"]), S["body"]))

# Skills
section("Core Skills")
story.append(Paragraph("&nbsp;|&nbsp; ".join(E(s) for s in d["skills"]), S["body"]))

# Experience
section("Professional Experience")
for j in d["experience"]:
    story.append(Paragraph(f'{E(j["title"])} &mdash; {E(j["company"])}', S["role"]))
    story.append(Paragraph(meta_line(j.get("location", ""), j["start"], j["end"]), S["meta"]))
    for b in j["bullets"]:
        bullet(b)

if d.get("earlier_experience"):
    story.append(Paragraph("Earlier Experience", S["role"]))
    for j in d["earlier_experience"]:
        loc = f', {j["location"]}' if j.get("location") else ""
        line = f'{E(j["title"])} &mdash; {E(j["company"])}{E(loc)}&nbsp; |&nbsp; {daterange(j["start"], j["end"])}'
        bullet(line)

# Education
section("Education")
for e in d["education"]:
    dr = daterange(e.get("start", ""), e.get("end", ""))
    tail = f'&nbsp; |&nbsp; {dr}' if dr else ""
    story.append(Paragraph(f'<b>{E(e["degree"])}</b> &mdash; {E(e["school"])}{tail}', S["body"]))
if d.get("education_honors"):
    story.append(Paragraph(f'Honors: {E(d["education_honors"])}', S["body"]))

# Certifications  (name, issuer, and (MM/YYYY) issue date when available)
section("Certifications")
cert_strs = []
for cert in d["certifications"]:
    s = E(cert["name"])
    if cert.get("issuer"):
        s += f', {E(cert["issuer"])}'
    if cert.get("issue_date"):
        if cert.get("expires"):
            s += f' ({E(cert["issue_date"])}&nbsp;&ndash;&nbsp;{E(cert["expires"])})'
        else:
            s += f' ({E(cert["issue_date"])})'
    cert_strs.append(s)
story.append(Paragraph("&nbsp;|&nbsp; ".join(cert_strs), S["body"]))

doc = BaseDocTemplate(OUT, pagesize=LETTER,
                      leftMargin=0.6*inch, rightMargin=0.6*inch,
                      topMargin=0.5*inch, bottomMargin=0.5*inch,
                      title=f'{d["name"]} - Resume', author=d["name"])
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame])])
doc.build(story)
print("Wrote", OUT)
