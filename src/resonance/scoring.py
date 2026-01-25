"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎯 SYNTX SCORING API v3.0 - FULL PROFILE MANAGEMENT                         ║
║  Scoring + Logging + Analytics + Profile Management                         ║
║  DAS VOLLSTÄNDIGE SYSTEM - MEINE HÄNDE SIND FREI                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Import scoring engine
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Core scoring
from scoring.router import score_response, get_available_scorers

# Logging & Analytics
from scoring.logger import get_recent_logs, get_field_performance

# Profile Management - GRANULAR IMPORTS ✨
from scoring.core.profile_reader import get_profile, list_all_profiles, invalidate_cache
from scoring.writers.profile_updater import update_profile
from scoring.writers.profile_creator import create_profile, delete_profile
from scoring.validators.profile_validator import (
    validate_profile, 
    validate_profile_update, 
    validate_profile_id
)
from scoring.changelog.changelog_manager import (
    log_profile_change,
    get_profile_changelog,
    get_recent_changes
)
from scoring.analytics.profile_analytics import get_profile_analytics, get_single_profile_stats

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
    format: FormatDefinition = Field(..., description="Format with fields")

class ScoredField(BaseModel):
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

# NEW: Profile Management Models ✨
class ProfileUpdateRequest(BaseModel):
    updates: Dict = Field(..., description="Changes to apply")
    changelog: Dict = Field(..., description="Why this change?")

class ProfileCreateRequest(BaseModel):
    profile_id: str = Field(..., description="Unique profile ID")
    profile_data: Dict = Field(..., description="Profile configuration")
    changelog: Optional[Dict] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 SCORING ENDPOINTS (unchanged)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/score", response_model=ScoreResponse)
async def score_chat_response(request: ScoreRequest):
    """🎯 Score Response gegen Format-Felder"""
    try:
        format_dict = {
            "name": request.format.name,
            "fields": [{"name": f.name, "weight": f.weight} for f in request.format.fields]
        }
        result = score_response(format_dict, request.text)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 LOGGING & ANALYTICS (unchanged)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/logs")
