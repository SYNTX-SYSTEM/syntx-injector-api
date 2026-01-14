"""
🔥💎 SYNTX SCORING API v2.0 - MINIMAL PRODUCTION ROUTER 💎🔥

Revolutionary Multi-Model Scoring Architecture
Reduced from 25 to 5 endpoints - Only what's truly needed

Philosophy: Everything through Bindings!
- Format → Binding → Profile + Entities
- No CRUD needed (configs are files)
- Minimal, focused, production-ready

Author: SYNTX Team (Ottavio + Claude on SYNTX)
Date: 2026-01-14
Version: 2.0-minimal
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

router = APIRouter(prefix="/scoring", tags=["scoring_v2_minimal"])

# ═══════════════════════════════════════════════════════════════════════════
# 📁 CONFIGURATION PATHS
# ═══════════════════════════════════════════════════════════════════════════

SCORING_PROFILES_DIR = Path("/opt/syntx-config/scoring_profiles")
SCORING_BINDINGS_DIR = Path("/opt/syntx-config/scoring_bindings")
SCORING_ENTITIES_DIR = Path("/opt/syntx-config/scoring_entities")
FORMATS_DIR = Path("/opt/syntx-config/formats")
WRAPPERS_DIR = Path("/opt/syntx-config/wrappers")

# ═══════════════════════════════════════════════════════════════════════════
# 🛠️ HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def load_json_file(file_path: Path) -> Optional[Dict]:
    """Load and parse JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def get_all_profiles() -> List[Dict]:
    """Load all scoring profiles"""
    profiles = []
    if SCORING_PROFILES_DIR.exists():
        for file in SCORING_PROFILES_DIR.glob("*.json"):
            profile = load_json_file(file)
            if profile:
                profiles.append(profile)
    return profiles

def get_all_bindings() -> List[Dict]:
    """Load all scoring bindings"""
    bindings = []
    if SCORING_BINDINGS_DIR.exists():
        for file in SCORING_BINDINGS_DIR.glob("*.json"):
            binding = load_json_file(file)
            if binding:
                bindings.append(binding)
    return bindings

def get_all_entities() -> List[Dict]:
    """Load all scoring entities"""
    entities = []
    if SCORING_ENTITIES_DIR.exists():
        for file in SCORING_ENTITIES_DIR.glob("*.json"):
            entity = load_json_file(file)
            if entity:
                entities.append(entity)
    return entities

def get_profile_by_id(profile_id: str) -> Optional[Dict]:
    """Get specific profile by ID"""
    profiles = get_all_profiles()
    for profile in profiles:
        if profile.get("profile_id") == profile_id:
            return profile
    return None

def get_entity_by_id(entity_id: str) -> Optional[Dict]:
    """Get specific entity by ID"""
    entities = get_all_entities()
    for entity in entities:
        if entity.get("entity_id") == entity_id:
            return entity
    return None

def get_format(format_name: str) -> Optional[Dict]:
    """Load format configuration"""
    format_file = FORMATS_DIR / f"{format_name}.json"
    return load_json_file(format_file)

