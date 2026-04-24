import os, logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8782625568:AAHkQbnPKyyBeNXU609HoTYXmdm21Helk8g"
logging.basicConfig(level=logging.INFO)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alekum SHEPIM nima istaysiz")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("❌ Faqat Instagram havolalarini yuboring!")
        return
    msg = await update.message.reply_text("⏳ Yuklanmoqda... (1-3 daqiqa)")
    user_id = update.message.from_user.id
    video_path = f"{DOWNLOAD_DIR}/{user_id}.mp4"
    audio_path = f"{DOWNLOAD_DIR}/{user_id}.mp3"
    try:
        with yt_dlp.YoutubeDL({'outtmpl': video_path, 'format': 'best', 'quiet': True, 'socket_timeout': 120}) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Video')
        with yt_dlp.YoutubeDL({'outtmpl': f"{DOWNLOAD_DIR}/{user_id}.%(ext)s", 'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}], 'quiet': True, 'socket_timeout': 120}) as ydl:
            ydl.download([url])
        await msg.edit_text("✅ Yuborilmoqda...")
        if os.path.exists(video_path):
            with open(video_path, 'rb') as f:
                await update.message.reply_video(f, caption=f"🎬 {title}", read_timeout=120, write_timeout=120)
        if os.path.exists(audio_path):
            with open(audio_path, 'rb') as f:
                await update.message.reply_audio(f, caption=f"🎵 {title}", read_timeout=120, write_timeout=120)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Xatolik: {str(e)[:200]}")
    finally:
        for p in [video_path, audio_path]:
            if os.path.exists(p): os.remove(p)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))
    print("🤖 Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
