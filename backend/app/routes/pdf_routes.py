from __future__ import annotations

from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PyPDF2 import PdfReader

from app.models.schemas import KeyPointsResponse, QuizResponse, SummaryResponse, TextRequest, UploadResponse
from app.services.keypoints import extract_key_points
from app.services.quiz_generator import generate_quiz
from app.services.summarize import summarize_text


router = APIRouter(tags=["study-assistant"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """Accept PDF or text files, extract text, and return preview + full extracted text."""
    filename = file.filename or "uploaded_file"
    suffix = filename.lower().split(".")[-1] if "." in filename else ""

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    extracted_text = ""

    if suffix == "pdf":
        try:
            reader = PdfReader(BytesIO(content))
            pages_text = [page.extract_text() or "" for page in reader.pages]
            extracted_text = "\n".join(pages_text).strip()
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {exc}") from exc

    elif suffix in {"txt", "md", "csv"}:
        extracted_text = content.decode("utf-8", errors="ignore").strip()
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, TXT, MD, or CSV file.",
        )

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No readable text found in the file.")

    preview = extracted_text[:500]
    return UploadResponse(filename=filename, text_preview=preview, extracted_text=extracted_text)


@router.post("/summarize", response_model=SummaryResponse)
def summarize(payload: TextRequest) -> SummaryResponse:
    summary = summarize_text(payload.text)
    return SummaryResponse(summary=summary)


@router.post("/keypoints", response_model=KeyPointsResponse)
def keypoints(payload: TextRequest) -> KeyPointsResponse:
    points = extract_key_points(payload.text)
    return KeyPointsResponse(key_points=points)


@router.post("/generate-quiz", response_model=QuizResponse)
def generate_quiz_route(payload: TextRequest) -> QuizResponse:
    quiz = generate_quiz(payload.text)
    return QuizResponse(quiz=quiz)
