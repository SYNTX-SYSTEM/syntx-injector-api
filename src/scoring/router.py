"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧠 SYNTX SCORING ROUTER v2.1 - FIELDBRAIN + LOGGING                         ║
║                                                                              ║
║  Format-based field scoring mit Dynamic Profiles + Score Logging.           ║
║  Jeder Score wird geloggt für Analytics & Optimization.                     ║
║                                                                              ║
║  "Das System denkt in Profilen und lernt aus Geschichte." 💎                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, List, Any

# FIELDBRAIN Modules
from .core.profile_reader import get_profile, get_profile_for_field
from .dynamic_scorer import score_with_profile
from .registry import ensure_field_registered
from .logger import log_score  # NEW


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 MAIN SCORING FUNCTION - FIELDBRAIN + LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

def score_response(format_data: Dict, response_text: str) -> Dict[str, Any]:
    """
    🧠 Score LLM response based on format fields - FIELDBRAIN v0.1 + Logging
    
    **NEW: Score Logging**
    - Jeder Score wird in /opt/syntx-logs/scoring/ geloggt
    - JSONL Format für Analytics
    - Field, Score, Profile, Components
    
    Args:
        format_data: Format definition with fields
        response_text: The LLM response to score
    
    Returns:
        Score result with logged entries
    """
    
    # Extract fields from format
    fields = format_data.get("fields", [])
    format_name = format_data.get("name", "unknown")
    
    if not fields:
        return {
            "error": "No fields in format",
            "scored_fields": [],
            "total_score": 0.0,
            "format_name": format_name,
            "field_count": 0
        }
    
    scored_fields = []
    total_weighted_score = 0.0
    
    for field in fields:
        field_name = field.get("name", "")
        field_weight = field.get("weight", 1.0)
        
        # 🌱 STEP 1: Ensure field is registered
        field_meta = ensure_field_registered(field_name)
        
        # 🎯 STEP 2: Get profile for this field
        profile_id = get_profile_for_field(field_name)
        profile = get_profile(profile_id)
        
        if not profile:
            profile_id = "default_fallback"
            profile = get_profile(profile_id)
        
        # ⚡ STEP 3: Score with profile
        score_result = score_with_profile(
            profile,
            response_text,
            keywords=field_meta.get("keywords", [])
        )
        
        # Calculate weighted score
        score = score_result["score"]
        weighted_score = score * field_weight
        total_weighted_score += weighted_score
        
        # 📊 STEP 4: LOG THE SCORE (NEW!)
        try:
            log_score(
                field_name=field_name,
                score=score,
                text=response_text,
                profile_used=profile_id,
                components=score_result.get("components", {}),
                metadata={
                    "format": format_name,
                    "weight": field_weight,
                    "weighted_score": weighted_score
                }
            )
        except Exception as e:
            # Don't fail scoring if logging fails
            print(f"⚠️ Logging failed for {field_name}: {e}")
        
        # Add to results
        scored_fields.append({
            "name": field_name,
            "score": score,
            "weight": field_weight,
            "weighted_score": round(weighted_score, 2),
            "profile_used": profile_id,
            "profile_name": profile.get("name", "Unknown"),
            "strategy": score_result.get("strategy", "Unknown"),
            "components": score_result.get("components", {}),
            "auto_registered": field_meta.get("auto_registered", False)
        })
    
    # Calculate total score (normalize by sum of weights)
    total_weight = sum(f.get("weight", 1.0) for f in fields)
    normalized_total_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    return {
        "scored_fields": scored_fields,
        "total_score": round(normalized_total_score, 2),
        "format_name": format_name,
        "field_count": len(fields),
        "total_weight": total_weight,
        "fieldbrain_version": "0.1.0",
        "logging_enabled": True  # NEW
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  📋 AVAILABLE SCORERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_available_scorers() -> Dict[str, Any]:
    """
    🔍 Get list of available scoring profiles
    
    Returns profiles instead of hardcoded functions
    """
    from .core.profile_reader import list_all_profiles
    
    profiles = list_all_profiles()
    
    return {
        "profiles": profiles,
        "total_profiles": len(profiles),
        "fieldbrain_version": "0.1.0",
        "note": "🧠 FIELDBRAIN aktiv - Profile-based scoring"
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 FIELDBRAIN v0.1 + LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
# Profile-based scoring with persistent logging.
# Every score becomes training data. 💎⚡🌊
