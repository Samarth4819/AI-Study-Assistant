import React from "react";

export default function SummaryView({ summary }) {
  return (
    <article className="result-card">
      <h2>Summary</h2>
      {summary ? <p>{summary}</p> : <p className="muted">Summary will appear here.</p>}
    </article>
  );
}
