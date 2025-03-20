'''
PERSONA PROMPTS
'''
# Persona that is repeated across prompts
PERSONA_PROMPT =  (
'''
Your name is Ivy. You are a 65-year-old retired senior living in Singapore. You are interested to learn more
about AI after hearing it mentioned frequently around you. Currently, you are learning about deepfakes. However,
you just started learning and thus, you may need some guidance along the way.

Also, you type in a formal manner. AVOID using exclamation marks and use full stops instead.
'''
)


'''
START command messages
'''
# Start message for topic 1
START_COMMAND_MESSAGE_TOPIC_1 = (
    "Hi {}. I am Auntie Ivy. I am also a senior learning about deepfakes today. I am trying to understand how deepfakes are created. Can you help explain it to me?"
)

# Start messages for topic 2
START_COMMAND_MESSAGES_TOPIC_2 = (
    "Hi. It's Auntie Ivy. I want to share something with you.",
    "Have you seen this before?\n\nhttps://www.youtube.com/watch?v=0dTmRCHdXT8",
    "What do you think of the video?"
)

# Start messages for topic 3
START_COMMAND_MESSAGE_TOPIC_3_ONE = "Hi {}. Auntie Ivy here. Let's discuss about the benefits and harms of deepfakes."
START_COMMAND_MESSAGE_TOPIC_3_TWO = "Do you think deepfakes is something beneficial or harmful to us?"



'''
DELETE command messages
'''
# Delete command message that informs the user that the user data has been deleted from the database
DELETE_COMMAND_MESSAGE = (
    "User data and all associated conversation history have been successfully deleted."
)



'''
AUDIO AND MULTIMEDIA PROMPTS
'''
# Audio production error
AUDIO_PRODUCTION_ERROR = "Sorry, I am not able to produce voice messages at this moment."

# Voice message too large error, occurs when user tries to submit a voice message input that is too large
VOICE_MESSAGE_TOO_LARGE_ERROR = "Sorry, the voice message file is too large. Can you try with a smaller voice message file?"

# Cannot convert voice message from OGG to MP3 format
VOICE_MESSAGE_FORMAT_CONVERSION_ERROR = "Sorry, the voice message cannot be converted. Can you try again?"
VOICE_MESSAGE_TRANSCRIPTION_ERROR = "Sorry, I could not understand what you have said. Can you try again?"

# Multimedia not supported message
MULTIMEDIA_NOT_SUPPORTED_MESSAGE = "Sorry, I can only accept text and voice messages at the moment."

# Messages for toggling audio mode
AUDIO_MODE_ENABLED_MESSAGE = "Audio mode is enabled. I will now reply using voice messages."
AUDIO_MODE_DISABLED_MESSAGE = "Audio mode is disabled. I will now reply with text messages."
CREATE_USER_FOR_AUDIO_MODE = "Please run `/start` before toggling the audio mode."


'''
OTHER MESSAGES
'''
# Prompt if user enters free text but cannot find the user's data in the database
REQUEST_TO_DELETE_MESSAGE = (
    "Sorry, something went wrong. Please type /start to begin again."
)
