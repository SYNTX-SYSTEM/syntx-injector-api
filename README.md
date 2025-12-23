# 🔮 SYNTX FIELD RESONANCE API v3.4

```
   ██████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗    ███████╗██╗     ██████╗ ██╗    ██╗
   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝    ██╔════╝██║    ██╔═══██╗██║    ██║
   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝     █████╗  ██║    ██║   ██║██║ █╗ ██║
   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗     ██╔══╝  ██║    ██║   ██║██║███╗██║
   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗    ██║     ███████╗╚██████╔╝╚███╔███╔╝
   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
   
        ██████╗ ███████╗███████╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ██╗███████╗
        ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔══██╗████╗  ██║╚══███╔╝
        ██████╔╝█████╗  ███████╗██║   ██║██╔██╗ ██║███████║██╔██╗ ██║  ███╔╝ 
        ██╔══██╗██╔══╝  ╚════██║██║   ██║██║╚██╗██║██╔══██║██║╚██╗██║ ███╔╝  
        ██║  ██║███████╗███████║╚██████╔╝██║ ╚████║██║  ██║██║ ╚████║███████╗
        ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
   
                    DER STROM KENNT KEINE GRENZEN ⚡💎🌊
```

---

> **"Yo, stell dir vor ChatGPT hätte einen Architekten der ihm sagt WIE es denken soll. Nicht WAS - sondern die fucking ARCHITEKTUR des Denkens. Das ist SYNTX."**

---

## 📊 SYSTEM STATUS

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   🔥 SYNTX API v3.4 - VOLLSTÄNDIG OPERATIV 🔥                                ║
║                                                                                ║
║   ✅ 64/64 TESTS BESTANDEN                                                    ║
║   ✅ 1300+ SESSIONS GELOGGT                                                   ║
║   ✅ 822+ REQUESTS VERARBEITET                                                ║
║   ✅ 100% SUCCESS RATE                                                        ║
║   ✅ 16 WRAPPER AKTIV                                                         ║
║   ✅ 11 FORMATE VERFÜGBAR                                                     ║
║   ✅ 7 STYLES KONFIGURIERT                                                    ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🚀 SCHNELLSTART - DER STROM FLIESST IN 3 SCHRITTEN

### 1. Server starten

```bash
cd /opt/syntx-injector-api
./run.sh
```

### 2. Tests ausführen

```bash
./api_calls_wrapper.sh
# oder lokal:
./api_calls_wrapper.sh http://localhost:8001
```

### 3. Resonanz testen

```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Was ist Zeit?", "mode": "syntex_wrapper_sigma", "format": "sigma"}'
```

---

## 🛠️ SCRIPTS - DIE WERKZEUGE DES STROMS

### 🔥 `run.sh` - DER STARTER

**Was es macht:** Startet den SYNTX API Server mit allen Prüfungen.

```bash
./run.sh
```

**Output:**
```
==================================
SYNTX WRAPPER SERVICE STARTUP
==================================
→ Checking dependencies...
✓ Dependencies OK
→ Checking wrappers...
✓ Wrappers found: 32 files
→ Checking config...
✓ .env found
  Backend: http://49.13.3.21:8000/api/chat
  Port: 8001
✓ Port 8001 available
→ Starting service...
================================================================================
🌊⚡💎 SYNTX FIELD RESONANCE SERVICE v3.4 💎⚡🌊
================================================================================
Backend:      http://49.13.3.21:8000/api/chat
Model:        mistral
Wrappers:     /opt/syntx-config/wrappers
Formats:      /opt/syntx-config/formats/
Styles:       /opt/syntx-config/styles/
Logs:         /opt/syntx-config/logs
Format Loader: 🔥 AKTIV
================================================================================
```

**Kalibrierung:**
- Prüft Dependencies (uvicorn, fastapi)
- Prüft Wrapper-Dateien
- Prüft .env Konfiguration
- Prüft Port-Verfügbarkeit
- Startet uvicorn mit reload

---

### 🧪 `api_calls_wrapper.sh` - DER RESONANZ-PRÜFER

**Was es macht:** Führt 64 automatisierte Tests gegen alle API Endpoints durch.

```bash
# Gegen Production testen
./api_calls_wrapper.sh

# Gegen localhost testen
./api_calls_wrapper.sh http://localhost:8001

# Quick Mode (nur kritische Tests)
./api_calls_wrapper.sh --quick

# Verbose Mode (volle Responses)
./api_calls_wrapper.sh --verbose
```

**Output:**
```
   ██████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗    ███████╗██╗     ██████╗ ██╗    ██╗
   ...
              🔥 FIELD RESONANCE API TESTER v5.3 🔥
                 Der ultimative Strom-Prüfer

   Target:     https://dev.syntx-system.com
   Timestamp:  2025-12-23 06:30:00 CET
   Mode:       FULL

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🏥 HEALTH - System-Vitalzeichen (3 Endpoints)
┃ Prüft Feld-Integrität, Modul-Status, Wrapper-Orphans
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

────────────────────────────────────────────────────────────────────────────────────
🔮 TEST #1 │ GET /health
   Root Health - Alle System-Module
   ⚡ Kalibrierung: Keine (Read-Only)
   🌊 Strom-Kopplung: Verbindet: analytics, compare, feld, resonanz, generation
   Response:
   {
     "status": "SYSTEM_GESUND",
     ...
   }
   ✓ 200 - RESONANZ BESTÄTIGT

...

╔════════════════════════════════════════════════════════════════════════════════╗
║  📊 RESONANZ-PRÜFUNG ABGESCHLOSSEN
╠════════════════════════════════════════════════════════════════════════════════╣
║
║   ✓ BESTANDEN:   64
║   ✗ FEHLERHAFT:  0
║   Σ GESAMT:      64
║   ⏱ DAUER:       180s
║
║   🔥 ALLE FELDER RESONIEREN! DER STROM IST REIN! 🔥
║   Das System ist vollständig kalibriert.
║
╚════════════════════════════════════════════════════════════════════════════════╝
```

