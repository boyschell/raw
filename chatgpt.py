import os
import logging
import requests
from telegram import Update
from telegram.ext import Filters
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Telegram bot token from BotFather
TELEGRAM_TOKEN = os.getenv('6742667446:AAFhjpdI7m6Pk1MZz0fS6qP9LFb0idcTQkE')  # Replace with your Telegram bot token

# OpenAI API Key
OPENAI_API_KEY = os.getenv('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')  # Replace with your OpenAI API key
API_URL = "https://api.openai.com/v1/engines/davinci/completions"

update_queue = Queue()
updater = Updater(bot=bot, update_queue=update_queue)

dispatcher = Dispatcher(updater.bot, update_queue)
dispatcher.use_context = True


# Define a function to handle incoming Telegram messages
def handle_message(update: Update, context: CallbackContext):
  message_text = update.message.text
  chat_id = update.message.chat_id

  # Check if the message is code-related and needs assistance 
  if message_text.startswith("/codefix"):
    # Extract the code from the message 
    code_to_fix = message_text[8:] # Adjust the index as needed

    # Send the code to ChatGPT for assistance
    response = openai.Completion.create(
      engine="davinci", # Use the appropriate ChatGPT engine  
      prompt=f"Fix the following code:\n```{code_to_fix}```",
      max_tokens=50 # Adjust the response length as needed
    )

    # Extract the response from ChatGPT
    fixed_code = response.choices[0].text
    
    # Send the fixed code back to the user
    bot.send_message(chat_id=chat_id, text=f"Here's the fixed code:\n```{fixed_code}```")

  else:
    # Handle other non-code related messages here
    bot.send_message(chat_id=chat_id, text="I can only assist with code fixes. Use /codefix to get help.")

# Define a command handler  
def start(update: Update, context: CallbackContext):
  update.message.reply_text("Welcome to the CodeFix Bot! Send /codefix followed by your code for assistance.")

# Set up the message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)
dispatcher.add_handler(message_handler)

# Set up the command handler
dispatcher.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
  # Start the Telegram bot updater and the Flask app
  updater.start_polling()  
  app.run(debug=True)
