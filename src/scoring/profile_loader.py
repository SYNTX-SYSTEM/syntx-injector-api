"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🧠 SYNTX PROFILE LOADER - DAS SCORING-GEHIRN                                ║
║                                                                              ║
║  Lädt Scoring Profiles aus JSON.                                            ║
║  Cache im Memory. Reload on demand.                                         ║
║                                                                              ║
║  "Ein System, das seine Regeln aus Daten liest, nicht aus Code." 💎         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
#  📁 PROFILE LOCATION
# ═══════════════════════════════════════════════════════════════════════════════

PROFILES_PATH = Path("/opt/syntx-injector-api/scoring_profiles.json")

# Memory Cache
_profiles_cache: Optional[Dict] = None
_last_loaded: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 LOAD PROFILES
# ═══════════════════════════════════════════════════════════════════════════════

def load_profiles(force_reload: bool = False) -> Dict:
    """
    🔥 Lädt Scoring Profiles aus JSON
    
    Caching Strategy:
    - Erste Load: Lädt von Disk
    - Weitere Loads: Return aus Cache
    - force_reload=True: Neu laden (für Updates)
    
    Returns:
        {
            "version": "0.1.0",
            "profiles": {...},
            "field_to_profile_mapping": {...}
        }
    """
    global _profiles_cache, _last_loaded
    
    # Cache hit?
    if _profiles_cache is not None and not force_reload:
        return _profiles_cache
    
    # Load from disk
    if not PROFILES_PATH.exists():
        raise FileNotFoundError(
            f"❌ Scoring profiles nicht gefunden: {PROFILES_PATH}"
        )
    
    with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    # Cache
    _profiles_cache = profiles
    _last_loaded = datetime.utcnow()
    
    return profiles


def get_profile(profile_id: str, force_reload: bool = False) -> Optional[Dict]:
    """
    🎯 Get einzelnes Profile
    
    Args:
        profile_id: z.B. "default_fallback", "flow_bidir_v1"
        force_reload: Force reload from disk
    
    Returns:
        Profile Dict oder None wenn nicht gefunden
    """
    profiles = load_profiles(force_reload=force_reload)
    return profiles.get("profiles", {}).get(profile_id)


def get_profile_for_field(field_name: str) -> str:
    """
    🔍 Welches Profile für welches Feld?
    
    Logic:
    1. Check field_to_profile_mapping
    2. Fallback: "default_fallback"
    
    Args:
        field_name: z.B. "driftkorper", "kalibrierung"
    
    Returns:
        profile_id (str)
    """
    profiles = load_profiles()
    mapping = profiles.get("field_to_profile_mapping", {})
    
    return mapping.get(field_name, "default_fallback")


def list_all_profiles() -> Dict:
    """
    📋 Liste aller verfügbaren Profiles
    
    Returns:
        {
            "default_fallback": {"name": "...", "strategy": "..."},
            "flow_bidir_v1": {...},
            ...
        }
    """
    profiles = load_profiles()
    return profiles.get("profiles", {})


# ═══════════════════════════════════════════════════════════════════════════════
#  💾 SAVE PROFILES (für Updates)
# ═══════════════════════════════════════════════════════════════════════════════

def save_profiles(profiles_data: Dict) -> None:
    """
    💾 Speichert Profiles zurück zu Disk
    
    Use Cases:
    - API Update via PUT /resonanz/scoring/profiles/{id}
    - GPT schlägt optimierte Weights vor
    - Admin tweaked Patterns
    
    Args:
        profiles_data: Complete profiles dict
    """
    global _profiles_cache, _last_loaded
    
    # Update timestamp
    profiles_data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    
    # Write to disk
    with open(PROFILES_PATH, 'w', encoding='utf-8') as f:
        json.dump(profiles_data, f, indent=2, ensure_ascii=False)
    
    # Invalidate cache
    _profiles_cache = None
    _last_loaded = None


def update_profile(profile_id: str, updates: Dict) -> Dict:
    """
    🔄 Update einzelnes Profile
    
    Args:
        profile_id: z.B. "flow_bidir_v1"
        updates: Partial updates {"components": {"pattern_match": {"weight": 0.7}}}
    
    Returns:
        Updated profile
    """
    profiles = load_profiles()
    
    if profile_id not in profiles.get("profiles", {}):
        raise ValueError(f"❌ Profile '{profile_id}' nicht gefunden")
    
    # Deep merge
    current = profiles["profiles"][profile_id]
    
    # Merge components if provided
    if "components" in updates:
        for comp_name, comp_data in updates["components"].items():
            if comp_name in current.get("components", {}):
                current["components"][comp_name].update(comp_data)
            else:
                current.setdefault("components", {})[comp_name] = comp_data
    
    # Merge top-level fields
    for key, value in updates.items():
        if key != "components":
            current[key] = value
    
    # Save
    save_profiles(profiles)
    
    return current


def reload_profiles() -> Dict:
    """
    🔄 Force reload profiles from disk
    
    Returns:
        Reloaded profiles
    """
    return load_profiles(force_reload=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 STATS
# ═══════════════════════════════════════════════════════════════════════════════

def get_loader_stats() -> Dict:
    """
    📊 Profile Loader Stats
    
    Returns:
        {
            "cached": true/false,
            "last_loaded": "...",
            "total_profiles": N
        }
    """
    global _profiles_cache, _last_loaded
    
    return {
        "cached": _profiles_cache is not None,
        "last_loaded": _last_loaded.isoformat() + "Z" if _last_loaded else None,
        "total_profiles": len(_profiles_cache.get("profiles", {})) if _profiles_cache else 0
    }
