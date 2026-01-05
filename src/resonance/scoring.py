"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎯 SYNTX SCORING API v2.1 - FIELDBRAIN + LOGGING + MANAGEMENT               ║
║  Field-based Response Scoring mit Logs, Analytics & Profile Management      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Import scoring engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from scoring.router import score_response, get_available_scorers
from scoring.logger import get_recent_logs, get_field_performance
from scoring.profile_loader import get_profile, save_profiles, list_all_profiles

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
    """FIELDBRAIN v0.1 - Profile-based scoring"""
    name: str
    score: float
    weight: float
    weighted_score: float
    profile_used: str
    profile_name: Optional[str] = None
    strategy: Optional[str] = None
    components: Optional[Dict] = None
    auto_registered: Optional[bool] = False

class ScoreResponse(BaseModel):
    scored_fields: List[ScoredField]
    total_score: float
    format_name: str
    field_count: int
    total_weight: float
    fieldbrain_version: Optional[str] = "0.1.0"
    logging_enabled: Optional[bool] = True


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 SCORING ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/score", response_model=ScoreResponse)
async def score_chat_response(request: ScoreRequest):
    """
    🎯 Score Response gegen Format-Felder
    
    **FIELDBRAIN v0.1 - Profile-Based Scoring + Logging**
    
    Nimmt:
    - `text`: Der LLM Response Text
    - `format`: Format Definition mit Feldern + Gewichten
    
    Gibt zurück:
    - Scores für jedes Feld (0.0-1.0)
    - Profile verwendet
    - Component breakdown
    - Gesamt-Score (normalisiert)
    
    **NEW: Alle Scores werden geloggt für Analytics**
    """
    try:
        format_dict = {
            "name": request.format.name,
            "fields": [
                {"name": f.name, "weight": f.weight}
                for f in request.format.fields
            ]
        }
        
        result = score_response(format_dict, request.text)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 LOGGING & ANALYTICS ENDPOINTS (NEW!)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/logs")
async def get_scoring_logs(
    limit: int = Query(100, description="Max entries to return"),
    field: Optional[str] = Query(None, description="Filter by field name"),
    min_score: Optional[float] = Query(None, description="Minimum score filter"),
    max_score: Optional[float] = Query(None, description="Maximum score filter")
):
    """
    📊 Get recent score logs
    
    **FIELDBRAIN Analytics - Die Augen des Systems**
    
    Query Parameters:
    - `limit`: Max entries (default: 100)
    - `field`: Filter by specific field
    - `min_score`: Only scores >= this value
    - `max_score`: Only scores <= this value
    
    Returns:
    - List of score log entries (JSONL format)
    - Each entry: timestamp, field, score, profile, components
    
    **Example:**
```
    GET /resonanz/scoring/logs?field=driftkorper&min_score=0.5&limit=50
```
    """
    try:
        logs = get_recent_logs(
            limit=limit,
            field=field,
            min_score=min_score,
            max_score=max_score
        )
        
        return {
            "logs": logs,
            "count": len(logs),
            "filters": {
                "field": field,
                "min_score": min_score,
                "max_score": max_score,
                "limit": limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log retrieval failed: {str(e)}")


@router.get("/scoring/analytics/performance/{field_name}")
async def get_field_analytics(
    field_name: str,
    days: int = Query(7, description="Number of days to analyze")
):
    """
    📈 Get performance analytics for a field
    
    **FIELDBRAIN Analytics - Field Performance Tracking**
    
    Returns:
    - Total scores
    - Average, min, max, median scores
    - Profiles used
    - Score distribution
    
    **Example:**
```
    GET /resonanz/scoring/analytics/performance/driftkorper?days=7
```
    
    **Response:**
```json
    {
      "field": "driftkorper",
      "total_scores": 150,
      "avg_score": 0.45,
      "min_score": 0.0,
      "max_score": 0.95,
      "median_score": 0.42,
      "profiles_used": ["dynamic_language_v1", "default_fallback"]
    }
```
    """
    try:
        analytics = get_field_performance(field_name, days=days)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 PROFILE MANAGEMENT ENDPOINTS (NEW!)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/profiles")
async def list_profiles():
    """
    📋 List all scoring profiles
    
    **FIELDBRAIN Profile Management**
    
    Returns all available profiles with their configurations.
    """
    try:
        profiles = list_all_profiles()
        return {
            "profiles": profiles,
            "total": len(profiles),
            "fieldbrain_version": "0.1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile listing failed: {str(e)}")


@router.get("/scoring/profiles/{profile_id}")
async def get_profile_details(profile_id: str):
    """
    🔍 Get specific profile details
    
    **FIELDBRAIN Profile Management**
    
    Returns full configuration for a single profile.
    
    **Example:**
```
    GET /resonanz/scoring/profiles/dynamic_language_v1
```
    """
    try:
        profile = get_profile(profile_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
        
        return {
            "profile_id": profile_id,
            "profile": profile
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile retrieval failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 HEALTH & INFO
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/available")
async def get_available_scoring_methods():
    """
    🔍 Liste verfügbare Scorer
    
    **FIELDBRAIN v0.1 - Returns Profiles, not functions**
    """
    return get_available_scorers()


@router.get("/scoring/health")
async def scoring_health():
    """
    🏥 Scoring System Health Check
    
    Prüft:
    - Scoring Module verfügbar
    - Profiles geladen
    - Registry funktioniert
    - Logging aktiv
    """
    try:
        scorers = get_available_scorers()
        
        # Check if logs directory exists
        from pathlib import Path
        logs_exist = Path("/opt/syntx-logs/scoring").exists()
        
        return {
            "status": "🟢 FIELDBRAIN AKTIV",
            "version": "0.1.0",
            "profiles_loaded": scorers.get("total_profiles", 0),
            "logging_enabled": logs_exist,
            "features": [
                "Profile-based scoring",
                "Auto-registration",
                "Score logging",
                "Analytics",
                "Profile management"
            ]
        }
    except Exception as e:
        return {
            "status": "🔴 SCORING ERROR",
            "error": str(e)
        }
