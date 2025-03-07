from prompts.topic_1_prompts import TOPIC_1_STAGE_1_INTENT_ONE_PROMPT, TOPIC_1_STAGE_1_INTENT_ONE_SUPPORT_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array, produce_text_or_voice_message
from services.database_manager import fetchKnowledgeWithId, fetchKnowledge
from services.helper_functions import convert_list_to_bullet_points
import ast
import re


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
    knowledge_facts_with_id = fetchKnowledgeWithId(user_id)
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
    response_formatted = re.sub(r'\((\d+),\s*(.*)\)', r'(\1, "\2")', response)
    fact_id, fact = ast.literal_eval(response_formatted)

    # Handle cases
    if fact == "support":
        await handle_supporting_fact(user_id, update)
        print("Support")
    elif fact == "contradict":
        print("Contradict")
    else:
        # New fact
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
    knowledge_facts = fetchKnowledge(user_id)
    knowledge_facts_string = convert_list_to_bullet_points(knowledge_facts)

    
    
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_ONE_SUPPORT_PROMPT.format(knowledge_facts_string),
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

