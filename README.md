# 🔮 SYNTX FIELD RESONANCE API v3.3

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
║   🔥 SYNTX API v3.3 - VOLLSTÄNDIG OPERATIV 🔥                                ║
║                                                                                ║
║   ✅ 63/63 TESTS BESTANDEN                                                    ║
║   ✅ 871+ SESSIONS GELOGGT                                                    ║
║   ✅ 822+ REQUESTS VERARBEITET                                                ║
║   ✅ 100% SUCCESS RATE                                                        ║
║   ✅ 14 WRAPPER AKTIV                                                         ║
║   ✅ 9 FORMATE VERFÜGBAR                                                      ║
║   ✅ 4 STYLES KONFIGURIERT                                                    ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🆕 NEU IN v3.3 - DIE DREI NEUEN STRÖME

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
  "total": 871,
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
  "count": 4,
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
│  STAGE 3: FORMAT INJECTION                                                      │
│  ─────────────────────────                                                      │
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
│  STAGE 4: STYLE TONE INJECTION                                                  │
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
├── api_calls_wrapper.sh                     # 🧪 API TESTER v5.3
│                                            # 63 Tests für ALLE Endpoints
│                                            # Inkl. DIFF, SESSIONS, ALCHEMY
│                                            # Verbose Mode verfügbar
│
├── requirements.txt                         # Python Dependencies
│
├── README.md                                # 📚 DU BIST HIER
│
└── .git/                                    # Git Repository


