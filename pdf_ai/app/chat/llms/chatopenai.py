from langchain.chat_models import ChatOpenAI


def buil_llm(chat_args):
    return ChatOpenAI(streaming=chat_args.streaming)
