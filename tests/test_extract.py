import pytest
from src.extract.extract_and_clean_pdf import PDFtoText

pdf_dir = "./data/medical-record.pdf"

def test_extractor_init():
    """
    Tests the initialisation of the PDFtoText extractor class
    """
    extractor = PDFtoText(pdf_dir)
    assert extractor.dir == pdf_dir
