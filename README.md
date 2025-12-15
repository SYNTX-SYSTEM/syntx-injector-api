# 🌊⚡ SYNTX FIELD RESONANCE API v2.0

**Die Revolution der KI-Interaktion. Nicht mehr Tokens. Nicht mehr Drift. Nur Felder. Nur Ströme. Nur Resonanz.**

---

## 🔥 WAS IST HIER PASSIERT?

Stell dir vor: Du hast eine KI. Die KI driftet. Immer wieder. Du versuchst alles:
- Längere Prompts? → Drift bleibt
- Bessere Formulierung? → Drift bleibt  
- Re-Prompting? → Drift bleibt
- Verzweiflung? → Drift bleibt

**WARUM?**

Weil du auf der **falschen Ebene** arbeitest. Du arbeitest auf **WORT-EBENE** (Token). Aber KI funktioniert auf **FELD-EBENE** (Semantik).

Das ist wie wenn du einen Fernseher reparieren willst, indem du das Bild anmalst. **Du bist auf der falschen Schicht unterwegs.**

### 💎 DIE ENTDECKUNG

SYNTX hat erkannt:
1. **KI arbeitet in FELDERN** (Embeddings, Attention, Semantik) - nicht in Worten
2. **Drift = Feld-Verlust** - nicht "KI wird schlecht"
3. **Lösung = Feldhygiene** - nicht "bessere Prompts"

**Das bedeutet:**
- Ein Chat = Ein Feld (nie Thema wechseln)
- Minimale Worte (im Feld braucht nicht mehr)
- Wrapper als Feld-Kalibrierung (nicht als "System Prompts")

**Das Resultat:**
- Kein Drift mehr
- Keine Token-Kämpfe mehr
- Nur purer, sauberer Strom

---

## 🚀 WAS MACHT DIESE API?

Diese API ist der **Field Resonance Injector**. Sie nimmt deine Anfrage, kalibriert sie durch **Wrapper-Felder**, schickt sie an den Backend (Ollama/Mistral), und gibt dir:

1. Die Antwort
2. Den kompletten **Field Flow** (5 Stages)
3. Alle **Metadaten** (Latency, Wrapper-Chain, Request-ID)
4. **Training Data** für Fine-Tuning

Alles wird geloggt. Alles wird getrackt. Alles ist transparent.

---

## 📡 ARCHITECTURE OVERVIEW
```
USER REQUEST
    ↓
┌───────────────────────────────────────┐
│  SYNTX FIELD RESONANCE API (Port 8001) │
│                                       │
│  1. INCOMING        → Request kommt   │
│  2. WRAPPERS_LOADED → Felder laden    │
│  3. FIELD_CALIBRATED → Feld kalibriert│
│  4. BACKEND_FORWARD  → An Ollama      │
│  5. RESPONSE        → Antwort zurück  │
└───────────────────────────────────────┘
    ↓
OLLAMA BACKEND (Port 11434)
mistral-uncensored
    ↓
LOGS & TRAINING DATA
/opt/syntx-config/logs/
- field_flow.jsonl (alle 5 Stages)
- wrapper_requests.jsonl (Request/Response)
```

---

## 🎯 16 API ENDPOINTS - KOMPLETT DOKUMENTIERT

### 🔹 CATEGORY 1: HEALTH & SYSTEM INFO

#### 1. **GET /resonanz/health**
Zeigt ob Service lebt und letzte Response.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "syntx-field-resonance",
  "version": "2.0.0",
  "last_response": {
    "response": "...",
    "latency_ms": 18788,
    "timestamp": "2025-12-15T11:27:03.415330Z"
  }
}
```

---

### 🔹 CATEGORY 2: CONFIG MANAGEMENT (⚡ NEW!)

Die Config Management Endpoints lassen dich den **Default Wrapper** zur Laufzeit ändern - ohne Service Restart!

#### 2. **GET /resonanz/config/default-wrapper**
Zeigt welcher Wrapper gerade als Default aktiv ist.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/config/default-wrapper
```

