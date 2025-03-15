from services.database_manager import saveMessageToConversationHistory, fetchConversationHistory, updateUserTopicAndStage
from telegram import Update
from services.message_manager import produce_text_or_voice_message, prepare_messages_array
from services.openai_manager import generate_text_gpt
from definitions.role import Role
from prompts.topic_3_prompts import TOPIC_3_STAGE_1_PROMPT, TOPIC_3_STAGE_1_PROMPT_CONCLUDING, TOPIC_3_STAGE_2_MESSAGES


'''
Properties
'''
current_topic = 3
current_stage = 1
number_of_messages_before_transition = 10


'''
Determines how the agent should reply to the user in topic 3 stage 2, which is about discussing
how deepfakes is bad for fake news.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_three_stage_one(user_id: int, update: Update, user_message: str):
    # Save the user's response
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)

    # Check how many messages are there already
    number_of_messages = len(fetchConversationHistory(user_id, current_topic, current_stage, current_topic, current_stage))
    if (number_of_messages >= number_of_messages_before_transition):
        # Conclude and move onto the next topic

        # STEP 1: Prepare a transition message
        messages = prepare_messages_array(
            prompt=TOPIC_3_STAGE_1_PROMPT_CONCLUDING,
            user_id=user_id,
            lower_bound_topic=current_topic,
            lower_bound_stage=current_stage,
            upper_bound_topic=current_topic,
            upper_bound_stage=current_stage
        )
        response = generate_text_gpt("gpt-4o", messages, 1)
        message = response
        await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)

        # STEP 2: Output the hard-coded messages to discuss about the next topic
        for message in TOPIC_3_STAGE_2_MESSAGES:
            saveMessageToConversationHistory(user_id, Role.SYSTEM, message, current_topic, current_stage + 1)
            await update.message.reply_text(message)
        
        # STEP 3: Update the user topic and substage
        updateUserTopicAndStage(user_id, current_topic, current_stage + 1)

    else:
        # Continue talking about the current topic
        messages = prepare_messages_array(
            prompt=TOPIC_3_STAGE_1_PROMPT,
            user_id=user_id,
            lower_bound_topic=current_topic,
            lower_bound_stage=current_stage,
            upper_bound_topic=current_topic,
            upper_bound_stage=current_stage
        )
        response = generate_text_gpt("gpt-4o", messages, 1)
        message = response

        # Produce response
        await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)
