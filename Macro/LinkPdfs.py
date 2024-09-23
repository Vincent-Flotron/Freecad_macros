import sys
from PyPDF2 import PdfMerger
import os


# Get the root directory from the command line argument
if len(sys.argv) != 2:
    print(sys.argv)
    print("Usage: LinkPdfs.py <root_directory>")
    sys.exit(56)

root = sys.argv[1]

# Initialize the list of PDFs to merge
pdfs = []
pdfs_to_link_file = os.path.join(root, "pdfsToLink.txt")

# Read the list of PDF files from the text file
with open(pdfs_to_link_file, mode='r') as file:
    line = file.readline()
    while line:
        pdfs.append(line.strip())  # Strip newline characters
        line = file.readline()

# Initialize PdfMerger
merger = PdfMerger()

# Append each PDF to the merger
for pdf in pdfs:
    merger.append(pdf)

# Write the output PDF if there are pages
if merger.pages:
    output_pdf = os.path.join(root, "selected_pages_output.pdf")
    merger.write(output_pdf)
    merger.close()
    print(f"Selected pages exported to '{output_pdf}'\n")
else:
    print("No TechDraw pages were selected for export.\n")
