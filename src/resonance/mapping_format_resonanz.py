from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()
MAPPING_FILE = Path("/opt/syntx-config/mapping.json")

# 🔥 DIRECT BINDING ENDPOINT - NO VALIDATION
@router.put("/formats/{format_name}/kalibriere-format-profil")
async def kalibriere_format_profil(format_name: str, profile_id: str):
    """
    💎 KALIBRIERE FORMAT → PROFIL
    Bindet Profile direkt an Format - OHNE available_profiles Validation
    
    Args:
        format_name: Format name (z.B. 'sigma', 'human')
        profile_id: Profile ID (z.B. 'claude_test_v1')
    
    Returns:
        Success message mit binding details
    """
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="❌ Mapping file not found")
    
    # LOAD MAPPING
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mappings = data.get("mappings", {})
    
    # CHECK FORMAT EXISTS
    if format_name not in mappings:
        raise HTTPException(status_code=404, detail=f"❌ Format '{format_name}' not in mappings")
    
    # UPDATE PROFILE_ID
    mappings[format_name]["profile_id"] = profile_id
    
    # SAVE
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return {
        "erfolg": True,
        "format": format_name,
        "profile_id": profile_id,
        "message": f"✅ Profile '{profile_id}' bound to '{format_name}'",
        "binding": mappings[format_name]
    }

# 🌊 GET PROFIL-STROM FÜR FORMAT
@router.get("/formats/{format_name}/stroeme-profil-fuer-format")
async def get_profil_strom_fuer_format(format_name: str):
    """
    🌊 PROFIL-STRÖME FÜR FORMAT
    Gibt alle Binding-Details für ein spezifisches Format zurück
    
    Args:
        format_name: Format name (z.B. 'sigma', 'human')
    
    Returns:
        Format mit allen Binding-Details inkl. Profile info
    """
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="❌ Mapping file not found")
    
    # LOAD MAPPING
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mappings = data.get("mappings", {})
    
    # CHECK FORMAT EXISTS
    if format_name not in mappings:
        raise HTTPException(status_code=404, detail=f"❌ Format '{format_name}' not in mappings")
    
    mapping = mappings[format_name]
    profile_id = mapping.get("profile_id")
    
    # LOAD PROFILE DETAILS IF EXISTS
    profile_details = None
    if profile_id:
        profile_path = Path(f"/opt/syntx-config/profiles/{profile_id}.json")
        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_details = json.load(f)
    
    return {
        "erfolg": True,
        "format_name": format_name,
        "binding": {
            "profile_id": profile_id,
            "profile_exists": profile_details is not None,
            "profile_details": profile_details,
            "mistral_wrapper": mapping.get("mistral_wrapper"),
            "gpt_wrapper": mapping.get("gpt_wrapper"),
            "drift_scoring": mapping.get("drift_scoring", {}),
            "resonanz_score": mapping.get("resonanz_score", 0.0)
        },
        "message": f"🌊 Profil-Strom für Format '{format_name}'"
    }
