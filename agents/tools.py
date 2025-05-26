import uuid
from typing import List, Dict

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# Khởi tạo vector store dùng OpenAI embeddings
vector_store = InMemoryVectorStore(OpenAIEmbeddings())

def get_user_id(config: RunnableConfig) -> str:
    return config.get("user_id", "default")

@tool
def search_memory(query: str, config: RunnableConfig) -> List[str]:
    """
    Tìm kiếm trong bộ nhớ đã lưu các đoạn phù hợp với truy vấn.
    Trả về nội dung văn bản.
    """
    user_id = get_user_id(config)
    docs = vector_store.similarity_search(query, k=5, filter=lambda d: d.metadata.get("user_id") == user_id)
    return [doc.page_content for doc in docs]

@tool
def save_recall_memory(memory: str, config: RunnableConfig) -> str:
    """Save memory to vectorstore for later semantic retrieval."""
    user_id = get_user_id(config)
    document = Document(
        page_content=memory, id=str(uuid.uuid4()), metadata={"user_id": user_id}
    )
    vector_store.add_documents([document])
    return memory

tools = [search_memory, save_recall_memory]
