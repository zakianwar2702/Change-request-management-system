import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import "./Dashboard.css";

function RequestList() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/tickets/")
      .then((res) => res.json())
      .then((data) => {
        setRequests(data || []);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <div className="dashboard">

        {/* HEADER */}
        <div className="dashboard-header">
          <h1>All Requests</h1>
          <p>View and track all change requests</p>
        </div>

        {/* TABLE */}
        <div className="table-section">
          <h2>Request List</h2>

          <table className="dashboard-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Status</th>
                <th>Requester</th>
              </tr>
            </thead>

            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="5">Loading requests...</td>
                </tr>
              ) : requests.length === 0 ? (
                <tr>
                  <td colSpan="5">No requests found</td>
                </tr>
              ) : (
                requests.map((req) => (
                  <tr key={req.id}>
                    <td>{req.ticket_number}</td>
<td>{req.project_name}</td>
<td>{req.description}</td>
<td>
  <span className={`status ${req.status?.toLowerCase()}`}>
    {req.status}
  </span>
</td>
<td>{req.employee_name}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

      </div>
    </Layout>
  );
}

export default RequestList;