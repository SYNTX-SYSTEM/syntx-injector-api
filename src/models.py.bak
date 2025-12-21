"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🌊 SYNTX WRAPPER SERVICE - DRIFTKÖRPER DEFINITIONEN 🌊                    ║
║                                                                              ║
║    Nicht "Data Models" - FELD-RESONANZ-PARAMETER.                            ║
║    Diese Schemas definieren wie Felder durch das System fließen.             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """
    🌊 CHAT RESONANZ REQUEST
    
    Nicht "Request Body" - FELD-AKTIVIERUNGS-PARAMETER.
    
    ════════════════════════════════════════════════════════════════════════════
    
    WICHTIG - ZWEI DIMENSIONEN:
    
        mode   = WIE denkt das Modell? (Wrapper = Stil, Tonalität)
        format = WAS kommt raus? (Format = Felder, Struktur)
    
    ════════════════════════════════════════════════════════════════════════════
    
    Beispiel:
        {
            "prompt": "Analysiere das Internet",
            "mode": "syntex_wrapper_sigma",    ← WIE (kreativ, systemisch)
            "format": "syntex_system"          ← WAS (3 Felder Output)
        }
    
    ════════════════════════════════════════════════════════════════════════════
    """
    
    # 🎯 DER PROMPT - Was der User fragt
    prompt: str = Field(..., min_length=1, description="Die Frage an das Feld")
    
    # 🎭 DER MODUS - WIE das Modell denkt (Wrapper)
    mode: str = Field(
        default="syntex_wrapper_sigma", 
        description="Wrapper = WIE denkt das Modell? Stil, Tonalität, Persönlichkeit"
    )
    
    # 🔥 DAS FORMAT - WAS rauskommt (NEU!)
    format: Optional[str] = Field(
        default=None,
        description="Format = WAS kommt raus? Felder, Struktur. z.B. 'syntex_system', 'human', 'sigma'"
    )
    
    # 🔧 WRAPPER-LAYER KONTROLLE
    include_init: bool = Field(
        default=True, 
        description="SYNTX Init-Wrapper inkludieren?"
    )
    include_terminology: bool = Field(
        default=False, 
        description="Terminologie-Wrapper inkludieren?"
    )
    
    # ⚙️ MODELL-PARAMETER
    max_new_tokens: int = Field(
        default=500, 
        ge=1, 
        le=4096,
        description="Max Tokens für Response"
    )
    temperature: float = Field(
        default=0.7, 
        ge=0.0, 
        le=2.0,
        description="Kreativität (0=deterministisch, 2=chaos)"
    )
    top_p: float = Field(
        default=0.95, 
        ge=0.0, 
        le=1.0,
        description="Nucleus Sampling"
    )
    do_sample: bool = Field(
        default=True,
        description="Sampling aktivieren?"
    )
    
    # 🌍 SPRACHE (NEU!)
    language: str = Field(
        default="de",
        description="Sprache für Format-Felder: 'de' oder 'en'"
    )


class ChatResponse(BaseModel):
    """
    🌊 CHAT RESONANZ RESPONSE
    
    Nicht "Response Body" - FELD-MANIFESTATION.
    
    Das Feld hat resoniert. Dies ist das Resultat.
    """
    
    # 💎 DIE ANTWORT
    response: str
    
    # 📊 METADATA - Wie das Feld floss
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Request ID, Wrapper Chain, Latency, Format..."
    )
    
    # 🌊 FIELD FLOW - Alle 5 Stages
    field_flow: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Kompletter Feld-Flow durch alle Stages"
    )


class FormatInfo(BaseModel):
    """
    📋 FORMAT INFO
    
    Kurze Info über ein verfügbares Format.
    """
    name: str
    fields_count: int
    description: str
    languages: List[str]
