from prompts.topic_2_prompts import TOPIC_2_DEFAULT_KNOWLEDGE, TOPIC_2_STAGE_2_DISCUSSION_PROMPT, TOPIC_2_STAGE_2_TRANSITION_PROMPT_ONE, TOPIC_2_STAGE_2_TRANSITION_PROMPT_TWO
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message
from services.database_manager import updateUserTopicAndStage
from services.helper_functions import convert_list_to_bullet_points


'''
Properties
'''
current_topic = 2
current_stage = 2


'''
Handles the discussion on the deepfake video of DPM Lawrence Wong

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def handle_discussion(user_id, update):
    # Obtain knowledge
    knowledge_facts_string = convert_list_to_bullet_points(TOPIC_2_DEFAULT_KNOWLEDGE)

    # Prepare discussion handler
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_2_DISCUSSION_PROMPT.format(knowledge_facts_string),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response


    # Produce output
    if (message == 'done'):
        # Discussion has ended, move onto the next stage
        updateUserTopicAndStage(user_id, current_topic, current_stage + 1)
        await produce_text_or_voice_message(user_id, TOPIC_2_STAGE_2_TRANSITION_PROMPT_ONE, current_topic, current_stage + 1, update, True)
        await produce_text_or_voice_message(user_id, TOPIC_2_STAGE_2_TRANSITION_PROMPT_TWO, current_topic, current_stage + 1, update, True)
    else:
        # Discussion has not ended, continue discussing about it
        await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)

