import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        [
            InlineKeyboardButton("💰 Precios", callback_data="precios"),
            InlineKeyboardButton("🛒 Comprar", callback_data="comprar"),
        ],
        [
            InlineKeyboardButton("🧠 JonisAI", callback_data="ia"),
            InlineKeyboardButton("❓ Ayuda", callback_data="ayuda"),
        ],
    ]

    await update.message.reply_text(
        "🤖 ¡Bienvenido a JonisAI!\n\n"
        "Soy el asistente automático de JonisAI.\n"
        "¿Qué deseas hacer?",
        reply_markup=InlineKeyboardMarkup(teclado),
    )


async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "precios":
        texto = (
            "💰 *PRECIOS DE JONISAI*\n\n"
            "🪙 100 tokens → 50 NIO\n"
            "🪙 500 tokens → 200 NIO\n"
            "🪙 1,000 tokens → 350 NIO\n"
            "🪙 5,000 tokens → 1,500 NIO\n\n"
            "Los tokens sirven para utilizar JonisAI."
        )

    elif query.data == "comprar":
        texto = (
            "🛒 *COMPRAR TOKENS*\n\n"
            "Puedes elegir uno de estos paquetes:\n\n"
            "🪙 100 → 50 NIO\n"
            "🪙 500 → 200 NIO\n"
            "🪙 1,000 → 350 NIO\n"
            "🪙 5,000 → 1,500 NIO\n\n"
            "🚧 Sistema de compra automática en preparación."
        )

    elif query.data == "ia":
        texto = (
            "🧠 *JONISAI*\n\n"
            "Puedes utilizar nuestro asistente de IA "
            "para hacer preguntas, programar y conversar."
        )

    else:
        texto = (
            "❓ *AYUDA*\n\n"
            "Usa los botones del menú para consultar "
            "precios, comprar tokens o conocer JonisAI."
        )

    await query.edit_message_text(texto, parse_mode="Markdown")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(botones))

print("🤖 Bot de Telegram iniciado...")
app.run_polling()
