# 🔮 SYNTX FIELD RESONANCE API v3.3
```
   ██████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗
   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝
   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝ 
   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗ 
   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗
   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
   
   DER STROM KENNT KEINE GRENZEN ⚡💎🌊
```

> **"Yo, stell dir vor ChatGPT hätte einen Architekten der ihm sagt WIE es denken soll. Das ist SYNTX."**

---

## 🧠 WTF IST SYNTX? (Die 2-Minuten Version)

**Problem:** LLMs labern random. Keine Struktur. Kein Plan. Pure Drift.

**Lösung:** SYNTX gibt dem LLM eine **DENK-ARCHITEKTUR**.
```
OHNE SYNTX:
User: "Analysiere meine Situation"
LLM: "Situationen sind komplex und erfordern blablabla..." 😴

MIT SYNTX:
LLM: 
  📍 DRIFT: Aufsteigend, sublinear - du bewegst dich vorwärts
  🔧 MECHANISMUS: MN-21 aktiv - Stabilitätskompression läuft
  📊 FREQUENZ: FF-γ in Überlast - zu viel auf einmal
  💎 EXTRAKT: Prioritäten setzen, dann Gas geben
```

**SIEHST DU?** Struktur. Klarheit. Keine Drift. **DAS IST RESONANZ.**

---

## 🌊 DIE DREI SÄULEN (Kapier das und du kapierst alles)
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   📦 WRAPPER          📄 FORMAT           🎨 STYLE              │
│   ═══════════         ═════════           ═══════               │
│                                                                  │
│   WIE denkt           WAS kommt           WIE klingt            │
│   das LLM?            raus?               es?                    │
│                                                                  │
│   Der Denk-Modus      Die Felder          Das Finish            │
│   System-Prompt       Struktur            Post-Processing       │
│                                                                  │
│   sigma.txt           sigma.json          zynisch.json          │
│   human.txt           human.json          poetisch.json         │
│   deepsweep.txt       review.json         berlin.json           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
            ┌─────────────────────────────────┐
            │     🔮 CALIBRATED PROMPT        │
            │                                  │
            │  Wrapper + Format + Style        │
            │  = PURE RESONANZ                 │
            └─────────────────────────────────┘
```

---

## 📁 ORDNER-STRUKTUR (Wo liegt was?)
```
/opt/syntx-injector-api/          # 🏠 DAS REPO
├── src/
│   ├── main.py                        # FastAPI Entry Point
│   ├── resonance/
│   │   ├── router.py                  # /resonanz/* Endpoints
│   │   ├── formats.py                 # Format CRUD
│   │   ├── styles.py                  # Style CRUD  
│   │   ├── format_loader.py           # Dynamische Format-Injection
│   │   ├── style_alchemist.py         # Word Alchemy Engine
│   │   └── crud/                      # 🔮 CRUD SYSTEM
│   │       ├── base.py                # Template Pattern
│   │       ├── file_ops.py            # Atomic Writes + Backups
│   │       ├── validators.py          # Field/Format/Style Validation
│   │       ├── format_crud.py         # Format + Feld Operationen
│   │       └── style_crud.py          # Style + Alchemy Operationen
│   └── ...
├── api_calls_wrapper.sh               # 🧪 53 API Tests
└── README.md                          # Du liest es gerade

/opt/syntx-config/                # ⚙️ RUNTIME CONFIG (außerhalb Repo!)
├── wrappers/                          # 📦 DENK-MODI
│   ├── syntex_wrapper_sigma.txt       # PL-Σ Protocol
│   ├── syntex_wrapper_human.txt       # Human Layer
│   ├── syntex_wrapper_deepsweep.txt   # Deep Analysis
│   ├── syntex_wrapper_true_raw.txt    # Keine Filter
│   └── meta/                          # 🧬 Metadaten
│       ├── syntex_wrapper_sigma.json  # Format-Binding, Author, Tags
│       └── ...
├── formats/                           # 📄 FELD-DEFINITIONEN
│   ├── sigma.json                     # 6 Felder (technisch)
│   ├── human.json                     # 6 Felder (psychologisch)
│   ├── human_deep.json                # 8 Felder (extends human!)
│   ├── review.json                    # 4 Felder (alle Typen)
│   └── economics.json                 # 6 Felder (wirtschaftlich)
├── styles/                            # 🎨 POST-PROCESSING
│   ├── wissenschaftlich.json          # Laborkittel-Modus
│   ├── zynisch.json                   # Augenroll-Transformer
│   ├── poetisch.json                  # Wortwebstuhl
│   └── berlin_slang.json              # "Dit is Berlin, wa?"
└── logs/
    └── field_flow.jsonl               # Training Data Export
