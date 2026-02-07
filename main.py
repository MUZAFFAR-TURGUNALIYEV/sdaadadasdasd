from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = "8268999726:AAHtUPWKCblz0ke9tfRZRPnV5IJ10mFC48s"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Instagram link
    if text and "instagram.com" in text:
        await update.message.reply_text("Instagram video yuborildi, lekin ovoz chiqarish uchun FFmpeg kerak bo‘ladi. Bu versiyada faqat linkni yuborish mumkin.")
        await update.message.reply_text(f"Instagram link: {text}")

    # Telegram video
    elif update.message.video:
        await update.message.reply_text("Video yuborildi, lekin ovoz chiqarish uchun FFmpeg kerak bo‘ladi. Bu versiyada faqat video yuboriladi.")
        video_file = await update.message.video.get_file()
        video_path = "temp_video.mp4"
        await video_file.download_to_drive(video_path)
        await update.message.reply_video(open(video_path, "rb"))
        os.remove(video_path)

    else:
        await update.message.reply_text("Iltimos, Instagram linki yoki video yuboring!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot ishga tushdi...")
app.run_polling()