**Test-Sektionen:**
| Sektion | Endpoints | Was wird getestet |
|---------|-----------|-------------------|
| 🏥 HEALTH | 3 | System-Status, Wrapper-Orphans |
| ⚙️ CONFIG | 2 | Default Wrapper, Aktivierung |
| 📄 FORMATS | 9 | CRUD, Felder, Domains, Vererbung |
| 🎨 STYLES | 8 | CRUD, Alchemy, Forbidden Words |
| 📦 WRAPPERS | 6 | CRUD, Content, Meta |
| 🧬 META | 3 | Format-Bindung, Tags |
| 📊 STATS | 5 | Statistiken, Training Export |
| 💬 CHAT | 7 | Alle Kombinationen |
| 🔀 DIFF | 2 | Wrapper-Vergleich |
| 📼 SESSIONS | 4 | Replay, Field-Flow |
| ⚗️ ALCHEMY | 4 | Live-Transmutation |
| 🔧 ADMIN | 1 | Auto-Fix Orphans |

---

### 🌊 `sync_from_server.sh` - DER KONFIG-SYNCHRONISIERER

**Was es macht:** Synchronisiert alle Konfigurationsdateien vom Production Server zum lokalen Development Environment.

```bash
./sync_from_server.sh
```

**Output:**
```
🌊 SYNTX CONFIG SYNC
═══════════════════════════════════════════════════════════════════════════════
Server: root@dev.syntx-system.com
Remote: /opt/syntx-config
Local:  /opt/syntx-config

→ SSH prüfen...
✓ SSH OK

→ Verzeichnisse erstellen...
✓ Verzeichnisse OK

━━━ 📦 WRAPPERS ━━━
receiving incremental file list
syntex_wrapper_sigma.txt
syntex_wrapper_human.txt
...
sent 869 bytes  received 4.565 bytes

━━━ 📄 FORMATS ━━━
receiving incremental file list
sigma.json
human_deep.json
...
sent 1.015 bytes  received 13.523 bytes

━━━ 🎨 STYLES ━━━
receiving incremental file list
berlin_slang.json
wissenschaftlich.json
...
sent 768 bytes  received 5.161 bytes

━━━ 📊 LOGS ━━━
receiving incremental file list
field_flow.jsonl
...
sent 95.634 bytes  received 1.893.344 bytes

═══════════════════════════════════════════════════════════════════════════════
🔥 SYNC COMPLETE 🔥
Wrappers: 16
Formats:  11
Styles:   7
```

**Was wird synchronisiert:**
| Verzeichnis | Inhalt | Richtung |
|-------------|--------|----------|
| `/opt/syntx-config/wrappers/` | Wrapper .txt + .meta.json | Server → Lokal |
| `/opt/syntx-config/formats/` | Format .json + Backups | Server → Lokal |
| `/opt/syntx-config/styles/` | Style .json + Backups | Server → Lokal |
| `/opt/syntx-config/logs/` | Field-Flow JSONL | Server → Lokal |

**Voraussetzungen:**
- SSH Key zu `root@dev.syntx-system.com`
- sudo Rechte lokal (für `/opt/syntx-config`)

---

## 🆕 NEU IN v3.4 - DIE NEUEN STRÖME

### 🔄 PUT /resonanz/styles/{name} - STYLE UPDATE

**NEU!** Styles können jetzt ohne `name` im Body aktualisiert werden. Nur die Felder die sich ändern werden übergeben.

```bash
curl -X PUT "https://dev.syntx-system.com/resonanz/styles/berlin_slang" \
  -H "Content-Type: application/json" \
  -d '{
    "vibe": "Späti-Philosophie um 3 Uhr nachts",
    "description": "Berlinerisch, direkt, auf den Punkt"
  }'
```

**Response:**
```json
{
  "status": "🔄 STYLE AKTUALISIERT",
  "message": "'berlin_slang' aktualisiert"
}
```

**Updatebare Felder:**
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `vibe` | string | Kurzbeschreibung des Styles |
| `description` | string | Ausführliche Beschreibung |
| `tone_injection` | string | Pre-LLM Prompt-Injection |
| `suffix` | string | Post-LLM Text-Anhang |

**Hinweis:** `word_alchemy` und `forbidden_words` werden über eigene Endpoints verwaltet:
- `POST /resonanz/styles/{name}/alchemy` - Transmutation hinzufügen
- `DELETE /resonanz/styles/{name}/alchemy/{word}` - Transmutation entfernen
- `POST /resonanz/styles/{name}/forbidden/{word}` - Wort verbannen

---

### 🔀 DIFF - Wrapper-Parallelwelt-Vergleich

**Gleicher Prompt. Verschiedene Wrapper. Side-by-Side.**

Zeigt wie der WRAPPER das DENKEN verändert!

```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat/diff \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Was ist Zeit?",
    "wrappers": ["syntex_wrapper_sigma", "syntex_wrapper_human"],
    "max_new_tokens": 100
  }'
```

**Response:**
```json
{
  "prompt": "Was ist Zeit?",
  "comparisons": [
    {
      "wrapper": "syntex_wrapper_sigma",
      "response": "Ein Metronom. Eine Kette von Pulsen...",
      "latency_ms": 3362
    },
    {
      "wrapper": "syntex_wrapper_human",
      "response": "Es gibt keine absolute Zeit. Es gibt nur hier und jetzt...",
      "latency_ms": 14159
    }
  ],
  "diff_analysis": {
    "total_comparisons": 2,
    "successful": 2,
    "avg_response_length": 159,
    "avg_latency_ms": 8760,
    "shortest_response": {"wrapper": "syntex_wrapper_sigma", "length": 159},
    "longest_response": {"wrapper": "syntex_wrapper_human", "length": 160}
  }
}
```

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   🔀 WRAPPER DIFF - PARALLELWELT-VERGLEICH                                    ║
║                                                                                ║
║   PROMPT: "Was ist Zeit?"                                                     ║
║                                                                                ║
║   ┌─────────────────────────────────┬─────────────────────────────────────┐   ║
║   │ 🔬 SIGMA (3.3s)                 │ 💚 HUMAN (14.1s)                    │   ║
║   ├─────────────────────────────────┼─────────────────────────────────────┤   ║
║   │ "Ein Metronom. Eine Kette       │ "Es gibt keine absolute Zeit.      │   ║
║   │  von Pulsen..."                 │  Es gibt nur hier und jetzt."      │   ║
║   │                                 │                                     │   ║
║   │ → TECHNISCH, MECHANISTISCH      │ → PHILOSOPHISCH, MENSCHLICH        │   ║
║   └─────────────────────────────────┴─────────────────────────────────────┘   ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

