from langchain import LLMChain, OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain.docstore import InMemoryDocstore
from langchain.agents import ZeroShotAgent, AgentExecutor
import faiss

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

        # Perform clinical evaluation
        self.clinical_eval_llm = models.clinical_eval_llm
        self.clinical_eval_tools = models.clinical_eval_tools


    def evaluate_treatment_plan(self):

        # Initialise the vector store
        embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
        index = faiss.IndexFlatL2(embedding_size)
        embedding_fn = OpenAIEmbeddings().embed_query
        vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})
        retriever = vectorstore.as_retriever(search_kwargs=dict(k=4))
        memory = VectorStoreRetrieverMemory(retriever=retriever, memory_key="context")

        # Add memory objects
        memory = self.load_query_responses(memory)

        # Define custom prompt
        prefix = """Answer the following questions as best you can. You have access to the following tools:"""
        suffix = """Begin!"

            MEDICAL HISTORY:
            {context}

            Question: {input}
            {agent_scratchpad}"""
        clinical_eval_prompt = ZeroShotAgent.create_prompt(
            self.clinical_eval_tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "context", "agent_scratchpad"],
        )

        # Define agent chain and run
        llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=clinical_eval_prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=self.clinical_eval_tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=self.clinical_eval_tools, verbose=True, memory=memory
        )

        result = agent_chain.run(input=f"Is the treatment plan '{self.treatment_plan}' appropriate for someone with this medical history?")

        return result


    def get_major_treatment(self):

        if 'treatment_plan' in self.clinical_json:
            llm_chain = LLMChain(
                llm=self.treatment_plan_llm,
                prompt=prompts.treatment_plan_prompt
            )
            extracted_key_treatment = llm_chain.apply([{"treatment_plan": self.clinical_json['treatment_plan']}])

            return extracted_key_treatment[0]['text']

        else:
            raise Exception("No treatment plan found in clinical JSON.")


    def load_query_responses(self, memory):

        for query_response in self.query_responses:
            memory.save_context({"input": query_response['query']},
                                {"output": query_response['answer']})

        return memory


        