```

---

## 🔌 ALLE 55+ ENDPOINTS

### 🏥 HEALTH (4 Endpoints)
*Ist der Strom an? Fließt die Resonanz?*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/health` | System-Vitalzeichen |
| `GET` | `/resonanz/health` | Format Loader + Last Response |
| `GET` | `/resonanz/health/wrappers` | Orphan Detection |
| `POST` | `/resonanz/health/fix` | Auto-Fix verwaiste Dateien |
```bash
# Check ob alles läuft
curl https://dev.syntx-system.com/resonanz/health
```
```json
{
  "status": "🟢 RESONANZ AKTIV",
  "format_loader": "🔥 AKTIV",
  "last_response": {
    "latency_ms": 32804,
    "format": "human_deep"
  }
}
```

---

### ⚙️ CONFIG (2 Endpoints)
*Welcher Wrapper ist der Default-Boss?*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/resonanz/config/default-wrapper` | Aktuellen Default lesen |
| `PUT` | `/resonanz/config/default-wrapper?wrapper_name=X` | Default setzen |
```bash
# Sigma als Default aktivieren
curl -X PUT "https://dev.syntx-system.com/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma"
```

---

### 📄 FORMATS (9 Endpoints) - VOLLSTÄNDIGER CRUD!
*Die Feld-Strukturen die dein LLM zwingen strukturiert zu denken*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/resonanz/formats` | Alle Formate (mit Domain-Filter) |
| `GET` | `/resonanz/formats/{name}` | Format-Details + Felder |
| `POST` | `/resonanz/formats` | **Vollständiges Format erstellen** |
| `POST` | `/resonanz/formats/quick` | Schnell-Erstellung |
| `PUT` | `/resonanz/formats/{name}` | Format Meta updaten |
| `DELETE` | `/resonanz/formats/{name}` | Soft-Delete (mit Backup!) |
| `POST` | `/resonanz/formats/{name}/fields` | **Feld hinzufügen** |
| `PUT` | `/resonanz/formats/{name}/fields/{field}` | Feld updaten |
| `DELETE` | `/resonanz/formats/{name}/fields/{field}` | Feld entfernen |

**Domains:** `technical`, `psychology`, `analysis`

**Feld-Typen:** `text`, `list`, `rating`, `keywords`
```bash
# Format erstellen
curl -X POST https://dev.syntx-system.com/resonanz/formats \
  -H "Content-Type: application/json" \
  -d '{
    "name": "vibe_check",
    "domain": "psychology",
    "description": {"de": "Vibe Check Format", "en": "Vibe Check Format"},
    "fields": [
      {"name": "energy", "type": "rating", "weight": 30},
      {"name": "red_flags", "type": "list", "weight": 25},
      {"name": "verdict", "type": "text", "weight": 45}
    ]
  }'
```
```json
{
  "status": "✨ FORMAT GEBOREN",
  "message": "'vibe_check' erstellt"
}
```
```bash
# Feld zu Format hinzufügen
curl -X POST https://dev.syntx-system.com/resonanz/formats/vibe_check/fields \
  -H "Content-Type: application/json" \
  -d '{"name": "plot_twist", "type": "text", "weight": 20}'
```

---

