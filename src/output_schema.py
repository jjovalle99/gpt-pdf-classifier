from langchain_core.pydantic_v1 import BaseModel, Field


class Classification(BaseModel):
    label: str = Field(
        description="one of the following: COVER_PAGE, BLANK_PAGE, TEXT_PAGE, IMAGE_PAGE, DIAGRAM_PAGE, TEXT_PLUS_IMAGE_PAGE, TEXT_PLUS_DIAGRAM_PAGE, TABLE_PAGE, TEXT_PLUS_TABLE_PAGE, UNKNOWN"
    )
