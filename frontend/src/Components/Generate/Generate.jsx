import React, { useState } from "react";
import axios from "axios";
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import './Generate.css';

const Generate = () => {
  const [difficulty, setDifficulty] = useState("easy");
  const [riddle, setRiddle] = useState(null);
  const [riddleId, setRiddleId] = useState(null);
  const [answer, setAnswer] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [error, setError] = useState("");
  const API_URL = "http://192.168.187.160:8000";

  const generateEnigma = async () => {
    try {
      const response = await axios.post(`${API_URL}/enigma/generate/`, {
        level: difficulty
      });
      setRiddle(response.data.riddle);
      setRiddleId(response.data.id);
      setAnswer(null);
      setUserAnswer("");
      setFeedback("");
      setError("");
    } catch (error) {
      setError("Failed to generate riddle.");
      setRiddle(null);
      setRiddleId(null);
      setAnswer(null);
      setUserAnswer("");
      setFeedback("");
    }
  };

const revealAnswer = async () => {
  if (!riddleId) return;
  try {
    const response = await axios.get(`${API_URL}/enigma/answer/${riddleId}/`);
    setAnswer(response.data.answer);
  } catch (err) {
    setAnswer("Failed to load answer.");
  }
};


  const checkUserAnswer = () => {
    if (!userAnswer || !answer) return;

    const user = userAnswer.trim().toLowerCase();
    const correct = answer.trim().toLowerCase();

    if (user === correct) {
      setFeedback("🎉 Great job! You got it right!");
    } else {
      setFeedback("❌ Try again!");
    }
  };

  const resetRiddle = () => {
    setRiddle(null);
    setRiddleId(null);
    setAnswer(null);
    setUserAnswer("");
    setFeedback("");
    setError("");
  };

  return (
    <div className="enigme-container">
      <div className="generation">
        <strong>Select difficulty</strong>
        <select
          name="difficulty"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">Easy</option>
          <option value="hard">Hard</option>
        </select>
        <button onClick={generateEnigma}>Generate</button>
      </div>

      {riddle && (
        <div className="riddle-box">
          <h3>🧩 Riddle:</h3>
          <p>{riddle}</p>

          <input
            className="answer-input"
            type="text"
            placeholder="Your answer"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
          /><br />
          <button className="check-btn" onClick={checkUserAnswer}>Check Answer</button>

          <button className="reveal-button" onClick={revealAnswer}>
            See Answer
          </button>

          {answer && <p className="answer">✅ Answer: {answer}</p>}

          <button className="reset-button" onClick={resetRiddle}>Reset</button>

          {feedback && <p className="popup">{feedback}</p>}
        </div>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Generate;
