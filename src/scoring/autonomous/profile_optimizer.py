"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚙️ PROFILE OPTIMIZER - Der Vorschläger                                      ║
║                                                                              ║
║  Generiert konkrete Update-Vorschläge basierend auf Pattern-Analyse.        ║
║  "Optimierung ist nicht Veränderung. Optimierung ist Evolution." 💎          ║
║                                                                              ║
║  GPT-validated architecture with safety limits                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

from scoring.core.profile_reader import get_profile
from scoring.autonomous.pattern_extractor import extract_missing_patterns
from scoring.validators.profile_validator import validate_profile_update


# Safety limits (GPT-validated)
MAX_PATTERNS_PER_UPDATE = 5
MIN_CONFIDENCE_FOR_SUGGESTION = 0.3


# ═══════════════════════════════════════════════════════════════════════════════
#  ⚙️ GENERATE UPDATE SUGGESTION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_update_suggestion(
    field_name: str,
    profile_id: str,
    missing_patterns: List[Dict],
    max_patterns: int = MAX_PATTERNS_PER_UPDATE
) -> Dict:
    """
    ⚙️ Generate concrete update suggestion for a profile
    
    Returns:
        {
            "suggestion_id": "...",
            "profile_id": "...",
            "field_name": "...",
            "confidence": 0.75,
            "patterns_to_add": ["term1", "term2"],
            "reasoning": "...",
            "update_payload": {...},  # Ready to send to PUT /profiles/{id}
            "estimated_impact": {...}
        }
    """
    # Filter by confidence
    high_confidence = [
        p for p in missing_patterns 
        if p["confidence"] >= MIN_CONFIDENCE_FOR_SUGGESTION
    ]
    
    # Limit to max patterns (safety)
    selected = sorted(
        high_confidence, 
        key=lambda x: x["confidence"], 
        reverse=True
    )[:max_patterns]
    
    if not selected:
        return {
            "status": "no_suggestions",
            "reason": f"No patterns with confidence >= {MIN_CONFIDENCE_FOR_SUGGESTION}"
        }
    
    # Get current profile
    profile = get_profile(profile_id)
    if not profile:
        return {
            "status": "error",
            "reason": f"Profile {profile_id} not found"
        }
    
    # Determine which component to update
    # Strategy: Find first component with 'patterns' or 'tokens' key
    target_component = None
    target_key = None
    
    for comp_name, comp_data in profile.get("components", {}).items():
        if "patterns" in comp_data:
            target_component = comp_name
            target_key = "patterns"
            break
        elif "tokens" in comp_data:
            target_component = comp_name
            target_key = "tokens"
            break
    
    if not target_component:
        return {
            "status": "error",
            "reason": "No suitable component found in profile (needs 'patterns' or 'tokens' key)"
        }
    
    # Get current patterns
    current_patterns = profile["components"][target_component].get(target_key, [])
    
    # Build new pattern list
    new_terms = [p["term"] for p in selected]
    updated_patterns = current_patterns + new_terms
    
    # Build update payload
    update_payload = {
        "components": {
            target_component: {
                target_key: updated_patterns
            }
        }
    }
    
    # Validate update
    is_valid, errors = validate_profile_update(update_payload)
    if not is_valid:
        return {
            "status": "validation_error",
            "reason": f"Update validation failed: {errors}"
        }
    
    # Calculate aggregate confidence
    avg_confidence = sum(p["confidence"] for p in selected) / len(selected)
    
    # Build reasoning
    pattern_list = ", ".join(f"'{p['term']}' ({p['frequency']}x)" for p in selected)
    reasoning = (
        f"Analysis of {len(missing_patterns)} low-score samples for field '{field_name}' "
        f"identified {len(selected)} missing patterns: {pattern_list}. "
        f"Adding to {target_component}.{target_key}."
    )
    
    # Generate suggestion ID
    suggestion_id = f"{profile_id}_{field_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "status": "ready",
        "suggestion_id": suggestion_id,
        "profile_id": profile_id,
        "field_name": field_name,
        "confidence": round(avg_confidence, 2),
        "patterns_to_add": new_terms,
        "target_component": target_component,
        "target_key": target_key,
        "reasoning": reasoning,
        "update_payload": {
            "updates": update_payload,
            "changelog": {
                "changed_by": "autonomous_system",
                "reason": reasoning,
                "field_analyzed": field_name,
                "pattern_count": len(new_terms),
                "avg_confidence": round(avg_confidence, 2)
            }
        },
        "estimated_impact": {
            "patterns_before": len(current_patterns),
            "patterns_after": len(updated_patterns),
            "new_patterns": len(new_terms)
        },
        "created_at": datetime.now().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 GENERATE SUGGESTIONS FROM ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_suggestions_from_analysis(analysis_result: Dict) -> List[Dict]:
    """
    🎯 Generate update suggestions for all problematic fields
    
    Takes output from log_analyzer.analyze_low_scores()
    Returns list of suggestions
    """
    suggestions = []
    
    problematic_fields = analysis_result.get("problematic_fields", {})
    
    for field_name, field_data in problematic_fields.items():
        profile_id = field_data["profile_used"]
        sample_texts = field_data.get("all_samples", field_data.get("sample_texts", []))
        
        # Extract missing patterns
        pattern_analysis = extract_missing_patterns(
            field_name=field_name,
            sample_texts=sample_texts,
            profile_id=profile_id
        )
        
        # Generate suggestion
        suggestion = generate_update_suggestion(
            field_name=field_name,
            profile_id=profile_id,
            missing_patterns=pattern_analysis["missing_patterns"]
        )
        
        # Only add if ready
        if suggestion.get("status") == "ready":
            suggestions.append(suggestion)
    
    return suggestions


# ═══════════════════════════════════════════════════════════════════════════════
#  💾 SAVE/LOAD SUGGESTIONS
# ═══════════════════════════════════════════════════════════════════════════════

SUGGESTIONS_DIR = Path("/opt/syntx-logs/optimization_suggestions")
SUGGESTIONS_DIR.mkdir(parents=True, exist_ok=True)


def save_suggestion(suggestion: Dict) -> str:
    """💾 Save suggestion to file"""
    suggestion_id = suggestion["suggestion_id"]
    filepath = SUGGESTIONS_DIR / f"{suggestion_id}.json"
    
    with open(filepath, 'w') as f:
        json.dump(suggestion, f, indent=2)
    
    return str(filepath)


def load_pending_suggestions() -> List[Dict]:
    """📋 Load all pending suggestions"""
    suggestions = []
    
    for filepath in sorted(SUGGESTIONS_DIR.glob("*.json")):
        try:
            with open(filepath) as f:
                suggestion = json.load(f)
                # Only include if status is still "ready"
                if suggestion.get("status") == "ready":
                    suggestions.append(suggestion)
        except Exception as e:
            print(f"⚠️  Error loading {filepath}: {e}")
    
    return suggestions
