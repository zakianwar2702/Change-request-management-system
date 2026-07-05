import React, { useEffect, useState } from "react";

function AssignDeveloper() {
  const [developer, setDeveloper] = useState("");
  const [developers, setDevelopers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/tickets/users/")
      .then((response) => response.json())
      .then((data) => {
        setDevelopers(data);
      })
      .catch((error) => {
        console.error("Error loading developers:", error);
      });
  }, []);

  const assignDeveloper = () => {
    if (!developer) {
      alert("Please select a developer");
      return;
    }

    alert(`Developer ${developer} assigned successfully!`);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>Assign Developer</h2>

      <label>Select Developer</label>
      <br /><br />

      <select
        value={developer}
        onChange={(e) => setDeveloper(e.target.value)}
      >
        <option value="">Select</option>

        {developers.map((dev) => (
          <option key={dev.id} value={dev.username}>
            {dev.username}
          </option>
        ))}

      </select>

      <br /><br />

      <button onClick={assignDeveloper}>
        Assign
      </button>
    </div>
  );
}

export default AssignDeveloper;