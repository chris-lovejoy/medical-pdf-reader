from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain import LLMChain

from .. import prompts
from .. import models

class QueryClinicalJSON():
    """
    This object can be used to extract information answer queries based on 
    structured clinical text.
    """
    def __init__(self, clinical_json):
        self.clinical_json = clinical_json
        self.extract_info_llm = models.extract_info_llm
        self.answer_query_llm = models.answer_query_llm
        self.specify_source_llm = models.specify_source_llm
        self.evaluate_confidence_llm = models.evaluate_confidence_llm
        self.extract_chain_type = "stuff"
        self.query_chain_type = "stuff"
        self.medical_record_extracts = self.extract_strings_from_clinical_json()
        self.vectorstore = FAISS.from_texts(self.medical_record_extracts, OpenAIEmbeddings())
        self.extracted_responses = {}
        self.query_responses = []

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

    def answer_query(self, query):
        """
        This function uses retrieval-augmented question-answering to answer
        a query (as True/False). It uses the specify_source_quote and evaluate_confidence
        functions to also identify the precise relevant part of the medical
        record and a confidence score for the answer.
        """

        if self.query_chain_type == "map_reduce":            
            chain_type_kwargs = {"question_prompt": prompts.answer_query_map_prompt,
                    "combine_prompt": prompts.answer_query_combine_prompt}
        elif self.query_chain_type == "stuff":
            chain_type_kwargs = {"prompt": prompts.answer_query_stuff_prompt}
        else:
            chain_type_kwargs = {}

        # Define question-answering chain for query
        qa = RetrievalQA.from_chain_type(
            llm=self.answer_query_llm,
            chain_type=self.query_chain_type, 
            retriever=self.vectorstore.as_retriever(search_kwargs=dict(k=3)),
            chain_type_kwargs=chain_type_kwargs,
            return_source_documents=True
            # verbose=True,
        )

        # Get result from query
        result = qa({"query": query})
        answer = result['result']
        answer = self.enforce_true_false(answer)

        # Extract precise source quote
        source_docs = result['source_documents']
        source_quote = self.specify_source_quote(query, answer, source_docs)

        # Get confidence score
        confidence_score = self.evaluate_confidence(query, answer, source_quote)

        # Define dictionary entry and append to query responses
        query_response_dict = {
            "query": query,
            "answer": answer,
            "source_quote": source_quote,
            "confidence_score": confidence_score
        }
        self.query_responses.append(query_response_dict)

    def specify_source_quote(self, query, answer, source_docs):
        """
        Identifies the specific quoted source from the patient record which
        supports the answer to the query.
        NOTE: In future, could look to map this to source content more explicitly.
        """

        # Join source content across all of the source docs used by the retrieval QA chain
        source_content = "\n".join([doc.page_content for doc in source_docs])

        # Specify and execute chain
        llm_chain = LLMChain(
            llm=self.specify_source_llm,
            prompt=prompts.specify_source_prompt
        )
        source_quote = llm_chain.apply([
            {
            "query": query,
            "answer": answer,
            "source_content": source_content
            },
        ])
    
        return source_quote[0]['text']


    def evaluate_confidence(self, query, answer, source_quote):
        """
        Provides a confidence evaluation based only on the answer and the 
        extracted source quote to support it.
        (So if source quote not appropriate, confidence score will be low.)
        """
    
        # Specify and execute chain
        llm_chain = LLMChain(
            llm=self.evaluate_confidence_llm,
            prompt=prompts.evaluate_confidence_prompt
        )
        confidence_score = llm_chain.apply([
            {
            "query": query,
            "answer": answer,
            "source_quote": source_quote
            },
        ])
    
        return confidence_score[0]['text']
    
    def enforce_true_false(self, answer):
        """
        This function looks for 'true' or 'false' in the LLM response 
        text and converts it into a boolean True or False. This helps
        to handle LLM variations such as "True." or "True, because..."
        """
        if "true" in answer.lower():
            return True
        elif "false" in answer.lower():
            return False
        else:
            return None # TODO: test that None is handled okay. If not use "" or alternative

    def extract_strings_from_clinical_json(self):
        """
        This function converst the dictionary elements in clinical_json
        into strings with the following format:
            "{key name} (extracts from medical record): {value}"
        For example:
            "chief complaint (extracts from medical record): hemorrhoids"
        """
        extracts = []
        for key, value in self.clinical_json.items():
            extracts.append(f"{key.replace('_',' ')} (extract from medical record): {value}")
        return extracts
