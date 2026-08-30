from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os
import base64

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY")

if not HF_TOKEN:
    raise RuntimeError("Falta HUGGINGFACE_API_KEY en Render")

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)

# Modelo multimodal: texto + imágenes
MODEL = "Qwen/Qwen2.5-VL-3B-Instruct"


@app.route("/")
def home():
    return "JonisAI Backend funcionando"


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No se recibieron datos"
            }), 400

        message = data.get("message", "").strip()
        image = data.get("image")

        if not message and not image:
            return jsonify({
                "error": "Debes enviar un mensaje o una imagen"
            }), 400

        system_message = (
            "Eres JonisAI, un asistente inteligente especializado "
            "en programación, tecnología y solución de problemas. "
            "Explica de forma clara, sencilla y paso a paso. "
            "Puedes analizar imágenes cuando el usuario las envíe. "
            "Si aparece código, errores o capturas de pantalla, "
            "analízalos y explica cómo solucionarlos."
        )

        # ==========================================
        # MENSAJE DEL USUARIO
        # ==========================================

        content = []

        if message:

            content.append({
                "type": "text",
                "text": message
            })

        # ==========================================
        # IMAGEN
        # ==========================================

        if image:

            # La imagen llega como:
            # data:image/jpeg;base64,XXXXX

            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image
                }
            })

        # ==========================================
        # CONSULTA AL MODELO
        # ==========================================

        completion = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": content
                }
            ],

            max_tokens=700,
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

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
