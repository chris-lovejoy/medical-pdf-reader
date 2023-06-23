"""
This is an executable script for implementing the full extraction 
and querying pipeline.
"""

import asyncio

from src.extract.extract_and_clean_pdf import PDFtoText
from src.parse.parse_to_clinical import TextToClinicalJSON


# Config for calling the script
reporting = True
debug = True
saving = True

skip_pdf_extracting = False
skip_parsing = False





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


if __name__ == '__main__':

    clean_text = extract_text_from_pdf()
    clinical_json = parse_clinical_json_from_text(clean_text)

