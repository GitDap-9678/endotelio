import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
USER_ID = int(os.environ.get('USER_ID', '0'))
PORT = int(os.environ.get('PORT', 8443))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bandeja_temporal = {}
alertas = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📥 Bandeja", callback_data='bandeja'),
            InlineKeyboardButton("🚨 Alertas", callback_data='alertas')
        ],
        [
            InlineKeyboardButton("📊 Estado", callback_data='estado')
        ]
    ]
    
    await update.message.reply_text(
        f"🧬 *SISTEMA ENDOTELIO*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✅ Bot Online\n"
        f"📅 {datetime.now().strftime('%H:%M')}\n\n"
        f"Envíame archivos:",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return
    
    doc = update.message.document
    bandeja_temporal[doc.file_id] = {
        'nombre': doc.file_name,
        'tamaño': doc.file_size,
        'fecha': datetime.now()
    }
    
    await update.message.reply_text(
        f"✅ Recibido: {doc.file_name}\n"
        f"📊 {doc.file_size/1024:.1f} KB"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'bandeja':
        msg = f"📥 Bandeja: {len(bandeja_temporal)} archivos"
        await query.edit_message_text(msg)
    elif query.data == 'alertas':
        msg = f"🚨 Alertas: {len(alertas)}"
        await query.edit_message_text(msg)
    elif query.data == 'estado':
        msg = "📊 Sistema funcionando"
        await query.edit_message_text(msg)

def main():
    logger.info("Iniciando bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://endotelio.onrender.com/{TELEGRAM_TOKEN}"
    )

if __name__ == '__main__':
    main()