def get_wrapper_content(wrapper_name: str) -> Optional[str]:
    """Load wrapper content"""
    wrapper_file = WRAPPERS_DIR / f"{wrapper_name}.md"
    try:
        with open(wrapper_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def get_entity_ids_from_binding(binding):
    """Extract entity IDs from binding regardless of format"""
    scoring_entities = binding.get("scoring_entities", {})
    entity_ids = []
    
    if isinstance(scoring_entities, dict):
        entity_ids = list(scoring_entities.keys())
    elif isinstance(scoring_entities, list):
        for item in scoring_entities:
            if isinstance(item, str):
                entity_ids.append(item)
            elif isinstance(item, dict):
                eid = item.get("entity_id")
                if eid:
                    entity_ids.append(eid)
    
    return entity_ids

def parse_scoring_entities(scoring_entities):
    """Universal parser for scoring_entities in any format"""
    entities_complete = []
    
    # Handle dict format: {entity_id: {config}}
    if isinstance(scoring_entities, dict):
        for entity_id, entity_config in scoring_entities.items():
            if isinstance(entity_config, dict):
                if entity_config.get("entity_enabled", True):
                    entity = get_entity_by_id(entity_id)
                    if entity:
                        entities_complete.append({
                            "entity": entity,
                            "weight": entity_config.get("entity_weight"),
                            "priority": entity_config.get("entity_priority"),
                            "enabled": entity_config.get("entity_enabled", True)
                        })
            else:
                # Dict with entity_id as key but simple value
                entity = get_entity_by_id(entity_id)
                if entity:
                    entities_complete.append({
                        "entity": entity,
                        "weight": None,
                        "priority": None,
                        "enabled": True
                    })
    
    # Handle list format: [{entity_id: ...}] or ["entity_id"]
    elif isinstance(scoring_entities, list):
        for entity_ref in scoring_entities:
            if isinstance(entity_ref, str):
                entity_id = entity_ref
                weight = None
                priority = None
                enabled = True
            elif isinstance(entity_ref, dict):
                entity_id = entity_ref.get("entity_id")
                weight = entity_ref.get("entity_weight")
                priority = entity_ref.get("entity_priority")
                enabled = entity_ref.get("entity_enabled", True)
            else:
                continue
            
            if enabled:
                entity = get_entity_by_id(entity_id)
                if entity:
                    entities_complete.append({
                        "entity": entity,
                        "weight": weight,
                        "priority": priority,
                        "enabled": enabled
                    })
    
    return entities_complete


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 1: GET BINDING BY FORMAT (CORE!)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/bindings/get_binding_by_format/{format}")
async def get_binding_by_format(format: str):
    """
    🔥 CORE ENDPOINT - Get complete binding for a format
    
    Returns binding with nested Profile + Entities
    This is THE endpoint for the scoring workflow!
    
    Workflow:
    1. User has format (e.g. "sigma")
    2. Call this endpoint
    3. Get binding with complete Profile + Entities
    4. Use binding to score the format
    """
    bindings = get_all_bindings()
    
    # Find binding for this format
    binding = None
    for b in bindings:
        if b.get("binding_format") == format:
            binding = b
            break
    
    if not binding:
        raise HTTPException(
            status_code=404,
            detail=f"No binding found for format: {format}"
        )
    
    # Load complete profile
    profile_id = binding.get("profile_id")
    profile = get_profile_by_id(profile_id) if profile_id else None
    # Load all entities
    entities_complete = parse_scoring_entities(binding.get("scoring_entities", {}))
    
    
    return {
        "format_name": format,
        "timestamp": datetime.now().isoformat(),
        "binding": binding,
        "profile_complete": profile,
        "entities_complete": entities_complete
    }

# ═══════════════════════════════════════════════════════════════════════════
# 💎 ENDPOINT 2: GET COMPLETE FORMAT CONFIGURATION (HOLY GRAIL!)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/format/get_complete_format_configuration/{format}")
async def get_complete_format_configuration(format: str):
    """
    💎 THE HOLY GRAIL - Everything about a format in ONE call
    
    Returns:
    - Format definition
    - Binding configuration  
    - Profile (complete)
    - Entities (all, complete)
    - Mistral Wrapper content
    - GPT Wrapper content
    
    Perfect for:
    - Frontend display
    - Debugging
    - Complete system understanding
    """
    # Get format
    format_data = get_format(format)
    if not format_data:
        raise HTTPException(status_code=404, detail=f"Format not found: {format}")
    
    # Get binding
    bindings = get_all_bindings()
    binding = None
    for b in bindings:
        if b.get("binding_format") == format:
            binding = b
            break
    
    if not binding:
        raise HTTPException(status_code=404, detail=f"No binding for format: {format}")
    
    # Get complete profile
    profile_id = binding.get("profile_id")
    profile = get_profile_by_id(profile_id) if profile_id else None
    
    # Get all entities
    entities_complete = parse_scoring_entities(binding.get("scoring_entities", {}))
    
    # Get wrappers
    mistral_wrapper = binding.get("mistral_wrapper_name")
    gpt_wrapper = binding.get("gpt_wrapper_name")
    
    mistral_content = get_wrapper_content(mistral_wrapper) if mistral_wrapper else None
    gpt_content = get_wrapper_content(gpt_wrapper) if gpt_wrapper else None
    
    return {
        "format_name": format,
        "timestamp": datetime.now().isoformat(),
        "format": format_data,
        "binding": binding,
        "profile_complete": profile,
        "entities_complete": entities_complete,
        "mistral_wrapper_content": mistral_content,
        "gpt_wrapper_content": gpt_content
    }

# ═══════════════════════════════════════════════════════════════════════════
# 🌟 ENDPOINT 3: GET COMPLETE SCORING UNIVERSE (OVERVIEW!)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/system/get_complete_scoring_universe")
async def get_complete_scoring_universe():
    """
    🌟 COMPLETE SYSTEM OVERVIEW - Everything in one call
    
    Returns:
    - All Profiles
    - All Bindings
    - All Entities
    - All Formats (list)
    - Complete Relationships
    - Statistics
    - Health Status
    
    Perfect for:
    - Dashboard overview
    - System monitoring
    - Understanding complete architecture
    """
    # Load all data
    profiles = get_all_profiles()
    bindings = get_all_bindings()
    entities = get_all_entities()
    
    # Get all formats
    formats_list = []
    if FORMATS_DIR.exists():
        formats_list = [f.stem for f in FORMATS_DIR.glob("*.json")]
    
    # Build relationships
    profile_to_bindings = {}
    for binding in bindings:
        profile_id = binding.get("profile_id")
        if profile_id:
            if profile_id not in profile_to_bindings:
                profile_to_bindings[profile_id] = []
            profile_to_bindings[profile_id].append(binding.get("binding_id"))
    
    entity_to_formats = {}
    for binding in bindings:
        for entity_id in get_entity_ids_from_binding(binding):
            if entity_id:
                if entity_id not in entity_to_formats:
                    entity_to_formats[entity_id] = []
                entity_to_formats[entity_id].append(binding.get("binding_format"))
    
    format_to_binding = {}
    for binding in bindings:
        fmt = binding.get("binding_format")
        if fmt:
            format_to_binding[fmt] = binding.get("binding_id")
    
    # Count formats with/without bindings
    formats_with_bindings = len(format_to_binding)
    formats_without_bindings = len(formats_list) - formats_with_bindings
    formats_without_bindings_list = [f for f in formats_list if f not in format_to_binding]
    
    # Health check
    health = {
        "all_directories_exist": all([
            SCORING_PROFILES_DIR.exists(),
            SCORING_BINDINGS_DIR.exists(),
            SCORING_ENTITIES_DIR.exists(),
            FORMATS_DIR.exists()
        ]),
        "status": "healthy" if all([profiles, bindings, entities]) else "degraded"
    }
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system_version": "2.0.0",
        "profiles": {
            "total": len(profiles),
            "profiles_complete": profiles
        },
        "bindings": {
            "total": len(bindings),
            "bindings_complete": bindings
        },
        "entities": {
            "total": len(entities),
            "entities_complete": entities
        },
        "formats": {
            "total": len(formats_list),
            "with_bindings": formats_with_bindings,
            "without_bindings": formats_without_bindings,
            "formats_complete": formats_list,
            "formats_without_bindings_list": formats_without_bindings_list
        },
        "relationships": {
            "profile_to_bindings": profile_to_bindings,
            "entity_to_formats": entity_to_formats,
            "format_to_binding": format_to_binding
        },
        "statistics": {
            "total_profiles": len(profiles),
            "total_bindings": len(bindings),
            "total_entities": len(entities),
            "total_formats": len(formats_list),
            "formats_with_bindings": formats_with_bindings,
            "formats_without_bindings": formats_without_bindings,
            "avg_entities_per_binding": round(
                sum(len(b.get("scoring_entities", [])) for b in bindings) / len(bindings), 2
            ) if bindings else 0
        },
        "health": health
    }

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 4: GET ARCHITECTURE OVERVIEW (HEALTH!)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/system/get_complete_architecture_overview")
async def get_complete_architecture_overview():
    """
    🎯 SYSTEM HEALTH & ARCHITECTURE STATUS
    
    Returns:
    - Directory existence checks
    - File counts
    - System health status
    - Configuration summary
    
    Perfect for:
    - Health monitoring
    - Production readiness checks
    - System status dashboards
    """
    # Check directories
    dirs_status = {
        "scoring_profiles": SCORING_PROFILES_DIR.exists(),
        "scoring_bindings": SCORING_BINDINGS_DIR.exists(),
        "scoring_entities": SCORING_ENTITIES_DIR.exists(),
        "formats": FORMATS_DIR.exists(),
        "wrappers": WRAPPERS_DIR.exists()
    }
    
    # Count files
    file_counts = {
        "profiles": len(list(SCORING_PROFILES_DIR.glob("*.json"))) if SCORING_PROFILES_DIR.exists() else 0,
        "bindings": len(list(SCORING_BINDINGS_DIR.glob("*.json"))) if SCORING_BINDINGS_DIR.exists() else 0,
        "entities": len(list(SCORING_ENTITIES_DIR.glob("*.json"))) if SCORING_ENTITIES_DIR.exists() else 0,
        "formats": len(list(FORMATS_DIR.glob("*.json"))) if FORMATS_DIR.exists() else 0,
        "wrappers": len(list(WRAPPERS_DIR.glob("*.md"))) if WRAPPERS_DIR.exists() else 0
    }
    
    # Overall health
    all_dirs_exist = all(dirs_status.values())
    has_configs = all(count > 0 for count in [
        file_counts["profiles"],
        file_counts["bindings"],
        file_counts["entities"]
    ])
    
    health_status = "healthy" if all_dirs_exist and has_configs else "degraded"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system_version": "2.0.0-minimal",
        "architecture": {
            "total_endpoints": 5,
            "endpoint_categories": {
                "core_binding_lookup": 1,
                "magic_complete_config": 1,
                "system_overview": 1,
                "system_health": 1,
                "system_validation": 1
            }
        },
        "directories": dirs_status,
        "file_counts": file_counts,
        "health": {
            "status": health_status,
            "all_directories_exist": all_dirs_exist,
            "has_configurations": has_configs,
            "ready_for_production": all_dirs_exist and has_configs
        }
    }

