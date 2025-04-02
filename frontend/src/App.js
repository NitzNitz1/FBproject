import React, { useState } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [jobId, setJobId] = useState('');
  const [jobData, setJobData] = useState(null);
  const [loading, setLoading] = useState(false);

  const createJob = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/job?username=${username}`, {
        method: 'POST'
      });
      const data = await response.json();
      setJobId(data.job_id);
      alert("Job created successfully!");
    } catch (error) {
      alert("Failed creating a job");
    } finally {
      setLoading(false);
    }
  };

  const fetchJob = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/job/${jobId}`);
      const data = await response.json();
      setJobData(data);
    } catch (error) {
      alert("ERROR");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1> Facebook Job Lookup</h1>

      <div className="form">
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Insert a username"
        />
        <button onClick={createJob} disabled={loading || !username}>
          Create a job
        </button>
      </div>

      {jobId && (
        <div className="status-section">
          <h3>Job ID: {jobId}</h3>
          <button onClick={fetchJob} disabled={loading}>
            Show job details
          </button>
        </div>
      )}

      {jobData && (
  <div className="result">
    <h3>JOB DETAILS:</h3>
    <table className="job-table">
      <tbody>
        <tr><td><strong>ID:</strong></td><td>{jobData._id}</td></tr>
        <tr><td><strong>Username:</strong></td><td>{jobData.username}</td></tr>
<tr>
  <td><strong>Status:</strong></td>
  <td>
    <span className={`status ${jobData.status.toLowerCase()}`}>
      {jobData.status}
    </span>
  </td>
</tr>
        <tr><td><strong>Start:</strong></td><td>{jobData.start_date}</td></tr>
        <tr><td><strong>End:</strong></td><td>{jobData.end_date || "—"}</td></tr>
        <tr><td><strong>FBID:</strong></td><td>{jobData.fbid || "—"}</td></tr>
        <tr><td><strong>Success:</strong></td><td>{jobData.success === null ? "—" : jobData.success.toString()}</td></tr>
        <tr><td><strong>Error:</strong></td><td>{jobData.error_message || "—"}</td></tr>
      </tbody>
    </table>
  </div>
)}

    </div>
  );
}

export default App;
