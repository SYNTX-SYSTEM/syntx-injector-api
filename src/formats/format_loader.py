"""
🌊 SYNTX FORMAT LOADER - Rapper Edition

Nicht "File Loading" - FELD-DEFINITION AKTIVIERUNG.

Lädt Format-JSONs und baut daraus die Prompt-Struktur,
die das Modell ausfüllen soll.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
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


def build_format_prompt(format_name: str, language: str = "de") -> str:
    """
    🔥 FORMAT-PROMPT BAUEN
    
    DAS IST DIE MAGIE!
    
    Baut aus dem JSON die Prompt-Struktur:
    
    ### Driftkörperanalyse:
    WAS ist das analysierte Objekt?...
    
    ### Kalibrierung:
    WIE verändert sich das System?...
    
    ### Strömung:
    WIE fließt Energie?...
    """
    fields = get_format_fields(format_name, language)
    
    if not fields:
        return ""
    
    sections = []
    
    for field in fields:
        header = field["header"]
        description = field["description"]
        
        # Baue Section
        section = f"### {header}:\n{description}"
        sections.append(section)
    
    # Intro hinzufügen
    format_data = load_format(format_name)
    if format_data:
        desc = format_data.get("description", {})
        intro = desc.get(language, desc.get("de", ""))
        if intro:
            sections.insert(0, f"[Format: {format_name}]\n{intro}\n")
    
    return "\n\n".join(sections)


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
