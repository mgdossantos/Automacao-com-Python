from pathlib import Path
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

PDF_FOLDER = Path("relatorios/pdf")
PDF_FOLDER.mkdir(parents=True, exist_ok=True)


def generate_pdf(summary, chart_path, highlights, report_date):
    pdf_file = PDF_FOLDER / f"report_{report_date}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_file),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        spaceAfter=10
    )

    normal_style = styles["Normal"]

    elements = []

    elements.append(Paragraph("Relatório Automático de Mercado", styles["Title"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Data do relatório: {report_date}", normal_style))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Resumo Executivo", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Maior alta:</b> {highlights['top_gainer']['ticker']} "
            f"({highlights['top_gainer']['percent_change']:.2f}%)",
            normal_style
        )
    )
    elements.append(
        Paragraph(
            f"<b>Maior queda:</b> {highlights['top_loser']['ticker']} "
            f"({highlights['top_loser']['percent_change']:.2f}%)",
            normal_style
        )
    )
    elements.append(
        Paragraph(
            f"<b>Maior volume:</b> {highlights['top_volume']['ticker']} "
            f"({int(highlights['top_volume']['volume']):,})",
            normal_style
        )
    )

    elements.append(Spacer(1, 16))
    elements.append(Paragraph("Gráfico de preços", subtitle_style))

    if chart_path.exists():
        elements.append(Image(str(chart_path), width=16 * cm, height=7 * cm))

    elements.append(Spacer(1, 16))
    elements.append(Paragraph("Tabela resumo", subtitle_style))

    table_data = [[
        "Ticker", "Nome", "Close", "% Variação", "Volume", "Classificação"
    ]]

    for _, row in summary.iterrows():
        table_data.append([
            row["ticker"],
            str(row["name"]),
            f"{row['close']:.2f}" if row["close"] is not None else "",
            f"{row['percent_change']:.2f}" if row["percent_change"] is not None else "",
            f"{int(row['volume']):,}" if pd.notna(row["volume"]) else "",
            row["movement_class"]
        ])

    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#EAF2F8")]),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
    ]))

    elements.append(table)

    doc.build(elements)

    print(f"PDF gerado: {pdf_file}")
    return pdf_file