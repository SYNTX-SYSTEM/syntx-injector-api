"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    📄 FORMAT CRUD - Formate + Felder verwalten                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .base import SyntxCrudBase
from .validators import FormatValidator, FieldValidator

class FormatCrud(SyntxCrudBase):
    def __init__(self):
        super().__init__(Path("/opt/syntx-config/formats"), ".json")
    
    def validate(self, data: Dict) -> Tuple[bool, Optional[str]]: return FormatValidator.validate(data)
    def normalize(self, data: Dict) -> Dict: return FormatValidator.normalize(data)
    
    # ═══════════════════════════════════════════════════════════════════════
    #  🔧 FELD-OPERATIONEN
    # ═══════════════════════════════════════════════════════════════════════
    
    def add_field(self, format_name: str, field: Dict) -> Tuple[bool, str, Optional[Dict]]:
        fmt = self.get(format_name)
        if not fmt: return False, f"Format '{format_name}' nicht gefunden", None
        ok, err = FieldValidator.validate(field)
        if not ok: return False, err, None
        if field["name"] in [f["name"] for f in fmt.get("fields", [])]:
            return False, f"Feld '{field['name']}' existiert bereits", None
        self.alchemist.create_backup(format_name)
        fmt["fields"].append(FieldValidator.normalize(field))
        self.alchemist.write_json(format_name, fmt)
        return True, f"Feld '{field['name']}' hinzugefügt", fmt
    
    def update_field(self, format_name: str, field_name: str, updates: Dict) -> Tuple[bool, str, Optional[Dict]]:
        fmt = self.get(format_name)
        if not fmt: return False, f"Format '{format_name}' nicht gefunden", None
        idx = next((i for i, f in enumerate(fmt.get("fields", [])) if f["name"] == field_name), None)
        if idx is None: return False, f"Feld '{field_name}' nicht gefunden", None
        self.alchemist.create_backup(format_name)
        updated = {**fmt["fields"][idx], **updates, "name": field_name}
        ok, err = FieldValidator.validate(updated)
        if not ok: return False, err, None
        fmt["fields"][idx] = FieldValidator.normalize(updated)
        self.alchemist.write_json(format_name, fmt)
        return True, f"Feld '{field_name}' aktualisiert", fmt
    
    def remove_field(self, format_name: str, field_name: str) -> Tuple[bool, str, Optional[Dict]]:
        fmt = self.get(format_name)
        if not fmt: return False, f"Format '{format_name}' nicht gefunden", None
        original = len(fmt.get("fields", []))
        fmt["fields"] = [f for f in fmt["fields"] if f["name"] != field_name]
        if len(fmt["fields"]) == original: return False, f"Feld '{field_name}' nicht gefunden", None
        if not fmt["fields"]: return False, "Letztes Feld kann nicht gelöscht werden", None
        self.alchemist.create_backup(format_name)
        self.alchemist.write_json(format_name, fmt)
        return True, f"Feld '{field_name}' entfernt", fmt
    
    def get_with_inheritance(self, name: str) -> Optional[Dict]:
        fmt = self.get(name)
        if not fmt or "extends" not in fmt: return fmt
        parent = self.get(fmt["extends"])
        if not parent: return fmt
        parent_fields = {f["name"]: f for f in parent.get("fields", [])}
        for f in fmt.get("fields", []): parent_fields[f["name"]] = f
        result = {**fmt, "fields": list(parent_fields.values()), "_inherited_from": fmt["extends"]}
        return result
    
    def list_by_domain(self, domain: str) -> List[str]:
        return [n for n in self.list_all() if (self.get(n) or {}).get("domain") == domain]
    
    def get_all_domains(self) -> List[str]:
        return sorted(set(self.get(n).get("domain") for n in self.list_all() if self.get(n) and self.get(n).get("domain")))