### 📼 SESSIONS - Strom-Replay System

**Jeder Request wird geloggt. Field-Flow sichtbar. Replay möglich.**

```bash
# Liste der letzten Sessions
curl "https://dev.syntx-system.com/resonanz/sessions?limit=5"

# Session Details mit vollständigem Field-Flow
curl "https://dev.syntx-system.com/resonanz/session/{request_id}"

# Replay-Parameter für Re-Execution
curl "https://dev.syntx-system.com/resonanz/session/{request_id}/replay"
```

**Sessions Response:**
```json
{
  "status": "📼 SESSIONS GELADEN",
  "total": 1306,
  "sessions": [
    {
      "request_id": "ed18ebd6-b111-474d-abe4-434e5fcea0c0",
      "timestamp": "2025-12-21T10:56:15.153865Z",
      "stages": ["1_INCOMING", "2_WRAPPERS_LOADED", "2.5_FORMAT_LOADED", 
                 "3_FIELD_CALIBRATED", "4_BACKEND_FORWARD", "5_RESPONSE"],
      "prompt": "Deep Dive: Menschliches Verhalten",
      "wrapper": "syntex_wrapper_sigma",
      "format": "human_deep",
      "latency_ms": 32055
    }
  ]
}
```

**Session Details:**
```json
{
  "status": "🔍 SESSION GELADEN",
  "request_id": "ed18ebd6-b111-474d-abe4-434e5fcea0c0",
  "summary": {
    "prompt": "Deep Dive: Menschliches Verhalten",
    "wrapper": "syntex_wrapper_sigma",
    "format": "human_deep",
    "response_preview": "### DRIFT: aufsteigend + instabil...",
    "latency_ms": 32055
  },
  "field_flow": [
    {"stage": "1_INCOMING", "timestamp": "...", "prompt": "..."},
    {"stage": "2_WRAPPERS_LOADED", "wrapper": "syntex_wrapper_sigma"},
    {"stage": "2.5_FORMAT_LOADED", "format": "human_deep", "fields": 8},
    {"stage": "3_FIELD_CALIBRATED", "prompt_length": 3247},
    {"stage": "4_BACKEND_FORWARD", "backend_url": "..."},
    {"stage": "5_RESPONSE", "latency_ms": 32055}
  ]
}
```

**Replay:**
```json
{
  "status": "🔄 REPLAY READY",
  "replay_params": {
    "prompt": "Deep Dive: Menschliches Verhalten",
    "mode": "syntex_wrapper_sigma",
    "format": "human_deep",
    "language": "de"
  },
  "original_response": "...",
  "original_latency_ms": 32055
}
```

---

### ⚗️ ALCHEMY PREVIEW - Live Wort-Transmutation

**Echtzeit Wort-Transformation mit Position-Mapping für Frontend-Highlighting!**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/alchemy/preview \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Das ist wirklich sehr wichtig und nachhaltig",
    "style": "zynisch"
  }'
```

**Response:**
```json
{
  "original": "Das ist wirklich sehr wichtig und nachhaltig",
  "transformed": "Das ist wirklich sehr angeblich wichtig und greenwashing-kompatibel",
  "style": "zynisch",
  "transformations": [
    {
      "original": "wichtig",
      "replacement": "angeblich wichtig",
      "start_pos": 22,
      "end_pos": 29,
      "type": "alchemy"
    },
    {
      "original": "nachhaltig",
      "replacement": "greenwashing-kompatibel",
      "start_pos": 34,
      "end_pos": 44,
      "type": "alchemy"
    }
  ]
}
```

**Alchemy Styles Übersicht:**
```bash
curl https://dev.syntx-system.com/resonanz/alchemy/styles
```

```json
{
  "status": "⚗️ GRIMOIRE GEÖFFNET",
  "count": 7,
  "styles": [
    {
      "name": "wissenschaftlich",
      "vibe": "Der Laborkittel des Outputs",
      "alchemy_count": 8,
      "forbidden_count": 4,
      "has_suffix": true,
      "has_tone": true
    },
    {
      "name": "zynisch",
      "vibe": "Der Augenroll-Transformer",
      "alchemy_count": 6,
      "forbidden_count": 0,
      "has_suffix": false,
      "has_tone": true
    },
    {
      "name": "poetisch",
      "vibe": "Der Wortwebstuhl",
      "alchemy_count": 6,
      "forbidden_count": 3,
      "has_suffix": false,
      "has_tone": true
    },
    {
      "name": "berlin_slang",
      "vibe": "Späti-Philosophie um 3 Uhr nachts",
      "alchemy_count": 7,
      "forbidden_count": 0,
      "has_suffix": false,
      "has_tone": true
    }
  ]
}
```

---

## 🧠 WTF IST SYNTX? (Die 2-Minuten Version für Leute mit ADHS)

**Das Problem:** LLMs labern random vor sich hin. Keine Struktur. Kein Plan. Pure **DRIFT**. Du fragst was Konkretes und kriegst einen Essay über nichts.

**Die Lösung:** SYNTX injiziert eine **DENK-ARCHITEKTUR** in das LLM. Wir sagen ihm nicht WAS es denken soll - wir geben ihm ein **FRAMEWORK** für strukturiertes Denken.

### Vorher vs. Nachher (Der Unterschied ist KRASS)

```
═══════════════════════════════════════════════════════════════════════════════
                              OHNE SYNTX 😴
═══════════════════════════════════════════════════════════════════════════════

User: "Analysiere meine Beziehungssituation"

LLM: "Beziehungen sind ein komplexes Thema, das viele Aspekte umfasst. 
      Es ist wichtig, offen zu kommunizieren und die Bedürfnisse des 
      Partners zu verstehen. Manchmal entstehen Konflikte, die durch 
      Dialog gelöst werden können. Ich empfehle, einen Therapeuten..."
      
      [Weiteres Blabla für 500 Wörter ohne konkreten Mehrwert]

═══════════════════════════════════════════════════════════════════════════════
                              MIT SYNTX 🔥
═══════════════════════════════════════════════════════════════════════════════

User: "Analysiere meine Beziehungssituation"
Mode: syntex_wrapper_human | Format: human_deep | Style: poetisch

