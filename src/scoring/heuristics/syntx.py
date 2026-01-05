"""
SYNTX Field-Specific Heuristic Scorers
Score range: 0.0 - 1.0
"""
import re
from typing import List

def _count_keywords(text: str, keywords: List[str]) -> float:
    """Helper: Count keyword occurrences, normalize to 0-1"""
    text_lower = text.lower()
    total_matches = sum(text_lower.count(kw.lower()) for kw in keywords)
    # Normalize: 0 matches = 0.0, 5+ matches = 1.0
    return min(total_matches / 5.0, 1.0)

def _has_dynamic_language(text: str) -> float:
    """Helper: Detect dynamic vs static language"""
    dynamic_indicators = [
        r'\bkippt\b', r'\bbewegt\b', r'\bwandelt\b', r'\bverändert\b',
        r'\bfließt\b', r'\bdriftet\b', r'\bschwingt\b', r'\bpendelt\b'
    ]
    matches = sum(1 for pattern in dynamic_indicators if re.search(pattern, text, re.IGNORECASE))
    return min(matches / 4.0, 1.0)

def _has_feedback_indicators(text: str) -> float:
    """Helper: Detect feedback loops and iterations"""
    feedback_patterns = [
        r'\bfeedback\b', r'\brückkopplung\b', r'\bschleife\b',
        r'\biterativ\b', r'\banpassung\b', r'\bkorrektur\b'
    ]
    matches = sum(1 for pattern in feedback_patterns if re.search(pattern, text, re.IGNORECASE))
    return min(matches / 3.0, 1.0)

def _has_flow_indicators(text: str) -> float:
    """Helper: Detect flow and bidirectional movement"""
    flow_patterns = [
        r'\bvon .+ nach\b', r'\bzwischen .+ und\b',
        r'\bwechselseitig\b', r'\bbidirektional\b',
        r'\btransfer\b', r'\baustausch\b'
    ]
    matches = sum(1 for pattern in flow_patterns if re.search(pattern, text, re.IGNORECASE))
    return min(matches / 3.0, 1.0)

# ═══════════════════════════════════════════════════════════════
# SYNTX FIELD SCORERS
# ═══════════════════════════════════════════════════════════════

def score_driftkorper(text: str) -> float:
    """
    Score DRIFTKORPER field (0.0-1.0)
    
    Evaluates:
    - Keywords: drift, bewegung, richtung, kippt, instabil, wandel
    - Dynamic language vs static
    - Directional indicators
    
    Weighting: 60% keywords, 40% dynamic language
    """
    keywords = [
        'drift', 'bewegung', 'richtung', 'kippt', 'instabil',
        'wandel', 'veränderung', 'dynamik', 'schwankung'
    ]
    
    keyword_score = _count_keywords(text, keywords)
    dynamic_score = _has_dynamic_language(text)
    
    return (keyword_score * 0.6) + (dynamic_score * 0.4)

def score_kalibrierung(text: str) -> float:
    """
    Score KALIBRIERUNG field (0.0-1.0)
    
    Evaluates:
    - Keywords: anpassung, justierung, abstimmung, korrektur
    - Feedback loops mentioned
    - Precision vs imprecision indicators
    
    Weighting: 50% keywords, 50% feedback indicators
    """
    keywords = [
        'kalibrierung', 'anpassung', 'justierung', 'abstimmung',
        'korrektur', 'präzision', 'ausrichtung', 'einstellen'
    ]
    
    keyword_score = _count_keywords(text, keywords)
    feedback_score = _has_feedback_indicators(text)
    
    return (keyword_score * 0.5) + (feedback_score * 0.5)

def score_stromung(text: str) -> float:
    """
    Score STRÖMUNG field (0.0-1.0)
    
    Evaluates:
    - Keywords: fluss, energie, transfer, austausch, strom
    - Flow dynamics indicators
    - Bidirectional movement
    
    Weighting: 50% keywords, 50% flow indicators
    """
    keywords = [
        'strömung', 'fluss', 'energie', 'transfer', 'austausch',
        'strom', 'zirkulation', 'bewegung', 'dynamik'
    ]
    
    keyword_score = _count_keywords(text, keywords)
    flow_score = _has_flow_indicators(text)
    
    return (keyword_score * 0.5) + (flow_score * 0.5)

# Additional SYNTX scorers can be added here:
# def score_subprotokoll(text: str) -> float: ...
# def score_tier(text: str) -> float: ...
# def score_resonanzsplit(text: str) -> float: ...
