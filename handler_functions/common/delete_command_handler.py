from prompts.common_prompts import DELETE_COMMAND_MESSAGE
from services.database_manager import delete_user
from telegram import Update
from telegram.ext import CallbackContext


'''
Handler function for /delete command where it deletes the current user from
the database, being equivalent to a reset of the user's conversation history with
the bot.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_delete(update: Update, _: CallbackContext):
    # Obtain user information from Telegram API
    user_id = update.effective_user.id

    # Delete user
    delete_user(user_id)

    # Inform the user
    await update.message.reply_text(DELETE_COMMAND_MESSAGE)
       
  