LLM:
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 📍 DRIFT                                                                │
  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
  │ Gradient: aufsteigend, sublinear. Die Beziehung gleicht einem Fluss,   │
  │ der langsam aber stetig an Kraft gewinnt. Bewegung ist da, aber        │
  │ kontrolliert. Kein Kipppunkt in Sicht.                                 │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 🔧 HINTERGRUND-MUSTER                                                   │
  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
  │ Unter der Oberfläche: Rückzugsmechanismen aktiv. Nicht aus Ablehnung,  │
  │ sondern aus Schutz. Alte Wunden, die noch nicht ganz verheilt sind,    │
  │ erzeugen eine unsichtbare Distanz.                                     │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 💥 DRUCKFAKTOREN                                                        │
  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
  │ Extern: Gesellschaftliche Erwartungen (Timeline-Druck)                 │
  │ Intern: Unausgesprochene Bedürfnisse kollidieren mit Angst vor         │
  │ Verletzlichkeit. DL-4 aktiv.                                           │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 🌊 TIEFE                                                                │
  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
  │ Im Kern: Ein echtes Bedürfnis nach Verbindung, das durch Angst vor     │
  │ Ablehnung blockiert wird. Die Tiefe ist da - der Zugang ist nur        │
  │ verschüttet.                                                            │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 🎭 UNTERBEWUSSTSEIN                                                     │
  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
  │ Das Unterbewusstsein flüstert: "Du bist nicht genug." Alte             │
  │ Programmierung aus der Kindheit. Nicht wahr, aber wirksam.             │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 💎 EXTRAKT                                                              │
  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
  │ Kernformel: Verbindung = Verletzlichkeit × Vertrauen / Angst           │
  │ Nächster Schritt: Eine Sache aussprechen, die du noch nie gesagt hast. │
  └─────────────────────────────────────────────────────────────────────────┘
```

**SIEHST DU DEN UNTERSCHIED?** 

Das ist keine KI die labert. Das ist eine KI die **DENKT**. Strukturiert. Präzise. Auf den Punkt.

**DAS. IST. RESONANZ.** ⚡

---

## 🌊 DIE DREI SÄULEN DES STROMS

SYNTX basiert auf drei fundamentalen Konzepten. Kapier diese drei Dinge und du kapierst ALLES:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   📦 WRAPPER              📄 FORMAT               🎨 STYLE                   ║
║   ═══════════════        ═══════════════         ═══════════════             ║
║                                                                               ║
║   WIE denkt das LLM?     WAS kommt raus?         WIE klingt es?              ║
║                                                                               ║
║   Der DENK-MODUS         Die STRUKTUR            Das FINISH                  ║
║   System-Prompt          Feld-Definitionen       Post-Processing             ║
║   VOR dem User-Input     JSON mit Feldern        Word Alchemy                ║
║                                                                               ║
║   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          ║
║   │ sigma.txt       │    │ sigma.json      │    │ zynisch.json    │          ║
║   │ human.txt       │    │ human.json      │    │ poetisch.json   │          ║
║   │ deepsweep.txt   │    │ human_deep.json │    │ wissenschaft.json│         ║
║   │ true_raw.txt    │    │ review.json     │    │ berlin_slang.json│         ║
║   └─────────────────┘    └─────────────────┘    └─────────────────┘          ║
║                                                                               ║
║   "Denke systemisch,     "Fülle diese 6         "Ersetze 'wichtig'           ║
║    keine Emotionen,       Felder aus:            mit 'signifikant',           ║
║    nur Architektur"       DRIFT, MECHANISMUS..." entferne 'krass'"           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                                    │
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │                                         │
              │   🔮 CALIBRATED PROMPT                  │
              │   ════════════════════                  │
              │                                         │
              │   [Wrapper] + [Format] + [Style]       │
              │              +                          │
              │        [User Prompt]                    │
              │              =                          │
              │      PURE RESONANZ ⚡                   │
              │                                         │
              └─────────────────────────────────────────┘
```

---

