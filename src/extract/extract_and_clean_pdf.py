"""This file extracts and cleans text from the medical record PDF"""


from unstructured.partition.pdf import partition_pdf

class PDFtoText:
    """
    This object extracts and cleans text from a medical record PDF at the specified
    directory.
    """
    def __init__(self, pdf_dir):
        self.dir = pdf_dir
        self.initial_text = None
        
    
    def load_initial_text(self):
        """
        This function loads the initial text from the PDF using the unstructured library.
        """
        elements = partition_pdf(self.dir, ocr_languages="eng", include_page_breaks=False)
        text = ""
        for element in elements:
            text += "\n" + str(element)
        self.initial_text = text

    