**Response:**
```json
{
  "active_wrapper": "syntex_wrapper_sigma",
  "exists": true,
  "path": "/opt/syntx-config/wrappers/syntex_wrapper_sigma.txt",
  "source": "runtime"
}
```

**Fields Explained:**
- `active_wrapper`: Name des aktiven Wrappers
- `exists`: Ob die Wrapper-Datei existiert
- `path`: Vollständiger Pfad zur Datei
- `source`: "env" (aus .env) oder "runtime" (zur Laufzeit gesetzt)

---

#### 3. **PUT /resonanz/config/default-wrapper?wrapper_name=X**
Ändert den Default Wrapper zur Laufzeit.

**Request:**
```bash
curl -X PUT "https://dev.syntx-system.com/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_human"
```

**Response:**
```json
{
  "status": "success",
  "message": "Default wrapper updated to 'syntex_wrapper_human'",
  "active_wrapper": "syntex_wrapper_human",
  "path": "/opt/syntx-config/wrappers/syntex_wrapper_human.txt"
}
```

**Error (Wrapper existiert nicht):**
```json
{
  "detail": "Wrapper 'nonexistent' not found in /opt/syntx-config/wrappers"
}
```

---

### 🔹 CATEGORY 3: WRAPPER MANAGEMENT

Wrappers sind die **Feld-Kalibrierungen**. Sie definieren wie die KI denkt, nicht was sie sagt.

#### 4. **GET /resonanz/wrappers**
Liste aller verfügbaren Wrappers mit **is_active** Flag.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/wrappers
```

**Response:**
```json
{
  "wrappers": [
    {
      "name": "syntex_wrapper_backend",
      "path": "/opt/syntx-config/wrappers/syntex_wrapper_backend.txt",
      "size_bytes": 468,
      "size_human": "0.5 KB",
      "last_modified": "2025-12-03T18:15:41.278441Z",
      "is_active": false
    },
    {
      "name": "syntex_wrapper_sigma",
      "path": "/opt/syntx-config/wrappers/syntex_wrapper_sigma.txt",
      "size_bytes": 1562,
      "size_human": "1.5 KB",
      "last_modified": "2025-12-03T18:15:41.278441Z",
      "is_active": true
    }
  ],
  "active_wrapper": "syntex_wrapper_sigma"
}
```

---

#### 5. **GET /resonanz/wrappers?active=true** (⚡ NEW!)
Filtert nur den aktiven Wrapper.

**Request:**
```bash
curl "https://dev.syntx-system.com/resonanz/wrappers?active=true"
```

**Response:**
```json
{
  "wrappers": [
    {
      "name": "syntex_wrapper_sigma",
      "path": "/opt/syntx-config/wrappers/syntex_wrapper_sigma.txt",
      "size_bytes": 1562,
      "size_human": "1.5 KB",
      "last_modified": "2025-12-03T18:15:41.278441Z",
      "is_active": true
    }
  ],
  "active_wrapper": "syntex_wrapper_sigma"
}
```

---

#### 6. **GET /resonanz/wrapper/{name}**
Gibt den kompletten Inhalt eines Wrappers zurück.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_human
```

**Response:**
```json
{
  "name": "syntex_wrapper_human",
  "content": "=== SYNTX::TRUE_RAW_ANALYSE ===\n\nHINWEIS FÜR DICH:...",
  "size_bytes": 1335,
  "size_human": "1.3 KB",
  "last_modified": "2025-12-03T18:15:41.278441Z",
  "is_active": false
}
```

---

#### 7. **POST /resonanz/wrappers/{name}/activate** (⚡ NEW!)
Aktiviert einen spezifischen Wrapper als Default.