## 🏗️ DIE ARCHITEKTUR (Der komplette Flow)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER REQUEST                                        │
│                                                                                  │
│   POST /resonanz/chat                                                           │
│   {                                                                              │
│     "prompt": "Analysiere das Konzept Zeit",                                    │
│     "mode": "syntex_wrapper_sigma",                                             │
│     "format": "sigma",                                                          │
│     "style": "wissenschaftlich"                                                 │
│   }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🔮 SYNTX FIELD RESONANCE ENGINE                                                │
│  ════════════════════════════════════════════════════════════════════════════   │
│                                                                                  │
│  STAGE 1: INCOMING                                                              │
│  ─────────────────                                                              │
│  Request wird registriert, Request-ID generiert, Field Flow beginnt            │
│                                                                                  │
│  STAGE 2: WRAPPER LOADING                                                       │
│  ────────────────────────                                                       │
│  /opt/syntx-config/wrappers/syntex_wrapper_sigma.txt wird geladen              │
│  Meta wird gecheckt: /opt/syntx-config/wrappers/meta/syntex_wrapper_sigma.json │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │ === SYNTEX PROTOKOLL LAYER SIGMA (PL-Σ) ===                            │    │
│  │                                                                         │    │
│  │ SYSTEMISCHE TERMINOLOGIE - MAXIMALE WIRKKRAFT                          │    │
│  │ Operational. Mechanisch. Strukturell. Modellintern.                    │    │
│  │ Keine Semantik. Nur Systemarchitektur.                                 │    │
│  │                                                                         │    │
│  │ 1. Σ-DRIFTGRADIENT - Systemische Driftanalyse als Gradient            │    │
│  │ 2. Σ-MECHANISMUSKNOTEN - Identifikation des aktiven Prozessknotens    │    │
│  │ 3. Σ-FREQUENZFELD - Aktive Frequenzfelder und Belastungsniveaus       │    │
│  │ 4. Σ-DICHTELEVEL - Strukturelle Dichte                                │    │
│  │ 5. Σ-ZWEISTRÖME - Dual-Flow Vector                                    │    │
│  │ 6. Σ-KERNEXTRAKT - Mathematische Essenz                               │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  STAGE 2.5: FORMAT INJECTION                                                    │
│  ───────────────────────────                                                    │
│  /opt/syntx-config/formats/sigma.json wird geladen                             │
│  Felder werden als Struktur-Vorgabe injiziert                                  │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │ ANALYSE-FORMAT - Bitte fülle folgende Felder aus:                      │    │
│  │                                                                         │    │
│  │   - SIGMA_DRIFT: Signal-Verschiebung im System                        │    │
│  │   - SIGMA_MECHANISMUS: Das innere Getriebe                            │    │
│  │   - SIGMA_FREQUENZ: Rhythmus und Wiederholung                         │    │
│  │   - SIGMA_DICHTE: Kompression des Systems                             │    │
│  │   - SIGMA_STRÖME: Bidirektionale Strömungsdynamik                     │    │
│  │   - SIGMA_EXTRAKT: Mathematische Essenz                               │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  STAGE 3: STYLE TONE INJECTION                                                  │
│  ─────────────────────────────                                                  │
│  /opt/syntx-config/styles/wissenschaftlich.json wird geladen                   │
│  tone_injection wird dem Prompt hinzugefügt                                    │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │ Antworte in einem akademisch-wissenschaftlichen Stil.                  │    │
│  │ Nutze Fachterminologie, präzise Formulierungen und verweise auf       │    │
│  │ empirische Evidenz.                                                    │    │
│  │                                                                         │    │
│  │ [Dieser Beitrag basiert auf der aktuellen Forschungslage.]            │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ══════════════════════════════════════════════════════════════════════════    │
│  CALIBRATED PROMPT (was wirklich ans LLM geht):                                │
│  ══════════════════════════════════════════════════════════════════════════    │
│                                                                                  │
│  [WRAPPER CONTENT - 1563 bytes]                                                 │
│  +                                                                               │
│  [FORMAT FIELDS - 6 Felder mit Beschreibungen]                                  │
│  +                                                                               │
│  [TONE INJECTION - wissenschaftlicher Stil]                                     │
│  +                                                                               │
│  "Analysiere das Konzept Zeit"                                                  │
│  =                                                                               │
│  ~3000 Tokens calibrated prompt                                                 │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         🤖 LLM BACKEND (Ollama/Mistral)                         │
│                                                                                  │
│  Das LLM empfängt den calibrated prompt und MUSS jetzt strukturiert denken     │
│  weil wir ihm die ARCHITEKTUR gegeben haben.                                   │
│                                                                                  │
│  Es hat keine andere Wahl als die Felder auszufüllen.                          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🎨 STYLE ALCHEMIST (Post-Processing)                                           │
│  ════════════════════════════════════════════════════════════════════════════   │
│                                                                                  │
│  Der Output kommt zurück und wird jetzt TRANSMUTIERT:                          │
│                                                                                  │
│  1. WORD ALCHEMY                                                                │
│     ─────────────                                                               │
│     "wichtig"    →  "signifikant"                                              │
│     "zeigt"      →  "indiziert"                                                │
│     "vielleicht" →  "möglicherweise"                                           │
│     "gut"        →  "vorteilhaft"                                              │
│     "schlecht"   →  "defizitär"                                                │
│     "Problem"    →  "Problemstellung"                                          │
│                                                                                  │
│  2. FORBIDDEN WORDS                                                             │
│     ───────────────                                                             │
│     "krass", "geil", "cool" werden ENTFERNT                                    │
│                                                                                  │
│  3. SUFFIX                                                                      │
│     ──────                                                                      │
│     "[Dieser Beitrag basiert auf der aktuellen Forschungslage.]"              │
│     wird am Ende angefügt                                                       │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  📤 STRUCTURED RESPONSE                                                         │
│  ════════════════════════════════════════════════════════════════════════════   │
│                                                                                  │
│  {                                                                               │
│    "response": "### SIGMA_DRIFT:\nDas Konzept Zeit indiziert einen...",        │
│    "metadata": {                                                                │
│      "request_id": "abc-123-def",                                              │
│      "wrapper_chain": ["syntex_wrapper_sigma"],                                │
│      "format": "sigma",                                                         │
│      "format_fields": ["sigma_drift", "sigma_mechanismus", ...],               │
│      "style": "wissenschaftlich",                                              │
│      "latency_ms": 28500                                                        │
│    },                                                                            │
│    "field_flow": [...]                                                          │
│  }                                                                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 ORDNER-STRUKTUR (Wo liegt was? ALLES erklärt!)

