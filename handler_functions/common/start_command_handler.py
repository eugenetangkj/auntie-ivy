from prompts.common_prompts import START_COMMAND_MESSAGE_TOPIC_1, START_COMMAND_MESSAGES_TOPIC_2, START_COMMAND_MESSAGE_TOPIC_3
from telegram import Update
from telegram.ext import CallbackContext
from services.database_manager import check_if_user_exist, add_user, determineUserTopic, updateUserTopicAndStage, add_knowledge, saveMessageToConversationHistory
from prompts.topic_1_prompts import TOPIC_1_STAGE_1_DEFAULT_KNOWLEDGE
from definitions.role import Role

'''
Handler function for /start command where it initiates the conversation, informing
the user what it can do.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_start(update: Update, _: CallbackContext):
    # Obtain user information from Telegram API
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id


    # Check if the user exists in the database.
    if not check_if_user_exist(user_id):
        # User does not exist. Add the user to the database.
        add_user(user_id)
    
    # Send the introduction message depending on the current topic of the bot
    topic, = determineUserTopic(user_id)
    if topic is None or topic >= 4:
        # For some reason, topic cannot be found or it is an invalid topic. Reset the topic to default topic 1 and stage 1
        updateUserTopicAndStage(1, 1)
        topic = 1

    # Set the corresponding introduction messages depending on the current topic
    if topic == 1:
        add_knowledge(user_id, TOPIC_1_STAGE_1_DEFAULT_KNOWLEDGE)
        start_message = START_COMMAND_MESSAGE_TOPIC_1.format(user_name)
        saveMessageToConversationHistory(user_id, Role.SYSTEM, start_message, topic, 1)
        await update.message.reply_text(start_message.format(user_name))

    elif topic == 2:
        #TODO: Handle knowledge


        for start_message in START_COMMAND_MESSAGES_TOPIC_2:
            saveMessageToConversationHistory(user_id, Role.SYSTEM, start_message, topic, 1)
            await update.message.reply_text(start_message.format(user_name))

    elif topic == 3:
        start_message = START_COMMAND_MESSAGE_TOPIC_3 
        saveMessageToConversationHistory(user_id, Role.SYSTEM, start_message, topic, 1) # Always start at stage 1   
        await update.message.reply_text(start_message.format(user_name))
