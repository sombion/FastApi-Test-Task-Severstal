from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class SRoll(BaseModel):
    length: int = Field(..., ge=0)
    weight: int = Field(..., ge=0)
    date_added: datetime | None = Field(...)
    date_removed: datetime | None = Field(...)