"""FastAPI backend for Virtuele Burgerraad."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import json
import asyncio

from . import storage

# TODO: Replace with burgerraad imports when implemented
# from .burgerraad import (
#     run_full_burgerraad,
#     stage1_eerste_reacties,
#     stage2_coalitievorming,
#     stage3_coalitiedebatten,
#     stage4_ombudsman_rapport,
# )

app = FastAPI(title="Virtuele Burgerraad API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateConversationRequest(BaseModel):
    """Request to create a new conversation."""

    pass


class SendMessageRequest(BaseModel):
    """Request to send a message in a conversation."""

    content: str


class ConversationMetadata(BaseModel):
    """Conversation metadata for list view."""

    id: str
    created_at: str
    title: str
    message_count: int


class Conversation(BaseModel):
    """Full conversation with all messages."""

    id: str
    created_at: str
    title: str
    messages: List[Dict[str, Any]]


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "service": "Virtuele Burgerraad API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Virtuele Burgerraad API"}


@app.get("/api/conversations", response_model=List[ConversationMetadata])
async def list_conversations():
    """List all conversations (metadata only)."""
    return storage.list_conversations()


@app.post("/api/conversations", response_model=Conversation)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    conversation = storage.create_conversation(conversation_id)
    return conversation


@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all its messages."""
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


# TODO: Implement Virtuele Burgerraad endpoints in Task 6
# These will replace the old LLM Council message endpoints
#
# @app.post("/api/sessions")
# async def create_session(policy_text: str):
#     """Create a new burgerraad session with policy text."""
#     pass
#
# @app.post("/api/sessions/{session_id}/stage1")
# async def run_stage1(session_id: str):
#     """Run Stage 1: Eerste Reacties."""
#     pass
#
# @app.post("/api/sessions/{session_id}/stage2")
# async def run_stage2(session_id: str):
#     """Run Stage 2: Coalitievorming."""
#     pass
#
# @app.post("/api/sessions/{session_id}/stage3")
# async def run_stage3(session_id: str):
#     """Run Stage 3: Coalitiedebatten."""
#     pass
#
# @app.post("/api/sessions/{session_id}/stage4")
# async def run_stage4(session_id: str):
#     """Run Stage 4: Ombudsman Rapport."""
#     pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
