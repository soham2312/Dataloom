import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Profile({ currentUser }) { // Assuming currentUser is passed as a prop
    const navigate = useNavigate();
    const [selectedFiles, setSelectedFiles] = useState([]);

    const handleFileChange = (event) => {
        setSelectedFiles(Array.from(event.target.files));
    };

    const uploadFiles = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("username", currentUser.username); // Add the current user's username

        selectedFiles.forEach(file => {
            formData.append("file", file);
        });

        try {
            const response = await fetch("http://127.0.0.1:8000/file/upload/", {
                method: "POST",
                body: formData,
            });
            console.log(response.status);
            if (response.ok) {
                console.log("Files uploaded successfully");
            } else {
                const errorText = await response.text();
                console.error("Failed to upload files:", errorText);
            }
        } catch (error) {
            console.error("Error uploading files:", error);
        }
    };

    const signOut = () => {
        localStorage.removeItem("cairocodersToken");
        navigate("/");
    };

    return (
        <>
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <div>
                                    <input type="file" onChange={handleFileChange} multiple />
                                    <button className="btn btn-primary" onClick={uploadFiles}>Upload</button>
                                </div>
                                <hr />
                                <h4>Manage Datasets:</h4>
                                {/* Display list of selected files */}
                                {selectedFiles.map((file, index) => (
                                    <p key={index}>{file.name}</p>
                                ))}
                                <button className="btn btn-success" onClick={signOut}>Sign Out</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}