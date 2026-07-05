import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>CRM System</h2>

      <Link to="/">Dashboard</Link>
      <Link to="/request-form">New Request</Link>
      <Link to="/request-list">Request List</Link>
      <Link to="/approval">Approval</Link>
      <Link to="/assign-developer">Assign Developer</Link>
    </div>
  );
}

export default Sidebar;