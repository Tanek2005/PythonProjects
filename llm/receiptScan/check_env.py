from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file.

    :param pdf_path: Path to the PDF file.
    :return: A single string containing all text from the PDF.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

print(extract_text_from_pdf('pdfs/rs.pdf'))