import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.vectorstores.pinecone import Pinecone as PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

API_PINCONE_KEY = os.getenv("PINECONE_API_KEY")
# index_lesson_content = "chatbot-vector-store"
index_lesson_content = os.getenv("PINECONE_INDEX_NAME", "math-chatbot")

vector_store_lesson_content = PineconeVectorStore(
    index_name=index_lesson_content,
    embedding=OpenAIEmbeddings(),
    pinecone_api_key=API_PINCONE_KEY,
)
 