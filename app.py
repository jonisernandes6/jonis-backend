from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError("Falta GROQ_API_KEY")

client = Groq(api_key=API_KEY)

@app.route("/")
def home():
    return "JonisAI Backend funcionando"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Falta el mensaje"}), 400

    message = data["message"]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Eres JonisAI, un asistente experto en programación. Explica el código de forma clara y sencilla."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return jsonify({
        "response": response.choices[0].message.content
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
