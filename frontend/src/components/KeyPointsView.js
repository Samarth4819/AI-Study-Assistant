import React from "react";

export default function KeyPointsView({ keyPoints }) {
  return (
    <article className="result-card">
      <h2>Key Points</h2>
      {keyPoints.length > 0 ? (
        <ul>
          {keyPoints.map((point, index) => (
            <li key={`${point.slice(0, 20)}-${index}`}>{point}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">Key points will appear here.</p>
      )}
    </article>
  );
}
