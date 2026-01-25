# ═══════════════════════════════════════════════════════════════════════════
# 🧠 PROFILE CRUD ENDPOINTS - Extended Format Layer
# ═══════════════════════════════════════════════════════════════════════════

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os
from pathlib import Path
import logging
import re

router = APIRouter()
logger = logging.getLogger(__name__)

PROFILES_DIR = "/opt/syntx-config/profiles"

# ═══════════════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    active: bool = True
    weight: float = Field(..., ge=0, le=100)
    tags: Optional[List[str]] = []
    patterns: Optional[List[str]] = []
    strategy: Optional[str] = None
    entity_weights: Optional[Dict[str, float]] = None
    thresholds: Optional[Dict[str, float]] = None
    drift_thresholds: Optional[Dict[str, float]] = None
    field_scoring_methods: Optional[Dict[str, Any]] = None
    components: Optional[Dict[str, Any]] = None
    entity_weights: Optional[Dict[str, float]] = None
    thresholds: Optional[Dict[str, float]] = None
    drift_thresholds: Optional[Dict[str, float]] = None
    field_scoring_methods: Optional[Dict[str, Any]] = None

class ProfileUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=100)
    entity_weights: Optional[Dict[str, float]] = None
    thresholds: Optional[Dict[str, float]] = None
    drift_thresholds: Optional[Dict[str, float]] = None
    field_scoring_methods: Optional[Dict[str, Any]] = None
    description: str = Field(..., min_length=1)
    active: bool
    weight: float = Field(..., ge=0, le=100)
    tags: Optional[List[str]] = []
    patterns: Optional[List[str]] = []
    strategy: Optional[str] = None
    components: Optional[Dict[str, Any]] = None

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def generate_profile_id(name: str) -> str:
    """Generate unique ID from name"""
    base_id = re.sub(r'[^a-z0-9_]+', '_', name.lower().strip())
    base_id = base_id.strip('_')
    
    if not base_id:
        base_id = "profile"
    
    profile_id = base_id
    counter = 1
    while os.path.exists(os.path.join(PROFILES_DIR, f"{profile_id}.json")):
        profile_id = f"{base_id}_{counter}"
        counter += 1
    
    return profile_id

