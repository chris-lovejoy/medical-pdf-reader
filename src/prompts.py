from langchain.prompts.prompt import PromptTemplate


remove_symbols_prompt_template = """Please return an exact copy of the following text, but where words include symbols, use the surrounding context to identify the appropriate word and replace the word with symbols with the appropriate word.

    EXTRACTED TEXT: {context}

    Please clean and return an exact copy of the full text.

    CLEAN EXTRACTED TEXT: """

remove_symbols_prompt = PromptTemplate(
    template=remove_symbols_prompt_template, input_variables=["context"]
)

identify_acronyms_prompt_template = """Please identify all the medical acronyms in the following text and return them as a list.

        EXTRACTED TEXT: {context}

        Please return the acronyms in as a list, for example: BTW, NIMBY, NA, HPC

        ACRONYMS: """

identify_acronyms_prompt = PromptTemplate(
    template=identify_acronyms_prompt_template, input_variables=["context"]
)

replace_acronyms_prompt_template = """Please return an exact copy of the following text, but replace the following acronyms with expanded words where you can. Use the surrounding context to identify the appropriate expanded acronym and replace it. If you're not sure, just leave the original arconym.

        EXTRACTED TEXT: {context}
        ACRONYMS: {list_of_acronyms}

        Please replace return an exact copy of the full text with the full text instead of the acronyms.

        EXTRACTED TEXT WITH EXPANDED ACRONYMS: """

replace_acronyms_prompt = PromptTemplate(
    template=replace_acronyms_prompt_template, input_variables=["context", "list_of_acronyms"]
)