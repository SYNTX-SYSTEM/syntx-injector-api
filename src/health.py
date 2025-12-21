"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    🏥 SYNTX HEALTH - SYSTEM VITALZEICHEN                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter
from pathlib import Path
import json

from .config import settings
from .streams import FORMAT_LOADER_AVAILABLE

router = APIRouter(tags=["health"])


@router.get("/health")
async def root_health():
    """🏥 Root Health Check"""
    return {
        "status": "SYSTEM_GESUND",
        "api_version": "3.3.0",
        "modules": ["wrappers", "formats", "styles", "diff", "sessions", "alchemy"]
    }


@router.get("/resonanz/health")
async def resonance_health():
    """🏥 Resonanz Health - Mit letztem Response"""
    log_file = settings.log_dir / "field_flow.jsonl"
    last_response = None
    
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in reversed(lines[-10:]):
                    entry = json.loads(line)
                    if entry.get("stage") == "5_RESPONSE":
                        last_response = {
                            "response": entry.get("response", "")[:200] + "...",
                            "latency_ms": entry.get("latency_ms"),
                            "timestamp": entry.get("timestamp"),
                            "format": entry.get("format")
                        }
                        break
        except:
            pass
    
    return {
        "status": "🟢 RESONANZ AKTIV",
        "service": "syntx-field-resonance",
        "version": "3.3.0",
        "format_loader": "🔥 AKTIV" if FORMAT_LOADER_AVAILABLE else "❌ NICHT VERFÜGBAR",
        "last_response": last_response
    }


@router.get("/api/chat/health")
async def chat_health():
    """Health für Compatibility"""
    return await resonance_health()


@router.get("/resonanz/health/wrappers")
async def wrapper_health():
    """🏥 Wrapper Orphan Detection"""
    from .resonance.wrapper_meta import check_health
    return check_health()


@router.post("/resonanz/health/fix")
async def fix_wrapper_health():
    """🔧 Auto-Fix Orphans"""
    from .resonance.wrapper_meta import auto_fix_orphans
    return auto_fix_orphans()
