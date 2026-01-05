"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🎯 PATTERN EXTRACTOR - Der Entdecker                                        ║
║                                                                              ║
║  Hybrid Model (GPT-validated):                                               ║
║  1. Frequency Analysis (baseline)                                            ║
║  2. GPT-4 Semantic Clustering (high-precision)                               ║
║  3. Embedding Analysis (optional, for future)                                ║
║                                                                              ║
║  "Patterns verstecken sich in Wiederholung und Resonanz." 💎                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, List, Set
from collections import Counter
import re
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scoring.core.profile_reader import get_profile


# ═══════════════════════════════════════════════════════════════════════════════
#  🔤 TOKENIZE TEXT
# ═══════════════════════════════════════════════════════════════════════════════

def tokenize(text: str) -> List[str]:
    """
    Simple tokenization: lowercase, remove punctuation, split
    """
    # Lowercase
    text = text.lower()
    
    # Remove punctuation but keep umlauts
    text = re.sub(r'[^\wäöüß\s-]', ' ', text)
    
    # Split and filter short tokens
    tokens = [t for t in text.split() if len(t) > 2]
    
    return tokens


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 FREQUENCY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_frequent_terms(
    sample_texts: List[str],
    min_frequency: int = 3,
    max_terms: int = 20
) -> List[Dict]:
    """
    🔍 Step 1: Frequency-based pattern discovery
    
    Returns list of candidate terms with frequency
    """
    all_tokens = []
    for text in sample_texts:
        all_tokens.extend(tokenize(text))
    
    # Count frequencies
    term_counts = Counter(all_tokens)
    
    # Filter stopwords (basic German stopwords)
    stopwords = {
        'der', 'die', 'das', 'und', 'ist', 'ein', 'eine', 'mit', 
        'von', 'für', 'auf', 'als', 'dem', 'den', 'des', 'sich',
        'nicht', 'auch', 'werden', 'aus', 'bei', 'nach', 'um',
        'wird', 'durch', 'kann', 'oder', 'sind', 'hat', 'wie'
    }
    
    # Get frequent terms
    candidates = []
    for term, count in term_counts.most_common(max_terms * 2):  # Get extra for filtering
        if term not in stopwords and count >= min_frequency:
            candidates.append({
                "term": term,
                "frequency": count,
                "sample_count": len(sample_texts),
                "ratio": round(count / len(sample_texts), 2)
            })
    
    return candidates[:max_terms]


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 FILTER EXISTING PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

def get_existing_patterns(profile_id: str) -> Set[str]:
    """
    Get all patterns/tokens already in a profile
    """
    profile = get_profile(profile_id)
    if not profile:
        return set()
    
    patterns = set()
    
    # Extract from all components
    components = profile.get("components", {})
    for component_name, component_data in components.items():
        # Check for 'patterns' key
        if "patterns" in component_data:
            patterns.update(p.lower() for p in component_data["patterns"])
        
        # Check for 'tokens' key
        if "tokens" in component_data:
            patterns.update(t.lower() for t in component_data["tokens"])
    
    return patterns


def filter_novel_patterns(
    candidates: List[Dict],
    profile_id: str
) -> List[Dict]:
    """
    🔍 Remove patterns that already exist in profile
    """
    existing = get_existing_patterns(profile_id)
    
    novel = []
    for candidate in candidates:
        term = candidate["term"].lower()
        
        # Check if term (or very similar) already exists
        if term not in existing:
            # Also check for partial matches (e.g. "wandern" vs "wandert")
            stem = term[:4] if len(term) > 4 else term  # Simple stemming
            is_similar = any(stem in ex or ex in term for ex in existing)
            
            if not is_similar:
                novel.append(candidate)
    
    return novel


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 EXTRACT MISSING PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_missing_patterns(
    field_name: str,
    sample_texts: List[str],
    profile_id: str,
    min_frequency: int = 3,
    max_patterns: int = 10
) -> Dict:
    """
    🎯 Main function: Extract patterns missing from profile
    
    GPT-validated Hybrid Model:
    1. Frequency analysis
    2. Filter existing patterns
    3. Rank by relevance
    
    Returns:
        {
            "field_name": "...",
            "profile_id": "...",
            "sample_count": 10,
            "missing_patterns": [
                {
                    "term": "wandert",
                    "frequency": 8,
                    "confidence": 0.75,
                    "reason": "Appears 8 times in 10 low-score samples"
                }
            ]
        }
    """
    # Step 1: Frequency analysis
    frequent_terms = extract_frequent_terms(
        sample_texts,
        min_frequency=min_frequency,
        max_terms=max_patterns * 2
    )
    
    # Step 2: Filter existing patterns
    novel_patterns = filter_novel_patterns(frequent_terms, profile_id)
    
    # Step 3: Calculate confidence and rank
    results = []
    for pattern in novel_patterns[:max_patterns]:
        # Simple confidence based on frequency ratio
        confidence = min(0.95, pattern["ratio"] * 1.5)  # Cap at 0.95
        
        results.append({
            "term": pattern["term"],
            "frequency": pattern["frequency"],
            "sample_ratio": pattern["ratio"],
            "confidence": round(confidence, 2),
            "reason": f"Appears {pattern['frequency']} times in {pattern['sample_count']} samples (not in profile)"
        })
    
    return {
        "field_name": field_name,
        "profile_id": profile_id,
        "sample_count": len(sample_texts),
        "analysis_method": "frequency_baseline",
        "missing_patterns": results,
        "pattern_count": len(results)
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🧪 GPT-4 SEMANTIC ANALYSIS (Phase 3.2)
# ═══════════════════════════════════════════════════════════════════════════════

def extract_patterns_with_gpt(
    field_name: str,
    sample_texts: List[str],
    profile_id: str,
    existing_patterns: List[str]
) -> Dict:
    """
    🤖 GPT-4 powered semantic pattern extraction
    
    TODO: Implement in Phase 3.2
    - Send samples + existing patterns to GPT-4
    - Ask for semantic analysis
    - Extract high-precision patterns
    
    For now: placeholder
    """
    return {
        "status": "not_implemented",
        "message": "GPT-4 semantic analysis coming in Phase 3.2",
        "method": "gpt4_semantic_clustering"
    }
