from prompts.topic_3_prompts import TOPIC_3_DEFAULT_KNOWLEDGE, TOPIC_3_STAGE_1_DISCUSSION_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message
from services.helper_functions import convert_list_to_bullet_points


'''
Properties
'''
current_topic = 3
current_stage = 1


'''
Handles the discussion on the benefits and harms of deepfakes.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def handle_discussion(user_id, update):
    # Obtain knowledge
    knowledge_facts_string = convert_list_to_bullet_points(TOPIC_3_DEFAULT_KNOWLEDGE)

    # Prepare discussion handler
    messages = prepare_messages_array(
        prompt=TOPIC_3_STAGE_1_DISCUSSION_PROMPT.format(knowledge_facts_string),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 1)
    message = response

    # Produce the response
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)

