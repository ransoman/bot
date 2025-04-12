import os
import random
import logging
import aiohttp
from telegram import Update, MessageEntity
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# Ganti token dengan token bot kamu
BOT_TOKEN = "7953818033:AAHanu-auAM67GoJ6I6gBlBFlyI5wsGsnUI"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *X-BOT V1 AKTIF*\n\n"
        "Ketik /help buat lihat fitur bot.",
        parse_mode='Markdown'
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *FITUR X-BOT:*\n"
        "/dadu — Lempar dadu 🎲\n"
        "/suit — Main batu-gunting-kertas ✊✌️✋\n"
        "/tebakangka — Tebak angka 1-10 🎯\n"
        "/iptrace <ip> — Lacak lokasi IP 🌐\n"
        "/yt <link> — Download video YouTube 🎥\n"
        "\nBot juga auto-reply kalau kamu mention dia 🤖",
        parse_mode='Markdown'
    )

# /dadu
async def dadu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hasil = random.randint(1, 6)
    await update.message.reply_text(f"🎲 Angka dadu: {hasil}")

# /suit
async def suit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pilihan = random.choice(["✊ Batu", "✌️ Gunting", "✋ Kertas"])
    await update.message.reply_text(f"Aku pilih: {pilihan}")

# /tebakangka
async def tebakangka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    angka = random.randint(1, 10)
    await update.message.reply_text("🎯 Coba tebak angka dari 1 - 10!")

    def check(m: Update):
        return m.from_user.id == update.message.from_user.id

    try:
        response = await context.bot.wait_for('message', timeout=15)
        if str(angka) == response.text.strip():
            await update.message.reply_text("🎉 Benar!")
        else:
            await update.message.reply_text(f"❌ Salah! Jawabannya: {angka}")
    except:
        await update.message.reply_text("⌛ Terlalu lama... coba lagi!")

# /iptrace
async def iptrace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Contoh: /iptrace 8.8.8.8")
        return

    ip = context.args[0]
    url = f"http://ip-api.com/json/{ip}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data["status"] == "success":
                msg = (
                    f"🌍 *IP Trace Result:*\n"
                    f"IP: `{ip}`\n"
                    f"Negara: {data['country']} - {data['countryCode']}\n"
                    f"Kota: {data['city']}\n"
                    f"Isp: {data['isp']}\n"
                    f"Koordinat: {data['lat']}, {data['lon']}"
                )
            else:
                msg = "❌ IP tidak valid atau gagal dilacak."
            await update.message.reply_text(msg, parse_mode='Markdown')

# /yt (placeholder)
async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Fitur YouTube belum diaktifkan.")

# Auto-save media
async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username or update.message.from_user.first_name
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        filename = f"media/{user}_photo.jpg"
        await file.download_to_drive(filename)
        await update.message.reply_text("🖼️ Foto disimpan.")
    elif update.message.video:
        file = await update.message.video.get_file()
        filename = f"media/{user}_video.mp4"
        await file.download_to_drive(filename)
        await update.message.reply_text("🎞️ Video disimpan.")

# Auto-reply kalau disebut
async def mention_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = (await context.bot.get_me()).username.lower()
    if any(ent.type == MessageEntity.MENTION and bot_username in update.message.text.lower()
           for ent in update.message.entities or []):
        await update.message.reply_text("🤖 Aku dipanggil? Aku di sini, siap bantu!")

# === MAIN SETUP ===
if __name__ == '__main__':
    if not os.path.exists("media"):
        os.makedirs("media")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dadu", dadu))
    app.add_handler(CommandHandler("suit", suit))
    app.add_handler(CommandHandler("tebakangka", tebakangka))
    app.add_handler(CommandHandler("iptrace", iptrace))
    app.add_handler(CommandHandler("yt", yt))

    # Auto media save
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, save_media))

    # Auto responder if mentioned
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mention_reply))

    print("✅ X-BOT V1 is running...")
    app.run_polling()