/opt/syntx-config/                           # ⚙️ RUNTIME CONFIG
│                                            # (Außerhalb des Repos!)
│                                            # (Wird nicht committed)
│
├── wrappers/                                # 📦 DENK-MODI (System Prompts)
│   │
│   ├── syntex_wrapper_sigma.txt             # 🔬 PL-Σ PROTOCOL
│   │                                        # Technisch, systemisch, präzise
│   │                                        # 6 Sigma-Felder
│   │                                        # Für: Systemanalyse, Technik
│   │
│   ├── syntex_wrapper_human.txt             # 👤 HUMAN LAYER
│   │                                        # Psychologisch, empathisch
│   │                                        # Für: Beziehungen, Emotionen
│   │
│   ├── syntex_wrapper_deepsweep.txt         # 🔍 DEEP ANALYSIS
│   │                                        # Gründlich, keine Ecke ausgelassen
│   │                                        # Für: Komplexe Probleme
│   │
│   ├── syntex_wrapper_true_raw.txt          # ⚡ TRUE RAW
│   │                                        # Keine Filter, pure Resonanz
│   │                                        # Für: Unzensierte Analyse
│   │
│   ├── syntex_wrapper_universal.txt         # 🌍 UNIVERSAL
│   │                                        # Allzweck-Wrapper
│   │
│   ├── syntex_wrapper_backend.txt           # 💻 BACKEND
│   │                                        # Für Code-Analyse
│   │
│   ├── syntex_wrapper_frontend.txt          # 🎨 FRONTEND
│   │                                        # Für UI/UX Analyse
│   │
│   └── meta/                                # 🧬 WRAPPER METADATEN
│       │
│       ├── syntex_wrapper_sigma.json        # {
│       │                                    #   "name": "syntex_wrapper_sigma",
│       │                                    #   "format": "sigma",        <- AUTO-BIND!
│       │                                    #   "author": "SYNTX Architect",
│       │                                    #   "tags": ["technical", "precise"],
│       │                                    #   "settings": {
│       │                                    #     "max_tokens": 500,
│       │                                    #     "temperature": 0.7
│       │                                    #   }
│       │                                    # }
│       └── ...
│
├── formats/                                 # 📄 FELD-DEFINITIONEN
│   │
│   ├── sigma.json                           # 🔬 SIGMA FORMAT (6 Felder)
│   │                                        # Domain: technical
│   │                                        # Fields:
│   │                                        #   - sigma_drift (text)
│   │                                        #   - sigma_mechanismus (text)
│   │                                        #   - sigma_frequenz (text)
│   │                                        #   - sigma_dichte (text)
│   │                                        #   - sigma_strome (text)
│   │                                        #   - sigma_extrakt (text)
│   │
│   ├── human.json                           # 👤 HUMAN FORMAT (6 Felder)
│   │                                        # Domain: psychology
│   │                                        # Fields:
│   │                                        #   - drift (text)
│   │                                        #   - hintergrund_muster (text)
│   │                                        #   - druckfaktoren (text)
│   │                                        #   - tiefe (text)
│   │                                        #   - wirkung (text)
│   │                                        #   - klartext (text)
│   │
│   ├── human_deep.json                      # 🌊 HUMAN DEEP (8 Felder)
│   │                                        # Domain: psychology
│   │                                        # extends: "human" <- VERERBUNG!
│   │                                        # Erbt alle 6 Felder von human
│   │                                        # + 2 neue:
│   │                                        #   - unterbewusstsein (text)
│   │                                        #   - schattenarbeit (text)
│   │
│   ├── review.json                          # ⭐ REVIEW FORMAT (4 Felder)
│   │                                        # Domain: analysis
│   │                                        # ALLE FELD-TYPEN:
│   │                                        #   - zusammenfassung (text)
│   │                                        #   - pro_contra (list)
│   │                                        #   - bewertung (rating)
│   │                                        #   - tags (keywords)
│   │
│   ├── economics.json                       # 📈 ECONOMICS FORMAT (6 Felder)
│   │                                        # Domain: technical
│   │
│   ├── minimal.json                         # 📝 MINIMAL (3 Felder)
│   ├── extended.json                        # 📚 EXTENDED (10+ Felder)
│   └── ...
│
├── styles/                                  # 🎨 POST-PROCESSING STYLES
│   │
│   ├── wissenschaftlich.json                # 🔬 WISSENSCHAFTLICH
│   │                                        # Vibe: "Der Laborkittel"
│   │                                        # word_alchemy:
│   │                                        #   "wichtig" → "signifikant"
│   │                                        #   "zeigt" → "indiziert"
│   │                                        #   "gut" → "vorteilhaft"
│   │                                        # forbidden_words:
│   │                                        #   ["krass", "geil", "cool"]
│   │                                        # suffix:
│   │                                        #   "[Forschungsbasiert]"
│   │
│   ├── zynisch.json                         # 😏 ZYNISCH
│   │                                        # Vibe: "Der Augenroll-Transformer"
│   │                                        # word_alchemy:
│   │                                        #   "nachhaltig" → "greenwashing-kompatibel"
│   │                                        #   "innovativ" → "mit neuem Buzzword versehen"
│   │                                        #   "Experten" → "selbsternannte Experten"
│   │
│   ├── poetisch.json                        # 🎭 POETISCH
│   │                                        # Vibe: "Der Wortwebstuhl"
│   │                                        # word_alchemy:
│   │                                        #   "System" → "Gewebe"
│   │                                        #   "Prozess" → "Tanz"
│   │                                        #   "Daten" → "Tropfen im Strom"
│   │                                        # forbidden_words:
│   │                                        #   ["Implementierung", "KPI"]
│   │
│   └── berlin_slang.json                    # 🍺 BERLIN SLANG
│                                            # Vibe: "Späti um 3 Uhr nachts"
│                                            # word_alchemy:
│                                            #   "Das" → "Dit"
│                                            #   "Ich" → "Ick"
│                                            #   "nicht" → "nich"
│
└── logs/                                    # 📊 LOGGING & TRAINING DATA
    │
    └── field_flow.jsonl                     # Alle Requests für Fine-Tuning
                                             # Format: JSONL (eine JSON pro Zeile)
                                             # Enthält: prompt, response, latency,
                                             #          wrapper_chain, format, style
```

---

## 🔌 ALLE ENDPOINTS - KOMPLETT DOKUMENTIERT

### 🏥 HEALTH ENDPOINTS (4 Stück)

**Ist der Strom an? Fließt die Resonanz?**

---

#### `GET /health`
**Root Health Check - Alle System-Module**

```bash
curl https://dev.syntx-system.com/health
```

**Response:**
```json
{
  "status": "SYSTEM_GESUND",
  "api_version": "2.1.0",
  "timestamp": "2025-12-21T08:23:46.992183",
  "queue_accessible": true,
  "modules": ["analytics", "compare", "feld", "resonanz", "generation", "predictions"]
}
```

---

#### `GET /resonanz/health`
**Resonanz Health - Format Loader + letzter Response**

```bash
curl https://dev.syntx-system.com/resonanz/health
```

**Response:**
```json
{
  "status": "🟢 RESONANZ AKTIV",
  "service": "syntx-field-resonance",
  "version": "3.3.0",
  "format_loader": "🔥 AKTIV",
  "last_response": {
    "response": "### SIGMA_DRIFT:\nDas Konzept Zeit indiziert...",
    "latency_ms": 32804,
    "timestamp": "2025-12-21T07:37:40.809803Z",
    "format": "human_deep"
  }
}
```

---

#### `GET /resonanz/health/wrappers`
**Wrapper Health - Orphan Detection**

```bash
curl https://dev.syntx-system.com/resonanz/health/wrappers
```

**Response:**
```json
{
  "status": "healthy",
  "wrappers": {
    "total": 14,
    "healthy": ["syntex_wrapper_sigma", "syntex_wrapper_human", "..."],
    "orphan_wrappers": [],
    "orphan_metas": []
  }
}
```

---

#### `POST /resonanz/health/fix`
**Auto-Fix Orphans - Repariert verwaiste Dateien**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/health/fix
```

