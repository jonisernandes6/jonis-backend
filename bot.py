import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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
    texto = (
        "👤 *MI CUENTA*\n\n"
        "Aquí podrás consultar:\n\n"
        "🪙 Tus tokens\n"
        "🆔 Tu ID de acceso\n"
        "📦 Tus compras\n"
        "💳 Tu plan\n\n"
        "⚙️ Sistema de cuenta en preparación."
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

async def pagos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "💳 *MÉTODOS DE PAGO*\n\n"
        "Puedes comprar tokens de JonisAI.\n\n"
        "🌎 Precio mostrado en:\n"
        "🇳🇮 Córdobas (NIO)\n"
        "🇺🇸 Dólares (USD)\n\n"
        "🛡️ El sistema de pago automático "
        "se conectará próximamente.\n\n"
        "💡 Después del pago, los tokens "
        "se agregarán a tu cuenta."
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


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "❓ *AYUDA DE JONISAI*\n\n"
        "Puedes utilizar los siguientes comandos:\n\n"
        "/start — 🏠 Menú principal\n"
        "/precios — 💰 Ver precios\n"
        "/comprar — 🛒 Comprar tokens\n"
        "/ia — 🧠 Información de JonisAI\n"
        "/cuenta — 👤 Mi cuenta\n"
        "/ayuda — ❓ Ayuda\n"
        "/soporte — 📞 Soporte\n\n"
        "También puedes utilizar los botones "
        "del menú."
    )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Menú principal", callback_data="menu")],
    ])

    await update.callback_query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado
    )


async def soporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "📞 *SOPORTE JONISAI*\n\n"
        "¿Tienes algún problema con tu cuenta, "
        "tokens o compra?\n\n"
        "Puedes escribir tu problema y "
        "posteriormente conectaremos este botón "
        "con nuestro sistema de soporte.\n\n"
        "🟢 Atención automática de JonisAI."
    )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Menú principal", callback_data="menu")],
    ])

    await update.callback_query.edit_message_text(
        texto,
        parse_mode="Markdown",
        reply_markup=teclado
    )

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    opciones = {
        "menu": mostrar_menu,
        "precios": precios,
        "comprar": comprar,
        "ia": ia,
        "cuenta": cuenta,
        "pagos": pagos,
        "ayuda": ayuda,
        "soporte": soporte,
    }

    funcion = opciones.get(query.data)

    if funcion:
        await funcion(update, context)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", mostrar_menu))
app.add_handler(CommandHandler("precios", precios))
app.add_handler(CommandHandler("comprar", comprar))
app.add_handler(CommandHandler("ia", ia))
app.add_handler(CommandHandler("cuenta", cuenta))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("soporte", soporte))

app.add_handler(CallbackQueryHandler(botones))

print("🤖 Bot de Telegram iniciado...")
app.run_polling()