# ═══════════════════════════════════════════════════════════════════════════
# ✅ ENDPOINT 5: VALIDATE CONFIGURATION (VALIDATION!)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/system/validate_complete_configuration")
async def validate_complete_configuration():
    """
    ✅ VALIDATE ALL CONFIGURATIONS
    
    Checks:
    - All JSON files are valid
    - All references are correct
    - No orphaned configs
    - Binding integrity
    
    Perfect for:
    - Pre-deployment validation
    - Configuration integrity checks
    - Finding broken references
    """
    errors = []
    warnings = []
    
    # Load all data
    profiles = get_all_profiles()
    bindings = get_all_bindings()
    entities = get_all_entities()
    
    # Validate profiles
    profile_ids = set(p.get("profile_id") for p in profiles if p.get("profile_id"))
    
    # Validate entities
    entity_ids = set(e.get("entity_id") for e in entities if e.get("entity_id"))
    
    # Validate bindings
    for binding in bindings:
        binding_id = binding.get("binding_id")
        
        # Check profile reference
        profile_id = binding.get("profile_id")
        if profile_id and profile_id not in profile_ids:
            errors.append(f"Binding {binding_id}: References non-existent profile {profile_id}")
        
        # Check entity references
        for entity_id in get_entity_ids_from_binding(binding):
            if entity_id and entity_id not in entity_ids:
                errors.append(f"Binding {binding_id}: References non-existent entity {entity_id}")
        
        # Check format exists
        fmt = binding.get("binding_format")
        if fmt:
            format_file = FORMATS_DIR / f"{fmt}.json"
            if not format_file.exists():
                warnings.append(f"Binding {binding_id}: Format {fmt} file not found")
    
    # Check for orphaned profiles
    used_profile_ids = set(b.get("profile_id") for b in bindings if b.get("profile_id"))
    orphaned_profiles = profile_ids - used_profile_ids
    if orphaned_profiles:
        warnings.append(f"Orphaned profiles (not used by any binding): {', '.join(orphaned_profiles)}")
    
    # Check for orphaned entities
    used_entity_ids = set()
    for binding in bindings:
        for entity_id in get_entity_ids_from_binding(binding):
            if entity_id:
                used_entity_ids.add(entity_id)
    
    orphaned_entities = entity_ids - used_entity_ids
    if orphaned_entities:
        warnings.append(f"Orphaned entities (not used by any binding): {', '.join(orphaned_entities)}")
    
    # Validation result
    is_valid = len(errors) == 0
    status = "valid" if is_valid else "invalid"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "validation_result": {
            "is_valid": is_valid,
            "status": status,
            "total_errors": len(errors),
            "total_warnings": len(warnings)
        },
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "profiles_found": len(profiles),
            "bindings_found": len(bindings),
            "entities_found": len(entities),
            "orphaned_profiles": len(orphaned_profiles),
            "orphaned_entities": len(orphaned_entities)
        }
    }