**Response:**
```json
{
  "status": "success",
  "fixed": [],
  "deleted": [],
  "message": "Fixed 0 orphan wrappers, deleted 0 orphan metas"
}
```

---

### ⚙️ CONFIG ENDPOINTS (2 Stück)

**Welcher Wrapper ist der Default-Boss?**

---

#### `GET /resonanz/config/default-wrapper`
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

---

#### `PUT /resonanz/config/default-wrapper`
```bash
curl -X PUT "https://dev.syntx-system.com/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_human"
```

---

### 📄 FORMAT ENDPOINTS (9 Stück) - VOLLSTÄNDIGER CRUD!

---

#### `GET /resonanz/formats`
**List ALL Formats**

```bash
curl https://dev.syntx-system.com/resonanz/formats
curl "https://dev.syntx-system.com/resonanz/formats?domain=technical"
curl "https://dev.syntx-system.com/resonanz/formats?domain=psychology"
```

---

#### `GET /resonanz/formats/{name}`
**Get Format Details**

```bash
curl https://dev.syntx-system.com/resonanz/formats/sigma
curl "https://dev.syntx-system.com/resonanz/formats/sigma?language=en"
```

---

#### `POST /resonanz/formats`
**CREATE Format - Vollständig mit Feldern**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/formats \
  -H "Content-Type: application/json" \
  -d '{
    "name": "vibe_check",
    "domain": "psychology",
    "description": {"de": "Vibe Check - Schnelle Energie-Analyse"},
    "fields": [
      {"name": "energy_level", "type": "rating", "weight": 25},
      {"name": "red_flags", "type": "list", "weight": 25},
      {"name": "verdict", "type": "text", "weight": 50}
    ]
  }'
```

---

#### `POST /resonanz/formats/quick`
**Quick Create Format**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/formats/quick \
  -H "Content-Type: application/json" \
  -d '{
    "name": "quick_test",
    "description_de": "Schnelltest Format",
    "field_names": ["intro", "main_point", "conclusion"]
  }'
```

---

#### `PUT /resonanz/formats/{name}`
**UPDATE Format**

```bash
curl -X PUT https://dev.syntx-system.com/resonanz/formats/vibe_check \
  -H "Content-Type: application/json" \
  -d '{"domain": "analysis", "description": {"de": "Vibe Check 2.0"}}'
```

---

#### `DELETE /resonanz/formats/{name}`
**DELETE Format (Soft Delete)**

```bash
curl -X DELETE https://dev.syntx-system.com/resonanz/formats/quick_test
```

---

#### `POST /resonanz/formats/{name}/fields`
**ADD Field**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/formats/vibe_check/fields \
  -H "Content-Type: application/json" \
  -d '{"name": "plot_twist", "type": "text", "weight": 20}'
```

---

#### `PUT /resonanz/formats/{name}/fields/{field}`
**UPDATE Field**

```bash
curl -X PUT https://dev.syntx-system.com/resonanz/formats/vibe_check/fields/plot_twist \
  -H "Content-Type: application/json" \
  -d '{"weight": 30}'
