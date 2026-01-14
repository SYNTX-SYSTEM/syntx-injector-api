"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   🔥💎 SYNTX SCORING API v2.0 - COMPLETE ENDPOINT SUITE 💎🔥             ║
║                                                                           ║
║   Revolutionary scoring architecture with:                               ║
║   - Clean separation: Profiles, Bindings, Entities                       ║
║   - Complete data retrieval endpoints                                    ║
║   - Full CRUD operations                                                 ║
║   - SYNTX volltext naming                                                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException, Body
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

router = APIRouter(prefix="/scoring", tags=["SYNTX Scoring v2.0"])

# ═══════════════════════════════════════════════════════════════════════════
#  📁 PATHS
# ═══════════════════════════════════════════════════════════════════════════

SYNTX_CONFIG = Path("/opt/syntx-config")
PROFILES_DIR = SYNTX_CONFIG / "scoring_profiles"
BINDINGS_DIR = SYNTX_CONFIG / "scoring_bindings"
ENTITIES_DIR = SYNTX_CONFIG / "scoring_entities"
FORMATS_DIR = SYNTX_CONFIG / "formats"
WRAPPERS_DIR = SYNTX_CONFIG / "wrappers"

# ═══════════════════════════════════════════════════════════════════════════
#  🛠️ HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def load_json_file(filepath: Path) -> Dict:
    """Load and parse JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {filepath.name}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {filepath.name}: {str(e)}")

def save_json_file(filepath: Path, data: Dict) -> None:
    """Save data as JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save {filepath.name}: {str(e)}")

def list_json_files(directory: Path) -> List[str]:
    """List all JSON files in directory"""
    if not directory.exists():
        return []
    return [f.stem for f in directory.glob("*.json")]

# ═══════════════════════════════════════════════════════════════════════════
#  📊 SCORING PROFILES ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/profiles/list_all_profiles")
async def list_all_profiles():
    """
    List all available scoring profiles
    
    Returns:
        List of profile IDs and basic info
    """
    profiles = []
    for profile_file in PROFILES_DIR.glob("*.json"):
        try:
            data = load_json_file(profile_file)
            profiles.append({
                "profile_id": data.get("profile_id"),
                "profile_name": data.get("profile_name"),
                "profile_version": data.get("profile_version"),
                "filename": profile_file.name
            })
        except Exception as e:
            continue
    
    return {
        "total_profiles": len(profiles),
        "profiles": profiles
    }

@router.get("/profiles/get_profile_by_id/{profile_id}")
async def get_profile_by_id(profile_id: str):
    """
    Get complete profile by ID
    
    Args:
        profile_id: Profile identifier
    
    Returns:
        Complete profile data
    """
    profile_file = PROFILES_DIR / f"{profile_id}.json"
    if not profile_file.exists():
        raise HTTPException(status_code=404, detail=f"Profile not found: {profile_id}")
    
    data = load_json_file(profile_file)
    data["source_file"] = str(profile_file)
    return data

