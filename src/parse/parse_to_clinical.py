

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
  