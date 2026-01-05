"""
🌊 SYNTX Config Management - FIXED: Default vs Runtime Separation
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Dict
import os

from src.core.config import settings

router = APIRouter()

# ═══════════════════════════════════════════════════════════════
# 📁 FILE PATHS
# ═══════════════════════════════════════════════════════════════

ACTIVE_WRAPPER_FILE = Path("/opt/syntx-config/active_wrapper.txt")      # DEFAULT
RUNTIME_WRAPPER_FILE = Path("/opt/syntx-config/runtime_wrapper.txt")    # ACTIVE (NEW!)


# ═══════════════════════════════════════════════════════════════
# 🔧 HELPER FUNCTIONS - DEFAULT WRAPPER
# ═══════════════════════════════════════════════════════════════

def get_active_wrapper() -> str:
    """Get default wrapper (fallback)."""
    if ACTIVE_WRAPPER_FILE.exists():
        with open(ACTIVE_WRAPPER_FILE, 'r') as f:
            return f.read().strip()
    return os.getenv('DEFAULT_WRAPPER', 'syntex_wrapper_universal')


def set_active_wrapper(wrapper_name: str) -> None:
    """Set default wrapper (fallback)."""
    ACTIVE_WRAPPER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ACTIVE_WRAPPER_FILE, 'w') as f:
        f.write(wrapper_name)


# ═══════════════════════════════════════════════════════════════
# 🔧 HELPER FUNCTIONS - RUNTIME WRAPPER (NEW!)
# ═══════════════════════════════════════════════════════════════

def get_runtime_wrapper() -> str:
    """Get currently running wrapper (runtime, not default)."""
    if RUNTIME_WRAPPER_FILE.exists():
        with open(RUNTIME_WRAPPER_FILE, 'r') as f:
            return f.read().strip()
    # Fallback to default if no runtime set
    return get_active_wrapper()


def set_runtime_wrapper(wrapper_name: str) -> None:
    """Set runtime active wrapper (doesn't change default)."""
    RUNTIME_WRAPPER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RUNTIME_WRAPPER_FILE, 'w') as f:
        f.write(wrapper_name)


# ═══════════════════════════════════════════════════════════════
# 📦 ENDPOINTS - DEFAULT WRAPPER (unchanged)
# ═══════════════════════════════════════════════════════════════

@router.get("/config/default-wrapper")
async def get_default_wrapper() -> Dict:
    """Get current default wrapper configuration."""
    active = get_active_wrapper()
    wrapper_path = settings.wrapper_dir / f"{active}.txt"
    
    return {
        "active_wrapper": active,
        "exists": wrapper_path.exists(),
        "path": str(wrapper_path),
        "source": "runtime" if ACTIVE_WRAPPER_FILE.exists() else "env"
    }


@router.put("/config/default-wrapper")
async def update_default_wrapper(wrapper_name: str) -> Dict:
    """Update default wrapper at runtime (ONLY DEFAULT, not runtime!)."""
    wrapper_path = settings.wrapper_dir / f"{wrapper_name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Wrapper '{wrapper_name}' not found in {settings.wrapper_dir}"
        )
    
    set_active_wrapper(wrapper_name)
    
    return {
        "status": "success",
        "message": f"Default wrapper updated to '{wrapper_name}' (runtime unchanged)",
        "default_wrapper": wrapper_name,
        "runtime_wrapper": get_runtime_wrapper(),
        "path": str(wrapper_path)
    }


# ═══════════════════════════════════════════════════════════════
# ⚡ ENDPOINTS - RUNTIME WRAPPER (NEW!)
# ═══════════════════════════════════════════════════════════════

@router.get("/config/runtime-wrapper")
async def get_runtime_wrapper_endpoint() -> Dict:
    """Get currently running wrapper (runtime, not default)."""
    runtime = get_runtime_wrapper()
    default = get_active_wrapper()
    wrapper_path = settings.wrapper_dir / f"{runtime}.txt"
    
    return {
        "runtime_wrapper": runtime,
        "default_wrapper": default,
        "is_same": (runtime == default),
        "exists": wrapper_path.exists(),
        "path": str(wrapper_path),
        "source": "runtime" if RUNTIME_WRAPPER_FILE.exists() else "default"
    }


@router.put("/config/runtime-wrapper")
async def update_runtime_wrapper(wrapper_name: str) -> Dict:
    """
    🎯 SET RUNTIME WRAPPER - Sofort aktiv!
    
    Setzt den Wrapper der JETZT SOFORT verwendet wird.
    Unterschied zu default-wrapper:
    - default: Wird beim nächsten Start verwendet
    - runtime: Wird SOFORT verwendet (überschreibt default temporär)
    """
    wrapper_path = settings.wrapper_dir / f"{wrapper_name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Wrapper '{wrapper_name}' nicht gefunden"
        )
    
    # SET RUNTIME (not default!)
    set_runtime_wrapper(wrapper_name)
    
    return {
        "status": "success",
        "message": f"Runtime wrapper aktiviert: '{wrapper_name}' 🎯",
        "runtime_wrapper": wrapper_name,
        "default_wrapper": get_active_wrapper(),
        "path": str(wrapper_path),
        "note": "Runtime wrapper ist SOFORT aktiv!"
    }

