import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="overlay">
        <div className="landing-content">
          <h1 className="title">
            Change Request
            <span> Management System</span>
          </h1>

          <p className="subtitle">
            Streamline change requests, approvals, tracking, and implementation
            through one secure platform designed for teams and organizations.
          </p>

          <div className="button-group">
            <button
              className="start-btn"
              onClick={() => navigate("/login")}
            >
              Get Started →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;