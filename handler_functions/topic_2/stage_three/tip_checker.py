from prompts.topic_2_prompts import TOPIC_2_STAGE_2_CHECK_TIP_EXIST_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array
from services.helper_functions import convert_list_to_bullet_points
from services.database_manager import fetchKnowledge

'''
Properties
'''
current_topic = 2
current_stage = 3


'''
Determines whether a given tip is already found in the agent's existing knowledge.

Parameters:
    - user_id: ID of the user
    - tip: Tip to check

Return:
    - 'support' if the tip exists, else 'new'.
'''
def check_tip_in_knowledge_base(user_id, tip):
    # Obtain knowledge
    knowledge_facts = fetchKnowledge(user_id, current_topic)
    knowledge_facts_string = convert_list_to_bullet_points(knowledge_facts)

    # Prepare tip knowledge checker
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_2_CHECK_TIP_EXIST_PROMPT.format(tip, knowledge_facts_string),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response
    return message
