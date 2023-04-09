import os
import requests
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram API token
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Adobe Enhance API endpoint
ENHANCE_URL = "https://api.adobe.com/v2/eebc4a54-a9a4-4aa4-bd68-5c5f5e21f5c5/audio/analyze"

# Create the bot object
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define a function to handle incoming messages
def handle_message(update, context):
    # Get the audio file from the message
    file = context.bot.get_file(update.message.audio.file_id)
    # Download the audio file to a temporary location
    file_path = file.download()
    # Enhance the audio file using the Adobe Enhance API
    headers = {"x-api-key": os.getenv("ADOBE_API_KEY")}
    response = requests.post(ENHANCE_URL, headers=headers, files={"file": open(file_path, "rb")})
    # Send the enhanced audio file back to the user
    context.bot.send_audio(chat_id=update.message.chat_id, audio=response.content)
    # Delete the temporary file
    os.remove(file_path)

# Register the message handler with the dispatcher
dispatcher.add_handler(MessageHandler(Filters.audio, handle_message))

# Start the bot
updater.start_polling()
