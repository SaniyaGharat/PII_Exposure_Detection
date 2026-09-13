"""
PII Exposure Detection - PDF Document Generator
Generates clean, readable PDF documents from structured text content using ReportLab.
"""

from pathlib import Path
from typing import Union
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted


def generate_pdf_from_text(
    text_content: str,
    output_pdf_path: Union[str, Path],
    title: str = "Document"
) -> Path:
    """
    Renders structured text into a cleanly styled, readable PDF document.

    Args:
        text_content: The text content of the document.
        output_pdf_path: Destination path for the .pdf file.
        title: Document title for metadata.

    Returns:
        Path to the generated PDF.
    """
    output_path = Path(output_pdf_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=title,
    )

    styles = getSampleStyleSheet()

    # Define custom styles
    header_style = ParagraphStyle(
        name="DocHeader",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        alignment=1, # Center
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=12,
    )

    section_style = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceBefore=8,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        name="FormBody",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
    )

    story = []

    # Parse lines to render formatted document elements
    lines = text_content.strip().split("\n")
    current_block = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("===") or stripped.startswith("---"):
            if current_block:
                block_text = "\n".join(current_block)
                story.append(Preformatted(block_text, body_style))
                current_block = []
            story.append(Spacer(1, 4))
        else:
            current_block.append(line)

    if current_block:
        block_text = "\n".join(current_block)
        story.append(Preformatted(block_text, body_style))

    doc.build(story)
    return output_path
