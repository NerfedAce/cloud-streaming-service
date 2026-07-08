import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Stream.css";

function Stream() {
    const { id } = useParams();
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;
    const [video, setVideo] = useState(null);

    useEffect(() => {
        const fetchVideo = async () => {
            try {
                const response = await axios.get(
                    `${API_URL}/api/video/${id}`
                );

                setVideo(response.data);
            } catch (err) {
                console.error(err);
            }
        };

        fetchVideo();
    }, [id]);

    if (!video) return <h2>Loading...</h2>;

    return (
        <div className="stream-page">
            <div className="stream-container">

                <h1 className="stream-title">
                    {video.title}
                </h1>

                <video className="stream-video" controls>
                    <source src={video.url} type="video/mp4" />
                </video>

                <div className="stream-info">
                    <span className="stream-length">
                        {video.length} minutes
                    </span>
                </div>

            </div>
        </div>
    );
}

export default Stream;
