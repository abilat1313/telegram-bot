import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = "8307326016:AAEniuzPEezOGIp_H1nZRWx2bKrrl7Q5nak"
OPENAI_API_KEY = "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"

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "Ты — личный помощник."},
            {"role": "user", "content": user_text}
        ]
    }

    response = requests.post(OPENAI_URL, headers=headers, json=data).json()

    try:
        reply = response["choices"][0]["message"]["content"]
    except:
        reply = "Ошибка OpenAI"

    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot started!")
    await app.run_polling()

import asyncio
asyncio.run(main())
