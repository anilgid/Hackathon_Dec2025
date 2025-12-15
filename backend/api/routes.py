from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.services.security import SecurityService
from backend.agents.root_agent import RootAgent

router = APIRouter()
root_agent = RootAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sanitized_input: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to handle chat messages.
    Sanitizes input and routes to the Root Agent.
    """
    raw_message = request.message
    
    # 1. Sanitize Input
    sanitized_message = SecurityService.sanitize_input(raw_message)
    
    # 2. Log request (Basic print for now, Middleware handles detailed logs)
    # print(f"Received message: {sanitized_message}") # Handled by middleware ideally
    
    try:
        # 3. Pass to Root Agent
        agent_response = await root_agent.process_request(sanitized_message)
        
        return ChatResponse(
            response=agent_response,
            sanitized_input=sanitized_message
        )
    except Exception as e:
        # Log the error
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
