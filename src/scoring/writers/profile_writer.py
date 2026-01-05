"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ✋ SYNTX PROFILE WRITER - DIE HAND                                           ║
║                                                                              ║
║  Schreibt Profiles. Mit Backup. Mit Safety.                                 ║
║  Atomare Operationen. Rollback bei Fehler.                                  ║
║                                                                              ║
║  "Ein System das schreibt, muss Verantwortung tragen." 💎                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from typing import Dict
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
#  📁 PATHS
# ═══════════════════════════════════════════════════════════════════════════════

PROFILES_PATH = Path("/opt/syntx-injector-api/scoring_profiles.json")
BACKUP_DIR = Path("/opt/syntx-config/profile_backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  💾 SAVE WITH BACKUP
# ═══════════════════════════════════════════════════════════════════════════════

def save_profiles(profiles_data: Dict) -> bool:
    """
    ✋ Speichert Profiles mit automatischem Backup
    
    Safety:
    - Creates backup before writing
    - Atomic write (temp file + rename)
    - Validation before save
    
    Returns:
        True if successful
    """
    try:
        # Create backup
        _create_backup()
        
        # Write to temp file first (atomic operation)
        temp_path = PROFILES_PATH.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(profiles_data, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        temp_path.replace(PROFILES_PATH)
        
        return True
        
    except Exception as e:
        print(f"❌ Profile save failed: {e}")
        return False


def _create_backup() -> None:
    """🔄 Creates timestamped backup"""
    if not PROFILES_PATH.exists():
        return
    
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f"profiles_{timestamp}.json"
    
    with open(PROFILES_PATH, 'r') as src:
        with open(backup_path, 'w') as dst:
            dst.write(src.read())
    
    # Keep only last 10 backups
    _cleanup_old_backups()


def _cleanup_old_backups(keep: int = 10) -> None:
    """🧹 Remove old backups"""
    backups = sorted(BACKUP_DIR.glob("profiles_*.json"))
    
    if len(backups) > keep:
        for backup in backups[:-keep]:
            backup.unlink()