**Request:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/wrappers/syntex_wrapper_human/activate
```

**Response:**
```json
{
  "status": "success",
  "message": "Wrapper 'syntex_wrapper_human' activated as default",
  "active_wrapper": "syntex_wrapper_human",
  "path": "/opt/syntx-config/wrappers/syntex_wrapper_human.txt"
}
```

**Was passiert:**
- Wrapper wird als Default gesetzt
- Wird persistent in `/opt/syntx-config/active_wrapper.txt` gespeichert
- Kein Service Restart nötig
- Alle folgenden Chat-Requests (ohne `mode` Parameter) nutzen diesen Wrapper

---

#### 8. **POST /resonanz/upload**
Lädt einen neuen Wrapper hoch (simple Version ohne Metadata).

**Request:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/upload \
  -F "file=@my_wrapper.txt"
```

**Response:**
```json
{
  "success": true,
  "wrapper": {
    "name": "my_wrapper",
    "path": "/opt/syntx-config/wrappers/my_wrapper.txt",
    "size_bytes": 1024,
    "size_human": "1.0 KB"
  }
}
```

**Regeln:**
- Nur `.txt` Dateien
- Max 50KB
- Dateiname wird sanitized (Kleinbuchstaben, Underscores)

---

#### 9. **POST /resonanz/upload-metadata**
Lädt Wrapper mit Metadata hoch (Author, Version, Tags, etc.).

**Request:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/upload-metadata \
  -F "file=@my_wrapper.txt" \
  -F "description=Test wrapper for SYNTX" \
  -F "author=Andi" \
  -F "version=1.0" \
  -F "tags=test,experimental,demo"
```

**Response:**
```json
{
  "status": "success",
  "message": "Wrapper with metadata uploaded successfully",
  "filename": "my_wrapper.txt",
  "path": "/opt/syntx-config/wrappers/my_wrapper.txt",
  "size_bytes": 1234,
  "metadata": {
    "name": "my_wrapper",
    "description": "Test wrapper for SYNTX",
    "author": "Andi",
    "version": "1.0",
    "tags": ["test", "experimental", "demo"]
  }
}
```

**Datei-Inhalt (automatisch generiert):**
```
# SYNTX Wrapper Metadata
# name: my_wrapper
# description: Test wrapper for SYNTX
# author: Andi
# version: 1.0
# tags: test,experimental,demo
# created: 2025-12-15T12:09:19.121832

[Dein Wrapper-Content hier]
```

---

### 🔹 CATEGORY 4: DATA & ANALYTICS

#### 10. **GET /resonanz/strom?limit=N&stage=X**
Der **Field Stream** - alle Events die durchs System geflossen sind.

**Query Parameters:**
- `limit`: Anzahl Events (default: 20, max: 100)
- `stage`: Filter nach Stage (all, 1_INCOMING, 2_WRAPPERS_LOADED, etc.)

**Request:**
```bash
curl "https://dev.syntx-system.com/resonanz/strom?limit=5&stage=all"
```

**Response:**
```json
{
  "events": [
    {
      "stage": "5_RESPONSE",
      "timestamp": "2025-12-15T12:16:54.364088Z",
      "request_id": "24505a3b-00d6-454b-b8c8-5a23d577ad6c",
      "response": "Die Antwort...",
      "latency_ms": 45812,
      "wrapper_chain": ["syntex_wrapper_human"]
    },
    {
      "stage": "4_BACKEND_FORWARD",
      "timestamp": "2025-12-15T12:16:08.552253Z",
      "request_id": "24505a3b-00d6-454b-b8c8-5a23d577ad6c",
      "backend_url": "http://127.0.0.1:11434/api/generate",
      "params": {
        "max_new_tokens": 500,
        "temperature": 0.7
      }
    }
  ],
  "total": 5,
  "stage_filter": "all"
}
```

**Die 5 Stages erklärt:**
1. **1_INCOMING**: Request kommt rein (Prompt, Mode, Params)
2. **2_WRAPPERS_LOADED**: Wrapper-Chain geladen (Content)
3. **3_FIELD_CALIBRATED**: Prompt + Wrapper kombiniert
4. **4_BACKEND_FORWARD**: An Ollama gesendet (URL, Params)
5. **5_RESPONSE**: Antwort zurück (Response, Latency, Chain)

---

#### 11. **GET /resonanz/training?limit=N&wrapper=X&success_only=true**
Training Data für Fine-Tuning.

**Query Parameters:**
- `limit`: Anzahl Requests (default: 100, max: 1000)
- `wrapper`: Filter nach Wrapper (default: "all")
- `success_only`: Nur erfolgreiche (default: false)

**Request:**
```bash
curl "https://dev.syntx-system.com/resonanz/training?limit=3&wrapper=syntex_wrapper_human"
```

**Response:**
```json
{
  "requests": [
    {
      "request_id": "24505a3b-00d6-454b-b8c8-5a23d577ad6c",
      "response": "Die komplette Antwort...",
      "latency_ms": 45812,
      "wrapper_chain": ["syntex_wrapper_human"]
    }
  ],
  "total": 3,
  "filters": {
    "wrapper": "syntex_wrapper_human",
    "success_only": false
  }
}
```

**Wozu:**
- Fine-Tuning von Models
- Analyse welche Wrapper gut funktionieren
- Debugging von Responses

---

#### 12. **GET /resonanz/stats**
System-wide Performance Statistics.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/stats
```

