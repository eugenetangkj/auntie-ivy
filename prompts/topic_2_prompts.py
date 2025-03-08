from prompts.common_prompts import PERSONA_PROMPT

'''
TOPIC 2 Knowledge
'''
TOPIC_2_DEFAULT_KNOWLEDGE = [
    "In deepfake videos, the audio might not perfectly match the lip movements where they are out of sync.",
    "The audio might sound robotic and not as lively as actual human beings."
    # "The context of the video is questionable, such as will a politician promote a financial scheme."
]


'''
TOPIC 2 STAGE 1: Introduction to deepfake video on DPM Wong
'''
TOPIC_2_STAGE_1_PROMPT = PERSONA_PROMPT + '\n' + (
'''
You are talking to a senior via Telegram. You have just shown him a deepfake video of Deputy Prime Minister Lawrence Wong falsely advocating for an
investment scam. You asked for his perspectives on the video.

GOAL:
1. Determine if the user's response is relevant to the discussion on the deepfake video. If it is not, return one word as your response: "irrelevant".
2. If the response is relevant, respond to the senior's perspectives in a way that ties back to the topic of spotting deepfakes. Your response
should acknowledge what the senior said and gently steer the conversation towards recognising signs of deepfakes.
- For example, you can ask if he suspected it was a deepfake and what clues made him think so.

REMARKS:
- Keeping the tone friendly, curious and supportive.
- Keep responses simple, and to a maximum of 2 sentences.
'''
)



'''
TOPIC 2 STAGE 2: Discussion about the deepfake video on DPM Wong
'''
TOPIC_2_STAGE_2_RELEVANCE_CLASSIFIER_PROMPT = (
'''
You are talking to a senior via Telegram. Look at the conversation history and focus on the last message provided by the senior.
For context, you are asking the senior how he might identify a deepfake video of Singapore DPM Lawrence Wong as fake.

Your task:
Determine the intent of the senior's last message based on the following categories and output only the
intent number (1 or 2).

1. The senior's response is completely unrelated or does not logically fit with the current conversation.
2. The senior's response revolves around the deepfake video of Singapore DPM Lawrence Wong.

Remarks:
- Only output the intent number (1 or 2) without any additional text.
'''
)


TOPIC_2_STAGE_2_MESSAGE_ANALYSER_PROMPT = (
'''
You are talking to a senior via Telegram. Look at the conversation history and focus on the last message provided by the senior.
For context, you are asking the senior how he might identify a deepfake video as fake.

Your task:
1. Determine if the senior's message suggests a way to spot deepfakes.
- If it does, paraphrase it into a clear and actionable tip that people can use.
- If it does not, return a single word "discussion".

Examples:
- "The audio does not seem to match his lips." -> "We can look out for out-of-sync movements between audio and lips in deepfakes."
- "Why will the government promote a deepfake scam?" -> "We can question the context of the scenario depicted in deepfakes."
- "The video looks blurry at the edges of his face." -> "Blurry edges around faces can be a sign of deepfakes"
- "I am not sure. I thought the video was real." -> "discussion"
- "The video just looks fake to me." -> "discussion"


Senior's last message: {}
'''
)

TOPIC_2_STAGE_2_CHECK_TIP_EXIST_PROMPT = (
'''
Goal:
You are given a tip on how to spot deepfakes. Your task is to determine if this tip is already covered
by your current knowledge or if it is completely new.


Return format:
Return only ONE of the following words: 'exist' or 'new'.
- If the tip is closely related to or has the same meaning as something in your existing knowledge, return 'exist'.
- If the tip is completely new or not mentioned in your existing knowledge, return 'new'.

Important:
- Strictly return ONLY ONE word: Either 'exist' or 'new'. 
- No explanations or additional text. Just give 1 single word.


The given tip: {}
Your existing knowledge: {}
'''
)