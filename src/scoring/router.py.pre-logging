"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧠 SYNTX SCORING ROUTER v2.0 - FIELDBRAIN EDITION                           ║
║                                                                              ║
║  Format-based field scoring mit Dynamic Profiles.                           ║
║  Keine hardcoded Scorer mehr. Nur Profile.                                  ║
║                                                                              ║
║  "Das System denkt in Profilen, nicht in Code." 💎                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, List, Any

# FIELDBRAIN Modules
from .profile_loader import get_profile, get_profile_for_field
from .dynamic_scorer import score_with_profile
from .registry import ensure_field_registered


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 MAIN SCORING FUNCTION - FIELDBRAIN POWERED
# ═══════════════════════════════════════════════════════════════════════════════

def score_response(format_data: Dict, response_text: str) -> Dict[str, Any]:
    """
    🧠 Score LLM response based on format fields - FIELDBRAIN v0.1
    
    **NEW: Profile-Based Scoring**
    - Jedes Feld nutzt ein Profile aus scoring_profiles.json
    - Auto-Registration von unbekannten Feldern
    - Dynamische Component Execution
    - Keine hardcoded Scorer mehr
    
    Args:
        format_data: Format definition with fields
            {
                "name": "syntx_true_raw",
                "fields": [
                    {"name": "driftkorper", "weight": 1.0},
                    {"name": "kalibrierung", "weight": 1.0},
                    {"name": "stromung", "weight": 0.7}
                ]
            }
        response_text: The LLM response to score
    
    Returns:
        {
            "scored_fields": [
                {
                    "name": "driftkorper",
                    "score": 0.75,
                    "weight": 1.0,
                    "weighted_score": 0.75,
                    "profile_used": "dynamic_language_v1",
                    "components": {...}
                },
                ...
            ],
            "total_score": 0.82,
            "format_name": "syntx_true_raw",
            "field_count": 3,
            "fieldbrain_version": "0.1.0"
        }
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
        
        # 🌱 STEP 1: Ensure field is registered (lazy auto-registration)
        field_meta = ensure_field_registered(field_name)
        
        # 🎯 STEP 2: Get profile for this field
        profile_id = get_profile_for_field(field_name)
        profile = get_profile(profile_id)
        
        if not profile:
            # Fallback if profile not found
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
        "fieldbrain_version": "0.1.0"
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  📋 AVAILABLE SCORERS - NOW PROFILE-BASED
# ═══════════════════════════════════════════════════════════════════════════════

def get_available_scorers() -> Dict[str, Any]:
    """
    🔍 Get list of available scoring profiles
    
    **NEW: Returns profiles instead of hardcoded functions**
    
    Returns:
        {
            "profiles": {
                "default_fallback": {...},
                "flow_bidir_v1": {...},
                ...
            },
            "total_profiles": 4,
            "fieldbrain_version": "0.1.0"
        }
    """
    from .profile_loader import list_all_profiles
    
    profiles = list_all_profiles()
    
    return {
        "profiles": profiles,
        "total_profiles": len(profiles),
        "fieldbrain_version": "0.1.0",
        "note": "🧠 FIELDBRAIN aktiv - Profile-based scoring"
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 DAS IST FIELDBRAIN v0.1
# ═══════════════════════════════════════════════════════════════════════════════
# Keine hardcoded Scorer. Nur Profiles.
# Auto-Registration. Dynamic Execution.
# GPT kann tweaken. System lernt. 💎⚡🌊
