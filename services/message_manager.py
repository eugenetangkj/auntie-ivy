from services.database_manager import saveMessageToConversationHistory
from definitions.role import Role
from services.openai_manager import generate_speech_whisper, AUDIO_WHISPER_PATH
from services.database_manager import fetchConversationHistory
from prompts.common_prompts import AUDIO_PRODUCTION_ERROR
import os



'''
Prepare the array of messages to put into chat completion API.

Parameters:
    - prompt: Prompt to be given
    - user_id: ID of the user
    - lower_bound_topic: Topic of the lower bound to fetch conversation history from
    - lower_bound_stage: Stage of the lower bound to fetch conversation history from
    - upper_bound_topic: Topic of the upper bound to fetch conversation history from
    - upper_bound_stage: Substage of the upper bound to fetch conversation history from

    
Return value:
    - messages: List of messages which includes the prompt and the conversation history.
'''
def prepare_messages_array(prompt, user_id, lower_bound_topic, lower_bound_stage, upper_bound_topic, upper_bound_stage):
    # Generate the developer prompt
    messages = [
        {
            "role": "developer",
            "content": prompt
        }
    ]

    # Fetch conversation history from the database
    # Fetch all messages within the specified stages
    conversation_history = fetchConversationHistory(
        user_id,
        lower_bound_topic,
        lower_bound_stage,
        upper_bound_topic,
        upper_bound_stage)
    formatted_conversation_history = [{"role": role, "content": message} for role, message in conversation_history]


    # Combine into a single messages list
    messages.extend(formatted_conversation_history)

    # Return the list of messages
    return messages


'''
Outputs a text message and saves it into the database.

Parameters:
    - user_id: ID of the user
    - message: Message to output and save
    - current_topic: Topic to save the message
    - current_stage: Stage to save the message
    - update: Update frame from Telegram
'''
async def output_and_save_text_message(user_id, message, current_topic, current_stage, update):
    await update.message.reply_text(message, parse_mode="markdown")
    saveMessageToConversationHistory(user_id, Role.SYSTEM, message, current_topic, current_stage)


'''
Produce a voice message for the given text message. If it does not work,
produce a text message instead.

Then, save the message into the database.

Parameters:
    - user_id: ID of the user
    - message: Message to output and save
    - current_topic: Topic to save the message
    - current_stage: Stage to save the message
    - update: Update frame from Telegram
'''
async def produce_voice_message(user_id, message, current_topic, current_stage, update):
    audio_file_path = generate_speech_whisper(message)
    if audio_file_path is not None:
        # Successful audio production so we send the voice message to the user.
        voice_file = open(audio_file_path, "rb")
        await update.message.reply_voice(voice=voice_file)
        voice_file.close()
            
        # Delete audio files that are created
        os.remove(audio_file_path)
        os.remove(AUDIO_WHISPER_PATH)
        
    else:
        # Cannot product audio. Show error message to the user.
        await update.message.reply_text(AUDIO_PRODUCTION_ERROR)
        await update.message.reply_text(message, parse_mode="markdown")

        # Delete audio files that are created
        os.remove(AUDIO_WHISPER_PATH)
    
    # Save message
    saveMessageToConversationHistory(user_id, Role.SYSTEM, message, current_topic, current_stage)