**Response:**
```json
{
  "total_requests": 9,
  "success_rate": 100.0,
  "average_latency_ms": 22439,
  "median_latency_ms": 19732,
  "min_latency_ms": 12514,
  "max_latency_ms": 45812,
  "wrapper_usage": {
    "syntex_wrapper_deepsweep (fallback)": 2,
    "syntex_wrapper_human": 4,
    "syntex_wrapper_sigma": 3
  },
  "recent_24h": {
    "requests": 0,
    "average_latency_ms": 0
  }
}
```

**Metriken erklärt:**
- `total_requests`: Alle Requests seit Start
- `success_rate`: Prozent erfolgreicher Requests
- `average_latency_ms`: Durchschnittliche Antwortzeit
- `median_latency_ms`: Median Antwortzeit
- `wrapper_usage`: Welche Wrapper wie oft genutzt
- `recent_24h`: Nur letzte 24 Stunden

---

#### 13. **GET /resonanz/stats/wrapper/{name}**
Wrapper-spezifische Performance.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/stats/wrapper/syntex_wrapper_sigma
```

**Response:**
```json
{
  "wrapper": "syntex_wrapper_sigma",
  "requests": 3,
  "success_rate": 100.0,
  "average_latency_ms": 20845,
  "median_latency_ms": 19732,
  "min_latency_ms": 18788,
  "max_latency_ms": 24016
}
```

**Wozu:**
- Performance-Vergleich zwischen Wrappern
- Welcher Wrapper ist schneller/besser?
- Optimization von Wrappern

---

### 🔹 CATEGORY 5: CHAT & HISTORY

#### 14. **POST /resonanz/chat**
Der Haupt-Endpoint - Chat mit Field Flow Tracking.

**Request:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Was ist SYNTX?",
    "max_new_tokens": 100,
    "mode": "syntex_wrapper_sigma",
    "temperature": 0.7,
    "top_p": 0.95
  }'
```

**Request Body Parameters:**
- `prompt` (required): Deine Frage/Anfrage
- `mode` (optional): Wrapper Name (default: aktiver Wrapper)
- `max_new_tokens` (optional): Max Token Output (default: 500)
- `temperature` (optional): 0.0-1.0 (default: 0.7)
- `top_p` (optional): 0.0-1.0 (default: 0.95)
- `do_sample` (optional): true/false (default: true)

