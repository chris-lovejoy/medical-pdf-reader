"""This file specifies the clinical JSON structure to parse patient information into"""

from pydantic import BaseModel, Field
from typing import List, Optional

class ClinicalJSON(BaseModel):
        chief_complaint: Optional[str] = Field(
            description="The symptom or symptoms that brought the patient to the doctor and how they have evolved over time. Also known as the presenting complaint",
            # examples = [("Presenting complaint chest pain. Patient reported with chest pain since yesterday and some shortness of breath overnight. Doctors assessment: likely musculoskeletal chest pain, with some anxiety",
                    # "chest pain and shortness of breath")]
        )
        past_medical_history: Optional[str] = Field(
            description="All previously diagnosed medical conditions or previous surgical operations."
        )
        medications: Optional[List[Medication]] = Field(
            description="The medications that the patient is current taking. Does not include medication that they are no longer taking.",
            examples = [
                (
                    "Medication List chloramphenicol 0.5 mg QDS chlordiazepoxide 5mg when required salbutamol inahler 4 times a day Past Medical History review last week by their GP",
                    [
                        {"name": "chloramphenicol", "dose": "0.5 mg QDS"},
                        {"name": "chlordiazepoxide", "dose": "5mg when required"},
                        {"name": "salbutamol inhaler", "dose": "4 times a day"}
                    ]
                ),
                # (
                #     "Patient on metformin 1g BD and currently on short course of chlordiazepoxide 5mg. Was taking sertraline but stopped six months ago. Also used to take warfarin 3mg/day",
                #     [
                #            {"name": "metformin", "dose": "1g BD"},
                #            {"name": "chlordiazepoxide", "dose": "5mg"},
                #     ]
                # )
            ]
        )
        allergies: Optional[str] = Field(
            description="Information about patient drug allergies."
        )
        family_history: Optional[str] = Field(
            description="All of the medical conditions that family members of the patient have had."
        )
        social_history: Optional[str] = Field(
            #    description="All of the patient's social history."
        )
        physical_examination: Optional[str] = Field(
            description="The findings from performing a physical examination of the patient."
        )        
        # doctors_assessment: Optional[str] = Field(
        #     description="The doctor's concluding assessment of the patient."
        # ) # NOTE: Not included, as harms performance for treatment plan
        treatment_plan: Optional[str] = Field(
            description="The step-by-step treatment plan by the doctor for the patient. Usually found at the end of clincial notes.",
        )

        # NOTE: Other things to consider extracting:
        # - Administrative information
        # - Vital signs
        # - Blood tests results?


class ComplexClinicalJSON(BaseModel):
        """
        An alternative schema with more granular divisions of fields.
        """

        # TODO: implement this.

        # Fields which can be easily sub-divided further with sub-field schemas:
        # Physical examination: {"organ_system": "description of findings"}
        # Family history: {"family_member: "medical_conditions"}
        # Social history: {"area e.g. substance use": "description"}
        # Treatment plan: {"treatment_item": "first treatment item", "treatment_item": "second treatment item"}
        # (as per https://eyurtsev.github.io/kor/validation.html#complex-structure)


class SimpleClinicalJSON(BaseModel):
        """
        An alternative schema which has fewer fields.
        """
        chief_complaint: Optional[str] = Field(
                description="The symptom or symptoms that brought the patient to the doctor and how they have evolved over time. Also known as the presenting complaint",
                examples = [
                    ("Presenting complaint chest pain. Patient reported with chest pain since yesterday and some shortness of breath overnight. Doctors assessment: likely musculoskeletal chest pain, with some anxiety",
                    {"chief_complaint": "chest pain and shortness of breath"}),
                ]
        )
        medical_context: Optional[str] = Field(
            description="All background medical information about the patient (outside the presenting complaint)."
        )
        medical_findings: Optional[str] = Field(
            description="All examination findings, test results and other investigations performed by doctors."
        )
        social_context: Optional[str] = Field(
            description="All background social information about the patient."
        )
        treatment_plan: Optional[str] = Field(
            description="The step-by-step treatment plan by the doctor for the patient. Usually found at the end of clincial notes.",
        )
        # other: Optional[str] = Field(
        #     description="All other information that doesn't fit in other sections."
        # )
