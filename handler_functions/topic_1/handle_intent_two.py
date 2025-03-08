from prompts.topic_1_prompts import TOPIC_1_STAGE_1_INTENT_TWO_PROMPT_ONE, TOPIC_1_STAGE_1_INTENT_TWO_MESSAGES, TOPIC_1_STAGE_1_INTENT_ONE_NEW_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message
from services.database_manager import updateKnowledgeFactUsingId, retrieve_id_of_contradicting_fact, remove_contradicting_facts_for_user
import random


'''
Properties
'''
current_topic = 1
current_stage = 1


'''
Handles what to do if the learner is affirming that his knowledge is correct. The agent updates the new information in his
knowledge base, removing the original old fact.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def formulate_response_intent_two(user_id, update):
    # STEP 1: Read conversation history to know which is the new fact
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_TWO_PROMPT_ONE,
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 0)
    new_fact = response


    # STEP 2: Update the fact in the knowledge table
    id_of_contradicting_fact = retrieve_id_of_contradicting_fact(user_id)
    if (id_of_contradicting_fact is None):
        return
    updateKnowledgeFactUsingId(user_id, id_of_contradicting_fact, new_fact)
    
    # STEP 3: Remove entry in contradicting_facts table
    remove_contradicting_facts_for_user(user_id)
    
    # STEP 4: Follow-up with an acknowledgement message
    random_message = random.choice(TOPIC_1_STAGE_1_INTENT_TWO_MESSAGES)
    await produce_text_or_voice_message(user_id, random_message, current_topic, current_stage, update, True)

    # STEP 5: Continue the conversation
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_NEW_PROMPT.format(new_fact),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 1)
    message = response
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)

