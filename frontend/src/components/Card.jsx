import "./Card.css"
import {Link} from "react-router-dom";

function Card({img , title , length ,id}){

    return(
        <Link to={`/stream/${id}`} className="card-link">
            <div className="card-container">
                <div className="card">
                    <div className="card-body">
                        <img src={img} alt = "error"/>
                        <h2>{title}</h2>
                        <h3> length : {length}</h3>
                    </div>
                </div>
            </div>
        </Link>
    )
}

export default Card;