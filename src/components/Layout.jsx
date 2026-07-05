import { Link, useNavigate } from "react-router-dom";

function Layout({ children }) {
  const navigate = useNavigate();

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <div
        style={{
          width: "250px",
          background: "#1E293B",
          color: "white",
          padding: "20px",
        }}
      >
        <h2>CRM System</h2>

        <div
          style={{
            marginTop: "30px",
            display: "flex",
            flexDirection: "column",
            gap: "15px",
          }}
        >
          <Link to="/dashboard" style={linkStyle}>
            Dashboard
          </Link>

          <Link to="/request-form" style={linkStyle}>
            New Request
          </Link>

          <Link to="/request-list" style={linkStyle}>
            Request List
          </Link>

          <Link to="/approval" style={linkStyle}>
            Approval
          </Link>

          <Link to="/developer-assignment" style={linkStyle}>
            Developer Assignment
          </Link>
          <Link to="/developer-dashboard" style={linkStyle}>
  Developer Dashboard
</Link>

          <button
            onClick={() => navigate("/")}
            style={{
              marginTop: "20px",
              padding: "10px",
              background: "#EF4444",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
            }}
          >
            Logout
          </button>
        </div>
      </div>

      <div style={{ flex: 1, background: "#F8FAFC" }}>
        <div
          style={{
            background: "white",
            padding: "20px",
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <h2>Change Management Request System</h2>

            <div
              style={{
                background: "#E2E8F0",
                padding: "8px 15px",
                borderRadius: "20px",
              }}
            >
              Welcome, Admin
            </div>
          </div>
        </div>

        <div style={{ padding: "20px" }}>
          {children}

          <div
            style={{
              textAlign: "center",
              marginTop: "40px",
              color: "#64748B",
            }}
          >
            © 2026 Change Management Request System
          </div>
        </div>
      </div>
    </div>
  );
}

const linkStyle = {
  color: "white",
  textDecoration: "none",
  padding: "10px",
  background: "#334155",
  borderRadius: "8px",
};

export default Layout;