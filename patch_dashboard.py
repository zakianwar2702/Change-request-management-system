from pathlib import Path

path = Path('src/pages/Dashboard.jsx')
new_content = '''import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [recentTickets, setRecentTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/summary/")
      .then((response) => {
        if (!response.ok) throw new Error("Dashboard API fetch failed");
        return response.json();
      })
      .then((data) => {
        setSummary(data.summary);
        setRecentTickets(data.recent_tickets || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const cards = [
    { title: "Total Requests", value: summary?.total ?? 45, color: "#2563EB" },
    { title: "Open", value: summary?.open ?? 8, color: "#F59E0B" },
    { title: "In Progress", value: summary?.in_progress ?? 5, color: "#8B5CF6" },
    { title: "Resolved", value: summary?.resolved ?? 12, color: "#06B6D4" },
    { title: "Closed", value: summary?.closed ?? 15, color: "#22C55E" },
    { title: "Recent Tickets", value: recentTickets.length, color: "#EF4444" },
  ];

  return (
    <Layout>
      <h1>CRM Dashboard</h1>

      <p style={{ color: "#64748B" }}>
        Welcome to the Change Management Dashboard
      </p>

      <div style={{ marginTop: "20px", marginBottom: "20px" }}>
        <button onClick={() => navigate("/request-form")}>Create Request</button>

        <button
          style={{ marginLeft: "10px" }}
          onClick={() => navigate("/request-list")}
        >
          View Requests
        </button>

        <button
          style={{ marginLeft: "10px" }}
          onClick={() => navigate("/approval")}
        >
          Approval Queue
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3,1fr)",
          gap: "20px",
        }}
      >
        {cards.map((card, index) => (
          <div
            key={index}
            style={{
              background: card.color,
              color: "white",
              padding: "20px",
              borderRadius: "12px",
            }}
          >
            <h3>{card.title}</h3>
            <h1>{card.value}</h1>
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: "40px" }}>
        Recent Change Requests
      </h2>

      <table
        style={{
          width: "100%",
          marginTop: "15px",
          background: "white",
        }}
      >
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Requester</th>
          </tr>
        </thead>

        <tbody>
          {loading ? (
            <tr>
              <td colSpan="4" style={{ textAlign: "center" }}>
                Loading tickets…
              </td>
            </tr>
          ) : error ? (
            <tr>
              <td colSpan="4" style={{ textAlign: "center", color: "red" }}>
                {error}
              </td>
            </tr>
          ) : recentTickets.length === 0 ? (
            <tr>
              <td colSpan="4" style={{ textAlign: "center" }}>
                No recent tickets found.
              </td>
            </tr>
          ) : (
            recentTickets.map((ticket) => (
              <tr key={ticket.id}>
                <td>{ticket.id}</td>
                <td>{ticket.title}</td>
                <td>{ticket.status}</td>
                <td>{ticket.requester}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </Layout>
  );
}

export default Dashboard;
'''

path.write_text(new_content, encoding='utf-8')
print('Updated Dashboard.jsx')
