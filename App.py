import tempfile

import time 
import json

import streamlit as st
import asyncio

import src.extract.extract_and_clean_pdf as extract_and_clean_pdf
import src.parse.parse_to_clinical as parse_to_clinical
from src.query.query import QueryClinicalJSON

st.set_page_config(
        page_title="Medical PDF Reader",
        page_icon = ":stethoscope:"
)

with st.sidebar:
    
    st.markdown('''
    ## ABOUT
    This app extracts information from medical record PDFs into a structured **clinical JSON format™️** (patent pending*).
    
    ---

    This enables you to:
    - **Extract specific information** contained within the medical record
    - **Ask questions** about content within the medical record
    - **Use clinical reasoning** to assess medical decisions made in the record
    
    ---

    The **clinical JSON format** is a single-level JSON document with the following fields:
    - chief_complaint
    - medications
    - allergies
    - family_history
    - physical_examination
    - treatment_plan
    
    You can see an example [here](https://github.com/chris-lovejoy/medical-pdf-reader/blob/main/tests/example.json).    
    
    ---

    NOTE: At present, this only supports PDFs up to 3-4 pages.

    ---
    
    _*just kidding_
    
    ''')

def main():

    st.title("The Medical PDF Reader 🩺🔍")

    st.write("""To get started, either upload a PDF or upload a JSON that adheres to the **clinical
      JSON format**""")


    # Initialise PDF upload state
    if "pdf_uploaded" not in st.session_state:
        st.session_state["pdf_uploaded"] = False

    # Initialise JSON upload state
    if "json_uploaded" not in st.session_state:
        st.session_state["json_uploaded"] = False

    st.markdown("### Option 1: Upload a medical record as a PDF")
    pdf = st.file_uploader("Upload your PDF", type='pdf') 
    
    if pdf is not None:
        st.session_state["pdf_uploaded"] = True
    
    if st.session_state["pdf_uploaded"] is False:
        st.markdown("### Option 2: Upload a JSON that adheres to the **clinical JSON™ format**")
        json_data = st.file_uploader("Upload a clinical JSON file", type='json') 
        
        if json_data is not None:
            clinical_json = json.loads(json_data.read())
            st.session_state["json_uploaded"] = True
            st.session_state["clinical_json"] = clinical_json


    if pdf is not None:
        pdf_file_path = save_temp_file(pdf)

        if st.button("Extract Information into Clinical JSON"):
            clinical_json = extract_clinical_json(pdf_file_path)
            st.session_state["clinical_json"] = clinical_json
            st.session_state["json_uploaded"] = True           

    if st.session_state["json_uploaded"]:

        with st.expander("View Clinical JSON data"):
            st.write(st.session_state["clinical_json"])
        
        json_data = json.dumps(st.session_state["clinical_json"], indent=4)

        st.download_button("Download Clinical JSON data", 
            json_data, file_name="clinical_json.json", 
            mime="application/json"
            )
        # NOTE: the JSON output isn't perfect, as doesn't handle the second indent.

        st.divider()
        if "query_object" not in st.session_state:
            st.session_state["query_object"] = QueryClinicalJSON(st.session_state["clinical_json"])

        st.markdown("## Extract Information")
        st.markdown("##### For Example:")
        if st.button("Patient's chief complaint"):
            extract_info(st.session_state["query_object"], st.session_state["clinical_json"], "Patient's chief complaint")
        if st.button("Suggested treatment plan the doctor is recommending"):
            extract_info(st.session_state["query_object"], st.session_state["clinical_json"], "Suggested treatment plan the doctor is recommending")
        if st.button("A list of allergies the patient has"):
            extract_info(st.session_state["query_object"], st.session_state["clinical_json"], "A list of allergies the patient has")
        if st.button("A list of medications the patient is taking, with any known side-effects"):
            extract_info(st.session_state["query_object"], st.session_state["clinical_json"], "A list of medications the patient is taking, with any known side-effects")

        st.markdown("#### Or Custom:")
        info_to_extract = st.text_input("Information to extract")
        if st.button("Extract custom information"):
            extract_info(st.session_state["query_object"], st.session_state["clinical_json"], info_to_extract)

        st.markdown("#### Extracted Info:")
        if "extracted_info" in st.session_state:
            parsed_data = list(st.session_state["query_object"].extracted_responses.items())
            for key, value in parsed_data:
                st.markdown(f"""**{key}:** {value}""")

        else:
            st.write("No information extracted yet.")

        st.divider()

        st.markdown("## Ask a question")
        st.markdown("##### For Example:")
        if st.button("Does the patient have a family history of hypertension?"):
            answer_query(st.session_state["query_object"], st.session_state["clinical_json"], "Does the patient have a family history of hypertension?")
        if st.button("Does the patient have a family history of colon cancer?"):
            answer_query(st.session_state["query_object"], st.session_state["clinical_json"], "Does the patient have a family history of colon cancer?")
        if st.button("Has the patient experienced bright red blood per rectum?"):
            answer_query(st.session_state["query_object"], st.session_state["clinical_json"], "Has the patient experienced bright red blood per rectum?")


        st.markdown("#### Or Custom:")
        custom_query = st.text_input("Query")
        if st.button("Submit query"):
            answer_query(st.session_state["query_object"], st.session_state["clinical_json"], custom_query)

        st.markdown("#### Questions and Answers:")
        if 'query_answered' in st.session_state:
            for index, query_response in enumerate(st.session_state["query_object"].query_responses):
                st.markdown(f"##### \nQUERY {index + 1}:")
                st.write(f"QUESTION: {query_response['query']}")
                st.write(f"RESPONSE: {query_response['answer']}")
                st.write(f"SUPPORTING EVIDENCE: {query_response['source_quote']}")
                st.write(f"CONFIDENCE: {query_response['confidence_score']}")
        else:
            st.write("No questions answered yet.")

        st.divider()

        # st.markdown("### Use Clinical Reasoning")
        # st.write("TODO")


