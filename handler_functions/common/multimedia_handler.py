from prompts.common_prompts import MULTIMEDIA_NOT_SUPPORTED_MESSAGE
from telegram import Update
from telegram.ext import CallbackContext


'''
Handler function for sending multimedia files which include images and documents

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_multimedia(update: Update, _: CallbackContext):

    # Tell user that multimedia is not supported
    await update.message.reply_text(MULTIMEDIA_NOT_SUPPORTED_MESSAGE)
