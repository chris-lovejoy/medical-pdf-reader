"""
This is an executable script for implementing the full extraction 
and querying pipeline.
"""

from src.extract.extract_and_clean_pdf import PDFtoText
from src.parse.parse_to_clinical import TextToClinicalJSON


# Config for calling the script
reporting = True
debug = True
saving = True

skip_extracting = False
skip_parsing = False




def extract_text_from_pdf():
    if not skip_extracting:
        extractor = PDFtoText("./data/medical-record.pdf")
        extractor.load_initial_text()
        if debug:
            print("\nINITIAL TEXT:", extractor.initial_text)
        extractor.clean_initial_text_auto()
        if debug:
            print("\nCLEAN TEXT (after auto):", extractor.clean_text)
        extractor.clean_initial_text_llm()
        if debug:
            print("\nCLEAN TEXT (after llm cleaning):", extractor.clean_text)
        if saving:
            with open('./output/clean-text.txt', 'w') as file:
                file.write(extractor.clean_text)
        clean_text = extractor.clean_text 

    else:
        with open('./output/clean-text.txt', 'r') as file:
            clean_text = file.read()
    
    return clean_text


if __name__ == '__main__':

    extract_text_from_pdf()