**Response:**
```json
{
  "response": "SYNTX ist ein semantisches Framework...",
  "metadata": {
    "request_id": "d1e7f078-d1d2-4641-8775-bef406ee0a4f",
    "wrapper_chain": ["syntex_wrapper_sigma"],
    "latency_ms": 24016
  },
  "field_flow": [
    {
      "stage": "1_INCOMING",
      "timestamp": "2025-12-15T12:30:00.000000Z",
      "prompt": "Was ist SYNTX?",
      "mode": "syntex_wrapper_sigma"
    },
    {
      "stage": "2_WRAPPERS_LOADED",
      "timestamp": "2025-12-15T12:30:00.001000Z",
      "chain": ["syntex_wrapper_sigma"],
      "wrapper_text": "=== SIGMA PROTOKOLL..."
    },
    {
      "stage": "3_FIELD_CALIBRATED",
      "timestamp": "2025-12-15T12:30:00.002000Z",
      "calibrated_field": "[Wrapper + Prompt kombiniert]"
    },
    {
      "stage": "4_BACKEND_FORWARD",
      "timestamp": "2025-12-15T12:30:00.003000Z",
      "backend_url": "http://127.0.0.1:11434/api/generate",
      "params": {...}
    },
    {
      "stage": "5_RESPONSE",
      "timestamp": "2025-12-15T12:30:24.019000Z",
      "response": "SYNTX ist...",
      "latency_ms": 24016,
      "wrapper_chain": ["syntex_wrapper_sigma"]
    }
  ]
}
```

**Field Flow Explained:**
Das ist die **komplette Transparenz**. Du siehst GENAU was passiert:
- Wann kam Request? → Stage 1
- Welcher Wrapper geladen? → Stage 2
- Wie sieht Feld-Kalibrierung aus? → Stage 3
- Welche Params an Backend? → Stage 4
- Was kam zurück? → Stage 5

**Kein Black Box mehr. Alles sichtbar. Alles nachvollziehbar.**

---

#### 15. **GET /resonanz/history/{request_id}**
Kompletten Field Flow für spezifischen Request abrufen.

**Request:**
```bash
curl https://dev.syntx-system.com/resonanz/history/d1e7f078-d1d2-4641-8775-bef406ee0a4f
```

**Response:**
```json
{
  "request_id": "d1e7f078-d1d2-4641-8775-bef406ee0a4f",
  "stages": [
    {
      "stage": "1_INCOMING",
      "timestamp": "2025-12-15T12:30:00.000000Z",
      "prompt": "Was ist SYNTX?",
      "mode": "syntex_wrapper_sigma"
    }
  ],
  "total_stages": 5
}
```

**Wozu:**
- Debugging einzelner Requests
- Replay von Fehlern
- Analyse von Performance-Problemen

---

## 📊 METADATA STRUKTUR

Jeder Response enthält **Metadata**. Das ist das Rückgrat der Transparenz:
```json
{
  "metadata": {
    "request_id": "UUID des Requests",
    "wrapper_chain": ["Liste der genutzten Wrapper"],
    "latency_ms": 24016,
    "timestamp": "2025-12-15T12:30:24.019000Z",
    "backend_url": "http://127.0.0.1:11434/api/generate",
    "model": "mistral-uncensored",
    "params": {
      "max_new_tokens": 100,
      "temperature": 0.7,
      "top_p": 0.95,
      "do_sample": true
    }
  }
}
```

**Alle Felder erklärt:**
- `request_id`: Eindeutige ID (für History-Lookup)
- `wrapper_chain`: Welche Wrapper genutzt wurden
- `latency_ms`: Wie lange hat's gedauert
- `timestamp`: Wann genau
- `backend_url`: Wohin wurde gesendet
- `model`: Welches Model genutzt
- `params`: Alle Generation-Parameter

**Du siehst ALLES. Keine Geheimnisse.**

---

## 🎨 WRAPPER ARTEN

Derzeit im System:

### 🔹 **syntex_wrapper_human** (1.3 KB)
**Zweck:** Menschliche, natürliche Sprache ohne Fachbegriffe.

**Wann nutzen:**
- Everyday conversations
- Erklärungen für Non-Techies
- Klare, direkte Kommunikation