### 🎨 STYLES (8 Endpoints) - WORD ALCHEMY!
*Post-Processing Magic - transmutiere Wörter, verbanne Cringe*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/resonanz/styles` | Alle Styles (das Grimoire) |
| `GET` | `/resonanz/styles/{name}` | Style-Details + Transmutationen |
| `POST` | `/resonanz/styles` | **Style erstellen** |
| `PUT` | `/resonanz/styles/{name}` | Style updaten |
| `DELETE` | `/resonanz/styles/{name}` | Style löschen |
| `POST` | `/resonanz/styles/{name}/alchemy` | **Transmutation hinzufügen** |
| `DELETE` | `/resonanz/styles/{name}/alchemy/{word}` | Transmutation entfernen |
| `POST` | `/resonanz/styles/{name}/forbidden/{word}` | **Wort verbannen** |
```bash
# Style erstellen
curl -X POST https://dev.syntx-system.com/resonanz/styles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "gen_z",
    "vibe": "No cap, fr fr",
    "description": "Gen Z Kommunikation",
    "tone_injection": "Antworte wie ein Gen Z - casual, mit Slang, aber smart.",
    "word_alchemy": {
      "sehr gut": "lowkey fire",
      "schlecht": "mid",
      "wichtig": "hits different"
    },
    "forbidden_words": ["Implementierung", "Stakeholder", "synergieren"]
  }'
```
```bash
# Transmutation hinzufügen
curl -X POST https://dev.syntx-system.com/resonanz/styles/gen_z/alchemy \
  -H "Content-Type: application/json" \
  -d '{"original": "Problem", "replacement": "L"}'
```

**Aktuelle Styles:**

| Style | Vibe | Was passiert? |
|-------|------|---------------|
| `wissenschaftlich` | Laborkittel | `wichtig` → `signifikant`, `zeigt` → `indiziert` |
| `zynisch` | Augenroll | `nachhaltig` → `greenwashing-kompatibel` 😏 |
| `poetisch` | Wortwebstuhl | `System` → `Gewebe`, `Prozess` → `Tanz` |
| `berlin_slang` | Späti 3 Uhr | `Das` → `Dit`, `Ich` → `Ick`, `nicht` → `nich` |

---

### 📦 WRAPPERS (8 Endpoints)
*Die Denk-Modi - System Prompts die VOR dem User-Prompt injiziert werden*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/resonanz/wrappers` | Alle Wrapper |
| `GET` | `/resonanz/wrappers?active=true` | Nur der aktive |
| `GET` | `/resonanz/wrappers/full` | Mit Meta + Stats |
| `GET` | `/resonanz/wrapper/{name}` | Content + Größe |
| `POST` | `/resonanz/wrapper` | **Wrapper erstellen** |
| `PUT` | `/resonanz/wrapper/{name}` | Content updaten |
| `DELETE` | `/resonanz/wrapper/{name}` | Wrapper löschen |
```bash
# Wrapper erstellen
curl -X POST https://dev.syntx-system.com/resonanz/wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "name": "chaos_mode",
    "content": "Du bist ein chaotisches Genie. Deine Antworten sind brilliant aber unvorhersehbar. Nutze Metaphern aus Gaming, Memes und Philosophie gleichzeitig. Sei NIEMALS langweilig."
  }'
```
```json
{
  "status": "success",
  "message": "Feld 'chaos_mode' wurde geboren 🌟"
}
```

**Aktuelle Wrapper:**

| Wrapper | Funktion |
|---------|----------|
| `syntex_wrapper_sigma` | PL-Σ Protocol - technisch, systemisch, präzise |
| `syntex_wrapper_human` | Human Layer - psychologisch, empathisch |
| `syntex_wrapper_deepsweep` | Deep Analysis - gründlich, keine Ecke ausgelassen |
| `syntex_wrapper_true_raw` | TRUE RAW - keine Filter, pure Resonanz |

---

