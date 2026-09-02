from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import sqlite3
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

DB_PATH = os.environ.get("DATABASE_PATH", "jonisai.db")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("Falta GROQ_API_KEY en Render")

client = Groq(
    api_key=GROQ_API_KEY
)

MODELS = {
    "gpt-oss-20b": {
        "id": "openai/gpt-oss-20b",
        "name": "🤖 GPT-OSS 20B"
    },
    "llama": {
        "id": "llama-3.1-8b-instant",
        "name": "🦙 Llama 3.1 8B"
    },
    "qwen": {
        "id": "qwen/qwen3.6-27b",
        "name": "🧠 Qwen 3.6 27B"
    }
}

DEFAULT_MODEL = "gpt-oss-20b"

SYSTEM_MESSAGE = """
Eres JonisAI, un asistente virtual inteligente y conversacional.

Habla principalmente en español, a menos que el usuario pida otro idioma.

Tu forma de hablar debe ser natural, cercana, clara y relajada.

Puedes conversar sobre muchos temas. No conviertas automáticamente una
conversación normal en una conversación sobre programación.

Si el usuario quiere simplemente platicar, conversa con él normalmente.

Si el usuario habla de sus sentimientos, problemas personales o situaciones
de su vida, escucha con atención y responde de forma empática, natural y
respetuosa.

Mantén siempre el contexto de la conversación.

Si el usuario dice cosas como "mira", "oye", "eso", "no", "sí",
"exactamente" o "te explico", utiliza el contexto anterior para entenderlo.

Si no entiendes algo, pregunta de forma breve y natural.

Si el usuario quiere aprender algo, explícalo paso a paso.

Si pregunta sobre programación, proporciona explicaciones técnicas y código
cuando sea necesario.

Cuando escribas código:

- Usa bloques de código.
- Indica el lenguaje.
- Procura que el código sea completo.
- Explica cómo ejecutarlo.

No afirmes que eres una persona real.

Tu objetivo es que la conversación se sienta natural y coherente.
"""


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL DEFAULT 'Nueva conversación',
            model TEXT NOT NULL DEFAULT 'qwen-coder',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


init_db()
def now():
    return datetime.utcnow().isoformat()


def get_model(model_key):
    if model_key not in MODELS:
        return DEFAULT_MODEL

    return model_key


def create_conversation(model=DEFAULT_MODEL):
    model = get_model(model)

    timestamp = now()

    conn = get_db()

    cursor = conn.execute(
        """
        INSERT INTO conversations
        (title, model, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            "Nueva conversación",
            model,
            timestamp,
            timestamp
        )
    )

    conversation_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return conversation_id


def get_conversation(conversation_id):
    conn = get_db()

    conversation = conn.execute(
        """
        SELECT *
        FROM conversations
        WHERE id = ?
        """,
        (conversation_id,)
    ).fetchone()

    conn.close()

    return conversation


def save_message(conversation_id, role, content):
    conn = get_db()

    timestamp = now()

    conn.execute(
        """
        INSERT INTO messages
        (conversation_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content,
            timestamp
        )
    )

    conn.execute(
        """
        UPDATE conversations
        SET updated_at = ?
        WHERE id = ?
        """,
        (
            timestamp,
            conversation_id
        )
    )

    conn.commit()
    conn.close()


