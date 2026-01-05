"""
SYNTX Fallback Scorer
Generic scoring for fields without specific heuristics
"""
import re
from typing import List

def _extract_keywords_from_field_name(field_name: str) -> List[str]:
    """
    Extract meaningful keywords from field name
    Examples:
        "driftkorper" -> ["drift", "korper"]
        "sigma_mechanismus" -> ["sigma", "mechanismus"]
        "emotionale_wirkung" -> ["emotionale", "wirkung", "emotion"]
    """
    # Remove prefixes like "sigma_", "syntx_"
    cleaned = re.sub(r'^(sigma|syntx|field)_', '', field_name.lower())
    
    # Split on underscores and camelCase
    parts = re.findall(r'[a-z]+', cleaned)
    
    # Add variations (e.g., "emotionale" -> "emotion")
    keywords = []
    for part in parts:
        keywords.append(part)
        # Add root forms for common German suffixes
        if part.endswith('ung'):
            keywords.append(part[:-3])  # "bewegung" -> "beweg"
        elif part.endswith('keit'):
            keywords.append(part[:-4])  # "geschwindigkeit" -> "geschwind"
        elif part.endswith('heit'):
            keywords.append(part[:-4])
    
    return list(set(keywords))  # Remove duplicates

def _calculate_keyword_density(text: str, keywords: List[str]) -> float:
    """
    Calculate keyword density in text
    Returns normalized score 0.0-1.0
    """
    text_lower = text.lower()
    word_count = len(text_lower.split())
    
    if word_count == 0:
        return 0.0
    
    # Count occurrences of each keyword
    total_matches = sum(text_lower.count(kw) for kw in keywords)
    
    # Normalize: density = matches / word_count * 100
    # Scale to 0-1 where 5% density = 1.0
    density = (total_matches / word_count) * 100
    return min(density / 5.0, 1.0)

def _calculate_context_presence(text: str, keywords: List[str]) -> float:
    """
    Check if keywords appear in meaningful context
    (not just mentions, but discussed)
    """
    text_lower = text.lower()
    sentences = re.split(r'[.!?]+', text_lower)
    
    context_score = 0.0
    for sentence in sentences:
        # Check if multiple keywords appear in same sentence
        matches_in_sentence = sum(1 for kw in keywords if kw in sentence)
        if matches_in_sentence >= 2:
            context_score += 0.3
        elif matches_in_sentence == 1:
            context_score += 0.1
    
    return min(context_score, 1.0)

def fallback_score(field_name: str, text: str) -> float:
    """
    Generic scoring for fields without specific heuristics
    
    Strategy:
    1. Extract keywords from field_name
    2. Calculate keyword density in text
    3. Check contextual presence
    4. Combine scores
    
    Args:
        field_name: Name of the field (e.g., "driftkorper", "sigma_mechanismus")
        text: Response text to score
    
    Returns:
        float: Score between 0.0 and 1.0
    
    Examples:
        >>> fallback_score("bewegung", "Das System bewegt sich dynamisch")
        0.75  # High score due to keyword match
        
        >>> fallback_score("unbekannt", "Keine relevanten Inhalte")
        0.1   # Low score, no matches
    """
    # Extract keywords from field name
    keywords = _extract_keywords_from_field_name(field_name)
    
    if not keywords:
        # If no keywords extracted, return minimal score
        return 0.1
    
    # Calculate components
    density_score = _calculate_keyword_density(text, keywords)
    context_score = _calculate_context_presence(text, keywords)
    
    # Weighted combination
    # 60% density (keyword frequency)
    # 40% context (meaningful discussion)
    final_score = (density_score * 0.6) + (context_score * 0.4)
    
    # Ensure minimum 0.1 for any non-empty text
    if len(text.strip()) > 0:
        final_score = max(final_score, 0.1)
    
    return round(final_score, 2)
