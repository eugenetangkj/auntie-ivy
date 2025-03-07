from prompts.topic_1_prompts import TOPIC_1_STAGE_1_INTENT_CLASSIFIER
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array


'''
Properties
'''
current_topic = 1
current_stage = 1
DEFAULT_INTENT = 4


'''
Determines the intent of the user's message

Parameters:
    - user_id: ID of the user

Return:
    - The number indicating the intent of the user's message
'''
def determine_intent(user_id):
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_INTENT_CLASSIFIER,
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
        intent_number = int(message)
        return intent_number
    
    except ValueError:
        # Set default to fourth intent
        return DEFAULT_INTENT