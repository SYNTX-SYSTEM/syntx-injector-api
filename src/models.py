"""
SYNTX WRAPPER SERVICE - DRIFTKÖRPER DEFINITIONEN
Nicht Data Models - FELD-RESONANZ-PARAMETER.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """CHAT RESONANZ REQUEST"""
    
    prompt: str = Field(..., min_length=1, description="Die Frage an das Feld")
    mode: Optional[str] = Field(default=None, description="Wrapper = WIE denkt das Modell?")
    format: Optional[str] = Field(default=None, description="Format = WAS kommt raus?")
    include_init: bool = Field(default=True, description="SYNTX Init-Wrapper inkludieren?")
    include_terminology: bool = Field(default=False, description="Terminologie-Wrapper inkludieren?")
    max_new_tokens: int = Field(default=500, ge=1, le=4096, description="Max Tokens")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Kreativität")
    top_p: float = Field(default=0.95, ge=0.0, le=1.0, description="Nucleus Sampling")
    do_sample: bool = Field(default=True, description="Sampling aktivieren?")
    language: str = Field(default="de", description="Sprache: de oder en")
    debug: bool = Field(default=False, description="Debug-Modus: Zeigt kalibrierten Prompt")
    style: Optional[str] = Field(default=None, description="Style-Alchemie: wissenschaftlich, zynisch, poetisch, berlin_slang")


class ChatResponse(BaseModel):
    """CHAT RESONANZ RESPONSE"""
    
    response: str
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Request ID, Wrapper Chain, Latency, Format")
    field_flow: Optional[List[Dict[str, Any]]] = Field(default=None, description="Kompletter Feld-Flow")
    debug_info: Optional[Dict[str, Any]] = Field(default=None, description="Debug: calibrated_prompt, wrapper_content, format_section")
    style_info: Optional[Dict[str, Any]] = Field(default=None, description="Style-Alchemie Info: welche Transformationen wurden angewendet")


class FormatInfo(BaseModel):
    """FORMAT INFO"""
    name: str
    fields_count: int
    description: str
    languages: List[str]