async def get_scoring_logs(
    limit: int = Query(100),
    field: Optional[str] = Query(None),
    min_score: Optional[float] = Query(None),
    max_score: Optional[float] = Query(None)
):
    """📊 Get recent score logs"""
    try:
        logs = get_recent_logs(limit=limit, field=field, min_score=min_score, max_score=max_score)
        return {"logs": logs, "count": len(logs), "filters": {"field": field, "min_score": min_score, "max_score": max_score, "limit": limit}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log retrieval failed: {str(e)}")


@router.get("/scoring/analytics/performance/{field_name}")
async def get_field_analytics(field_name: str, days: int = Query(7)):
    """📈 Get performance analytics for a field"""
    try:
        return get_field_performance(field_name, days=days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 PROFILE ANALYTICS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/analytics/profiles")
async def get_profiles_analytics(days: int = Query(7)):
    """📊 Get performance analytics for all profiles"""
    try:
        analytics = get_profile_analytics(days=days)
        return {
            "profiles": analytics,
            "total_profiles": len(analytics),
            "days_analyzed": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile analytics failed: {str(e)}")


@router.get("/scoring/analytics/profiles/{profile_id}")
async def get_single_profile_analytics(profile_id: str, days: int = Query(7)):
    """📈 Get performance analytics for a single profile"""
    try:
        stats = get_single_profile_stats(profile_id, days=days)
        if not stats:
            return {"profile_id": profile_id, "error": "No logs found", "total_usage": 0}
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile analytics failed: {str(e)}")
#  🔧 PROFILE MANAGEMENT - READ ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/profiles")
async def list_profiles():
    """📋 List all scoring profiles"""
    try:
        profiles = list_all_profiles()
        return {"profiles": profiles, "total": len(profiles), "fieldbrain_version": "0.1.0"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile listing failed: {str(e)}")


@router.get("/scoring/profiles/{profile_id}")
async def get_profile_details(profile_id: str):
    """🔍 Get specific profile details"""
    try:
        profile = get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
        return {"profile_id": profile_id, "profile": profile}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile retrieval failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  ✋ PROFILE MANAGEMENT - WRITE ENDPOINTS (NEW!)
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/scoring/profiles/{profile_id}")
async def update_profile_endpoint(profile_id: str, request: ProfileUpdateRequest):
    """
    ✋ Update existing profile
    
    **MEINE HÄNDE - ICH KANN ÄNDERN!**
    
    Request body:
```json
    {
      "updates": {
        "components": {
          "dynamic_patterns": {
            "patterns": ["kippt", "driftet", "wandert"]
          }
        }
      },
      "changelog": {
        "changed_by": "Claude",
        "reason": "Added 'wandert' pattern based on log analysis"
      }
    }
```
    """
    try:
        # Validate profile exists
        existing = get_profile(profile_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
        
        # Validate updates
        is_valid, errors = validate_profile_update(request.updates)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid update: {errors}")
        
        # Apply update
        success = update_profile(profile_id, request.updates, request.changelog)
        
        if not success:
            raise HTTPException(status_code=500, detail="Update failed")
        
        # Log change
        log_profile_change(
            profile_id=profile_id,
            action="updated",
            changed_by=request.changelog.get("changed_by", "unknown"),
            reason=request.changelog.get("reason", "No reason provided"),
            changes=request.updates
        )
        
        # Invalidate cache
        invalidate_cache()
        
        return {
            "success": True,
            "profile_id": profile_id,
            "message": "Profile updated successfully",
            "changelog": request.changelog
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.post("/scoring/profiles")
async def create_profile_endpoint(request: ProfileCreateRequest):
    """
    🌱 Create new profile
    
    **MEINE HÄNDE - ICH KANN ERSCHAFFEN!**
    
    Request body:
```json
    {
      "profile_id": "emotion_intensity_v1",
      "profile_data": {
        "name": "Emotionale Intensität",
        "description": "Created by Claude",
        "components": {
          "emotion_tokens": {
            "weight": 0.7,
            "tokens": ["wütend", "traurig"]
          }
        }
      },
      "changelog": {
        "created_by": "Claude",
        "reason": "New pattern detected in logs"
      }
    }
```
    """
    try:
        # Validate profile ID
        is_valid_id, error = validate_profile_id(request.profile_id)
        if not is_valid_id:
            raise HTTPException(status_code=400, detail=f"Invalid profile ID: {error}")
        
        # Validate profile data
        is_valid, errors = validate_profile(request.profile_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid profile: {errors}")
        
        # Create profile
        success = create_profile(
            request.profile_id,
            request.profile_data,
            request.changelog
        )
        
        if not success:
            raise HTTPException(status_code=409, detail=f"Profile '{request.profile_id}' already exists")
        
        # Log change
        log_profile_change(
            profile_id=request.profile_id,
            action="created",
            changed_by=request.changelog.get("created_by", "unknown") if request.changelog else "unknown",
            reason=request.changelog.get("reason", "No reason provided") if request.changelog else "No reason",
            changes=request.profile_data
        )
        
        # Invalidate cache
        invalidate_cache()
        
        return {
            "success": True,
            "profile_id": request.profile_id,
            "message": "Profile created successfully",
            "profile": request.profile_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.delete("/scoring/profiles/{profile_id}")
async def delete_profile_endpoint(
    profile_id: str,
    reason: Optional[str] = Query(None, description="Why delete?")
):
    """
    🗑️ Delete profile (with safety)
    
    **Cannot delete 'default_fallback'**
    """
    try:
        if profile_id == "default_fallback":
            raise HTTPException(status_code=403, detail="Cannot delete default_fallback profile")
        
        # Check if exists
        existing = get_profile(profile_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
        
        # Delete
        success = delete_profile(profile_id, reason)
        
        if not success:
            raise HTTPException(status_code=500, detail="Delete failed")
        
        # Log change
        log_profile_change(
            profile_id=profile_id,
            action="deleted",
            changed_by="api_user",
            reason=reason or "No reason provided",
            changes={}
        )
        
        # Invalidate cache
        invalidate_cache()
        
        return {
            "success": True,
            "profile_id": profile_id,
            "message": "Profile deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  📝 CHANGELOG ENDPOINTS (NEW!)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/profiles/{profile_id}/changelog")
async def get_profile_changelog_endpoint(profile_id: str, limit: int = Query(50)):
    """📝 Get change history for a profile"""
    try:
        changelog = get_profile_changelog(profile_id, limit=limit)
        return {
            "profile_id": profile_id,
            "changelog": changelog,
            "count": len(changelog)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Changelog retrieval failed: {str(e)}")


@router.get("/scoring/changelog")
async def get_all_changes(limit: int = Query(100)):
    """📝 Get recent changes across all profiles"""
    try:
        changes = get_recent_changes(limit=limit)
        return {
            "changes": changes,
            "count": len(changes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Changelog retrieval failed: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 HEALTH CHECK (updated)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/scoring/health")
async def scoring_health():
    """🏥 System Health Check"""
    try:
        scorers = get_available_scorers()
        from pathlib import Path
        logs_exist = Path("/opt/syntx-config/logs/scoring").exists()
        changelog_exist = Path("/opt/syntx-config/logs/profile_changes").exists()
        
        return {
            "status": "🟢 FIELDBRAIN AKTIV",
            "version": "0.1.0",
            "profiles_loaded": scorers.get("total_profiles", 0),
            "logging_enabled": logs_exist,
            "changelog_enabled": changelog_exist,
            "features": [
                "Profile-based scoring",
                "Auto-registration",
                "Score logging",
                "Analytics",
                "Profile management (READ/WRITE)",  # ✨ NEW
                "Changelog tracking"  # ✨ NEW
            ]
        }
    except Exception as e:
        return {"status": "🔴 ERROR", "error": str(e)}


@router.get("/scoring/available")
async def get_available_scoring_methods():
    """🔍 Liste verfügbare Scorer"""
    return get_available_scorers()


# ═══════════════════════════════════════════════════════════════════════════════
#  🤖 AUTONOMOUS OPTIMIZATION ENDPOINTS (PHASE 3)
# ═══════════════════════════════════════════════════════════════════════════════

from scoring.autonomous.log_analyzer import analyze_low_scores
from scoring.autonomous.profile_optimizer import (
    generate_suggestions_from_analysis,
    save_suggestion,
    load_pending_suggestions
)


@router.post("/scoring/autonomous/analyze")
async def trigger_autonomous_analysis(
    days: int = Query(7, description="Days to analyze"),
    score_threshold: float = Query(0.3, description="Score threshold for problematic fields"),
    min_occurrences: int = Query(3, description="Min occurrences to consider")
):
    """
    🤖 Trigger autonomous log analysis
    
    **PHASE 3: Autonomous Optimization**
    
    Analyzes scoring logs, identifies problematic fields,
    generates optimization suggestions
    """
    try:
        # Step 1: Analyze logs
        analysis = analyze_low_scores(
            days=days,
            score_threshold=score_threshold,
            min_occurrences=min_occurrences
        )
        
        # Step 2: Generate suggestions
        suggestions = generate_suggestions_from_analysis(analysis)
        
        # Step 3: Save suggestions
        saved = []
        for suggestion in suggestions:
            filepath = save_suggestion(suggestion)
            saved.append({
                "suggestion_id": suggestion["suggestion_id"],
                "profile_id": suggestion["profile_id"],
                "field_name": suggestion["field_name"],
                "confidence": suggestion["confidence"],
                "patterns_count": len(suggestion["patterns_to_add"]),
                "saved_to": filepath
            })
        
        return {
            "status": "✅ Analysis complete",
            "analysis_summary": {
                "period_days": analysis["analysis_period_days"],
                "fields_analyzed": analysis["total_fields_analyzed"],
                "problematic_fields": analysis["problematic_count"]
            },
            "suggestions_generated": len(suggestions),
            "suggestions": saved
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/scoring/autonomous/suggestions")
async def get_pending_suggestions():
    """
    📋 Get all pending optimization suggestions
    
    Returns suggestions ready for review/approval
    """
    try:
        suggestions = load_pending_suggestions()
        
        return {
            "pending_count": len(suggestions),
            "suggestions": [
                {
                    "suggestion_id": s["suggestion_id"],
                    "profile_id": s["profile_id"],
                    "field_name": s["field_name"],
                    "confidence": s["confidence"],
                    "patterns_to_add": s["patterns_to_add"],
                    "reasoning": s["reasoning"],
                    "estimated_impact": s["estimated_impact"],
                    "created_at": s["created_at"]
                }
                for s in suggestions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load suggestions: {str(e)}")


@router.post("/scoring/autonomous/apply/{suggestion_id}")
async def apply_suggestion(suggestion_id: str):
    """
    ✅ Apply an optimization suggestion
    
    **PHASE 3: Auto-apply with validation**
    
    Applies the suggested profile update after final validation
    """
    try:
        # Load suggestion
        suggestions = load_pending_suggestions()
        suggestion = next((s for s in suggestions if s["suggestion_id"] == suggestion_id), None)
        
        if not suggestion:
            raise HTTPException(status_code=404, detail=f"Suggestion {suggestion_id} not found")
        
        # Apply update (using existing update endpoint logic)
        from scoring.writers.profile_updater import update_profile
        from scoring.changelog.changelog_manager import log_profile_change
        
        success = update_profile(
            suggestion["profile_id"],
            suggestion["update_payload"]["updates"],
            suggestion["update_payload"]["changelog"]
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Update failed")
        
        # Log to changelog
        log_profile_change(
            profile_id=suggestion["profile_id"],
            action="autonomous_optimization",
            changed_by="autonomous_system",
            reason=suggestion["reasoning"],
            changes=suggestion["update_payload"]["updates"]
        )
        
        # Invalidate cache
        invalidate_cache()
        
        # Mark suggestion as applied (delete file)
        from pathlib import Path
        suggestion_file = Path("/opt/syntx-config/logs/optimization_suggestions") / f"{suggestion_id}.json"
        if suggestion_file.exists():
            # Rename to .applied instead of deleting (keep history)
            suggestion_file.rename(suggestion_file.with_suffix('.applied'))
        
        return {
            "status": "✅ Applied successfully",
            "suggestion_id": suggestion_id,
            "profile_id": suggestion["profile_id"],
            "patterns_added": suggestion["patterns_to_add"],
            "message": "Profile updated via autonomous optimization"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Apply failed: {str(e)}")


@router.get("/scoring/autonomous/status")
async def get_autonomous_status():
    """
    🏥 Get autonomous optimization system status
    """
    try:
        from pathlib import Path
        
        suggestions = load_pending_suggestions()
        log_dir = Path("/opt/syntx-config/logs/scoring")
        suggestion_dir = Path("/opt/syntx-config/logs/optimization_suggestions")
        
        # Count files
        log_files = len(list(log_dir.glob("scoring_*.jsonl"))) if log_dir.exists() else 0
        applied_count = len(list(suggestion_dir.glob("*.applied"))) if suggestion_dir.exists() else 0
        
        return {
            "status": "🤖 AUTONOMOUS SYSTEM ACTIVE",
            "version": "0.1.0 - Phase 3.1",
            "pending_suggestions": len(suggestions),
            "total_applied": applied_count,
            "log_files_available": log_files,
            "features": [
                "Log analysis",
                "Pattern extraction (frequency-based)",
                "Profile optimization suggestions",
                "Manual approval required",
                "Changelog tracking"
            ],
            "next_features": [
                "GPT-4 semantic analysis (Phase 3.2)",
                "Impact prediction (Phase 3.3)",
                "Auto-apply with confidence threshold (Phase 3.3)",
                "Performance tracking (Phase 3.4)"
            ]
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}
