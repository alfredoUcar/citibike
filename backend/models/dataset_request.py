from pydantic import BaseModel, Field


class DatasetRequest(BaseModel):
    year: int = Field(
        ..., ge=2013, le=2025, description="Year must be between 2013 and 2025."
    )
    month: int | None = Field(
        None, ge=1, le=12, description="Month must be between 1 and 12."
    )