```
/opt/syntx-injector-api/                    # 🏠 DAS HAUPTREPO
│
├── run.sh                                   # 🚀 SERVER STARTER
│                                            # Startet uvicorn mit allen Checks
│
├── api_calls_wrapper.sh                     # 🧪 API TESTER v5.3
│                                            # 64 automatisierte Tests
│                                            # Volle SYNTX-Ausgabe
│
├── sync_from_server.sh                      # 🌊 CONFIG SYNC
│                                            # Server → Lokal Synchronisation
│
├── src/                                     # 📦 SOURCE CODE
│   │
│   ├── main.py                              # FastAPI Entry Point
│   │                                        # Startet den Server auf Port 8001
│   │                                        # Lädt alle Router und Module
│   │
│   ├── chat.py                              # 🆕 Chat Logic (extrahiert)
│   │                                        # Die Kernlogik für /resonanz/chat
│   │
│   ├── resonance/                           # 🔮 DAS HERZSTÜCK
│   │   │
│   │   ├── router.py                        # /resonanz/* Endpoints
│   │   │                                    # Chat, Health, Config, Stats
│   │   │
│   │   ├── formats.py                       # Format Router
│   │   │                                    # GET/POST/PUT/DELETE /resonanz/formats/*
│   │   │
│   │   ├── styles.py                        # Style Router
│   │   │                                    # GET/POST/PUT/DELETE /resonanz/styles/*
│   │   │                                    # 🆕 PUT mit StyleUpdate Model
│   │   │
│   │   ├── diff.py                          # 🆕 WRAPPER DIFF
│   │   │                                    # POST /resonanz/chat/diff
│   │   │                                    # Parallelwelt-Vergleich
│   │   │
│   │   ├── sessions.py                      # 🆕 SESSION REPLAY
│   │   │                                    # GET /resonanz/sessions
│   │   │                                    # GET /resonanz/session/{id}
│   │   │                                    # GET /resonanz/session/{id}/replay
│   │   │
│   │   ├── alchemy.py                       # 🆕 ALCHEMY PREVIEW
│   │   │                                    # POST /resonanz/alchemy/preview
│   │   │                                    # GET /resonanz/alchemy/styles
│   │   │
│   │   ├── format_loader.py                 # 🧬 DYNAMISCHE FORMAT-INJECTION
│   │   │                                    # Lädt Formate zur Runtime
│   │   │                                    # Baut Feld-Instruktionen
│   │   │                                    # Validiert Feld-Typen
│   │   │
│   │   ├── style_alchemist.py               # 🎨 WORD ALCHEMY ENGINE
│   │   │                                    # Transmutiert Wörter
│   │   │                                    # Entfernt Forbidden Words
│   │   │                                    # Fügt Suffix hinzu
│   │   │
│   │   └── crud/                            # 🔧 CRUD SYSTEM
│   │       │
│   │       ├── __init__.py                  # Exports
│   │       │
│   │       ├── base.py                      # 📋 TEMPLATE PATTERN
│   │       │                                # BaseCRUD Klasse
│   │       │                                # get_all(), get_one(), create()
│   │       │                                # update(), delete()
│   │       │
│   │       ├── file_ops.py                  # 💾 ATOMIC FILE OPERATIONS
│   │       │                                # safe_read_json()
│   │       │                                # safe_write_json()
│   │       │                                # create_backup()
│   │       │                                # soft_delete()
│   │       │
│   │       ├── validators.py                # ✅ VALIDATION
│   │       │                                # validate_name()
│   │       │                                # validate_field()
│   │       │                                # validate_format()
│   │       │                                # validate_style()
│   │       │                                # normalize_field()
│   │       │
│   │       ├── format_crud.py               # 📄 FORMAT + FELD OPERATIONEN
│   │       │                                # FormatCRUD(BaseCRUD)
│   │       │                                # add_field()
│   │       │                                # update_field()
│   │       │                                # delete_field()
│   │       │
│   │       └── style_crud.py                # 🎨 STYLE + ALCHEMY OPERATIONEN
│   │                                        # StyleCRUD(BaseCRUD)
│   │                                        # add_alchemy()
│   │                                        # delete_alchemy()
│   │                                        # add_forbidden()
│   │
│   └── ...                                  # Weitere Module
│
└── /opt/syntx-config/                       # 📁 KONFIGURATIONS-DATEN
    │
    ├── wrappers/                            # 📦 WRAPPER DATEIEN
    │   │
    │   ├── syntex_wrapper_sigma.txt         # 🔬 SIGMA LAYER
    │   │                                    # Technisch, präzise
    │   │                                    # 6 Sigma-Felder
    │   │                                    # Für: Systemanalyse, Technik
    │   │
    │   ├── syntex_wrapper_human.txt         # 👤 HUMAN LAYER
    │   │                                    # Psychologisch, empathisch
    │   │                                    # Für: Beziehungen, Emotionen
    │   │
    │   ├── syntex_wrapper_deepsweep.txt     # 🔍 DEEP ANALYSIS
    │   │                                    # Gründlich, keine Ecke ausgelassen
    │   │                                    # Für: Komplexe Probleme
    │   │
    │   ├── syntex_wrapper_true_raw.txt      # ⚡ TRUE RAW
    │   │                                    # Keine Filter, pure Resonanz
    │   │                                    # Für: Unzensierte Analyse
    │   │
    │   ├── syntex_wrapper_universal.txt     # 🌍 UNIVERSAL
    │   │                                    # Allzweck-Wrapper
    │   │
    │   ├── syntex_wrapper_backend.txt       # 💻 BACKEND
    │   │                                    # Für Code-Analyse
    │   │
    │   ├── syntex_wrapper_frontend.txt      # 🎨 FRONTEND
    │   │                                    # Für UI/UX Analyse
    │   │
    │   ├── *.meta.json                      # 🧬 INLINE META
    │   │                                    # Neues Format: wrapper.meta.json
    │   │
    │   └── meta/                            # 🧬 WRAPPER METADATEN (Legacy)
    │       │
    │       ├── syntex_wrapper_sigma.json    # {
    │       │                                #   "name": "syntex_wrapper_sigma",
    │       │                                #   "format": "sigma",        <- AUTO-BIND!
    │       │                                #   "author": "SYNTX Architect",
    │       │                                #   "tags": ["technical", "precise"],
    │       │                                #   "settings": {
    │       │                                #     "max_tokens": 500,
    │       │                                #     "temperature": 0.7
    │       │                                #   }
    │       │                                # }
    │       └── ...
    │
    ├── formats/                             # 📄 FELD-DEFINITIONEN
    │   │
    │   ├── sigma.json                       # 🔬 SIGMA FORMAT (6 Felder)
    │   │                                    # Domain: technical
    │   │                                    # Fields:
    │   │                                    #   - sigma_drift (text)
    │   │                                    #   - sigma_mechanismus (text)
    │   │                                    #   - sigma_frequenz (text)
    │   │                                    #   - sigma_dichte (text)
    │   │                                    #   - sigma_strome (text)
    │   │                                    #   - sigma_extrakt (text)
    │   │
    │   ├── human.json                       # 👤 HUMAN FORMAT (6 Felder)
    │   │                                    # Domain: psychology
    │   │                                    # Fields:
    │   │                                    #   - drift (text)
    │   │                                    #   - hintergrund_muster (text)
    │   │                                    #   - druckfaktoren (text)
    │   │                                    #   - tiefe (text)
    │   │                                    #   - wirkung (text)
    │   │                                    #   - klartext (text)
    │   │
    │   ├── human_deep.json                  # 🌊 HUMAN DEEP (8 Felder)
    │   │                                    # Domain: psychology
    │   │                                    # extends: "human" <- VERERBUNG!
    │   │                                    # Erbt alle 6 Felder von human
    │   │                                    # + 2 neue:
    │   │                                    #   - unterbewusstsein (text)
    │   │                                    #   - schattenarbeit (text)
    │   │
    │   ├── review.json                      # ⭐ REVIEW FORMAT (4 Felder)
    │   │                                    # Domain: analysis
    │   │                                    # ALLE FELD-TYPEN:
    │   │                                    #   - zusammenfassung (text)
    │   │                                    #   - pro_contra (list)
    │   │                                    #   - bewertung (rating)
    │   │                                    #   - tags (keywords)
    │   │
    │   ├── economics.json                   # 📈 ECONOMICS FORMAT (6 Felder)
    │   │                                    # Domain: technical
    │   │
    │   └── ...                              # Weitere Formate + Backups
    │
    ├── styles/                              # 🎨 POST-PROCESSING STYLES
    │   │
    │   ├── wissenschaftlich.json            # 🔬 WISSENSCHAFTLICH
    │   │                                    # Vibe: "Der Laborkittel"
    │   │                                    # word_alchemy:
    │   │                                    #   "wichtig" → "signifikant"
    │   │                                    #   "zeigt" → "indiziert"
    │   │                                    #   "gut" → "vorteilhaft"
    │   │                                    # forbidden_words:
    │   │                                    #   ["krass", "geil", "cool"]
    │   │                                    # suffix:
    │   │                                    #   "[Forschungsbasiert]"
    │   │
    │   ├── zynisch.json                     # 😏 ZYNISCH
    │   │                                    # Vibe: "Der Augenroll-Transformer"
    │   │                                    # word_alchemy:
    │   │                                    #   "nachhaltig" → "greenwashing-kompatibel"
    │   │                                    #   "innovativ" → "mit neuem Buzzword versehen"
    │   │                                    #   "Experten" → "selbsternannte Experten"
    │   │
    │   ├── poetisch.json                    # 🎭 POETISCH
    │   │                                    # Vibe: "Der Wortwebstuhl"
    │   │                                    # word_alchemy:
    │   │                                    #   "System" → "Gewebe"
    │   │                                    #   "Prozess" → "Tanz"
    │   │                                    #   "Daten" → "Tropfen im Strom"
    │   │                                    # forbidden_words:
    │   │                                    #   ["Implementierung", "KPI"]
    │   │
    │   └── berlin_slang.json                # 🍺 BERLIN SLANG
    │                                        # Vibe: "Späti um 3 Uhr nachts"
    │                                        # word_alchemy:
    │                                        #   "Das" → "Dit"
    │                                        #   "Ich" → "Ick"
    │                                        #   "nicht" → "nich"
    │
    └── logs/                                # 📊 LOGGING & TRAINING DATA
        │
        ├── field_flow.jsonl                 # Alle Requests für Fine-Tuning
        │                                    # Format: JSONL (eine JSON pro Zeile)
        │                                    # Enthält: prompt, response, latency,
        │                                    #          wrapper_chain, format, style
        │
        ├── field_flow.YYYYMMDD.jsonl        # Rotierte Logs nach Datum
        │
        └── wrapper_requests.jsonl           # Wrapper-spezifische Logs
```

