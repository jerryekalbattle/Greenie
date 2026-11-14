
import os
import uuid
import cohere

from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "change-this-secret"
)

co = cohere.ClientV2(
    api_key=os.environ["COHERE_API_KEY"]
)

conversations = {}


@app.route("/")
def home():
    if "chat_id" not in session:
        session["chat_id"] = str(uuid.uuid4())

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    chat_id = session.get("chat_id")

    if not chat_id:
        return jsonify({"reply": "Please refresh the page."}), 400

    if chat_id not in conversations:
        conversations[chat_id] = []

    messages = conversations[chat_id]

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = co.chat(
            model="command-a-03-2025",
            messages=messages[-20:]
        )

        bot_reply = response.message.content[0].text

        messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({"reply": bot_reply})

    except Exception:
        messages.pop()
        app.logger.exception("Cohere API error")

        return jsonify({
            "reply": "Sorry! Something went wrong."
        }), 500


if __name__ == "__main__":
    print("GREENIE IS STARTING!")
    app.run(host="127.0.0.1", port=5000, debug=True)
