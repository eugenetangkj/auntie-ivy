from telegram import Update
from telegram.ext import CallbackContext
from services.audio_manager import MAX_FILE_SIZE_MB, convert_from_ogg_to_mp3
from services.openai_manager import get_openai_client
import os
from handler_functions.common.freetext_handler import reply_to_user_message
from prompts.common_prompts import VOICE_MESSAGE_TOO_LARGE_ERROR, VOICE_MESSAGE_FORMAT_CONVERSION_ERROR, VOICE_MESSAGE_TRANSCRIPTION_ERROR


'''
Handler function for audio messages that the user sends. It takes the audio messsage,
transcribes it using OpenAI's Whisper model, then executes the same logic as free text handler
by using the transcribed message.

Parameters:
    - update: Update frame from Telegram

Returns:
    No return value
'''
async def handle_voice_message(update: Update, _: CallbackContext):
    # Step 0: Obtain the voice message and user properties
    user_id = update.effective_user.id
    voice = update.message.voice
    file = await voice.get_file()
    file_size = file.file_size / (1024 * 1024)


    # Step 1: Check if file size exceeds maximum limit
    if file_size > MAX_FILE_SIZE_MB:
        await update.message.reply_text(VOICE_MESSAGE_TOO_LARGE_ERROR)
        return


    # Step 2: Download the voice message file temporarily for processing
    temp_file_path = f"temp_files/temp_voice_{voice.file_id}.ogg"
    await file.download_to_drive(temp_file_path)


    # Step 3: Convert to MP3 for model to use later
    mp3_file_path = convert_from_ogg_to_mp3(temp_file_path)
    if not mp3_file_path:
        # Conversion was not successful
        await update.message.reply_text(VOICE_MESSAGE_FORMAT_CONVERSION_ERROR)
        os.remove(temp_file_path)
        return


    # Step 4: Send MP3 into Whisper model
    try:
        # Transcribe using Whisper
        client = get_openai_client()
        audio_file = open(mp3_file_path, "rb")
        transcribed_message = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language="en"
        )
        print(transcribed_message)

        # Let the bot process the user's message
        await reply_to_user_message(update, user_id, transcribed_message)

    except Exception as e:
        # Got problem transcribing with Whisper
        print(e)
        await update.message.reply_text(VOICE_MESSAGE_TRANSCRIPTION_ERROR)
       
    finally:
        # Cleanup by closing and removing the files
        audio_file.close()
        os.remove(temp_file_path)
        os.remove(mp3_file_path)