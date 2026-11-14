
import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function SurgeryDirectory() {

    const [apiKey, setApiKey] = useState("");
    const [authenticated, setAuthenticated] = useState(false);

    const [surgeries, setSurgeries] = useState([]);
    const [selectedSurgery, setSelectedSurgery] = useState(null);

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    // Verify the API key before allowing access
    async function verifyKey() {

        setError("");
        setLoading(true);

        try {

            const response = await fetch(`${API_URL}/verify-key`, {
                method: "GET",
                headers: {
                    "X-API-Key": apiKey
                }
            });

            if (!response.ok) {
                throw new Error("Unable to retrieve surgeries.");
            }

            setAuthenticated(true);

            await loadSurgeries();

        } catch (err) {

            setError(err.message);
            setAuthenticated(false);

        } finally {

            setLoading(false);

        }
    }


    // Retrieve all surgeries
    async function loadSurgeries() {

        try {

            const response = await fetch(`${API_URL}/surgeries`, {
                headers: {
                    "X-API-Key": apiKey
                }
            });

            if (!response.ok) {
                throw new Error("Unable to retrieve surgeries.");
            }

            const data = await response.json();

            setSurgeries(data);

        } catch (err) {

            setError(err.message);
            setAuthenticated(false);

        }
    }


    // Retrieve individual surgery information
    async function loadSurgery(surgeryId) {

        setError("");
        setSelectedSurgery(null);

        try {

            const response = await fetch(
                `${API_URL}/surgeries/${surgeryId}`,
                {
                    headers: {
                        "X-API-Key": apiKey
                    }
                }
            );

            if (!response.ok) {
                const errorData = await response.text();

                throw new Error(
                    `Surgery request failed (${response.status}): ${errorData}`
                );

            }

            const data = await response.json();

            setSelectedSurgery(data);

        } catch (err) {

            setError(err.message);

        }
    }

    
    // Login screen
    if (!authenticated) {
        return (
            <div className="app-container">
                <div className="login-container">

                    <div className="login-icon">🌿</div>

                    <h1>Greenie</h1>

                    <p className="subtitle">
                        Your cardiovascular care companion. We care about your health so you can recover with confidence and peace of mind.
                    </p>

                    <h2>Welcome!</h2>

                    <p>
                        Enter your access key to explore cardiovascular
                        surgeries, medication information, and recovery resources.
                    </p>

                    <input
                        type="password"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && apiKey.trim() && !loading) {
                                verifyKey();
                            }
                        }}
                        placeholder="Enter your API passkey"
                    />

                    <button
                        onClick={verifyKey}
                        disabled={loading || !apiKey.trim()}
                    >
                        {loading ? "Verifying..." : "Access Greenie"}
                    </button>

                    {error && (
                        <p className="error-message">{error}</p>
                    )}

                    <p className="login-footer">
                        🌱 Here to help you navigate your care journey.
                    </p>

                </div>
            </div>
        );
    }



    // Main directory after successful login
    
    return (
        <div className="app-container">

            <header className="header">
                <div>
<<<<<<< HEAD

                    <h2>{selectedSurgery.name}</h2>


                    <p>{selectedSurgery.description}</p>

                    <h3>Surgery Information</h3>

                    <pre>
                        {JSON.stringify(
                            selectedSurgery.surgery_info,
                            null,
                            2
                        )}
                    </pre>

                    <h3>Medication Information</h3>

                    <pre>
                        {JSON.stringify(
                            selectedSurgery.medication,
                            null,
                            2
                        )}
                    </pre>

                    <h3>Recovery</h3>

                    <pre>
                        {JSON.stringify(
                            selectedSurgery.recovery,
                            null,
                            2
                        )}
                    </pre>

                    <h3>Risks</h3>

                    <ul>
                        {selectedSurgery.risks.map((risk, index) => (
                            <li key={index}>{risk}</li>
                        ))}
                    </ul>

=======
                    <div className="logo">
                        Greenie 🌿
                    </div>
                    <div className="subtitle">
                        Your cardiovascular care companion
                    </div>
>>>>>>> 9c50f2a53a62f1d3bb6cb4bb507352aaf14808a5
                </div>

                <button
                    className="logout-button"
                    onClick={() => {
                        setAuthenticated(false);
                        setApiKey("");
                        setSurgeries([]);
                        setSelectedSurgery(null);
                    }}
                >
                    Log Out
                </button>
            </header>

            <div className="card">
                <h1>Welcome to Greenie!</h1>
                <p>
                    Explore cardiovascular surgeries, recovery
                    information, and medication resources.
                </p>
            </div>

            <h2>🌱 Available Surgeries</h2>

            <div className="surgery-grid">
                {surgeries.map((surgery) => (
                    <div className="card" key={surgery.id}>
                        <h3>{surgery.name}</h3>
                        <p>{surgery.category}</p>
                        <p>{surgery.description}</p>

                        <button onClick={() => loadSurgery(surgery.id)}>
                            View Details
                        </button>
                    </div>
                ))}
            </div>

            {selectedSurgery && (
                <div className="card">
                    <h2>{selectedSurgery.name}</h2>
                    <p>{selectedSurgery.description}</p>

                    <div className="detail-section">
                        <h3>🫀 Surgery Information</h3>
                        {Object.entries(selectedSurgery.surgery_info || {}).map(
                            ([key, value]) => (
                                <p key={key}>
                                    <strong>{key}:</strong> {value}
                                </p>
                            )
                        )}
                    </div>

                    <div className="detail-section">
                        <h3>💊 Medication Information</h3>
                        {selectedSurgery.medication_info?.map(
                            (medication, index) => (
                                <p key={index}>
                                    {typeof medication === "string"
                                        ? medication
                                        : medication.name}
                                </p>
                            )
                        )}
                    </div>

                    <div className="detail-section">
                        <h3>🌿 Recovery</h3>
                        {Object.entries(selectedSurgery.recovery || {}).map(
                            ([key, value]) => (
                                <p key={key}>
                                    <strong>{key}:</strong> {value}
                                </p>
                            )
                        )}
                    </div>

                    <div className="detail-section">
                        <h3>⚠️ Potential Risks</h3>
                        <ul>
                            {selectedSurgery.risks?.map((risk, index) => (
                                <li key={index}>{risk}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}

            {error && <p className="error-message">{error}</p>}

        </div>
    );

}

export default SurgeryDirectory;