def extract_clinical_json(pdf_file_path):

    extraction = extract_and_clean_pdf.PDFtoText(pdf_file_path)
    with st.spinner("Extracting Text..."):
        time.sleep(1)
        extraction.load_initial_text()
        st.success("Raw text successfully extracted.")
    with st.spinner("Cleaning Text... (may take up to a minute)"):
        extraction.clean_initial_text_auto()
        extraction.clean_initial_text_llm()
        st.success("Text has been cleaned.")
    with st.spinner("Parsing Text..."):
        parser = parse_to_clinical.TextToClinicalJSON(extraction.clean_text)
        asyncio.run(parser.parse_text_to_clinical_json())
        st.success("Text parsing complete.")

    st.balloons()

    return parser.clinical_json

def extract_info(queryObject, clinical_json, info_to_extract):
    
    with st.spinner("Extracting info..."):
        queryObject.extract_info(info_to_extract)
        st.session_state["query_object"] = queryObject
        st.session_state["extracted_info"] = True

    success_message = st.success("Extraction complete.")
    time.sleep(1)
    success_message.empty()


def answer_query(queryObject, clinical_json, question):

    with st.spinner("Answering query..."):
        queryObject.answer_query(question)
        st.session_state["query_object"] = queryObject
        st.session_state["query_answered"] = True

    success_message = st.success("Query answered.")
    time.sleep(1)
    success_message.empty()




def save_temp_file(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.read())
    return temp_file.name


foot = f"""
<div style="
    position: fixed;
    bottom: 0;
    left: 30%;
    right: 0;
    width: 50%;
    padding: 0px 0px;
    text-align: center;
">
    <p>Made with ❤ by <a href='https://twitter.com/ChrisLovejoy_'>Chris Lovejoy</a></p>
</div>
"""

hide_components = """
    <style>
    
    #MainMenu {visibility: hidden;
    # }
        footer {visibility: hidden;
        }
        .css-card {
            border-radius: 0px;
            padding: 30px 10px 10px 10px;
            background-color: #f8f9fa;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
            font-family: "IBM Plex Sans", sans-serif;
        }
        
        .card-tag {
            border-radius: 0px;
            padding: 1px 5px 1px 5px;
            margin-bottom: 10px;
            position: absolute;
            left: 0px;
            top: 0px;
            font-size: 0.6rem;
            font-family: "IBM Plex Sans", sans-serif;
            color: white;
            background-color: green;
            }
            
        .css-zt5igj {left:0;
        }
        
        span.css-10trblm {margin-left:0;
        }
        
        div.css-1kyxreq {margin-top: -40px;
        }
        
        
    
        
        

    </style>
    """

# Add custom CSS
st.markdown(foot, unsafe_allow_html=True)
st.markdown(hide_components, unsafe_allow_html=True,
)

if __name__ == '__main__':
    st.session_state["extracted"] = None
    main()

