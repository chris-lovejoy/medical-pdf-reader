from langchain.prompts.prompt import PromptTemplate


## ============== Cleaning the text extracted from PDF =============== ##

REMOVE_SYMBOLS_PROMPT_TEMPLATE = """Please return an exact copy of the following text, but where words include symbols, use the surrounding context to identify the appropriate word and replace the word with symbols with the appropriate word.

EXTRACTED TEXT: {context}

Please clean and return an exact copy of the full text.

CLEAN EXTRACTED TEXT: """
remove_symbols_prompt = PromptTemplate(
    template=REMOVE_SYMBOLS_PROMPT_TEMPLATE, input_variables=["context"]
)

IDENTIFY_ACRONYMS_PROMPT_TEMPLATE = """Please identify all the medical acronyms in the following text and return them as a short list.

EXTRACTED TEXT: {context}

Please return only the medical acronyms, as a list of acronyms, for example: CPR, COPD, MRI, ECG

ACRONYMS: """
identify_acronyms_prompt = PromptTemplate(
    template=IDENTIFY_ACRONYMS_PROMPT_TEMPLATE, input_variables=["context"]
)

REPLACE_ACRONYMS_PROMPT_TEMPLATE = """Please return an exact copy of the following text, but replace the following acronyms with expanded words where you can. Use the surrounding context to identify the appropriate expanded acronym and replace it. If you're not sure, just leave the original arconym.

EXTRACTED TEXT: {context}
ACRONYMS: {list_of_acronyms}

Please replace return an exact copy of the full text with the full text instead of the acronyms.

EXTRACTED TEXT WITH EXPANDED ACRONYMS: """
replace_acronyms_prompt = PromptTemplate(
    template=REPLACE_ACRONYMS_PROMPT_TEMPLATE,
    input_variables=["context", "list_of_acronyms"]
)

## ====== Extracting and querying info from the clinical JSON ======= ##

INFO_EXTRACTION_STUFF_PROMPT_TEMPLATE = """Please extract the information about the following from that patient's medical record: {question}
         
Segments of the medical record:
{context}

{question}: """
# Statements that hindered performance, so I removed them:
    # Please answer, using exact copies of the relevant parts of the text where appropriate.
    # If you can't find the information, just say that you can't find it,
    # don't try to make up an answer.
    # Please provide your answer as the exact specific text segment extracted
    # from the medical record. 
info_extraction_stuff_prompt = PromptTemplate(
    template=INFO_EXTRACTION_STUFF_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

INFO_EXTRACTION_MAP_PROMPT_TEMPLATE = """Use the following portion of a medical record to see if any of the text is related to a specific topic.
        
Return any relevant parts as exact quotes, without any modification. If you can't find relevant information, just say that you can't find it, don't try to make up an answer.

{context}

Specific topic: {question}

Relevant text, if any: """
info_extraction_map_prompt = PromptTemplate(
    template=INFO_EXTRACTION_MAP_PROMPT_TEMPLATE, 
    input_variables=["context", "question"]
)

INFO_EXTRACTION_COMBINE_PROMPT_TEMPLATE = """Given the following extracted parts of a medical record, provide a relevant extract for this topic: {question}

Return the relevant part as an exact quote, without any modification.

=========
{summaries}
=========

Specific extract: """
info_extraction_combine_prompt = PromptTemplate(
    template=INFO_EXTRACTION_COMBINE_PROMPT_TEMPLATE, 
    input_variables=["summaries", "question"]
)

ANSWER_QUERY_STUFF_PROMPT_TEMPLATE = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Please provide your answer as either True or False.

Question: {question}
Answer (True or False): """
answer_query_stuff_prompt = PromptTemplate(
    template=ANSWER_QUERY_STUFF_PROMPT_TEMPLATE, 
    input_variables=["context", "question"]
)

ANSWER_QUERY_MAP_PROMPT_TEMPLATE = """Use the following portion of a medical record to see if any of the text is related to a specific topic.
        
Return any relevant parts as exact quotes, without any modification. If you can't find relevant information, just say that you can't find it, don't try to make up an answer.

{context}

Specific topic: {question}

Relevant text, if any: """
answer_query_map_prompt = PromptTemplate(
    template=ANSWER_QUERY_MAP_PROMPT_TEMPLATE, 
    input_variables=["context", "question"]
)

ANSWER_QUERY_COMBINE_PROMPT_TEMPLATE = """Given the following extracted parts of a medical record, answer this question: {question}

If you don't know the answer, just say that you don't know, don't try to make up an answer.

=========
{summaries}
=========

Answer: """
answer_query_combine_prompt = PromptTemplate(
    template=ANSWER_QUERY_COMBINE_PROMPT_TEMPLATE, 
    input_variables=["summaries", "question"]
)

SPECIFY_SOURCE_PROMPT_TEMPLATE = """Extract the exact specific text segment which supports the answer shown below and nothing more. If you can't see an appropriate quote, just say that you don't know, don't try to make up an answer.

Extracts from the document:
{source_content}

Query: {query}
Answer: {answer}

Please provide your answer as the exact specific text segment extracted from the document.

Specific Supporting Text Segments: """
specify_source_prompt = PromptTemplate(
    template=SPECIFY_SOURCE_PROMPT_TEMPLATE, 
    input_variables=["query", "answer", "source_content"]
)

EVALUATE_CONFIDENCE_PROMPT_TEMPLATE = """Determine a confidence score for the answer shown below, based on the text extract from a patient's medical record.

Text extract: {source_quote}
Query: {query}
Answer: {answer}

Please provide your confidence as a score out of 10.

Confidence Score (e.g. 5/10): """
evaluate_confidence_prompt = PromptTemplate(
    template=EVALUATE_CONFIDENCE_PROMPT_TEMPLATE, 
    input_variables=["query", "answer", "source_quote"]
)


## ================= Clinical Evaluation  =================== ##

TREATMENT_PLAN_TEMPLATE = """Identify and name the single main element in this treatment plan.

Treatment plan: {treatment_plan}

Key element of treatment plan: """
treatment_plan_prompt = PromptTemplate(
    template=TREATMENT_PLAN_TEMPLATE, 
    input_variables=["treatment_plan"]
)
