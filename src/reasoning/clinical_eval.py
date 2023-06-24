from langchain import LLMChain

from .. import models
from .. import prompts


class ClinicalEval():
    """
    This object can be used to evaluate the whether a clinical decision
    is appropriate.
    """
    def __init__(self, clinical_json, query_responses):

        # Load required variables
        self.clinical_json = clinical_json
        self.query_responses = query_responses
        
        # Extract treatment plan
        self.treatment_plan_llm = models.treatment_plan_llm
        self.treatment_plan = self.get_major_treatment()



    def get_major_treatment(self):

        llm_chain = LLMChain(
            llm=self.treatment_plan_llm,
            prompt=prompts.treatment_plan_prompt
        )
        extracted_key_treatment = llm_chain.apply([{"treatment_plan": self.clinical_json['treatment_plan']}])

        return extracted_key_treatment[0]['text']

