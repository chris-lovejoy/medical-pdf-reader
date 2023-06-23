import pytest
import json

from rouge_score import rouge_scorer

import src.query.query as query

verbose = True
# NOTE: run ```pytest -s``` to see the print outputs

optimal_clinical_text = "./tests/clinical_text.txt"
optimal_clinical_json_dir = "./tests/example.json"


extraction_ground_truth = {
    "Patient’s chief complaint" : "hemorrhoids",
    "Suggested treatment plan the doctor is recommending" : "colonoscopy to screen for malignant \
        neoplasm of colon, seek evaluation for banding procedure after colonoscopy",
    "A list of allergies the patient has" : "NKDA, no known drug allergies",
    "A list of medications the patient is taking, with any known side-effects" : 
    "Clenpiq: Possible side effects include nausea, vomiting, abdominal pain, and dehydration.\
        \nDiclofenac: Possible side effects include skin irritation, rash, and stomach upset.\
        \nMeloxicam: Possible side effects include stomach upset, nausea, and headache.",
}

querying_ground_truth = [
    {
    'query': "Does the patient have a family history of hypertension?",
    'answer': True,
    'source_quote': "\nMother: Arthritis, Hypertensive disorder, Hypercholesterolemia.\
        Father: Hypertensive disorder, Congestive heart failure, Diabetes mellitus, Chronic \
        obstructive pulmonary disease, Arthritis, Heart disease. Brother: Congestive heart failure,\
        Asthma.", # TODO: consider weaning this down
    },
    {
    'query': "Does the patient have a family history of colon cancer?",
    'answer': True,
    'source_quote': "Patient has family history of colon cancer (grandfather on his eighties)",
    },
    # "Does the patient have a family history of stroke?",
    # "Does the patient have a family history of diabetes?",
    {
    'query': "Has the patient experienced minimal bright red blood per rectum?",
    'answer': True,
    'source_quote': "Patient has BPRPR last year. Bright red blood per rectum.",
    },
    # "Is the patient deaf?",
]


@pytest.mark.skip(reason="too costly to run via API calls")
def test_parsing_performance():

    # TODO: implement test which:
    # (1) loads the optimal medical text
    # (2) looks for presence of key information in the extracted and parsed text

    return None
