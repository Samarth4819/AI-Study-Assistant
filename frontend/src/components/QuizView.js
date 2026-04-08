import React, { useState } from "react";

export default function QuizView({ quiz }) {
  const [selectedAnswers, setSelectedAnswers] = useState({});

  function selectOption(questionIndex, option) {
    setSelectedAnswers((prev) => ({ ...prev, [questionIndex]: option }));
  }

  return (
    <article className="result-card">
      <h2>Quiz</h2>
      {quiz.length === 0 && <p className="muted">Quiz questions will appear here.</p>}

      {quiz.map((item, qIndex) => {
        const selected = selectedAnswers[qIndex];
        const showResult = Boolean(selected);
        const isCorrect = selected === item.answer;

        return (
          <div className="quiz-item" key={`${item.question.slice(0, 20)}-${qIndex}`}>
            <h3>{qIndex + 1}. {item.question}</h3>

            <div className="quiz-options">
              {item.options.map((option, optIndex) => (
                <button
                  key={`${option.slice(0, 10)}-${optIndex}`}
                  type="button"
                  className={`option-btn ${selected === option ? "selected" : ""}`}
                  onClick={() => selectOption(qIndex, option)}
                >
                  {option}
                </button>
              ))}
            </div>

            {showResult && (
              <p className={isCorrect ? "correct" : "incorrect"}>
                {isCorrect ? "Correct!" : `Not quite. Correct answer: ${item.answer}`}
              </p>
            )}
          </div>
        );
      })}
    </article>
  );
}