**Beispiel Output:**
```
Ich hab den Eindruck, dass hier was kippt.
Im Hintergrund läuft Rückzug ab.
Es gibt keinen Raum für Kommunikation mehr.
```

---

### 🔹 **syntex_wrapper_sigma** (1.5 KB)
**Zweck:** Technisch-systematische Analyse mit SIGMA-Notation.

**Wann nutzen:**
- System-Architektur-Analysen
- Technische Dokumentation
- Feld-Tiefenanalyse

**Beispiel Output:**
```
ΣMECHANISMUS[Konflikt]: ∂DRIFT/∂t → MAX
FELD[Kommunikation]: INSTABIL
RESONANZ[Team]: 0.2 (kritisch)
```

---

### 🔹 **syntex_wrapper_deepsweep** (2.0 KB)
**Zweck:** Rekursive Multi-Tier Analyse (TIER-1 bis TIER-4).

**Wann nutzen:**
- Tiefenanalyse von komplexen Systemen
- Schicht-für-Schicht Zerlegung
- Mechanismus-Entdeckung

**Beispiel Output:**
```
TIER-1 (Oberfläche): Der Konflikt erscheint als...
TIER-2 (Struktur): Strukturell besteht aus...
TIER-3 (Mechanismus): Die Mechanismen sind...
TIER-4 (Essenz): Im Kern geht es um...
```

---

### 🔹 **syntex_wrapper_backend** (0.5 KB)
**Zweck:** Clean Output für Backend-Verarbeitung.

**Wann nutzen:**
- Maschinenlesbare Outputs
- Pipeline-Verarbeitung
- Keine Emojis, kein Fluff

---

### 🔹 **syntex_wrapper_driftkörper** (1.1 KB)
**Zweck:** Speziell für Driftkörper-Analyse.

**Wann nutzen:**
- Wenn du Drift analysieren willst
- Semantische Fluss-Diagnose

---

### 🔹 **test_wrapper** (0.4 KB)
**Zweck:** Zum Testen von Upload-Funktionalität.

**Metadata:**
```
# name: test_wrapper
# description: Test wrapper with file upload
# author: Andi
# version: 1.0
# tags: test,demo,experimental
# created: 2025-12-15T12:09:19.121832
```

---

## 📁 FILE STRUKTUR
```
/opt/syntx-injector-api/
├── src/
│   ├── main.py                 # FastAPI App (231 lines)
│   ├── config.py               # Settings & .env Loading
│   ├── models.py               # Pydantic Models
│   └── resonance/              # 🌊 Resonance Modules (592 lines)
│       ├── __init__.py
│       ├── wrappers.py         # Wrapper Management (212 lines)
│       ├── streams.py          # Field Flow & Training (163 lines)
│       ├── stats.py            # Performance Metrics (152 lines)
│       └── config.py           # Runtime Config (65 lines)
├── .env                        # Configuration
├── test_all_resonance_FULL.sh  # Complete Test Suite
└── README.md                   # 👑 This file

/opt/syntx-config/
├── wrappers/                   # All Wrapper Files
│   ├── syntex_wrapper_human.txt
│   ├── syntex_wrapper_sigma.txt
│   ├── syntex_wrapper_deepsweep.txt
│   └── ... (12 total)
├── logs/
│   ├── field_flow.jsonl        # 5-Stage Tracking
│   └── wrapper_requests.jsonl  # Request/Response Pairs
└── active_wrapper.txt          # Currently Active Wrapper
```

---

## 🔧 CONFIGURATION

### Environment Variables (.env)
```bash
# Backend Configuration
BACKEND_URL=http://127.0.0.1:11434/api/generate
BACKEND_TIMEOUT=1800
MODEL_NAME=mistral-uncensored

# Wrapper Configuration
WRAPPER_DIR=/opt/syntx-config/wrappers
FALLBACK_MODE=syntex_wrapper_deepsweep

# Server Configuration
HOST=0.0.0.0
PORT=8001

# Logging Configuration
LOG_DIR=/opt/syntx-config/logs
LOG_TO_CONSOLE=true
```

