from telegram import Update
from telegram.ext import CallbackContext
from services.database_manager import updateUserTopicAndStage, determineUserTopic, updateUserStance
from definitions.topics import MIN_TOPIC, MAX_TOPIC, TOPIC_NAMES

'''
Handler function for /topic command where it allows the user to change the topic of the bot.
When the user changes a topic, we reset the stage to 1 for that topic.

Parameters:
    - update: Update frame from Telegram
    - context: The CallbackContext from Telegram

Returns:
    No return value
'''
async def handle_topic(update: Update, context: CallbackContext):
    # Obtain user id
    user_id = update.effective_user.id
    # Check if an argument is provided
    if context.args:
        try:
            # Extract the number from the command argument
            topic_num = int(context.args[0])
            user_current_topic = determineUserTopic(user_id)

            # Determine if topic number is a valid topic number
            if (topic_num == user_current_topic):
                await update.message.reply_text("You are already in Topic {}.".format(topic_num))
            elif (topic_num >= MIN_TOPIC and topic_num <= MAX_TOPIC):
                updateUserTopicAndStage(user_id, topic_num, 1)
                updateUserStance(user_id, '')
                await update.message.reply_text("Topic has been changed to Topic {}: {}".format(topic_num, TOPIC_NAMES[topic_num]))
                await update.message.reply_text("Please run the `/start` command.")
            else:
                await update.message.reply_text("Please select a valid topic number in [{}, {}].".format(MIN_TOPIC, MAX_TOPIC))

        except ValueError:
            # Invalid topic number
            await update.message.reply_text("Please provide a valid number after /topic.")
    else:
        # No topic number was provided
        await update.message.reply_text("Please provide a valid number after /topic. For example, /topic 2.")
