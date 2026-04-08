from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.pdf_routes import router as study_router


app = FastAPI(title="AI Study Assistant API", version="0.1.0")

# CORS allows the React frontend (localhost:3000) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {"message": "Backend is running!"}


app.include_router(study_router)
