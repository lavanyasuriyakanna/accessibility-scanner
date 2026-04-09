import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    if (!url) {
      alert("Please enter a URL");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/scanner/scan/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div>
      {/* 🔷 NAVBAR */}
      <nav style={styles.navbar}>
        <h2 style={{ margin: 0 }}>🚀 WebScanner</h2>
        <div>
          <span style={styles.navItem}>Home</span>
          <span style={styles.navItem}>About</span>
          <span style={styles.navItem}>Contact</span>
        </div>
      </nav>

      {/* 🔷 MAIN CONTENT */}
      <div style={styles.container}>
        <h1>🔍 Website Accessibility Scanner</h1>

        <div style={styles.inputBox}>
          <input
            type="text"
            placeholder="Enter website URL (https://example.com)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={styles.input}
          />

          <button onClick={handleScan} style={styles.button}>
            Scan
          </button>
        </div>

        {loading && <p>⏳ Scanning...</p>}

        {result && (
          <div style={styles.resultBox}>
            <h2>✅ Score: {result.score}</h2>
            <h3>📄 Title: {result.title}</h3>

            <h3>⚠️ Issues:</h3>
            <ul>
              {result.issues.map((issue, index) => (
                <li key={index}>
                  <b>{issue.type}</b> - {issue.message}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

/* 🔷 STYLES */
const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 30px",
    backgroundColor: "#1e293b",
    color: "white",
  },
  navItem: {
    marginLeft: "20px",
    cursor: "pointer",
  },
  container: {
    padding: "40px",
    textAlign: "center",
    fontFamily: "Arial",
  },
  inputBox: {
    marginTop: "20px",
  },
  input: {
    padding: "10px",
    width: "300px",
    marginRight: "10px",
  },
  button: {
    padding: "10px 20px",
    backgroundColor: "#2563eb",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
  resultBox: {
    marginTop: "30px",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    display: "inline-block",
    textAlign: "left",
  },
};

export default App;