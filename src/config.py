from langchain import OpenAI
from langchain.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

remove_symbols_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    openai_api_key=openai_api_key
    )
