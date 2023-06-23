
from .. import prompts
from .. import config

class QueryClinicalJSON():
    """
    This object can be used to extract information answer queries based on 
    structured clinical text.
    """
    def __init__(self, clinical_json):
        self.clinical_json = clinical_json
        self.extract_info_llm = config.extract_info_llm
        self.answer_query_llm = config.answer_query_llm
        self.specify_source_llm = config.specify_source_llm
        self.evaluate_confidence_llm = config.evaluate_confidence_llm