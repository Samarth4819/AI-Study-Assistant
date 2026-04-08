from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Source text to process")


class SummaryResponse(BaseModel):
    summary: str


class KeyPointsResponse(BaseModel):
    key_points: list[str]


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str


class QuizResponse(BaseModel):
    quiz: list[QuizQuestion]


class UploadResponse(BaseModel):
    filename: str
    text_preview: str
    extracted_text: str
