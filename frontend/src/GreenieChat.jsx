
import { useState } from "react";

function GreenieChat() {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            text: "Hi! I'm Greenie 🌿 How can I help you learn about cardiovascular surgery today?"
        }
    ]);
    const [loading, setLoading] = useState(false);

    async function sendMessage(event) {
        event.preventDefault();

        const userMessage = message.trim();

        if (!userMessage || loading) return;

        setMessages((previous) => [
            ...previous,
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
                body: JSON.stringify({
                    message: userMessage
                })
            });

            if (!response.ok) {
                throw new Error("Greenie could not respond right now.");
            }

            const data = await response.json();

            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    text: data.reply || "I'm sorry, I couldn't find an answer."
                }
            ]);
        } catch (error) {
            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    text: "I'm having trouble connecting right now. Please check that the Greenie server is running and try again."
                }
            ]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="greenie-chat">
            {isOpen && (
                <section className="chat-window">
                    <header className="chat-header">
                        <div className="chat-header-info">
                            <div className="chat-avatar">🌿</div>
                            <div>
                                <h3>Greenie</h3>
                                <span>Here to help you learn</span>
                            </div>
                        </div>

                        <button
                            className="chat-close"
                            onClick={() => setIsOpen(false)}
                            aria-label="Close chat"
                        >
                            ×
                        </button>
                    </header>

                    <div className="chat-welcome">
                        <span>💚</span>
                        <p>Ask me anything about cardiovascular surgery.</p>
                    </div>

                    <div className="chat-messages" aria-live="polite">
                        {messages.map((item, index) => (
                            <div
                                key={index}
                                className={`message-row ${item.role === "user" ? "user-row" : "assistant-row"}`}
                            >
                                {item.role === "assistant" && (
                                    <div className="message-avatar">🌿</div>
                                )}

                                <div
                                    className={`message-bubble ${item.role === "user" ? "user-bubble" : "assistant-bubble"}`}
                                >
                                    {item.text}
                                </div>
                            </div>
                        ))}

                        {loading && (
                            <div className="message-row assistant-row">
                                <div className="message-avatar">🌿</div>
                                <div className="message-bubble assistant-bubble typing">
                                    Greenie is thinking...
                                </div>
                            </div>
                        )}
                    </div>

                    <form className="chat-input-area" onSubmit={sendMessage}>
                        <input
                            type="text"
                            value={message}
                            onChange={(event) => setMessage(event.target.value)}
                            placeholder="Ask Greenie something..."
                            aria-label="Message Greenie"
                            disabled={loading}
                        />

                        <button
                            type="submit"
                            disabled={!message.trim() || loading}
                            aria-label="Send message"
                        >
                            ↑
                        </button>
                    </form>

                    <p className="chat-disclaimer">
                        Greenie provides educational information, not personal medical advice.
                    </p>
                </section>
            )}

            <button
                className={`chat-toggle ${isOpen ? "chat-toggle-open" : ""}`}
                onClick={() => setIsOpen(!isOpen)}
                aria-label={isOpen ? "Close Greenie chat" : "Open Greenie chat"}
            >
                {isOpen ? "×" : "💬"}
                {!isOpen && <span>Chat with Greenie</span>}
            </button>
        </div>
    );
}

export default GreenieChat;
