"""
🔍 SYNTX FORMAT SCANNER
Scannt Responses gegen Format-Definitionen.
Findet: Fehlende Felder, Low-Quality, Inkohärenz.
"""
import re
from typing import Dict, List, Tuple, Optional
from .format_loader import load_format, get_format_fields


def parse_response_fields(response: str) -> Dict[str, str]:
    """
    📝 RESPONSE PARSEN
    
    Extrahiert Felder aus Response anhand ### HEADER: Pattern
    """
    fields = {}
    
    # Pattern: ### FELDNAME: oder ### FELDNAME (mit oder ohne Doppelpunkt)
    pattern = r'###\s*([A-ZÄÖÜa-zäöü_\-]+)[:\s]*\n(.*?)(?=###|\Z)'
    matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
    
    for header, content in matches:
        # Normalize header
        normalized = header.upper().strip().replace("-", "_").replace(" ", "_")
        fields[normalized] = content.strip()
    
    return fields


def scan_response(format_name: str, response: str, language: str = "de") -> Dict:
    """
    🔍 RESPONSE SCANNEN
    
    Hauptfunktion: Scannt Response gegen Format.
    
    Returns:
        {
            "format": str,
            "missing_fields": List[str],
            "low_quality_fields": List[Dict],
            "field_lengths": Dict[str, int],
            "field_scores": Dict[str, float],
            "coherence_score": float,
            "recommendations": List[str]
        }
    """
    format_data = load_format(format_name)
    if not format_data:
        return {"error": f"Format '{format_name}' nicht gefunden"}
    
    expected_fields = get_format_fields(format_name, language)
    parsed_fields = parse_response_fields(response)
    
    # 1. Missing Fields
    missing_fields = []
    for field in expected_fields:
        header = field["header"].upper().replace("-", "_").replace(" ", "_")
        # Check verschiedene Varianten
        found = False
        for parsed_header in parsed_fields.keys():
            if header in parsed_header or parsed_header in header:
                found = True
                break
        if not found:
            missing_fields.append(field["header"])
    
    # 2. Field Lengths
    field_lengths = {k: len(v) for k, v in parsed_fields.items()}
    
    # 3. Low Quality Fields
    low_quality_fields = []
    field_scores = {}
    
    for field in expected_fields:
        header = field["header"].upper().replace("-", "_").replace(" ", "_")
        content = None
        
        # Find matching content
        for parsed_header, parsed_content in parsed_fields.items():
            if header in parsed_header or parsed_header in header:
                content = parsed_content
                break
        
        if content is None:
            field_scores[field["header"]] = 0.0
            continue
        
        # Score berechnen
        score = 0.0
        reasons = []
        
        # Length Check
        min_len = field.get("validation", {}).get("min_length", 30)
        max_len = field.get("validation", {}).get("max_length", 3000)
        content_len = len(content)
        
        if content_len < min_len:
            reasons.append(f"too_short (min: {min_len})")
            score += 20
        elif content_len > max_len:
            reasons.append(f"too_long (max: {max_len})")
            score += 40
        else:
            score += 60
        
        # Keyword Check
        keywords = field.get("keywords", [])
        if isinstance(keywords, dict):
            keywords = keywords.get(language, keywords.get("de", []))
        
        keyword_hits = sum(1 for kw in keywords if kw.lower() in content.lower())
        keyword_ratio = keyword_hits / max(len(keywords), 1)
        score += keyword_ratio * 40
        
        if keyword_ratio < 0.2:
            reasons.append("low_keyword_match")
        
        field_scores[field["header"]] = round(score, 1)
        
        if score < 50 or reasons:
            low_quality_fields.append({
                "field": field["header"],
                "score": round(score, 1),
                "length": content_len,
                "reasons": reasons
            })
    
    # 4. Coherence Score (Durchschnitt aller Feld-Scores)
    scores = [s for s in field_scores.values() if s > 0]
    coherence_score = round(sum(scores) / max(len(scores), 1), 1)
    
    # Penalty für fehlende Felder
    missing_penalty = len(missing_fields) * 10
    coherence_score = max(0, coherence_score - missing_penalty)
    
    # 5. Recommendations
    recommendations = []
    
    for field in missing_fields:
        recommendations.append(f"❌ Feld '{field}' fehlt komplett")
    
    for lq in low_quality_fields:
        if "too_short" in str(lq.get("reasons", [])):
            recommendations.append(f"⚠️ Feld '{lq['field']}' zu kurz ({lq['length']} chars)")
        if "low_keyword_match" in str(lq.get("reasons", [])):
            recommendations.append(f"⚠️ Feld '{lq['field']}' hat wenig relevante Keywords")
    
    if coherence_score < 50:
        recommendations.append("🔴 Gesamtkohärenz kritisch niedrig - Response neu generieren")
    elif coherence_score < 70:
        recommendations.append("🟡 Gesamtkohärenz verbesserungswürdig")
    else:
        recommendations.append("🟢 Gesamtkohärenz akzeptabel")
    
    return {
        "format": format_name,
        "fields_expected": len(expected_fields),
        "fields_found": len(parsed_fields),
        "missing_fields": missing_fields,
        "low_quality_fields": low_quality_fields,
        "field_lengths": field_lengths,
        "field_scores": field_scores,
        "coherence_score": coherence_score,
        "recommendations": recommendations
    }
