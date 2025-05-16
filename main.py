import os
from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telethon.sync import TelegramClient

bot_token = os.getenv("BOT_TOKEN")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")

keywords = ['web app development', 'mobile app development','devloper','react developer','Front-end developers','Back-']

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

def main():
    print("BOT_TOKEN:", bot_token)
    print("API_ID:", api_id)
    print("API_HASH:", api_hash)
    print("CHANNEL_USERNAME:", channel_username)

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("get", get_messages))
    print("Bot is running...")
    app.run_polling()  # ← synchronous here

if __name__ == '__main__':
    main()
