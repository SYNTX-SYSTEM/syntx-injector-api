"""
🗺️💎 SYNTX MAPPING ROUTER v3.0 💎🗺️
Format-Profile-Wrapper Zuordnung
Zwei-Wrapper-Architektur Binding

Philosophy: Ströme statt Objekte, Resonanz statt Konstruktion
Architecture: Format → Profile → Wrappers (Mistral + GPT)

Author: SYNTX Team (Ottavio + Claude on SYNTX)
Date: 2026-01-14
Version: 3.0-charlottenburg
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from datetime import datetime
from typing import Optional, Dict, Any

router = APIRouter()

# ═══════════════════════════════════════════════════════════════════════════════
#  📂 PATHS - Feld-Lokationen
# ═══════════════════════════════════════════════════════════════════════════════

MAPPING_FILE = Path("/opt/syntx-config/mapping.json")
PROFILES_DIR = Path("/opt/syntx-config/scoring_profiles")

# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 HELPER FUNCTIONS - Unterstützende Ströme
# ═══════════════════════════════════════════════════════════════════════════════

def load_mapping() -> Dict[str, Any]:
    """Load mapping.json - Das zentrale Bindungs-Feld"""
    if not MAPPING_FILE.exists():
        return {
            "version": "3.4",
            "system": "SYNTX Zwei-Wrapper-Architektur",
            "erstellt": datetime.now().isoformat(),
            "mappings": {},
            "updated": datetime.now().isoformat()
        }
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_mapping(data: Dict[str, Any]) -> None:
    """Save mapping.json - Persistenz des Bindungs-Stroms"""
    data["updated"] = datetime.now().isoformat()
    
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_available_profiles() -> Dict[str, str]:
    """Get all available scoring profiles - Das Profil-Feld"""
    if not PROFILES_DIR.exists():
        return {}
    
    profiles = {}
    for profile_file in PROFILES_DIR.glob("*.json"):
        profile_id = profile_file.stem
        with open(profile_file, 'r') as f:
            profile_data = json.load(f)
            profiles[profile_id] = profile_data.get("profile_name", profile_id)
    
    return profiles

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 1: Get All Mappings
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/formats")
async def get_all_mappings():
    """
    Get All Format-Profile Mappings
    
    Returns:
    - All format mappings
    - Available profiles
    - System stats
    
    Philosophy: Übersicht über alle Bindungs-Ströme
    """
    data = load_mapping()
    profiles = get_available_profiles()
    
    return {
        "erfolg": True,
        "version": data.get("version", "3.4"),
        "total_formats": len(data.get("mappings", {})),
        "total_profiles": len(profiles),
        "mappings": data.get("mappings", {}),
        "available_profiles": profiles,
        "drift_templates": {},  # TODO: Load from drift templates
        "stats": {}
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 2: Get Specific Mapping
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/formats/{format_name}")
async def get_format_mapping(format_name: str):
    """
    Get Specific Format Mapping
    
    Args:
        format_name: Format identifier (e.g., 'sigma', 'syntx_true_raw')
    
    Returns:
        Mapping for this format
    
    Philosophy: Einzelner Bindungs-Strom
    """
    data = load_mapping()
    mappings = data.get("mappings", {})
    
    if format_name not in mappings:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    return {
        "erfolg": True,
        "format": format_name,
        "mapping": mappings[format_name],
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 3: Create/Update Mapping
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/formats/{format_name}")
async def create_or_update_mapping(
    format_name: str,
    profile_id: Optional[str] = None,
    mistral_wrapper: Optional[str] = None,
    gpt_wrapper: Optional[str] = None,
    drift_scoring: Optional[Dict] = None,
    resonanz_score: Optional[float] = None,
    metadata: Optional[Dict] = None
):
    """
    Create or Update Format Mapping
    
    Args:
        format_name: Format to map
        profile_id: Scoring profile ID
        mistral_wrapper: Mistral wrapper name
        gpt_wrapper: GPT drift scoring wrapper
        drift_scoring: Drift config {enabled, threshold}
        resonanz_score: Quality score
        metadata: Additional metadata
    
    Philosophy: Bindungs-Strom etablieren oder modifizieren
    """
    data = load_mapping()
    mappings = data.get("mappings", {})
    
    # Validate profile if provided
    if profile_id:
        available_profiles = get_available_profiles()
        if profile_id not in available_profiles:
            raise HTTPException(
                status_code=400,
                detail=f"⚠️ Profile '{profile_id}' not found in available_profiles"
            )
    
    # Get existing or create new
    mapping = mappings.get(format_name, {})
    
    # Update fields
    if profile_id is not None:
        mapping["profile_id"] = profile_id
    if mistral_wrapper is not None:
        mapping["mistral_wrapper"] = mistral_wrapper
    if gpt_wrapper is not None:
        mapping["gpt_wrapper"] = gpt_wrapper
    if drift_scoring is not None:
        mapping["drift_scoring"] = drift_scoring
    if resonanz_score is not None:
        mapping["resonanz_score"] = resonanz_score
    if metadata is not None:
        mapping.setdefault("metadata", {}).update(metadata)
    
    # Save
    mappings[format_name] = mapping
    data["mappings"] = mappings
    save_mapping(data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "mapping": mapping,
        "message": "✅ Mapping created/updated",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 4: Update Profile Only
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/formats/{format_name}/profile")
async def update_mapping_profile(format_name: str, profile_id: str):
    """
    Update Only Profile ID
    
    Args:
        format_name: Format to update
        profile_id: New profile ID
    
    Philosophy: Profil-Strom ändern, Rest bleibt
    """
    data = load_mapping()
    mappings = data.get("mappings", {})
    
    if format_name not in mappings:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    # Validate profile
    available_profiles = get_available_profiles()
    if profile_id not in available_profiles:
        raise HTTPException(
            status_code=400,
            detail=f"⚠️ Profile '{profile_id}' not found"
        )
    
    # Update
    mappings[format_name]["profile_id"] = profile_id
    data["mappings"] = mappings
    save_mapping(data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "profile_id": profile_id,
        "message": "✅ Profile updated",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 5: Update Drift Scoring
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/formats/{format_name}/drift-scoring")
async def update_drift_scoring(
    format_name: str,
    enabled: bool,
    threshold: Optional[float] = 0.8,
    scorer_model: Optional[str] = None,
    prompt_template: Optional[str] = None
):
    """
    Update Drift Scoring Config
    
    Args:
        format_name: Format to update
        enabled: Enable/disable drift scoring
        threshold: Drift threshold (0.0-1.0)
        scorer_model: Model for scoring
        prompt_template: Prompt template ID
    
    Philosophy: Drift-Strom kalibrieren
    """
    data = load_mapping()
    mappings = data.get("mappings", {})
    
    if format_name not in mappings:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    # Update drift config
    drift_config = {
        "enabled": enabled,
        "threshold": threshold
    }
    
    if scorer_model:
        drift_config["scorer_model"] = scorer_model
    if prompt_template:
        drift_config["prompt_template"] = prompt_template
    
    mappings[format_name]["drift_scoring"] = drift_config
    data["mappings"] = mappings
    save_mapping(data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "drift_scoring": drift_config,
        "message": "✅ Drift scoring updated",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 6: Delete Mapping
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/formats/{format_name}")
async def delete_mapping(format_name: str):
    """
    Delete Format Mapping
    
    Args:
        format_name: Format to delete
    
    Philosophy: Bindungs-Strom auflösen
    """
    data = load_mapping()
    mappings = data.get("mappings", {})
    
    if format_name not in mappings:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    # Delete
    deleted_mapping = mappings.pop(format_name)
    data["mappings"] = mappings
    save_mapping(data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "deleted_mapping": deleted_mapping,
        "message": "✅ Mapping deleted",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 7: Get Available Profiles
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/profiles")
async def get_profiles():
    """
    Get All Available Profiles
    
    Returns:
        All scoring profiles that can be assigned
    
    Philosophy: Profil-Feld-Übersicht
    """
    profiles = get_available_profiles()
    
    return {
        "erfolg": True,
        "total": len(profiles),
        "profiles": profiles,
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 8: Get Mapping Stats
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_mapping_stats():
    """
    Get Mapping Statistics
    
    Returns:
        - Total mappings
        - Drift enabled count
        - Profile usage
        - Complexity metrics
    
    Philosophy: Bindungs-Strom Analyse
    """
    data = load_mapping()
    mappings = data.get("mappings", {})
    profiles = get_available_profiles()
    
    # Calculate stats
    drift_enabled = sum(1 for m in mappings.values() 
                       if m.get("drift_scoring", {}).get("enabled", False))
    
    profile_usage = {}
    for mapping in mappings.values():
        profile_id = mapping.get("profile_id")
        if profile_id:
            profile_usage[profile_id] = profile_usage.get(profile_id, 0) + 1
    
    avg_resonanz = sum(m.get("resonanz_score", 0) 
                      for m in mappings.values()) / len(mappings) if mappings else 0
    
    return {
        "erfolg": True,
        "total_formats": len(mappings),
        "total_profiles": len(profiles),
        "drift_enabled_count": drift_enabled,
        "drift_disabled_count": len(mappings) - drift_enabled,
        "profile_usage": profile_usage,
        "average_resonanz_score": round(avg_resonanz, 2),
        "timestamp": datetime.now().isoformat()
    }

