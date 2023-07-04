"""This file extracts and cleans text from the medical record PDF"""

from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean, clean_non_ascii_chars

import textwrap3

from langchain import LLMChain

from .. import models
from .. import prompts


class PDFtoText:
    """
    This object extracts and cleans text from a medical record PDF at the specified
    directory.
    """
    def __init__(self, pdf_dir):
        self.dir = pdf_dir
        self.chunk_length = 2000
        self.initial_text = None
        self.text_chunks = None
        self.clean_chunks = []
        self.clean_text = None
        self.remove_symbols_llm = models.remove_symbols_llm
        self.identify_acronyms_llm = models.identify_acronyms_llm
        self.replace_acronyms_llm = models.replace_acronyms_llm

    def load_and_clean_text(self):
        """
        This function calls the below functions to complete the full loading and cleaning pipeline.
        """
        self.load_initial_text()
        self.split_text()
        for chunk in self.text_chunks:
            clean_chunk = self.clean_initial_text_auto(chunk)
            cleaner_chunk = self.clean_initial_text_llm(clean_chunk)
            self.clean_chunks.append(cleaner_chunk)
        self.clean_text = ' '.join()

    def load_initial_text(self):
        """
        This function loads the initial text from the PDF using the unstructured library.
        """
        elements = partition_pdf(self.dir, ocr_languages="eng", include_page_breaks=False)
        text = ""
        for element in elements:
            text += "\n" + str(element)
        self.initial_text = text

    def split_text(self):
        """
        This function splits the text into individual sections which can be cleaned separately.
        """
        chunks = textwrap3.wrap(self.initial_text, self.chunk_length)
        self.text_chunks = chunks

    def clean_initial_text_auto(self, chunk):
        """
        This function uses the unstructured library to clean the initial text
        """
        # Declare clean text variable to pass through into subsequent functions
        # clean_text = self.initial_text

        # Use unstructured library cleaner functions
        clean_chunk = clean(chunk, dashes=True, bullets=True, 
                           lowercase=False, extra_whitespace=False)
        clean_chunk = clean_non_ascii_chars(clean_chunk)

        # TODO: Consider adding alternative methods of cleaning too, such as unstructured
        # library cleaning functions and spacy functions as per this article:
        # https://www.analyticsvidhya.com/blog/2021/06/data-extraction-from-unstructured-pdfs/

        return clean_chunk

    def clean_initial_text_llm(self, clean_chunk):
        """
        This function uses LLMs to clean the extracted text, by calling other LLM helper
        scripts below.
        NOTE: this must be run after clean_initial_auto
        """
        # Use LLM to remove artefact symbols from document
        cleaner_chunk = self.remove_symbols_with_llm(clean_chunk)

        # Use LLM to expand out acronyms
        cleaner_chunk = self.expand_acronyms_with_llm(cleaner_chunk)

        # Use LLM to clean spelling and grammar
        # (But commented out as not necessary)
        # clean_text = self.clean_spelling_and_grammar(clean_text)

        # TODO: consider adding some safety fallback mechanisms - so that if a method of cleaning
        # provides a wildly different (e.g. much shorter) output, then it just sticks with the
        # 'unclean' original

        return cleaner_chunk

    def remove_symbols_with_llm(self, clean_chunk):
        """
        This function uses LLMs to remove symbol artefacts from the initial extraction
        from the PDF.
        """

        # TODO: update this for handling longer texts, by dividing up the text into chunks
    
        llm_chain = LLMChain(
            llm=self.remove_symbols_llm,
            prompt=prompts.remove_symbols_prompt
        )
        clean_extracted_text = llm_chain.apply([{"context": clean_chunk}])

        return clean_extracted_text[0]['text']


    def expand_acronyms_with_llm(self, cleaner_chunk):
        """
        This function uses LLMs to expand out medical acronyms in the text.
        It does so in two stages:
        (1) Identify all the acronyms in the text
        (2) Use that list of acronyms to replace the acronyms where possible.
        """

        # TODO: consider an alternative implementation:
        # (1) identify all acronyms in the text (using an LLM)
        # (2) define a mapping of acronyms to full words as a dictionary/JSON and return it (using an LLM, 
        #       which can see the wider context of the acronyms. perhaps with few shot examples)
        # (3) then, apply that mapping to the text (not using an LLM)
        # TODO: also, consider modifying to a medical-specific model here -> probably using langchain

        llm_chain = LLMChain(
            llm=self.identify_acronyms_llm,
            prompt=prompts.identify_acronyms_prompt
        )
        list_of_acronyms = llm_chain.apply([{"context": cleaner_chunk}])

        llm_chain = LLMChain(
            llm=self.replace_acronyms_llm,
            prompt=prompts.replace_acronyms_prompt
        )
        clean_expanded_text = llm_chain.apply([{"context": cleaner_chunk, "list_of_acronyms": list_of_acronyms}])

        return clean_expanded_text[0]['text']

    
    # def clean_spelling_and_grammar(self, clean_text):

        # NOTE: not implemented, as model is already doing this without being explicitly asked,
        # in the other "cleaning" functions.

    #     return clean_fixed_text[0]['text']
