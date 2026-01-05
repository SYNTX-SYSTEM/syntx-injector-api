"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎯 SYNTX SCORING ROUTER                                                     ║
║  Field-based Response Scoring                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Import scoring engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from scoring.router import score_response, get_available_scorers

router = APIRouter(prefix="/resonanz", tags=["scoring"])


# ═══════════════════════════════════════════════════════════════════════════════
#  📦 MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class FieldDefinition(BaseModel):
    name: str
    weight: float = 1.0

class FormatDefinition(BaseModel):
    name: str
    fields: List[FieldDefinition]

class ScoreRequest(BaseModel):
    text: str = Field(..., description="Response text to score")
    format: FormatDefinition = Field(..., description="Format with fields to score against")

class ScoredField(BaseModel):
    name: str
    score: float
    weight: float
    weighted_score: float
    scoring_method: str

class ScoreResponse(BaseModel):
    scored_fields: List[ScoredField]
    total_score: float
    format_name: str
    field_count: int
    total_weight: float


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/score", response_model=ScoreResponse)
async def score_chat_response(request: ScoreRequest):
    """
    🎯 Score Response gegen Format-Felder
    
    **Das Herzstück der Heuristik!**
    
    Nimmt:
    - `text`: Der LLM Response Text
    - `format`: Format Definition mit Feldern + Gewichten
    
    Gibt zurück:
    - Scores für jedes Feld (0.0-1.0)
    - Gewichtete Scores
    - Gesamt-Score (normalisiert)
    
    **Beispiel:**
```json
    {
      "text": "Das System driftet stark nach links und braucht Kalibrierung...",
      "format": {
        "name": "syntx_true_raw",
        "fields": [
          {"name": "driftkorper", "weight": 1.0},
          {"name": "kalibrierung", "weight": 1.0},
          {"name": "stromung", "weight": 0.7}
        ]
      }
    }
```
    
    **Scoring Logic:**
    1. Für jedes Feld: Suche spezifische Heuristik (z.B. `score_driftkorper`)
    2. Wenn nicht gefunden: Fallback-Scorer
    3. Multipliziere Score × Weight
    4. Summiere alle weighted scores
    5. Normalisiere durch Summe der Weights
    """
    try:
        # Convert Pydantic models to dicts
        format_dict = {
            "name": request.format.name,
            "fields": [
                {"name": f.name, "weight": f.weight}
                for f in request.format.fields
            ]
        }
        
        # Score the response
        result = score_response(format_dict, request.text)
        
        # Check for errors
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@router.get("/scoring/available")
async def get_available_scoring_methods():
    """
    🔍 Liste verfügbare Scorer
    
    Zeigt:
    - Spezifische Heuristiken (z.B. driftkorper, kalibrierung, stromung)
    - Fallback-Verfügbarkeit
    
    **Beispiel Response:**
```json
    {
      "specific": ["driftkorper", "kalibrierung", "stromung"],
      "fallback": "Available for all fields"
    }
```
    """
    return get_available_scorers()


@router.get("/scoring/health")
async def scoring_health():
    """
    🏥 Scoring System Health Check
    
    Prüft:
    - Scoring Module verfügbar
    - Heuristiken geladen
    - Fallback funktioniert
    """
    try:
        scorers = get_available_scorers()
        
        return {
            "status": "🟢 SCORING AKTIV",
            "specific_scorers": len(scorers.get("specific", [])),
            "scorers": scorers,
            "fallback": "Available"
        }
    except Exception as e:
        return {
            "status": "🔴 SCORING ERROR",
            "error": str(e)
        }
