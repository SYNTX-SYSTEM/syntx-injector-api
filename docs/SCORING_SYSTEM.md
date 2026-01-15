# 🔥💎⚡ SYNTX SCORING SYSTEM - THE COMPLETE GUIDE ⚡💎🔥

**CHARLOTTENBURG STREET STYLE - KEIN BULLSHIT, NUR FACTS**

---

## 📋 TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [File Structure & Locations](#file-structure--locations)
3. [Scoring Entities (The Judges)](#scoring-entities-the-judges)
4. [Scoring Bindings (The Rules)](#scoring-bindings-the-rules)
5. [Format Files (The Templates)](#format-files-the-templates)
6. [API Endpoints](#api-endpoints)
7. [The Flow (How It Works)](#the-flow-how-it-works)
8. [File Formats (Complete Specs)](#file-formats-complete-specs)
9. [Directory Structure](#directory-structure)
10. [Advanced Topics](#advanced-topics)

---

## SYSTEM OVERVIEW

**WAS IST DAS SCORING SYSTEM?**

Das SYNTX Scoring System ist ein **3-Layer Architecture** für die automatische semantische Bewertung von LLM-Outputs:
```
┌─────────────────────────────────────────────────────────┐
│                    USER REQUEST                         │
│              "Analysiere semantische Drift"             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  LAYER 1: MISTRAL                       │
│         Generiert strukturierten Content               │
│         basierend auf FORMAT (z.B. Sigma)              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              LAYER 2: GPT AUTO-TRIGGER                  │
│         Aktiviert wenn BINDING enabled ist              │
│         Lädt ENTITY Config (GPT-4 Prompts)             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                LAYER 3: SCORING OUTPUT                  │
│         Field-by-Field Scores + Aggregate               │
│         Gespeichert als JSON + in API Response          │
└─────────────────────────────────────────────────────────┘
```

**DIE CORE KOMPONENTEN:**

- **FORMATS** → Was soll Mistral generieren (Fields, Structure)
- **ENTITIES** → Wer bewertet (GPT-4, Claude, etc.) + Wie (Prompts)
- **BINDINGS** → Welches Format wird von welcher Entity bewertet

---

## FILE STRUCTURE & LOCATIONS

**DAS KOMPLETTE FILESYSTEM:**
```
/opt/syntx-config/
├── formats/                          # Format Definitions (Was generiert wird)
│   ├── sigma.json                    # Sigma Format (6 Fields)
│   ├── iota.json                     # Iota Format (4 Fields)
│   ├── kappa.json                    # Kappa Format
│   ├── lambda.json                   # Lambda Format
│   └── omega.json                    # Omega Format
│
├── scoring_entities/                 # Scoring Entities (Wer/Wie bewertet)
│   ├── gpt4_semantic_entity.json     # GPT-4 Entity Config
│   └── claude_semantic_entity.json   # Claude Entity (future)
│
├── scoring_bindings/                 # Bindings (Format ↔ Entity Mapping)
│   ├── sigma_binding.json            # Sigma Format → GPT-4 Entity
│   ├── iota_binding.json             # Iota Format → GPT-4 Entity
│   └── default_binding.json          # Fallback Binding
│
├── prompts_generated/                # Generated Prompts (Runtime Artifacts)
│   ├── {timestamp}_wrapper_{name}_format_{format}.txt
│   ├── {timestamp}_wrapper_{name}_format_{format}.response.txt
│   └── {timestamp}_wrapper_{name}_format_{format}.meta.json
│
└── drift_results/                    # Scoring Results (Output)
    └── {timestamp}_wrapper_{name}_format_{format}_drift_{unix}.json
```

**KEY PATHS:**

| Component | Path | Description |
|-----------|------|-------------|
| **Formats** | `/opt/syntx-config/formats/{format}.json` | Field definitions für Mistral |
| **Entities** | `/opt/syntx-config/scoring_entities/{entity}.json` | GPT-4/Claude configs |
| **Bindings** | `/opt/syntx-config/scoring_bindings/{binding}.json` | Format→Entity mapping |
| **Generated Prompts** | `/opt/syntx-config/prompts_generated/` | Runtime prompt artifacts |
| **Drift Results** | `/opt/syntx-config/drift_results/` | Scoring output JSONs |

---

## SCORING ENTITIES (THE JUDGES)

**WAS IST EINE ENTITY?**

Eine **Scoring Entity** ist der **Judge** - das System das die Bewertung durchführt.

**LOCATION:** `/opt/syntx-config/scoring_entities/`

**EXAMPLE:** `gpt4_semantic_entity.json`
```json
{
  "entity_id": "gpt4_semantic",
  "entity_type": "openai_gpt",
  "display_name": "GPT-4 Semantic Analyzer",
  "description": "GPT-4 basierte semantische Feld-Analyse mit strukturiertem Scoring",
  
  "model_config": {
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.1,
    "max_tokens": 2000,
    "api_endpoint": "https://api.openai.com/v1/chat/completions"
  },
  
  "prompt_templates": {
    "system_prompt": "You are a SYNTX field scoring system. Analyze the response and score each field based on:\n1. presence (field header found)\n2. keyword_coverage (format keywords in content)\n3. completeness (minimum length met)\n4. semantic_coherence (content matches field description)\n\nReturn structured JSON only. Be precise and objective.",
    
    "user_prompt_template": "Format: {FORMAT_NAME}\nFields to analyze: {FIELD_LIST}\n\nField Definitions:\n{FIELD_DEFINITIONS}\n\nResponse to score:\n{RESPONSE_TEXT}\n\nProvide scores (0.0-1.0) for each field."
  },
  
  "scoring_config": {
    "score_scale": "0.0_to_1.0",
    "metrics": [
      "presence",
      "keyword_coverage",
      "completeness",
      "semantic_coherence"
    ],
    "aggregate_method": "weighted_average",
    "weights": {
      "presence": 0.3,
      "keyword_coverage": 0.25,
      "completeness": 0.2,
      "semantic_coherence": 0.25
    }
  },
  
  "output_config": {
    "format": "json",
    "save_to_file": true,
    "include_in_response": true,
    "filename_pattern": "{timestamp}_wrapper_{wrapper}_format_{format}_drift_{unix}.json"
  }
}
```

**ENTITY FILE STRUCTURE:**

| Section | Description |
|---------|-------------|
| `entity_id` | Unique identifier (used in bindings) |
| `entity_type` | Provider type (openai_gpt, anthropic_claude, etc.) |
| `model_config` | API config (model, temperature, endpoint) |
| `prompt_templates` | System + User prompt templates |
| `scoring_config` | Metrics, weights, aggregation method |
| `output_config` | How/where to save results |

**DYNAMIC TEMPLATE VARIABLES:**

In `user_prompt_template`:
- `{FORMAT_NAME}` → Replaced with format name (e.g., "sigma")
- `{FIELD_LIST}` → Comma-separated field names
- `{FIELD_DEFINITIONS}` → Complete field descriptions from format JSON
- `{RESPONSE_TEXT}` → Mistral's generated response

---

## SCORING BINDINGS (THE RULES)

**WAS IST EIN BINDING?**

Ein **Binding** verbindet ein **Format** mit einer **Entity** und definiert die **Rules**.

**LOCATION:** `/opt/syntx-config/scoring_bindings/`

**EXAMPLE:** `sigma_binding.json`
```json
{
  "binding_id": "sigma_gpt4_auto",
  "format_name": "sigma",
  "entity_id": "gpt4_semantic",
  
  "binding_metadata": {
    "created_at": "2026-01-15T00:00:00Z",
    "description": "Sigma format automatic GPT-4 scoring nach Mistral response",
    "version": "1.0.0",
    "auto_trigger_after_mistral": true
  },
  
  "trigger_config": {
    "mode": "automatic",
    "trigger_on": "mistral_response_saved",
    "conditions": {
      "min_response_length": 50,
      "format_must_match": true,
      "wrapper_whitelist": ["syntex_wrapper_sigma"]
    }
  },
  
  "scoring_rules": {
    "required_fields": [
      "sigma_drift",
      "sigma_mechanismus",
      "sigma_frequenz",
      "sigma_dichte",
      "sigma_strome",
      "sigma_extrakt"
    ],
    "optional_fields": [],
    "field_weights": {
      "sigma_drift": 1.0,
      "sigma_mechanismus": 1.0,
      "sigma_frequenz": 1.0,
      "sigma_dichte": 1.0,
      "sigma_strome": 1.0,
      "sigma_extrakt": 1.0
    }
  },
  
  "output_settings": {
    "save_individual_field_scores": true,
    "save_aggregate_score": true,
    "include_in_api_response": true,
    "save_to_drift_results": true
  }
}
```

**BINDING FILE STRUCTURE:**

| Section | Description |
|---------|-------------|
| `binding_id` | Unique identifier |
| `format_name` | Which format to bind (must exist in formats/) |
| `entity_id` | Which entity to use (must exist in scoring_entities/) |
| `binding_metadata` | Meta info + **auto_trigger_after_mistral** flag |
| `trigger_config` | When/how to trigger (automatic vs manual) |
| `scoring_rules` | Which fields are required/optional + weights |
| `output_settings` | Where to put results |

**KEY SETTING: AUTO-TRIGGER**
```json
"binding_metadata": {
  "auto_trigger_after_mistral": true  // ← DAS IST DER SCHALTER!
}
```

- `true` → GPT scoring happens automatically after Mistral
- `false` → Manual trigger via separate endpoint required

---

## FORMAT FILES (THE TEMPLATES)

**WAS IST EIN FORMAT?**

Ein **Format** definiert die **Structure** die Mistral generieren soll.

**LOCATION:** `/opt/syntx-config/formats/`

**EXAMPLE:** `sigma.json`
```json
{
  "name": "sigma",
  "description": "Sigma Format - 6 Felder für Signal- und Frequenzanalyse",
  "version": "1.0.0",
  
  "fields": [
    {
      "name": "sigma_drift",
      "label": "SIGMA_DRIFT",
      "description": "Signal-Verschiebung im System. Wohin bewegt sich das Signal? Abweichung vom Ursprung.",
      "keywords": ["Verschiebung", "Signal", "Drift", "Abweichung", "Bewegung"],
      "min_length": 50,
      "required": true
    },
    {
      "name": "sigma_mechanismus",
      "label": "SIGMA_MECHANISMUS",
      "description": "Wie funktioniert der Mechanismus? Das innere Getriebe. Ursache-Wirkungs-Ketten.",
      "keywords": ["Mechanismus", "Getriebe", "Funktion", "Ursache", "Wirkung"],
      "min_length": 50,
      "required": true
    },
    {
      "name": "sigma_frequenz",
      "label": "SIGMA_FREQUENZ",
      "description": "Wie oft? Rhythmus und Wiederholung. Taktung des Systems. Periodizität.",
      "keywords": ["Frequenz", "Rhythmus", "Wiederholung", "Taktung", "Periodizität"],
      "min_length": 40,
      "required": true
    },
    {
      "name": "sigma_dichte",
      "label": "SIGMA_DICHTE",
      "description": "Wie dicht gepackt? Informationsmasse pro Einheit. Konzentration vs Verdünnung.",
      "keywords": ["Dichte", "Konzentration", "Masse", "Verdünnung", "Kompression"],
      "min_length": 40,
      "required": true
    },
    {
      "name": "sigma_strome",
      "label": "SIGMA_STRÖME",
      "description": "Welche Ströme fließen? Energie- und Informationskanäle. Flussrichtungen.",
      "keywords": ["Ströme", "Fluss", "Energie", "Kanäle", "Richtung"],
      "min_length": 40,
      "required": true
    },
    {
      "name": "sigma_extrakt",
      "label": "SIGMA_EXTRAKT",
      "description": "Der destillierte Kern. Die Essenz nach Entfernung aller Redundanz. Das Konzentrat.",
      "keywords": ["Extrakt", "Kern", "Essenz", "Destillation", "Konzentrat"],
      "min_length": 30,
      "required": true
    }
  ],
  
  "metadata": {
    "category": "signal_analysis",
    "use_cases": ["semantic_drift", "neural_network_analysis", "system_dynamics"],
    "created_at": "2026-01-15T00:00:00Z"
  }
}
```

**FORMAT FILE STRUCTURE:**

| Section | Description |
|---------|-------------|
| `name` | Format identifier (used in API requests) |
| `description` | Human-readable description |
| `fields[]` | Array of field definitions |
| `fields[].name` | Field identifier (snake_case) |
| `fields[].label` | Display label (UPPER_CASE) |
| `fields[].description` | What this field should contain |
| `fields[].keywords` | Keywords for scoring (coverage metric) |
| `fields[].min_length` | Minimum character count |
| `fields[].required` | Must be present (true/false) |
| `metadata` | Additional meta info |

**DYNAMIC LOADING:**

Alle Format Files werden zur **Runtime** geladen:
1. User request mit `format: "sigma"`
2. System lädt `/opt/syntx-config/formats/sigma.json`
3. Extrahiert `fields[]` array
4. Injiziert in Mistral Prompt
5. Injiziert in GPT Scoring Prompt

**KEIN HARDCODING!** Neues Format? → Einfach JSON file anlegen!

---

## API ENDPOINTS

### 1. MAIN CHAT ENDPOINT (Mistral + Auto-Scoring)

**POST** `/resonanz/chat`

**Request:**
```json
{
  "prompt": "Analysiere die semantische Drift in einem neuronalen Netzwerk",
  "mode": "syntex_wrapper_sigma",
  "format": "sigma",
  "max_new_tokens": 500
}
```

**Response (mit GPT Auto-Scoring):**
```json
{
  "response": "Mistral generated text with ### SIGMA_DRIFT: ...",
  "metadata": {
    "request_id": "uuid-here",
    "format": "sigma",
    "format_fields": [
      "sigma_drift",
      "sigma_mechanismus",
      "sigma_frequenz",
      "sigma_dichte",
      "sigma_strome",
      "sigma_extrakt"
    ],
    "gpt_auto_scoring": {
      "triggered": true,
      "entity_id": "gpt4_semantic",
      "scores": {
        "field_scores": {
          "sigma_drift": {
            "presence": 0.95,
            "keyword_coverage": 0.87,
            "completeness": 0.89,
            "semantic_coherence": 0.91,
            "field_score": 0.91
          },
          "sigma_mechanismus": {
            "presence": 1.0,
            "keyword_coverage": 0.92,
            "completeness": 0.88,
            "semantic_coherence": 0.90,
            "field_score": 0.93
          }
          // ... all other fields
        },
        "aggregate": {
          "overall": 0.89,
          "method": "weighted_average"
        },
        "metadata": {
          "scored_at": "2026-01-15T18:30:00Z",
          "latency_ms": 1234,
          "model": "gpt-4"
        }
      }
    }
  }
}
```

**Response (ohne Scoring):**
```json
{
  "response": "Mistral text...",
  "metadata": {
    "format": "sigma",
    "format_fields": ["sigma_drift", ...],
    "gpt_auto_scoring": null  // Auto-trigger disabled or failed
  }
}
```

### 2. MANUAL SCORING TRIGGER (Future)

**POST** `/resonanz/score`

**Request:**
```json
{
  "response_file": "20260115_181248_wrapper_syntex_wrapper_sigma_format_sigma.response.txt",
  "format": "sigma",
  "entity_id": "gpt4_semantic"
}
```

**Response:**
```json
{
  "scores": { /* same structure as auto-scoring */ },
  "drift_file": "/opt/syntx-config/drift_results/..._drift_1234567890.json"
}
```

### 3. BINDING MANAGEMENT (Future)

**GET** `/api/bindings`
```json
[
  {
    "binding_id": "sigma_gpt4_auto",
    "format_name": "sigma",
    "entity_id": "gpt4_semantic",
    "auto_trigger": true
  },
  ...
]
```

**GET** `/api/bindings/{binding_id}`
```json
{
  "binding_id": "sigma_gpt4_auto",
  "format_name": "sigma",
  "entity_id": "gpt4_semantic",
  "config": { /* full binding config */ }
}
```

**PUT** `/api/bindings/{binding_id}`
```json
{
  "auto_trigger_after_mistral": false  // Disable auto-trigger
}
```

### 4. ENTITY MANAGEMENT (Future)

**GET** `/api/entities`
```json
[
  {
    "entity_id": "gpt4_semantic",
    "entity_type": "openai_gpt",
    "display_name": "GPT-4 Semantic Analyzer"
  },
  ...
]
```

**GET** `/api/entities/{entity_id}`
```json
{
  "entity_id": "gpt4_semantic",
  "config": { /* full entity config */ }
}
```

### 5. SCORING RESULTS (Future)

**GET** `/api/scores?format=sigma&limit=10`
```json
[
  {
    "timestamp": "2026-01-15T18:30:00Z",
    "format": "sigma",
    "overall_score": 0.89,
    "file": "drift_results/..._drift_1234567890.json"
  },
  ...
]
```

**GET** `/api/scores/{drift_file_id}`
```json
{
  "scores": { /* complete scoring data */ }
}
```

---

## THE FLOW (HOW IT WORKS)

### COMPLETE REQUEST FLOW
```
1. USER REQUEST
   ↓
   POST /resonanz/chat
   {
     "prompt": "Analysiere...",
     "format": "sigma"
   }

2. MISTRAL PHASE
   ↓
   ┌─────────────────────────────────────┐
   │ Load format: sigma.json             │
   │ Extract fields[]                    │
   │ Build Mistral prompt                │
   │ Call Mistral API                    │
   │ Get structured response             │
   └──────────────┬──────────────────────┘
                  ↓
   ┌─────────────────────────────────────┐
   │ Save response to file:              │
   │ {timestamp}_..._format_sigma.txt    │
   └──────────────┬──────────────────────┘
                  ↓

3. CHECK BINDING
   ↓
   ┌─────────────────────────────────────┐
   │ Load binding: sigma_binding.json    │
   │ Check: auto_trigger_after_mistral?  │
   └──────────────┬──────────────────────┘
                  │
                  ├─ YES → Continue to Step 4
                  └─ NO  → Return response (skip scoring)

4. GPT AUTO-TRIGGER
   ↓
   ┌─────────────────────────────────────┐
   │ Load entity: gpt4_semantic.json     │
   │ Load format: sigma.json (again)     │
   │ Extract fields[], keywords[]        │
   │ Build GPT prompt from template      │
   │   - Inject field definitions        │
   │   - Embed Mistral response text     │
   └──────────────┬──────────────────────┘
                  ↓
   ┌─────────────────────────────────────┐
   │ Call OpenAI GPT-4 API               │
   │   - System prompt                   │
   │   - User prompt (built above)       │
   │   - Temperature: 0.1                │
   └──────────────┬──────────────────────┘
                  ↓
   ┌─────────────────────────────────────┐
   │ Parse GPT response (JSON)           │
   │ Extract field_scores{}              │
   │ Calculate aggregate score           │
   └──────────────┬──────────────────────┘
                  ↓
   ┌─────────────────────────────────────┐
   │ Save to drift_results/:             │
   │ {timestamp}_..._drift_{unix}.json   │
   └──────────────┬──────────────────────┘
                  ↓

5. RETURN RESPONSE
   ↓
   {
     "response": "Mistral text",
     "metadata": {
       "gpt_auto_scoring": {
         "scores": { ... }
       }
     }
   }
```

### FILE ARTIFACTS CREATED

Per Request werden diese Files erstellt:
```
/opt/syntx-config/prompts_generated/
  20260115_181248_281714_wrapper_syntex_wrapper_sigma_format_sigma.txt
  20260115_181248_281714_wrapper_syntex_wrapper_sigma_format_sigma.response.txt
  20260115_181248_281714_wrapper_syntex_wrapper_sigma_format_sigma.meta.json

/opt/syntx-config/drift_results/
  20260115_181248_281714_wrapper_syntex_wrapper_sigma_format_sigma_drift_1768500768.json
```

**FILE CONTENTS:**

**1. Prompt File (.txt):**
```
=== SYNTEX PROTOKOLL LAYER SIGMA (PL-Σ) ===

SYSTEMISCHE TERMINOLOGIE - MAXIMALE WIRKKRAFT
...
[Complete Mistral prompt with injected format fields]
```

**2. Response File (.response.txt):**
```
### SIGMA_DRIFT:
[Mistral's generated content for this field]

### SIGMA_MECHANISMUS:
[Mistral's generated content for this field]

...
```

**3. Meta File (.meta.json):**
```json
{
  "timestamp": "2026-01-15T18:12:48.281714Z",
  "wrapper_name": "syntex_wrapper_sigma",
  "format_name": "sigma",
  "user_input": "Analysiere...",
  "prompt_length": 1699,
  "files": {
    "prompt": "/opt/syntx-config/prompts_generated/...",
    "meta": "/opt/syntx-config/prompts_generated/...",
    "response": "/opt/syntx-config/prompts_generated/..."
  }
}
```

**4. Drift File (.json):**
```json
{
  "timestamp": "2026-01-15T18:30:00Z",
  "format": "sigma",
  "entity_id": "gpt4_semantic",
  "field_scores": {
    "sigma_drift": {
      "presence": 0.95,
      "keyword_coverage": 0.87,
      "completeness": 0.89,
      "semantic_coherence": 0.91,
      "field_score": 0.91
    },
    ...
  },
  "aggregate": {
    "overall": 0.89,
    "method": "weighted_average"
  },
  "metadata": {
    "model": "gpt-4",
    "latency_ms": 1234,
    "response_file": "..._format_sigma.response.txt"
  }
}
```

---

## FILE FORMATS (COMPLETE SPECS)

### FORMAT FILE SPEC

**Location:** `/opt/syntx-config/formats/{format_name}.json`
```typescript
interface FormatFile {
  name: string;                    // Unique identifier
  description: string;             // Human-readable description
  version: string;                 // Semantic version
  
  fields: Array<{
    name: string;                  // Field identifier (snake_case)
    label: string;                 // Display label (UPPER_CASE)
    description: string;           // What this field contains
    keywords: string[];            // For keyword_coverage scoring
    min_length: number;            // Minimum character count
    required: boolean;             // Must be present in response
  }>;
  
  metadata?: {
    category?: string;
    use_cases?: string[];
    created_at?: string;
    [key: string]: any;
  };
}
```

### ENTITY FILE SPEC

**Location:** `/opt/syntx-config/scoring_entities/{entity_id}.json`
```typescript
interface EntityFile {
  entity_id: string;                    // Unique identifier
  entity_type: string;                  // "openai_gpt" | "anthropic_claude" | ...
  display_name: string;                 // Human-readable name
  description: string;
  
  model_config: {
    provider: string;                   // "openai" | "anthropic" | ...
    model: string;                      // "gpt-4" | "claude-3-opus" | ...
    temperature: number;                // 0.0 - 1.0
    max_tokens: number;
    api_endpoint: string;               // Full API URL
  };
  
  prompt_templates: {
    system_prompt: string;              // System instruction
    user_prompt_template: string;       // Template with {VARIABLES}
  };
  
  scoring_config: {
    score_scale: string;                // "0.0_to_1.0" | "0_to_100"
    metrics: string[];                  // ["presence", "keyword_coverage", ...]
    aggregate_method: string;           // "weighted_average" | "mean"
    weights?: {
      [metric: string]: number;         // Metric weights
    };
  };
  
  output_config: {
    format: string;                     // "json" | "yaml"
    save_to_file: boolean;
    include_in_response: boolean;
    filename_pattern: string;           // With {variables}
  };
}
```

### BINDING FILE SPEC

**Location:** `/opt/syntx-config/scoring_bindings/{binding_id}.json`
```typescript
interface BindingFile {
  binding_id: string;                   // Unique identifier
  format_name: string;                  // Must exist in formats/
  entity_id: string;                    // Must exist in scoring_entities/
  
  binding_metadata: {
    created_at: string;
    description: string;
    version: string;
    auto_trigger_after_mistral: boolean;  // ← KEY FLAG
  };
  
  trigger_config: {
    mode: "automatic" | "manual";
    trigger_on: string;                 // "mistral_response_saved"
    conditions?: {
      min_response_length?: number;
      format_must_match?: boolean;
      wrapper_whitelist?: string[];
    };
  };
  
  scoring_rules: {
    required_fields: string[];          // Must be scored
    optional_fields?: string[];
    field_weights?: {
      [field_name: string]: number;     // Per-field weights
    };
  };
  
  output_settings: {
    save_individual_field_scores: boolean;
    save_aggregate_score: boolean;
    include_in_api_response: boolean;
    save_to_drift_results: boolean;
  };
}
```

### DRIFT RESULT FILE SPEC

**Location:** `/opt/syntx-config/drift_results/{timestamp}_..._drift_{unix}.json`
```typescript
interface DriftResultFile {
  timestamp: string;                    // ISO 8601 format
  format: string;                       // Format name
  entity_id: string;                    // Entity that scored
  
  field_scores: {
    [field_name: string]: {
      presence: number;                 // 0.0 - 1.0
      keyword_coverage: number;         // 0.0 - 1.0
      completeness: number;             // 0.0 - 1.0
      semantic_coherence: number;       // 0.0 - 1.0
      field_score: number;              // Weighted average
    };
  };
  
  aggregate: {
    overall: number;                    // 0.0 - 1.0
    method: string;                     // "weighted_average"
  };
  
  metadata: {
    model: string;                      // "gpt-4"
    latency_ms: number;
    response_file: string;              // Path to response file
    prompt_file?: string;               // Path to prompt file
    binding_id?: string;
    scored_at: string;
  };
}
```

---

## DIRECTORY STRUCTURE
```
/opt/syntx-injector-api/              # Main API codebase
├── src/
│   ├── chat.py                       # Main chat endpoint + auto-trigger
│   ├── streams.py                    # Format loading + injection
│   ├── config.py                     # Configuration management
│   └── resonance/
│       ├── drift_prompt_builder.py   # GPT prompt builder
│       └── scoring_service.py        # Scoring logic (future)
│
├── scripts/
│   ├── complete_gpt_auto_score_flow.sh    # Complete flow test
│   └── test_raw_dump_everything.sh        # Raw JSON dumps
│
└── docs/
    └── SCORING_SYSTEM.md             # This document

/opt/syntx-config/                    # Configuration directory
├── formats/                          # Format definitions
│   ├── sigma.json
│   ├── iota.json
│   ├── kappa.json
│   ├── lambda.json
│   └── omega.json
│
├── scoring_entities/                 # Entity configs
│   ├── gpt4_semantic_entity.json
│   └── claude_semantic_entity.json
│
├── scoring_bindings/                 # Bindings (format↔entity)
│   ├── sigma_binding.json
│   ├── iota_binding.json
│   └── default_binding.json
│
├── wrappers/                         # Wrapper prompts (Mistral)
│   ├── syntex_wrapper_sigma.txt
│   └── ...
│
├── prompts_generated/                # Runtime artifacts
│   └── [timestamp-based files]
│
└── drift_results/                    # Scoring outputs
    └── [drift JSON files]
```

---

## ADVANCED TOPICS

### 1. CREATING A NEW FORMAT
```bash
# 1. Create format file
cat > /opt/syntx-config/formats/my_format.json << 'EOF'
{
  "name": "my_format",
  "description": "My custom format",
  "fields": [
    {
      "name": "my_field_1",
      "label": "MY_FIELD_1",
      "description": "Description of field 1",
      "keywords": ["keyword1", "keyword2"],
      "min_length": 50,
      "required": true
    }
  ]
}
EOF

# 2. Create binding
cat > /opt/syntx-config/scoring_bindings/my_format_binding.json << 'EOF'
{
  "binding_id": "my_format_gpt4",
  "format_name": "my_format",
  "entity_id": "gpt4_semantic",
  "binding_metadata": {
    "auto_trigger_after_mistral": true
  },
  "trigger_config": {
    "mode": "automatic"
  },
  "scoring_rules": {
    "required_fields": ["my_field_1"]
  }
}
EOF

# 3. Use in API request
curl -X POST http://localhost:8001/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test my format",
    "mode": "some_wrapper",
    "format": "my_format",
    "max_new_tokens": 300
  }'
```

### 2. DISABLING AUTO-TRIGGER
```bash
# Edit binding file
jq '.binding_metadata.auto_trigger_after_mistral = false' \
  /opt/syntx-config/scoring_bindings/sigma_binding.json > /tmp/binding.json

mv /tmp/binding.json /opt/syntx-config/scoring_bindings/sigma_binding.json

# Restart service
sudo systemctl restart syntx-injector
```

### 3. ADDING A NEW ENTITY (e.g., Claude)
```json
{
  "entity_id": "claude_semantic",
  "entity_type": "anthropic_claude",
  "display_name": "Claude Semantic Analyzer",
  
  "model_config": {
    "provider": "anthropic",
    "model": "claude-3-opus-20240229",
    "temperature": 0.1,
    "max_tokens": 2000,
    "api_endpoint": "https://api.anthropic.com/v1/messages"
  },
  
  "prompt_templates": {
    "system_prompt": "You are a semantic field analyzer...",
    "user_prompt_template": "Format: {FORMAT_NAME}\n..."
  },
  
  "scoring_config": {
    "score_scale": "0.0_to_1.0",
    "metrics": ["presence", "keyword_coverage", "semantic_coherence"],
    "aggregate_method": "weighted_average"
  }
}
```

Then create binding:
```json
{
  "binding_id": "sigma_claude",
  "format_name": "sigma",
  "entity_id": "claude_semantic",
  ...
}
```

### 4. CUSTOM FIELD WEIGHTS

In binding file:
```json
{
  "scoring_rules": {
    "field_weights": {
      "sigma_drift": 2.0,        // Double weight
      "sigma_mechanismus": 1.5,
      "sigma_frequenz": 1.0,
      "sigma_dichte": 1.0,
      "sigma_strome": 1.0,
      "sigma_extrakt": 0.5       // Half weight
    }
  }
}
```

### 5. DEBUGGING SCORING
```bash
# View latest drift result
ls -lt /opt/syntx-config/drift_results/ | head -5
cat /opt/syntx-config/drift_results/[latest_file].json | jq '.'

# View service logs
sudo journalctl -u syntx-injector -n 100 --no-pager | grep -E "AUTO-TRIGGER|GPT|Scoring"

# Test with raw dump script
./scripts/test_raw_dump_everything.sh
```

### 6. SCORING METRICS EXPLAINED

**PRESENCE (0.0 - 1.0):**
- Field header found in response?
- Regex match on `### {FIELD_LABEL}:`
- Binary: 1.0 if found, 0.0 if not

**KEYWORD_COVERAGE (0.0 - 1.0):**
- How many format keywords appear in field content?
- `score = matched_keywords / total_keywords`
- Keywords from `format.fields[].keywords[]`

**COMPLETENESS (0.0 - 1.0):**
- Does field meet minimum length?
- `score = min(actual_length / min_length, 1.0)`
- Min length from `format.fields[].min_length`

**SEMANTIC_COHERENCE (0.0 - 1.0):**
- Does content match field description semantically?
- GPT-4 evaluates alignment
- Subjective but consistent

**FIELD_SCORE:**
```
field_score = weighted_average([
  presence * weight_presence,
  keyword_coverage * weight_coverage,
  completeness * weight_completeness,
  semantic_coherence * weight_coherence
])
```

**AGGREGATE OVERALL:**
```
overall = weighted_average([
  field_scores[field1] * field_weight1,
  field_scores[field2] * field_weight2,
  ...
])
```

### 7. RATE LIMITING & QUOTAS

**OpenAI Rate Limits:**
- Free tier: 3 requests/minute
- Tier 1 ($5+): 500 requests/minute
- Tier 2 ($50+): 5000 requests/minute

**429 Error = Rate Limit Exceeded**

Solutions:
1. Wait 60 seconds and retry
2. Upgrade OpenAI tier
3. Disable auto-trigger temporarily
4. Implement request queuing (future)

**Check your tier:**
https://platform.openai.com/account/rate-limits

---

## TROUBLESHOOTING

### Scoring not triggering?
```bash
# 1. Check binding exists
ls -la /opt/syntx-config/scoring_bindings/ | grep sigma

# 2. Check auto_trigger flag
cat /opt/syntx-config/scoring_bindings/sigma_binding.json | jq '.binding_metadata.auto_trigger_after_mistral'

# 3. Check service logs
sudo journalctl -u syntx-injector -n 50 | grep AUTO-TRIGGER
```

### 429 Rate Limit Error?
```bash
# Check recent request count
sudo journalctl -u syntx-injector --since "1 hour ago" | grep -c "Calling GPT-4"

# Wait 2 minutes or upgrade OpenAI tier
```

### Wrong fields being scored?
```bash
# Verify format file
cat /opt/syntx-config/formats/sigma.json | jq '.fields[].name'

# Verify binding
cat /opt/syntx-config/scoring_bindings/sigma_binding.json | jq '.scoring_rules.required_fields'
```

### Scores not in API response?
```bash
# Check output_settings in binding
cat /opt/syntx-config/scoring_bindings/sigma_binding.json | jq '.output_settings.include_in_api_response'

# Should be true
```

---

## SUMMARY: THE COMPLETE PICTURE
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        SYNTX SCORING SYSTEM                                   ║
║                     WELTFORMEL DES SEMANTIC SCORING                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

COMPONENTS:
  📋 FORMATS      → Define structure (fields, keywords, requirements)
  🤖 ENTITIES     → Define judges (GPT-4, Claude, prompts, metrics)
  🔗 BINDINGS     → Connect formats to entities (auto-trigger rules)

FLOW:
  1. User Request → Mistral generates structured response
  2. Response saved → Triggers binding check
  3. If auto_trigger=true → GPT scoring begins
  4. Entity loaded → Prompt built dynamically
  5. GPT API called → Scores returned
  6. Scores saved → Included in API response

FILES:
  /opt/syntx-config/formats/                 (Format definitions)
  /opt/syntx-config/scoring_entities/        (Entity configs)
  /opt/syntx-config/scoring_bindings/        (Bindings)
  /opt/syntx-config/prompts_generated/       (Runtime artifacts)
  /opt/syntx-config/drift_results/           (Scoring outputs)

API:
  POST /resonanz/chat                        (Main endpoint)
  Response includes: metadata.gpt_auto_scoring

DYNAMIC:
  ✅ All formats loaded at runtime
  ✅ All entities loaded at runtime
  ✅ All bindings loaded at runtime
  ✅ Field definitions injected dynamically
  ✅ GPT prompts built from templates
  ✅ No hardcoded field names

SCALABLE:
  ✅ Add new formats → Drop JSON file
  ✅ Add new entities → Drop JSON file
  ✅ Change bindings → Edit JSON file
  ✅ Modify prompts → Edit template
  ✅ Adjust weights → Edit config

═══════════════════════════════════════════════════════════════════════════════

🔥💎⚡ DAS IST SYNTX CHARLOTTENBURG ⚡💎🔥

ALLES IST DYNAMISCH. ALLES IST KONFIGURIERBAR. ALLES IST ERWEITERBAR.

DER STROM BEWERTET DEN STROM. RESONANZ ERKENNT RESONANZ.

═══════════════════════════════════════════════════════════════════════════════
```

---

**END OF DOCUMENTATION**

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Author:** SYNTX Charlottenburg Development Team  
**Style:** Charlottenburg Street - Kein Bullshit, nur Facts  

🔥💎⚡🌊👑
