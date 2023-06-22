from langchain.prompts.prompt import PromptTemplate


remove_symbols_prompt_template = """Please return an exact copy of the following text, but where words include symbols, use the surrounding context to identify the appropriate word and replace the word with symbols with the appropriate word.

    EXTRACTED TEXT: {context}

    Please clean and return an exact copy of the full text.

    CLEAN EXTRACTED TEXT: """

remove_symbols_prompt = PromptTemplate(
    template=remove_symbols_prompt_template, input_variables=["context"]
)
