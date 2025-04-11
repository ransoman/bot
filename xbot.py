from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import random
import os
from datetime import datetime
import aiohttp

# --- KONFIGURASI ---
BOT_TOKEN = '7953818033:AAHanu-auAM67GoJ6I6gBlBFlyI5wsGsnUI'
os.makedirs("logs", exist_ok=True)

# --- FITUR 1: START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Halo {update.effective_user.first_name}! Aku X-BOT 🤖 Siap bantu kamu!")

# --- FITUR 2: AUTO RESPONDER SAAT DISEBUT ---
async def mention_responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and context.bot.username.lower() in update.message.text.lower():
        await update.message.reply_text(f"Ada apa, {update.effective_user.first_name}? Aku dipanggil~ 🤖")

# --- FITUR 3: MINI GAMES ---
async def tebak_angka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    angka = random.randint(1, 10)
    await update.message.reply_text("🎯 Aku sudah pilih angka 1-10. Tebak!")
    await update.message.reply_text(f"Jawaban: {angka} 😆")

async def suit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pilihan = ["batu", "gunting", "kertas"]
    bot = random.choice(pilihan)
    await update.message.reply_text(f"Aku milih: {bot} ✊✌✋")

async def lempar_dadu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    angka = random.randint(1, 6)
    await update.message.reply_text(f"🎲 Dadu menunjukkan: {angka}")

# --- FITUR 4: DARK MODE / HACKING STYLE ---
async def darkmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = """💻 Accessing Hidden Network...
🔍 Scanning Ports...
🧠 Intelligence Gathering Complete.

👁‍🗨 Target: Anonymous
🕶 Status: Active Surveillance"""
    await update.message.reply_text(teks)

# --- FITUR 5: DOWNLOAD YOUTUBE ---
async def download_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan format: /yt <link_youtube>")
        return

    url = context.args[0]
    await update.message.reply_text("🔄 Sedang mendownload...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open('video.mp4', 'rb') as video:
        await update.message.reply_video(video=video)

# --- FITUR 6: AUTO SAVE MEDIA ---
async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username or update.effective_user.first_name
    date = datetime.now().strftime("%Y%m%d-%H%M%S")

    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        path = f"logs/{user}-{date}.jpg"
        await file.download_to_drive(path)
        await update.message.reply_text("🖼 Foto disimpan.")

    elif update.message.video:
        video = update.message.video
        file = await video.get_file()
        path = f"logs/{user}-{date}.mp4"
        await file.download_to_drive(path)
        await update.message.reply_text("📹 Video disimpan.")

# --- FITUR 7: PING API EKSTERNAL ---
async def cek_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.ipify.org?format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            await update.message.reply_text(f"🔔 IP Publik: {data['ip']}")

# --- FITUR 8: IP TRACE ---
async def iptrace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan format: /iptrace <IP atau domain>")
        return
    ip = context.args[0]
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}") as resp:
            data = await resp.json()
            if data['status'] == 'success':
                msg = (
                    f"🌐 IP: {data['query']}\n"
                    f"🏙️ Kota: {data['city']}\n"
                    f"🌍 Negara: {data['country']}\n"
                    f"🛰️ ISP: {data['isp']}\n"
                    f"📡 Koordinat: {data['lat']}, {data['lon']}\n"
                    f"🧭 Zona Waktu: {data['timezone']}"
                )
            else:
                msg = "❌ IP tidak ditemukan atau tidak valid."
            await update.message.reply_text(msg)

# --- RUN APP ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tebakangka", tebak_angka))
    app.add_handler(CommandHandler("suit", suit))
    app.add_handler(CommandHandler("dadu", lempar_dadu))
    app.add_handler(CommandHandler("darkmode", darkmode))
    app.add_handler(CommandHandler("yt", download_youtube))
    app.add_handler(CommandHandler("pingapi", cek_status))
    app.add_handler(CommandHandler("iptrace", iptrace))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mention_responder))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, save_media))

    print("✅ X-BOT V1 AKTIF...")
    app.run_polling()
