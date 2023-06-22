"""This file extracts and cleans text from the medical record PDF"""


from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean, clean_non_ascii_chars

class PDFtoText:
    """
    This object extracts and cleans text from a medical record PDF at the specified
    directory.
    """
    def __init__(self, pdf_dir):
        self.dir = pdf_dir
        self.initial_text = None
        self.clean_text = None
        
    
    def load_initial_text(self):
        """
        This function loads the initial text from the PDF using the unstructured library.
        """
        elements = partition_pdf(self.dir, ocr_languages="eng", include_page_breaks=False)
        text = ""
        for element in elements:
            text += "\n" + str(element)
        self.initial_text = text

    def clean_initial_text_auto(self):
        """
        This function uses the unstructured library to clean the initial text
        """
        # Declare clean text variable to pass through into subsequent functions
        clean_text = self.initial_text

        # Use unstructured library cleaner functions
        clean_text = clean(clean_text, dashes=True, bullets=True, 
                           lowercase=False, extra_whitespace=False)
        clean_text = clean_non_ascii_chars(clean_text)

        # TODO: Consider adding alternative methods of cleaning too, such as unstructured
        # library cleaning functions and spacy functions as per this article:
        # https://www.analyticsvidhya.com/blog/2021/06/data-extraction-from-unstructured-pdfs/

        self.clean_text = clean_text
