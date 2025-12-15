"""
SYNTX Wrapper Service - Data Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    """Request model for /api/chat"""
    prompt: str = Field(..., min_length=1)
    mode: str = Field(default="cyberdark")
    include_init: bool = Field(default=True)
    include_terminology: bool = Field(default=False)
    max_new_tokens: int = Field(default=500, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    do_sample: bool = Field(default=True)

class ChatResponse(BaseModel):
    """Response model"""
    response: str
    metadata: Optional[Dict[str, Any]] = None
    field_flow: Optional[List[Dict[str, Any]]] = None
