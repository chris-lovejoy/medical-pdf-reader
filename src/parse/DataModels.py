"""This file specifies the clinical JSON structure to parse patient information into"""

from pydantic import BaseModel, Field
from typing import List, Optional

class ClinicalJSON(BaseModel):
        chief_complaint: Optional[str] = Field(
            description="The symptom or symptoms that brought the patient to the doctor and how they have evolved over time. Also known as the presenting complaint",
        )