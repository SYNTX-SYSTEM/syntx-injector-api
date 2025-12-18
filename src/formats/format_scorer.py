"""
📊 SYNTX FORMAT SCORER
Bewertet Format-Definitionen selbst (nicht Responses).
Meta-reflexive Qualitätsanalyse.
"""
from typing import Dict, List, Set
from collections import Counter
from .format_loader import load_format, get_format_fields


def calculate_semantic_clarity(fields: List[Dict]) -> float:
    """
    📝 SEMANTISCHE KLARHEIT
    
    Bewertet wie sprechend/verständlich die Feldnamen sind.
    - Längere Namen = besser (bis 30 chars)
    - Keine kryptischen Abkürzungen
    - Underscore-Trennung OK
    """
    if not fields:
        return 0.0
    
    scores = []
    for field in fields:
        name = field.get("name", "")
        score = 0.0
        
        # Länge (optimal: 8-25 chars)
        length = len(name)
        if 8 <= length <= 25:
            score += 40
        elif 5 <= length < 8:
            score += 25
        elif length > 25:
            score += 30
        else:
            score += 10
        
        # Keine reinen Abkürzungen (weniger als 4 chars ohne underscore)
        parts = name.split("_")
        abbrev_count = sum(1 for p in parts if len(p) <= 2)
        if abbrev_count == 0:
            score += 30
        elif abbrev_count == 1:
            score += 20
        else:
            score += 5
        
        # Hat Description
        desc = field.get("description", {})
        if isinstance(desc, dict) and desc.get("de"):
            desc_len = len(desc.get("de", ""))
            if desc_len > 50:
                score += 30
            elif desc_len > 20:
                score += 20
            else:
                score += 10
        
        scores.append(min(score, 100))
    
    return round(sum(scores) / len(scores), 1)


def calculate_redundancy(fields: List[Dict], language: str = "de") -> Dict:
    """
    🔄 REDUNDANZ-CHECK
    
    Findet Keyword-Überlappungen zwischen Feldern.
    """
    keyword_sets = {}
    
    for field in fields:
        name = field.get("name", "unknown")
        keywords = field.get("keywords", {})
        if isinstance(keywords, dict):
            keywords = keywords.get(language, keywords.get("de", []))
        keyword_sets[name] = set(kw.lower() for kw in keywords)
    
    # Paarweise Überlappung
    overlaps = []
    field_names = list(keyword_sets.keys())
    
    for i, name1 in enumerate(field_names):
        for name2 in field_names[i+1:]:
            common = keyword_sets[name1] & keyword_sets[name2]
            if len(common) >= 2:
                overlaps.append({
                    "fields": [name1, name2],
                    "common_keywords": list(common)
                })
    
    return {
        "overlap_count": len(overlaps),
        "overlapping_pairs": overlaps
    }


def calculate_field_balance(fields: List[Dict]) -> Dict:
    """
    ⚖️ FELD-BALANCE
    
    Prüft ob Gewichtungen ausgewogen sind.
    """
    weights = [f.get("weight", 0) for f in fields]
    
    if not weights or sum(weights) == 0:
        return {"status": "NO_WEIGHTS", "details": "Keine Gewichtungen definiert"}
    
    avg = sum(weights) / len(weights)
    variance = sum((w - avg) ** 2 for w in weights) / len(weights)
    std_dev = variance ** 0.5
    
    # Bewertung
    if std_dev < 3:
        status = "EXCELLENT"
    elif std_dev < 5:
        status = "OK"
    elif std_dev < 10:
        status = "UNBALANCED"
    else:
        status = "CRITICAL"
    
    return {
        "status": status,
        "avg_weight": round(avg, 1),
        "std_deviation": round(std_dev, 1),
        "min_weight": min(weights),
        "max_weight": max(weights),
        "total": sum(weights)
    }


