from dataclasses import dataclass
from typing import List
from agents.intent import IntentAgent
from config.llm_config import LLM_CONFIG, MODEL

LLM_KEY = {
    "role": "system",
    "content": """You are a program, you direct ouput the required datatype, without any human language and extra infomation. You will be given a sentence, extract no more than 5 keyword, output in json format, example: [`keyword1`, `keyword2`, .. ].
    """,
}


def chat_intent(query: str) -> str:
    intent = IntentAgent().get_agent()
    reply = intent.generate_reply(messages=[{"content": query, "role": "user"}])
    return reply


# def chat_key(query: str) -> str:

#     # Use Ollama to get a response based on initial memory
#     response = ollama.chat(
#         model="gemma2:2b",
#         messages=[
#             LLM_KEY,
#             {
#                 "role": "user",
#                 "content": query,
#             },
#         ],
#     )
#     return response["message"]["content"]


@dataclass
class Query:
    text: str
    intent: str
    keywords: List[str]


class InputParser:
    def __init__(self):
        self.intents = [
            "search",
            "discussion",
            "chat",
            "sensitive",
        ]

    def parse_query(self, text: str) -> Query:
        # Basic keyword extraction (in production, use proper NLP)
        # TODO: use NLP
        keywords = [
            word.lower() for word in text.split() if len(word) > 3 and word.isalnum()
        ]

        # Simple intent classification
        intent = self._classify_intent(text)

        return Query(text=text, intent=intent, keywords=keywords)

    def _classify_intent(self, text: str) -> str:
        # Simple rule-based classification
        # TODO: LLM intent
        while True:
            res: str = chat_intent(text)
            if res.__contains__("discussion"):
                return "discussion"
            elif res.__contains__("search"):
                return "search"
            elif res.__contains__("chat"):
                return "chat"
            elif res.__contains__("sensitive"):
                return "sensitive"
            else:
                res = "repeat"