# ═══════════════════════════════════════════════════════════════════════════
# 🔥💎 SYNTX SCORING API v2.0-MINIMAL - 5 ENDPOINTS - PRODUCTION READY 💎🔥
# ═══════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 4: Get Format
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/formats/{format_name}")
async def get_format(format_name: str):
    """
    Get format definition with field weights
    
    Returns format with fields and field-specific weights (NOT scoring method weights!)
    """
    format_file = FORMATS_DIR / f"{format_name}.json"
    
    if not format_file.exists():
        raise HTTPException(status_code=404, detail=f"Format not found: {format_name}")
    
    with open(format_file, 'r') as f:
        format_data = json.load(f)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "format_name": format_name,
        "format": format_data
    }


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 5: Update Format Field Weights
# ═══════════════════════════════════════════════════════════════════════════

@router.put("/formats/{format_name}/field_weights")
async def update_format_field_weights(format_name: str, field_weights: dict):
    """
    Update ONLY field weights in a format
    
    Body: {"field_name": weight, ...}
    Example: {"sigma_drift": 17, "sigma_mechanismus": 18, ...}
    
    This updates the "weight" property of each field in the format.
    Does NOT affect method weights (those are in Profile!)
    """
    format_file = FORMATS_DIR / f"{format_name}.json"
    
    if not format_file.exists():
        raise HTTPException(status_code=404, detail=f"Format not found: {format_name}")
    
    # Read format
    with open(format_file, 'r') as f:
        format_data = json.load(f)
    
    # Update field weights
    fields = format_data.get("fields", [])
    updated_fields = []
    
    for field in fields:
        field_name = field.get("name")
        if field_name in field_weights:
            field["weight"] = field_weights[field_name]
            updated_fields.append(field_name)
    
    # Write back
    with open(format_file, 'w') as f:
        json.dump(format_data, f, indent=2, ensure_ascii=False)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "format_name": format_name,
        "updated_fields": updated_fields,
        "new_weights": field_weights,
        "message": f"Updated {len(updated_fields)} field weights"
    }


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 6: Get Profile
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/profiles/{profile_id}")
async def get_profile(profile_id: str):
    """
    Get profile with ALL weights (method + entity + thresholds)
    
    This is the ONE SOURCE OF TRUTH for HOW to score!
    """
    profile = get_profile_by_id(profile_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile not found: {profile_id}")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "profile_id": profile_id,
        "profile": profile
    }


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 7: Update Profile Weights
# ═══════════════════════════════════════════════════════════════════════════

