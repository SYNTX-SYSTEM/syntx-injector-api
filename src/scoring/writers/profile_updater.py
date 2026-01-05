"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔄 SYNTX PROFILE UPDATER - DIE MODIFIKATION                                 ║
║                                                                              ║
║  Updated bestehende Profiles.                                               ║
║  Deep merge. Changelog tracking.                                            ║
║                                                                              ║
║  "Ein System das sich ändert, dokumentiert seine Veränderung." 💎           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, Optional
from datetime import datetime

from ..core.profile_reader import load_profiles
from ..writers.profile_writer import save_profiles


# ═══════════════════════════════════════════════════════════════════════════════
#  🔄 UPDATE PROFILE
# ═══════════════════════════════════════════════════════════════════════════════

def update_profile(
    profile_id: str,
    updates: Dict,
    changelog: Optional[Dict] = None
) -> bool:
    """
    🔄 Update existing profile
    
    Args:
        profile_id: Profile to update
        updates: Changes to apply (deep merge)
        changelog: Change documentation
    
    Returns:
        True if successful
    """
    data = load_profiles(force_reload=True)
    
    if profile_id not in data.get("profiles", {}):
        return False
    
    profile = data["profiles"][profile_id]
    
    # Deep merge components
    if "components" in updates:
        if "components" not in profile:
            profile["components"] = {}
        
        for comp_name, comp_data in updates["components"].items():
            if comp_name not in profile["components"]:
                profile["components"][comp_name] = {}
            
            profile["components"][comp_name].update(comp_data)
    
    # Update other fields
    for key, value in updates.items():
        if key not in ["components", "changelog", "created_at"]:
            profile[key] = value
    
    # Add changelog entry
    if changelog:
        _add_changelog_entry(profile, changelog)
    
    # Update metadata
    profile["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save
    return save_profiles(data)


def _add_changelog_entry(profile: Dict, changelog: Dict) -> None:
    """📝 Add changelog entry to profile"""
    if "changelog" not in profile:
        profile["changelog"] = []
    
    changelog["timestamp"] = datetime.utcnow().isoformat() + "Z"
    profile["changelog"].append(changelog)
