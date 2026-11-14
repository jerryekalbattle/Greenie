
import { useState } from "react";

const API_URL = "https://greenie-medical-api.onrender.com";

function SurgeryDirectory() {
    const [apiKey, setApiKey] = useState("");
    const [authenticated, setAuthenticated] = useState(false);
    const [surgeries, setSurgeries] = useState([]);
    const [selectedSurgery, setSelectedSurgery] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function loadSurgeries(key) {
        const response = await fetch(`${API_URL}/surgeries`, {
            headers: {
                "X-API-Key": key
            }
        });

        if (!response.ok) {
            throw new Error("Could not load the surgery library.");
        }

        const data = await response.json();

        const surgeryList = Array.isArray(data)
            ? data
            : Array.isArray(data.surgeries)
                ? data.surgeries
                : Object.values(data);

        setSurgeries(surgeryList);
    }

    async function verifyKey(event) {
        event.preventDefault();
        setError("");
        setLoading(true);

        try {
            const response = await fetch(`${API_URL}/verify-key`, {
                headers: {
                    "X-API-Key": apiKey
                }
            });

            if (!response.ok) {
                throw new Error("That access key is not valid. Please try again.");
            }

            await loadSurgeries(apiKey);
            setAuthenticated(true);
        } catch (err) {
            setError(err.message || "Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    async function loadSurgery(surgeryId) {
        setError("");
        setLoading(true);

        try {
            const response = await fetch(
                `${API_URL}/surgeries/${encodeURIComponent(surgeryId)}`,
                {
                    headers: {
                        "X-API-Key": apiKey
                    }
                }
            );

            if (!response.ok) {
                throw new Error("Could not load the surgery details.");
            }

            const data = await response.json();
            setSelectedSurgery(data);
        } catch (err) {
            setError(err.message || "Unable to load this surgery.");
        } finally {
            setLoading(false);
        }
    }

    function logout() {
        setAuthenticated(false);
        setApiKey("");
        setSurgeries([]);
        setSelectedSurgery(null);
        setSearchTerm("");
        setError("");
    }

    const filteredSurgeries = surgeries.filter((surgery) => {
        const search = searchTerm.toLowerCase();

        return (
            surgery.name?.toLowerCase().includes(search) ||
            surgery.category?.toLowerCase().includes(search) ||
            surgery.description?.toLowerCase().includes(search)
        );
    });

    if (!authenticated) {
        return (
            <main className="login-page">
                <section className="login-container">
                    <div className="login-icon">🌿</div>

                    <p className="eyebrow">
                        YOUR CARDIOVASCULAR LEARNING GUIDE
                    </p>

                    <h1>Welcome to Greenie</h1>

                    <p className="login-description">
                        Your friendly guide to learning about cardiovascular
                        surgeries, treatments, and recovery.
                    </p>

                    <form onSubmit={verifyKey} className="login-form">
                        <label htmlFor="api-key">Access key</label>

                        <input
                            id="api-key"
                            type="password"
                            value={apiKey}
                            onChange={(event) => setApiKey(event.target.value)}
                            placeholder="Enter your access key"
                            required
                        />

                        <button type="submit" disabled={loading}>
                            {loading ? "Checking..." : "Enter Greenie"}
                        </button>
                    </form>

                    {error && (
                        <p className="error-message" role="alert">
                            {error}
                        </p>
                    )}

                    <p className="login-footer">
                        A welcoming space to learn, explore, and understand.
                    </p>
                </section>
            </main>
        );
    }

    return (
        <div className="app-container">
            <aside className="sidebar">
                <div className="sidebar-brand">
                    <span className="brand-icon">🌿</span>
                    <span>Greenie</span>
                </div>

                <p className="sidebar-label">MENU</p>

                <button
                    className={`nav-item ${!selectedSurgery ? "active" : ""}`}
                    onClick={() => setSelectedSurgery(null)}
                >
                    <span>⌂</span> Surgery Library
                </button>

                <div className="sidebar-bottom">
                    <div className="sidebar-note">
                        <span>💚</span>
                        <p>Knowledge makes every step easier.</p>
                    </div>

                    <button className="logout-button" onClick={logout}>
                        ↪ Log out
                    </button>
                </div>
            </aside>

            <main className="main-content">
                <header className="topbar">
                    <div>
                        <p className="eyebrow">YOUR HEALTH LEARNING SPACE</p>
                        <h2>Greenie Dashboard</h2>
                    </div>

                    <div className="profile-icon">🌱</div>
                </header>

                {error && (
                    <p className="error-message" role="alert">
                        {error}
                    </p>
                )}

                {!selectedSurgery ? (
                    <>
                        <section className="welcome-banner">
                            <div>
                                <p className="eyebrow">WELCOME TO GREENIE</p>
                                <h1>Let's learn something new.</h1>
                                <p>
                                    Explore cardiovascular surgeries and
                                    understand the journey, one step at a time.
                                </p>
                            </div>

                            <div className="welcome-illustration">🌿</div>
                        </section>

                        <section className="library-heading">
                            <div>
                                <p className="eyebrow">EXPLORE AND DISCOVER</p>
                                <h2>Surgery Library</h2>
                                <p className="section-description">
                                    Browse the available surgery guides below.
                                </p>
                            </div>

                            <span className="count-pill">
                                {surgeries.length} guides
                            </span>
                        </section>

                        <div className="search-container">
                            <span>⌕</span>
                            <input
                                type="search"
                                value={searchTerm}
                                onChange={(event) =>
                                    setSearchTerm(event.target.value)
                                }
                                placeholder="Search surgeries or categories..."
                                aria-label="Search surgeries"
                            />
                        </div>

                        {loading ? (
                            <p className="empty-message">Loading...</p>
                        ) : filteredSurgeries.length > 0 ? (
                            <section className="surgery-grid">
                                {filteredSurgeries.map((surgery, index) => {
                                    const surgeryId =
                                        surgery.id ||
                                        surgery.surgery_id ||
                                        surgery.slug;

                                    return (
                                        <article
                                            className="surgery-card"
                                            key={surgeryId || surgery.name || index}
                                        >
                                            <div className="surgery-card-icon">
                                                ♥
                                            </div>

                                            <p className="card-category">
                                                {surgery.category || "CARDIOVASCULAR"}
                                            </p>

                                            <h3>
                                                {surgery.name || "Surgery Guide"}
                                            </h3>

                                            <p className="card-description">
                                                {surgery.description ||
                                                    "Explore this surgery guide and learn more."}
                                            </p>

                                            <button
                                                className="view-button"
                                                onClick={() => loadSurgery(surgeryId)}
                                                disabled={!surgeryId}
                                            >
                                                Explore guide <span>→</span>
                                            </button>
                                        </article>
                                    );
                                })}
                            </section>
                        ) : (
                            <div className="empty-message">
                                <span>🔎</span>
                                <h3>No surgeries found</h3>
                                <p>Try another search term.</p>
                            </div>
                        )}
                    </>
                ) : (
                    <section className="details-page">
                        <button
                            className="back-button"
                            onClick={() => setSelectedSurgery(null)}
                        >
                            ← Back to Surgery Library
                        </button>

                        <div className="details-heading">
                            <div className="surgery-card-icon">♥</div>

                            <p className="eyebrow">
                                {selectedSurgery.category || "SURGERY GUIDE"}
                            </p>

                            <h1>{selectedSurgery.name}</h1>

                            <p>{selectedSurgery.description}</p>
                        </div>

                        <nav
                            className="details-navigation"
                            aria-label="Surgery information"
                        >
                            <a href="#about-surgery">📋 Overview</a>
                            <a href="#medication">💊 Medication</a>
                            <a href="#recovery">🌱 Recovery</a>
                            <a href="#risks">⚠️ Risks</a>
                        </nav>

                        {selectedSurgery.surgery_info && (
                            <section
                                className="detail-card"
                                id="about-surgery"
                            >
                                <h2>📋 About the surgery</h2>

                                {Object.entries(
                                    selectedSurgery.surgery_info
                                ).map(([key, value]) => (
                                    <div className="detail-section" key={key}>
                                        <h3>
                                            {key.replaceAll("_", " ")}
                                        </h3>
                                        <p>{String(value)}</p>
                                    </div>
                                ))}
                            </section>
                        )}

                        {selectedSurgery.medication && (
                            <section
                                className="detail-card"
                                id="medication"
                            >
                                <h2>💊 Medication information</h2>

                                <p>
                                    {selectedSurgery.medication.information ||
                                        "Please refer to the care team's medication instructions."}
                                </p>
                            </section>
                        )}

                        {selectedSurgery.recovery && (
                            <section
                                className="detail-card recovery-card"
                                id="recovery"
                            >
                                <h2>🌱 Recovery and follow-up</h2>

                                {Object.entries(
                                    selectedSurgery.recovery
                                ).map(([key, value]) => (
                                    <div className="detail-section" key={key}>
                                        <h3>
                                            {key.replaceAll("_", " ")}
                                        </h3>
                                        <p>{String(value)}</p>
                                    </div>
                                ))}
                            </section>
                        )}

                        {Array.isArray(selectedSurgery.risks) && (
                            <section
                                className="detail-card risks-card"
                                id="risks"
                            >
                                <h2>⚠️ Possible risks</h2>

                                <ul className="risk-list">
                                    {selectedSurgery.risks.map((risk, index) => (
                                        <li key={index}>{risk}</li>
                                    ))}
                                </ul>
                            </section>
                        )}

                        <p className="medical-notice">
                            Greenie provides educational information only.
                            Always follow the advice of your qualified
                            healthcare team for personal medical decisions.
                        </p>
                    </section>
                )}
            </main>
        </div>
    );
}

export default SurgeryDirectory;