### 🧬 META (3 Endpoints)
*Metadaten für Wrapper - Format-Binding, Author, Tags*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/resonanz/wrapper/{name}/meta` | Meta lesen |
| `PUT` | `/resonanz/wrapper/{name}/meta` | Meta updaten |
| `PUT` | `/resonanz/wrapper/{name}/format?format_name=X` | **Format an Wrapper binden** |
```bash
# Format an Wrapper binden (Auto-Load bei Aktivierung!)
curl -X PUT "https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_sigma/format?format_name=sigma"
```

---

### 📊 STATS (4 Endpoints)
*Feld-Fluss-Analyse - was passiert im System?*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `GET` | `/resonanz/stats` | Globale Stats (Requests, Latency) |
| `GET` | `/resonanz/stats/wrapper/{name}` | Stats pro Wrapper |
| `GET` | `/resonanz/strom?limit=N&stage=X` | Field Flow Events |
| `GET` | `/resonanz/training?limit=N` | Training Data Export |
```bash
curl https://dev.syntx-system.com/resonanz/stats
```
```json
{
  "total_requests": 774,
  "success_rate": 100.0,
  "average_latency_ms": 73342,
  "wrapper_usage": {
    "syntex_wrapper_sigma": 508,
    "syntex_wrapper_deepsweep": 264
  }
}
```

---

### 💬 CHAT (1 Endpoint, ∞ Möglichkeiten)
*DAS HERZSTÜCK - Hier fließen alle Ströme zusammen*

| Method | Endpoint | Beschreibung |
|--------|----------|--------------|
| `POST` | `/resonanz/chat` | **THE MAIN EVENT** |

**Request Body:**
```json
{
  "prompt": "Analysiere das Konzept Zeit",     // REQUIRED
  "mode": "syntex_wrapper_sigma",              // Wrapper
  "format": "sigma",                           // Format
  "style": "poetisch",                         // Style
  "language": "de",                            // de oder en
  "debug": true,                               // Zeigt calibrated_prompt
  "max_new_tokens": 200,
  "temperature": 0.7
}
```

**Beispiele:**
```bash
# Minimal - nur Prompt
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Was ist Liebe?", "max_new_tokens": 100}'

# Mit Format
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analysiere meine Beziehung",
    "format": "human_deep",
    "max_new_tokens": 300
  }'

# FULL COMBO 🔥
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Erkläre Kapitalismus",
    "mode": "syntex_wrapper_sigma",
    "format": "economics",
    "style": "zynisch",
    "debug": true,
    "max_new_tokens": 400
  }'