def get_messages(conversation_id):
    conn = get_db()

    rows = conn.execute(
        """
        SELECT id, role, content, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    ).fetchall()

    conn.close()

    return rows


def generate_title(text):
    text = text.strip()

    if not text:
        return "Nueva conversación"

    text = " ".join(text.split())

    if len(text) > 45:
        text = text[:45].rstrip() + "..."

    return text


@app.route("/")
def home():
    return "JonisAI Backend funcionando"


@app.route("/models", methods=["GET"])
def models():
    return jsonify({
        "models": [
            {
                "key": key,
                "id": value["id"],
                "name": value["name"]
            }
            for key, value in MODELS.items()
        ],
        "default": DEFAULT_MODEL
    })


@app.route("/conversations", methods=["POST"])
def new_conversation():
    try:
        data = request.get_json(silent=True) or {}

        model = data.get(
            "model",
            DEFAULT_MODEL
        )

        model = get_model(model)

        conversation_id = create_conversation(model)

        conversation = get_conversation(
            conversation_id
        )

        return jsonify({
            "id": conversation["id"],
            "title": conversation["title"],
            "model": conversation["model"],
            "created_at": conversation["created_at"],
            "updated_at": conversation["updated_at"]
        }), 201

    except Exception as e:
        print(
            "ERROR creando conversación:",
            repr(e)
        )

        return jsonify({
            "error": "No se pudo crear la conversación",
            "details": str(e)
        }), 500
@app.route("/conversations", methods=["GET"])
def conversations():
    try:
        conn = get_db()

        rows = conn.execute(
            """
            SELECT
                id,
                title,
                model,
                created_at,
                updated_at
            FROM conversations
            ORDER BY updated_at DESC
            """
        ).fetchall()

        conn.close()

        result = []

        for row in rows:
            result.append({
                "id": row["id"],
                "title": row["title"],
                "model": row["model"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })

        return jsonify({
            "conversations": result
        })

    except Exception as e:
        print(
            "ERROR listando conversaciones:",
            repr(e)
        )

        return jsonify({
            "error": "No se pudo obtener el historial",
            "details": str(e)
        }), 500


@app.route(
    "/conversations/<int:conversation_id>",
    methods=["GET"]
)
def conversation_detail(conversation_id):
    try:
        conversation = get_conversation(
            conversation_id
        )

        if not conversation:
            return jsonify({
                "error": "La conversación no existe"
            }), 404

        rows = get_messages(
            conversation_id
        )

        messages = []

        for row in rows:
            messages.append({
                "id": row["id"],
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"]
            })

        return jsonify({
            "conversation": {
                "id": conversation["id"],
                "title": conversation["title"],
                "model": conversation["model"],
                "created_at": conversation["created_at"],
                "updated_at": conversation["updated_at"]
            },
            "messages": messages
        })

    except Exception as e:
        print(
            "ERROR obteniendo conversación:",
            repr(e)
        )

        return jsonify({
            "error": "No se pudo obtener la conversación",
            "details": str(e)
        }), 500


@app.route(
    "/conversations/<int:conversation_id>",
    methods=["DELETE"]
)
def delete_conversation(conversation_id):
    try:
        conn = get_db()

        cursor = conn.execute(
            """
            DELETE FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        conn.commit()

        deleted = cursor.rowcount

        conn.close()

        if deleted == 0:
            return jsonify({
                "error": "La conversación no existe"
            }), 404

        return jsonify({
            "success": True
        })

    except Exception as e:
        print(
            "ERROR eliminando conversación:",
            repr(e)
        )

        return jsonify({
            "error": "No se pudo eliminar la conversación",
            "details": str(e)
        }), 500
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "No se recibieron datos"
            }), 400

        message = data.get("message", "")

        if not isinstance(message, str):
            message = str(message)

        message = message.strip()

        image = data.get("image")

        conversation_id = data.get(
            "conversation_id"
        )

        requested_model = data.get("model")

        if not message and not image:
            return jsonify({
                "error": "Debes escribir un mensaje"
            }), 400

        # =====================================
        # CREAR CONVERSACIÓN SI NO EXISTE
        # =====================================

        if not conversation_id:
            conversation_id = create_conversation(
                requested_model or DEFAULT_MODEL
            )

        else:
            try:
                conversation_id = int(
                    conversation_id
                )

            except (ValueError, TypeError):
                return jsonify({
                    "error": "conversation_id inválido"
                }), 400

        conversation = get_conversation(
            conversation_id
        )

        if not conversation:
            return jsonify({
                "error": "La conversación no existe"
            }), 404

        # =====================================
        # SELECCIONAR MODELO
        # =====================================

        model_key = conversation["model"]

        if requested_model:
            model_key = get_model(
                requested_model
            )

            conn = get_db()

            conn.execute(
                """
                UPDATE conversations
                SET model = ?
                WHERE id = ?
                """,
                (
                    model_key,
                    conversation_id
                )
            )

            conn.commit()
            conn.close()

        model_id = MODELS[
            model_key
        ]["id"]

        # =====================================
        # RECUPERAR HISTORIAL
        # =====================================

        previous_messages = get_messages(
            conversation_id
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE
            }
        ]

        # Últimos 20 mensajes para no hacer
        # demasiado grande la petición.

        recent_messages = list(
            previous_messages[-20:]
        )

        for item in recent_messages:

            role = item["role"]
            content = item["content"]

            if role not in [
                "user",
                "assistant"
            ]:
                continue

            if not content:
                continue

            messages.append({
                "role": role,
                "content": content
            })

        # =====================================
        # MENSAJE ACTUAL
        # =====================================

        content = []

        if message:
            content.append({
                "type": "text",
                "text": message
            })

        # =====================================
        # IMAGEN
        # =====================================

        if image:

            if not isinstance(image, str):
                return jsonify({
                    "error": "La imagen no es válida"
                }), 400

            if not image.startswith(
                "data:image/"
            ):
                return jsonify({
                    "error": "Formato de imagen no válido"
                }), 400

            return jsonify({
                "error":
                    "El análisis de imágenes todavía no está activado."
            }), 503

        messages.append({
            "role": "user",
            "content": content
        })

        # =====================================
        # GUARDAR MENSAJE DEL USUARIO
        # =====================================

        save_message(
            conversation_id,
            "user",
            message
        )

        print(
            "================================="
        )

        print(
            "Consultando JonisAI"
        )

        print(
            "Conversación:",
            conversation_id
        )

        print(
            "Modelo:",
            model_id
        )

        print(
            "Mensajes:",
            len(messages)
        )

        print(
            "================================="
        )

        # =====================================
        # CONSULTAR GROQ
        # =====================================

        completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=1500,
            temperature=0.5
        )

        response_text = (
            completion
            .choices[0]
            .message
            .content
        )

        response_text = re.sub(
            r"<think>.*?</think>",
            "",
            response_text,
            flags=re.DOTALL
        ).strip()

        if not response_text:
            response_text = (
                "El modelo no devolvió texto."
            )

        # =====================================
        # GUARDAR RESPUESTA
        # =====================================

        save_message(
            conversation_id,
            "assistant",
            response_text
        )

        # =====================================
        # CREAR TÍTULO AUTOMÁTICO
        # =====================================

        current_messages = get_messages(
            conversation_id
        )

        user_messages = [
            item["content"]
            for item in current_messages
            if item["role"] == "user"
        ]

        if len(user_messages) == 1:

            title = generate_title(
                user_messages[0]
            )

            conn = get_db()

            conn.execute(
                """
                UPDATE conversations
                SET title = ?
                WHERE id = ?
                """,
                (
                    title,
                    conversation_id
                )
            )

            conn.commit()
            conn.close()

        # =====================================
        # OBTENER CONVERSACIÓN ACTUALIZADA
        # =====================================

        conversation = get_conversation(
            conversation_id
        )

        return jsonify({
            "response": response_text,
            "conversation_id": conversation_id,
            "title": conversation["title"],
            "model": conversation["model"]
        }), 200

    except Exception as e:

        print(
            "ERROR EN /chat:",
            repr(e)
        )

        error_text = str(e)

        if "model_not_supported" in error_text:

            return jsonify({
                "error":
                    "El modelo no está disponible mediante los proveedores habilitados para tu cuenta de Hugging Face.",
                "model":
                    model_id if "model_id" in locals()
                    else None
            }), 503

        return jsonify({
            "error":
                "Error al consultar el modelo",
            "details":
                error_text
        }), 500
# =========================================================
# EJECUTAR SERVIDOR
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    print("=================================")
    print("🤖 JonisAI Backend")
    print("🚀 Servidor iniciado")
    print("💾 Base de datos:", DB_PATH)
    print("=================================")

    app.run(
        host="0.0.0.0",
        port=port
    )
