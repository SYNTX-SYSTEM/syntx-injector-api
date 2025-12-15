"""
SYNTX Field Resonance - Configuration Management

Dynamic wrapper configuration at runtime.
Not "settings" - FIELD CALIBRATION.
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Dict

from ..config import settings

router = APIRouter(prefix="/resonanz", tags=["resonance-config"])

ACTIVE_WRAPPER_FILE = Path("/opt/syntx-config/active_wrapper.txt")


def get_active_wrapper() -> str:
    """Get currently active default wrapper."""
    if ACTIVE_WRAPPER_FILE.exists():
        with open(ACTIVE_WRAPPER_FILE, 'r') as f:
            return f.read().strip()
    return settings.fallback_mode


def set_active_wrapper(wrapper_name: str) -> None:
    """Set active default wrapper."""
    ACTIVE_WRAPPER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ACTIVE_WRAPPER_FILE, 'w') as f:
        f.write(wrapper_name)


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
    """Update default wrapper at runtime."""
    wrapper_path = settings.wrapper_dir / f"{wrapper_name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Wrapper '{wrapper_name}' not found in {settings.wrapper_dir}"
        )
    
    set_active_wrapper(wrapper_name)
    
    return {
        "status": "success",
        "message": f"Default wrapper updated to '{wrapper_name}'",
        "active_wrapper": wrapper_name,
        "path": str(wrapper_path)
    }