@router.post("/profiles/create_new_profile")
async def create_new_profile(profile_data: Dict = Body(...)):
    """
    Create new scoring profile
    
    Body:
        profile_data: Complete profile definition
    
    Returns:
        Created profile with metadata
    """
    profile_id = profile_data.get("profile_id")
    if not profile_id:
        raise HTTPException(status_code=400, detail="profile_id is required")
    
    profile_file = PROFILES_DIR / f"{profile_id}.json"
    if profile_file.exists():
        raise HTTPException(status_code=409, detail=f"Profile already exists: {profile_id}")
    
    # Add metadata
    profile_data["profile_metadata"] = profile_data.get("profile_metadata", {})
    profile_data["profile_metadata"]["created_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_json_file(profile_file, profile_data)
    
    return {
        "message": "Profile created successfully",
        "profile_id": profile_id,
        "file_location": str(profile_file)
    }

@router.put("/profiles/update_profile_by_id/{profile_id}")
async def update_profile_by_id(profile_id: str, profile_data: Dict = Body(...)):
    """
    Update existing profile
    
    Args:
        profile_id: Profile to update
        profile_data: New profile data
    
    Returns:
        Updated profile confirmation
    """
    profile_file = PROFILES_DIR / f"{profile_id}.json"
    if not profile_file.exists():
        raise HTTPException(status_code=404, detail=f"Profile not found: {profile_id}")
    
    # Add update metadata
    profile_data["profile_metadata"] = profile_data.get("profile_metadata", {})
    profile_data["profile_metadata"]["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_json_file(profile_file, profile_data)
    
    return {
        "message": "Profile updated successfully",
        "profile_id": profile_id,
        "file_location": str(profile_file)
    }

@router.delete("/profiles/delete_profile_by_id/{profile_id}")
async def delete_profile_by_id(profile_id: str):
    """
    Delete scoring profile
    
    Args:
        profile_id: Profile to delete
    
    Returns:
        Deletion confirmation
    """
    profile_file = PROFILES_DIR / f"{profile_id}.json"
    if not profile_file.exists():
        raise HTTPException(status_code=404, detail=f"Profile not found: {profile_id}")
    
    # Check if profile is in use
    bindings_using = []
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding = load_json_file(binding_file)
            if binding.get("scoring_profile_reference") == profile_id:
                bindings_using.append(binding.get("binding_id"))
        except:
            continue
    
    if bindings_using:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete profile in use by bindings: {', '.join(bindings_using)}"
        )
    
    profile_file.unlink()
    
    return {
        "message": "Profile deleted successfully",
        "profile_id": profile_id
    }

# ═══════════════════════════════════════════════════════════════════════════
#  🔗 SCORING BINDINGS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/bindings/list_all_bindings")
async def list_all_bindings():
    """List all scoring bindings"""
    bindings = []
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            data = load_json_file(binding_file)
            bindings.append({
                "binding_id": data.get("binding_id"),
                "binding_format": data.get("binding_format"),
                "scoring_profile_reference": data.get("scoring_profile_reference"),
                "filename": binding_file.name
            })
        except:
            continue
    
    return {
        "total_bindings": len(bindings),
        "bindings": bindings
    }

@router.get("/bindings/get_binding_by_id/{binding_id}")
async def get_binding_by_id(binding_id: str):
    """Get complete binding by ID"""
    binding_file = BINDINGS_DIR / f"{binding_id}.json"
    if not binding_file.exists():
        raise HTTPException(status_code=404, detail=f"Binding not found: {binding_id}")
    
    data = load_json_file(binding_file)
    data["source_file"] = str(binding_file)
    return data

@router.get("/bindings/get_binding_by_format/{format_name}")
async def get_binding_by_format(format_name: str):
    """Get binding for specific format"""
    # Try direct naming convention first
    binding_file = BINDINGS_DIR / f"{format_name}_binding.json"
    if binding_file.exists():
        data = load_json_file(binding_file)
        data["source_file"] = str(binding_file)
        return data
    
    # Search all bindings
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            data = load_json_file(binding_file)
            if data.get("binding_format") == format_name:
                data["source_file"] = str(binding_file)
                return data
        except:
            continue
    
    raise HTTPException(status_code=404, detail=f"No binding found for format: {format_name}")

@router.post("/bindings/create_new_binding")
async def create_new_binding(binding_data: Dict = Body(...)):
    """Create new scoring binding"""
    binding_id = binding_data.get("binding_id")
    if not binding_id:
        raise HTTPException(status_code=400, detail="binding_id is required")
    
    binding_file = BINDINGS_DIR / f"{binding_id}.json"
    if binding_file.exists():
        raise HTTPException(status_code=409, detail=f"Binding already exists: {binding_id}")
    
    # Add metadata
    binding_data["binding_metadata"] = binding_data.get("binding_metadata", {})
    binding_data["binding_metadata"]["created_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_json_file(binding_file, binding_data)
    
    return {
        "message": "Binding created successfully",
        "binding_id": binding_id,
        "file_location": str(binding_file)
    }

@router.put("/bindings/update_binding_by_id/{binding_id}")
async def update_binding_by_id(binding_id: str, binding_data: Dict = Body(...)):
    """Update existing binding"""
    binding_file = BINDINGS_DIR / f"{binding_id}.json"
    if not binding_file.exists():
        raise HTTPException(status_code=404, detail=f"Binding not found: {binding_id}")
    
    binding_data["binding_metadata"] = binding_data.get("binding_metadata", {})
    binding_data["binding_metadata"]["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_json_file(binding_file, binding_data)
    
    return {
        "message": "Binding updated successfully",
        "binding_id": binding_id
    }

@router.delete("/bindings/delete_binding_by_id/{binding_id}")
async def delete_binding_by_id(binding_id: str):
    """Delete scoring binding"""
    binding_file = BINDINGS_DIR / f"{binding_id}.json"
    if not binding_file.exists():
        raise HTTPException(status_code=404, detail=f"Binding not found: {binding_id}")
    
    binding_file.unlink()
    
    return {
        "message": "Binding deleted successfully",
        "binding_id": binding_id
    }

# ═══════════════════════════════════════════════════════════════════════════
#  🤖 SCORING ENTITIES ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/entities/list_all_entities")
async def list_all_entities():
    """List all scoring entities"""
    entities = []
    for entity_file in ENTITIES_DIR.glob("*.json"):
        try:
            data = load_json_file(entity_file)
            entities.append({
                "entity_id": data.get("entity_id"),
                "entity_name": data.get("entity_name"),
                "entity_type": data.get("entity_type"),
                "filename": entity_file.name
            })
        except:
            continue
    
    return {
        "total_entities": len(entities),
        "entities": entities
    }

@router.get("/entities/get_entity_by_id/{entity_id}")
async def get_entity_by_id(entity_id: str):
    """Get complete entity by ID"""
    entity_file = ENTITIES_DIR / f"{entity_id}.json"
    if not entity_file.exists():
        raise HTTPException(status_code=404, detail=f"Entity not found: {entity_id}")
    
    data = load_json_file(entity_file)
    data["source_file"] = str(entity_file)
    return data

@router.post("/entities/create_new_entity")
async def create_new_entity(entity_data: Dict = Body(...)):
    """Create new scoring entity"""
    entity_id = entity_data.get("entity_id")
    if not entity_id:
        raise HTTPException(status_code=400, detail="entity_id is required")
    
    entity_file = ENTITIES_DIR / f"{entity_id}.json"
    if entity_file.exists():
        raise HTTPException(status_code=409, detail=f"Entity already exists: {entity_id}")
    
    entity_data["entity_metadata"] = entity_data.get("entity_metadata", {})
    entity_data["entity_metadata"]["created_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_json_file(entity_file, entity_data)
    
    return {
        "message": "Entity created successfully",
        "entity_id": entity_id,
        "file_location": str(entity_file)
    }

@router.put("/entities/update_entity_by_id/{entity_id}")
async def update_entity_by_id(entity_id: str, entity_data: Dict = Body(...)):
    """Update existing entity"""
    entity_file = ENTITIES_DIR / f"{entity_id}.json"
    if not entity_file.exists():
        raise HTTPException(status_code=404, detail=f"Entity not found: {entity_id}")
    
    entity_data["entity_metadata"] = entity_data.get("entity_metadata", {})
    entity_data["entity_metadata"]["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    save_json_file(entity_file, entity_data)
    
    return {
        "message": "Entity updated successfully",
        "entity_id": entity_id
    }

@router.delete("/entities/delete_entity_by_id/{entity_id}")
async def delete_entity_by_id(entity_id: str):
    """Delete scoring entity"""
    entity_file = ENTITIES_DIR / f"{entity_id}.json"
    if not entity_file.exists():
        raise HTTPException(status_code=404, detail=f"Entity not found: {entity_id}")
    
    # Check if entity is in use
    bindings_using = []
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding = load_json_file(binding_file)
            entities = binding.get("scoring_entities", {})
            if entity_id in entities or any(
                e.get("entity_config_reference") == entity_id 
                for e in entities.values() if isinstance(e, dict)
            ):
                bindings_using.append(binding.get("binding_id"))
        except:
            continue
    
    if bindings_using:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete entity in use by bindings: {', '.join(bindings_using)}"
        )
    
    entity_file.unlink()
    
    return {
        "message": "Entity deleted successfully",
        "entity_id": entity_id
    }

# ═══════════════════════════════════════════════════════════════════════════
#  💎 COMPLETE DATA RETRIEVAL - THE MAGIC ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/format/get_complete_format_configuration/{format_name}")
async def get_complete_format_configuration(format_name: str):
    """
    🔥💎 THE MAGIC ENDPOINT 💎🔥
    
    Returns EVERYTHING for a format:
    - Format definition
    - Binding
    - Profile
    - All Entities
    - Mistral Wrapper
    
    This is the holy grail - complete traceability in one call!
    """
    result = {
        "format_name": format_name,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # 1. Load Format
    format_file = FORMATS_DIR / f"{format_name}.json"
    if not format_file.exists():
        raise HTTPException(status_code=404, detail=f"Format not found: {format_name}")
    
    result["format"] = load_json_file(format_file)
    result["format"]["source_file"] = str(format_file)
    
    # 2. Load Binding
    try:
        binding_response = await get_binding_by_format(format_name)
        result["binding"] = binding_response
    except HTTPException:
        result["binding"] = None
        result["warning"] = f"No binding found for format: {format_name}"
        return result
    
    # 3. Load Profile
    profile_ref = result["binding"].get("scoring_profile_reference")
    if profile_ref:
        try:
            result["profile"] = await get_profile_by_id(profile_ref)
        except HTTPException:
            result["profile"] = None
            result["warning"] = f"Profile not found: {profile_ref}"
    
    # 4. Load all Entities
    entities_config = result["binding"].get("scoring_entities", {})
    result["entities"] = []
    
    for entity_key, entity_config in entities_config.items():
        if isinstance(entity_config, dict):
            entity_ref = entity_config.get("entity_config_reference")
            if entity_ref:
                try:
                    entity_data = await get_entity_by_id(entity_ref)
                    entity_data["binding_config"] = entity_config
                    result["entities"].append(entity_data)
                except HTTPException:
                    continue
    
    # 5. Load Mistral Wrapper
    wrapper_ref = result["binding"].get("mistral_wrapper_reference")
    if wrapper_ref:
        wrapper_file = WRAPPERS_DIR / f"{wrapper_ref}.txt"
        if wrapper_file.exists():
            with open(wrapper_file, 'r', encoding='utf-8') as f:
                result["mistral_wrapper"] = {
                    "wrapper_name": wrapper_ref,
                    "content": f.read(),
                    "source_file": str(wrapper_file)
                }
    
    return result

@router.get("/profile/get_complete_profile_usage/{profile_id}")
async def get_complete_profile_usage(profile_id: str):
    """
    Returns EVERYTHING for a profile:
    - Profile definition
    - All Bindings using this profile
    - All Formats using this profile (via bindings)
    - Usage statistics
    """
    # Load Profile
    profile = await get_profile_by_id(profile_id)
    
    # Find all bindings using this profile
    bindings_using = []
    formats_using = []
    
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding = load_json_file(binding_file)
            if binding.get("scoring_profile_reference") == profile_id:
                bindings_using.append({
                    "binding_id": binding.get("binding_id"),
                    "binding_format": binding.get("binding_format"),
                    "source_file": str(binding_file)
                })
                formats_using.append(binding.get("binding_format"))
        except:
            continue
    
    return {
        "profile": profile,
        "used_by_bindings": bindings_using,
        "used_by_formats": formats_using,
        "statistics": {
            "total_bindings_using": len(bindings_using),
            "total_formats_using": len(formats_using)
        }
    }

@router.get("/binding/get_complete_binding_details/{binding_id}")
async def get_complete_binding_details(binding_id: str):
    """
    Returns EVERYTHING for a binding:
    - Binding definition
    - Format it's bound to
    - Profile it references
    - All Entities it uses
    - Mistral Wrapper
    """
    # Load Binding
    binding = await get_binding_by_id(binding_id)
    
    result = {
        "binding": binding
    }
    
    # Load Format
    format_name = binding.get("binding_format")
    if format_name:
        format_file = FORMATS_DIR / f"{format_name}.json"
        if format_file.exists():
            result["format"] = load_json_file(format_file)
            result["format"]["source_file"] = str(format_file)
    
    # Load Profile
    profile_ref = binding.get("scoring_profile_reference")
    if profile_ref:
        try:
            result["profile"] = await get_profile_by_id(profile_ref)
        except HTTPException:
            result["profile"] = None
    
    # Load Entities
    entities_config = binding.get("scoring_entities", {})
    result["entities"] = []
    
    for entity_key, entity_config in entities_config.items():
        if isinstance(entity_config, dict):
            entity_ref = entity_config.get("entity_config_reference")
            if entity_ref:
                try:
                    entity_data = await get_entity_by_id(entity_ref)
                    entity_data["binding_config"] = entity_config
                    result["entities"].append(entity_data)
                except HTTPException:
                    continue
    
    # Load Mistral Wrapper
    wrapper_ref = binding.get("mistral_wrapper_reference")
    if wrapper_ref:
        wrapper_file = WRAPPERS_DIR / f"{wrapper_ref}.txt"
        if wrapper_file.exists():
            with open(wrapper_file, 'r', encoding='utf-8') as f:
                result["mistral_wrapper"] = {
                    "wrapper_name": wrapper_ref,
                    "content": f.read(),
                    "source_file": str(wrapper_file)
                }
    
    return result

@router.get("/entity/get_complete_entity_usage/{entity_id}")
async def get_complete_entity_usage(entity_id: str):
    """
    Returns EVERYTHING for an entity:
    - Entity definition
    - All Bindings using this entity
    - All Formats using this entity (via bindings)
    - Usage statistics
    """
    # Load Entity
    entity = await get_entity_by_id(entity_id)
    
    # Find all bindings using this entity
    bindings_using = []
    formats_using = set()
    
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding = load_json_file(binding_file)
            entities = binding.get("scoring_entities", {})
            
            # Check if entity is used
            entity_found = False
            for ent_config in entities.values():
                if isinstance(ent_config, dict):
                    if ent_config.get("entity_config_reference") == entity_id:
                        entity_found = True
                        break
            
            if entity_found:
                bindings_using.append({
                    "binding_id": binding.get("binding_id"),
                    "binding_format": binding.get("binding_format"),
                    "source_file": str(binding_file)
                })
                formats_using.add(binding.get("binding_format"))
        except:
            continue
    
    return {
        "entity": entity,
        "used_by_bindings": bindings_using,
        "used_by_formats": list(formats_using),
        "statistics": {
            "total_bindings_using": len(bindings_using),
            "total_formats_using": len(formats_using)
        }
    }

# ═══════════════════════════════════════════════════════════════════════════
#  🎯 SYSTEM STATUS & HEALTH
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/system/get_complete_architecture_overview")
async def get_complete_architecture_overview():
    """
    Returns complete system overview:
    - All profiles (count + list)
    - All bindings (count + list)
    - All entities (count + list)
    - All formats with bindings
    - System health
    """
    profiles_response = await list_all_profiles()
    bindings_response = await list_all_bindings()
    entities_response = await list_all_entities()
    
    # Find formats with bindings
    formats_with_bindings = {}
    for binding in bindings_response["bindings"]:
        format_name = binding.get("binding_format")
        if format_name:
            formats_with_bindings[format_name] = binding.get("binding_id")
    
    # Count total formats
    total_formats = len(list(FORMATS_DIR.glob("*.json")))
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "system_version": "2.0.0",
        "architecture": {
            "profiles": {
                "total": profiles_response["total_profiles"],
                "list": profiles_response["profiles"]
            },
            "bindings": {
                "total": bindings_response["total_bindings"],
                "list": bindings_response["bindings"]
            },
            "entities": {
                "total": entities_response["total_entities"],
                "list": entities_response["entities"]
            },
            "formats": {
                "total": total_formats,
                "with_bindings": len(formats_with_bindings),
                "without_bindings": total_formats - len(formats_with_bindings),
                "bindings_map": formats_with_bindings
            }
        },
        "health": {
            "all_directories_exist": all([
                PROFILES_DIR.exists(),
                BINDINGS_DIR.exists(),
                ENTITIES_DIR.exists(),
                FORMATS_DIR.exists(),
                WRAPPERS_DIR.exists()
            ]),
            "status": "healthy"
        }
    }

@router.get("/system/validate_complete_configuration")
async def validate_complete_configuration():
    """
    Validates entire scoring system:
    - Check all bindings reference valid profiles
    - Check all bindings reference valid entities
    - Check all bindings reference valid formats
    - Check all files are readable
    - Return validation report
    """
    validation_report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "valid": True,
        "errors": [],
        "warnings": [],
        "checks_performed": 0
    }
    
    # Check all bindings
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding = load_json_file(binding_file)
            binding_id = binding.get("binding_id")
            validation_report["checks_performed"] += 1
            
            # Check profile reference
            profile_ref = binding.get("scoring_profile_reference")
            if profile_ref:
                profile_file = PROFILES_DIR / f"{profile_ref}.json"
                if not profile_file.exists():
                    validation_report["errors"].append(
                        f"Binding '{binding_id}' references non-existent profile: {profile_ref}"
                    )
                    validation_report["valid"] = False
            
            # Check format reference
            format_name = binding.get("binding_format")
            if format_name:
                format_file = FORMATS_DIR / f"{format_name}.json"
                if not format_file.exists():
                    validation_report["warnings"].append(
                        f"Binding '{binding_id}' references format '{format_name}' which doesn't exist in formats/"
                    )
            
            # Check entity references
            entities = binding.get("scoring_entities", {})
            for entity_config in entities.values():
                if isinstance(entity_config, dict):
                    entity_ref = entity_config.get("entity_config_reference")
                    if entity_ref:
                        entity_file = ENTITIES_DIR / f"{entity_ref}.json"
                        if not entity_file.exists():
                            validation_report["errors"].append(
                                f"Binding '{binding_id}' references non-existent entity: {entity_ref}"
                            )
                            validation_report["valid"] = False
        except Exception as e:
            validation_report["errors"].append(
                f"Failed to validate binding {binding_file.name}: {str(e)}"
            )
            validation_report["valid"] = False
    
    validation_report["summary"] = {
        "total_errors": len(validation_report["errors"]),
        "total_warnings": len(validation_report["warnings"]),
        "status": "valid" if validation_report["valid"] else "invalid"
    }
    
    return validation_report

# ═══════════════════════════════════════════════════════════════════════════
#  🌟 MEGA COMPLETE ENDPOINTS - THE ULTIMATE DATA RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════


@router.get("/system/get_all_scoring_entities_complete")
async def get_all_scoring_entities_complete():
    """
    🔥💎 MEGA ENDPOINT: ALL SCORING ENTITIES WITH COMPLETE DETAILS 💎🔥
    
    Returns EVERYTHING about all scoring entities (GPT-4, Claude, Pattern, etc.):
    - All entities with complete configuration
    - All bindings using each entity
    - All formats using each entity
    - Complete usage statistics
    
    This shows the COMPLETE scoring entity landscape!
    """
    all_scoring_entities = []
    
    # Load all entities with complete data
    for entity_file in ENTITIES_DIR.glob("*.json"):
        try:
            entity_data = load_json_file(entity_file)
            entity_id = entity_data.get("entity_id")
            
            # Find all bindings using this entity
            bindings_using = []
            formats_using = []
            
            for binding_file in BINDINGS_DIR.glob("*.json"):
                try:
                    binding = load_json_file(binding_file)
                    entities_in_binding = binding.get("scoring_entities", {})
                    
                    # Check if this entity is used in the binding
                    for entity_key, entity_config in entities_in_binding.items():
                        if isinstance(entity_config, dict):
                            if entity_config.get("entity_config_reference") == entity_id:
                                bindings_using.append({
                                    "binding_id": binding.get("binding_id"),
                                    "binding_format": binding.get("binding_format"),
                                    "entity_weight": entity_config.get("entity_weight"),
                                    "entity_priority": entity_config.get("entity_priority"),
                                    "entity_enabled": entity_config.get("entity_enabled")
                                })
                                formats_using.append(binding.get("binding_format"))
                                break
                except:
                    continue
            
            # Build complete scoring entity entry
            scoring_entity_entry = {
                "entity": entity_data,
                "usage": {
                    "bindings": bindings_using,
                    "formats": list(set(formats_using)),
                    "statistics": {
                        "total_bindings": len(bindings_using),
                        "total_formats": len(set(formats_using))
                    }
                }
            }
            
            all_scoring_entities.append(scoring_entity_entry)
        except:
            continue
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_scoring_entities": len(all_scoring_entities),
        "scoring_entities": all_scoring_entities
    }

@router.get("/system/get_all_bindings_complete")
async def get_all_bindings_complete():
    """
    🔥💎 MEGA ENDPOINT: ALL BINDINGS WITH COMPLETE DETAILS 💎🔥
    
    Returns EVERYTHING about all bindings with full nested data:
    - All bindings with complete configuration
    - Complete profile data for each binding
    - Complete entity data for each binding
    - Format data for each binding
    - Mistral wrapper content
    
    This shows the COMPLETE binding landscape with all relationships!
    """
    all_bindings_complete = []
    
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding_data = load_json_file(binding_file)
            binding_id = binding_data.get("binding_id")
            
            # Load complete profile
            profile_ref = binding_data.get("scoring_profile_reference")
            profile_complete = None
            if profile_ref:
                profile_file = PROFILES_DIR / f"{profile_ref}.json"
                if profile_file.exists():
                    profile_complete = load_json_file(profile_file)
            
            # Load complete entities
            entities_complete = []
            entities_config = binding_data.get("scoring_entities", {})
            for entity_key, entity_config in entities_config.items():
                if isinstance(entity_config, dict):
                    entity_ref = entity_config.get("entity_config_reference")
                    if entity_ref:
                        entity_file = ENTITIES_DIR / f"{entity_ref}.json"
                        if entity_file.exists():
                            entity_data = load_json_file(entity_file)
                            entity_data["binding_configuration"] = entity_config
                            entities_complete.append(entity_data)
            
            # Load format
            format_name = binding_data.get("binding_format")
            format_complete = None
            if format_name:
                format_file = FORMATS_DIR / f"{format_name}.json"
                if format_file.exists():
                    format_complete = load_json_file(format_file)
            
            # Load mistral wrapper
            wrapper_ref = binding_data.get("mistral_wrapper_reference")
            wrapper_content = None
            if wrapper_ref:
                wrapper_file = WRAPPERS_DIR / f"{wrapper_ref}.txt"
                if wrapper_file.exists():
                    with open(wrapper_file, 'r', encoding='utf-8') as f:
                        wrapper_content = f.read()
            
            # Build complete binding entry
            binding_entry = {
                "binding": binding_data,
                "profile_complete": profile_complete,
                "entities_complete": entities_complete,
                "format_complete": format_complete,
                "mistral_wrapper_content": wrapper_content
            }
            
            all_bindings_complete.append(binding_entry)
        except:
            continue
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_bindings": len(all_bindings_complete),
        "bindings_complete": all_bindings_complete
    }

@router.get("/system/get_complete_scoring_universe")
async def get_complete_scoring_universe():
    """
    🔥💎 ULTIMATE MEGA ENDPOINT: THE COMPLETE SCORING UNIVERSE 💎🔥
    
    Returns ABSOLUTELY EVERYTHING in one massive response:
    - All profiles with complete attributes
    - All bindings with complete attributes
    - All entities with complete attributes
    - All formats (with and without bindings)
    - Complete relationship mapping
    - System statistics
    
    This is THE HOLY GRAIL endpoint - everything in one call!
    """
    # Get all profiles complete
    profiles_complete = []
    for profile_file in PROFILES_DIR.glob("*.json"):
        try:
            profile_data = load_json_file(profile_file)
            profile_data["source_file"] = str(profile_file)
            profiles_complete.append(profile_data)
        except:
            continue
    
    # Get all bindings complete
    bindings_complete = []
    for binding_file in BINDINGS_DIR.glob("*.json"):
        try:
            binding_data = load_json_file(binding_file)
            binding_data["source_file"] = str(binding_file)
            bindings_complete.append(binding_data)
        except:
            continue
    
    # Get all entities complete
    entities_complete = []
    for entity_file in ENTITIES_DIR.glob("*.json"):
        try:
            entity_data = load_json_file(entity_file)
            entity_data["source_file"] = str(entity_file)
            entities_complete.append(entity_data)
        except:
            continue
    
    # Get all formats
    formats_all = []
    formats_with_bindings = {}
    formats_without_bindings = []
    
    for format_file in FORMATS_DIR.glob("*.json"):
        try:
            format_data = load_json_file(format_file)
            format_name = format_data.get("name")
            format_data["source_file"] = str(format_file)
            formats_all.append(format_data)
            
            # Check if has binding
            has_binding = False
            for binding in bindings_complete:
                if binding.get("binding_format") == format_name:
                    formats_with_bindings[format_name] = binding.get("binding_id")
                    has_binding = True
                    break
            
            if not has_binding:
                formats_without_bindings.append(format_name)
        except:
            continue
    
    # Build relationship map
    relationship_map = {
        "profile_to_bindings": {},
        "profile_to_formats": {},
        "entity_to_bindings": {},
        "entity_to_formats": {},
        "format_to_binding": formats_with_bindings
    }
    
    # Map profiles to bindings and formats
    for profile in profiles_complete:
        profile_id = profile.get("profile_id")
        relationship_map["profile_to_bindings"][profile_id] = []
        relationship_map["profile_to_formats"][profile_id] = []
        
        for binding in bindings_complete:
            if binding.get("scoring_profile_reference") == profile_id:
                relationship_map["profile_to_bindings"][profile_id].append(binding.get("binding_id"))
                relationship_map["profile_to_formats"][profile_id].append(binding.get("binding_format"))
    
    # Map entities to bindings and formats
    for entity in entities_complete:
        entity_id = entity.get("entity_id")
        relationship_map["entity_to_bindings"][entity_id] = []
        relationship_map["entity_to_formats"][entity_id] = []
        
        for binding in bindings_complete:
            entities_in_binding = binding.get("scoring_entities", {})
            for ent_config in entities_in_binding.values():
                if isinstance(ent_config, dict):
                    if ent_config.get("entity_config_reference") == entity_id:
                        relationship_map["entity_to_bindings"][entity_id].append(binding.get("binding_id"))
                        relationship_map["entity_to_formats"][entity_id].append(binding.get("binding_format"))
                        break
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "system_version": "2.0.0",
        
        "profiles": {
            "total": len(profiles_complete),
            "profiles_complete": profiles_complete
        },
        
        "bindings": {
            "total": len(bindings_complete),
            "bindings_complete": bindings_complete
        },
        
        "entities": {
            "total": len(entities_complete),
            "entities_complete": entities_complete
        },
        
        "formats": {
            "total": len(formats_all),
            "with_bindings": len(formats_with_bindings),
            "without_bindings": len(formats_without_bindings),
            "formats_complete": formats_all,
            "formats_without_bindings_list": formats_without_bindings
        },
        
        "relationships": relationship_map,
        
        "statistics": {
            "total_profiles": len(profiles_complete),
            "total_bindings": len(bindings_complete),
            "total_entities": len(entities_complete),
            "total_formats": len(formats_all),
            "formats_with_bindings": len(formats_with_bindings),
            "formats_without_bindings": len(formats_without_bindings),
            "avg_entities_per_binding": sum(len(b.get("scoring_entities", {})) for b in bindings_complete) / len(bindings_complete) if bindings_complete else 0
        },
        
        "health": {
            "all_directories_exist": all([
                PROFILES_DIR.exists(),
                BINDINGS_DIR.exists(),
                ENTITIES_DIR.exists(),
                FORMATS_DIR.exists(),
                WRAPPERS_DIR.exists()
            ]),
            "status": "healthy"
        }
    }
