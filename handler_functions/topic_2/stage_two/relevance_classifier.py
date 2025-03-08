from prompts.topic_2_prompts import TOPIC_2_STAGE_2_RELEVANCE_CLASSIFIER_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array


'''
Properties
'''
current_topic = 2
current_stage = 2
DEFAULT_RELEVANCE = 1


'''
Determines the relevance of the user's message

Parameters:
    - user_id: ID of the user

Return:
    - 1 if it is irrelevant to the current conversation, else return 2
'''
def determine_relevance(user_id):
   
    # Prepare relevance classifier
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_2_RELEVANCE_CLASSIFIER_PROMPT,
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )

    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response

    try:
        relevance_number = int(message)
        return relevance_number
    
    except ValueError:
        # Set default to fourth intent
        return DEFAULT_RELEVANCE