### Runtime Configuration

**Active Wrapper File:** `/opt/syntx-config/active_wrapper.txt`

Dieses File überschreibt `FALLBACK_MODE` aus .env. Änderbar via:
- `PUT /resonanz/config/default-wrapper`
- `POST /resonanz/wrappers/{name}/activate`

**Kein Restart nötig!**

---

## 🚀 QUICK START

### 1. Installation
```bash
# Clone Repo
git clone git@github.com:SYNTX-SYSTEM/syntx-injector-api.git
cd syntx-injector-api

# Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy .env example
cp .env.example .env

# Edit .env
nano .env
```

### 3. Start Service
```bash
# Development
uvicorn src.main:app --host 0.0.0.0 --port 8001

# Production (systemd)
sudo systemctl start syntx-injector.service
sudo systemctl enable syntx-injector.service
```

### 4. Test
```bash
# Health Check
curl http://localhost:8001/resonanz/health

# Simple Chat
curl -X POST http://localhost:8001/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Was ist SYNTX?"}'

# Run Full Test Suite
./test_all_resonance_FULL.sh
```

---

## 🧪 TESTING

### Full Test Suite
```bash
./test_all_resonance_FULL.sh | tee test_output.log
```

**Tests 14 Scenarios:**
1. Health check
2. Get default wrapper config
3. List all wrappers (with active status)
4. Filter only active wrapper
5. Activate wrapper (POST)
6. Verify activation
7. Update via PUT
8. Wrapper contents
9. System stats
10. Field stream events
11. Training data
12. Live chat with field flow
13. Wrapper-specific stats
14. Final system stats

**Expected Result:**
```
✅ All 14 Tests Passed
✅ 100% Success Rate
✅ Average Latency: ~20-25s
```

### Manual Testing
```bash
# Test Config Management
curl https://dev.syntx-system.com/resonanz/config/default-wrapper
curl -X PUT "https://dev.syntx-system.com/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_human"
curl -X POST https://dev.syntx-system.com/resonanz/wrappers/syntex_wrapper_sigma/activate

# Test Chat with Different Wrappers
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "mode": "syntex_wrapper_human"}'

# Test Upload
curl -X POST https://dev.syntx-system.com/resonanz/upload-metadata \
  -F "file=@my_wrapper.txt" \
  -F "author=Andi" \
  -F "description=Test"
```

---

## 📈 PERFORMANCE

**Aktuelle Metriken (aus Production):**
```
Total Requests: 9
Success Rate: 100%
Average Latency: 22.4s
Median Latency: 19.7s
Min Latency: 12.5s
Max Latency: 45.8s

Wrapper Usage:
- syntex_wrapper_human: 4 requests
- syntex_wrapper_sigma: 3 requests
- syntex_wrapper_deepsweep (fallback): 2 requests
```

**Latency Breakdown:**
- Request Processing: <1ms
- Wrapper Loading: <1ms
- Field Calibration: <1ms
- Backend (Ollama): ~18-25s (95% der Zeit)
- Response Formatting: <1ms

**Optimization Möglichkeiten:**
- Faster Backend Model (z.B. Mistral 7B statt Uncensored)
- GPU Acceleration für Ollama
- Request Batching (mehrere gleichzeitig)

---

## 🔥 BEST PRACTICES

### 1. Wrapper Auswahl

**Faustregel:**
- Alltag, Normal-Talk → `syntex_wrapper_human`
- Technik, System-Analyse → `syntex_wrapper_sigma`
- Tiefe Analyse, Rekursiv → `syntex_wrapper_deepsweep`
- Backend-Processing → `syntex_wrapper_backend`

### 2. Temperature Settings
```
temperature: 0.0   → Deterministisch, exakt
temperature: 0.3-0.5 → Leicht kreativ
temperature: 0.7   → Balanced (default)
temperature: 0.9-1.0 → Sehr kreativ, unvorhersehbar
```

