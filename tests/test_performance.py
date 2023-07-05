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

@pytest.mark.skip(reason="too costly to run via API calls")
def test_extraction_performance():

    with open(optimal_clinical_json_dir, 'r') as file:
        clinical_json = json.load(file)

    queryObject = query.QueryClinicalJSON(clinical_json)

    for key, _ in extraction_ground_truth.items():
        queryObject.extract_info(key)

    rouge1_scores = []
    rougeL_scores = []

    for key, value in queryObject.extracted_responses.items():
        rouge1, rougeL = calculate_extraction_score(value, extraction_ground_truth[key])

        rouge1_scores.append(rouge1)
        rougeL_scores.append(rougeL)

    if verbose:
        print("\nrouge1 scores are:", rouge1_scores)
        print("rougeL scores are:", rougeL_scores)

        print("Extractions are:", queryObject.extracted_responses.values())

    assert sum(rouge1_scores)/len(rouge1_scores) > 0.5
    assert sum(rougeL_scores)/len(rougeL_scores) > 0.5


@pytest.mark.skip(reason="too costly to run via API calls")
def test_evaluation_true_false():

    with open(optimal_clinical_json_dir, 'r') as file:
        clinical_json = json.load(file)

    queryObject = query.QueryClinicalJSON(clinical_json)

    for index in range(len(querying_ground_truth)):
        queryObject.answer_query(querying_ground_truth[0]['query'])

    for index in range(len(querying_ground_truth)):
        print(f"\nFOR QUERY '{querying_ground_truth[0]['query']}:")
        print(f"Predicted: {queryObject.query_responses[index]['answer']}")
        print(f"Actual: {querying_ground_truth[index]['answer']}")
        assert queryObject.query_responses[index]['answer'] == querying_ground_truth[index]['answer']
        # TODO: consider setting up the assert differently -> as it will stop before doing the rest.

@pytest.mark.skip(reason="too costly to run via API calls")
def test_evaluation_sources():

    with open(optimal_clinical_json_dir, 'r') as file:
        clinical_json = json.load(file)

    # TODO: implement this as per test evaluation but for sources
    # ROUGE score probably best comparison too

    return None


def calculate_extraction_score(extraction1, extraction2):

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(extraction1, extraction2)
    rouge1 = scores['rouge1'].fmeasure
    rougeL = scores['rougeL'].fmeasure
    
    return rouge1, rougeL


def calculate_query_performance():
    
    # TODO: implement this

    return None
