import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telethon.sync import TelegramClient
from fastapi import FastAPI
import uvicorn

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")

app = FastAPI()
telegram_app = ApplicationBuilder().token(bot_token).build()

keywords = ['web app development', 'mobile app development','developer','react developer','Front-end developers','Back-']

async def get_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = TelegramClient('session', api_id, api_hash)
    await client.start()

    response = ""
    count = 0
    async for message in client.iter_messages(channel_username, limit=100):
        if message.text:
            count += 1
            response += f"📅 {message.date.strftime('%Y-%m-%d %H:%M')}\n💬 {message.text}\n\n"

    await client.disconnect()

    if count > 0:
        await update.message.reply_text(response[:4000])
    else:
        await update.message.reply_text("No messages retrieved at all.")

telegram_app.add_handler(CommandHandler("get", get_messages))

@app.get("/")
def root():
    return {"status": "Bot running"}

@app.on_event("startup")
async def on_startup():
    webhook_url = os.getenv("WEBHOOK_URL")  # e.g. "https://yourapp.onrender.com"
    await telegram_app.bot.set_webhook(url=webhook_url)
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling()  # safe even with webhook set

@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.updater.stop()
    await telegram_app.stop()
    await telegram_app.shutdown()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
