from services.database_manager import saveMessageToConversationHistory
from telegram import Update
from services.message_manager import produce_text_or_voice_message
from definitions.role import Role
from determine_relevance import determine_if_answer_is_relevant
from intent_classifier import determine_intent


'''
Properties
'''
current_topic = 1
current_stage = 1


'''
Determines how the agent should reply to the user in topic 1 stage 1, which is about discussing
on how a deepfake is created.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_one_stage_one(user_id: int, update: Update, user_message: str):
    # Pass through the AI chain to determine how to handle the response

    # STEP 1: Determine if the user answered something relevant to the conversation
    did_user_give_a_relevant_answer = determine_if_answer_is_relevant(user_id, user_message)
    if not did_user_give_a_relevant_answer:
        # Answer was not relevant or cannot be determined
        # Do not save the current pair of messages, just tell the learner to try again
        await produce_text_or_voice_message(
            user_id,
            "I am sorry but I did not understand that based on the context of the conversation. Let's stick to the conversation.",
            current_topic,
            current_stage,
            update,
            False
        )
        return
    

    # STEP 2: Intent classifier
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)
    intent_number = determine_intent(user_id)


    await update.message.reply_text(str(intent_number), parse_mode="markdown")





    # # Fetch only messages in the current topic and stage
    # messages = prepare_messages_array(
    #     prompt=TOPIC_1_STAGE_1_PROMPT,
    #     user_id=user_id,
    #     lower_bound_topic=current_topic,
    #     lower_bound_stage=current_stage,
    #     upper_bound_topic=current_topic,
    #     upper_bound_stage=current_stage
    # )


    # # Use OpenAI chat completion
    # response = generate_text_gpt("gpt-4o", messages, 0)
    # message = response
   

    # # Output based on whether the user has enabled audio output
    # if (determine_is_audio_enabled(user_id)):
    #     # Case 1: Audio is enabled. We need to output audio message and save the message into the database.
    #     await produce_voice_message(user_id, message, current_topic, current_stage, update)
    # else:
    #     # Case 2: Audio is disabled. We need to output text message and save the message into the database.
    #     await output_and_save_text_message(user_id, message, current_topic, current_stage, update)
