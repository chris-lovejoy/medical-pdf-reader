import pytest
from src.extract.extract_and_clean_pdf import PDFtoText

pdf_dir = "./data/medical-record.pdf"
example_initial_text_extraction = "\nMedical Record Pa#ent Name: John Smith DOB: 06/16/1982 MRN: 456789123 Sex: Male\nChief Complaint hemorrhoids, new pa@ent Pa/ent’s Care Team Primary Care Provider: Name: Care Provider MD Address: 123 Main Street, Cocoa, FL 12345 Phone: (123) 456- 7899 Fax: (123) 456-7899 NPI: 1234567899 Sports Medicine: Name: Sports Medicine Address: 123 Main Street, Cocoa, FL 12345 Phone: (123) 456-7899 Fax: (123) 456-7899 NPI: 1234567899\nPa/ent’s Pharmacies Pharmacy: Name: Pharmacy Address: 123 Main Street, Cocoa, FL 12345 Phone: (123) 456-7899 Fax: (123) 456- 7899 Vitals Ht: 6 P 2 in Wt: 165 lbs BMI: 21.2 Pulse: 96 bpm RR: 16 02Sat: 87%\nAllergies\nAllergies not reviewed (last reviewed 11/28/2022) • NKDA Medica/ons\nClenpiq 10 rng-3.5 gram-12 gram/160 ml oral solu#on Take 320 ml by oral route as directed • diclofenac 1 % topical gel BMI: 21.2 02Sat: 87% 02/10/23 prescribad 11 /28/22 ﬁlled · APPLY 2 GRAMS\nTO THE AFFECTED AREA(S) TOPICALLY FOUR TIMES A DAY\nmeloxicarn 15 mg tablet TAKE ONE TABLET BY MOUTH ONE TIME DAILY\nProblems Reviewed Problems · No known problems\nFamily History Family History not reviewed (last reviewed 11/28/2022)\nMother\nArthri@s - Hypertensive disorder - Hypercholesterolemia\nFather\nHypertensive disorder - Conges@ve heart failure - Dlabatas mallitus\nChronic obstruc@ve lung disease - Arthri@s - Heart disease\nBrother\nConges@ve heart failure - Asthma\nSocial History Social History not reviewed (last reviewed 11/28/2022)\nAc#vi#es of Dally Living\nAre you deaf or do you have serious diﬃculty hearing?: No Are you able to walk?: Yes: walks without restric@ons Do you have transporta@on diﬃcul@es?: No\nDiet and Exercise\nWhat type of diet are you following?: Regular What Is your exercise level?: None\nEduca#on and Occupa#on What is the highest grade or level of school you have completed or the highest degree you have received?: High school graduate Are you currently employed?: Yes What Is your occupa@on?: Lineman\nAdvance Direc#ve Do you have a medical power of agorney?: No Is blood transfusion acceptable in an emergency?: Yes\nSubstance Use Do you or have you ever smoked tobacco?: Currant every day smoker How much tobacco do you chew?; none At what age did you start smoking tobacco?: 20 How much tobacco do you smoke?: 1 pack per day How many years have you smoked tobacco?: 20 What is your level of alcohol consump@on?: None How many years have you consumed alcohol?: 20 What is your level of caﬀeine consump@on?: Occasional\nMarriage and Sexuality What is your rela@onship status?: Married Are you sexually ac@ve?: Yes Do you use protec@on during sex?: No How many children do you have?: 3\nHome and Environment Do you have any pets?: Yes Are you passively exposed to smoke?: Yes\nLifestyle Do you feel stressed (tense, restless, nervous, or anxious, or unable to sleep at night)?: Not at all Do you use your seat belt or car seat rou@nely?: No\nPMG Social History Do you have a support system?: Yes Domes@c violence history: No\nContracep@on used: Vasectomy Other tobacco products: None Living will: No Educa@on speciﬁcs: Public school Home health; No\nGender Iden#ty and LGBTQ Iden@ty Gender Iden@ty: Choose not to disclose First name used: John Sexual orienta@on: Choose not to disclose\nSurgical History Surgical History not reviewed (last reviewed 11/28/2022) Past Medical History Past Medical History not reviewed (last reviewed 11/28/2022)\nHPI Pa@ent is a 41 y/o male with history of lateral epicondyli@s who is seen for the ﬁrst @me at this prac@ce. Pa@ent never had a colonoscopy. Pa@ent is complaining of symptoma@c haemorrhoids two months ago, one of which had ruptured and bled last year. Pa@ent has family history of colon cancer (grandfather on his eigh@es). Pa@ent denies blood in stool.\nROS ROS as noted in the HPJ\nPhysical Exam Cons#tu#onal: General Appearance: healthy-appearing, well-nourished, and well-developed. Level of Distress: NAO. Ambula@on: ambula@ng normally.\nPsychiatric: Insight: good Judgement. Mental Status: ac@ve and alert. Orienta@on: to @me, place, and person. Memory: recent memory normal.\nAbdomen: Bowel Sounds: normal. Inspec@on and Palpa@on: no tenderness, guarding, masses, rebound tenderness, or CVA tenderness and soP and non-distended. Liver: non-tender and no hepatomegaly. Spleen: non-tender and no splenomegaly. Hernia: none palpable.\nAssessment/ Plan\n1. Haemorrhoids Pa@ent is asymptoma@c right know. I advised to seek evalua@on for banding procedure aPer colonoscopy (depending on evalua@on done) K64.9: Unspeciﬁed haemorrhoids.\n2. Screening for malignant neoplasm of colon Pa@ent will have colonoscopy with average risk. Consent signed. Risks associated with this procedure such as bleeding, Infec@on and perfora@on were discussed with the pa@ent.\nZ12.11: Encounter for screening for malignant neoplasm of colon • Clenpiq 10 mg-3.5 gram-12 gram/160 ml oral solu#on - Take 320 ml by oral route as directed Qty: (320) ml Reﬁlls: 0\n3. Family history of cancer of colon- Pa@ent has family history of colon cancer (grandfather on his eigh@es) Z80.0: Family history of malignant neoplasm of diges@ve organs\n4. Haematochezia - Pa@ent has BRBPR last year K92.1: Melena"
example_auto_clean_text_extraction = "Medical Record Pa#ent Name: John Smith DOB: 06/16/1982 MRN: 456789123 Sex: Male Chief Complaint hemorrhoids, new pa@ent Pa/ents Care Team Primary Care Provider: Name: Care Provider MD Address: 123 Main Street, Cocoa, FL 12345 Phone: (123) 456 7899 Fax: (123) 456 7899 NPI: 1234567899 Sports Medicine: Name: Sports Medicine Address: 123 Main Street, Cocoa, FL 12345 Phone: (123) 456 7899 Fax: (123) 456 7899 NPI: 1234567899 Pa/ents Pharmacies Pharmacy: Name: Pharmacy Address: 123 Main Street, Cocoa, FL 12345 Phone: (123) 456 7899 Fax: (123) 456 7899 Vitals Ht: 6 P 2 in Wt: 165 lbs BMI: 21.2 Pulse: 96 bpm RR: 16 02Sat: 87% Allergies Allergies not reviewed (last reviewed 11/28/2022)  NKDA Medica/ons Clenpiq 10 rng 3.5 gram 12 gram/160 ml oral solu#on Take 320 ml by oral route as directed  diclofenac 1 % topical gel BMI: 21.2 02Sat: 87% 02/10/23 prescribad 11 /28/22 lled  APPLY 2 GRAMS TO THE AFFECTED AREA(S) TOPICALLY FOUR TIMES A DAY meloxicarn 15 mg tablet TAKE ONE TABLET BY MOUTH ONE TIME DAILY Problems Reviewed Problems  No known problems Family History Family History not reviewed (last reviewed 11/28/2022) Mother Arthri@s Hypertensive disorder Hypercholesterolemia Father Hypertensive disorder Conges@ve heart failure Dlabatas mallitus Chronic obstruc@ve lung disease Arthri@s Heart disease Brother Conges@ve heart failure Asthma Social History Social History not reviewed (last reviewed 11/28/2022) Ac#vi#es of Dally Living Are you deaf or do you have serious diculty hearing?: No Are you able to walk?: Yes: walks without restric@ons Do you have transporta@on dicul@es?: No Diet and Exercise What type of diet are you following?: Regular What Is your exercise level?: None Educa#on and Occupa#on What is the highest grade or level of school you have completed or the highest degree you have received?: High school graduate Are you currently employed?: Yes What Is your occupa@on?: Lineman Advance Direc#ve Do you have a medical power of agorney?: No Is blood transfusion acceptable in an emergency?: Yes Substance Use Do you or have you ever smoked tobacco?: Currant every day smoker How much tobacco do you chew?; none At what age did you start smoking tobacco?: 20 How much tobacco do you smoke?: 1 pack per day How many years have you smoked tobacco?: 20 What is your level of alcohol consump@on?: None How many years have you consumed alcohol?: 20 What is your level of caeine consump@on?: Occasional Marriage and Sexuality What is your rela@onship status?: Married Are you sexually ac@ve?: Yes Do you use protec@on during sex?: No How many children do you have?: 3 Home and Environment Do you have any pets?: Yes Are you passively exposed to smoke?: Yes Lifestyle Do you feel stressed (tense, restless, nervous, or anxious, or unable to sleep at night)?: Not at all Do you use your seat belt or car seat rou@nely?: No PMG Social History Do you have a support system?: Yes Domes@c violence history: No Contracep@on used: Vasectomy Other tobacco products: None Living will: No Educa@on specics: Public school Home health; No Gender Iden#ty and LGBTQ Iden@ty Gender Iden@ty: Choose not to disclose First name used: John Sexual orienta@on: Choose not to disclose Surgical History Surgical History not reviewed (last reviewed 11/28/2022) Past Medical History Past Medical History not reviewed (last reviewed 11/28/2022) HPI Pa@ent is a 41 y/o male with history of lateral epicondyli@s who is seen for the rst @me at this prac@ce. Pa@ent never had a colonoscopy. Pa@ent is complaining of symptoma@c haemorrhoids two months ago, one of which had ruptured and bled last year. Pa@ent has family history of colon cancer (grandfather on his eigh@es). Pa@ent denies blood in stool. ROS ROS as noted in the HPJ Physical Exam Cons#tu#onal: General Appearance: healthy appearing, well nourished, and well developed. Level of Distress: NAO. Ambula@on: ambula@ng normally. Psychiatric: Insight: good Judgement. Mental Status: ac@ve and alert. Orienta@on: to @me, place, and person. Memory: recent memory normal. Abdomen: Bowel Sounds: normal. Inspec@on and Palpa@on: no tenderness, guarding, masses, rebound tenderness, or CVA tenderness and soP and non distended. Liver: non tender and no hepatomegaly. Spleen: non tender and no splenomegaly. Hernia: none palpable. Assessment/ Plan 1. Haemorrhoids Pa@ent is asymptoma@c right know. I advised to seek evalua@on for banding procedure aPer colonoscopy (depending on evalua@on done) K64.9: Unspecied haemorrhoids. 2. Screening for malignant neoplasm of colon Pa@ent will have colonoscopy with average risk. Consent signed. Risks associated with this procedure such as bleeding, Infec@on and perfora@on were discussed with the pa@ent. Z12.11: Encounter for screening for malignant neoplasm of colon  Clenpiq 10 mg 3.5 gram 12 gram/160 ml oral solu#on Take 320 ml by oral route as directed Qty: (320) ml Rells: 0 3. Family history of cancer of colon Pa@ent has family history of colon cancer (grandfather on his eigh@es) Z80.0: Family history of malignant neoplasm of diges@ve organs 4. Haematochezia Pa@ent has BRBPR last year K92.1: Melena"

