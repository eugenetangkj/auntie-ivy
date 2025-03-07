from services.database_manager import saveMessageToConversationHistory
from telegram import Update
from services.message_manager import produce_text_or_voice_message
from definitions.role import Role
from handler_functions.topic_1.determine_relevance import determine_if_answer_is_relevant
from handler_functions.topic_1.intent_classifier import determine_intent
from handler_functions.topic_1.handle_intent_one import formulate_response_intent_one
from handler_functions.topic_1.handle_intent_two import formulate_response_intent_two
from handler_functions.topic_1.handle_intent_three import formulate_response_intent_three
from handler_functions.topic_1.handle_intent_four import formulate_response_intent_four


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


    if (intent_number == 1):
        print(1)
        await formulate_response_intent_one(user_id, update)
    elif (intent_number == 2):
        print(2)
        await formulate_response_intent_two(user_id, update)
    elif (intent_number == 3):
        print(3)
        await formulate_response_intent_three(user_id, update)
    else:
        print(4)
        await formulate_response_intent_four(user_id, update)
