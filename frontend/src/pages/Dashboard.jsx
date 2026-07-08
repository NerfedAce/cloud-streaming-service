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


    useEffect(() => {
        const fetchVideos = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/api/videos/${user}`
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
                <h2 onClick={() =>{ navigate(`/upload/${user}`)} }>upload</h2>
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