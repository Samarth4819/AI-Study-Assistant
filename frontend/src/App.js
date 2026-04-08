import React, { useMemo, useState } from "react";
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
    <div className="app-shell">
      <header className="hero">
        <h1>AI Study Assistant</h1>
        <p>
          Upload notes or PDFs and instantly get summaries, key points, and quiz questions.
        </p>
      </header>

      <main className="dashboard">
        <section className="panel">
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
            <div className="preview-card">
              <h3>Extracted Text Preview</h3>
              <p>{sourceText.slice(0, 500)}{sourceText.length > 500 ? "..." : ""}</p>
            </div>
          )}
        </section>

        <section className="panel outputs">
          <SummaryView summary={summary} />
          <KeyPointsView keyPoints={keyPoints} />
          <QuizView quiz={quiz} />
        </section>
      </main>
    </div>
  );
}
