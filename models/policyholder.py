from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional

class PolicyType(str, Enum):
    HEALTH = "Health"
    VEHICLE = "Vehicle"
    LIFE = "Life"

class Policyholder(BaseModel):
    policyholder_id: str = Field(..., description="Unique identifier for the policyholder")
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100)
    policy_type: PolicyType
    sum_insured: float = Field(..., ge=0)
    registration_date: datetime = Field(default_factory=datetime.now)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if not all(x.isalpha() or x.isspace() for x in v):
            raise ValueError('Name must contain only letters and spaces')
        return v.strip()

    @validator('sum_insured')
    def validate_sum_insured(cls, v):
        if v <= 0:
            raise ValueError('Sum insured must be greater than 0')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "policyholder_id": "PH001",
                "name": "John Doe",
                "age": 30,
                "policy_type": "Health",
                "sum_insured": 100000.00
            }
        } 