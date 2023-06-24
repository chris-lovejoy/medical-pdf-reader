
class ClinicalEval():
    """
    This object can be used to evaluate the whether a clinical decision
    is appropriate.
    """
    def __init__(self, clinical_json, query_responses):

        # Load required variables
        self.clinical_json = clinical_json
        self.query_responses = query_responses
        

