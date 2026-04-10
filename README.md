# AI Study Assistant

AI Study Assistant is a full-stack app that converts uploaded PDFs or notes into:
- concise summaries
- key points
- multiple-choice quizzes

It uses a FastAPI backend and a React frontend.

## Project Structure

```text
AI Study Assistant/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── pdf_routes.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── summarize.py
│       │   ├── keypoints.py
│       │   └── quiz_generator.py
│       └── models/
│           ├── __init__.py
│           └── schemas.py
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── App.js
│       ├── styles.css
│       ├── api/
│       │   └── api.js
│       └── components/
│           ├── UploadForm.js
│           ├── SummaryView.js
│           ├── KeyPointsView.js
│           └── QuizView.js
├── .gitignore
└── README.md
```

## Features

- Upload PDF, TXT, MD, or CSV files
- Extract text and show preview
- Generate summary from extracted text
- Extract top key points
- Create interactive multiple-choice quiz
- Loading states and error handling on frontend

## Backend Setup (FastAPI)

### 1) Create and activate virtual environment

Windows PowerShell:

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2) Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 2.1) Enable AI-quality generation (recommended)

Set your Gemini API key before running backend:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
$env:GEMINI_MODEL="gemini-2.5-flash"
```

If `GEMINI_API_KEY` is set, summary/key points/quiz are generated using LLM prompts for much better quality.
If it is not set, the app falls back to local heuristic logic.

If you want to test optional local transformer summarization:

```powershell
pip install transformers torch
```

### 3) Run backend

From the `backend` folder:

```powershell
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`.

## Frontend Setup (React)

```powershell
cd frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000`.

## API Endpoints

- `GET /` -> `{ "message": "Backend is running!" }`
- `POST /upload` -> Upload PDF/text file and return extracted text + preview
- `POST /summarize` -> Input: `{ "text": "..." }` -> summary
- `POST /keypoints` -> Input: `{ "text": "..." }` -> key points list
- `POST /generate-quiz` -> Input: `{ "text": "..." }` -> quiz list with:

```json
{
	"question": "",
	"options": [""],
	"answer": ""
}
```

## NLP Integration Notes

Current implementation supports two modes:
- LLM mode (recommended): Gemini-powered generation for summary, key points, and quiz quality similar to modern AI assistants.
- Fallback mode: local deterministic logic when API key is not configured.

- `backend/app/services/llm_client.py`
	- Central Gemini API wrapper
	- Handles JSON extraction for structured outputs
- `backend/app/services/summarize.py`
	- LLM summary prompt with concise highlights
- `backend/app/services/keypoints.py`
	- LLM key-point extraction into structured JSON
- `backend/app/services/quiz_generator.py`
	- LLM MCQ generation with validation of options/answers

You can still swap to HuggingFace/local models later by editing service modules.

## Future Expansion Ideas

- Add a database (e.g., PostgreSQL) to save uploads and study history
- Add user authentication
- Add model selection per task (summary/key points/quiz)
- Add caching for repeated requests
- Add background jobs for large files