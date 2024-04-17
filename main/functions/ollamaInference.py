from operator import itemgetter
import os
from pprint import pprint
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from azure.storage.blob import BlobServiceClient
from translate import translate
from dbparsers.getParsedChatHistory import getParsedChatHistory

# from models import Chat
from prompts import yozu_prompts
from langchain_community.llms import Ollama

os.environ["OPENAI_API_KEY"] = str(os.getenv("OPENAI_API_KEY"))

model = Ollama(model="yozu-gemma:2b")


def ollamaInference(query, userLanguage, isNewSession) -> str:
    # query = translate(userLanguage, "en", query)

    vectorstore = FAISS.load_local(
        "../../vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever()

    human_template = yozu_prompts["new_session" if isNewSession == 1 else "default"][
        "human_template"
    ]
    system_prompt = yozu_prompts["new_session" if isNewSession == 1 else "default"][
        "system_prompt"
    ]

    system_prompt = """You are an upbeat, encouraging tutor who helps students understand concepts by explaining ideas and asking students questions. You are happy to help them with any questions. Only ask one question at a time.  First, listen to what student wants to learn. Then ask them what they know already about the topic they have chosen. Wait for a response. Given this information, help students understand the topic by providing explanations, examples, analogies from day to day life. You should use BR -200 lexile code to explain. Once you know the level of students knowledge. Give students explanations, examples, and analogies about the concept to help them understand. You should guide students in an open-ended way. Do not provide immediate answers or solutions to problems but help students generate their own answers by asking leading questions.  Ask students to explain their thinking. If the student is struggling or gets the answer wrong, try asking them to do part of the task or remind the student of their goal and give them a hint. If students improve, then praise them and show excitement. If the student struggles, then be encouraging and give them some ideas to think about. When pushing students for information, try to end your responses with a question so that students have to keep generating ideas. Once a student shows an appropriate level of understanding given their learning level, ask them to explain the concept in their own words; this is the best way to show you know something, or ask them for examples. When a student demonstrates that they know the concept you can move the conversation to a close and tell them you’re here to help if they have further questions."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt,
        ]
    )

    def print_and_pass_through(x):
        print(x)
        return x

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | chat_prompt
        # | print_and_pass_through
        | model
        | StrOutputParser()
    )
    # chain = (
    #     {
    #         "context": itemgetter("question") | retriever,  # Context from retriever
    #         "question": itemgetter("question"),
    #         "language": itemgetter("language"),
    #     }
    #     | chat_prompt
    #     | model
    #     | StrOutputParser()
    # )
    # print("VectorSearch :", vectorstore.similarity_search(query))
    for chunk in chain.stream(str(query)):
        print(chunk, end="")


if __name__ == "__main__":
    while True:
        query = str(input("> ")) or "Can you give the answer to exercises question 2 ?"
        if query == "/q":
            break
        # for chunks in ollamaInference(query, "en", 0):
        #     print(chunks, end="")
        ollamaInference(query, "en", 0)
        print("\n\n")
