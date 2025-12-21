"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    🎨 STYLE CRUD - Post-Processing Alchemy verwalten                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from pathlib import Path
from typing import Dict, Optional, Tuple
from .base import SyntxCrudBase
from .validators import StyleValidator

class StyleCrud(SyntxCrudBase):
    def __init__(self):
        super().__init__(Path("/opt/syntx-config/styles"), ".json")
    
    def validate(self, data: Dict) -> Tuple[bool, Optional[str]]: return StyleValidator.validate(data)
    def normalize(self, data: Dict) -> Dict: return StyleValidator.normalize(data)
    
    def add_transmutation(self, style_name: str, original: str, replacement: str) -> Tuple[bool, str]:
        style = self.get(style_name)
        if not style: return False, f"Style '{style_name}' nicht gefunden"
        self.alchemist.create_backup(style_name)
        style.setdefault("word_alchemy", {})[original] = replacement
        self.alchemist.write_json(style_name, style)
        return True, f"'{original}' → '{replacement}'"
    
    def remove_transmutation(self, style_name: str, original: str) -> Tuple[bool, str]:
        style = self.get(style_name)
        if not style: return False, f"Style '{style_name}' nicht gefunden"
        if original not in style.get("word_alchemy", {}): return False, f"'{original}' nicht gefunden"
        self.alchemist.create_backup(style_name)
        del style["word_alchemy"][original]
        self.alchemist.write_json(style_name, style)
        return True, f"'{original}' entfernt"
    
    def add_forbidden(self, style_name: str, word: str) -> Tuple[bool, str]:
        style = self.get(style_name)
        if not style: return False, f"Style '{style_name}' nicht gefunden"
        if word in style.get("forbidden_words", []): return False, f"'{word}' bereits verbannt"
        self.alchemist.create_backup(style_name)
        style.setdefault("forbidden_words", []).append(word)
        self.alchemist.write_json(style_name, style)
        return True, f"'{word}' verbannt"