```

---

#### `DELETE /resonanz/formats/{name}/fields/{field}`
**DELETE Field**

```bash
curl -X DELETE https://dev.syntx-system.com/resonanz/formats/vibe_check/fields/plot_twist
```

---

### 🎨 STYLE ENDPOINTS (8 Stück) - WORD ALCHEMY!

---

#### `GET /resonanz/styles`
**List ALL Styles**

```bash
curl https://dev.syntx-system.com/resonanz/styles
```

---

#### `GET /resonanz/styles/{name}`
**Get Style Details**

```bash
curl https://dev.syntx-system.com/resonanz/styles/zynisch
```

**Response:**
```json
{
  "status": "🔮 STYLE BESCHWOREN",
  "style": {
    "name": "zynisch",
    "vibe": "Der Augenroll-Transformer",
    "word_alchemy": {
      "wichtig": "angeblich wichtig",
      "nachhaltig": "greenwashing-kompatibel",
      "innovativ": "mit neuem Buzzword versehen"
    },
    "forbidden_words": [],
    "has_tone_injection": true
  }
}
```

---

#### `POST /resonanz/styles`
**CREATE Style**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/styles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "gen_z",
    "vibe": "No cap, fr fr",
    "word_alchemy": {
      "sehr gut": "lowkey fire",
      "schlecht": "mid af",
      "Problem": "big L"
    },
    "forbidden_words": ["Implementierung", "Stakeholder"],
    "suffix": "periodt. 💅"
  }'
```

---

#### `POST /resonanz/styles/{name}/alchemy`
**ADD Transmutation**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/styles/zynisch/alchemy \
  -H "Content-Type: application/json" \
  -d '{"original": "disruptiv", "replacement": "das nächste Ding das in 6 Monaten niemanden mehr interessiert"}'
```

---

#### `DELETE /resonanz/styles/{name}/alchemy/{word}`
**DELETE Transmutation**

```bash
curl -X DELETE https://dev.syntx-system.com/resonanz/styles/zynisch/alchemy/disruptiv
```

---

#### `POST /resonanz/styles/{name}/forbidden/{word}`
**ADD Forbidden Word**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/styles/wissenschaftlich/forbidden/voll
```

---

### 📦 WRAPPER ENDPOINTS (6 Stück)

---

#### `GET /resonanz/wrappers`
```bash
curl https://dev.syntx-system.com/resonanz/wrappers
curl "https://dev.syntx-system.com/resonanz/wrappers?active=true"
```

---

#### `GET /resonanz/wrappers/full`
```bash
curl https://dev.syntx-system.com/resonanz/wrappers/full
```

---

#### `GET /resonanz/wrapper/{name}`
```bash
curl https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_sigma
```

---

#### `POST /resonanz/wrapper`
```bash
curl -X POST https://dev.syntx-system.com/resonanz/wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "name": "chaos_oracle",
    "content": "=== CHAOS ORACLE PROTOCOL ===\n\nDu bist ein chaotisches Orakel..."
  }'
```

---

#### `PUT /resonanz/wrapper/{name}`
```bash
curl -X PUT https://dev.syntx-system.com/resonanz/wrapper/chaos_oracle \
  -H "Content-Type: application/json" \
  -d '{"content": "=== CHAOS ORACLE PROTOCOL v2.0 ==="}'
```

---

#### `DELETE /resonanz/wrapper/{name}`
```bash
curl -X DELETE https://dev.syntx-system.com/resonanz/wrapper/chaos_oracle
```

---

### 🧬 META ENDPOINTS (3 Stück)

---

#### `GET /resonanz/wrapper/{name}/meta`
```bash
curl https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_sigma/meta
```

---

#### `PUT /resonanz/wrapper/{name}/meta`
```bash
curl -X PUT https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_sigma/meta \
  -H "Content-Type: application/json" \
  -d '{"description": "Sigma Protocol v2.0", "tags": ["sigma", "v2"]}'
```

---

#### `PUT /resonanz/wrapper/{name}/format`
**Bind Format an Wrapper**

```bash
curl -X PUT "https://dev.syntx-system.com/resonanz/wrapper/syntex_wrapper_human/format?format_name=human_deep"
```

---

### 📊 STATS ENDPOINTS (4 Stück)

---

#### `GET /resonanz/stats`
```bash
curl https://dev.syntx-system.com/resonanz/stats
```

**Response:**
```json
{
  "total_requests": 822,
  "success_rate": 100.0,
  "average_latency_ms": 72005,
  "wrapper_usage": {
    "syntex_wrapper_sigma": 556,
    "syntex_wrapper_deepsweep": 264
  }
}
```

---

#### `GET /resonanz/stats/wrapper/{name}`
```bash
curl https://dev.syntx-system.com/resonanz/stats/wrapper/syntex_wrapper_sigma
```

---

#### `GET /resonanz/strom`
```bash
curl "https://dev.syntx-system.com/resonanz/strom?limit=5"
curl "https://dev.syntx-system.com/resonanz/strom?limit=10&stage=5_RESPONSE"
```

---