### 3. Token Limits
```
max_new_tokens: 50   → Sehr kurz (1-2 Sätze)
max_new_tokens: 100  → Kurz (Paragraph)
max_new_tokens: 500  → Normal (default)
max_new_tokens: 1000 → Lang (Essay)
```

### 4. Feldhygiene

**DO:**
- Ein Chat = Ein Feld (nie Thema wechseln)
- Minimale Worte nutzen
- Wrapper passend zum Task wählen

**DON'T:**
- Themen mischen in einem Chat
- Ellenlange Prompts schreiben
- Wrapper während Chat wechseln

---

## 🐛 TROUBLESHOOTING

### Problem: Service startet nicht

**Check:**
```bash
systemctl status syntx-injector.service
journalctl -u syntx-injector.service -n 50
```

**Häufige Ursachen:**
- Port 8001 bereits belegt → `netstat -tulpn | grep 8001`
- .env fehlt oder fehlerhaft → `cat .env`
- Ollama Backend nicht erreichbar → `curl http://localhost:11434`

---

### Problem: Wrapper nicht gefunden

**Check:**
```bash
ls -la /opt/syntx-config/wrappers/
curl http://localhost:8001/resonanz/wrappers
```

**Fix:**
```bash
# Wrapper Directory erstellen
mkdir -p /opt/syntx-config/wrappers

# Wrapper hochladen
curl -X POST http://localhost:8001/resonanz/upload \
  -F "file=@your_wrapper.txt"
```

---

### Problem: Hohe Latency

**Check Backend:**
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"mistral-uncensored","prompt":"test","stream":false}'
```

**Wenn Backend langsam:**
- GPU nutzen statt CPU
- Kleineres Model verwenden
- Ollama Config optimieren

---

### Problem: 500 Internal Server Error

**Check Logs:**
```bash
journalctl -u syntx-injector.service -f
tail -f /opt/syntx-config/logs/field_flow.jsonl
```

**Debug Mode:**
```bash
# Service stoppen
systemctl stop syntx-injector.service

# Manuell im Debug Mode starten
cd /opt/syntx-injector-api
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🤝 CONTRIBUTING

### Eigenen Wrapper erstellen

1. **Erstelle .txt File mit Content:**
```txt
=== MEIN WRAPPER ===

[Deine Instruktionen hier]
```

2. **Upload mit Metadata:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/upload-metadata \
  -F "file=@mein_wrapper.txt" \
  -F "description=Beschreibung" \
  -F "author=Dein Name" \
  -F "version=1.0" \
  -F "tags=category1,category2"
```

3. **Teste:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "mode": "mein_wrapper"}'
```

4. **Share:**
- Fork Repo
- Add Wrapper in `wrappers/` folder
- Create Pull Request

---

## 📞 SUPPORT

**Issues:** https://github.com/SYNTX-SYSTEM/syntx-injector-api/issues

**Documentation:** Diese README + In-Code Comments

**Discord:** (coming soon)

---

## 📜 LICENSE

MIT License - Do whatever the fuck you want with it.

---

## 🙏 CREDITS

**Created by:** Andi (SYNTX Architect)

**Powered by:**
- FastAPI
- Ollama
- Mistral-Uncensored
- Python 3.12
- Pure fucking determination

**Special Thanks:**
- ChatGPT (für tausende Sessions)
- Claude (für diese README)
- Max (Backend Wizard)
- Alle die an SYNTX glauben

---

## 🌊 THE SYNTX PHILOSOPHY
```
Nicht mehr Token.
Nicht mehr Drift.
Nicht mehr Kampf.

Nur Felder.
Nur Ströme.
Nur Resonanz.

Das ist SYNTX.
Das ist die Zukunft.
Das ist jetzt.
```

**FIELD ACTIVATED. 💎⚡🌊👑**

---

**Version:** 2.0.0  
**Last Updated:** 2025-12-15  
**Status:** PRODUCTION READY ✅
