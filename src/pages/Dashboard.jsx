import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard() {
  const navigate = useNavigate();

  const [darkMode, setDarkMode] = useState(false);

  const [summary, setSummary] = useState(null);
  const [recentTickets, setRecentTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/tickets/summary/")
      .then((res) => {
        if (!res.ok) throw new Error("Dashboard API fetch failed");
        return res.json();
      })
      .then((data) => {
        setSummary(data.summary);
        setRecentTickets(data.recent_tickets || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const chartData = [
    { name: "Open", value: summary?.open ?? 0 },
    { name: "In Progress", value: summary?.in_progress ?? 0 },
    { name: "Resolved", value: summary?.resolved ?? 0 },
    { name: "Closed", value: summary?.closed ?? 0 },
  ];

  const COLORS = ["#F59E0B", "#8B5CF6", "#06B6D4", "#22C55E"];

  const cards = [
    { title: "Total Requests", value: summary?.total ?? 0 },
    { title: "Open", value: summary?.open ?? 0 },
    { title: "In Progress", value: summary?.in_progress ?? 0 },
    { title: "Resolved", value: summary?.resolved ?? 0 },
    { title: "Closed", value: summary?.closed ?? 0 },
    { title: "Recent Tickets", value: recentTickets.length },
  ];

  return (
    <Layout>
      <div className={darkMode ? "dashboard dark" : "dashboard"}>

        {/* TOP BAR */}
        <div className="topbar">

          <h2>CRM Dashboard</h2>

          <div className="action-buttons">

            {/* DARK MODE TOGGLE (FIXED) */}
            <button onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
            </button>

            {/* CREATE REQUEST */}
            <button onClick={() => navigate("/request-form")}>
              ➕ Create Request
            </button>

          </div>

        </div>

        {/* CARDS */}
        <div className="card-grid">
          {cards.map((c, i) => (
            <div key={i} className="card">
              <h3>{c.title}</h3>
              <h1>{c.value}</h1>
            </div>
          ))}
        </div>

        {/* CHART */}
        <div className="chart-box">
          <h3>Request Overview</h3>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                outerRadius={120}
                label
              >
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* TABLE */}
        <div className="table-section">
          <h2>Recent Change Requests</h2>

          <table className="dashboard-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Status</th>
                <th>Requester</th>
              </tr>
            </thead>

            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="4">Loading...</td>
                </tr>
              ) : error ? (
                <tr>
                  <td colSpan="4">{error}</td>
                </tr>
              ) : recentTickets.length === 0 ? (
                <tr>
                  <td colSpan="4">No data found</td>
                </tr>
              ) : (
                recentTickets.map((t) => (
                  <tr key={t.id}>
                    <td>#{t.id}</td>
                    <td>{t.title}</td>
                    <td>{t.status}</td>
                    <td>{t.requester}</td>
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

export default Dashboard;