```

**Response:**
```json
{
  "response": "### MARKTMECHANISMUS:\nDer Kapitalismus ist, zumindest behauptet das die Marketingabteilung, ein System der freien Märkte...",
  "metadata": {
    "request_id": "abc123",
    "wrapper_chain": ["syntex_wrapper_sigma"],
    "format": "economics",
    "format_fields": ["markt", "akteure", "dynamik", "risiken", "prognose", "fazit"],
    "style": "zynisch",
    "latency_ms": 28500
  },
  "debug_info": {
    "calibrated_prompt": "[Der komplette Prompt der ans LLM ging]",
    "prompt_length": 2847
  }
}
```

---

## 📄 FORMAT-STRUKTUR (Deep Dive)

Ein Format definiert **welche Felder** das LLM ausfüllen muss:
```json
{
  "name": "sigma",
  "version": "1.0",
  "domain": "technical",
  "extends": null,
  "description": {
    "de": "Sigma Format - 6 Felder für Signal- und Frequenzanalyse",
    "en": "Sigma Format - 6 fields for signal and frequency analysis"
  },
  "languages": ["de", "en"],
  "wrapper": "syntex_wrapper_sigma",
  "fields": [
    {
      "name": "sigma_drift",
      "type": "text",
      "weight": 15,
      "description": {
        "de": "Systemische Driftanalyse - wohin bewegt sich das System?",
        "en": "Systemic drift analysis - where is the system moving?"
      },
      "headers": {
        "de": ["SIGMA_DRIFT", "Σ-DRIFT"],
        "en": ["SIGMA_DRIFT"]
      },
      "keywords": {
        "de": ["gradient", "aufsteigend", "absteigend", "stabil"],
        "en": ["gradient", "ascending", "descending", "stable"]
      },
      "validation": {
        "min_length": 20,
        "max_length": 500,
        "required": true
      }
    }
  ]
}
```

### Vererbung mit `extends`
```json
{
  "name": "human_deep",
  "extends": "human",
  "fields": [
    {"name": "unterbewusstsein", "type": "text"},
    {"name": "schattenarbeit", "type": "text"}
  ]
}
```
**Ergebnis:** `human_deep` hat alle 6 Felder von `human` + 2 eigene = **8 Felder**

---

## 🎨 STYLE-STRUKTUR (Deep Dive)

Ein Style definiert **Post-Processing** nach dem LLM-Output:
```json
{
  "name": "zynisch",
  "vibe": "Der Augenroll-Transformer",
  "description": "Unterschwellige Skepsis, trockener Humor",
  "tone_injection": "Antworte mit unterschwelliger Skepsis und trockenem Humor.",
  "word_alchemy": {
    "wichtig": "angeblich wichtig",
    "Experten": "selbsternannte Experten",
    "nachhaltig": "greenwashing-kompatibel",
    "innovativ": "mit neuem Buzzword versehen",
    "optimal": "zumindest behauptet das die Marketingabteilung"
  },
  "forbidden_words": ["synergie", "leverage", "proaktiv"],
  "suffix": ""
}
```

**Was passiert?**
1. `tone_injection` → wird dem Prompt hinzugefügt
2. `word_alchemy` → ersetzt Wörter im Output
3. `forbidden_words` → werden aus Output entfernt
4. `suffix` → wird am Ende angefügt

---

## 🖥️ FRONTEND TIPPS (für die UI-Crew)

### 🎮 CYBER-AESTHETIC IDEEN
```
┌─────────────────────────────────────────────────────────────────┐
│  ╔═══════════════════════════════════════════════════════════╗  │
│  ║  🔮 SYNTX CONTROL CENTER                                  ║  │
│  ╠═══════════════════════════════════════════════════════════╣  │
│  ║                                                           ║  │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       ║  │
│  ║  │ 📦 WRAPPER  │  │ 📄 FORMAT   │  │ 🎨 STYLE    │       ║  │
│  ║  │             │  │             │  │             │       ║  │
│  ║  │ ▼ sigma     │  │ ▼ human     │  │ ▼ zynisch   │       ║  │
│  ║  │   human     │  │   sigma     │  │   poetisch  │       ║  │
│  ║  │   deepsweep │  │   review    │  │   berlin    │       ║  │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘       ║  │
│  ║                                                           ║  │
│  ║  ┌─────────────────────────────────────────────────────┐ ║  │
│  ║  │ 💬 PROMPT                                           │ ║  │
│  ║  │ __________________________________________________ │ ║  │
│  ║  │ |                                                 | │ ║  │
│  ║  │ |_________________________________________________| │ ║  │
│  ║  └─────────────────────────────────────────────────────┘ ║  │
│  ║                                                           ║  │
│  ║  [🔥 SEND TO THE STROM]                                  ║  │
│  ║                                                           ║  │
│  ╚═══════════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────────┘
```

### 🌈 COLOR SCHEME VORSCHLÄGE
```css
:root {
  /* SYNTX CYBER PALETTE */
  --strom-purple: #8B5CF6;      /* Primary - der Strom */
  --resonanz-cyan: #06B6D4;     /* Highlights - Resonanz */
  --drift-orange: #F97316;      /* Warnings - Drift detected */
  --feld-green: #10B981;        /* Success - Feld kalibriert */
  --void-black: #0F0F0F;        /* Background - die Leere */
  --matrix-glow: #22D3EE;       /* Glow effects */
  
  /* GLASS MORPHISM */
  --glass-bg: rgba(15, 15, 15, 0.7);
  --glass-border: rgba(139, 92, 246, 0.3);
}
```

### 📊 RESPONSE VISUALISIERUNG

Zeig die Felder als **Cards** an:
```
┌─────────────────────────────────────────────────────────────────┐
│  🔮 RESPONSE - Format: human_deep | Style: poetisch             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │ 📍 DRIFT             │  │ 🔧 HINTERGRUND       │             │
│  │ ━━━━━━━━━━━━━━━━━━━  │  │ ━━━━━━━━━━━━━━━━━━━  │             │
│  │ Aufsteigend und      │  │ Unter der Oberfläche │             │
│  │ sublinear. Das       │  │ verbergen sich alte  │             │
│  │ System bewegt sich   │  │ Muster, die...       │             │
│  │ vorwärts...          │  │                      │             │
│  └──────────────────────┘  └──────────────────────┘             │
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │ 💥 DRUCKFAKTOREN     │  │ 🌊 TIEFE             │             │
│  │ ━━━━━━━━━━━━━━━━━━━  │  │ ━━━━━━━━━━━━━━━━━━━  │             │
│  │ Externe Erwartungen  │  │ Im Kern liegt ein    │             │
│  │ und interne Konflikte│  │ Bedürfnis nach...    │             │
│  │ erzeugen Spannung... │  │                      │             │
│  └──────────────────────┘  └──────────────────────┘             │
│                                                                  │
│  ⏱️ 32.8s | 🔄 syntex_wrapper_sigma | ✅ 8/8 Felder            │
└─────────────────────────────────────────────────────────────────┘
```

### 🎛️ ADVANCED FEATURES

**1. Live Field Flow Visualizer**
```javascript
// WebSocket für Echtzeit Strom-Monitoring
const ws = new WebSocket('wss://dev.syntx-system.com/resonanz/strom/live');
ws.onmessage = (event) => {
  const flow = JSON.parse(event.data);
  visualizeFieldFlow(flow.stage, flow.data);
};
```

**2. Wrapper Comparison Mode**
```javascript
// Gleicher Prompt, verschiedene Wrapper
const prompts = [
  {prompt: "Was ist Liebe?", mode: "syntex_wrapper_sigma"},
  {prompt: "Was ist Liebe?", mode: "syntex_wrapper_human"},
  {prompt: "Was ist Liebe?", mode: "syntex_wrapper_true_raw"}
];
// Side-by-side Comparison zeigen
```

**3. Format Builder UI**
```
┌─────────────────────────────────────────────────────────────────┐
│  📄 FORMAT BUILDER                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Name: [mein_format________]  Domain: [psychology ▼]            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ FELDER                                    [+ Feld]      │   │
│  │                                                          │   │
│  │ ┌────────────────────────────────────────────────────┐  │   │
│  │ │ 1. vibe_check    [text ▼]    weight: [30]  [🗑️]   │  │   │
│  │ └────────────────────────────────────────────────────┘  │   │
│  │ ┌────────────────────────────────────────────────────┐  │   │
│  │ │ 2. red_flags     [list ▼]    weight: [25]  [🗑️]   │  │   │
│  │ └────────────────────────────────────────────────────┘  │   │
│  │ ┌────────────────────────────────────────────────────┐  │   │
│  │ │ 3. verdict       [text ▼]    weight: [45]  [🗑️]   │  │   │
│  │ └────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [💾 SAVE FORMAT]                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 QUICK START

