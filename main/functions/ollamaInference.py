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
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from azure.storage.blob import BlobServiceClient
from translate import translate
from dbparsers.getParsedChatHistory import getParsedChatHistory
# from models import Chat
from prompts import yozu_prompts
from langchain_community.llms import Ollama

os.environ["OPENAI_API_KEY"] = str(os.getenv("testOPENAI_API_KEY"))

def ollamaInference(query, userLanguage, isNewSession) -> str:
    query = translate(userLanguage, "en", query)

    vectorstore = FAISS.load_local(
        "vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever()

    human_template = yozu_prompts["new_session" if isNewSession == 1 else "default"][
        "human_template"
    ]
    system_prompt = yozu_prompts["new_session" if isNewSession == 1 else "default"][
        "system_prompt"
    ]

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_template = 'Answer the question based only on the following context; disregard the context if student is conversing:\n{context}\n\nQuestion: {question}\n\nAnswer in the following language: {language}\n  '
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt,
        ]
    )

    model = Ollama(model="phi")
    chain = (
        {
            "context": itemgetter("question") | retriever,  # Context from retriever
            "question": itemgetter("question"),
            "language": itemgetter("language"),
        }
        | chat_prompt
        | model
        | StrOutputParser()
    )
    # print("VectorSearch :", vectorstore.similarity_search(query))
    output = chain.invoke(
        {"question": str(query), "language": "english"}
    )
    return output


if __name__ == "__main__":
    print(ollamaInference("Can you explain figure 1.1 ?", "en", 0))
    