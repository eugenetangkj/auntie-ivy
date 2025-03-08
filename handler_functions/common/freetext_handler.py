from prompts.common_prompts import REQUEST_TO_DELETE_MESSAGE
from telegram import Update
from telegram.ext import CallbackContext
from services.database_manager import determineUserTopicAndStage, saveMessageToConversationHistory
from handler_functions.topic_1.topic_one_stage_one import handle_topic_one_stage_one
from handler_functions.topic_2.stage_one.topic_two_stage_one import handle_topic_two_stage_one
from handler_functions.topic_2.stage_two.topic_two_stage_two import handle_topic_two_stage_two

'''
Handler function for free text messages that the user sends. It determines which topic
and which stage the user is in to determine how the agent should reply.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_free_text(update: Update, _: CallbackContext):
    # Obtain user information from Telegram API
    user_id = update.effective_user.id
    user_message = update.message.text

    # Process user message
    await reply_to_user_message(update, user_id, user_message)


'''
Determines how the agent will reply depending on the current topic and stage that the user is in. This is
the common function to be called for both voice message and free text handlers.

Parameters:
    - update: Update frame from Telegram
    - user_message: User message that the bot needs to reply to
    - user_id: ID of the user
'''
async def reply_to_user_message(update: Update, user_id: int, user_message: str):
    # Step 1: Determine the current topic and substage that the user is in
    current_topic, current_stage = determineUserTopicAndStage(user_id)
    

    # Step 2: Handle case where user is not actually registered in the database yet
    if (current_topic is None or current_stage is None):
        await update.message.reply_text(REQUEST_TO_DELETE_MESSAGE)
        return
    

    if (current_topic == 1):
        # TOPIC 1: How is a deepfake created
        await handle_topic_one_stage_one(user_id, update, user_message)
    elif (current_topic == 2):
        # TOPIC 2: How to spot deepfakes
        if (current_stage == 1):
            await handle_topic_two_stage_one(user_id, update, user_message)
        elif (current_stage == 2):
            await handle_topic_two_stage_two(user_id, update, user_message)
        else:
            print("TODO for stage 2")
    else:
        await update.message.reply_text("We are still constructing this part of the conversational flow.")
