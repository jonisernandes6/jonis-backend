import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

def menu_principal():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💰 Precios", callback_data="precios"),
            InlineKeyboardButton("🛒 Comprar", callback_data="comprar"),
        ],
        [
            InlineKeyboardButton("🧠 JonisAI", callback_data="ia"),
            InlineKeyboardButton("👤 Mi cuenta", callback_data="cuenta"),
        ],
        [
            InlineKeyboardButton("💳 Pagos", callback_data="pagos"),
            InlineKeyboardButton("❓ Ayuda", callback_data="ayuda"),
        ],
        [
            InlineKeyboardButton("📞 Soporte", callback_data="soporte"),
        ],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update, context)

async def mostrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🤖 *Bienvenido a JonisAI*\n\n"
        "Tu asistente de inteligencia artificial para:\n"
        "💬 Conversar\n"
        "💻 Programar\n"
        "🧠 Resolver preguntas\n"
        "🚀 Crear y aprender\n\n"
        "¿Qué deseas hacer?"
    )

    if update.message:
        await update.message.reply_text(
            texto,
            parse_mode="Markdown",
            reply_markup=menu_principal()
        )
    else:
        query = update.callback_query
        await query.edit_message_text(
            texto,
            parse_mode="Markdown",
            reply_markup=menu_principal()
        )

async def precios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "💰 *PRECIOS DE JONISAI*\n\n"
        "🪙 *100 tokens*\n"
        "🇳🇮 50 NIO\n"
        "🇺🇸 1.36 USD\n\n"
        "🪙 *500 tokens*\n"
        "🇳🇮 200 NIO\n"
        "🇺🇸 5.44 USD\n\n"
        "🪙 *1,000 tokens*\n"
        "🇳🇮 350 NIO\n"
        "🇺🇸 9.52 USD\n\n"
        "🪙 *5,000 tokens*\n"
        "🇳🇮 1,500 NIO\n"
        "🇺🇸 40.80 USD\n\n"
        "✨ Los tokens se utilizan para utilizar JonisAI."
    )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Comprar tokens", callback_data="comprar")],
        [InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")],
    ])

    await update.callback_query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado
    )

async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🛒 *COMPRAR TOKENS*\n\n"
        "Elige el paquete que quieras:\n\n"
        "🪙 100 tokens — C$50 / US$1.36\n"
        "🪙 500 tokens — C$200 / US$5.44\n"
        "🪙 1,000 tokens — C$350 / US$9.52\n"
        "🪙 5,000 tokens — C$1,500 / US$40.80\n\n"
        "💳 Próximamente podrás seleccionar "
        "el paquete y realizar el pago automáticamente."
    )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ver precios", callback_data="precios")],
        [InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")],
    ])

    await update.callback_query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado
    )

async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🧠 *JONISAI*\n\n"
        "Tu asistente de inteligencia artificial.\n\n"
        "💬 Conversación\n"
        "💻 Programación\n"
        "❓ Preguntas y respuestas\n"
        "📚 Aprendizaje\n\n"
        "🚀 Abre JonisAI y comienza a utilizarlo."
    )

    teclado = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🚀 Abrir JonisAI",
                url="https://huggingface.co/spaces/jonisrejion89/jonis-IA-gpt"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Volver al menú",
                callback_data="menu"
            )
        ],
    ])

    await update.callback_query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado
    )

async def cuenta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "👤 *Mi Cuenta*\n\nAquí verás tus tokens restantes y estado de suscripción."
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")]])
    await update.callback_query.edit_message_text(texto, reply_markup=teclado)

async def pagos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "💳 *Pagos*\n\nMétodos de pago disponibles: PayPal, Transferencia Bancaria."
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")]])
    await update.callback_query.edit_message_text(texto, reply_markup=teclado)

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "❓ *Ayuda*\n\nSi tienes problemas, contacta a soporte."
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")]])
    await update.callback_query.edit_message_text(texto, reply_markup=teclado)

async def soporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "📞 *Soporte*\n\nCorreo: soporte@jonisai.com"
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")]])
    await update.callback_query.edit_message_text(texto, reply_markup=teclado)

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update, context)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu$"))
    application.add_handler(CallbackQueryHandler(precios, pattern="^precios$"))
    application.add_handler(CallbackQueryHandler(comprar, pattern="^comprar$"))
    application.add_handler(CallbackQueryHandler(ia, pattern="^ia$"))
    application.add_handler(CallbackQueryHandler(cuenta, pattern="^cuenta$"))
    application.add_handler(CallbackQueryHandler(pagos, pattern="^pagos$"))
    application.add_handler(CallbackQueryHandler(ayuda, pattern="^ayuda$"))
    application.add_handler(CallbackQueryHandler(soporte, pattern="^soporte$"))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
