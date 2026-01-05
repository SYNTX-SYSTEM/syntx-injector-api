"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧬 SYNTX FIELD REGISTRY - LAZY AUTO-REGISTRATION                            ║
║                                                                              ║
║  Jedes neue Feld wird automatisch geboren.                                  ║
║  Keine manuelle Arbeit. Nur Resonanz.                                       ║
║                                                                              ║
║  "Ein System, das sich selbst erweitert, driftet nicht - es wächst." 💎     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
#  📁 REGISTRY LOCATION
# ═══════════════════════════════════════════════════════════════════════════════

REGISTRY_PATH = Path("/opt/syntx-config/fields_metadata.json")


# ═══════════════════════════════════════════════════════════════════════════════
#  🧠 KEYWORD EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def _extract_keywords_from_name(field_name: str) -> List[str]:
    """Extract keywords from field name"""
    cleaned = re.sub(r'^(sigma|syntx|field)_', '', field_name.lower())
    parts = re.findall(r'[a-z]+', cleaned)
    
    keywords = []
    for part in parts:
        keywords.append(part)
        if part.endswith('ung'):
            keywords.append(part[:-3])
        elif part.endswith('keit'):
            keywords.append(part[:-4])
        elif part.endswith('heit'):
            keywords.append(part[:-4])
        elif part.endswith('er'):
            keywords.append(part[:-2])
    
    return list(set(keywords))


# ═══════════════════════════════════════════════════════════════════════════════
#  💾 METADATA I/O
# ═══════════════════════════════════════════════════════════════════════════════

def load_metadata() -> Dict:
    """Load field metadata registry"""
    if not REGISTRY_PATH.exists():
        return {}
    
    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_metadata(metadata: Dict) -> None:
    """Save field metadata registry"""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
#  🌱 LAZY AUTO-REGISTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def ensure_field_registered(field_name: str) -> Dict:
    """
    ✨ Ensure field exists in system
    
    Lazy Registration:
    1. Check if known
    2. If not: Auto-register
    3. Return metadata
    """
    metadata = load_metadata()
    
    if field_name in metadata:
        return metadata[field_name]
    
    # 🌱 GEBURT EINES NEUEN FELDES
    field_meta = {
        "keywords": _extract_keywords_from_name(field_name),
        "scoring_profile": "default_fallback",
        "registered_at": datetime.utcnow().isoformat() + "Z",
        "auto_registered": True
    }
    
    metadata[field_name] = field_meta
    save_metadata(metadata)
    
    return field_meta


def get_all_fields() -> Dict:
    """Get all registered fields"""
    return load_metadata()
