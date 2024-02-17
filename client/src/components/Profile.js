import React, { } from "react";
import {useNavigate} from "react-router-dom";
 
export default function Profile(){
    const navigate = useNavigate();
    const signOut = () => {
        localStorage.removeItem('cairocodersToken')
        navigate("/");
    }
    return(
        <>
            <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h2 className="card-title">Profile Page</h2>
                            <p className="card-text">Hi, this is your profile</p>
                            <button className="btn btn-success" onClick={signOut}>Sign Out</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
             
        </>
    )
}