from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator

class ClaimStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class Claim(BaseModel):
    claim_id: str = Field(..., description="Unique identifier for the claim")
    policyholder_id: str = Field(..., description="ID of the policyholder")
    claim_amount: float = Field(..., gt=0)
    reason: str = Field(..., min_length=10, max_length=500)
    status: ClaimStatus = Field(default=ClaimStatus.PENDING)
    date_of_claim: datetime = Field(default_factory=datetime.now)
    
    @validator('claim_amount')
    def validate_claim_amount(cls, v):
        if v <= 0:
            raise ValueError('Claim amount must be greater than 0')
        return v

    @validator('reason')
    def validate_reason(cls, v):
        if not v.strip():
            raise ValueError('Reason cannot be empty')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "claim_id": "CL001",
                "policyholder_id": "PH001",
                "claim_amount": 5000.00,
                "reason": "Medical expenses for routine checkup",
                "status": "Pending"
            }
        } 