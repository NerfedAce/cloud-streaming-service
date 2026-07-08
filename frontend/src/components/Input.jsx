import {useState} from "react";
import "./Input.css"

function Input ({value , onChange , placeholder}){

    return (
        <div className="input-container">
            <input className="input-group" placeholder={placeholder} value={value} onChange={(e) => onChange(e.target.value)} />
        </div>
    )

}

export default Input;