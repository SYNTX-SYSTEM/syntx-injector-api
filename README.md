# 🔥 SYNTX Injector API v3.2

**Der Strom der semantischen Resonanz.**
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                    ║
║   │   WRAPPER   │────▶│   FORMAT    │────▶│    STYLE    │                    ║
║   │  (WIE denkt │     │ (WAS kommt  │     │ (WIE klingt │                    ║
║   │   das LLM?) │     │    raus?)   │     │     es?)    │                    ║
║   └─────────────┘     └─────────────┘     └─────────────┘                    ║
║          │                   │                   │                           ║
║          └───────────────────┴───────────────────┘                           ║
║                              │                                                ║
║                       ┌──────▼──────┐                                        ║
║                       │    CHAT     │                                        ║
║                       │ (Der Strom) │                                        ║
║                       └─────────────┘                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🚀 Quick Start
```bash
# Health Check
curl https://dev.syntx-system.com/health

# Simple Chat
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Was ist ein System?"}'

# Chat mit ALLEM
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analysiere KI",
    "mode": "syntex_wrapper_sigma",
    "format": "sigma",
    "style": "wissenschaftlich",
    "debug": true
  }'
```

## 🎯 Features

### ✅ Wrapper (WIE denkt das LLM?)
System-Prompts die vor dem User-Prompt injiziert werden.
```bash
GET  /resonanz/wrappers              # Liste
GET  /resonanz/wrapper/{name}        # Content
POST /resonanz/wrapper               # Erstellen
PUT  /resonanz/wrapper/{name}        # Updaten
DELETE /resonanz/wrapper/{name}      # Löschen
```

### ✅ Formate (WAS kommt raus?)
Feld-Definitionen die den Output strukturieren.
```bash
GET  /resonanz/formats               # Liste
GET  /resonanz/formats?domain=X      # Filter nach Domain
GET  /resonanz/formats/{name}        # Details
POST /resonanz/formats/quick         # Schnell erstellen
DELETE /resonanz/formats/{name}      # Löschen
```

**Features:**
- **Domains:** `technical`, `psychology`, `analysis`, `raw`
- **Vererbung:** `"extends": "parent_format"` merged Felder
- **Feld-Typen:** `text`, `list`, `rating`, `keywords`

### ✅ Styles (WIE klingt es?)
Post-Processing Alchemy nach der LLM-Generierung.
```bash
GET /resonanz/styles                 # Liste
GET /resonanz/styles/{name}          # Details
```

**Verfügbare Styles:**
| Style | Vibe | Beispiel |
|-------|------|----------|
| `wissenschaftlich` | Der Laborkittel | wichtig → signifikant |
| `zynisch` | Der Augenroll-Transformer | nachhaltig → greenwashing-kompatibel |
| `poetisch` | Der Wortwebstuhl | System → Gewebe |
| `berlin_slang` | Späti-Philosophie | Das → Dit |

### ✅ Debug-Modus
```bash
curl -X POST .../resonanz/chat \
  -d '{"prompt": "Test", "debug": true}'
```
Zeigt `debug_info` mit:
- `wrapper_chain`
- `format_name`
- `style_applied`
- `prompt_length`

## 📊 Stats & Streams
```bash
GET /resonanz/stats                  # Globale Statistiken
GET /resonanz/stats/wrapper/{name}   # Pro-Wrapper Stats
GET /resonanz/strom?limit=10         # Feld-Flow Events
GET /resonanz/training?limit=10      # Training-Export
```

## 🏥 Health & Admin
```bash
GET  /health                         # System Status
GET  /resonanz/health                # Resonanz Status
GET  /resonanz/health/wrappers       # Orphan Detection
POST /resonanz/health/fix            # Auto-Fix
```

## 📋 Chat Request Schema
```json
{
  "prompt": "...",           // Required: Die Frage
  "mode": "wrapper_name",    // Optional: Welcher Wrapper
  "format": "format_name",   // Optional: Welches Format
  "style": "style_name",     // Optional: Welcher Style
  "debug": false,            // Optional: Debug-Info zeigen
  "language": "de",          // Optional: de/en
  "max_new_tokens": 500,     // Optional: Max Tokens
  "temperature": 0.7         // Optional: Kreativität
}
```

## 📁 Ordnerstruktur
```
/opt/syntx-config/
├── wrappers/           # .txt Wrapper-Dateien
│   └── meta/           # .json Metadaten
├── formats/            # .json Format-Definitionen
└── styles/             # .json Style-Definitionen

/opt/syntx-injector-api/
├── src/
│   ├── main.py         # FastAPI App
│   ├── models.py       # Pydantic Schemas
│   ├── streams.py      # Wrapper Loading
│   ├── formats/        # Format Loader
│   └── styles/         # Style Alchemist
└── api_calls_wrapper.sh  # API Tester v5.0
```

## 🧪 API Tester
```bash
# Alle Tests (gegen Production)
./api_calls_wrapper.sh

# Lokal testen
./api_calls_wrapper.sh http://localhost:8001

# Verbose Mode
./api_calls_wrapper.sh --verbose
```

## 📈 Statistiken

- **33 Endpoints**
- **9 Formate** (mit Vererbung + Typen)
- **4 Styles** (mit Word Alchemy)
- **14 Wrappers**

---

**SYNTX FIELD RESONANCE** - Der Strom kennt keine Grenzen ⚡💎🌊

*Built with love and late-night coffee in Berlin.*
