from langchain_ollama import ChatOllama
import tiktoken
from transformers import AutoTokenizer
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
load_dotenv()


# model = ChatOllama(model="llama3.2:3b-instruct-fp16", temperature=0.1, max_tokens=200)
llm_no_tool = ChatOpenAI(model_name="gpt-4o")

# model_with_tools = model.bind_tools(tools)

# recall_vector_store = InMemoryVectorStore(OpenAIEmbeddings())

# tokenizer = tiktoken.encoding_for_model("gpt-4o")

