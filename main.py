"""
This is an executable script for implementing the full extraction 
and querying pipeline.
"""

import asyncio
import json

from src.extract.extract_and_clean_pdf import PDFtoText
from src.parse.parse_to_clinical import TextToClinicalJSON
from src.query.query import QueryClinicalJSON


# Config for calling the script
reporting = True # If True, this will report progress and findings to the console
debug = False # If True, this will provide step-by-step visualisation of intermediates
saving = False # If True, this will save intermediate objects into 'output' folder

skip_pdf_extracting = False
skip_parsing = False
skip_extraction_query = False
skip_question_query = False


# Specify the information to extract
extraction_list = [
    "Patient’s chief complaint",
    "Suggested treatment plan the doctor is recommending",
    "A list of allergies the patient has",
    "A list of medications the patient is taking, with any known side-effects",
]

# Specify the answers to query
query_list = [
    "Does the patient have a family history of hypertension?",
    "Does the patient have a family history of colon cancer?",
    # "Does the patient have a family history of stroke?",
    # "Does the patient have a family history of diabetes?",
    "Has the patient experienced bright red blood per rectum?",
    # "Has the patient experienced minimal bright red blood per rectum?",
    # "Is the patient deaf?",
]



def extract_text_from_pdf():
    if not skip_pdf_extracting:
        extractor = PDFtoText("./data/medical-record.pdf")
        if reporting:
            print("\nLoading and extracting text from PDF...")
        extractor.load_initial_text()
        if debug:
            print("\nINITIAL TEXT:", extractor.initial_text)
        extractor.clean_initial_text_auto()
        if debug:
            print("\nCLEAN TEXT (after auto):", extractor.clean_text)
        extractor.clean_initial_text_llm()
        if debug:
            print("\nCLEAN TEXT (after llm cleaning):", extractor.clean_text)
        if reporting:
            print("PDF extraction complete.")    
        if saving:
            with open('./output/clean-text.txt', 'w') as file:
                file.write(extractor.clean_text)
        clean_text = extractor.clean_text 

    else:
        with open('./output/clean-text.txt', 'r') as file:
            clean_text = file.read()
    
    return clean_text


def parse_clinical_json_from_text(clean_text):
    if not skip_parsing:
        parser = TextToClinicalJSON(clean_text)
        if reporting:
            print("\nParsing PDF contents into clinical JSON...")
        asyncio.run(parser.chunk_and_parse_doc())
        if debug:
            print("CHUNKED PARSING:", parser.chunked_parsing)
        parser.combine_parsed_chunks()
        if debug:
            print("COMBINED PARSING:", parser.combined_parsing)
        parser.clean_clinical_json()
        if debug:
            print("CLEANED CLINICAL JSON:", parser.clinical_json)
        if reporting:
            print("Parsing into clinical JSON complete.")
        if saving:
            with open('./output/clinical-json.json', 'w') as file:
                json.dump(parser.clinical_json, file)
        clinical_json = parser.clinical_json
    
    else:
        with open('./output/clinical-json.json', 'r') as file:
            clinical_json = json.load(file)
    
    return clinical_json




def extract_from_clinical_json(clinical_json):
    if not skip_extraction_query:
        queryObject = QueryClinicalJSON(clinical_json)
        if reporting:
            print("\nPerforming extraction queries...")
        for index, info_to_extract in enumerate(extraction_list):
            queryObject.extract_info(info_to_extract)
            if reporting:
                print(f"\nQUERY {index + 1}:")
                print(f"{info_to_extract}: {queryObject.extracted_responses[info_to_extract]}")
        if reporting:
            print("\nExtraction queries complete.")
    else:
        pass

def query_from_clinical_json(clinical_json):
    if not skip_question_query:
        queryObject = QueryClinicalJSON(clinical_json)
        if reporting:
            print("\nPerforming question queries...")
        for index, medical_query in enumerate(query_list):
            queryObject.answer_query(medical_query)
            if reporting:
                print(f"\nQUERY {index + 1}:")
                print(f"QUESTION: {medical_query}")
                print(f"RESPONSE: {queryObject.query_responses[index]['answer']}")
                print(f"SUPPORTING EVIDENCE: {queryObject.query_responses[index]['source_quote']}")
                print(f"CONFIDENCE: {queryObject.query_responses[index]['confidence_score']}")
        if reporting:
            print("\nQuestion queries complete.")
    else:
        pass


if __name__ == '__main__':

    clean_text = extract_text_from_pdf()
    clinical_json = parse_clinical_json_from_text(clean_text)
    extract_from_clinical_json(clinical_json)
    query_from_clinical_json(clinical_json)