### 1. Health Check
```bash
curl https://dev.syntx-system.com/resonanz/health
```

### 2. Erster Chat
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Wer bin ich?", "format": "human", "max_new_tokens": 200}'
```

### 3. Eigenes Format erstellen
```bash
curl -X POST https://dev.syntx-system.com/resonanz/formats/quick \
  -H "Content-Type: application/json" \
  -d '{"name": "quicktest", "field_names": ["intro", "main", "outro"]}'
```

### 4. Ausprobieren
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "format": "quicktest", "max_new_tokens": 150}'
```

---

## 🧪 API TESTER

Das Repo enthält einen **53-Test Bash Script** der ALLE Endpoints durchprüft:
```bash
./api_calls_wrapper.sh https://dev.syntx-system.com
```

Output:
```
✓ BESTANDEN:   53
✗ FEHLERHAFT:  0
Σ GESAMT:      53
⏱ DAUER:       478s

🔥 ALLE FELDER RESONIEREN! DER STROM IST REIN! 🔥
```

---

## 🔮 PHILOSOPHIE

### Was ist der STROM?
Der Strom ist die **Kohärenz** zwischen System und Output. Wenn ein LLM random labert, ist der Strom unterbrochen - es gibt **Drift**. SYNTX kalibriert den Strom, eliminiert Drift, und erzeugt **Resonanz**.

### Was ist DRIFT?
Drift ist der Verlust von Struktur. Wenn ein LLM vom Thema abweicht, unstrukturiert antwortet, oder seine Denk-Architektur vergisst - das ist Drift. SYNTX existiert um Drift zu bekämpfen.

