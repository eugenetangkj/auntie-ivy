from prompts.common_prompts import AUDIO_MODE_ENABLED_MESSAGE, AUDIO_MODE_DISABLED_MESSAGE, CREATE_USER_FOR_AUDIO_MODE
from telegram import Update
from telegram.ext import CallbackContext
from services.database_manager import check_if_user_exist, determine_is_audio_enabled, set_is_audio_enabled


'''
Handler function for /audio command where it toggles the value of is_audio_enabled
for the current user in the users database.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_audio(update: Update, _: CallbackContext):
    # Obtain user information from Telegram API
    user_id = update.effective_user.id

    if check_if_user_exist(user_id):
        # User exist

        # Step 1: Check if audio mode is currently enabled
        is_audio_enabled = determine_is_audio_enabled(user_id)

        # Step 2: Toggle and save the value of is audio enabled
        new_is_audio_enabled = not is_audio_enabled
        set_is_audio_enabled(user_id, new_is_audio_enabled)


        # Step 3: Inform the user
        if (new_is_audio_enabled):
            # Current audio is enabled
            await update.message.reply_text(AUDIO_MODE_ENABLED_MESSAGE)
        else:
            # Current audio is disabled
            await update.message.reply_text(AUDIO_MODE_DISABLED_MESSAGE)
    else:
        # User does not exist yet
        await update.message.reply_text(CREATE_USER_FOR_AUDIO_MODE, parse_mode="markdown")
