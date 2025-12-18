"""
🌊 SYNTX FORMAT LOADER v2.0 - Rapper Edition
Nicht "File Loading" - FELD-DEFINITION AKTIVIERUNG.
Lädt Format-JSONs und baut daraus die Prompt-Struktur,
die das Modell ausfüllen MUSS.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

# Format Config Directory
FORMATS_DIR = Path("/opt/syntx-config/formats")


@lru_cache(maxsize=16)
def load_format(format_name: str) -> Optional[Dict]:
    """
    🌊 FORMAT LADEN
    
    Lädt komplettes Format-JSON.
    Cached für Performance.
    """
    format_path = FORMATS_DIR / f"{format_name}.json"
    
    if not format_path.exists():
        print(f"⚠️ Format nicht gefunden: {format_name}")
        return None
    
    try:
        with open(format_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Format Load Error: {e}")
        return None


def get_format_fields(format_name: str, language: str = "de") -> List[Dict]:
    """
    🔧 FELD-DEFINITIONEN HOLEN
    
    Gibt Liste von Feld-Dicts zurück mit:
    - name
    - header
    - description
    - keywords
    """
    format_data = load_format(format_name)
    if not format_data:
        return []
    
    fields = []
    for field in format_data.get("fields", []):
        # Header extrahieren (erster aus der Liste)
        headers = field.get("headers", {})
        header_list = headers.get(language, headers.get("de", []))
        header = header_list[0] if header_list else field.get("name", "Unknown")
        
        # Description extrahieren
        descriptions = field.get("description", {})
        description = descriptions.get(language, descriptions.get("de", ""))
        
        # Keywords extrahieren
        keywords = field.get("keywords", {})
        keyword_list = keywords.get(language, keywords.get("de", []))
        
        fields.append({
            "name": field.get("name"),
            "header": header,
            "description": description,
            "keywords": keyword_list,
            "weight": field.get("weight", 0)
        })
    
    return fields


def get_recommended_wrapper(format_name: str) -> Optional[str]:
    """
    🎯 EMPFOHLENEN WRAPPER HOLEN
    
    Liest "wrapper" Feld aus Format-JSON.
    """
    format_data = load_format(format_name)
    if not format_data:
        return None
    return format_data.get("wrapper")


def build_format_prompt(format_name: str, language: str = "de") -> str:
    """
    🔥 FORMAT-PROMPT BAUEN - v2.0 MIT ANWEISUNG!
    
    DAS IST DIE MAGIE!
    
    Baut aus dem JSON die Prompt-Struktur MIT Anweisung:
    
    ════════════════════════════════════════
    📋 ANALYSE-FORMAT - Bitte fülle folgende Felder aus:
    
    ### SIGMA_DRIFT:
    Signal-Verschiebung im System...
    
    ### SIGMA_MECHANISMUS:
    Wie funktioniert der Mechanismus?...
    ════════════════════════════════════════
    """
    fields = get_format_fields(format_name, language)
    
    if not fields:
        return ""
    
    # 🔥 ANWEISUNG bauen
    field_names = [f["header"] for f in fields]
    field_list = "\n".join([f"  – {name}" for name in field_names])
    
    if language == "de":
        instruction = f"""
📋 ANALYSE-FORMAT - Bitte fülle folgende Felder aus:

════════════════════════════════════════════════════════════

{field_list}

Strukturiere deine Antwort mit ### FELDNAME: als Header.
════════════════════════════════════════════════════════════
"""
    else:
        instruction = f"""
📋 ANALYSIS FORMAT - Please fill in the following fields:

════════════════════════════════════════════════════════════

{field_list}

Structure your response with ### FIELDNAME: as headers.
════════════════════════════════════════════════════════════
"""
    
    # Feld-Definitionen bauen
    sections = []
    for field in fields:
        header = field["header"]
        description = field["description"]
        section = f"### {header}:\n{description}"
        sections.append(section)
    
    # Format-Intro
    format_data = load_format(format_name)
    format_intro = ""
    if format_data:
        desc = format_data.get("description", {})
        intro = desc.get(language, desc.get("de", ""))
        if intro:
            format_intro = f"\n[Format: {format_name}]\n{intro}\n"
    
    # Alles zusammenbauen
    full_prompt = instruction + format_intro + "\n\n".join(sections)
    
    return full_prompt


def build_dynamic_prompt(
    user_prompt: str,
    format_name: str,
    language: str = "de"
) -> Tuple[str, Dict]:
    """
    🚀 DYNAMISCHER PROMPT BUILDER
    
    Kombiniert User-Prompt + Format zu einem kalibrierten Feld.
    
    Returns:
        (combined_prompt, metadata)
    """
    format_section = build_format_prompt(format_name, language)
    fields = get_format_fields(format_name, language)
    recommended_wrapper = get_recommended_wrapper(format_name)
    
    if not format_section:
        return user_prompt, {"error": f"Format '{format_name}' nicht gefunden"}
    
    # User-Prompt + Format kombinieren
    if language == "de":
        combined = f"""AUFGABE: {user_prompt}

{format_section}

💡 INSIGHT: Fasse am Ende die wichtigste Erkenntnis in 1-2 Sätzen zusammen.
"""
    else:
        combined = f"""TASK: {user_prompt}

{format_section}

💡 INSIGHT: Summarize the key insight in 1-2 sentences at the end.
"""
    
    metadata = {
        "format": format_name,
        "language": language,
        "fields_count": len(fields),
        "fields": [f["name"] for f in fields],
        "recommended_wrapper": recommended_wrapper
    }
    
    return combined, metadata


def list_formats() -> List[str]:
    """
    📋 ALLE VERFÜGBAREN FORMATE LISTEN
    """
    if not FORMATS_DIR.exists():
        return []
    
    return [f.stem for f in FORMATS_DIR.glob("*.json")]


def clear_format_cache():
    """
    🧹 CACHE LEEREN
    """
    load_format.cache_clear()
