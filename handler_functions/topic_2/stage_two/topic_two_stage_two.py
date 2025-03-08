from services.database_manager import saveMessageToConversationHistory, updateUserTopicAndStage, add_knowledge
from telegram import Update
from services.message_manager import produce_text_or_voice_message, prepare_messages_array
from services.openai_manager import generate_text_gpt
from definitions.role import Role
from handler_functions.topic_2.stage_two.relevance_classifier import determine_relevance
from handler_functions.topic_2.stage_two.message_analyser import analyse_message
from handler_functions.topic_2.stage_two.tip_checker import check_tip_in_knowledge_base
from handler_functions.topic_2.stage_two.discussion_handler import handle_discussion

'''
Properties
'''
current_topic = 2
current_stage = 2


'''
Determines how the agent should reply to the user in Topic 2 Stage 2, which is about discussing
how to spot signs of deepfake regarding the deepfake video on DPM Lawrence Wong

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_two_stage_two(user_id: int, update: Update, user_message: str):
    # STEP 1: Save the user message
    saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage)


    # STEP 1: Determine relevance
    intent = determine_relevance(user_id)
    print("Relevance: ", intent)
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
        print(fact_status)
        if (fact_status == 'new'):
            # Add to the knowledge base as it is absent
            add_knowledge(user_id, [analysed_message], current_topic)
    

    # STEP 5: Continue discussion on how to spot deepfakes
    await handle_discussion(user_id, update)


















    # STEP 2: Determine if the type of response: (Irrelevant, ''), ('New Way of Spotting', 'Way'), ('General', 'Discussion')
    # Or can use (1, string) like this


    # STEP 3: Handle irrelevant case


    # STEP 4: If it is a new way, add to the knowledge base




    # STEP 5: If it is just a general discussion case, we continue the discussion as per normal



    # STEP 6: Check if the conversation for this topic has ended. If so, we need to advance to the next phase


    # # STEP 2: Ask the learner about his opinion
    # messages = prepare_messages_array(
    #     prompt=TOPIC_2_STAGE_1_PROMPT,
    #     user_id=user_id,
    #     lower_bound_topic=current_topic,
    #     lower_bound_stage=current_stage,
    #     upper_bound_topic=current_topic,
    #     upper_bound_stage=current_stage
    # )
    # response = generate_text_gpt("gpt-4o", messages, 0)
    # message = response
    

    # # CASE 1: Irrelevant reply
    # if message == "irrelevant":
    #     await produce_text_or_voice_message(
    #         user_id,
    #         "I am sorry but I did not understand that based on the context of the conversation. Let's stick to the conversation.",
    #         current_topic,
    #         current_stage,
    #         update,
    #         False
    #     )
    # else:
    #     # CASE 2: Relevant reply
    #     await produce_text_or_voice_message(user_id, message, current_topic, current_stage, update, True)
    #     updateUserTopicAndStage(user_id, current_topic, current_stage + 1)
