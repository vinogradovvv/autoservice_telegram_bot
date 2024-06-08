"""
telegram bot main file
"""
from telegram_api.core import application as telegram_bot

telegram_bot.run_polling()

if __name__ == "main":
    telegram_bot.run_polling()
