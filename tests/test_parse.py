import pytest
from src.parse.parse_to_clinical import TextToClinicalJSON

sample_text = "This can become a sample clinical record, which needs to be parsed into the specified clinical format."

def test_parser_init():
    """
    Tests the initialisation of the TextToClinicalJSON parser class
    """
    parser = TextToClinicalJSON(sample_text)
    assert parser.text == sample_text

@pytest.mark.skip(reason="too costly to run via API calls") # Uncomment this to run locally
def test_parse_text_to_clinical_json():
    """
    Tests that parsing and cleaning of the text is performed using the TextToClinicalJSON parser class
    """
    parser = TextToClinicalJSON(sample_text)
    parser.parse_text_to_clinical_json()
    assert parser.clinical_json is not None 
    # TODO: update to a definition of reasonably accurate parsing
    # (Will need to incorporate the structure specified in the pydantic data model)