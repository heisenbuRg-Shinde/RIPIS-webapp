from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.reasoning import ReasoningEngine
from app.core.auth import get_current_user
from app.core.database import User

router = APIRouter()

# Initialize reasoning engine once
reasoning_engine = ReasoningEngine()


class ReasoningRequest(BaseModel):
    """Request model for reasoning endpoint"""
    interview_type: str  # 'coding' or 'theory'
    domain: str          # 'DSA', 'OS', or 'DBMS'
    subtopic: Optional[str] = None
    voice_assisted: bool = False


class ReasoningResponse(BaseModel):
    """Response model for reasoning endpoint"""
    concept: str
    approach: str
    pseudocode: str
    common_mistakes: str
    example_code: str
    syntax_structure: str
    voice_script: Optional[str] = None


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/reasoning", response_model=ReasoningResponse)
async def get_reasoning(
    request: ReasoningRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate structured reasoning for interview practice.
    
    Returns hints and guidance without providing final solutions.
    Requires authentication.
    """
    result = reasoning_engine.generate_reasoning(
        interview_type=request.interview_type,
        domain=request.domain,
        subtopic=request.subtopic,
        voice_assisted=request.voice_assisted
    )
    return result


@router.get("/domains")
async def get_domains():
    """Get available domains and their subtopics"""
    return {
        "domains": {
            "DSA": ["array", "string", "linked_list", "tree", "graph", "dynamic_programming", "sorting", "searching"],
            "OS": ["deadlock", "process_scheduling", "memory_management", "synchronization"],
            "DBMS": ["normalization", "transactions", "indexing", "joins", "query_optimization"]
        }
    }
