import React, { useState } from "react";

export default function UploadForm({ onUpload, disabled }) {
  const [file, setFile] = useState(null);

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!file || disabled) return;
    await onUpload(file);
  }

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <label htmlFor="fileInput">Upload PDF or text notes</label>
      <input
        id="fileInput"
        type="file"
        accept=".pdf,.txt,.md,.csv"
        onChange={handleFileChange}
        disabled={disabled}
      />
      <button className="secondary-btn" type="submit" disabled={!file || disabled}>
        Upload File
      </button>
    </form>
  );
}
