import React, { useMemo, useState } from "react";
import { BrowserRouter, Routes, Route, NavLink, Navigate } from "react-router-dom";
import UploadForm from "./components/UploadForm";
import SummaryView from "./components/SummaryView";
import KeyPointsView from "./components/KeyPointsView";
import QuizView from "./components/QuizView";
import { generateQuiz, getKeyPoints, summarizeText, uploadFile } from "./api/api";

export default function App() {
  const [sourceText, setSourceText] = useState("");
  const [summary, setSummary] = useState("");
  const [keyPoints, setKeyPoints] = useState([]);
  const [quiz, setQuiz] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const hasContent = useMemo(() => sourceText.trim().length > 0, [sourceText]);

  async function handleUpload(file) {
    setError("");
    setLoading(true);

    try {
      const data = await uploadFile(file);
      setSourceText(data.extracted_text || "");
      setSummary("");
      setKeyPoints([]);
      setQuiz([]);
    } catch (err) {
      setError(err.message || "Failed to upload file.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGenerateAll() {
    if (!hasContent) {
      setError("Please upload a PDF or text file first.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const [summaryData, keyPointsData, quizData] = await Promise.all([
        summarizeText(sourceText),
        getKeyPoints(sourceText),
        generateQuiz(sourceText),
      ]);

      setSummary(summaryData.summary || "");
      setKeyPoints(keyPointsData.key_points || []);
      setQuiz(quizData.quiz || []);
    } catch (err) {
      setError(err.message || "Failed to process study content.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <BrowserRouter>
      <div className="app-shell">
        <header className="hero">
          <h1>AI Study Assistant</h1>
          <p>
            Upload notes or PDFs and instantly get summaries, key points, and quiz questions.
          </p>
          <nav className="nav-menu">
            <NavLink to="/upload" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>Home</NavLink>
            <NavLink to="/summary" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>Summary</NavLink>
            <NavLink to="/overview" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>Overview</NavLink>
            <NavLink to="/quiz" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>Quiz</NavLink>
          </nav>
        </header>

        <main className="dashboard-pages">
          <Routes>
            <Route path="/" element={<Navigate to="/upload" replace />} />
            
            <Route path="/upload" element={
              <section className="panel" style={{ gridColumn: "1 / -1", maxWidth: "600px", margin: "0 auto" }}>
                <UploadForm onUpload={handleUpload} disabled={loading} />
                <button
                  className="primary-btn"
                  onClick={handleGenerateAll}
                  disabled={loading || !hasContent}
                  type="button"
                >
                  {loading ? "Processing..." : "Generate Study Materials"}
                </button>

                {error && <p className="error-text">{error}</p>}

                {hasContent && (
                  <div className="preview-card" style={{ marginTop: "20px" }}>
                    <h3>Extracted Text Preview</h3>
                    <p>{sourceText.slice(0, 500)}{sourceText.length > 500 ? "..." : ""}</p>
                  </div>
                )}
              </section>
            } />

            <Route path="/summary" element={
              <section className="panel" style={{ gridColumn: "1 / -1" }}>
                {!summary && hasContent && <p className="muted">Click "Generate Study Materials" on the Home page first.</p>}
                {!hasContent && <p className="muted">Please upload a file from the Home page first.</p>}
                {summary && <SummaryView summary={summary} />}
              </section>
            } />

            <Route path="/overview" element={
              <section className="panel" style={{ gridColumn: "1 / -1" }}>
                {keyPoints.length === 0 && hasContent && <p className="muted">Click "Generate Study Materials" on the Home page first.</p>}
                {!hasContent && <p className="muted">Please upload a file from the Home page first.</p>}
                {keyPoints.length > 0 && <KeyPointsView keyPoints={keyPoints} />}
              </section>
            } />

            <Route path="/quiz" element={
              <section className="panel" style={{ gridColumn: "1 / -1" }}>
                {quiz.length === 0 && hasContent && <p className="muted">Click "Generate Study Materials" on the Home page first.</p>}
                {!hasContent && <p className="muted">Please upload a file from the Home page first.</p>}
                {quiz.length > 0 && <QuizView quiz={quiz} />}
              </section>
            } />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