def calculate_i18n_score(format_data: Dict) -> Dict:
    """
    🌍 I18N SCORE
    
    Prüft Internationalisierungs-Vollständigkeit.
    """
    languages = format_data.get("languages", ["de"])
    fields = format_data.get("fields", [])
    
    if not fields:
        return {"score": 0, "details": "Keine Felder"}
    
    complete_count = 0
    incomplete_fields = []
    
    for field in fields:
        is_complete = True
        
        # Description check
        desc = field.get("description", {})
        for lang in languages:
            if not desc.get(lang):
                is_complete = False
                break
        
        # Headers check
        headers = field.get("headers", {})
        for lang in languages:
            if not headers.get(lang):
                is_complete = False
                break
        
        if is_complete:
            complete_count += 1
        else:
            incomplete_fields.append(field.get("name", "unknown"))
    
    score = round((complete_count / len(fields)) * 100, 1)
    
    return {
        "score": score,
        "languages": languages,
        "complete_fields": complete_count,
        "total_fields": len(fields),
        "incomplete_fields": incomplete_fields
    }


def find_risk_zones(fields: List[Dict], language: str = "de") -> List[Dict]:
    """
    ⚠️ RISIKOZONEN FINDEN
    
    Identifiziert problematische Felder.
    """
    risks = []
    
    for field in fields:
        name = field.get("name", "unknown")
        field_risks = []
        
        # Zu kurze Description
        desc = field.get("description", {})
        if isinstance(desc, dict):
            desc_text = desc.get(language, desc.get("de", ""))
        else:
            desc_text = str(desc)
        
        if len(desc_text) < 20:
            field_risks.append("description_too_short")
        
        # Vage Begriffe in Description
        vague_terms = ["etc", "usw", "sonstiges", "diverses", "allgemein", "general"]
        if any(term in desc_text.lower() for term in vague_terms):
            field_risks.append("vague_description")
        
        # Keine Keywords
        keywords = field.get("keywords", {})
        if isinstance(keywords, dict):
            keywords = keywords.get(language, keywords.get("de", []))
        if len(keywords) < 3:
            field_risks.append("insufficient_keywords")
        
        # Keine Validation
        if not field.get("validation"):
            field_risks.append("no_validation_rules")
        
        if field_risks:
            risks.append({
                "field": name,
                "risks": field_risks
            })
    
    return risks


def score_format(format_name: str, language: str = "de") -> Dict:
    """
    📊 FORMAT BEWERTEN - HAUPTFUNKTION
    
    Berechnet Gesamtscore für ein Format.
    """
    format_data = load_format(format_name)
    if not format_data:
        return {"error": f"Format '{format_name}' nicht gefunden"}
    
    fields = format_data.get("fields", [])
    
    # Einzelne Scores
    semantic_clarity = calculate_semantic_clarity(fields)
    redundancy = calculate_redundancy(fields, language)
    field_balance = calculate_field_balance(fields)
    i18n = calculate_i18n_score(format_data)
    risk_zones = find_risk_zones(fields, language)
    
    # Overall Score berechnen
    overall = 0.0
    overall += semantic_clarity * 0.30  # 30%
    overall += (100 - redundancy["overlap_count"] * 15) * 0.15  # 15%
    overall += (100 if field_balance["status"] in ["OK", "EXCELLENT"] else 50) * 0.20  # 20%
    overall += i18n["score"] * 0.25  # 25%
    overall += (100 - len(risk_zones) * 10) * 0.10  # 10%
    
    overall = max(0, min(100, round(overall, 1)))
    
    return {
        "format": format_name,
        "semantic_clarity": semantic_clarity,
        "redundancy": redundancy["overlap_count"],
        "redundancy_details": redundancy["overlapping_pairs"],
        "field_balance": field_balance["status"],
        "field_balance_details": field_balance,
        "i18n_score": i18n["score"],
        "i18n_details": i18n,
        "risk_zones": [r["field"] + "_" + "_".join(r["risks"]) for r in risk_zones],
        "risk_details": risk_zones,
        "overall": overall,
        "meta": {
            "fields_analyzed": len(fields),
            "languages": format_data.get("languages", []),
            "version": format_data.get("version", "unknown")
        }
    }
