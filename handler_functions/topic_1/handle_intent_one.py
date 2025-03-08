from prompts.topic_1_prompts import TOPIC_1_STAGE_1_INTENT_ONE_PROMPT, TOPIC_1_STAGE_1_INTENT_ONE_SUPPORT_PROMPT, TOPIC_1_STAGE_1_INTENT_ONE_SUPPORT_PROMPT_FOLLOW_UP, TOPIC_1_STAGE_1_INTENT_ONE_CONTRADICT_PROMPT
from prompts.topic_1_prompts import TOPIC_1_STAGE_1_NEW_KNOWLEDGE_MESSAGES, TOPIC_1_STAGE_1_INTENT_ONE_NEW_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message
from services.database_manager import fetchKnowledgeWithId, fetchKnowledge, fetchKnowledgeFactUsingId, add_knowledge, add_contradicting_fact
from services.helper_functions import convert_list_to_bullet_points
import ast
import re
import random


'''
Properties
'''
current_topic = 1
current_stage = 1


'''
Handles what to do if the learner provides factual information. The agent responds by comparing the factual
information with its current knowledge base.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def formulate_response_intent_one(user_id, update):
    knowledge_facts_with_id = fetchKnowledgeWithId(user_id, current_topic)
    formatted_knowledge_facts_with_id =  "\n".join([f"ID: {id}, Fact: {fact}" for id, fact in knowledge_facts_with_id])
    
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_PROMPT.format(formatted_knowledge_facts_with_id),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    response_formatted = re.sub(r'\((\d+),\s*([^\)]*)\)', r'(\1, "\2")', response)
    fact_id, fact = ast.literal_eval(response_formatted)

    # Handle cases
    if fact == "support":
        await handle_supporting_fact(user_id, update)
        print("Support")
    elif fact == "contradict":
        await handle_contradicting_fact(user_id, update, fact_id)
        print("Contradict")
    else:
        # New fact
        await handle_new_fact(user_id, update, fact)
        print("New fact")



'''
Helper function to carry out logic if the senior's information supports the agent's existing knowledge.
If so, the agent will affirm what the senior said and follow-up with a question to continue the conversation.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram

Return:
    - No return value
'''
async def handle_supporting_fact(user_id, update):
    # Step 1: Reinforce the supporting fact
    knowledge_facts = fetchKnowledge(user_id, current_topic)
    knowledge_facts_string = convert_list_to_bullet_points(knowledge_facts)

    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_SUPPORT_PROMPT.format(knowledge_facts_string),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response

    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)


    # Step 2: Ask follow-up question to continue the conversation
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_SUPPORT_PROMPT_FOLLOW_UP.format(knowledge_facts_string),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response

    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)


'''
Helper function to carry out logic if the senior's information contradicts the agent's existing knowledge.
If so, the agent will ask the senior if he is sure as it contradicts his information.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram
    - fact_id: ID of the agent's fact that the senior has contradicted.

Return:
    - No return value
'''
async def handle_contradicting_fact(user_id, update, fact_id):
    # Step 1: Add the contradicting fact into the database
    add_contradicting_fact(user_id, fact_id)

    # Step 2: Ask the senior if he is sure about it
    knowledge = fetchKnowledgeFactUsingId(user_id, fact_id)

    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_CONTRADICT_PROMPT.format(knowledge),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)



'''
Helper function to carry out logic if the senior's information is something new and not found within the agent's
existing knowledge. The agent will add the new fact into his knowledge base.

Parameters:
    - user_id: ID of the user
    - update: Update frame from Telegram
    - fact: The new fact to be added

Return:
    - No return value
'''
async def handle_new_fact(user_id, update, fact):
    # Step 1: Add new fact into the knowledge base
    add_knowledge(user_id, [fact])

    # Step 2: Tell the user thanks for sharing the information
    random_message = random.choice(TOPIC_1_STAGE_1_NEW_KNOWLEDGE_MESSAGES)
    await produce_text_or_voice_message(user_id, random_message, current_topic, current_stage, update, True)
    

    # Step 3: Ask a question to follow up
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_NEW_PROMPT.format(fact),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )
    response = generate_text_gpt("gpt-4o", messages, 1)
    message = response
    await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)

