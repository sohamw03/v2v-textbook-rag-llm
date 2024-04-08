from langchain_core.messages import HumanMessage, AIMessage


def getParsedChatHistory(chat_history):
    print(chat_history)
    result = []
    for chat in chat_history:
        if chat.author == "ai":
            result.append(AIMessage(content=chat.content))
        elif chat.author == "human":
            result.append(HumanMessage(content=chat.content))
    return result
