import FreeCAD as App
from PySide import QtGui, QtCore
from reportlab.lib           import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus      import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles    import getSampleStyleSheet
from reportlab.pdfgen        import canvas
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
import io

mod_to_import = 'MyTools'
if mod_to_import in sys.modules:
    del sys.modules[mod_to_import]
import MyTools
import re

last_page_number = -1
cartridge_data = [
    ['Designed By:', 'Wace'],
    ['Name', 'Liste des Plans'],
    ['Date:', '19.09.2024'],
    ['Size', 'A4'],
    ['Made with:', 'FreeCAD'],
    ['Version number:', 'V1']
]

cartridge_style = [
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.75, colors.black),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]

def create_plan_list_pdf():
    # Get all TechDraw pages
    doc   = App.ActiveDocument
    pages = [obj for obj in doc.Objects if MyTools.obj_is_a_page(obj)]

    # Extract Label and Label2 from pages and sort by Label
    frst_col_name = 'Label'
    seco_col_name = 'Label2'
    col_from_name = {frst_col_name: 0,
                     seco_col_name: 1}
    page_data = sorted([[page.Label, getattr(page, seco_col_name, '')] for page in pages], key=lambda x: x[col_from_name[seco_col_name]])
    pattern = re.compile(r'Page(\d+)')
    # Iterate over the pages and extract the page number
    pages_col = col_from_name[frst_col_name]
    for i in range(len(page_data)):
        match = pattern.search(page_data[i][pages_col])
        # Set page number to first column
        if match:
            page_data[i][pages_col] = int(match.group(1))
        else:
            page_data[i][pages_col] = 0  # Handle the case where the pattern does not match


    # Create PDF
    pdf_path = os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation), "Liste des Plans.pdf")
    
    pdf_doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Liste des Plans", styles['Title']))

    # Create table data
    table_data = [['Page', 'Dessin']] + page_data

    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),      # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # Header text color
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),               # Align first column (index 0) to the right
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),                # Align second column (index 1) to the left
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),   # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 14),                 # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),            # Padding for header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),    # Background for rows
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),     # Text color for rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),       # Font for rows
        ('FONTSIZE', (0, 1), (-1, -1), 12),                # Font size for rows
        ('TOPPADDING', (0, 1), (-1, -1), 6),               # Padding for rows
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),            # Padding for rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black)        # Grid for the entire table
    ]))

    elements.append(table)

    # Build PDF
    pdf_doc.build(elements)

    # Check if there's enough space on the last page for the cartridge
    if has_enough_space_for_cartridge(pdf_path):
        add_cartridge_table(pdf_path)
    else:
        add_cartridge_page(pdf_path)

    # Add page numbers
    add_page_numbers(pdf_path)

    QtGui.QMessageBox.information(None, "PDF Created", f"The PDF has been created at:\n{pdf_path}")

    # Open the PDF file with the default PDF viewer
    QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(pdf_path))
    MyTools.open_file_browser(pdf_path)

def has_enough_space_for_cartridge(pdf_path):
    # Simulate checking the last page of the PDF
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        last_page = reader.pages[-1]
        page_height = last_page.mediabox.height

        # Assume cartridge height is 150 units (you can adjust this)
        cartridge_height = 150

        # Check if there is enough space at the bottom of the page
        return (page_height > cartridge_height + 100)  # Adjust 100 for padding space

def add_cartridge_table(pdf_path):
    # Create a temporary PDF with the cartridge
    temp_pdf_path = os.path.splitext(pdf_path)[0] + "_temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=A4)

    # Create the table object
    table = Table(cartridge_data, colWidths=[150, 350])

    # Define table style
    table.setStyle(TableStyle(cartridge_style))

    # Set the table position on the canvas
    table.wrapOn(c, A4[0], A4[1])
    table.drawOn(c, 50, 50)  # Position at the bottom-left corner of the page

    c.showPage()
    c.save()

    # Combine original PDF and the cartridge PDF
    merge_pdfs(pdf_path, temp_pdf_path)

    # Clean up the temporary PDF
    os.remove(temp_pdf_path)

def merge_pdfs(original_pdf_path, cartridge_pdf_path):
    writer = PdfWriter()

    # Add the original PDF pages
    with open(original_pdf_path, 'rb') as original:
        original_reader = PdfReader(original)
        for page in original_reader.pages:
            writer.add_page(page)

    # Add the cartridge page
    with open(cartridge_pdf_path, 'rb') as cartridge:
        cartridge_reader = PdfReader(cartridge)
        for page in cartridge_reader.pages:
            writer.add_page(page)

    # Save the new PDF with the cartridge added
    with open(original_pdf_path, 'wb') as out_file:
        writer.write(out_file)

def add_page_numbers(pdf_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    page_offset = MyTools.get_highest_page_number(App.ActiveDocument) + 1

    for i, page in enumerate(reader.pages):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("Helvetica", 10)
        
        # Calculate the center of the page
        page_width, page_height = A4
        text = f"Page {page_offset + i}/{page_offset + total_pages - 1}"
        text_width = can.stringWidth(text, "Helvetica", 10)
        x = (page_width - text_width) / 2

        # Draw the centered text
        can.drawString(x, 20, text)
        can.save()

        packet.seek(0)
        new_page = PdfReader(packet).pages[0]
        page.merge_page(new_page)
        writer.add_page(page)

    with open(pdf_path, 'wb') as output_file:
        writer.write(output_file)

def add_cartridge_page(pdf_path):
    # Create a new PDF for the cartridge
    c = canvas.Canvas(pdf_path, pagesize=A4)

    # Create the table object
    table = Table(cartridge_data, colWidths=[150, 350])

    # Define table style
    table.setStyle(TableStyle(cartridge_style))

    # Set the table position on the canvas
    table.wrapOn(c, A4[0], A4[1])
    table.drawOn(c, 50, 50)  # Position at the bottom-left corner of the page

    c.showPage()
    c.save()

    # Open the original PDF to merge
    merge_pdfs(pdf_path, pdf_path)

create_plan_list_pdf()
