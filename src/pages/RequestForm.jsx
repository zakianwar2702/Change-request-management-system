import { useState } from "react";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function RequestForm() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    requester: "",
    project: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

 const handleSubmit = (e) => {
  e.preventDefault();

  fetch("/api/tickets/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      employee_name: formData.requester,
      project_name: formData.project,
      description: formData.description,
    }),
  })
    .then(async (res) => {
      const data = await res.json();

      if (!res.ok) {
        console.log(data);
        throw new Error("Failed");
      }

      navigate("/request-list");
    })
    .catch((err) => {
      console.error(err);
      alert("Error creating request");
    });
};

  return (
    <Layout>
      <div className="dashboard">

        <div
          style={{
            maxWidth: "850px",
            margin: "0 auto",
          }}
        >

          {/* Heading aligned with form */}
          <div
            className="dashboard-header"
            style={{
              marginBottom: "20px",
            }}
          >
            <div>
              <h2>Create New Change Request</h2>

              <p>
                Complete the form below to submit a new change request.
              </p>
            </div>
          </div>


          {/* Form Card */}
          <div
            className="card"
            style={{
              padding: "30px",
              borderRadius: "12px",
            }}
          >

            <form onSubmit={handleSubmit}>


              {/* Title */}
              <div style={{ marginBottom: "20px" }}>

                <label style={labelStyle}>
                  Request Title
                </label>

                <input
                  type="text"
                  name="title"
                  placeholder="Enter request title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  style={inputStyle}
                />

              </div>



              {/* Project + Requester */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "20px",
                  marginBottom: "20px",
                }}
              >

                <div>

                  <label style={labelStyle}>
                    Project
                  </label>

                  <select
                    name="project"
                    value={formData.project}
                    onChange={handleChange}
                    required
                    style={inputStyle}
                  >

                    <option value="">
                      Select Project
                    </option>

                    <option value="CRM System">
                      CRM System
                    </option>

                    <option value="HR Portal">
                      HR Portal
                    </option>

                    <option value="Finance App">
                      Finance App
                    </option>

                    <option value="Website Upgrade">
                      Website Upgrade
                    </option>

                  </select>

                </div>



                <div>

                  <label style={labelStyle}>
                    Requester
                  </label>

                  <input
                    type="text"
                    name="requester"
                    placeholder="Enter requester name"
                    value={formData.requester}
                    onChange={handleChange}
                    required
                    style={inputStyle}
                  />

                </div>


              </div>




              {/* Description */}
              <div style={{ marginBottom: "30px" }}>

                <label style={labelStyle}>
                  Description
                </label>


                <textarea
                  rows="6"
                  name="description"
                  placeholder="Describe the requested change..."
                  value={formData.description}
                  onChange={handleChange}
                  required
                  style={{
                    ...inputStyle,
                    resize: "vertical",
                  }}
                />


              </div>



              {/* Buttons */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "flex-end",
                  gap: "15px",
                }}
              >

                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  style={{
                    background: "#e5e7eb",
                    border: "none",
                    padding: "12px 25px",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontWeight: "600",
                  }}
                >
                  Cancel
                </button>



                <button
                  type="submit"
                  style={{
                    background: "#2563eb",
                    color: "white",
                    border: "none",
                    padding: "12px 28px",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontWeight: "600",
                  }}
                >
                  Submit Request
                </button>


              </div>


            </form>


          </div>


        </div>


      </div>
    </Layout>
  );
}



const labelStyle = {
  display: "block",
  fontWeight: "600",
  marginBottom: "8px",
  color: "#374151",
};



const inputStyle = {
  width: "100%",
  padding: "12px",
  border: "1px solid #d1d5db",
  borderRadius: "8px",
  fontSize: "15px",
  outline: "none",
  boxSizing: "border-box",
};



export default RequestForm;