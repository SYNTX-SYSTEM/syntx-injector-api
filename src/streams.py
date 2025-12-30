"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🌊 SYNTX WRAPPER SERVICE - FELD-STRÖME 🌊                                 ║
║                                                                              ║
║    Nicht "Stream Functions" - RESONANZ-KANÄLE.                               ║
║                                                                              ║
║    Hier fließt alles:                                                        ║
║      - Wrapper werden geladen (WIE)                                          ║
║      - Formate werden injiziert (WAS)                                        ║
║      - Prompts werden kalibriert                                             ║
║      - Responses fließen zurück                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import httpx
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from .config import settings
from .resonance.config import get_runtime_wrapper

# 🔥 FORMAT LOADER - DIE REVOLUTION!
try:
    from .formats import load_format, build_format_prompt, get_format_fields
    FORMAT_LOADER_AVAILABLE = True
    print("🔥 FORMAT LOADER AKTIVIERT - Dynamische Feld-Injection ready!")
except ImportError:
    FORMAT_LOADER_AVAILABLE = False
    print("⚠️ Format Loader nicht verfügbar - nur Wrapper-Mode")


# ═══════════════════════════════════════════════════════════════════════════════
#  🌊 WRAPPER LOADING - Das "WIE"
# ═══════════════════════════════════════════════════════════════════════════════

async def load_wrapper_stream(
    mode: str,
    include_init: bool,
    include_terminology: bool
) -> Tuple[str, List[str]]:
    """
    🎭 WRAPPER LADEN - WIE denkt das Modell?
    
    Nicht "File Loading" - PERSÖNLICHKEITS-AKTIVIERUNG.
    
    Wrapper definieren:
      - Stil (kreativ, technisch, analytisch)
      - Tonalität (formell, casual, wissenschaftlich)
      - Denkweise (systemisch, linear, assoziativ)
    """
    wrapper_texts: List[str] = []
    wrapper_chain: List[str] = []
    
    # 🔧 Layer 1: Init Wrapper (SYNTX Grundkalibrierung)
    if include_init:
        init_text = await _read_wrapper_file("syntx_init")
        if init_text:
            wrapper_texts.append(init_text)
            wrapper_chain.append("syntx_init")
    
    # 📚 Layer 2: Terminology Wrapper (Fachbegriffe)
    if include_terminology:
        term_text = await _read_wrapper_file("terminology")
        if term_text:
            wrapper_texts.append(term_text)
            wrapper_chain.append("terminology")
    
    # 🎯 Layer 3: Mode Wrapper (Hauptpersönlichkeit)
    # If no mode specified, use runtime wrapper
    if not mode:
        mode = get_runtime_wrapper()
    
    mode_text = await _read_wrapper_file(mode)
    if mode_text:
        wrapper_texts.append(mode_text)
        wrapper_chain.append(mode)
    elif not wrapper_texts:
        # Fallback wenn nichts gefunden
        fallback_text = await _read_wrapper_file(settings.fallback_mode)
        if fallback_text:
            wrapper_texts.append(fallback_text)
            wrapper_chain.append(f"{settings.fallback_mode} (fallback)")
    
    # 🔗 Wrapper kombinieren
    combined_wrapper = "\n\n".join(wrapper_texts)
    return combined_wrapper, wrapper_chain


