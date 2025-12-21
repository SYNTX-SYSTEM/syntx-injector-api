"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    🔮 SYNTX CRUD BASE - Template für alle CRUD Operationen                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from .file_ops import FileAlchemist

class SyntxCrudBase(ABC):
    def __init__(self, base_path: Path, extension: str = ".json"):
        self.alchemist = FileAlchemist(base_path)
        self.extension = extension
        self.base_path = base_path
    
    def get(self, name: str) -> Optional[Dict]: return self.alchemist.read_json(name, self.extension)
    def list_all(self) -> List[str]: return self.alchemist.list_all(self.extension)
    def exists(self, name: str) -> bool: return self.alchemist.exists(name, self.extension)
    def get_info(self, name: str) -> Optional[Dict]: return self.alchemist.get_info(name, self.extension)
    
    def create(self, data: Dict) -> Tuple[bool, str, Optional[Dict]]:
        ok, err = self.validate(data)
        if not ok: return False, err, None
        name = data.get("name")
        if self.exists(name): return False, f"'{name}' existiert bereits", None
        normalized = self.normalize(data)
        self.alchemist.write_json(name, normalized, self.extension)
        return True, f"'{name}' erstellt", normalized
    
    def update(self, name: str, updates: Dict) -> Tuple[bool, str, Optional[Dict]]:
        if not self.exists(name): return False, f"'{name}' nicht gefunden", None
        self.alchemist.create_backup(name, self.extension)
        existing = self.get(name)
        merged = {**existing, **updates, "name": name}
        ok, err = self.validate(merged)
        if not ok: return False, err, None
        normalized = self.normalize(merged)
        self.alchemist.write_json(name, normalized, self.extension)
        return True, f"'{name}' aktualisiert", normalized
    
    def delete(self, name: str) -> Tuple[bool, str]:
        if not self.exists(name): return False, f"'{name}' nicht gefunden"
        backup = self.alchemist.soft_delete(name, self.extension)
        return True, f"'{name}' gelöscht (Backup: {backup.name})"
    
    @abstractmethod
    def validate(self, data: Dict) -> Tuple[bool, Optional[str]]: pass
    @abstractmethod
    def normalize(self, data: Dict) -> Dict: pass
