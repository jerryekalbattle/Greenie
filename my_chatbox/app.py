
import os
import uuid
import cohere
import requests

from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
CORS(
    app,
    origins=os.environ.get(
        "FRONTEND_URL",
        "http://localhost:5173"
    ),
    supports_credentials=True
)

app.secret_key = os.environ["FLASK_SECRET_KEY"]
cookie_secure = (
    os.environ.get("SESSION_COOKIE_SECURE", "true").lower() == "true"
)

app.config.update(
    SESSION_COOKIE_SAMESITE="None" if cookie_secure else "Lax",
    SESSION_COOKIE_SECURE=cookie_secure,
    SESSION_COOKIE_HTTPONLY=True
)

co = cohere.ClientV2(
    api_key=os.environ["COHERE_API_KEY"]
)

MEDICAL_API_URL = os.environ.get(
    "MEDICAL_API_URL",
    "http://127.0.0.1:8001"
)
MEDICAL_API_KEY = os.environ["MEDICAL_API_KEY"]

conversations = {}
RESPONDER_USERNAME = os.environ.get("RESPONDER_USERNAME")
RESPONDER_PASSWORD = os.environ.get("RESPONDER_PASSWORD")


def get_surgery_information():
    try:
        response = requests.get(
            f"{MEDICAL_API_URL}/surgeries",
            headers={"X-API-Key": MEDICAL_API_KEY},
            timeout=10
        )
        response.raise_for_status()

        surgery_list = response.json()
        detailed_surgeries = []

        for surgery in surgery_list:
            surgery_response = requests.get(
                f"{MEDICAL_API_URL}/surgeries/{surgery['id']}",
                headers={"X-API-Key": MEDICAL_API_KEY},
                timeout=10
            )
            surgery_response.raise_for_status()
            detailed_surgeries.append(surgery_response.json())

        return detailed_surgeries

    except requests.RequestException:
        app.logger.exception("Medical API connection failed")
        return []
@app.route("/responder", methods=["GET"])
def responder_page():
    return render_template("responder.html")
@app.route("/responder-login", methods=["POST"])
def responder_login():
    data = request.get_json() or {}

    username = data.get("username", "")
    password = data.get("password", "")

    if (
        username == RESPONDER_USERNAME
        and password == RESPONDER_PASSWORD
    ):
        session["is_responder"] = True
        return jsonify({"success": True})

    return jsonify({
        "success": False,
        "message": "Incorrect username or password."
    }), 401
@app.route("/")
def home():
    if "chat_id" not in session:
        session["chat_id"] = str(uuid.uuid4())

    return render_template("index.html")

@app.route("/responder/messages", methods=["GET"])
def responder_messages():
    if not session.get("is_responder"):
        return jsonify({"error": "Unauthorized"}), 401

    result = []

    for chat_id, messages in conversations.items():
        result.append({
            "chat_id": chat_id,
            "messages": messages
        })

    return jsonify({"conversations": result})
@app.route("/responder/reply", methods=["POST"])
def responder_reply():
    if not session.get("is_responder"):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    chat_id = data.get("chat_id")
    reply = data.get("reply", "").strip()

    if not chat_id or not reply:
        return jsonify({"error": "Missing chat ID or reply"}), 400

    if chat_id not in conversations:
        return jsonify({"error": "Conversation not found"}), 404

    conversations[chat_id].append({
        "role": "assistant",
        "content": reply,
        "responder": True
    })

    return jsonify({"success": True})

@app.route("/chat/responder-replies", methods=["GET"])
def get_responder_replies():
    chat_id = session.get("chat_id")

    if not chat_id:
        chat_id = str(uuid.uuid4())
        session["chat_id"] = chat_id

    messages = conversations.get(chat_id, [])

    replies = [
        message["content"]
        for message in messages
        if message.get("responder") is True
    ]

    return jsonify({"replies": replies})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    chat_id = session.get("chat_id")

    if not chat_id:
        chat_id = str(uuid.uuid4())
        session["chat_id"] = chat_id

    if chat_id not in conversations:
        conversations[chat_id] = []

    messages = conversations[chat_id]

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        medical_info = get_surgery_information()

        system_message = {
            "role": "system",
            "content": (
                "You are Greenie, a friendly educational assistant. "
                "Use the following cardiovascular surgery API information "
                "when answering questions about those surgeries:\n"
                + str(medical_info)
                + "\nOnly make claims supported by the supplied information. "
                "If the information does not answer a question, say so. "
                "Do not diagnose, prescribe medication, or replace professional "
                "medical advice."
            )
        }

        response = co.chat(
            model="command-a-03-2025",
            messages=[system_message] + messages[-20:]
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
