from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
from handler_functions.common.start_command_handler import handle_start
from handler_functions.common.delete_command_handler import handle_delete
from handler_functions.common.freetext_handler import handle_free_text
from handler_functions.common.voice_message_handler import handle_voice_message
from handler_functions.common.audio_command_handler import handle_audio
from handler_functions.common.multimedia_handler import handle_multimedia
from handler_functions.common.topic_command_handler import handle_topic


# Load environment variables from the .env file
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# Main function to run the bot
def main():
    # Connects the script to the Telegram API
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Assigns command handler functions
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("delete", handle_delete))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    application.add_handler(CommandHandler("audio", handle_audio))
    application.add_handler(MessageHandler(filters.PHOTO, handle_multimedia))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_multimedia))
    application.add_handler(CommandHandler("topic", handle_topic))


    # Start the bot in polling mode where the bot will check Telegram servers every few seconds
    # to see if there are any new messages or updates from the user
    application.run_polling()



# Ensures that the main() function only runs when this Python script is run directly
if __name__ == '__main__':
    main()
