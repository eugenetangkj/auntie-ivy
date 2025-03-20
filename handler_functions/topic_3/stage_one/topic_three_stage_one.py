from telegram import Update
from services.message_manager import produce_text_or_voice_message
from services.database_manager import saveMessageToConversationHistory
from handler_functions.topic_3.stage_one.determine_relevance import determine_if_answer_is_relevant
from handler_functions.topic_3.stage_one.discussion_handler import handle_discussion
from definitions.role import Role

'''
Properties
'''
current_topic = 3
current_stage = 1


'''
Determines how the agent should reply to the user in topic 3 stage 1 which is discussing the harms and benefits
of deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_three_stage_one(user_id: int, update: Update, user_message: str):
    # Step 1: Determine if the user's message is relevant to the current conversation history
    is_message_relevant = determine_if_answer_is_relevant(user_id, user_message)

    # Step 2: Tell the user that the answer is irrelevant
    if (not is_message_relevant):
        await produce_text_or_voice_message(
            user_id,
            "I am sorry but I did not understand that based on the context of the conversation. Let's stick to the conversation.",
            current_topic,
            current_stage,
            update,
            False
        )
        return

    # Step 3: Answer is relevant. We save the answer first
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)
  
    # Step 4: We engage the discussion mode.
    await handle_discussion(user_id, update)
