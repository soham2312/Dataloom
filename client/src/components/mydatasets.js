import React, { useState, useEffect } from "react";
import axios from 'axios';

const Datasets = () => {
    const [datasets, setDatasets] = useState([]);

    useEffect(() => {
        // Fetch datasets from the backend
        const tok = localStorage.getItem('cairocodersToken');
        axios.get('http://localhost:8000/mydatasets', {
            headers: {
                'Authorization': `Bearer ${tok}`
            }
        }).then(response => {
            console.log('Response from API:', response.data); // Log the response data
            const formattedData = response.data.map(dataset => ({
                id: dataset._id.$oid, // Convert ObjectId to string or appropriate format
                name: dataset.name, // Assuming dataset object has a 'name' field
                // Add other fields as needed
            }));
            setDatasets(formattedData); // Update datasets state with formatted data
        }).catch(error => {
            console.error('Error fetching datasets:', error);
        });
    }, []);

    // Handle view and download dataset actions as before
    const handleViewDataset = (id) => {
        console.log('View dataset:', id);
    };

    const handleDownloadDataset = (id) => {
        console.log('Download dataset:', id);
    }

    return (
        <div className="container mt-5">
            <h1>Datasets</h1>
            <table className="table table-bordered">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {/* {datasets.map(dataset => (
                        <tr key={dataset.id}>
                            <td>{dataset.name}</td>
                            <td>
                                <button className="btn btn-primary" onClick={() => handleViewDataset(dataset.id)}>
                                    View
                                </button>
                                <button className="btn btn-secondary" onClick={() => handleDownloadDataset(dataset.id)}>
                                    Download
                                </button>
                            </td>
                        </tr>
                    ))} */}
                </tbody>
            </table>
        </div>
    );
};

export default Datasets;
