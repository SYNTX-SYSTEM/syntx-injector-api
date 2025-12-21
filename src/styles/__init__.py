"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🎨 SYNTX STYLE ALCHEMIST - Post-Processing Magic                         ║
║                                                                              ║
║    Der letzte Schliff. Die Politur. Der Duft.                               ║
║    Hier wird aus Output KUNST.                                               ║
║                                                                              ║
║    WRAPPER = WIE denkt es                                                   ║
║    FORMAT  = WAS kommt raus                                                  ║
║    STYLE   = WIE KLINGT es  ← DU BIST HIER                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache

# 🏠 Wo die Style-Rezepte wohnen
STYLE_GRIMOIRE = Path("/opt/syntx-config/styles")


@lru_cache(maxsize=16)
def summon_style(style_name: str) -> Optional[Dict]:
    """
    📜 STYLE BESCHWÖREN
    
    Lädt ein Style-Rezept aus dem Grimoire.
    Cached weil Magie teuer ist.
    """
    spell_path = STYLE_GRIMOIRE / f"{style_name}.json"
    
    if not spell_path.exists():
        print(f"⚠️ Style '{style_name}' nicht im Grimoire gefunden")
        return None
    
    try:
        with open(spell_path, 'r', encoding='utf-8') as tome:
            return json.load(tome)
    except Exception as e:
        print(f"❌ Style Beschwörung fehlgeschlagen: {e}")
        return None


def word_alchemy(text: str, transmutations: Dict[str, str]) -> str:
    """
    ⚗️ WORT-ALCHEMIE
    
    Verwandelt Blei-Worte in Gold-Worte.
    Case-insensitive, whole-word matching.
    """
    if not transmutations:
        return text
    
    result = text
    for lead_word, gold_word in transmutations.items():
        # Whole word replacement, case-insensitive
        pattern = re.compile(r'\b' + re.escape(lead_word) + r'\b', re.IGNORECASE)
        result = pattern.sub(gold_word, result)
    
    return result


def banish_forbidden(text: str, forbidden_scrolls: List[str]) -> str:
    """
    🚫 VERBANNTE WORTE ENTFERNEN
    
    Manche Worte gehören nicht in den Output.
    Sie werden... eliminiert.
    """
    if not forbidden_scrolls:
        return text
    
    result = text
    for cursed_word in forbidden_scrolls:
        pattern = re.compile(r'\b' + re.escape(cursed_word) + r'\b', re.IGNORECASE)
        result = pattern.sub('', result)
    
    # Clean up double spaces
    result = re.sub(r'  +', ' ', result)
    return result


def apply_style_magic(raw_output: str, style_name: str) -> tuple[str, Dict]:
    """
    🔮 STYLE MAGIE ANWENDEN
    
    Der große Zauber. Transformiert rohen Output in gestylten Output.
    
    Returns: (styled_output, style_info)
    """
    if not style_name:
        return raw_output, {"skipped": "Kein Style angegeben"}
    
    style = summon_style(style_name)
    if not style:
        return raw_output, {"error": f"Style '{style_name}' nicht gefunden"}
    
    # 🧪 Phase 1: Wort-Alchemie
    transmuted = word_alchemy(raw_output, style.get("word_alchemy", {}))
    
    # 🚫 Phase 2: Verbannte Worte
    purified = banish_forbidden(transmuted, style.get("forbidden_words", []))
    
    # 📝 Phase 3: Suffix anhängen
    suffix = style.get("suffix", "")
    final = purified + suffix if suffix else purified
    
    style_info = {
        "style_applied": style_name,
        "vibe": style.get("vibe", ""),
        "transmutations_available": len(style.get("word_alchemy", {})),
        "forbidden_count": len(style.get("forbidden_words", []))
    }
    
    return final, style_info


def get_tone_injection(style_name: str) -> str:
    """
    💉 TONE INJECTION HOLEN
    
    Der Tone wird VOR dem LLM injiziert.
    Der Rest passiert NACH dem LLM.
    """
    style = summon_style(style_name)
    if not style:
        return ""
    return style.get("tone_injection", "")


def list_available_styles() -> List[str]:
    """📋 ALLE STYLES IM GRIMOIRE"""
    if not STYLE_GRIMOIRE.exists():
        return []
    return [f.stem for f in STYLE_GRIMOIRE.glob("*.json")]


def get_style_info(style_name: str) -> Optional[Dict]:
    """📊 STYLE INFO"""
    style = summon_style(style_name)
    if not style:
        return None
    return {
        "name": style_name,
        "vibe": style.get("vibe", ""),
        "description": style.get("description", ""),
        "word_alchemy_count": len(style.get("word_alchemy", {})),
        "forbidden_words": style.get("forbidden_words", []),
        "has_suffix": bool(style.get("suffix")),
        "has_tone_injection": bool(style.get("tone_injection"))
    }


def clear_style_cache():
    """🧹 CACHE LEEREN"""
    summon_style.cache_clear()
