"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    📁 FILE ALCHEMIST - Atomare File Operations mit Backup                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

class FileAlchemist:
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
    
    def read_json(self, name: str, ext: str = ".json") -> Optional[Dict]:
        path = self.base_path / f"{name}{ext}"
        if not path.exists(): return None
        try:
            with open(path, 'r', encoding='utf-8') as f: return json.load(f)
        except: return None
    
    def write_json(self, name: str, data: Dict, ext: str = ".json") -> Path:
        self.base_path.mkdir(parents=True, exist_ok=True)
        path = self.base_path / f"{name}{ext}"
        tmp = self.base_path / f".{name}{ext}.tmp"
        with open(tmp, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.rename(path)
        return path
    
    def list_all(self, ext: str = ".json") -> List[str]:
        if not self.base_path.exists(): return []
        return sorted([f.stem for f in self.base_path.glob(f"*{ext}") if not f.stem.startswith('.')])
    
    def exists(self, name: str, ext: str = ".json") -> bool:
        return (self.base_path / f"{name}{ext}").exists()
    
    def create_backup(self, name: str, ext: str = ".json") -> Optional[Path]:
        path = self.base_path / f"{name}{ext}"
        if not path.exists(): return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = self.base_path / f".{name}{ext}.{ts}.backup"
        shutil.copy2(path, backup)
        return backup
    
    def soft_delete(self, name: str, ext: str = ".json") -> Optional[Path]:
        path = self.base_path / f"{name}{ext}"
        if not path.exists(): return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        deleted = self.base_path / f".{name}{ext}.{ts}.deleted"
        path.rename(deleted)
        return deleted
    
    def get_info(self, name: str, ext: str = ".json") -> Optional[Dict]:
        path = self.base_path / f"{name}{ext}"
        if not path.exists(): return None
        stat = path.stat()
        return {"name": name, "path": str(path), "size_bytes": stat.st_size, "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()}
