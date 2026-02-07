from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

TOKEN = "8268999726:AAHtUPWKCblz0ke9tfRZRPnV5IJ10mFC48s"

# Fon vazifa
async def fon_vazifa(app):
    chat_ids = [123456789]  # shu yerga foydalanuvchi chat_id larini qo'yish mumkin
    for chat_id in chat_ids:
        try:
            await app.bot.send_message(chat_id, "Salom! Bu fon vazifa xabari.")
        except Exception as e:
            print(f"Xatolik: {e}")

# Telegramdan xabar oluvchi handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Siz yozdingiz: {update.message.text}")

# Asosiy funksiya
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Background scheduler ishga tushadi
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.create_task(fon_vazifa(app)), 'interval', seconds=30)
    scheduler.start()

    print("Bot ishga tushdi...")
    app.run_polling()  # Bu allaqachon asyncio loop ishlatadi

if __name__ == "__main__":
    main()
