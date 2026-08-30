from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
CORS(app)

# ==========================================
# HUGGING FACE
# ==========================================

HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY")

if not HF_TOKEN:
    raise RuntimeError(
        "Falta HUGGINGFACE_API_KEY en Render"
    )

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)


# ==========================================
# MODELO
# ==========================================

MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"


# ==========================================
# INSTRUCCIONES DE JONISAI
# ==========================================

SYSTEM_MESSAGE = """
Eres JonisAI, un asistente inteligente.

Tu objetivo es ayudar al usuario de forma clara,
sencilla y útil.

Puedes ayudar con:

- Programación
- Python
- JavaScript
- HTML
- CSS
- Bases de datos
- Errores de código
- Tecnología
- Explicaciones
- Solución de problemas
- Aprendizaje

Cuando el usuario envíe una imagen, analízala
cuidadosamente y utiliza la información visible
para responder a su pregunta.

Si la imagen contiene código o un error,
explica qué está ocurriendo y cómo solucionarlo.

Explica paso a paso cuando sea necesario.

Cuando escribas código utiliza bloques de código.
"""


# ==========================================
# INICIO
# ==========================================

@app.route("/")
def home():

    return "JonisAI Backend funcionando"

@app.route("/models", methods=["GET"])
def models():
    try:
        models = client.list_deployed_models()

        resultado = []

        for model in models:
            resultado.append({
                "id": model.id,
                "provider": getattr(model, "provider", None)
            })

        return jsonify({
            "models": resultado
        }), 200

    except Exception as e:
        print("ERROR EN /models:", repr(e))

        return jsonify({
            "error": "No se pudieron consultar los modelos",
            "details": str(e)
        }), 500


# ==========================================
# CHAT
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        # ----------------------------------
        # RECIBIR JSON
        # ----------------------------------

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "error": "No se recibieron datos"
            }), 400


        # ----------------------------------
        # MENSAJE
        # ----------------------------------

        message = data.get(
            "message",
            ""
        )

        if not isinstance(message, str):
            message = str(message)

        message = message.strip()


        # ----------------------------------
        # IMAGEN
        # ----------------------------------

        image = data.get("image")


        # ----------------------------------
        # COMPROBAR DATOS
        # ----------------------------------

        if not message and not image:

            return jsonify({
                "error": (
                    "Debes escribir un mensaje "
                    "o enviar una imagen"
                )
            }), 400


        # ----------------------------------
        # CONTENIDO DEL USUARIO
        # ----------------------------------

        content = []


        # Texto

        if message:

            content.append({
                "type": "text",
                "text": message
            })


        # Imagen

        if image:

            if not isinstance(image, str):

                return jsonify({
                    "error": "La imagen no es válida"
                }), 400


            # Esperamos una imagen tipo:
            #
            # data:image/jpeg;base64,...
            #
            # o:
            #
            # data:image/png;base64,...

            if not image.startswith(
                "data:image/"
            ):

                return jsonify({
                    "error": (
                        "Formato de imagen no válido"
                    )
                }), 400


            content.append({

                "type": "image_url",

                "image_url": {
                    "url": image
                }

            })


        # ----------------------------------
        # MENSAJES PARA EL MODELO
        # ----------------------------------

        messages = [

            {
                "role": "system",
                "content": SYSTEM_MESSAGE
            },

            {
                "role": "user",
                "content": content
            }

        ]


        # ----------------------------------
        # CONSULTAR HUGGING FACE
        # ----------------------------------

        print(
            "Consultando modelo:",
            MODEL
        )

        print(
            "Tiene imagen:",
            bool(image)
        )


        completion = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            max_tokens=700,

            temperature=0.7

        )


        # ----------------------------------
        # RESPUESTA
        # ----------------------------------

        response_text = (
            completion
            .choices[0]
            .message
            .content
        )


        if not response_text:

            response_text = (
                "El modelo no devolvió texto."
            )


        return jsonify({

            "response": response_text

        }), 200


    # ======================================
    # ERROR
    # ======================================

    except Exception as e:

        print(
            "ERROR EN /chat:",
            repr(e)
        )


        error_text = str(e)


        # Error específico del modelo

        if (
            "model_not_supported"
            in error_text
        ):

            return jsonify({

                "error": (
                    "El modelo configurado no "
                    "está disponible mediante "
                    "los proveedores habilitados "
                    "para tu API de Hugging Face."
                ),

                "model": MODEL

            }), 503


        return jsonify({

            "error": (
                "Error al consultar "
                "el modelo de IA"
            ),

            "details": error_text

        }), 500


# ==========================================
# EJECUTAR SERVIDOR
# ==========================================

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
