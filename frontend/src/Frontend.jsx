
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
            <div>

                <h1>Cardiovascular Surgery Directory</h1>

                <h2>API Authentication</h2>

                <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="Enter API passkey"
                />

                <button
                    onClick={verifyKey}
                    disabled={loading || !apiKey.trim()}
                >
                    {loading ? "Verifying..." : "Access Directory"}
                </button>

                {error && <p>{error}</p>}

            </div>
        );
    }


    // Main directory after successful login
    return (

        <div>

            <h1>Cardiovascular Surgery Directory</h1>

            <button onClick={() => {
                setAuthenticated(false);
                setApiKey("");
                setSurgeries([]);
                setSelectedSurgery(null);
            }}>
                Log Out
            </button>

            <h2>Available Surgeries</h2>

            {surgeries.map((surgery) => (

                <button
                    key={surgery.id}
                    onClick={() => loadSurgery(surgery.id)}
                >
                    {surgery.name}
                </button>

            ))}


            {selectedSurgery && (

                <div>

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

                </div>

            )}

            {error && <p>{error}</p>}

        </div>

    );
}

export default SurgeryDirectory;
