import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Telegram bot token from BotFather
TELEGRAM_TOKEN = os.getenv('6742667446:AAFhjpdI7m6Pk1MZz0fS6qP9LFb0idcTQkE')  # Replace with your Telegram bot token

# OpenAI API Key
OPENAI_API_KEY = os.getenv('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')  # Replace with your OpenAI API key
API_URL = "https://api.openai.com/v1/engines/davinci/completions"

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hi! I'm your ChatGPT bot. Send me a message and I'll respond.")

# Function to handle messages
def echo(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    response = get_chatgpt_response(message)
    update.message.reply_text(response)

# Function to get response from ChatGPT
def get_chatgpt_response(message):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": message,
        "max_tokens": 100
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()['choices'][0]['text'].strip()

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
