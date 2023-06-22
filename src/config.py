from langchain import OpenAI
from langchain.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# (1) EXTRACT

remove_symbols_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    openai_api_key=openai_api_key
    )

identify_acronyms_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    openai_api_key=openai_api_key
    )

remove_acronyms_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    openai_api_key=openai_api_key
    )


# (2) PARSE

# TODO: consider a medical LLM for the clinical JSON parsing
clinical_parsing_llm = ChatOpenAI(
        # model_name="gpt-4",
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=openai_api_key,
    )

# clinical_parsing_llm = OpenAI(
#     model_name="text-davinci-003",
#     temperature=0,
#     openai_api_key=openai_api_key
# )
