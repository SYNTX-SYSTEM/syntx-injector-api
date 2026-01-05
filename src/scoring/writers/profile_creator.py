"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🌱 SYNTX PROFILE CREATOR - DIE GEBURT                                       ║
║                                                                              ║
║  Erschafft neue Profiles.                                                   ║
║  Mit Metadata. Mit Validation. Mit Changelog.                               ║
║                                                                              ║
║  "Ein System das erschafft, gibt Leben." 💎                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, Optional
from datetime import datetime

from ..core.profile_reader import load_profiles
from ..writers.profile_writer import save_profiles


# ═══════════════════════════════════════════════════════════════════════════════
#  🌱 CREATE PROFILE
# ═══════════════════════════════════════════════════════════════════════════════

def create_profile(
    profile_id: str,
    profile_data: Dict,
    changelog: Optional[Dict] = None
) -> bool:
    """
    🌱 Create new profile
    
    Args:
        profile_id: Unique ID for profile
        profile_data: Profile configuration
        changelog: Creation documentation
    
    Returns:
        True if successful, False if exists
    """
    data = load_profiles(force_reload=True)
    
    # Check if exists
    if profile_id in data.get("profiles", {}):
        return False
    
    # Add creation metadata
    profile_data["created_at"] = datetime.utcnow().isoformat() + "Z"
    profile_data["created_by"] = changelog.get("created_by", "unknown") if changelog else "system"
    
    # Add changelog
    if changelog:
        changelog["timestamp"] = datetime.utcnow().isoformat() + "Z"
        changelog["action"] = "created"
        profile_data["changelog"] = [changelog]
    
    # Add to data
    if "profiles" not in data:
        data["profiles"] = {}
    
    data["profiles"][profile_id] = profile_data
    
    # Save
    return save_profiles(data)


def delete_profile(profile_id: str, reason: Optional[str] = None) -> bool:
    """
    🗑️ Delete profile (with safety)
    
    Args:
        profile_id: Profile to delete
        reason: Why it's being deleted
    
    Returns:
        True if successful
    """
    data = load_profiles(force_reload=True)
    
    if profile_id not in data.get("profiles", {}):
        return False
    
    # Don't allow deleting default_fallback
    if profile_id == "default_fallback":
        return False
    
    # Remove from profiles
    del data["profiles"][profile_id]
    
    # Remove from mappings
    if "field_to_profile_mapping" in data:
        fields_to_update = [
            field for field, pid in data["field_to_profile_mapping"].items()
            if pid == profile_id
        ]
        for field in fields_to_update:
            data["field_to_profile_mapping"][field] = "default_fallback"
    
    # Save
    return save_profiles(data)
