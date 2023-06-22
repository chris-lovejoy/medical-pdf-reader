"""This file extracts and cleans text from the medical record PDF"""


from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean, clean_non_ascii_chars

from langchain import LLMChain

from .. import config
from .. import prompts


class PDFtoText:
    """
    This object extracts and cleans text from a medical record PDF at the specified
    directory.
    """
    def __init__(self, pdf_dir):
        self.dir = pdf_dir
        self.initial_text = None
        self.clean_text = None
        self.remove_symbols_llm = config.remove_symbols_llm        
    
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


    def clean_initial_text_llm(self):
        """
        This function uses LLMs to clean the extracted text, by calling other LLM helper
        scripts below.
        NOTE: this must be run after clean_initial_auto
        """
        # Use LLM to remove artefact symbols from document
        clean_text = self.remove_symbols_with_llm()

        # Use LLM to expand out acronyms
        # clean_text = self.expand_acronyms_with_llm(clean_text)

        # TODO: consider implementing LLM call to fix spelling and grammatical mistakes

        # TODO: consider adding some safety fallback mechanisms - so that if a method of cleaning
        # provides a wildly different (e.g. much shorter) output, then it just sticks with the
        # 'unclean' original

        self.clean_text = clean_text


    def remove_symbols_with_llm(self):
        """
        This function uses LLMs to remove symbol artefacts from the initial extraction
        from the PDF.
        """

        # TODO: update this for handling longer texts, by dividing up the text into chunks
    
        llm_chain = LLMChain(
            llm=self.remove_symbols_llm,
            prompt=prompts.remove_symbols_prompt
        )
        clean_extracted_text = llm_chain.apply([{"context": self.clean_text}])

        return clean_extracted_text[0]['text']


    def expand_acronyms_with_llm(clean_text):
        return None