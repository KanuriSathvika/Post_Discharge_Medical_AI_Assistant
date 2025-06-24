# from langgraph.graph import START,StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv      
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.receptionist_agent.receptionist_agent import receptionist_assistant
from agents.clinical_agent.clinical_agent import clinical_assistant


from langgraph_swarm import create_swarm
from langgraph_swarm import create_handoff_tool
from langgraph.checkpoint.memory import InMemorySaver


checkpointer = InMemorySaver()
workflow = create_swarm(
    [receptionist_assistant, clinical_assistant],
    default_active_agent="receptionist_assistant"
)
app = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}

# print("Welcome to the multi-agent chat! Type 'exit' to quit.")
# while True:
#     user_input = input("You: ")
#     if user_input.strip().lower() == "exit":
#         print("Goodbye!")
#         break
#     response = app.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
#     print("Agent:", response["messages"][-1].content)

