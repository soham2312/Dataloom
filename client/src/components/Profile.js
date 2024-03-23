import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Dropzone from "react-dropzone";
import { parse as parseCSV } from "papaparse";
import XLSX from "xlsx"; // Import XLSX library for Excel file parsing
import axios from 'axios';
export default function Profile() {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState(null);

    const signOut = () => {
        localStorage.removeItem('cairocodersToken');
        navigate("/");
    };

    const handleDrop = (acceptedFiles) => {
        const uploadedFile = acceptedFiles[0];
        setFile(uploadedFile);
        setError(null); // Clear previous error
    };

    const handleFileView = () => {
        if (file) {
            setLoading(true); // Set loading state while loading file content
            const reader = new FileReader();
            reader.onload = (e) => {
                const fileContent = e.target.result;
                // Check if the file is CSV or Excel
                if (file.name.endsWith('.csv')) {
                    parseCSV(fileContent, {
                        complete: (result) => {
                            setLoading(false); // Clear loading state after loading file content
                            setData(result.data);
                        },
                        error: (err) => {
                            setLoading(false); // Clear loading state in case of error
                            setError(err.message);
                        }
                    });
                } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
                    const workbook = XLSX.read(fileContent, { type: 'binary' });
                    const sheetName = workbook.SheetNames[0]; // Assume only one sheet
                    const sheet = workbook.Sheets[sheetName];
                    const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
                    setLoading(false); // Clear loading state after loading file content
                    setData(jsonData);
                } else {
                    setError("Unsupported file format");
                    setLoading(false); // Clear loading state
                }
            };
            reader.readAsBinaryString(file);
        }
    };

    const handleFileDownload = () => {
        if (file) {
            // Create a download link for the file
            const downloadLink = document.createElement("a");
            downloadLink.href = URL.createObjectURL(file);
            downloadLink.download = file.name;
            document.body.appendChild(downloadLink);
            // Simulate click on the download link
            downloadLink.click();
            // Remove the download link from the document
            document.body.removeChild(downloadLink);
        }
    };

    const handleFileUpload = async (username) => {
        if (file) {
            setLoading(true); // Set loading state while uploading file

            try {
                const formData = new FormData();
                formData.append("file", file);
                const tok = localStorage.getItem('cairocodersToken');

                const response = await axios.post("http://localhost:8000/upload", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `${tok}`,
                    }
                });


                if (response.data.message === "success") {
                    setLoading(false); // Clear loading state after successful upload
                    console.log("File uploaded successfully");
                } else {
                    throw new Error("Failed to upload file");
                }
            } catch (error) {
                setLoading(false); // Clear loading state in case of error
                console.error("Error uploading file:", error);
                setError("Error uploading file. Please try again.");
            }
        }
    };
    const handleMyDatasets = () => {
        navigate("/mydatasets"); // Redirect to the "My Datasets" page
    };
    return (
        <div className="container mt-5">
            <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">Your App</a>
                    <button
                        className="btn btn-primary btn-sm"
                        onClick={handleMyDatasets}
                    >
                        My Datasets
                    </button>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <button className="btn btn-outline-danger" onClick={signOut}>Sign Out</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <Dropzone onDrop={handleDrop}>
                        {({ getRootProps, getInputProps }) => (
                            <section>
                                <div {...getRootProps()} className="dropzone">
                                    <input {...getInputProps()} />
                                    <p>Drag & drop files here, or click to select files</p>
                                </div>
                            </section>
                        )}
                    </Dropzone>
                    {file && (
                        <div>
                            <h4>Uploaded File:</h4>
                            <span>{file.name}</span>
                            <button
                                className="btn btn-primary btn-sm mx-2"
                                onClick={handleFileView}
                            >
                                View
                            </button>
                            <button
                                className="btn btn-secondary btn-sm"
                                onClick={handleFileDownload}
                            >
                                Download
                            </button>
                            <button
                                className="btn btn-success btn-sm"
                                onClick={handleFileUpload}
                            >
                                Upload
                            </button>
                            {loading && <p>Loading file...</p>}
                            {error && <p className="text-danger">{error}</p>}
                            {data && (
                                <div>
                                    <h4>File Content:</h4>
                                    <table className="table table-bordered">
                                        <thead>
                                            <tr>
                                                {data[0].map((header, index) => (
                                                    <th key={index}>{header}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {data.slice(1).map((row, rowIndex) => (
                                                <tr key={rowIndex}>
                                                    {row.map((cell, cellIndex) => (
                                                        <td key={cellIndex}>{cell}</td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
