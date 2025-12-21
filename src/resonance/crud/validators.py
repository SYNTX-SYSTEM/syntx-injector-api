"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    ✅ SYNTX VALIDATORS - Datenintegrität für Felder, Formate, Styles        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import re
from typing import Dict, List, Optional, Tuple

class FieldValidator:
    VALID_TYPES = ["text", "list", "rating", "keywords"]
    
    @classmethod
    def validate(cls, field: Dict) -> Tuple[bool, Optional[str]]:
        if not field.get("name"): return False, "Feld braucht Namen"
        if not re.match(r'^[a-z][a-z0-9_]*$', field["name"]): return False, f"Name '{field['name']}' ungültig"
        if field.get("type", "text") not in cls.VALID_TYPES: return False, f"Type ungültig"
        return True, None
    
    @classmethod
    def normalize(cls, field: Dict) -> Dict:
        name = field.get("name", "unnamed")
        return {
            "name": name, "type": field.get("type", "text"), "weight": field.get("weight", 10),
            "description": field.get("description", {"de": "", "en": ""}),
            "headers": field.get("headers", {"de": [name.upper()], "en": [name.upper()]}),
            "keywords": field.get("keywords", {"de": [], "en": []}),
            "validation": field.get("validation", {"min_length": 10, "max_length": 2000, "required": True})
        }

class FormatValidator:
    VALID_DOMAINS = ["technical", "psychology", "analysis", "raw", "creative", "business"]
    
    @classmethod
    def validate(cls, data: Dict) -> Tuple[bool, Optional[str]]:
        if not data.get("name"): return False, "Format braucht Namen"
        if not re.match(r'^[a-z][a-z0-9_]*$', data["name"]): return False, f"Name ungültig"
        if not data.get("fields"): return False, "Format braucht Felder"
        for i, f in enumerate(data["fields"]):
            ok, err = FieldValidator.validate(f)
            if not ok: return False, f"Feld {i}: {err}"
        return True, None
    
    @classmethod
    def normalize(cls, data: Dict) -> Dict:
        return {
            "name": data.get("name"), "version": data.get("version", "1.0"),
            "domain": data.get("domain"), "extends": data.get("extends"),
            "description": data.get("description", {"de": "", "en": ""}),
            "languages": data.get("languages", ["de", "en"]),
            "wrapper": data.get("wrapper"),
            "fields": [FieldValidator.normalize(f) for f in data.get("fields", [])]
        }

class StyleValidator:
    @classmethod
    def validate(cls, data: Dict) -> Tuple[bool, Optional[str]]:
        if not data.get("name"): return False, "Style braucht Namen"
        if not re.match(r'^[a-z][a-z0-9_]*$', data["name"]): return False, "Name ungültig"
        return True, None
    
    @classmethod
    def normalize(cls, data: Dict) -> Dict:
        return {
            "name": data.get("name"), "vibe": data.get("vibe", ""),
            "description": data.get("description", ""), "tone_injection": data.get("tone_injection", ""),
            "word_alchemy": data.get("word_alchemy", {}),
            "forbidden_words": data.get("forbidden_words", []), "suffix": data.get("suffix", "")
        }
