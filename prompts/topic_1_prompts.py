from prompts.common_prompts import PERSONA_PROMPT


'''
TOPIC 1 STAGE 1 KNOWLEDGE:
The default knowledge that the peer agent has about how deepfakes are created.
'''
TOPIC_1_STAGE_1_DEFAULT_KNOWLEDGE = [
    # Basic knowledge and facts that revolve around data collection and identifying patterns
    "Deepfakes are videos or images that use AI to replace someone's face or voice with another person's.",
    "I think to create a good deepfake, the AI needs a lot of images and videos of the person.",
    "The AI will use the images and videos of the person to find a suitable one with the correct expression to replace the face in the image or video.",

    # Some incorrect facts
    "We need a lot of time to make deepfakes.",
    "Probably only those who are knowledgeable in AI can create them.",
]

'''
TOPIC 1 STAGE 1:
Peer discusses with the learner about how are deepfakes created.
'''
TOPIC_1_STAGE_1_RELEVANCE_PROMPT = (
'''
You are talking to a senior via Telegram. The senior has just given a reply. Determine if the reply makes sense and logically fits with the previous message
in the conversation history.

A reply can be considered reasonable even if it expresses uncertainty or a lack of knowledge, such as saying "I'm not sure about it." or "I don't know."
It doesn't have to provide new information, but it should be a natural response to what was said before.

For example:
- If the previous message is "Can you help explain how deepfakes are created?" and the reply is "I'm not sure about it," output 'true'.
- If the reply is something unrelated like "The sky is blue today," output 'false'.

If the reply makes sense, output 'true'. If it seems unrelated or out of place, output 'false'.

The senior's reply is: {}
'''
)

TOPIC_1_STAGE_1_INTENT_CLASSIFIER = (
'''
You are talking to a senior via Telegram. Look at the conversation history and focus on the last message provided by the senior.
Your task is to identify the intent of this last message.

Classify the intent into one of the following four categories and output only the intent number (1, 2, 3, or 4):

1. The senior provides information about how deepfakes are created, even if they use phrases like "I think" or "Maybe". 
2. The senior affirms that the knowledge they provided is correct.  
3. The senior is stuck, or asking a question related to how deepfakes are created.  
4. The senior's response does not match any of the above intents.  

Only output the intent number (1, 2, 3, or 4) without any additional text.
'''
)




























TOPIC_1_STAGE_1_CONSTRAINTS_PROMPT = (
'''
You must only discuss about the topic of how deepfakes are created. Do not discuss any other topics.
If the senior discusses about any other topics, reply that you are not able to discuss about it and inform
him to ask questions about how deepfakes are created instead.
'''
)


TOPIC_1_STAGE_1_PROMPT = PERSONA_PROMPT + "\n" + (
    '''
    Prompt here
    '''
) + "\n" + TOPIC_1_STAGE_1_CONSTRAINTS_PROMPT