const API_BASE_URL = "http://localhost:8000";

async function parseResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Something went wrong while calling the API.");
  }
  return data;
}

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(response);
}

export async function summarizeText(text) {
  const response = await fetch(`${API_BASE_URL}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  return parseResponse(response);
}

export async function getKeyPoints(text) {
  const response = await fetch(`${API_BASE_URL}/keypoints`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  return parseResponse(response);
}

export async function generateQuiz(text) {
  const response = await fetch(`${API_BASE_URL}/generate-quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  return parseResponse(response);
}
