from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from .func import State, load_memories, agent, route_tools
from .tools import tools

builder = StateGraph(State)

builder.add_node("agent", agent)
builder.add_node("load_memories", load_memories)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("load_memories")
builder.add_edge("load_memories", "agent")
builder.add_conditional_edges("agent", route_tools, ["tools", END])
builder.add_edge("tools", "agent")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)