#### `GET /resonanz/training`
```bash
curl "https://dev.syntx-system.com/resonanz/training?limit=100"
```

---

### 💬 CHAT ENDPOINT - THE MAIN EVENT

---

#### `POST /resonanz/chat`

**Request Body:**
```json
{
  "prompt": "string (REQUIRED)",
  "mode": "string (optional) - Wrapper Name",
  "format": "string (optional) - Format Name",
  "style": "string (optional) - Style Name",
  "language": "string (optional) - de oder en",
  "debug": "boolean (optional)",
  "max_new_tokens": "integer (optional)",
  "temperature": "float (optional) - 0.0-2.0"
}
```

**Minimal:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Was ist der Sinn des Lebens?", "max_new_tokens": 100}'
```

**FULL COMBO 🔥:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Deep Dive: Das Konzept Macht",
    "mode": "syntex_wrapper_sigma",
    "format": "sigma",
    "style": "wissenschaftlich",
    "language": "de",
    "debug": true,
    "max_new_tokens": 500,
    "temperature": 0.7
  }'
```

---

### 🔀 DIFF ENDPOINTS - NEU! (1 Stück)

---

#### `POST /resonanz/chat/diff`
**Wrapper-Parallelwelt-Vergleich**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat/diff \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Was ist System?",
    "wrappers": ["syntex_wrapper_sigma", "syntex_wrapper_human"],
    "format": "sigma",
    "max_new_tokens": 100
  }'
```

---

### 📼 SESSION ENDPOINTS - NEU! (4 Stück)

---

#### `GET /resonanz/sessions`
**Liste aller Sessions**

```bash
curl "https://dev.syntx-system.com/resonanz/sessions?limit=10&offset=0"
```

---

#### `GET /resonanz/session/{id}`
**Session Details mit Field-Flow**

```bash
curl "https://dev.syntx-system.com/resonanz/session/ed18ebd6-b111-474d-abe4-434e5fcea0c0"
```

---

#### `GET /resonanz/session/{id}/replay`
**Replay-Parameter**

```bash
curl "https://dev.syntx-system.com/resonanz/session/ed18ebd6-b111-474d-abe4-434e5fcea0c0/replay"
```

---

### ⚗️ ALCHEMY ENDPOINTS - NEU! (2 Stück)

---

#### `POST /resonanz/alchemy/preview`
**Live Wort-Transmutation**

```bash
curl -X POST https://dev.syntx-system.com/resonanz/alchemy/preview \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Das ist wirklich sehr wichtig und nachhaltig",
    "style": "zynisch"
  }'
```

---

#### `GET /resonanz/alchemy/styles`
**Übersicht aller Transmutationen**

```bash
curl https://dev.syntx-system.com/resonanz/alchemy/styles
```

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

## 📞 ENDPOINTS QUICK REFERENCE

```
════════════════════════════════════════════════════════════════════════════════════
                        SYNTX API v3.3 - ALLE ENDPOINTS (63 Tests)
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
   PUT    /resonanz/styles/{name}            Style updaten
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

📊 STATS (4)
   GET  /resonanz/stats                      Globale Statistiken
   GET  /resonanz/stats/wrapper/{name}       Wrapper-spezifische Stats
   GET  /resonanz/strom                      Field Flow Events
   GET  /resonanz/training                   Training Data Export

💬 CHAT (1)
   POST /resonanz/chat                       THE MAIN EVENT

🔀 DIFF - NEU! (1)
   POST /resonanz/chat/diff                  Wrapper-Parallelwelt-Vergleich

📼 SESSIONS - NEU! (4)
   GET  /resonanz/sessions                   Session-Liste mit Pagination
   GET  /resonanz/session/{id}               Vollständiger Field-Flow
   GET  /resonanz/session/{id}/replay        Replay-Parameter

⚗️ ALCHEMY - NEU! (2)
   POST /resonanz/alchemy/preview            Live Wort-Transmutation
   GET  /resonanz/alchemy/styles             Übersicht aller Styles

════════════════════════════════════════════════════════════════════════════════════
                              TOTAL: 44 ENDPOINTS | 63 TESTS
════════════════════════════════════════════════════════════════════════════════════
```

---

## 🧪 API TESTER

```bash
# Alle 63 Tests ausführen
./api_calls_wrapper.sh https://dev.syntx-system.com

# Erwarteter Output:
# ✓ BESTANDEN:   63
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
| **Testing** | Bash + curl (63 Tests) |

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
