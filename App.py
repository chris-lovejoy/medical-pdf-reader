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
    main()

