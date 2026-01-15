"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🌊 SYNTX WRAPPER META HANDLER 🌊                                          ║
║                                                                              ║
║    Nicht "JSON Handler" - FELD-DNA MANAGEMENT                                ║
║                                                                              ║
║    Jeder Wrapper hat:                                                        ║
║      - .txt        → Der Content (WIE denkt das Modell)                     ║
║      - .meta.json  → Die DNA (Format-Binding, Author, Stats, etc.)          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from ..config import settings


# ═══════════════════════════════════════════════════════════════════════════════
#  📂 PATHS
# ═══════════════════════════════════════════════════════════════════════════════

WRAPPER_DIR = Path("/opt/syntx-config/wrappers")
STATS_DIR = Path("/opt/syntx-config/logs/stats")


# ═══════════════════════════════════════════════════════════════════════════════
#  🧬 DEFAULT META TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

def create_default_meta(wrapper_name: str) -> Dict:
    """
    🧬 DEFAULT META ERSTELLEN
    
    Wenn ein Wrapper keine .meta.json hat,
    erstellen wir eine mit Defaults.
    """
    return {
        "name": wrapper_name,
        "format": None,
        "author": "unknown",
        "version": "1.0",
        "created": datetime.now().isoformat() + "Z",
        "description": "",
        "tags": [],
        "language": "de",
        "settings": {
            "max_tokens": 500,
            "temperature": 0.7
        },
        "auto_generated": True,
        "scoring_profile_id": None
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 META LADEN
# ═══════════════════════════════════════════════════════════════════════════════

def load_meta(wrapper_name: str) -> Optional[Dict]:
    """
    📖 META LADEN
    """
    meta_path = WRAPPER_DIR / f"{wrapper_name}.meta.json"
    
    if not meta_path.exists():
        return None
    
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Meta Load Error für {wrapper_name}: {e}")
        return None


def load_meta_or_default(wrapper_name: str) -> Dict:
    """
    📖 META LADEN ODER DEFAULT
    """
    meta = load_meta(wrapper_name)
    if meta is None:
        return create_default_meta(wrapper_name)
    return meta


# ═══════════════════════════════════════════════════════════════════════════════
#  💾 META SPEICHERN
# ═══════════════════════════════════════════════════════════════════════════════

def save_meta(wrapper_name: str, meta: Dict) -> bool:
    """
    💾 META SPEICHERN
    """
    meta_path = WRAPPER_DIR / f"{wrapper_name}.meta.json"
    
    try:
        meta["updated"] = datetime.now().isoformat() + "Z"
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ Meta Save Error für {wrapper_name}: {e}")
        return False


def delete_meta(wrapper_name: str) -> bool:
    """
    🗑️ META LÖSCHEN
    """
    meta_path = WRAPPER_DIR / f"{wrapper_name}.meta.json"
    
    if meta_path.exists():
        try:
            meta_path.unlink()
            return True
        except Exception as e:
            print(f"❌ Meta Delete Error für {wrapper_name}: {e}")
            return False
    return True


# ═══════════════════════════════════════════════════════════════════════════════
#  🔗 FORMAT BINDING
# ═══════════════════════════════════════════════════════════════════════════════

def get_format_binding(wrapper_name: str) -> Optional[str]:
    """
    🔗 FORMAT BINDING HOLEN
    """
    meta = load_meta(wrapper_name)
    if meta:
        return meta.get("format")
    return None


def set_format_binding(wrapper_name: str, format_name: Optional[str]) -> bool:
    """
    🔗 FORMAT BINDING SETZEN
    """
    meta = load_meta_or_default(wrapper_name)
    meta["format"] = format_name
    meta["auto_generated"] = False
    return save_meta(wrapper_name, meta)


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 STATS (in separatem Ordner)
# ═══════════════════════════════════════════════════════════════════════════════

def load_stats(wrapper_name: str) -> Dict:
    """
    📊 STATS LADEN
    """
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    stats_path = STATS_DIR / f"{wrapper_name}.stats.json"
    
    if not stats_path.exists():
        return {
            "wrapper": wrapper_name,
            "usage_count": 0,
            "total_tokens": 0,
            "avg_score": 0.0,
            "avg_latency_ms": 0,
            "last_used": None,
            "score_history": []
        }
    
    try:
        with open(stats_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"wrapper": wrapper_name, "usage_count": 0}


def save_stats(wrapper_name: str, stats: Dict) -> bool:
    """
    📊 STATS SPEICHERN
    """
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    stats_path = STATS_DIR / f"{wrapper_name}.stats.json"
    
    try:
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        return True
    except:
        return False


def increment_usage(wrapper_name: str, latency_ms: int = 0, score: float = 0.0, tokens: int = 0):
    """
    📊 USAGE INCREMENT
    """
    stats = load_stats(wrapper_name)
    
    stats["usage_count"] = stats.get("usage_count", 0) + 1
    stats["total_tokens"] = stats.get("total_tokens", 0) + tokens
    stats["last_used"] = datetime.now().isoformat() + "Z"
    
    old_count = stats["usage_count"] - 1
    old_avg = stats.get("avg_latency_ms", 0)
    if stats["usage_count"] > 0:
        stats["avg_latency_ms"] = int((old_avg * old_count + latency_ms) / stats["usage_count"])
    
    if score > 0:
        history = stats.get("score_history", [])
        history.append(score)
        if len(history) > 100:
            history = history[-100:]
        stats["score_history"] = history
        stats["avg_score"] = round(sum(history) / len(history), 2)
    
    save_stats(wrapper_name, stats)


# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

def check_health() -> Dict:
    """
    🏥 HEALTH CHECK
    """
    try:
        from ..formats import list_formats as get_available_formats
        available_formats = get_available_formats()
    except:
        available_formats = []
    
    txt_files = {f.stem for f in WRAPPER_DIR.glob("*.txt")}
    meta_files = {f.stem.replace(".meta", "") for f in WRAPPER_DIR.glob("*.meta.json")}
    
    orphan_txt = txt_files - meta_files
    orphan_meta = meta_files - txt_files
    healthy = txt_files & meta_files
    
    broken_bindings = []
    valid_bindings = []
    
    for wrapper_name in txt_files:
        meta = load_meta(wrapper_name)
        if meta and meta.get("format"):
            format_name = meta["format"]
            if format_name not in available_formats:
                broken_bindings.append({
                    "wrapper": wrapper_name,
                    "format": format_name,
                    "reason": "Format existiert nicht"
                })
            else:
                valid_bindings.append({
                    "wrapper": wrapper_name,
                    "format": format_name
                })
    
    used_formats = {b["format"] for b in valid_bindings}
    unused_formats = set(available_formats) - used_formats
    
    return {
        "status": "healthy" if not orphan_txt and not orphan_meta and not broken_bindings else "warning",
        "wrappers": {
            "total": len(txt_files),
            "healthy": list(healthy),
            "orphan_txt": list(orphan_txt),
            "orphan_meta": list(orphan_meta)
        },
        "formats": {
            "total": len(available_formats),
            "used": list(used_formats),
            "unused": list(unused_formats)
        },
        "bindings": {
            "valid": valid_bindings,
            "broken": broken_bindings
        },
        "auto_fixable": len(orphan_txt) > 0 or len(orphan_meta) > 0
    }


def auto_fix_orphans() -> Dict:
    """
    🔧 AUTO-FIX ORPHANS
    """
    health = check_health()
    
    fixed = []
    deleted = []
    
    for wrapper_name in health["wrappers"]["orphan_txt"]:
        meta = create_default_meta(wrapper_name)
        if save_meta(wrapper_name, meta):
            fixed.append({
                "wrapper": wrapper_name,
                "action": "created_meta",
                "meta": meta
            })
    
    for wrapper_name in health["wrappers"]["orphan_meta"]:
        if delete_meta(wrapper_name):
            deleted.append({
                "wrapper": wrapper_name,
                "action": "deleted_orphan_meta"
            })
    
    return {
        "status": "success",
        "fixed": fixed,
        "deleted": deleted,
        "message": f"Fixed {len(fixed)} orphan wrappers, deleted {len(deleted)} orphan metas"
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🔍 LIST ALL WITH META
# ═══════════════════════════════════════════════════════════════════════════════

def list_wrappers_with_meta() -> List[Dict]:
    """
    🔍 ALLE WRAPPER MIT META LISTEN
    """
    wrappers = []
    
    for txt_file in WRAPPER_DIR.glob("*.txt"):
        wrapper_name = txt_file.stem
        stat = txt_file.stat()
        
        meta = load_meta_or_default(wrapper_name)
        stats = load_stats(wrapper_name)
        
        wrappers.append({
            "name": wrapper_name,
            "path": str(txt_file),
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z',
            "meta": meta,
            "stats": stats,
            "has_meta": (WRAPPER_DIR / f"{wrapper_name}.meta.json").exists()
        })
    
    return sorted(wrappers, key=lambda x: x["name"])