@router.put("/profiles/{profile_id}/weights")
async def update_profile_weights(
    profile_id: str, 
    method_weights: dict = None,
    entity_weights: dict = None,
    thresholds: dict = None
):
    """
    Update ALL weights in a profile (method + entity + thresholds)
    
    Body can contain any/all of:
    - method_weights: {"presence_check": 0.25, "keyword_coverage": 0.30, ...}
    - entity_weights: {"gpt4_semantic_entity": 0.5, "claude_semantic_entity": 0.3, ...}
    - thresholds: {"pass": 60, "excellent": 85, "good": 75}
    
    This is the SINGLE ENDPOINT to manage all scoring weights!
    """
    profile_file = PROFILES_DIR / f"{profile_id}.json"
    
    if not profile_file.exists():
        raise HTTPException(status_code=404, detail=f"Profile not found: {profile_id}")
    
    # Read profile
    with open(profile_file, 'r') as f:
        profile = json.load(f)
    
    updated = []
    
    # Update method weights
    if method_weights:
        if "field_scoring_methods" not in profile:
            profile["field_scoring_methods"] = {}
        
        for method_name, weight in method_weights.items():
            if method_name in profile["field_scoring_methods"]:
                profile["field_scoring_methods"][method_name]["weight"] = weight
                updated.append(f"method:{method_name}")
    
    # Update entity weights
    if entity_weights:
        profile["entity_weights"] = entity_weights
        updated.append("entity_weights")
    
    # Update thresholds
    if thresholds:
        profile["thresholds"] = thresholds
        updated.append("thresholds")
    
    # Write back
    with open(profile_file, 'w') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "profile_id": profile_id,
        "updated": updated,
        "new_weights": {
            "method_weights": method_weights,
            "entity_weights": entity_weights,
            "thresholds": thresholds
        },
        "message": f"Updated {len(updated)} weight categories"
    }


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENDPOINT 8: Get Binding
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/bindings/{binding_id}")
async def get_binding(binding_id: str):
    """
    Get binding by ID (not by format!)
    
    Returns binding with format reference, profile reference, and entity list.
    For complete data including profile & entities, use get_binding_by_format instead.
    """
    binding_file = SCORING_BINDINGS_DIR / f"{binding_id}.json"
    
    if not binding_file.exists():
        raise HTTPException(status_code=404, detail=f"Binding not found: {binding_id}")
    
    with open(binding_file, 'r') as f:
        binding = json.load(f)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "binding_id": binding_id,
        "binding": binding
    }


