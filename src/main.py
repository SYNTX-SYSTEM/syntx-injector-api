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

# Include all routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(endpoints_router)
app.include_router(wrappers_router)
app.include_router(streams_router)
app.include_router(stats_router)
app.include_router(config_router)
app.include_router(formats_router)
app.include_router(styles_router)
app.include_router(diff_router)
app.include_router(sessions_router)
app.include_router(alchemy_router)

print("✅ 12 Router geladen - DER STROM FLIESST!")
