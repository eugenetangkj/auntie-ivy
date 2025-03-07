from prompts.topic_1_prompts import TOPIC_1_STAGE_1_INTENT_FOUR_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message
from services.helper_functions import convert_list_to_bullet_points
from services.database_manager import fetchKnowledge


'''
Properties
'''
current_topic = 1
current_stage = 1


'''
Handles what to do if the intent does not fall into any of the specified intents. The agent tries to formulate
a response based on its current knowledge to keep the conversation going.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def formulate_response_intent_four(user_id, update):
    knowledge_facts = fetchKnowledge(user_id)
    knowledge_facts_string = convert_list_to_bullet_points(knowledge_facts)

    
    
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_FOUR_PROMPT.format(knowledge_facts_string),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response


    # Produce output and save to the database
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)

