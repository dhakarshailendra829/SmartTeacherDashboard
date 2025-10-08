from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import pandas as pd
from datetime import datetime

def _make_paragraph(text, style_name="Normal"):
    styles = getSampleStyleSheet()
    return Paragraph(text, styles[style_name])

def generate_pdf_report(student_name, student_id, summary: dict, timeline_df: pd.DataFrame, images: dict):
    """
    Returns PDF bytes (in-memory) for download.
    images: dict of name -> BytesIO PNG buffers
    summary: dict with keys total_quizzes, total_thoughts, correct_total, wrong_total
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, fontSize=18, spaceAfter=14)
    normal = styles['Normal']

    # Title
    elements.append(Paragraph(f"Student Progress Report", title_style))
    elements.append(Paragraph(f"Name: <b>{student_name}</b>", normal))
    elements.append(Paragraph(f"Student ID: <b>{student_id}</b>", normal))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal))
    elements.append(Spacer(1, 12))

    summary_table_data = [
        ["Total Quizzes", summary.get("total_quizzes", 0)],
        ["Average Score", summary.get("avg_score", 0)],
        ["Total Thoughts", summary.get("total_thoughts", 0)],
        ["Total Correct Answers (approx)", summary.get("correct_total", 0)],
        ["Total Wrong Answers (approx)", summary.get("wrong_total", 0)]
    ]
    t = Table(summary_table_data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    if images.get('scores_png'):
        elements.append(Paragraph("Quiz Scores Over Time", styles['Heading2']))
        images['scores_png'].seek(0)
        img = Image(images['scores_png'], width=450, height=250)
        elements.append(img)
        elements.append(Spacer(1, 12))

    if images.get('correct_wrong_png'):
        elements.append(Paragraph("Correct vs Wrong", styles['Heading2']))
        images['correct_wrong_png'].seek(0)
        img2 = Image(images['correct_wrong_png'], width=350, height=200)
        elements.append(img2)
        elements.append(Spacer(1, 12))

    if not timeline_df.empty:
        elements.append(Paragraph("Activity Timeline (most recent first)", styles['Heading2']))
        td = timeline_df.copy()
        td['DateTime'] = td['DateTime'].astype(str)
        table_data = [["DateTime", "Type", "Detail"]]
        for _, r in td.head(50).iterrows():
            table_data.append([r['DateTime'], r['Type'], str(r['Detail'])])
        tbl = Table(table_data, colWidths=[150, 80, 240])
        tbl.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ]))
        elements.append(tbl)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
