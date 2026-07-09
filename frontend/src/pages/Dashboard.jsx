import Card from "../components/Card";
import axios from "axios";
import { useEffect, useState } from "react";
import {useNavigate, useParams} from "react-router-dom";
import "./Dashboard.css";
import {Navigate} from "react-router-dom";



function Dashboard() {
    const { user } = useParams();
    const [videos, setVideos] = useState([]);
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    useEffect(() => {
        const fetchVideos = async () => {
            try {
                const response = await axios.get(
                    `${API_URL}/api/videos/${user}`
                );
                setVideos(response.data);
            } catch (err) {
                console.log(err);
            }
        };

        fetchVideos();
    }, [user]);

    return (
        <div className="dashboard">
            <div className="changeTab">
                <h2 onClick={() =>{ navigate(`/upload/${user}`)} } style={{
        display: "inline-block",
        backgroundColor: "#2563eb",
        color: "white",
        padding: "10px 20px",
        borderRadius: "8px",
        cursor: "pointer",
        userSelect: "none",
    }}>UPLOAD</h2>
            </div>
            {videos.map(video => (
                <Card
                    key={video.id}
                    id={video.id}
                    img={video.img}
                    title={video.title}
                    length={video.length}
                />
            ))}
        </div>
    );
}

export default Dashboard;
