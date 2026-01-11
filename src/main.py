from fastapi import HTTPException
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🌊⚡💎 SYNTX FIELD RESONANCE SERVICE v3.3 💎⚡🌊                          ║
║                                                                              ║
║    DER RESONANZ-ORCHESTRATOR                                                 ║
║                                                                              ║
║    Diese Datei ist NUR für:                                                  ║
║      - App Initialization                                                    ║
║      - Router Loading                                                        ║
║      - Middleware                                                            ║
║                                                                              ║
║    Alles andere lebt in eigenen Strömen.                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .streams import FORMAT_LOADER_AVAILABLE


# ═══════════════════════════════════════════════════════════════════════════════
#  🚀 APP LIFECYCLE
# ═══════════════════════════════════════════════════════════════════════════════

from .resonance.drift_api import router as drift_router
from .resonance.wrapper_feld_resonanz import router as wrapper_feld_resonanz_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Das Resonanz-Feld öffnet sich."""
    print("=" * 80)
    print("🌊⚡💎 SYNTX FIELD RESONANCE SERVICE v3.3 💎⚡🌊")
    print("=" * 80)
    print(f"Backend:      {settings.backend_url}")
    print(f"Model:        {settings.model_name}")
    print(f"Wrappers:     {settings.wrapper_dir}")
    print(f"Formats:      /opt/syntx-config/formats/")
    print(f"Styles:       /opt/syntx-config/styles/")
    print(f"Logs:         {settings.log_dir}")
    print(f"Format Loader: {'🔥 AKTIV' if FORMAT_LOADER_AVAILABLE else '❌ NICHT VERFÜGBAR'}")
    print("=" * 80)
    print("🆕 NEUE STRÖME:")
    print("  /resonanz/chat/diff       → Wrapper-Vergleich")
    print("  /resonanz/sessions        → Session-Replay")
    print("  /resonanz/alchemy/preview → Live Wort-Transmutation")
    print("=" * 80)
    yield
    print("🌊 Resonanz-Feld schließt sich...")


# ═══════════════════════════════════════════════════════════════════════════════
#  🏗️ APP INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="🌊 SYNTX Field Resonance",
    description="Nicht API - RESONANZ-ORCHESTRATOR. Wrapper (WIE) + Format (WAS) + Style (FINISH) = Kalibrierte Antworten.",
    version="3.3.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════════
#  🔌 ROUTER LOADING - Alle Ströme zusammenführen
# ═══════════════════════════════════════════════════════════════════════════════

# Local Routers
from .health import router as health_router
from .chat import router as chat_router
from .endpoints import router as endpoints_router

# Core Resonance Routers
from .resonance.wrappers import router as wrappers_router
from .resonance.streams import router as streams_router
from .resonance.stats import router as stats_router
from .resonance.config import router as config_router
from .resonance.formats import router as formats_router
from .resonance.styles import router as styles_router

# 🆕 Neue Ströme
from .resonance.diff import router as diff_router
from .resonance.sessions import router as sessions_router
from .resonance.alchemy import router as alchemy_router
from .resonance.scoring import router as scoring_router
from api.profiles_crud import router as profiles_crud_router
from .resonance.scoring import router as scoring_router

# Include all routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(endpoints_router)
app.include_router(wrappers_router)
app.include_router(streams_router)
app.include_router(stats_router)
app.include_router(config_router, prefix="/resonanz")
app.include_router(formats_router)
app.include_router(styles_router)
app.include_router(diff_router)
app.include_router(sessions_router)
app.include_router(alchemy_router)
app.include_router(scoring_router)
app.include_router(drift_router)
app.include_router(scoring_router)
app.include_router(profiles_crud_router)

print("✅ 14 Router geladen - DER STROM FLIESST!")


# ═══════════════════════════════════════════════════════════════
# FORMAT-PROFILE MAPPING CRUD (COMPREHENSIVE)
# ═══════════════════════════════════════════════════════════════

from pathlib import Path
import json
from datetime import datetime

MAPPING_FILE = Path("/opt/syntx-config/mapping.json")
PROFILES_DIR = Path("/opt/syntx/profiles")


def load_mapping():
    """Load format-profile mapping"""
    if not MAPPING_FILE.exists():
        return {
            "version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "mappings": {},
            "available_profiles": {},
            "stats": {"total_formats": 0, "total_profiles": 0}
        }
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_mapping(data: dict):
    """Save format-profile mapping"""
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    
    # Update stats
    data["stats"]["total_formats"] = len(data.get("mappings", {}))
    data["stats"]["total_profiles"] = len(data.get("available_profiles", {}))
    
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.get("/mapping/formats")
async def get_all_format_mappings():
    """
    Get all format-to-profile mappings
    
    Returns complete mapping configuration including:
    - All format mappings
    - Available profiles
    - Drift scoring templates
    - Statistics
    """
    mapping_data = load_mapping()
    
    return {
        "erfolg": True,
        "version": mapping_data.get("version"),
        "total_formats": len(mapping_data.get("mappings", {})),
        "total_profiles": len(mapping_data.get("available_profiles", {})),
        "mappings": mapping_data.get("mappings", {}),
        "available_profiles": mapping_data.get("available_profiles", {}),
        "drift_templates": mapping_data.get("drift_prompt_templates", {}),
        "stats": mapping_data.get("stats", {})
    }


@app.get("/mapping/formats/{format_name}")
async def get_format_mapping(format_name: str):
    """
    Get profile mapping for specific format
    
    Returns:
    - Assigned profile_id
    - Drift scoring configuration
    - Format metadata
    """
    mapping_data = load_mapping()
    
    format_mapping = mapping_data.get(format_name)
    
    if not format_mapping:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    # Get profile details
    profile_id = format_mapping.get("profile_id")
    profile_info = mapping_data.get("available_profiles", {}).get(profile_id, {})
    
    return {
        "erfolg": True,
        "format": format_name,
        "mistral_wrapper": format_mapping.get("mistral_wrapper"),
        "gpt_wrapper": format_mapping.get("gpt_wrapper"),
        "profile_id": profile_id,
        "profile_info": profile_info,
        "drift_scoring": format_mapping.get("drift_scoring", {}),
        "metadata": format_mapping.get("metadata", {}),
        "message": f"✅ Mapping für Format '{format_name}' geladen"
    }


@app.post("/mapping/formats/{format_name}")
async def create_or_update_format_mapping(
    format_name: str,
    mapping_config: dict
):
    """
    Create or update format-to-profile mapping
    
    Body:
    {
      "profile_id": "soft_diagnostic_profile_v2",
      "drift_scoring": {
        "enabled": true,
        "scorer_model": "gpt-4",
        "prompt_template": "drift_analysis_v1"
      },
      "metadata": {
        "format_type": "diagnostic",
        "primary_use": "Drift Detection",
        "field_count": 6,
        "complexity": "high"
      }
    }
    """
    mapping_data = load_mapping()
    
    # Validate profile exists
    profile_id = mapping_config.get("profile_id")
    if profile_id and profile_id not in mapping_data.get("available_profiles", {}):
        raise HTTPException(
            status_code=400,
            detail=f"⚠️ Profile '{profile_id}' not found in available_profiles"
        )
    
    # Create or update mapping
    if "mappings" not in mapping_data:
        mapping_data["mappings"] = {}
    
    mapping_data["mappings"][format_name] = {
        "profile_id": profile_id,
        "drift_scoring": mapping_config.get("drift_scoring", {
            "enabled": False,
            "scorer_model": None,
            "prompt_template": None
        }),
        "metadata": mapping_config.get("metadata", {})
    }
    
    # Save
    save_mapping(mapping_data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "profile_id": profile_id,
        "drift_scoring_enabled": mapping_config.get("drift_scoring", {}).get("enabled", False),
        "message": f"💎 Mapping für Format '{format_name}' gespeichert"
    }


@app.put("/mapping/formats/{format_name}/profile")
async def update_format_profile(
    format_name: str,
    profile_update: dict
):
    """
    Update only the profile_id for a format
    
    Body:
    {
      "profile_id": "new_profile_name"
    }
    """
    mapping_data = load_mapping()
    
    if format_name not in mapping_data.get("mappings", {}):
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    profile_id = profile_update.get("profile_id")
    if not profile_id:
        raise HTTPException(
            status_code=400,
            detail="⚠️ profile_id required"
        )
    
    # Update profile
    mapping_data["mappings"][format_name]["profile_id"] = profile_id
    
    # Save
    save_mapping(mapping_data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "old_profile": mapping_data["mappings"][format_name].get("profile_id"),
        "new_profile": profile_id,
        "message": f"🔄 Profile updated for format '{format_name}'"
    }


@app.put("/mapping/formats/{format_name}/drift-scoring")
async def update_drift_scoring_config(
    format_name: str,
    drift_config: dict
):
    """
    Update drift scoring configuration for a format
    
    Body:
    {
      "enabled": true,
      "scorer_model": "gpt-4",
      "prompt_template": "drift_analysis_v1"
    }
    """
    mapping_data = load_mapping()
    
    if format_name not in mapping_data.get("mappings", {}):
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    # Update drift scoring
    mapping_data["mappings"][format_name]["drift_scoring"] = drift_config
    
    # Save
    save_mapping(mapping_data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "drift_scoring": drift_config,
        "message": f"⚡ Drift scoring config updated for '{format_name}'"
    }


@app.delete("/mapping/formats/{format_name}")
async def delete_format_mapping(format_name: str):
    """
    Delete format-to-profile mapping
    """
    mapping_data = load_mapping()
    
    if format_name not in mapping_data.get("mappings", {}):
        raise HTTPException(
            status_code=404,
            detail=f"❌ Format '{format_name}' has no mapping"
        )
    
    # Remove mapping
    removed = mapping_data["mappings"].pop(format_name)
    
    # Save
    save_mapping(mapping_data)
    
    return {
        "erfolg": True,
        "format": format_name,
        "removed_mapping": removed,
        "message": f"🗑️ Mapping für Format '{format_name}' gelöscht"
    }


@app.get("/mapping/profiles")
async def get_available_profiles():
    """
    Get all available scoring profiles
    """
    mapping_data = load_mapping()
    
    return {
        "erfolg": True,
        "total_profiles": len(mapping_data.get("available_profiles", {})),
        "profiles": mapping_data.get("available_profiles", {}),
        "message": "✅ Available profiles loaded"
    }


@app.get("/mapping/stats")
async def get_mapping_stats():
    """
    Get mapping statistics and analytics
    """
    mapping_data = load_mapping()
    
    mappings = mapping_data.get("mappings", {})
    
    # Calculate stats
    drift_enabled_count = sum(
        1 for m in mappings.values()
        if m.get("drift_scoring", {}).get("enabled", False)
    )
    
    profile_usage = {}
    for format_name, mapping in mappings.items():
        profile_id = mapping.get("profile_id")
        if profile_id:
            profile_usage[profile_id] = profile_usage.get(profile_id, 0) + 1
    
    complexity_distribution = {}
    for mapping in mappings.values():
        complexity = mapping.get("metadata", {}).get("complexity", "unknown")
        complexity_distribution[complexity] = complexity_distribution.get(complexity, 0) + 1
    
    return {
        "erfolg": True,
        "stats": {
            "total_formats": len(mappings),
            "total_profiles": len(mapping_data.get("available_profiles", {})),
            "drift_enabled_formats": drift_enabled_count,
            "drift_disabled_formats": len(mappings) - drift_enabled_count,
            "profile_usage": profile_usage,
            "complexity_distribution": complexity_distribution,
            "last_updated": mapping_data.get("last_updated")
        },
        "message": "📊 Mapping statistics calculated"
    }



# ═══════════════════════════════════════════════════════════════════════════════
#  🌀 GPT-WRAPPER-FELD STROEME – SYNTX FELDRESONANZ ARCHITEKTUR
# ═══════════════════════════════════════════════════════════════════════════════
from src.resonance.gpt_wrapper_feld_stroeme import router as gpt_wrapper_feld_router
from src.resonance.mapping_format_resonanz import router as mapping_format_router

# GPT-WRAPPER-FELD STROEME INTEGRIEREN
app.include_router(gpt_wrapper_feld_router)
app.include_router(mapping_format_router, prefix="/mapping", tags=["Mapping Format Resonanz"])
app.include_router(wrapper_feld_resonanz_router)