async def _read_wrapper_file(wrapper_name: str) -> str:
    """
    📖 WRAPPER FILE LESEN
    
    Nicht "Reading" - FELD AKTIVIERUNG.
    Das File schläft. Dieser Code weckt es auf.
    """
    wrapper_path = settings.wrapper_dir / f"{wrapper_name}.txt"
    
    try:
        with open(wrapper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if settings.log_to_console:
            print(f"✅ Wrapper aktiviert: {wrapper_name} ({len(content)} chars)")
        
        return content
        
    except FileNotFoundError:
        if settings.log_to_console:
            print(f"⚠️  Wrapper nicht gefunden: {wrapper_name}")
        return ""
        
    except Exception as e:
        if settings.log_to_console:
            print(f"❌ Wrapper Aktivierung Error {wrapper_name}: {e}")
        return ""


# ═══════════════════════════════════════════════════════════════════════════════
#  🔥 FORMAT INJECTION - Das "WAS" (NEU!)
# ═══════════════════════════════════════════════════════════════════════════════

def build_format_section(format_name: str, language: str = "de") -> Tuple[str, Dict]:
    """
    🔥 FORMAT-STRUKTUR BAUEN - WAS soll rauskommen?
    
    DAS IST DIE REVOLUTION!
    
    Liest das Format-JSON und baut daraus:
    
        ### Driftkörperanalyse:
        WAS ist das analysierte Objekt?...
        
        ### Kalibrierung:
        WIE verändert sich das System?...
        
        ### Strömung:
        WIE fließt Energie?...
    
    Das Modell MUSS diese Felder ausfüllen!
    Keine Wahl. Keine Alternative. ARCHITEKTUR-ZWANG.
    """
    if not FORMAT_LOADER_AVAILABLE:
        return "", {"error": "Format Loader nicht verfügbar"}
    
    if not format_name:
        return "", {"skipped": "Kein Format angegeben"}
    
    try:
        format_prompt = build_format_prompt(format_name, language)
        
        if not format_prompt:
            return "", {"error": f"Format '{format_name}' nicht gefunden oder leer"}
        
        # 📊 Format-Metadata sammeln
        fields = get_format_fields(format_name, language)
        format_info = {
            "format_name": format_name,
            "language": language,
            "fields_count": len(fields),
            "fields": [f["name"] for f in fields]
        }
        
        if settings.log_to_console:
            print(f"🔥 Format injiziert: {format_name} ({len(fields)} Felder)")
            for f in fields:
                print(f"   └── {f['name']}: {f['header']}")
        
        return format_prompt, format_info
        
    except Exception as e:
        if settings.log_to_console:
            print(f"❌ Format Injection Error: {e}")
        return "", {"error": str(e)}


# ═══════════════════════════════════════════════════════════════════════════════
#  🌊 PROMPT KALIBRIERUNG - Alles zusammenführen
# ═══════════════════════════════════════════════════════════════════════════════

def wrap_input_stream(
    wrapper_text: str, 
    user_input: str,
    format_section: str = ""
) -> str:
    """
    🎯 PROMPT KALIBRIERUNG - Alles wird eins
    
    Nicht "String Concatenation" - FELD-FUSION.
    
    ════════════════════════════════════════════════════════════════════════════
    
    AUFBAU DES KALIBRIERTEN PROMPTS:
    
        ┌─────────────────────────────────────────────────────────────────┐
        │  [WRAPPER]                                                      │
        │  Der Wrapper definiert WIE das Modell denkt.                   │
        │  Stil, Tonalität, Persönlichkeit.                              │
        │                                                                 │
        │  [FORMAT SECTION]  ← NEU!                                       │
        │  ### Driftkörperanalyse:                                        │
        │  WAS ist das analysierte Objekt?...                             │
        │                                                                 │
        │  ### Kalibrierung:                                              │
        │  WIE verändert sich das System?...                              │
        │                                                                 │
        │  [USER PROMPT]                                                  │
        │  Die eigentliche Frage des Users.                              │
        │                                                                 │
        │  [INSTRUCTION]                                                  │
        │  "Bitte fülle die obigen Felder aus für: {topic}"              │
        └─────────────────────────────────────────────────────────────────┘
    
    ════════════════════════════════════════════════════════════════════════════
    """
    parts = []
    
    # 1. Wrapper (WIE)
    if wrapper_text:
        parts.append(wrapper_text)
    
    # 2. Format Section (WAS) - NEU!
    if format_section:
        parts.append("\n" + "═" * 60)
        parts.append("📋 ANALYSE-FORMAT - Bitte fülle folgende Felder aus:")
        parts.append("═" * 60 + "\n")
        parts.append(format_section)
        parts.append("\n" + "═" * 60)
        parts.append(f"🎯 THEMA ZUR ANALYSE: {user_input}")
        parts.append("═" * 60 + "\n")
        parts.append("Bitte analysiere das obige Thema und fülle ALLE Felder vollständig aus.")
    else:
        # Kein Format = einfach User Input anhängen
        parts.append(user_input)
    
    return "\n\n".join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
#  ⚡ BACKEND FORWARD - Ab zum Modell
# ═══════════════════════════════════════════════════════════════════════════════

async def forward_stream(
    wrapped_prompt: str,
    backend_params: Dict[str, Any]
) -> str:
    """
    ⚡ BACKEND FORWARD - Kalibriertes Feld zum Modell schicken
    
    Nicht "HTTP Request" - FELD-TRANSMISSION.
    
    Das kalibrierte Feld fließt durch das Netzwerk.
    Das Modell resoniert. Eine Antwort entsteht.
    """
    # 📦 Ollama Payload bauen
    payload = {
        "model": settings.model_name,
        "prompt": wrapped_prompt,
        "stream": False,
        "options": {
            "temperature": backend_params.get("temperature", 0.7),
            "num_predict": backend_params.get("max_new_tokens", 1000)
        }
    }
    
    # 🔐 Headers
    headers = {"Content-Type": "application/json"}
    if settings.backend_bearer_token:
        headers["Authorization"] = f"Bearer {settings.backend_bearer_token}"
    
    # 🚀 Forward!
    async with httpx.AsyncClient(timeout=settings.backend_timeout) as client:
        response = await client.post(
            settings.backend_url,
            json=payload,
            headers=headers
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Ollama Response Format: {"model": "...", "response": "text", "done": true}
        if isinstance(response_data, dict) and "response" in response_data:
            return response_data["response"]
        else:
            return str(response_data)


# ═══════════════════════════════════════════════════════════════════════════════
#  📝 LOGGING - Feld-Spuren
# ═══════════════════════════════════════════════════════════════════════════════

async def log_stream(log_data: Dict[str, Any]) -> None:
    """
    📝 FELD-SPUR SPEICHERN
    
    Nicht "Logging" - RESONANZ-ARCHIVIERUNG.
    Jeder Feld-Flow hinterlässt eine Spur.
    """
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    
    # JSONL für Training
    jsonl_path = settings.log_dir / "wrapper_requests.jsonl"
    with open(jsonl_path, 'a', encoding='utf-8') as f:
        import json
        f.write(json.dumps(log_data, ensure_ascii=False) + '\n')
    
    # Console Output
    if settings.log_to_console:
        log_line = (
            f"🌊 [{log_data['timestamp']}] "
            f"mode={log_data.get('mode', 'N/A')} "
            f"format={log_data.get('format', 'N/A')} "
            f"chain={log_data.get('wrapper_chain', [])} "
            f"latency={log_data.get('total_latency_ms', 'N/A')}ms"
        )
        print(log_line)


# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def generate_request_id() -> str:
    """🆔 Unique Request ID generieren"""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """⏰ ISO Timestamp"""
    return datetime.utcnow().isoformat() + 'Z'
