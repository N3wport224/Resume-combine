#!/usr/bin/env python3
"""Generate an ATS-optimized, single-column PDF resume from structured data."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

OUT = "Andrew_Perez_Master_Resume.pdf"

NAVY = HexColor("#1a2a4a")
GREY = HexColor("#333333")

styles = {
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

def hr():
    return HRFlowable(width="100%", thickness=0.8, color=NAVY,
                      spaceBefore=1, spaceAfter=4)

def section(title):
    return [Paragraph(title.upper(), styles["section"]), hr()]

def bullets(items):
    return [Paragraph(f"&bull;&nbsp;&nbsp;{t}", styles["bullet"]) for t in items]

story = []

# Header
story.append(Paragraph("Andrew Perez", styles["name"]))
story.append(Paragraph(
    "Lone Tree, CO&nbsp; |&nbsp; (657) 259-8424&nbsp; |&nbsp; "
    "APerezJobs@gmail.com&nbsp; |&nbsp; linkedin.com/in/andrewperez1",
    styles["contact"]))

# Summary
story += section("Professional Summary")
story.append(Paragraph(
    "Process-driven IT Project Manager and operations leader with an MBA in IT "
    "Management and a Certified ScrumMaster (CSM) credential. Specializes in "
    "turning complex operational challenges into structured, scalable workflows "
    "across business intelligence, systems analysis, and agile team coordination. "
    "Currently at Xcel Energy, bridging organizational divisions and external "
    "partners to stabilize data integrity, track core assets, and resolve "
    "escalated systemic bottlenecks&mdash;consistently delivering on-time, "
    "cross-functional results.", styles["body"]))

# Core Skills
story += section("Core Skills")
story.append(Paragraph(
    "Operations Coordination&nbsp;|&nbsp; Cross-Functional Team Leadership&nbsp;|&nbsp; "
    "Vendor &amp; Supplier Management&nbsp;|&nbsp; Project Strategy &amp; Delivery&nbsp;|&nbsp; "
    "Agile &amp; Scrum Frameworks&nbsp;|&nbsp; Systems &amp; Data Analysis&nbsp;|&nbsp; "
    "Business Intelligence (BI)&nbsp;|&nbsp; Predictive Dashboards&nbsp;|&nbsp; "
    "Process Optimization&nbsp;|&nbsp; Risk Management&nbsp;|&nbsp; Inventory Control&nbsp;|&nbsp; "
    "Data Processing &amp; Analysis&nbsp;|&nbsp; MS Excel (Pivot Tables, Lookups)&nbsp;|&nbsp; "
    "SSH / Command Line", styles["body"]))

# Experience
story += section("Professional Experience")

def job(title, company, meta, items):
    out = [Paragraph(f"{title} &mdash; {company}", styles["role"]),
           Paragraph(meta, styles["meta"])]
    out += bullets(items)
    return out

story += job("Digital Lead", "Xcel Energy", "Minneapolis, MN&nbsp; |&nbsp; August 2022 &ndash; Present", [
    "Lead cross-functional digital process implementations across multi-state operations to align field workflows with enterprise strategic objectives; serve as primary operational link between utility division leads, regional project managers, and legacy technology teams.",
    "Synthesize, audit, and track operational assets and compliance records across complex relational databases to ensure high data fidelity.",
    "Champion Agile/Scrum best practices to accelerate resource allocation, streamline maintenance workflows, and eliminate procedural drag.",
    "Manage key vendor partnerships, establishing operational KPIs and resolving high-level systemic bottlenecks to secure seamless service delivery.",
])

story += job("Strategic Account Specialist", "AutoZone", "Robbinsdale, MN&nbsp; |&nbsp; October 2021 &ndash; October 2022", [
    "Managed high-volume B2B accounts as the commercial liaison between corporate clients, logistics providers, and procurement systems.",
    "Evaluated high-volume invoicing data, spot-checking variance anomalies and tracking supplier cost drivers to safeguard margin performance.",
    "Orchestrated demand-planning cycles, analyzing supplier pricing models and lead times to stabilize inventory pipelines.",
    "Led and coached a sales team with metrics-driven playbooks to scale operational capacity and surpass growth targets.",
])

story += job("Warehouse Team Lead", "MWI Animal Health", "Shakopee, MN&nbsp; |&nbsp; August 2019 &ndash; November 2019", [
    "Directed daily fulfillment logistics and resource planning across a high-throughput distribution center.",
    "Engineered and audited inventory distribution frameworks to maximize fulfillment velocity and reduce shrinkage.",
    "Coordinated with external 3PL providers and freight partners, renegotiating fulfillment touchpoints to optimize operational costs.",
])

story += job("Store Operations Coordinator", "Google Express", "Maple Grove, MN&nbsp; |&nbsp; August 2017 &ndash; June 2019", [
    "Orchestrated cross-functional systems coordination and data-integrity workflows supporting platform reliability and business intelligence reporting.",
    "Developed and tested end-to-end protocols for internal IT frameworks, isolating operational errors and validating system functionality against business requirements.",
    "Engineered data tracking models and reporting outputs used by engineering teams to document specifications for technology dashboards.",
    "Collaborated with stakeholders and development leads to translate raw data needs into structured process improvements.",
])

story += job("Project Manager", "Advanced E-Media, Inc. / WebJaguar E-Commerce", "August 2013 &ndash; October 2014", [
    "Managed digital data workflows, asset tracking, and customer operations coordination for an e-commerce platform.",
    "Maintained high-accuracy entry and auditing of client project records to ensure data fidelity.",
    "Partnered with cross-functional teams to streamline scheduling, clear fulfillment delays, and resolve account-level dependencies.",
])

# Earlier experience (compact)
story.append(Paragraph("Earlier Experience", styles["role"]))
story += bullets([
    "Service Technician &mdash; Apex Technical Solutions&nbsp; |&nbsp; September 2012 &ndash; July 2013",
    "Technician &mdash; GKN Aerospace&nbsp; |&nbsp; April 2010 &ndash; July 2010",
    "Senior Customer Service Representative &mdash; Union Bank, Newport Beach, CA&nbsp; |&nbsp; May 2008 &ndash; June 2009",
    "Operations Specialist &mdash; TVT Community Day School, Irvine, CA&nbsp; |&nbsp; June 2006 &ndash; August 2012",
])

# Education
story += section("Education")
story.append(Paragraph("<b>Master of Business Administration (MBA), IT Management</b> &mdash; Western Governors University", styles["body"]))
story.append(Paragraph("<b>Bachelor of Science (BS), Psychology</b> &mdash; University of Minnesota, Minneapolis, MN", styles["body"]))
story.append(Paragraph("Honors: Three University Excellence Awards (Ethical Leadership; Organizational Management)", styles["body"]))

# Certifications
story += section("Certifications")
story.append(Paragraph(
    "Certified ScrumMaster (CSM) &ndash; Scrum Alliance&nbsp;|&nbsp; Google Project Management&nbsp;|&nbsp; "
    "Google Data Analytics&nbsp;|&nbsp; Google Business Intelligence&nbsp;|&nbsp; IBM AI Engineering&nbsp;|&nbsp; "
    "IBM Data Science&nbsp;|&nbsp; IBM Data Analyst&nbsp;|&nbsp; Data Analysis &amp; Visualization Foundations (IBM)&nbsp;|&nbsp; "
    "Microsoft Project Management&nbsp;|&nbsp; Microsoft Program Management&nbsp;|&nbsp; ADP Payroll Specialist&nbsp;|&nbsp; "
    "ADP Compensation &amp; Benefits Analyst", styles["body"]))

doc = BaseDocTemplate(OUT, pagesize=LETTER,
                      leftMargin=0.6*inch, rightMargin=0.6*inch,
                      topMargin=0.5*inch, bottomMargin=0.5*inch,
                      title="Andrew Perez - Resume", author="Andrew Perez")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame])])
doc.build(story)
print("Wrote", OUT)
