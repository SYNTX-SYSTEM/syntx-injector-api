"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚡ SYNTX DYNAMIC SCORER - DAS AUSFÜHRUNGS-MODUL                             ║
║                                                                              ║
║  Executiert Scoring basierend auf Profiles.                                 ║
║  Strategy Router → Component Runner → Profile Math                          ║
║                                                                              ║
║  "Code ist tot. Profiles sind lebendig." 💎                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import re
from typing import Dict, List


# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 COMPONENT RUNNERS - DIE SCORING-MOTOREN
# ═══════════════════════════════════════════════════════════════════════════════

def run_keyword_density(text: str, keywords: List[str], normalize_at: float) -> float:
    """
    📊 Keyword Density Scorer
    
    Formula:
        matches / total_words * 100 / normalize_at
    
    Args:
        text: Input text
        keywords: List of keywords to search
        normalize_at: Normalization threshold (e.g. 5.0)
    
    Returns:
        Score 0.0-1.0
    """
    text_lower = text.lower()
    total_matches = sum(text_lower.count(kw.lower()) for kw in keywords)
    
    words = text_lower.split()
    if not words:
        return 0.0
    
    density = (total_matches / len(words)) * 100
    score = min(density / normalize_at, 1.0)
    
    return round(score, 2)


def run_context_presence(
    text: str, 
    keywords: List[str], 
    min_keywords_per_sentence: int
) -> float:
    """
    🔍 Context Presence Scorer
    
    Logic:
        Sätze mit 2+ Keywords = stärkerer Context
    
    Args:
        text: Input text
        keywords: Keywords to search
        min_keywords_per_sentence: Minimum matches per sentence
    
    Returns:
        Score 0.0-1.0
    """
    text_lower = text.lower()
    sentences = re.split(r'[.!?]+', text_lower)
    
    context_score = 0.0
    for sentence in sentences:
        matches_in_sentence = sum(1 for kw in keywords if kw.lower() in sentence)
        if matches_in_sentence >= min_keywords_per_sentence:
            context_score += 0.3
        elif matches_in_sentence == 1:
            context_score += 0.1
    
    return min(round(context_score, 2), 1.0)


def run_pattern_match(text: str, patterns: List[str], normalize_at: float) -> float:
    """
    🎯 Pattern Match Scorer
    
    Uses regex patterns to detect structures
    
    Args:
        text: Input text
        patterns: Regex patterns
        normalize_at: Normalization threshold
    
    Returns:
        Score 0.0-1.0
    """
    total_matches = 0
    for pattern in patterns:
        matches = len(re.findall(pattern, text, re.IGNORECASE))
        total_matches += matches
    
    score = min(total_matches / normalize_at, 1.0)
    return round(score, 2)


def run_token_match(text: str, tokens: List[str], normalize_at: float) -> float:
    """
    🔤 Token Match Scorer
    
    Simple token counting with normalization
    
    Args:
        text: Input text
        tokens: Tokens to count
        normalize_at: Normalization threshold
    
    Returns:
        Score 0.0-1.0
    """
    text_lower = text.lower()
    total_matches = sum(text_lower.count(token.lower()) for token in tokens)
    
    score = min(total_matches / normalize_at, 1.0)
    return round(score, 2)


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 COMPONENT EXECUTOR - ROUTER
# ═══════════════════════════════════════════════════════════════════════════════

def execute_component(
    component_name: str,
    component_config: Dict,
    text: str,
    keywords: List[str] = None
) -> float:
    """
    🔀 Component Executor Router
    
    Routes to correct component runner based on config
    
    Args:
        component_name: e.g. "keyword_density", "pattern_match"
        component_config: Component configuration from profile
        text: Input text
        keywords: Optional keywords (for fallback)
    
    Returns:
        Component score 0.0-1.0
    """
    # Keyword Density
    if "normalize_at" in component_config and not "patterns" in component_config and not "tokens" in component_config:
        kws = keywords or []
        return run_keyword_density(
            text, 
            kws, 
            component_config["normalize_at"]
        )
    
    # Context Presence
    if "min_keywords_per_sentence" in component_config:
        kws = keywords or []
        return run_context_presence(
            text,
            kws,
            component_config["min_keywords_per_sentence"]
        )
    
    # Pattern Match
    if "patterns" in component_config:
        return run_pattern_match(
            text,
            component_config["patterns"],
            component_config.get("normalize_at", 3.0)
        )
    
    # Token Match (flow_tokens, dynamic_patterns, etc.)
    if "tokens" in component_config:
        return run_token_match(
            text,
            component_config["tokens"],
            component_config.get("normalize_at", 5.0)
        )
    
    # Unknown component type - return 0
    return 0.0


# ═══════════════════════════════════════════════════════════════════════════════
#  🧮 PROFILE MATH - WEIGHTED COMBINATION
# ═══════════════════════════════════════════════════════════════════════════════

def score_with_profile(
    profile: Dict,
    text: str,
    keywords: List[str] = None
) -> Dict:
    """
    🎯 Score text using a profile
    
    **The Heart of FIELDBRAIN**
    
    Args:
        profile: Profile dict from scoring_profiles.json
        text: Text to score
        keywords: Optional keywords (for fallback)
    
    Returns:
        {
            "score": 0.75,
            "components": {
                "keyword_density": {"score": 0.8, "weight": 0.6, "weighted": 0.48},
                "context_presence": {"score": 0.7, "weight": 0.4, "weighted": 0.28}
            },
            "profile_id": "default_fallback",
            "strategy": "keyword_density + context"
        }
    """
    components = profile.get("components", {})
    
    component_scores = {}
    total_weighted_score = 0.0
    total_weight = 0.0
    
    for comp_name, comp_config in components.items():
        # Execute component
        comp_score = execute_component(
            comp_name,
            comp_config,
            text,
            keywords
        )
        
        # Get weight
        comp_weight = comp_config.get("weight", 1.0)
        weighted_score = comp_score * comp_weight
        
        # Store
        component_scores[comp_name] = {
            "score": comp_score,
            "weight": comp_weight,
            "weighted": round(weighted_score, 2)
        }
        
        total_weighted_score += weighted_score
        total_weight += comp_weight
    
    # Normalize by total weight
    final_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
    
    return {
        "score": round(final_score, 2),
        "components": component_scores,
        "profile_name": profile.get("name", "Unknown"),
        "strategy": profile.get("strategy", "Unknown")
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 DAS IST FIELDBRAIN
# ═══════════════════════════════════════════════════════════════════════════════
# Scoring aus Daten, nicht Code.
# Profiles sind lebendig. Components sind modular.
# GPT kann tweaken. System lernt. 💎⚡🌊
