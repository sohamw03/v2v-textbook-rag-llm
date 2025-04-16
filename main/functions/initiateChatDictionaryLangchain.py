from operator import itemgetter
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .translate import translate
from .prompts import vtv_prompts

os.environ["OPENAI_API_KEY"] = str(os.getenv("OPENAI_API_KEY"))


def initiateChatDictionaryLangchain(query, userLanguage) -> str:
    query = translate(userLanguage, "en", query)

    human_template = vtv_prompts["dictionary_mode"]["human_template"]
    system_prompt = vtv_prompts["dictionary_mode"]["system_prompt"]

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt,
        ]
    )

    model = ChatOpenAI()
    chain = (
        {"question": itemgetter("question")} | chat_prompt | model | StrOutputParser()
    )

    output = chain.invoke({"question": str(query)})

    return output


if __name__ == "__main__":
    query = "What is the meaning of the word Pollutant?"
    userLanguage = "en"
    isNewSession = 1

    initiateChatDictionaryLangchain(query, userLanguage, isNewSession)
