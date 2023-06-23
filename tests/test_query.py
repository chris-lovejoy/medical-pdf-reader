import pytest
import json

from src.query.query import QueryClinicalJSON

# Arrange
with open("./tests/example.json", "r") as f:
    clinical_json = json.load(f) 

@pytest.mark.skip(reason="erroneous error from openAI API")
def test_query_object_init():
    """
    Tests the initialisation of the QueryClinicalJSON object
    """
    queryObject = QueryClinicalJSON(clinical_json)
    assert queryObject.clinical_json == clinical_json

@pytest.mark.skip(reason="erroneous error from openAI API")
def test_enforce_true_false():
    """
    Tests that enforcing of true/false is performed correctly
    """
    queryObject = QueryClinicalJSON(clinical_json)

    example_text = "This is definitely true."
    output = queryObject.enforce_true_false(example_text)
    assert output is True

    example_text_2 = "FALSE!!"
    output = queryObject.enforce_true_false(example_text_2)
    assert output is False

@pytest.mark.skip(reason="erroneous error from openAI API")
def test_extract_strings():
    """
    Tests that extracting of strings is performed correctly
    """
    queryObject = QueryClinicalJSON(clinical_json)
    # TODO: implement this