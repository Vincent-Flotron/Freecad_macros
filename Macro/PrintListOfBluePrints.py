import FreeCAD as App
# import TechDraw
from PySide import QtGui, QtCore
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_plan_list_pdf():
    # Get all TechDraw pages
    doc = App.ActiveDocument
    pages = [obj for obj in doc.Objects if obj.TypeId == 'TechDraw::DrawPage']

    # Extract Label and Label2 from pages and sort by Label
    page_data = sorted([(page.Label, getattr(page, 'Label2', '')) for page in pages], key=lambda x: x[0])

    # Create PDF
    pdf_path = os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation), "Liste des Plans.pdf")
    
    pdf_doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Liste des Plans", styles['Title']))

    # Create table data
    table_data = [['Label', 'Label2']] + page_data

    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Build PDF with the custom cartridge function
    pdf_doc.build(elements, onFirstPage=add_cartridge)

    QtGui.QMessageBox.information(None, "PDF Created", f"The PDF has been created at:\n{pdf_path}")

def add_cartridge(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 12)

    # Draw cartridge
    canvas.rect(50, 50, 500, 150)

    # Add cartridge content
    data = [
        ['Designed By:', 'Escalier Cergnat'],
        ['Wace', 'Liste des Plans'],
        ['Date:', 'Size:'],
        ['19.09.2024', 'A4'],
        ['Made with FreeCAD', ''],
        ['Version number:', 'Sheet:'],
        ['V1', '1 / 60']
    ]

    x, y = 60, 180
    for row in data:
        canvas.drawString(x, y, row[0])
        canvas.drawString(x + 250, y, row[1])
        y -= 20

    # Add horizontal lines
    for i in range(1, 7):
        canvas.line(50, 50 + i * 30, 550, 50 + i * 30)

    # Add vertical line
    canvas.line(300, 50, 300, 200)

    canvas.restoreState()

create_plan_list_pdf()
