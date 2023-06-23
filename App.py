import streamlit as st

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




if __name__ == '__main__':
    main()

