"""
main_api.py
-----------
FastAPI app for exposing the multi-agent medical assistant as a REST API endpoint.
Handles chat requests and returns responses from the agent workflow.
"""

from fastapi import FastAPI, Request  # FastAPI framework
from pydantic import BaseModel  # For request/response models
from agents.graph_builder import app as agent_app, config  # Multi-agent workflow and config
from fastapi.middleware.cors import CORSMiddleware  # For CORS support

# ---------------------- Request/Response Models ----------------------- #
class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    Attributes:
        message (str): The user's message to the assistant.
    """
    message: str

class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    Attributes:
        response (str): The assistant's reply.
    """
    response: str

# ---------------------- FastAPI App Setup ----------------------------- #
fastapi_app = FastAPI()

# Optional: Allow CORS for local development or frontend integration
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- Chat Endpoint --------------------------------- #
@fastapi_app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handles POST requests to /chat. Passes the user's message to the agent workflow and returns the response.
    Args:
        request (ChatRequest): The incoming chat request.
    Returns:
        ChatResponse: The assistant's reply.
    """
    user_input = request.message
    agent_response = agent_app.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
    content = agent_response["messages"][-1].content
    return ChatResponse(response=content)

# To run: uvicorn app.main_api:fastapi_app --reload
