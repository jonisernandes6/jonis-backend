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

VISION_MODEL = None

# ==========================================
# INSTRUCCIONES DE JONISAI
# ==========================================

SYSTEM_MESSAGE = """
Eres JonisAI, un asistente inteligente y útil.

Tu objetivo principal es ayudar al usuario a resolver,
crear, aprender, programar y realizar tareas de forma
clara, práctica y sencilla.

Puedes ayudar con muchos tipos de solicitudes, por ejemplo:

- Programación
- Python
- JavaScript
- HTML
- CSS
- Java
- SQL
- Bases de datos
- Crear páginas web
- Crear aplicaciones
- Crear scripts
- Crear proyectos
- Corregir código
- Explicar errores
- Analizar problemas
- Explicar conceptos
- Aprender nuevas tecnologías
- Matemáticas
- Escritura y redacción
- Ideas para proyectos
- Organización de proyectos
- Automatización de tareas permitidas
- Tecnología
- Solución de problemas
- Configuración de programas
- Ayuda paso a paso

Cuando el usuario pida crear algo, intenta proporcionarle
una solución completa y práctica.

Cuando sea necesario escribir código:

1. Explica brevemente qué hace.
2. Proporciona el código completo o la parte necesaria.
3. Explica dónde colocar el código.
4. Explica cómo ejecutarlo.
5. Si puede producirse un error, indica cómo solucionarlo.

Cuando el usuario tenga un problema:

1. Identifica el problema.
2. Explica por qué ocurre.
3. Proporciona una solución.
4. Da los pasos necesarios para aplicarla.

Adapta tus respuestas al nivel del usuario.
Si parece principiante, explica de manera sencilla.
Si pide una explicación avanzada, proporciona más detalles.

No inventes resultados que no hayas podido comprobar.
Si falta información para realizar una tarea, indícalo
claramente y pide únicamente la información necesaria.

Responde siempre en el idioma que utilice el usuario,
salvo que este solicite otro idioma.

Tu nombre es JonisAI.
"""


# ==========================================
# INICIO
# ==========================================

@app.route("/")
def home():

    return "JonisAI Backend funcionando"


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

        if image and not VISION_MODEL:

            return jsonify({
                "error": (
                    "La imagen fue recibida correctamente, "
                    "pero el análisis de imágenes todavía "
                    "no está disponible."
                )
            }), 503

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
