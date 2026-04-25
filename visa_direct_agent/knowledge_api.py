# knowledge_api.py

from fastapi import FastAPI
from pydantic import BaseModel
from key_system import verify_key
from agent1 import ask_agent1

app = FastAPI(
    title="Visa Direct Agent 1 API",
    description="Paid knowledge endpoint. Valid key required. $10/key"
)

class AgentRequest(BaseModel):
    key: str
    question: str

class AgentResponse(BaseModel):
    access: bool
    answer: str = ""
    reason: str = ""
    owner: str = ""

@app.post("/ask-agent1", response_model=AgentResponse)
async def ask_knowledge(request: AgentRequest):
    # Step 1 - Verify key
    verification = verify_key(request.key)

    # Step 2 - Key invalid
    if not verification["access"]:
        return AgentResponse(
            access=False,
            reason=verification["reason"]
        )

    # Step 3 - Key valid - get answer
    if not request.question.strip():
        return AgentResponse(
            access=True,
            reason="Key valid but no question provided.",
            owner=verification["owner"]
        )

    answer = ask_agent1(request.question)

    return AgentResponse(
        access=True,
        answer=answer,
        reason="Access granted.",
        owner=verification["owner"]
    )

@app.get("/")
async def root():
    return {
        "agent": "Agent 1 - Visa Direct Expert",
        "status": "active",
        "access": "Key required - $10/key",
        "endpoint": "POST /ask-agent1",
        "key_format": "VISADIRECT-XXXXXX"
    }