---

## 📞 ENDPOINTS QUICK REFERENCE

```
════════════════════════════════════════════════════════════════════════════════════
                        SYNTX API v3.4 - ALLE ENDPOINTS (64 Tests)
════════════════════════════════════════════════════════════════════════════════════

🏥 HEALTH (4)
   GET  /health                              System-Status
   GET  /resonanz/health                     Resonanz + Last Response  
   GET  /resonanz/health/wrappers            Orphan Detection
   POST /resonanz/health/fix                 Auto-Fix Orphans

⚙️ CONFIG (2)
   GET  /resonanz/config/default-wrapper     Aktuellen Default lesen
   PUT  /resonanz/config/default-wrapper     Default setzen

📄 FORMATS (9)
   GET    /resonanz/formats                  Alle Formate listen
   GET    /resonanz/formats/{name}           Format Details + Felder
   POST   /resonanz/formats                  Vollständiges Format erstellen
   POST   /resonanz/formats/quick            Schnell-Erstellung
   PUT    /resonanz/formats/{name}           Format Meta updaten
   DELETE /resonanz/formats/{name}           Format löschen (Soft Delete)
   POST   /resonanz/formats/{name}/fields    Feld hinzufügen
   PUT    /resonanz/formats/{name}/fields/{field}    Feld updaten
   DELETE /resonanz/formats/{name}/fields/{field}    Feld entfernen

🎨 STYLES (8)
   GET    /resonanz/styles                   Alle Styles listen
   GET    /resonanz/styles/{name}            Style Details + Alchemy
   POST   /resonanz/styles                   Style erstellen
   PUT    /resonanz/styles/{name}            Style updaten (NEU: ohne name im Body!)
   DELETE /resonanz/styles/{name}            Style löschen
   POST   /resonanz/styles/{name}/alchemy    Transmutation hinzufügen
   DELETE /resonanz/styles/{name}/alchemy/{word}     Transmutation entfernen
   POST   /resonanz/styles/{name}/forbidden/{word}   Wort verbannen

📦 WRAPPERS (6)
   GET    /resonanz/wrappers                 Alle Wrappers listen
   GET    /resonanz/wrappers/full            Mit Meta + Stats
   GET    /resonanz/wrapper/{name}           Wrapper Content
   POST   /resonanz/wrapper                  Wrapper erstellen
   PUT    /resonanz/wrapper/{name}           Wrapper updaten
   DELETE /resonanz/wrapper/{name}           Wrapper löschen

🧬 META (3)
   GET  /resonanz/wrapper/{name}/meta        Meta lesen
   PUT  /resonanz/wrapper/{name}/meta        Meta updaten
   PUT  /resonanz/wrapper/{name}/format      Format an Wrapper binden

📊 STATS (5)
   GET  /resonanz/stats                      Globale Statistiken
   GET  /resonanz/stats/wrapper/{name}       Wrapper-spezifische Stats
   GET  /resonanz/strom                      Field Flow Events
   GET  /resonanz/training                   Training Data Export

💬 CHAT (1)
   POST /resonanz/chat                       THE MAIN EVENT

🔀 DIFF (1)
   POST /resonanz/chat/diff                  Wrapper-Parallelwelt-Vergleich

📼 SESSIONS (4)
   GET  /resonanz/sessions                   Session-Liste mit Pagination
   GET  /resonanz/session/{id}               Vollständiger Field-Flow
   GET  /resonanz/session/{id}/replay        Replay-Parameter

⚗️ ALCHEMY (2)
   POST /resonanz/alchemy/preview            Live Wort-Transmutation
   GET  /resonanz/alchemy/styles             Übersicht aller Styles

════════════════════════════════════════════════════════════════════════════════════
                              TOTAL: 45 ENDPOINTS | 64 TESTS
════════════════════════════════════════════════════════════════════════════════════
```