def load_profile(profile_id: str) -> dict:
    """Load profile from /opt/syntx-config/profiles/"""
    path = os.path.join(PROFILES_DIR, f"{profile_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_profile(profile_id: str, data: dict):
    """Save profile to /opt/syntx-config/profiles/"""
    os.makedirs(PROFILES_DIR, exist_ok=True)
    path = os.path.join(PROFILES_DIR, f"{profile_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/resonanz/profiles/crud")
async def create_profile(data: ProfileCreate):
    """CREATE - New profile with extended SYNTX layer"""
    
    profile_id = generate_profile_id(data.name)
    now = datetime.utcnow().isoformat() + "Z"
    
    profile = {
        "name": data.name,
        "description": data.description,
        "strategy": data.strategy or "custom",
        "components": data.components or {},
        "changelog": [{
            "action": "created",
            "created_by": "syntx_crud",
            "timestamp": now,
            "reason": "Profile created via CRUD system"
        }],
        "created_at": now,
        "updated_at": now,
        "label": data.label,
        "active": data.active,
        "weight": data.weight,
        "tags": data.tags or [],
        "patterns": data.patterns or []
    }
    
    # Oracle Fields
    if data.entity_weights is not None:
        profile["entity_weights"] = data.entity_weights
    if data.thresholds is not None:
        profile["thresholds"] = data.thresholds
    if data.drift_thresholds is not None:
        profile["drift_thresholds"] = data.drift_thresholds
    if data.field_scoring_methods is not None:
        profile["field_scoring_methods"] = data.field_scoring_methods
    
    save_profile(profile_id, profile)
    
    return {
        "status": "✅ PROFILE CREATED",
        "profile_id": profile_id,
        "profile": profile
    }

@router.put("/resonanz/profiles/crud/{profile_id}")
async def update_profile(profile_id: str, data: ProfileUpdate):
    """UPDATE - Merge fields with existing profile"""
    
    existing = load_profile(profile_id)
    now = datetime.utcnow().isoformat() + "Z"
    
    updated = {
        **existing,
        "name": data.name,
        "label": data.label,
        "description": data.description,
        "updated_at": now,
        "active": data.active,
        "weight": data.weight,
        "tags": data.tags or [],
        "patterns": data.patterns or [],
    }
    
    if data.strategy is not None:
        updated["strategy"] = data.strategy
    if data.components is not None:
        updated["components"] = data.components
    
    # Oracle Fields
    if data.entity_weights is not None:
        updated["entity_weights"] = data.entity_weights
    if data.thresholds is not None:
        updated["thresholds"] = data.thresholds
    if data.drift_thresholds is not None:
        updated["drift_thresholds"] = data.drift_thresholds
    if data.field_scoring_methods is not None:
        updated["field_scoring_methods"] = data.field_scoring_methods
    
    if "changelog" not in updated:
        updated["changelog"] = []
    
    updated["changelog"].append({
        "action": "updated",
        "updated_by": "syntx_crud",
        "timestamp": now,
        "reason": "Profile updated via CRUD"
    })
    
    save_profile(profile_id, updated)
    
    return {
        "status": "✅ PROFILE UPDATED",
        "profile_id": profile_id,
        "profile": updated
    }

@router.delete("/resonanz/profiles/crud/{profile_id}")
async def delete_profile(profile_id: str):
    """
    💀 PROFILE LÖSCHEN (Soft Delete + Mapping Cleanup)
    
    Löscht Profile ABER nicht wirklich - wird umbenannt zu .deleted!
    WICHTIG: Updated auch alle Mappings die dieses Profile benutzen!
    
    Das ist wie Mitarbeiter kündigen:
    • Zugangskarte deaktivieren (Profile → .deleted)
    • Aus allen Projekten austragen (Mapping cleanup)
    • Nicht einfach verschwinden lassen!
    
    Args:
        profile_id: Profile zum Löschen
    
    Returns:
        Bestätigung mit Info über betroffene Mappings
    
    Errors:
        404: Profile existiert nicht
        500: Löschen fehlgeschlagen
    """
    try:
        logger.info(f"Lösche Profile '{profile_id}' (soft delete + mapping cleanup)")
        
        # 1. Check ob Profile existiert
        profile_pfad = Path(PROFILES_DIR) / f"{profile_id}.json"
        
        if not profile_pfad.exists():
            logger.warning(f"⚠️ Profile '{profile_id}' nicht gefunden")
            raise HTTPException(
                status_code=404,
                detail=f"Profile '{profile_id}' existiert nicht Bruder!"
            )
        
        # 2. SOFT DELETE - Umbenennen statt Löschen!
        deleted_pfad = Path(PROFILES_DIR) / f"{profile_id}.json.deleted"
        
        try:
            profile_pfad.rename(deleted_pfad)
            logger.info(f"💀 Profile '{profile_id}' → .deleted umbenannt")
        except Exception as e:
            logger.error(f"🔴 Soft-Delete failed: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Konnte Profile nicht umbenennen: {str(e)}"
            )
        
        # 3. MAPPING CLEANUP - Warne über Mappings die dieses Profile nutzen!
        mapping_file = Path("/opt/syntx-config/mapping.json")
        betroffene_mappings = []
        
        try:
            if mapping_file.exists():
                logger.debug(f"Checke mapping.json für Profile '{profile_id}'")
                
                # Lade mapping.json
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    mapping_daten = json.load(f)
                
                # Suche Mappings die dieses Profile nutzen
                alle_mappings = mapping_daten.get("mappings", {})
                
                for format_name, mapping_config in alle_mappings.items():
                    if mapping_config.get("profile_id") == profile_id:
                        betroffene_mappings.append(format_name)
                        # WICHTIG: Wir löschen die Mappings NICHT!
                        # User muss sie manuell updaten auf neues Profile.
                        # Sonst hätten Formate plötzlich kein Profile mehr!
                        logger.warning(f"⚠️  Format '{format_name}' nutzt gelöschtes Profile '{profile_id}'!")
                
                if betroffene_mappings:
                    logger.warning(
                        f"⚠️  {len(betroffene_mappings)} Mappings nutzen gelöschtes Profile! "
                        f"User muss diese manuell updaten!"
                    )
                    
            else:
                logger.debug("mapping.json existiert nicht - kein Check nötig")
                
        except Exception as mapping_error:
            # Mapping-Check failed? Loggen aber nicht crashen!
            logger.warning(f"⚠️ Mapping-Check failed: {mapping_error}")
        
        return {
            "status": "💀 PROFILE FREIGEGEBEN",
            "profile_id": profile_id,
            "message": f"Profile → {profile_id}.json.deleted (kann wiederhergestellt werden)",
            "warning": {
                "affected_mappings": betroffene_mappings,
                "count": len(betroffene_mappings),
                "action_required": "Update diese Mappings auf ein neues Profile!" if betroffene_mappings else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Profile-Löschen '{profile_id}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Profile nicht löschen: {str(e)}"
        )



@router.get("/resonanz/profiles/crud")
async def list_profiles_crud():
    """
    LIST - Get all profiles from /opt/syntx-config/profiles/
    """
    
    if not os.path.exists(PROFILES_DIR):
        return {
            "status": "✅ OK",
            "count": 0,
            "profiles": {}
        }
    
    profiles = {}
    
    for filename in os.listdir(PROFILES_DIR):
        if filename.endswith('.json'):
            profile_id = filename[:-5]  # Remove .json
            try:
                profile_data = load_profile(profile_id)
                profiles[profile_id] = profile_data
            except Exception as e:
                print(f"Error loading profile {profile_id}: {e}")
                continue
    
    return {
        "status": "✅ OK", 
        "count": len(profiles),
        "profiles": profiles
    }

@router.get("/resonanz/profiles/crud/{profile_id}")
async def get_single_profile(profile_id: str):
    """
    GET SINGLE PROFILE
    
    Returns profile data from /opt/syntx-config/profiles/{profile_id}.json
    Same format as PUT/POST responses
    """
    try:
        profile_data = load_profile(profile_id)
        
        return {
            "status": "✅ PROFILE LOADED",
            "profile_id": profile_id,
            "profile": profile_data
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

