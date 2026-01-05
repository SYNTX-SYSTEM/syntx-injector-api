"""
SYNTX Scoring Router
Main orchestration for format-based field scoring
"""
from typing import Dict, List, Any
import importlib
from .fallback import fallback_score

def score_response(format_data: Dict, response_text: str) -> Dict[str, Any]:
    """
    Score LLM response based on format fields
    
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
                    "weighted_score": 0.75
                },
                ...
            ],
            "total_score": 0.82,
            "format_name": "syntx_true_raw",
            "field_count": 3
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
    
    # Import syntx heuristics module
    try:
        from .heuristics import syntx
    except ImportError:
        syntx = None
    
    for field in fields:
        field_name = field.get("name", "")
        field_weight = field.get("weight", 1.0)
        
        # Try to find specific scorer
        scorer_func = None
        if syntx:
            scorer_func_name = f"score_{field_name.lower()}"
            scorer_func = getattr(syntx, scorer_func_name, None)
        
        # Score the field
        if scorer_func and callable(scorer_func):
            # Use specific heuristic
            score = scorer_func(response_text)
            scoring_method = "specific"
        else:
            # Use fallback
            score = fallback_score(field_name, response_text)
            scoring_method = "fallback"
        
        # Calculate weighted score
        weighted_score = score * field_weight
        total_weighted_score += weighted_score
        
        # Add to results
        scored_fields.append({
            "name": field_name,
            "score": round(score, 2),
            "weight": field_weight,
            "weighted_score": round(weighted_score, 2),
            "scoring_method": scoring_method
        })
    
    # Calculate total score (normalize by sum of weights)
    total_weight = sum(f.get("weight", 1.0) for f in fields)
    normalized_total_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    return {
        "scored_fields": scored_fields,
        "total_score": round(normalized_total_score, 2),
        "format_name": format_name,
        "field_count": len(fields),
        "total_weight": total_weight
    }


def get_available_scorers() -> Dict[str, List[str]]:
    """
    Get list of available specific scorers
    
    Returns:
        {
            "specific": ["driftkorper", "kalibrierung", "stromung"],
            "fallback": "Available for all fields"
        }
    """
    try:
        from .heuristics import syntx
        
        # Find all score_* functions
        specific_scorers = [
            name.replace("score_", "")
            for name in dir(syntx)
            if name.startswith("score_") and callable(getattr(syntx, name))
        ]
        
        return {
            "specific": specific_scorers,
            "fallback": "Available for all fields"
        }
    except ImportError:
        return {
            "specific": [],
            "fallback": "Available for all fields"
        }
