from services.database_manager import saveMessageToConversationHistory, fetchConversationHistory, updateUserTopicAndStage, fetchUserStance
from telegram import Update
from services.message_manager import produce_text_or_voice_message, prepare_messages_array
from services.openai_manager import generate_text_gpt
from definitions.role import Role
from prompts.topic_3_prompts import TOPIC_3_STAGE_5_PROMPT


'''
Properties
'''
current_topic = 3
current_stage = 5


'''
Determines how the agent should reply to the user in topic 3 stage 5, which is about discussing
deepfakes usage in grief management.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_three_stage_five(user_id: int, update: Update, user_message: str):
    # Save the user's response
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)


    # Continue talking about the current topic
    agent_stance = 'bad' if fetchUserStance(user_id) == 'good' else 'bad'
    messages = prepare_messages_array(
        prompt=TOPIC_3_STAGE_5_PROMPT.format(agent_stance),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage - 1,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 1)
    message = response

    # Produce response
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)