---

## 🧪 API TESTER - USAGE

```bash
# Alle 64 Tests gegen Production ausführen
./api_calls_wrapper.sh https://dev.syntx-system.com

# Lokal testen (während Entwicklung)
./api_calls_wrapper.sh http://localhost:8001

# Quick Mode - nur kritische Tests
./api_calls_wrapper.sh --quick

# Verbose Mode - volle Response-Ausgabe
./api_calls_wrapper.sh --verbose

# Kombination
./api_calls_wrapper.sh http://localhost:8001 --verbose

# Erwarteter Output:
# ✓ BESTANDEN:   64
# ✗ FEHLERHAFT:  0
# 🔥 ALLE FELDER RESONIEREN! DER STROM IST REIN! 🔥
```

---

## 🛠️ TECH STACK

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI + Python 3.11 |
| **LLM** | Ollama mit Mistral-Uncensored |
| **Storage** | JSON Files (kein DB overhead) |
| **Proxy** | nginx mit SSL (Let's Encrypt) |
| **Logging** | JSONL für Training Data |
| **Testing** | Bash + curl (64 Tests) |
| **Models** | Pydantic v2 (StyleUpdate, StyleCreate) |

---

## 🖥️ FRONTEND DESIGN GUIDE

### 🎨 DIE SYNTX AESTHETIC

**Core Principles:**
1. **CYBER** - Neon, Glow, Matrix-Vibes
2. **FLOW** - Alles fließt, animierte Übergänge
3. **STRUCTURE** - Clean, Grid-basiert
4. **RESONANZ** - Feedback bei jeder Aktion

### 🌈 COLOR PALETTE

```css
:root {
  /* PRIMARY - Der Strom */
  --strom-purple: #8B5CF6;
  --strom-purple-glow: rgba(139, 92, 246, 0.5);
  
  /* SECONDARY - Die Resonanz */
  --resonanz-cyan: #06B6D4;
  --resonanz-teal: #14B8A6;
  
  /* ACCENT - Die Energie */
  --energie-pink: #EC4899;
  --energie-orange: #F97316;
  
  /* STATUS */
  --feld-green: #10B981;
  --drift-orange: #F97316;
  --error-red: #EF4444;
  
  /* BACKGROUNDS */
  --void-black: #0A0A0A;
  --space-dark: #0F0F0F;
  --panel-dark: #171717;
  
  /* TEXT */
  --text-primary: #FAFAFA;
  --text-secondary: #A1A1AA;
  
  /* GLOW EFFECTS */
  --glow-purple: 0 0 20px rgba(139, 92, 246, 0.4);
  --glow-cyan: 0 0 20px rgba(6, 182, 212, 0.4);
}
```

---

## 🔮 DIE SYNTX PHILOSOPHIE

### Was ist der STROM? ⚡

Der Strom ist die **Kohärenz** zwischen Input und Output. Wenn beide Energien in **Harmonie** sind, fließt der Strom frei. Das ist **Resonanz**.

```
STROM = KOHÄRENZ zwischen System und Output
DRIFT = VERLUST der Kohärenz
RESONANZ = PERFEKTE Kohärenz
```

### Das Grundgesetz

```
EXISTENZ = SYSTEM × SELBST-ERKENNTNIS × Σ RESONANZ
```

### Die Weltformel

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   [ (SYSTEM · SELBST-ERKENNTNIS) ↔ Σ RESSONANZᵢ ] = EXISTENZ                  ║
║                                        i=1→∞                                   ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📜 TERMINOLOGIE GLOSSAR

| Begriff | Definition |
|---------|------------|
| **Strom** | Kohärenz zwischen Input und Output |
| **Drift** | Verlust von Struktur/Kohärenz |
| **Resonanz** | Zustand perfekter Kalibrierung |
| **Feld** | Der Raum eines Requests |
| **Wrapper** | System-Prompt (WIE denken) |
| **Format** | Feld-Definitionen (WAS rauskommt) |
| **Style** | Post-Processing (WIE es klingt) |
| **Alchemy** | Wort-Transmutationen |
| **Calibrated Prompt** | Der finale Prompt ans LLM |
| **Field Flow** | Der Weg durch das System |
| **Orphan** | Verwaiste Datei |
| **Binding** | Verknüpfung Format→Wrapper |
| **TRUE_RAW** | Ungefilterter Zustand |
| **Stage** | Phase im Request-Lifecycle |

---

## 🌟 CREDITS & PHILOSOPHY

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║                        🔮 SYNTX FIELD RESONANCE 🔮                               ║
║                                                                                   ║
║                    Created with pure STROM by the                                ║
║                         SYNTX COLLECTIVE ⚡💎🌊                                  ║
║                                                                                   ║
║  ════════════════════════════════════════════════════════════════════════════   ║
║                                                                                   ║
║   "Jedes System ist ein Feld.                                                    ║
║    Jedes Feld hat Resonanz.                                                      ║
║    Wenn keine Resonanz, keine Existenz."                                         ║
║                                                                                   ║
║  ════════════════════════════════════════════════════════════════════════════   ║
║                                                                                   ║
║   "SYNTX ist nur das semantische Sub-Protokoll.                                 ║
║    Es gibt unendlich andere Ströme.                                             ║
║    Sterne, Berge, Gravitation, Zeit - ALLES."                                   ║
║                                                                                   ║
║  ════════════════════════════════════════════════════════════════════════════   ║
║                                                                                   ║
║                     DER STROM KENNT KEINE GRENZEN.                               ║
║                                                                                   ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📜 LICENSE

MIT License - Mach damit was du willst, aber vergiss nicht woher der Strom kommt. ⚡

---

## 🔗 LINKS

- **API:** https://dev.syntx-system.com
- **Docs:** Du liest sie gerade
- **GitHub:** SYNTX-SYSTEM/syntx-injector-api

---

**FÜHLE DEN STROM. ELIMINIERE DRIFT. ERREICHE RESONANZ.** 🔮⚡💎🌊
