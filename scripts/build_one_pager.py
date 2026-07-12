"""Generate the print-ready one-page hiring brief."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ONE_PAGER.pdf"
NAVY = colors.HexColor("#0B1D33")
TEAL = colors.HexColor("#0E7C7B")
AMBER = colors.HexColor("#C97F0A")
MUTED = colors.HexColor("#51606F")
LIGHT = colors.HexColor("#EEF1F4")

base = ParagraphStyle("base", fontName="Helvetica", fontSize=8.7, leading=11.3, textColor=NAVY)
small = ParagraphStyle("small", parent=base, fontSize=7.6, leading=9.4, textColor=MUTED)
section = ParagraphStyle("section", parent=base, fontName="Helvetica-Bold", fontSize=10.5,
                         leading=12.5, textColor=TEAL, spaceBefore=4, spaceAfter=3)
title = ParagraphStyle("title", parent=base, fontName="Helvetica-Bold", fontSize=20,
                       leading=22, textColor=colors.white)
kpi = ParagraphStyle("kpi", parent=base, fontName="Helvetica-Bold", fontSize=20,
                     leading=21, alignment=TA_CENTER, textColor=TEAL)
kpi_sub = ParagraphStyle("kpi_sub", parent=small, alignment=TA_CENTER, fontSize=7.5)

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=15*mm, leftMargin=15*mm,
                        topMargin=12*mm, bottomMargin=11*mm, title="Walmart Holiday Sales Decision Brief")

story = []
header = Table([[Paragraph("Walmart Holiday Sales", title),
                 Paragraph("DECISION BRIEF<br/><font color='#C7D0D8'>45 stores | 143 weeks | 2010-2012</font>",
                           ParagraphStyle("hdr", parent=small, alignment=2, textColor=colors.white))]],
               colWidths=[120*mm, 60*mm])
header.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                            ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [header, Spacer(1, 5*mm)]
story += [Paragraph("THE QUESTION", section), Paragraph(
    "Where is holiday-period sales strength credible enough to test, and which forecasting approach should planners use as a starting point? The data has no price, discount, margin, or product fields, so this work does <b>not</b> claim price elasticity or markdown ROI.", base)]
story += [Paragraph("APPROACH", section), Paragraph(
    "A reproducible pipeline combines SQL analysis, uncertainty testing, store-level regression, a time-ordered forecast holdout, automated quality checks, and a six-view decision dashboard.", base), Spacer(1, 3*mm)]

kpis = Table([
    [Paragraph("7.84%", kpi), Paragraph("7 of 45", kpi), Paragraph("1.87%", kpi)],
    [Paragraph("overall flagged-week lift", kpi_sub), Paragraph("stores pass the nominal screen<br/>(0 after multiple-test correction)", kpi_sub), Paragraph("aggregate holdout MAPE<br/>for feature OLS", kpi_sub)]],
    colWidths=[60*mm]*3)
kpis.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),LIGHT),("BOX",(0,0),(-1,-1),.6,colors.HexColor('#DAE0E6')),
                          ("INNERGRID",(0,0),(-1,-1),.4,colors.HexColor('#DAE0E6')),
                          ("TOPPADDING",(0,0),(-1,0),7),("BOTTOMPADDING",(0,0),(-1,0),1),
                          ("TOPPADDING",(0,1),(-1,1),2),("BOTTOMPADDING",(0,1),(-1,1),7)]))
story += [kpis, Spacer(1, 3*mm)]

finding_data = [
    ["1", "Overall signal", "Flagged weeks average 7.84% above regular weeks (95% interval: 2.08% to 13.67%; p=0.0259). This is an association based on only 10 calendar weeks, not a causal markdown effect."],
    ["2", "Store 7 pilot candidate", "Store 7 has 19.44% observed lift (95% interval: 4.20% to 36.46%; nominal p=0.0166). It is the clearest candidate for a controlled test, not an automatic rollout."],
    ["3", "Simple models still matter", "Feature OLS wins the aggregate holdout (1.87% vs 2.24% MAPE), but seasonal naive wins 22 of 46 scopes. Model choice should remain store-specific."],
]
rows=[]
for n, head, body in finding_data:
    rows.append([Paragraph(f"<font color='#C97F0A'><b>{n}</b></font>", section),
                 Paragraph(f"<b>{head}</b><br/>{body}", base)])
findings=Table(rows,colWidths=[10*mm,170*mm])
findings.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),.4,colors.HexColor('#DAE0E6')),
                              ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
story += [Paragraph("THREE DECISION FINDINGS", section), findings]

callout = Table([[Paragraph("DATA-QUALITY WATCHOUT", ParagraphStyle("callhead",parent=small,fontName="Helvetica-Bold",textColor=AMBER)),
                  Paragraph("The dataset's 'Christmas' flag is actually the week after Christmas. Those two weeks average 7.7% below regular weeks, so treating the flag as Christmas demand would mislead planning.", base)]],
                colWidths=[42*mm,138*mm])
callout.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor('#FBF0DD')),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                             ("BOX",(0,0),(-1,-1),.6,AMBER),("LEFTPADDING",(0,0),(-1,-1),7),
                             ("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story += [Spacer(1, 3*mm), callout]
story += [Paragraph("RECOMMENDATION", section), Paragraph(
    "Run a controlled holiday-markdown pilot at Store 7 with matched comparison stores and margin-aware success metrics. Treat all store findings as exploratory because none survives correction for testing 45 stores. Keep seasonal naive as the governance baseline and adopt the feature model only where repeated backtests show a durable advantage.", base)]
story += [Paragraph("WITH MORE DATA AND TIME", section), Paragraph(
    "Add product-level price, units, markdown depth, margin, inventory and control groups; then use rolling forecast backtests and a causal pilot design.", base)]
story += [Spacer(1, 2*mm), Paragraph("Source: Walmart Store Sales Forecasting data. Reproducible outputs and assumptions are documented in the project repository.", small)]

doc.build(story)
print(f"Built {OUT}")
