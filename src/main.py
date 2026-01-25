import os
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
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  🔥 GPT AUTO-TRIGGER SYSTEM VALIDATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Check OpenAI API Key
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY konfiguriert - GPT Auto-Trigger verfügbar")
    else:
        print("⚠️  OPENAI_API_KEY nicht gesetzt - GPT Auto-Trigger deaktiviert!")
    
    # Check Bindings with Auto-Trigger
    bindings_dir = Path("/opt/syntx-config/scoring_bindings")
    if bindings_dir.exists():
        bindings = list(bindings_dir.glob("*.json"))
        auto_trigger_count = 0
        
        for binding_file in bindings:
            try:
                with open(binding_file, 'r', encoding='utf-8') as f:
                    binding = json.load(f)
                if binding.get("binding_metadata", {}).get("auto_trigger_after_mistral"):
                    auto_trigger_count += 1
            except Exception:
                pass
        
        print(f"📊 Scoring Bindings: {len(bindings)} total, {auto_trigger_count} mit Auto-Trigger aktiviert")
    
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

# ═══════════════════════════════════════════════════════════════════════════
#  🔥💎 SYNTX SCORING API v2.0 - Revolutionary Architecture
# ═══════════════════════════════════════════════════════════════════════════
from .api.scoring_router import router as scoring_v2_router
from .api.mapping_router import router as mapping_router
from .api.gpt_wrapper_router import router as gpt_wrapper_router
from api.profiles_crud import router as profiles_crud_router
from .resonance.scoring import router as scoring_router

# ═══════════════════════════════════════════════════════════════════════════
#  🔥💎 SYNTX SCORING API v2.0 - Revolutionary Architecture
# ═══════════════════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════════════════
#  🔥💎 SYNTX SCORING API v2.0 Router
#  
#  Revolutionary scoring architecture with:
#  - Clean separation: Profiles / Bindings / Entities
#  - Complete CRUD operations
#  - Magic endpoints for complete data retrieval
#  - SYNTX volltext naming
# ═══════════════════════════════════════════════════════════════════════════
app.include_router(scoring_v2_router)
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
PROFILES_DIR = Path("/opt/syntx-config/profiles")


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


app.include_router(mapping_router, prefix="/mapping", tags=["🗺️ Mapping"])
app.include_router(gpt_wrapper_router, tags=["🤖 GPT-Wrapper"])
app.include_router(wrapper_feld_resonanz_router)
