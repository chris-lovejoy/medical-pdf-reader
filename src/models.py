from langchain import OpenAI, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents import Tool
from langchain.tools import DuckDuckGoSearchRun


import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key

huggingface_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_api_token


### EMBEDDINGS

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)


# (1) EXTRACT

remove_symbols_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
)

identify_acronyms_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
)

remove_acronyms_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
)

replace_acronyms_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
)


# (2) PARSE

# TODO: consider a medical LLM for the clinical JSON parsing
clinical_parsing_llm = ChatOpenAI(
    # model_name="gpt-4",
    model_name="gpt-3.5-turbo",
    temperature=0,
)

# Alternative, non-chat model
# clinical_parsing_llm = OpenAI(
#     model_name="text-davinci-003",
#     temperature=0,
#     openai_api_key=openai_api_key
# )



# (3) EXTRACT AND QUERY

extract_info_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.0,
)

answer_query_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.0,
)

# Alternative clinical LLM for query task
# answer_query_llm = HuggingFaceHub(
#     repo_id="emilyalsentzer/Bio_ClinicalBERT",
#     model_kwargs={"temperature": 0, "max_length": 64},
#     task="text-generation"
# )

specify_source_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.0,
)

evaluate_confidence_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.0,
)



# (4) CLINICAL EVALUATION

clinical_eval_llm = OpenAI(
    temperature=0.0,
)

# Alternative clinical LLM for query task
# clinical_eval_llm = HuggingFaceHub(
#     repo_id="emilyalsentzer/Bio_ClinicalBERT",
#     model_kwargs={"temperature": 0, "max_length": 64},
#     task="text-generation"
# )

treatment_plan_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0.0,
)


search = DuckDuckGoSearchRun()
clinical_eval_tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
]
