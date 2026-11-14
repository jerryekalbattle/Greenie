import { useState } from "react";

function App() {
  const [apiKey, setApiKey] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin() {
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/verify-key",
        {
          method: "GET",
          headers: {
            "X-API-Key": apiKey
          }
        }
      );

      if (!response.ok) {
        setError("Incorrect API passkey. Please try again.");
        return;
      }

      setIsAuthenticated(true);

    } catch (error) {
      setError("Unable to connect to the API. Is your server running?");
    }
  }

  if (isAuthenticated) {
    return (
      <div>
        <h1>Welcome to Cardiovascular Surgery Guide!</h1>
        <p>You have successfully accessed the website.</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Cardiovascular Surgery Guide</h1>
      <p>Enter your API passkey to continue.</p>

      <input
        type="password"
        placeholder="Enter API passkey"
        value={apiKey}
        onChange={(event) => setApiKey(event.target.value)}
      />

      <button onClick={handleLogin}>
        Continue
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
