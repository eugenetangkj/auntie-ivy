from services.database_manager import saveMessageToConversationHistory, updateUserTopicAndStage
from telegram import Update
from services.message_manager import produce_text_or_voice_message, prepare_messages_array
from services.openai_manager import generate_text_gpt
from definitions.role import Role
from prompts.topic_2_prompts import TOPIC_2_STAGE_1_PROMPT

'''
Properties
'''
current_topic = 2
current_stage = 1


'''
Determines how the agent should reply to the user in Topic 2 Stage 1, which is about discussing
the deepfake video on DPM Lawrence Wong and linking it to the topic of how to spot deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_two_stage_one(user_id: int, update: Update, user_message: str):
    # STEP 1: Save the user message
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)


    # STEP 2: Ask the learner about his opinion
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_1_PROMPT,
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response
    

    # CASE 1: Irrelevant reply
    if message == "irrelevant":
        await produce_text_or_voice_message(
            user_id,
            "I am sorry but I did not understand that based on the context of the conversation. Let's stick to the conversation.",
            current_topic,
            current_stage,
            update,
            False
        )
    else:
        # CASE 2: Relevant reply
        await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)
        updateUserTopicAndStage(user_id, current_topic, current_stage + 1)
