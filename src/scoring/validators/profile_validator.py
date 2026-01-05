"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🛡️ SYNTX PROFILE VALIDATOR - DER WÄCHTER                                    ║
║                                                                              ║
║  Validiert Profiles vor dem Speichern.                                      ║
║  Structure check. Component check. Safety check.                            ║
║                                                                              ║
║  "Ein System das validiert, schützt sich selbst." 💎                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
#  🛡️ VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_profile(profile_data: Dict) -> tuple[bool, Optional[List[str]]]:
    """
    🛡️ Validate profile structure
    
    Checks:
    - Required fields present
    - Components have weights
    - Weights sum correctly
    - No invalid data types
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # Check required fields
    if "name" not in profile_data:
        errors.append("Missing 'name' field")
    
    if "components" not in profile_data:
        errors.append("Missing 'components' field")
        return False, errors
    
    # Check components
    components = profile_data["components"]
    
    if not isinstance(components, dict):
        errors.append("'components' must be a dictionary")
        return False, errors
    
    if len(components) == 0:
        errors.append("Profile must have at least one component")
    
    total_weight = 0.0
    
    for comp_name, comp_data in components.items():
        if not isinstance(comp_data, dict):
            errors.append(f"Component '{comp_name}' must be a dictionary")
            continue
        
        # Check weight
        if "weight" not in comp_data:
            errors.append(f"Component '{comp_name}' missing 'weight'")
        else:
            weight = comp_data["weight"]
            if not isinstance(weight, (int, float)):
                errors.append(f"Component '{comp_name}' weight must be numeric")
            elif weight <= 0:
                errors.append(f"Component '{comp_name}' weight must be > 0")
            else:
                total_weight += weight
    
    # Weights should sum to something reasonable (0.8 - 1.2 range OK for rounding)
    if total_weight < 0.8 or total_weight > 1.2:
        errors.append(f"Component weights sum to {total_weight:.2f}, expected ~1.0")
    
    return len(errors) == 0, errors if errors else None


def validate_profile_update(updates: Dict) -> tuple[bool, Optional[List[str]]]:
    """
    🛡️ Validate profile update
    
    Lighter validation for updates (only check what's being changed)
    """
    errors = []
    
    if "components" in updates:
        components = updates["components"]
        
        if not isinstance(components, dict):
            errors.append("'components' must be a dictionary")
            return False, errors
        
        for comp_name, comp_data in components.items():
            if not isinstance(comp_data, dict):
                errors.append(f"Component '{comp_name}' must be a dictionary")
                continue
            
            # Check weight if present
            if "weight" in comp_data:
                weight = comp_data["weight"]
                if not isinstance(weight, (int, float)):
                    errors.append(f"Component '{comp_name}' weight must be numeric")
                elif weight <= 0:
                    errors.append(f"Component '{comp_name}' weight must be > 0")
    
    return len(errors) == 0, errors if errors else None


def validate_profile_id(profile_id: str) -> tuple[bool, Optional[str]]:
    """
    🛡️ Validate profile ID format
    
    Rules:
    - Only lowercase, numbers, underscore, hyphen
    - Must start with letter
    - Length 3-50
    """
    if not profile_id:
        return False, "Profile ID cannot be empty"
    
    if len(profile_id) < 3 or len(profile_id) > 50:
        return False, "Profile ID must be 3-50 characters"
    
    if not profile_id[0].isalpha():
        return False, "Profile ID must start with a letter"
    
    allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789_-")
    if not all(c in allowed_chars for c in profile_id):
        return False, "Profile ID can only contain: a-z, 0-9, _, -"
    
    return True, None
