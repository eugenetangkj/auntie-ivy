from services.database_manager import updateUserStance, saveMessageToConversationHistory, updateUserTopicAndStage
from telegram import Update
from services.message_manager import produce_text_or_voice_message, prepare_messages_array
from services.openai_manager import generate_text_gpt
from definitions.role import Role
from prompts.topic_3_prompts import TOPIC_3_STAGE_4_DETERMINE_STANCE, TOPIC_3_STAGE_2_CLARIFICATION_MESSAGE, TOPIC_3_STAGE_5_PROMPT


'''
Properties
'''
current_topic = 3
current_stage = 4


'''
Determines the learner's stance on whether using deepfakes in grief management
is good or bad.

Parameters:
    - user_id: User id of the user
    - update: Update frame from Telegram
    - user_message: User message sent from the user

Returns:
    - No return value
'''
async def handle_topic_three_stage_four(user_id: int, update: Update, user_message: str):
    # STEP 1: Determine the learner's stance
    messages = prepare_messages_array(
            prompt=TOPIC_3_STAGE_4_DETERMINE_STANCE.format(user_message),
            user_id=user_id,
            lower_bound_topic=current_topic + 1, # Do not want to fetch any conversation history
            lower_bound_stage=current_stage,
            upper_bound_topic=current_topic + 1,
            upper_bound_stage=current_stage
        )
    response = generate_text_gpt("gpt-4o", messages, 1)
    message = response


    # STEP 2: Handle cases
    if (message == 'good' or message == 'bad'):
        # Step 1: Process learner's stance
        updateUserStance(user_id, message)
        saveMessageToConversationHistory(user_id, Role.USER, user_message, current_topic, current_stage + 1)
        updateUserTopicAndStage(user_id, current_topic, current_stage + 1)

        # Step 2: Respond to the learner's message
        agent_stance = 'bad' if message == 'good' else 'bad' # We want opposing
        messages = prepare_messages_array(
            prompt=TOPIC_3_STAGE_5_PROMPT.format(agent_stance),
            user_id=user_id,
            lower_bound_topic=current_topic,
            lower_bound_stage=current_stage - 1,
            upper_bound_topic=current_topic,
            upper_bound_stage=current_stage + 1
        )
        response = generate_text_gpt("gpt-4o", messages, 1)
        message = response
        await produce_text_or_voice_message(user_id, message, current_topic, current_stage + 1, update, True)

    else:
        # Tell learner to be clearer on his stance
        await produce_text_or_voice_message(user_id, TOPIC_3_STAGE_2_CLARIFICATION_MESSAGE, current_topic, current_stage, update, False)