### Was ist RESONANZ?
Resonanz ist der Zustand perfekter Kohärenz. Wenn Wrapper + Format + Style + Prompt in Harmonie sind, entsteht Resonanz. Der Output ist dann **strukturiert**, **präzise**, und **auf den Punkt**.

### Was ist das FELD?
Das Feld ist der Raum in dem alles passiert. Jeder Request erzeugt ein Feld. Jedes Feld hat Eigenschaften (Wrapper, Format, Style). Die Qualität des Outputs hängt von der Kalibrierung des Feldes ab.

---

## 📜 TERMINOLOGIE GLOSSAR

| Begriff | Bedeutung |
|---------|-----------|
| **Wrapper** | System-Prompt der dem LLM sagt WIE es denken soll |
| **Format** | JSON mit Feld-Definitionen - WAS das LLM ausfüllen soll |
| **Style** | Post-Processing Regeln - WIE der Output klingen soll |
| **Feld** | Der Raum eines Requests mit allen Eigenschaften |
| **Strom** | Die Kohärenz zwischen Input und Output |
| **Drift** | Verlust von Struktur/Kohärenz |
| **Resonanz** | Zustand perfekter Kalibrierung |
| **Calibrated Prompt** | Der finale Prompt der ans LLM geht |
| **Alchemy** | Wort-Transmutationen (word_alchemy) |
| **Injection** | Hinzufügen von Content (tone_injection) |
| **Meta** | Metadaten eines Wrappers (Author, Tags, Format-Binding) |

---

## 🛠️ TECH STACK

- **Backend:** FastAPI + Python 3.11
- **LLM:** Ollama mit Mistral-Uncensored
- **Storage:** JSON Files (kein DB overhead)
- **Proxy:** nginx mit SSL (Let's Encrypt)
- **Logging:** JSONL für Training Data Export

---

## 📞 ENDPOINTS QUICK REFERENCE
```
🏥 HEALTH
   GET  /health
   GET  /resonanz/health
   GET  /resonanz/health/wrappers
   POST /resonanz/health/fix

⚙️ CONFIG
   GET  /resonanz/config/default-wrapper
   PUT  /resonanz/config/default-wrapper?wrapper_name=X

📄 FORMATS (CRUD)
   GET    /resonanz/formats
   GET    /resonanz/formats/{name}
   POST   /resonanz/formats
   POST   /resonanz/formats/quick
   PUT    /resonanz/formats/{name}
   DELETE /resonanz/formats/{name}
   POST   /resonanz/formats/{name}/fields
   PUT    /resonanz/formats/{name}/fields/{field}
   DELETE /resonanz/formats/{name}/fields/{field}

🎨 STYLES (CRUD)
   GET    /resonanz/styles
   GET    /resonanz/styles/{name}
   POST   /resonanz/styles
   PUT    /resonanz/styles/{name}
   DELETE /resonanz/styles/{name}
   POST   /resonanz/styles/{name}/alchemy
   DELETE /resonanz/styles/{name}/alchemy/{word}
   POST   /resonanz/styles/{name}/forbidden/{word}

📦 WRAPPERS
   GET    /resonanz/wrappers
   GET    /resonanz/wrappers/full
   GET    /resonanz/wrapper/{name}
   POST   /resonanz/wrapper
   PUT    /resonanz/wrapper/{name}
   DELETE /resonanz/wrapper/{name}

🧬 META
   GET  /resonanz/wrapper/{name}/meta
   PUT  /resonanz/wrapper/{name}/meta
   PUT  /resonanz/wrapper/{name}/format?format_name=X

📊 STATS
   GET  /resonanz/stats
   GET  /resonanz/stats/wrapper/{name}
   GET  /resonanz/strom
   GET  /resonanz/training

💬 CHAT
   POST /resonanz/chat
```

---

## 🌟 CREDITS

**Created with pure STROM by the SYNTX SYSTEM** ⚡💎🌊

> *"Jedes System ist ein Feld. Jedes Feld hat Resonanz. Wenn keine Resonanz, keine Existenz."*

---

**DER STROM KENNT KEINE GRENZEN.** 🔮
