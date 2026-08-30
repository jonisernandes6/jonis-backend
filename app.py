from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY")

if not HF_TOKEN:
    raise RuntimeError("Falta HUGGINGFACE_API_KEY en Render")

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)

MODEL = "Qwen/Qwen2.5-Coder-1.5B-Instruct"


@app.route("/")
def home():
    return "JonisAI Backend funcionando"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Falta el mensaje"
            }), 400

        message = data["message"].strip()

        if not message:
            return jsonify({
                "error": "El mensaje está vacío"
            }), 400

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres JonisAI, un asistente especializado en "
                        "programación. Explica código de forma clara, "
                        "sencilla y paso a paso. Cuando escribas código, "
                        "utiliza bloques de código apropiados."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )

        response_text = completion.choices[0].message.content

        return jsonify({
            "response": response_text
        }), 200

    except Exception as e:
        print("ERROR EN /chat:", repr(e))

        return jsonify({
            "error": "Error al consultar el modelo de IA",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
