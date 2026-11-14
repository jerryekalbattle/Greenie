
import { useState } from "react";

function GreenieChat() {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            text: "Hi! I'm Greenie. How can I help you learn about cardiovascular surgery?"
        }
    ]);
    const [loading, setLoading] = useState(false);

    async function sendMessage() {
        if (!message.trim() || loading) return;

        const userMessage = message.trim();

        setMessages(prev => [
            ...prev,
            { role: "user", text: userMessage }
        ]);

        setMessage("");
        setLoading(true);

        try {
            const response = await fetch("/chat", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.reply || "Chat request failed.");
            }

            setMessages(prev => [
                ...prev,
                { role: "assistant", text: data.reply }
            ]);

        } catch (error) {
            setMessages(prev => [
                ...prev,
                {
                    role: "assistant",
                    text: "Sorry! I couldn't connect to Greenie. Please check that the chatbot server is running."
                }
            ]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div style={{
            position: "fixed",
            bottom: "25px",
            right: "25px",
            zIndex: 1000,
            fontFamily: "Arial, sans-serif"
        }}>
            {isOpen && (
                <div style={{
                    width: "340px",
                    height: "430px",
                    background: "white",
                    border: "1px solid #ddd",
                    borderRadius: "15px",
                    boxShadow: "0 4px 20px rgba(0,0,0,0.2)",
                    display: "flex",
                    flexDirection: "column",
                    overflow: "hidden",
                    marginBottom: "12px"
                }}>
                    <div style={{
                        background: "#16865a",
                        color: "white",
                        padding: "16px",
                        fontWeight: "bold"
                    }}>
                        💚 Greenie Assistant
                    </div>

                    <div style={{
                        flex: 1,
                        overflowY: "auto",
                        padding: "12px"
                    }}>
                        {messages.map((msg, index) => (
                            <div key={index} style={{
                                background: msg.role === "user"
                                    ? "#dcf8e9"
                                    : "#f1f1f1",
                                padding: "10px",
                                borderRadius: "10px",
                                marginBottom: "10px",
                                marginLeft: msg.role === "user" ? "35px" : "0",
                                marginRight: msg.role === "assistant" ? "35px" : "0",
                                whiteSpace: "pre-wrap"
                            }}>
                                {msg.text}
                            </div>
                        ))}
                        {loading && <p>Greenie is thinking...</p>}
                    </div>

                    <div style={{
                        display: "flex",
                        padding: "10px",
                        borderTop: "1px solid #ddd",
                        gap: "6px"
                    }}>
                        <input
                            value={message}
                            onChange={e => setMessage(e.target.value)}
                            onKeyDown={e => {
                                if (e.key === "Enter") sendMessage();
                            }}
                            placeholder="Ask Greenie..."
                            style={{
                                flex: 1,
                                minWidth: 0,
                                padding: "10px",
                                borderRadius: "8px",
                                border: "1px solid #ccc"
                            }}
                        />

                        <button onClick={sendMessage} disabled={loading}>
                            Send
                        </button>
                    </div>
                </div>
            )}


<button
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    display: "block",
                    position: "relative",
                    backgroundColor: "#16865a",
                    color: "white",
                    border: "none",
                    borderRadius: "50%",
                    width: "65px",
                    height: "65px",
                    fontSize: "16px",
                    fontWeight: "bold",
                    cursor: "pointer",
                    boxShadow: "0 3px 12px rgba(0,0,0,0.3)"
                }}
            >
                CHAT
            </button>

        </div>
    );
}

export default GreenieChat;
