from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

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
        self.extract_chain_type = "stuff"
        self.query_chain_type = "stuff"
        self.medical_record_extracts = self.extract_strings_from_clinical_json()
        self.vectorstore = FAISS.from_texts(self.medical_record_extracts, OpenAIEmbeddings())
        self.extracted_responses = {}


    def extract_info(self, info_to_extract):
        """
        This function uses retrieval-augmented question-answering to extract
        the specified information from the structured clinical text (a form of
        extractive summarisation).
        """
        
        if self.extract_chain_type == "map_reduce":            
            chain_type_kwargs = {"question_prompt": prompts.info_extraction_map_prompt,
                    "combine_prompt": prompts.info_extraction_combine_prompt}
        elif self.extract_chain_type == "stuff":
            chain_type_kwargs = {"prompt": prompts.info_extraction_stuff_prompt}
        else:
            chain_type_kwargs = {}

        # Define question-answering chain for extraction
        qa = RetrievalQA.from_chain_type(
            llm=self.extract_info_llm,
            chain_type=self.extract_chain_type, 
            retriever=self.vectorstore.as_retriever(search_kwargs=dict(k=3)),
            chain_type_kwargs=chain_type_kwargs,
            return_source_documents=False
            # verbose=True,
        )

        # Get result from query
        result = qa({"query": info_to_extract})

        # Save extracted response in a dictionary
        self.extracted_responses[info_to_extract] = result['result']