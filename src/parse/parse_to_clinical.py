import itertools
import copy

from langchain.text_splitter import RecursiveCharacterTextSplitter
from kor import extract_from_documents, from_pydantic, create_extraction_chain

from .DataModels import ClinicalJSON
from .. import config


class TextToClinicalJSON():
    """
    An abstract class for extracting information from medical text into a structured clinical format.
    """
    def __init__(self, text):
        self.text = text
        self.schema, self.validator = from_pydantic(
            ClinicalJSON,
            description="Extract information from medical text into a structured clinical format.",
            # TODO consider writing an example (as per https://eyurtsev.github.io/kor/document_extraction.html)
        )
        self.clinical_parsing_llm = config.clinical_parsing_llm
        self.text_splitter = RecursiveCharacterTextSplitter() 
        self.chunked_parsing = None
        self.combined_parsing = None
        self.clinical_json = None

    
    async def parse_text_to_clinical_json(self):
        """
        This function calls the below helper functions to convert from an extracted text string
        into a structured clinical JSON format with the schema defined in the pydantic data model.
        """
        self.chunk_and_parse_doc()
        # self.combine_parsed_chunks()
        # self.clean_clinical_json()

    async def chunk_and_parse_doc(self):
        """
        This function chunks the single text string (using the RecursiveCharacterTextSplitter) and 
        then splits each chunk into the appropriate sections of the clinical JSON format
        accoring to the pydantic model schema. Uses the kor library (https://eyurtsev.github.io/kor/).
        The output is a list of dictionaries (one dictionary for each chunk).
        """

        chain = create_extraction_chain(
            self.clinical_parsing_llm, self.schema, 
            encoder_or_encoder_class="json", validator=self.validator
        )
        # NOTE: kor library passes the following warning here:
            # "UserWarning: The apredict_and_parse method is deprecated, instead pass an output parser directly to LLMChain"

        split_text = self.text_splitter.create_documents([self.text])

        document_extraction_results = await extract_from_documents(
            chain, split_text, max_concurrency=5, use_uid=False, return_exceptions=True
        )

        validated_data = list(
                itertools.chain.from_iterable(
                    extraction["validated_data"] for extraction in document_extraction_results
                )
            )
    
        self.chunked_parsing = validated_data
    
