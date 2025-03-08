from prompts.topic_2_prompts import TOPIC_2_STAGE_2_MESSAGE_ANALYSER_PROMPT
from services.openai_manager import generate_text_gpt
from services.message_manager import prepare_messages_array


'''
Properties
'''
current_topic = 2
current_stage = 3


'''
Analyses whether the user's message might be related to a way of spotting deepfakes

Parameters:
    - user_id: ID of the user
    - user_message: Latest message from the user

Return:
    - A paraphrased sentence of a tip in spotting deepfakes that is implied by the user,
      else returns the user's original message if it is not related to a way of spotting deepfakes
'''
def analyse_message(user_id, user_message):
    # Prepare message analyser
    messages = prepare_messages_array(
        prompt=TOPIC_2_STAGE_2_MESSAGE_ANALYSER_PROMPT.format(user_message),
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
