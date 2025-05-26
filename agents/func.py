from typing import List
from dotenv import load_dotenv
from config.llm import llm_no_tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from .prompt import prompt
from .tools import search_memory, tools
from langgraph.graph import MessagesState

# Khởi tạo LLM (OpenAI)
load_dotenv()
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.1, max_tokens=512)

class State(MessagesState):
    messages: List[HumanMessage]
    recall_memories: List[str]


def load_memories(state: State, config: RunnableConfig) -> State:
    """Truy vấn các memory cũ từ vector store dựa trên câu hỏi hiện tại."""
    messages = state.get("messages", [])
    query = "".join([m.content for m in messages if isinstance(m, HumanMessage)])
    memories = search_memory.invoke(query, config)
    return {"recall_memories": memories}


def agent(state: State, config: RunnableConfig) -> State:
    """Generate answer with LLM, optionally using retrieved memory."""
    llm_with_tools = llm_no_tool.bind_tools(tools)
    bound = prompt | llm_with_tools
    recall_str = (
        "<recall_memory>\n" + "\n".join(state["recall_memories"]) + "\n</recall_memory>"
    )
    prediction = bound.invoke(
        {
            "messages": state["messages"],
            "recall_memories": recall_str,
        }
    )
    return {
        "messages": [prediction],
    }


def route_tools(state: State) -> str:
    """Chuyển hướng đến tools nếu AIMessage chứa tool_calls"""
    messages = state.get("messages", [])
    if not isinstance(messages, list):
        messages = [messages]
    if not messages:
        return END
    last = messages[-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return END
