from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
import yt_dlp
import sys

TOKEN = "8268999726:AAHtUPWKCblz0ke9tfRZRPnV5IJ10mFC48s"

# EXE ichida FFmpeg faylini topish
def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller EXE ichida
        base_path = sys._MEIPASS
        return os.path.join(base_path, "ffmpeg.exe")
    else:
        # Oddiy Python ishga tushganda, tizimdagi ffmpeg
        return "ffmpeg"

FFMPEG_PATH = get_ffmpeg_path()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Instagram link
    if text and "instagram.com" in text:
        await update.message.reply_text("Instagram video yuklanmoqda, ovoz chiqarilmoqda...")
        voice_path = "voice.ogg"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': voice_path,
            'quiet': True,
            'ffmpeg_location': FFMPEG_PATH,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])
            await update.message.reply_voice(open(voice_path, 'rb'))
            os.remove(voice_path)
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")

    # Telegram video
    elif update.message.video:
        await update.message.reply_text("Video yuklanmoqda, ovoz chiqarilmoqda...")
        video_file = await update.message.video.get_file()
        video_path = "temp_video.mp4"
        voice_path = "voice.ogg"
        await video_file.download_to_drive(video_path)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': voice_path,
            'ffmpeg_location': FFMPEG_PATH,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_path])
            await update.message.reply_voice(open(voice_path, 'rb'))
            os.remove(voice_path)
            os.remove(video_path)
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")

    else:
        await update.message.reply_text("Iltimos, Instagram linki yoki video yuboring!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot ishga tushdi...")
app.run_polling()
