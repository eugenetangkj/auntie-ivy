from prompts.topic_2_prompts import TOPIC_2_STAGE_3_DISCUSSION_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message


'''
Properties
'''
current_topic = 2
current_stage = 3


'''
Handles the discussion on how to spot deepfakes

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def handle_discussion(user_id, update):

    # Prepare discussion handler
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_3_DISCUSSION_PROMPT,
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 1)
    message = response


    # Produce output
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)
