from agents.flow import graph
import uuid
from langchain_core.messages import HumanMessage, AIMessage

if __name__ == "__main__":
    while True:
        config = {
            "user_id": "1",
            "thread_id": str(uuid.uuid4())
        }
        user_input = input("You: ")
        state = {"messages": [HumanMessage(content=user_input)]}
        response = graph.invoke(state, config)
        print(f"Bot: {response['messages'][-1].content}")

        if user_input.lower() == "exit":
            break
