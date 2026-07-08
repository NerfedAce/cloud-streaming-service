import Input from "../components/Input";
import "./Login.css"
import axios from "axios";
import {useState} from "react";
import Card from "../components/Card";
import {Navigate, useNavigate} from "react-router-dom";


function Login() {

    const [form, setForm] = useState({user:"",password:""})

    const handleChange = (field,val) => {
        setForm({...form, [field]: val})
    }
    const navigate = useNavigate()
    const onLogin = async () => {
        try {
            const response = await axios.post("http://localhost:8000/login",form)
            if (response.status === 200){
                navigate(`/dashboard/${form.user}`)
            }
            else{
                console.log("error")
            }
        }
        catch(error){
            console.log(error)
        }

    }

    return (
        <>
            <div className="login-page">
                <div className="login">
                    <h2 className="heading"> LOGIN </h2>

                    <Input value={form.user} onChange={(value) => handleChange("user" , value)} placeholder="enter userID" />
                    <Input value={form.pass} onChange={(value) => handleChange("password",value)} placeholder="enter password" />
                    <button onClick={onLogin}>Login</button>
                </div>
            </div>

        </>
    )
}

export default Login