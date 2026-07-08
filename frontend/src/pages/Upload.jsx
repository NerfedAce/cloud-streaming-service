import { useState } from "react";
import axios from "axios";
import "./Upload.css";
import {useParams} from "react-router-dom";

function Upload() {
  const [title, setTitle] = useState("");
  const [video, setVideo] = useState(null);
  const API_URL = import.meta.env.VITE_API_URL;
  const {user} = useParams();
  const handleUpload = async () => {
    if (!video) {
      alert("Please select a video.");
      return;
    }

    const formData = new FormData();

    formData.append("title", title);
    formData.append("video", video);

    try {
      await axios.post(
        `${API_URL}/upload/${user}`,
        formData
      );

      alert("Video uploaded!");

      setTitle("");
      setVideo(null);
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-card">

        <h1>Upload Video</h1>

        <input
          className="upload-input"
          type="text"
          placeholder="Video Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="upload-file"
          type="file"
          accept="video/*"
          onChange={(e) => setVideo(e.target.files[0])}
        />

        {video && (
          <p className="filename">
            {video.name}
          </p>
        )}

        <button
          className="upload-btn"
          onClick={handleUpload}
        >
          Upload
        </button>

      </div>
    </div>
  );
}

export default Upload;
