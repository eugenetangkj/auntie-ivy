from prompts.common_prompts import PERSONA_PROMPT


'''
TOPIC 1 STAGE 1 KNOWLEDGE:

The default knowledge that the peer agent has about how deepfakes are created.
'''
TOPIC_1_STAGE_1_DEFAULT_KNOWLEDGE = [
    # Basic knowledge and facts that revolve around data collection and identifying patterns
    "Deepfakes are videos or images that use AI to replace someone's face or voice with another person's.",
    "I think to create a good deepfake, the AI needs a lot of images and videos of the person.",
    "The AI will use the images and videos of the person to find a suitable one with the correct expression to replace the face in the image or video."

    # Some incorrect facts
    "We need a lot of time to make deepfakes.",
    "Probably only those who are knowledgeable in AI can create them.",
]

'''
TOPIC 1 STAGE 1:
Assistant answers the questions that the user has about how are deepfakes created.

'''
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