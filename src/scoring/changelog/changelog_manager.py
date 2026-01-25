"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📝 SYNTX CHANGELOG MANAGER - DAS GEDÄCHTNIS                                 ║
║                                                                              ║
║  Verwaltet Profile Change History.                                          ║
║  Wer? Wann? Warum? Was?                                                     ║
║                                                                              ║
║  "Ein System das sich erinnert, kann reflektieren." 💎                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
#  📁 CHANGELOG LOCATION
# ═══════════════════════════════════════════════════════════════════════════════

CHANGELOG_DIR = Path("/opt/syntx-config/logs/profile_changes")
CHANGELOG_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  📝 LOG CHANGE
# ═══════════════════════════════════════════════════════════════════════════════

def log_profile_change(
    profile_id: str,
    action: str,
    changed_by: str,
    reason: str,
    changes: Dict
) -> None:
    """
    📝 Log a profile change
    
    Creates audit trail for all profile modifications
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "profile_id": profile_id,
        "action": action,  # "created", "updated", "deleted"
        "changed_by": changed_by,
        "reason": reason,
        "changes": changes
    }
    
    # Append to today's log
    log_file = CHANGELOG_DIR / f"changes_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 GET CHANGELOG
# ═══════════════════════════════════════════════════════════════════════════════

def get_profile_changelog(profile_id: str, limit: int = 50) -> List[Dict]:
    """
    📖 Get change history for a profile
    
    Returns recent changes (last 7 days)
    """
    changes = []
    
    for i in range(7):
        from datetime import timedelta
        date = datetime.utcnow().date() - timedelta(days=i)
        log_file = CHANGELOG_DIR / f"changes_{date.strftime('%Y-%m-%d')}.jsonl"
        
        if not log_file.exists():
            continue
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    if entry.get("profile_id") == profile_id:
                        changes.append(entry)
                        
                        if len(changes) >= limit:
                            return changes
                except json.JSONDecodeError:
                    continue
    
    return changes


def get_recent_changes(limit: int = 100) -> List[Dict]:
    """
    📖 Get all recent profile changes
    
    Returns changes across all profiles
    """
    changes = []
    
    for i in range(7):
        from datetime import timedelta
        date = datetime.utcnow().date() - timedelta(days=i)
        log_file = CHANGELOG_DIR / f"changes_{date.strftime('%Y-%m-%d')}.jsonl"
        
        if not log_file.exists():
            continue
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    changes.append(entry)
                    
                    if len(changes) >= limit:
                        return changes
                except json.JSONDecodeError:
                    continue
    
    return changes
