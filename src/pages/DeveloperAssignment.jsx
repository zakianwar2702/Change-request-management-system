import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import "./Dashboard.css";

function DeveloperAssignment() {
  const [tickets, setTickets] = useState([]);
  const [developers, setDevelopers] = useState([]);
  const [selectedDeveloper, setSelectedDeveloper] = useState({});

  useEffect(() => {
    loadTickets();
    loadDevelopers();
  }, []);

  const loadTickets = () => {
    fetch("http://127.0.0.1:8000/api/tickets/")
      .then((res) => res.json())
      .then((data) => setTickets(data))
      .catch((err) => console.error(err));
  };

  const loadDevelopers = () => {
    fetch("http://127.0.0.1:8000/api/tickets/users/")
      .then((res) => res.json())
      .then((data) => setDevelopers(data))
      .catch((err) => console.error(err));
  };

  const assignDeveloper = (ticketId) => {
    const developerId = selectedDeveloper[ticketId];

    if (!developerId) {
      alert("Please select a developer.");
      return;
    }

    fetch("http://127.0.0.1:8000/api/tickets/assign-developer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        change_request: ticketId,
        developer: developerId,
      }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Developer assigned successfully.");
        loadTickets();
      })
      .catch((err) => console.error(err));
  };

  return (
    <Layout>
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Developer Assignment</h1>
          <p>Assign approved change requests to developers</p>
        </div>

        <div className="table-section">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Ticket</th>
                <th>Employee</th>
                <th>Project</th>
                <th>Status</th>
                <th>Developer</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {tickets.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ textAlign: "center" }}>
                    No tickets found.
                  </td>
                </tr>
              ) : (
                tickets.map((ticket) => (
                  <tr key={ticket.id}>
                    <td>{ticket.ticket_number}</td>

                    <td>{ticket.employee_name}</td>

                    <td>{ticket.project_name}</td>

                    <td>
                      <span
                        style={{
                          background:
                            ticket.status === "Open"
                              ? "#DBEAFE"
                              : ticket.status === "In Progress"
                              ? "#FEF3C7"
                              : "#DCFCE7",
                          color:
                            ticket.status === "Open"
                              ? "#1D4ED8"
                              : ticket.status === "In Progress"
                              ? "#92400E"
                              : "#166534",
                          padding: "6px 14px",
                          borderRadius: "20px",
                          fontWeight: "600",
                          fontSize: "13px",
                        }}
                      >
                        {ticket.status}
                      </span>
                    </td>

                    <td>
                      <select
                        value={selectedDeveloper[ticket.id] || ""}
                        onChange={(e) =>
                          setSelectedDeveloper({
                            ...selectedDeveloper,
                            [ticket.id]: e.target.value,
                          })
                        }
                        style={{
                          width: "180px",
                          padding: "10px",
                          borderRadius: "8px",
                          border: "1px solid #CBD5E1",
                          background: "#fff",
                          fontSize: "14px",
                          cursor: "pointer",
                        }}
                      >
                        <option value="">Select Developer</option>

                        {developers.map((dev) => (
                          <option key={dev.id} value={dev.id}>
                            {dev.username}
                          </option>
                        ))}
                      </select>
                    </td>

                    <td>
                      <button
                        onClick={() => assignDeveloper(ticket.id)}
                        style={{
                          background: "#2563EB",
                          color: "white",
                          border: "none",
                          padding: "10px 20px",
                          borderRadius: "8px",
                          cursor: "pointer",
                          fontWeight: "600",
                          fontSize: "14px",
                          boxShadow: "0 4px 10px rgba(37,99,235,0.3)",
                          transition: "0.3s",
                        }}
                      >
                        Assign Developer
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

export default DeveloperAssignment;