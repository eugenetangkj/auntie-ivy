from prompts.topic_1_prompts import TOPIC_1_STAGE_1_RELEVANCE_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array


'''
Properties
'''
current_topic = 1
current_stage = 1


'''
Determines if the user has given a relevant answer based on the current conversation state.

Parameters:
    - user_id: ID of the user
    - user_message: User message that the user has just given.

Return:
    - True if the user has given a relevant answer, else returns False
'''
def determine_if_answer_is_relevant(user_id, user_message):
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_RELEVANCE_PROMPT.format(user_message),
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response

    is_answer_relevant = {'true': True, 'false': False}.get(message.lower())
    return is_answer_relevant