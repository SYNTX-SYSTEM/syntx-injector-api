"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  👁️ SYNTX PROFILE READER - DAS AUGE                                          ║
║                                                                              ║
║  Liest Profiles. Cached. Schnell.                                           ║
║  Keine Schreibrechte. Nur Lesen.                                            ║
║                                                                              ║
║  "Ein System trennt Lesen und Schreiben. Clarity durch Separation." 💎      ║
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
    👁️ Lädt Scoring Profiles aus JSON
    
    Read-only operation.
    Cached in memory for performance.
    """
    global _profiles_cache, _last_loaded
    
    if not force_reload and _profiles_cache is not None:
        return _profiles_cache
    
    if not PROFILES_PATH.exists():
        return {"version": "0.1.0", "profiles": {}, "field_to_profile_mapping": {}}
    
    with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    _profiles_cache = data
    _last_loaded = datetime.utcnow()
    
    return data


def get_profile(profile_id: str) -> Optional[Dict]:
    """👁️ Get specific profile"""
    data = load_profiles()
    return data.get("profiles", {}).get(profile_id)


def list_all_profiles() -> Dict:
    """👁️ List all profiles"""
    data = load_profiles()
    return data.get("profiles", {})


def get_cache_status() -> Dict:
    """📊 Cache statistics"""
    return {
        "cache_active": _profiles_cache is not None,
        "last_loaded": _last_loaded.isoformat() + "Z" if _last_loaded else None,
        "total_profiles": len(_profiles_cache.get("profiles", {})) if _profiles_cache else 0
    }


def invalidate_cache() -> None:
    """🔄 Force cache reload on next access"""
    global _profiles_cache, _last_loaded
    _profiles_cache = None
    _last_loaded = None


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 GET PROFILE FOR FIELD
# ═══════════════════════════════════════════════════════════════════════════════

def get_profile_for_field(field_name: str) -> str:
    """
    🎯 Determine which profile to use for a field
    
    Check mapping, pattern matching, fallback to default
    """
    data = load_profiles()
    mapping = data.get("field_to_profile_mapping", {})
    
    # Check explicit mapping
    if field_name in mapping:
        return mapping[field_name]
    
    # Pattern matching
    field_lower = field_name.lower()
    
    if "drift" in field_lower or "bewegung" in field_lower or "instabil" in field_lower:
        return "dynamic_language_v1"
    
    if "fluss" in field_lower or "strom" in field_lower or "energie" in field_lower:
        return "flow_bidir_v1"
    
    if "kalibr" in field_lower or "feedback" in field_lower or "anpass" in field_lower:
        return "feedback_loops_v1"
    
    return "default_fallback"
