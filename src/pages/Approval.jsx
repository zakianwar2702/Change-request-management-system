import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import "./Dashboard.css";

function Approval() {
  const [requests, setRequests] = useState([]);
  const [level, setLevel] = useState(1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);

    fetch(`http://127.0.0.1:8000/api/approvals/level${level}/`)
      .then((res) => res.json())
      .then((data) => {
        console.log("LEVEL DATA:", data);
        setRequests(data);
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [level]);

  const approveRequest = (id, status) => {
    fetch(`http://127.0.0.1:8000/api/approvals/approve/${id}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        status: status,
        remarks: "Updated",
      }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Approval Updated Successfully");
        window.location.reload();
      });
  };

  return (
    <Layout>
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Approval Queue</h1>
          <p>Manage Level 1 and Level 2 approvals</p>
        </div>

        {/* Level Buttons */}
        <div
          style={{
            display: "flex",
            gap: "15px",
            marginBottom: "25px",
          }}
        >
          <button
            onClick={() => setLevel(1)}
            style={{
              background: level === 1 ? "#2563EB" : "#E5E7EB",
              color: level === 1 ? "white" : "#374151",
              border: "none",
              padding: "12px 28px",
              borderRadius: "10px",
              cursor: "pointer",
              fontWeight: "600",
              fontSize: "15px",
              transition: "0.3s",
              boxShadow:
                level === 1
                  ? "0 4px 12px rgba(37,99,235,0.35)"
                  : "0 2px 6px rgba(0,0,0,0.15)",
            }}
          >
            Level 1
          </button>

          <button
            onClick={() => setLevel(2)}
            style={{
              background: level === 2 ? "#2563EB" : "#E5E7EB",
              color: level === 2 ? "white" : "#374151",
              border: "none",
              padding: "12px 28px",
              borderRadius: "10px",
              cursor: "pointer",
              fontWeight: "600",
              fontSize: "15px",
              transition: "0.3s",
              boxShadow:
                level === 2
                  ? "0 4px 12px rgba(37,99,235,0.35)"
                  : "0 2px 6px rgba(0,0,0,0.15)",
            }}
          >
            Level 2
          </button>
        </div>

        <div className="table-section">
          <h2>Level {level} Pending Requests</h2>

          <table className="dashboard-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Ticket</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="4">Loading...</td>
                </tr>
              ) : requests.length === 0 ? (
                <tr>
                  <td colSpan="4">No approvals found</td>
                </tr>
              ) : (
                requests.map((req) => (
                  <tr key={req.id}>
                    <td>{req.id}</td>

                    <td>{req.ticket}</td>

                    <td>
                      <span
                        style={{
                          padding: "6px 12px",
                          borderRadius: "20px",
                          background: "#FEF3C7",
                          color: "#92400E",
                          fontWeight: "600",
                        }}
                      >
                        {req.status}
                      </span>
                    </td>

                    <td>
                      <button
                        onClick={() =>
                          approveRequest(req.id, "Approved")
                        }
                        style={{
                          background: "#16A34A",
                          color: "white",
                          border: "none",
                          padding: "8px 18px",
                          borderRadius: "8px",
                          cursor: "pointer",
                          fontWeight: "600",
                          marginRight: "10px",
                        }}
                      >
                        ✓ Approve
                      </button>

                      <button
                        onClick={() =>
                          approveRequest(req.id, "Rejected")
                        }
                        style={{
                          background: "#DC2626",
                          color: "white",
                          border: "none",
                          padding: "8px 18px",
                          borderRadius: "8px",
                          cursor: "pointer",
                          fontWeight: "600",
                        }}
                      >
                        ✕ Reject
                      </button>
                    </td>
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

export default Approval;