from services.database_manager import saveMessageToConversationHistory, add_knowledge
from telegram import Update
from services.message_manager import produce_text_or_voice_message
from definitions.role import Role
from handler_functions.topic_2.stage_two.relevance_classifier import determine_relevance
from handler_functions.topic_2.stage_two.message_analyser import analyse_message
from handler_functions.topic_2.stage_two.tip_checker import check_tip_in_knowledge_base
from handler_functions.topic_2.stage_two.discussion_handler import handle_discussion

'''
Properties
'''
current_topic = 2
current_stage = 3


'''
Determines how the agent should reply to the user in Topic 2 Stage 3, which is about a general
discussion on how to spot deepfakes.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_two_stage_three(user_id: int, update: Update, user_message: str):
    # STEP 1: Save the user message
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)


    # STEP 1: Determine relevance
    intent = determine_relevance(user_id)
    if (intent == 1):
        # Not relevant
        await produce_text_or_voice_message(
            user_id,
            "I am sorry but I did not understand that based on the context of the conversation. Let's stick to the conversation.",
            current_topic,
            current_stage,
            update,
            False
        )
        return
    

    # STEP 2: Message is relevant, we save it to the conversation history
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)


    # STEP 3: Analyse the message to determine if it is related to a way of spotting deepfakes
    analysed_message = analyse_message(user_id, user_message)


    # STEP 4:
    if (analysed_message.lower() != 'discussion'):
        # It is a tip on spotting deepfakes
        fact_status = check_tip_in_knowledge_base(user_id, analysed_message)

        if (fact_status == 'new'):
            # Add to the knowledge base as it is absent
            add_knowledge(user_id, [analysed_message], current_topic)
    

    # STEP 5: Continue discussion on how to spot deepfakes
    await handle_discussion(user_id, update)
