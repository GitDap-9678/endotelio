import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
PUBLIC_URL = os.getenv("PUBLIC_URL")             # p.ej. https://endotelio-bot-jn62.onrender.com
PORT = int(os.getenv("PORT", "10000"))           # Render te da PORT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bot listo! Envíame archivos, textos o enlaces.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"Recibido: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, echo))

    # Ejecuta webhook (no polling). Render Free “despierta” con cada llamada.
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{PUBLIC_URL}/{TOKEN}",
    )

if __name__ == "__main__":
    main()
