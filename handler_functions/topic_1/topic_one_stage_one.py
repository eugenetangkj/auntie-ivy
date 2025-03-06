from prompts.topic_1_prompts import TOPIC_1_STAGE_1_PROMPT
from services.openai_manager import generate_text_gpt
from services.database_manager import determine_is_audio_enabled
from telegram import Update
from services.message_manager import prepare_messages_array, produce_voice_message, output_and_save_text_message


'''
Properties
'''
current_topic = 1
current_stage = 1


'''
Determines how the chatbot should reply to the user in topic 1 stage 1, which is about replying to
the user's questions on how a deepfake is created.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram

Returns:
    - No return value
'''
async def handle_topic_one_stage_one(user_id: int, update: Update):
    # Fetch only messages in the current topic and stage
    messages = prepare_messages_array(
        prompt=TOPIC_1_STAGE_1_PROMPT,
        user_id=user_id,
        lower_bound_topic=current_topic,
        lower_bound_stage=current_stage,
        upper_bound_topic=current_topic,
        upper_bound_stage=current_stage
    )


    # Use OpenAI chat completion
    response = generate_text_gpt("gpt-4o", messages, 0)
    message = response
   

    # Output based on whether the user has enabled audio output
    if (determine_is_audio_enabled(user_id)):
        # Case 1: Audio is enabled. We need to output audio message and save the message into the database.
        await produce_voice_message(user_id, message, current_topic, current_stage, update)
    else:
        # Case 2: Audio is disabled. We need to output text message and save the message into the database.
        await output_and_save_text_message(user_id, message, current_topic, current_stage, update)
