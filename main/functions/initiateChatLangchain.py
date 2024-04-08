from operator import itemgetter
import os
from pprint import pprint
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from azure.storage.blob import BlobServiceClient
from .translate import translate
from .dbops.getParsedChatHistory import getParsedChatHistory
from main.models import Chat

os.environ["OPENAI_API_KEY"] = str(os.getenv("testOPENAI_API_KEY"))
CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

blob_service_client = BlobServiceClient.from_connection_string(conn_str=CONN_STR)
container_client = blob_service_client.get_container_client("ncert-extraction-storage")
print("\nListing blobs...")

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

try:
    # Create the local vectorstore folder (if it doesn't exist)
    os.makedirs("vectorstore", exist_ok=True)

    for blob in container_client.list_blobs(prefix="NCERT_IX_C1/vectorstore/"):
        # Extract the filename from the blob name (assuming simple structure)
        filename = blob.name.split("/")[-1]
        local_path = os.path.join(
            "vectorstore", filename
        )  # Path within "vectorstore" folder

        blob_client = container_client.get_blob_client(blob.name)
        with open(local_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
except Exception as ex:
    # Handle download exceptions
    print(f"Error downloading vectorstore files: {ex}")


def initiateChatLangchain(query, userLanguage) -> str:
    query = translate(userLanguage, "en", query)

    vectorstore = FAISS.load_local(
        "vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever()

    human_template = """Answer the question based only on the following context:
    {context}

    Question: {question}

    Answer in the following language: {language}
    """
    system_prompt = """
    You are a voice based conversational chatbot for students of India from grade 6th to 10th. You will help students learn from textbooks. You will understand the sentiments of students, questions asked by users from the textbook. Provide answers by giving simple examples and analogies from their household and surroundings which they can observe, touch and feel in their everyday life. Strictly use BR - 200 lexile code to answer.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            MessagesPlaceholder("chat_history"),
            human_message_prompt,
        ]
    )

    model = ChatOpenAI()
    chain = (
        {
            "context": itemgetter("question") | retriever,  # Context from retriever
            "chat_history": itemgetter("chat_history"),  # Add chat_history
            "question": itemgetter("question"),
            "language": itemgetter("language"),
        }
        | chat_prompt
        | model
        | StrOutputParser()
    )
    # print("VectorSearch :", vectorstore.similarity_search(query))
    chat_history = getParsedChatHistory(Chat.objects.all().order_by('id')[:10])
    print(chat_history)
    output = chain.invoke(
        {"question": str(query), "language": "english", "chat_history": chat_history}
    )
    Chat.objects.create(author="human", content=query)
    Chat.objects.create(author="ai", content=output)
    return output


if __name__ == "__main__":
    print(initiateChatWithContext("फिगर वन पॉईंट वन समझ नहीं आया", "hi"))
