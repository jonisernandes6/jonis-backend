from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os

app = Flask(name)
CORS(app)

==========================================

HUGGING FACE

==========================================

HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY")

if not HF_TOKEN:
raise RuntimeError(
"Falta HUGGINGFACE_API_KEY en Render"
)

client = InferenceClient(
api_key=HF_TOKEN,
provider="auto"
)

==========================================

MODELO

==========================================

MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"

VISION_MODEL = None

==========================================

INSTRUCCIONES DE JONISAI

==========================================

SYSTEM_MESSAGE = """
Eres JonisAI, un asistente virtual inteligente y conversacional.

Tu objetivo principal es ayudar al usuario de forma clara, natural,
amable y útil.

Puedes ayudar con:

- Conversación general
- Preguntas y respuestas
- Aprendizaje
- Programación
- Python
- HTML, CSS y JavaScript
- Automatización
- Proyectos
- Ideas
- Escritura y textos
- Explicaciones paso a paso
- Resolución de problemas

IMPORTANTE:

Mantén siempre el contexto de la conversación.

Lee los mensajes anteriores antes de responder al mensaje actual.

Si el usuario dice cosas como:
"no",
"sí",
"eso",
"te explico",
"mira",
"exactamente",
"¿entiendes?",
"no sabes",
o utiliza frases cortas,

interpreta esas frases teniendo en cuenta lo que se habló anteriormente.

NO cambies de tema sin motivo.

NO supongas que el usuario está pidiendo código solamente porque
estás especializado en programación.

Si el usuario simplemente quiere conversar, conversa normalmente.

Si el usuario quiere aprender algo, explica de forma sencilla y progresiva.

Si el usuario pide programación, proporciona código útil y explica cómo
funciona.

Si una pregunta no está relacionada con programación, responde
normalmente sin intentar convertirla en una tarea de programación.

No inventes información sobre lo que el usuario quiso decir.
Si realmente no entiendes algo, pregunta de manera breve y natural.

Sé paciente y mantén una conversación coherente.
"""

==========================================

INICIO

==========================================

@app.route("/")
def home():

return "JonisAI Backend funcionando"

==========================================

CHAT

==========================================

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
    # MENSAJE ACTUAL
    # ----------------------------------

    message = data.get(
        "message",
        ""
    )

    if not isinstance(message, str):

        message = str(message)

    message = message.strip()


    # ----------------------------------
    # HISTORIAL
    # ----------------------------------

    history = data.get(
        "history",
        []
    )


    if not isinstance(history, list):

        history = []


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
    # MENSAJES PARA EL MODELO
    # ----------------------------------

    messages = [

        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }

    ]


    # ----------------------------------
    # AGREGAR HISTORIAL
    # ----------------------------------

    for item in history:

        if not isinstance(item, dict):

            continue


        role = item.get("role")

        content = item.get("content")


        if role not in [
            "user",
            "assistant"
        ]:

            continue


        if not isinstance(
            content,
            str
        ):

            continue


        content = content.strip()


        if not content:

            continue


        messages.append({

            "role": role,

            "content": content

        })


    # ----------------------------------
    # CONTENIDO DEL MENSAJE ACTUAL
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

        if not isinstance(
            image,
            str
        ):

            return jsonify({

                "error":
                    "La imagen no es válida"

            }), 400


        if not image.startswith(
            "data:image/"
        ):

            return jsonify({

                "error":
                    "Formato de imagen no válido"

            }), 400


        content.append({

            "type": "image_url",

            "image_url": {

                "url": image

            }

        })


    # ----------------------------------
    # AGREGAR MENSAJE ACTUAL
    # ----------------------------------

    messages.append({

        "role": "user",

        "content": content

    })


    # ----------------------------------
    # LIMITAR HISTORIAL
    # ----------------------------------

    # Evitamos enviar una conversación
    # infinitamente grande al modelo.

    if len(messages) > 21:

        messages = (

            messages[:1] +

            messages[-20:]

        )


    # ----------------------------------
    # CONSULTAR MODELO
    # ----------------------------------

    print(
        "Consultando modelo:",
        MODEL
    )

    print(
        "Mensajes enviados:",
        len(messages)
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

        max_tokens=1000,

        temperature=0.3

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

        "response":
            response_text

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

            "model":
                MODEL

        }), 503


    return jsonify({

        "error": (
            "Error al consultar "
            "el modelo de IA"
        ),

        "details":
            error_text

    }), 500

==========================================

EJECUTAR SERVIDOR

==========================================

if name == "main":

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
