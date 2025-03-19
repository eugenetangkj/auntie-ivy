from prompts.topic_3_prompts import TOPIC_3_STAGE_1_RELEVANCE_PROMPT
from services.openai_manager import generate_text_gpt
from services.database_manager import fetchLatestMessage

'''
Properties
'''
current_topic = 3
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
    previous_message = fetchLatestMessage(user_id, current_topic, current_stage, current_topic, current_stage)


    # Generate the prompt
    prompt = TOPIC_3_STAGE_1_RELEVANCE_PROMPT.format(previous_message, user_message)
    messages = [
        {
            "role": "developer",
            "content": prompt
        }
    ]

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response
    is_answer_relevant = {'true': True, 'false': False}.get(message.lower())
    print("Is answer relevant: ", is_answer_relevant)
    return is_answer_relevant