def test_extractor_init():
    """
    Tests the initialisation of the PDFtoText extractor class
    """
    extractor = PDFtoText(pdf_dir)
    assert extractor.dir == pdf_dir

def test_load_initial_text():
    """
    Tests that loading of the initial text is performed to minimal required
    accuracy
    """
    extractor = PDFtoText(pdf_dir)
    extractor.load_initial_text()
    ratio_of_example_words_contained = compare_overlap(extractor.initial_text, 
                                                       example_initial_text_extraction)
    assert ratio_of_example_words_contained >= 0.7


def test_clean_text_auto():
    """
    Tests that cleaning of the text is performed using library functions
    """
    # TODO: update this test so that the text fed in is an example with 
    # the types of things that should be removed, such as dashes, bullets, etc
    extractor = PDFtoText(pdf_dir)
    extractor.initial_text = example_initial_text_extraction
    extractor.clean_initial_text_auto()
    ratio_of_clean_words_contained = compare_overlap(extractor.clean_text,
                                            example_auto_clean_text_extraction)
    assert ratio_of_clean_words_contained >= 0.8


@pytest.mark.skip(reason="too costly to run via API calls") # Uncomment to run locally
def test_clean_text_llm():
    """
    Tests that cleaning of the text is performed using LLMs
    """
    # Arrange
    with open('./tests/clean-text.txt', 'r') as file:
        example_llm_clean_text_extraction = file.read()   
    extractor = PDFtoText(pdf_dir)
    extractor.clean_text = example_auto_clean_text_extraction
    extractor.clean_initial_text_llm()
    ratio_of_clean_words_contained = compare_overlap(extractor.clean_text,
                                        example_llm_clean_text_extraction)
    assert ratio_of_clean_words_contained >= 0.8


# HELPER FUNCTION
def compare_overlap(string1, string2):
    """
    Identifies the ratio of words in string2 which are also present
    in string1.
    """

    # Split the strings into words
    words1 = string1.split()
    words2 = string2.split()
    
    # Convert word lists into sets
    set1 = set(words1)
    set2 = set(words2)
    
    # Find the intersection of the sets
    overlap = set1.intersection(set2)
    
    # Calculate the ratio of overlapping words
    overlap_ratio = (len(overlap) / len(set2))
    
    return overlap_ratio
