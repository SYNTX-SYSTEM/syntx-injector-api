# ═══════════════════════════════════════════════════════════════════════════
# 🧠 PROFILE CRUD ENDPOINTS - Extended Format Layer
# ═══════════════════════════════════════════════════════════════════════════

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os
import re

router = APIRouter()

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
    components: Optional[Dict[str, Any]] = None

class ProfileUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=100)
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
    """DELETE - Remove profile from system"""
    
    path = os.path.join(PROFILES_DIR, f"{profile_id}.json")
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' not found")
    
    os.remove(path)
    
    return {
        "status": "✅ PROFILE DELETED",
        "profile_id": profile_id,
        "message": f"Profile removed from /opt/syntx-config/profiles/"
    }

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
