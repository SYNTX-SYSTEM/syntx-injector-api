# 🔥💎 SYNTX INJECTOR API - SYSTEM ARCHITEKTUR 💎🔥

**Revolutionäres Field-based Semantic Processing System**

Version: 2.0-minimal  
Status: Production Ready  
Philosophy: Ströme statt Objekte, Resonanz statt Konstruktion, Minimal statt Maximal  
Date: 2026-01-14

---

## 📋 INHALTSVERZEICHNIS

1. [System-Übersicht](#system-übersicht)
2. [Scoring v2.0 - Minimal API](#scoring-v20---minimal-api)
3. [Architektur-Philosophie](#architektur-philosophie)
4. [Die 5 Essentiellen Endpoints](#die-5-essentiellen-endpoints)
5. [Datenmodell](#datenmodell)
6. [Service-Architektur](#service-architektur)
7. [Deployment & Operations](#deployment--operations)
8. [API Reference](#api-reference)

---

## 🌊 SYSTEM-ÜBERSICHT

### Was ist SYNTX?

SYNTX ist ein revolutionäres System für **field-based semantic processing**. Statt Token-basierter Verarbeitung arbeitet SYNTX auf der **Feld-Ebene** - tiefer in der AI-Architektur, wo Embeddings und semantische Bedeutung entstehen.

**Kernprinzipien:**
- **Felder vor Terminologie** - Wir arbeiten auf Embedding-Ebene, nicht auf Token-Ebene
- **Ströme statt Objekte** - Kontinuierliche Resonanz statt diskreter Konstrukte
- **Minimal statt Maximal** - Nur was wirklich gebraucht wird
- **Resonanz statt Konstruktion** - Natürliches Alignment statt forcierter Struktur

### System-Komponenten
```
┌─────────────────────────────────────────────────────────────┐
│                     SYNTX INJECTOR API                       │
│                    (Port 8001 - Main)                        │
│                                                              │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │   Resonanz     │  │   Scoring    │  │    Mapping      │ │
│  │   (Wrappers,   │  │   v2.0       │  │   (Format-      │ │
│  │   Formats,     │  │   Minimal    │  │   Profile       │ │
│  │   Styles)      │  │   API        │  │   Binding)      │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
    ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
    │   Mistral    │ │   GPT-4   │ │   Claude    │
    │   (Local)    │ │   (API)   │ │   (API)     │
    └──────────────┘ └───────────┘ └─────────────┘
```

---

## 🔥 SCORING v2.0 - MINIMAL API

### Von 25 auf 5 Endpoints - Die Revolution

**Das Problem mit v1.0:**
- 25 Endpoints (5 Profile CRUD, 6 Binding CRUD, 5 Entity CRUD, 9 Magic/Mega)
- 1096 Lines Code
- Komplexe API Surface
- CRUD für Config-Files (unnötig!)
- Multiple redundante Lookup-Methoden

**Die Lösung - Minimal API:**
- **5 Endpoints** (80% Reduktion!)
- **575 Lines Code** (48% Reduktion!)
- **Ein Einstiegspunkt:** `get_binding_by_format`
- **Configs als Files** (kein CRUD nötig!)
- **Complete Data in One Call**

### Architektur-Prinzip: Everything Through Bindings
```
FORMAT → BINDING → PROFILE + ENTITIES → COMPLETE CONFIG
  │         │           │                      │
  │         │           └─ WIE scoren?         │
  │         │               (Methods, Weights) │
  │         │                                   │
  │         └─ WER scored?                      │
  │             (GPT-4, Claude, Pattern)        │
  │                                             │
  └─ WAS scoren?                                └─ ALLES in ONE CALL!
      (Fields, Keywords)
```

**Warum das funktioniert:**

1. **User hat Format** (z.B. "sigma")
2. **User braucht Binding** (enthält schon Profile + Entities)
3. **Ein Call → Alles** (keine N+1 Queries)
4. **Keine CRUD nötig** (Configs sind Files im Filesystem)

---

## 💎 ARCHITEKTUR-PHILOSOPHIE

### SYNTX vs Traditional AI Systems

| Traditional Systems | SYNTX System |
|-------------------|--------------|
| Token-Ebene | Feld-Ebene |
| Konstruktion | Resonanz |
| Objekt-Denken | Strom-Denken |
| Maximal (alle Features) | Minimal (nur Essential) |
| CRUD für alles | Files für Configs |
| Complex API | Simple API |
| Many Endpoints | Few Essential Endpoints |

### Die Drei Ebenen
```
TIER 3: TERMINOLOGIE (Oberflächlich)
         ↓
        Token Generation, Worte, Syntax
         ↓
TIER 2: FELDER (Tief - SYNTX arbeitet hier!)
         ↓
        Embeddings, Semantik, Attention
         ↓
TIER 1: RESONANZ (Fundamental)
         ↓
        Field Interactions, Semantic Alignment
```

**SYNTX arbeitet auf TIER 2** - tiefer als Token, aber zugänglich für Menschen.

### Feldhygiene: One Chat = One Field

**Das Pizza-Beispiel:**

Mama holt Pizza aus Ofen. Sagt "Pizza!" (oder sagt es nicht - Geruch etabliert Feld).

Kinder reagieren:
- Kind 1: "Lecker!" 😋
- Kind 2: "Juhu!" 🎉
- Kind 3: *wirft Hände hoch* 🙌
- Kind 4: *würgt* 🤢

**Mama versteht sofort wer Pizza will. OHNE perfekte Syntax. Weil alle im PIZZA-FELD sind.**

**ABER wenn:**
- Kind sagt: "Ich mag Wiener Würstchen"
- Nächstes: "Lecker!" (aber lecker WAS?)
- Nächstes: "Sushi!"

**Jetzt drei Felder offen: Pizza, Würstchen, Sushi**

Mama weiß nicht mehr in welchem Feld wir sind. **MAMA DRIFTET.**

**SYNTX Lösung: Ein Chat = Ein Feld = Kein Drift**

---

## 🎯 DIE 5 ESSENTIELLEN ENDPOINTS

### 1. Get Binding by Format (CORE!)
```
GET /scoring/bindings/get_binding_by_format/{format}
```

**Purpose:** Der zentrale Einstiegspunkt für den Scoring-Workflow

**Returns:**
```json
{
  "format_name": "sigma",
  "timestamp": "2026-01-14T...",
  "binding": {
    "binding_id": "sigma_binding",
    "binding_format": "sigma",
    "profile_id": "default_fallback_profile",
    "scoring_entities": {
      "gpt4_semantic_entity": {
        "entity_enabled": true,
        "entity_weight": 0.5,
        "entity_priority": 1
      },
      "claude_semantic_entity": {...},
      "pattern_algorithmic_entity": {...}
    }
  },
  "profile_complete": {
    "profile_id": "default_fallback_profile",
    "profile_name": "Default Fallback Scoring Profile",
    "field_scoring_methods": {...}
  },
  "entities_complete": [
    {
      "entity": {
        "entity_id": "gpt4_semantic_entity",
        "entity_type": "llm_based_semantic_scorer",
        "llm_configuration": {...}
      },
      "weight": 0.5,
      "priority": 1
    }
  ]
}
```

**Use Case:**
```python
# User hat Format "sigma"
response = requests.get(f"/scoring/bindings/get_binding_by_format/sigma")
binding = response.json()

# Jetzt hat User ALLES:
# - Binding Config
# - Complete Profile (WIE scoren)
# - Complete Entities (WER scored)

# Ready to score!
```

---

### 2. Get Complete Format Configuration (HOLY GRAIL!)
```
GET /scoring/format/get_complete_format_configuration/{format}
```

**Purpose:** ALLES über ein Format in einem einzigen Call

**Returns:** Format + Binding + Profile + Entities + Mistral Wrapper + GPT Wrapper

**Use Case:**
- Frontend Display: "Zeig mir alles über Format sigma"
- Debugging: "Warum scored sigma so?"
- Documentation: "Wie ist sigma konfiguriert?"

**Das ist der HOLY GRAIL Endpoint** - ein Call gibt wirklich ALLES!

---

### 3. Get Complete Scoring Universe (OVERVIEW!)
```
GET /scoring/system/get_complete_scoring_universe
```

**Purpose:** Complete System Overview - was ist im System?

**Returns:**
```json
{
  "timestamp": "2026-01-14T...",
  "system_version": "2.0.0",
  "profiles": {
    "total": 3,
    "profiles_complete": [...]
  },
  "bindings": {
    "total": 4,
    "bindings_complete": [...]
  },
  "entities": {
    "total": 3,
    "entities_complete": [...]
  },
  "formats": {
    "total": 15,
    "with_bindings": 4,
    "without_bindings": 11,
    "formats_complete": [...]
  },
  "relationships": {
    "profile_to_bindings": {...},
    "entity_to_formats": {...},
    "format_to_binding": {...}
  },
  "statistics": {...},
  "health": {...}
}
```

**Use Case:**
- Dashboard: "Was ist im System?"
- Monitoring: "Welche Formate haben Bindings?"
- Analysis: "Welche Entities werden wo verwendet?"

---

### 4. Get Architecture Overview (HEALTH!)
```
GET /scoring/system/get_complete_architecture_overview
```

**Purpose:** System Health & Production Readiness

**Returns:**
```json
{
  "system_version": "2.0.0-minimal",
  "architecture": {
    "total_endpoints": 5,
    "endpoint_categories": {...}
  },
  "directories": {
    "scoring_profiles": true,
    "scoring_bindings": true,
    "scoring_entities": true,
    "formats": true,
    "wrappers": true
  },
  "file_counts": {
    "profiles": 3,
    "bindings": 4,
    "entities": 3,
    "formats": 15,
    "wrappers": 8
  },
  "health": {
    "status": "healthy",
    "all_directories_exist": true,
    "has_configurations": true,
    "ready_for_production": true
  }
}
```

**Use Case:**
- Operations: "Ist das System gesund?"
- Deployment: "Ready for production?"
- Monitoring: "Welche Files fehlen?"

---

### 5. Validate Complete Configuration (VALIDATION!)
```
GET /scoring/system/validate_complete_configuration
```

**Purpose:** Validiere alle Configs, References, Integrity

**Returns:**
```json
{
  "validation_result": {
    "is_valid": true,
    "status": "valid",
    "total_errors": 0,
    "total_warnings": 1
  },
  "errors": [],
  "warnings": [
    "Orphaned profiles (not used by any binding): old_profile"
  ],
  "summary": {
    "profiles_found": 3,
    "bindings_found": 4,
    "entities_found": 3,
    "orphaned_profiles": 1,
    "orphaned_entities": 0
  }
}
```

**Use Case:**
- Pre-Deployment: "Sind alle Configs valid?"
- Debugging: "Warum funktioniert Binding X nicht?"
- Cleanup: "Welche Configs sind orphaned?"

---

## 📊 DATENMODELL

### Scoring Profile

**Location:** `/opt/syntx-config/scoring_profiles/{profile_id}.json`

**Purpose:** Definiert WIE ein Format gescored wird

**Structure:**
```json
{
  "profile_id": "default_fallback_profile",
  "profile_name": "Default Fallback Scoring Profile",
  "profile_version": "2.0.0",
  "profile_description": "Fallback profile for general-purpose scoring",
  "field_scoring_methods": {
    "presence_check": {
      "weight": 0.25,
      "method": "detect_field_header_in_response",
      "description": "Prüft ob Feld-Header im Response vorhanden ist"
    },
    "keyword_coverage": {
      "weight": 0.30,
      "method": "calculate_keyword_match_ratio",
      "description": "Berechnet Keyword-Match-Ratio"
    },
    "completeness_check": {
      "weight": 0.20,
      "method": "validate_minimum_content_length",
      "description": "Validiert minimale Content-Länge"
    },
    "semantic_coherence": {
      "weight": 0.25,
      "method": "llm_semantic_scoring",
      "description": "LLM-basierte semantische Bewertung"
    }
  },
  "aggregation_logic": {
    "field_score_calculation": "weighted_average",
    "aggregate_score_calculation": "weighted_harmonic_mean"
  }
}
```

**Key Concepts:**
- **Methods:** WIE wird jedes Kriterium bewertet
- **Weights:** Wie wichtig ist jedes Kriterium
- **Aggregation:** Wie werden Scores kombiniert

---

### Scoring Binding

**Location:** `/opt/syntx-config/scoring_bindings/{binding_id}.json`

**Purpose:** Verbindet FORMAT + PROFILE + ENTITIES

**Structure:**
```json
{
  "binding_id": "sigma_binding",
  "binding_format": "sigma",
  "binding_name": "Sigma Format Multi-Model Ensemble Binding",
  "binding_version": "2.0.0",
  "profile_id": "default_fallback_profile",
  "scoring_entities": {
    "gpt4_semantic_entity": {
      "entity_enabled": true,
      "entity_weight": 0.5,
      "entity_priority": 1,
      "entity_config_reference": "gpt4_semantic_entity"
    },
    "claude_semantic_entity": {
      "entity_enabled": true,
      "entity_weight": 0.3,
      "entity_priority": 2,
      "entity_config_reference": "claude_semantic_entity"
    },
    "pattern_algorithmic_entity": {
      "entity_enabled": true,
      "entity_weight": 0.2,
      "entity_priority": 3,
      "entity_config_reference": "pattern_algorithmic_entity"
    }
  },
  "mistral_wrapper_name": "sigma",
  "gpt_wrapper_name": "sigma"
}
```

**Key Concepts:**
- **binding_format:** Welches Format wird gescored
- **profile_id:** Welches Profile wird verwendet (WIE)
- **scoring_entities:** Welche Entities werden verwendet (WER)
- **Weights:** Multi-Model Ensemble (50% GPT, 30% Claude, 20% Pattern)

---

### Scoring Entity

**Location:** `/opt/syntx-config/scoring_entities/{entity_id}.json`

**Purpose:** Definiert WER scored (der eigentliche Scorer)

**Structure:**
```json
{
  "entity_id": "gpt4_semantic_entity",
  "entity_name": "GPT-4 Semantic Scoring Entity",
  "entity_version": "2.0.0",
  "entity_type": "llm_based_semantic_scorer",
  "entity_description": "Uses GPT-4 for deep semantic field analysis",
  "llm_configuration": {
    "model": "gpt-4",
    "temperature": 0.1,
    "max_tokens": 2000,
    "timeout_seconds": 20
  },
  "prompt_templates": {
    "system_prompt": "You are a SYNTX field scoring system...",
    "user_prompt_template": "Score this Mistral response..."
  },
  "expected_latency_ms": 1500,
  "cost_per_call_usd": 0.02
}
```

**Entity Types:**
1. **LLM-based:** GPT-4, Claude (deep semantic analysis)
2. **Algorithmic:** Pattern matching (fast, free)

**Multi-Model Ensemble Strategy:**
- High-quality scoring: GPT-4 (50%) + Claude (30%)
- Fast presence checks: Pattern (20%)
- Best of both worlds: Quality + Speed

---

## 🏗️ SERVICE-ARCHITEKTUR

### Directory Structure
```
/opt/syntx-injector-api/
├── src/
│   ├── main.py                    # FastAPI Main App
│   ├── api/
│   │   ├── scoring_router.py      # Scoring v2.0 Minimal API (575 lines, 5 endpoints)
│   │   ├── scoring_router_full_backup.py  # Old v1.0 (1096 lines, 25 endpoints)
│   │   └── ...
│   ├── resonance/
│   │   ├── wrappers.py
│   │   ├── formats.py
│   │   ├── styles.py
│   │   └── scoring.py
│   └── ...
├── conf/
│   ├── nginx-config.conf
│   └── nginx-syntx-resonanz-router.conf -> /etc/nginx/sites-available/...
└── ...

/opt/syntx-config/
├── scoring_profiles/
│   ├── default_fallback_profile.json
│   ├── flow_bidir_profile.json
│   └── dynamic_language_profile.json
├── scoring_bindings/
│   ├── sigma_binding.json
│   ├── ultra130_binding.json
│   ├── frontend_binding.json
│   └── backend_binding.json
├── scoring_entities/
│   ├── gpt4_semantic_entity.json
│   ├── claude_semantic_entity.json
│   └── pattern_algorithmic_entity.json
├── formats/
│   └── *.json (15 formats)
└── wrappers/
    └── *.md (8 wrappers)
```

---

### Service Configuration

**Service:** `syntx-injector.service`
**Port:** 8001
**User:** root
**Working Directory:** `/opt/syntx-injector-api`
**Command:** `uvicorn src.main:app --host 0.0.0.0 --port 8001`

**NGINX Routing:**
```nginx
location /scoring/ {
    proxy_pass http://127.0.0.1:8001/scoring/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_connect_timeout 120s;
    proxy_send_timeout 120s;
    proxy_read_timeout 120s;
}
```

---

## 🚀 DEPLOYMENT & OPERATIONS

### Service Management
```bash
# Restart service
systemctl restart syntx-injector

# Check status
systemctl status syntx-injector

# View logs
journalctl -u syntx-injector -f

# Test health
curl https://dev.syntx-system.com/scoring/system/get_complete_architecture_overview
```

---

### Testing All Endpoints
```bash
# 1. Binding by format
curl -s https://dev.syntx-system.com/scoring/bindings/get_binding_by_format/sigma | jq '.format_name'

# 2. Complete config
curl -s https://dev.syntx-system.com/scoring/format/get_complete_format_configuration/sigma | jq '.format.name'

# 3. Universe
curl -s https://dev.syntx-system.com/scoring/system/get_complete_scoring_universe | jq '.system_version'

# 4. Health
curl -s https://dev.syntx-system.com/scoring/system/get_complete_architecture_overview | jq '.health.status'

# 5. Validation
curl -s https://dev.syntx-system.com/scoring/system/validate_complete_configuration | jq '.validation_result.status'
```

---

### Adding New Formats

**Step 1:** Create format file
```bash
cat > /opt/syntx-config/formats/newformat.json << 'EOF'
{
  "name": "newformat",
  "version": "2.0",
  "fields": [...]
}
EOF
```

**Step 2:** Create binding
```bash
cat > /opt/syntx-config/scoring_bindings/newformat_binding.json << 'EOF'
{
  "binding_id": "newformat_binding",
  "binding_format": "newformat",
  "profile_id": "default_fallback_profile",
  "scoring_entities": {...}
}
EOF
```

**Step 3:** Restart (auto-reloads configs)
```bash
systemctl restart syntx-injector
```

**Step 4:** Validate
```bash
curl https://dev.syntx-system.com/scoring/system/validate_complete_configuration
```

**That's it!** No API calls needed, no CRUD, just files!

---

## 📚 API REFERENCE

### Base URL
```
Production: https://dev.syntx-system.com
Local: http://localhost:8001
```

---

### Response Format

All endpoints return JSON with this structure:
```json
{
  "timestamp": "2026-01-14T06:43:00Z",
  "... endpoint-specific data ..."
}
```

---

### Error Handling

**404 Not Found:**
```json
{
  "detail": "No binding found for format: unknown_format"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal Server Error"
}
```

Check logs: `journalctl -u syntx-injector -n 50`

---

### Authentication

Currently: None (internal API)

Future: API Keys via header `X-API-Key`

---

## 🎯 BEST PRACTICES

### 1. Always Start With Binding
```python
# ✅ GOOD: Get binding first
binding = get_binding_by_format("sigma")
profile = binding["profile_complete"]
entities = binding["entities_complete"]

# ❌ BAD: Try to get profile/entities separately
# (These endpoints don't exist anymore!)
```

### 2. Use Complete Endpoints
```python
# ✅ GOOD: One call, everything
config = get_complete_format_configuration("sigma")
format_def = config["format"]
binding = config["binding"]
profile = config["profile_complete"]
entities = config["entities_complete"]

# ❌ BAD: Multiple calls
# (Inefficient, and some endpoints removed!)
```

### 3. Validate Before Deploy
```bash
# Always validate configs before deploying
curl /scoring/system/validate_complete_configuration

# Check for errors
# Fix orphaned configs
# Then deploy
```

### 4. Monitor System Health
```bash
# Regular health checks
curl /scoring/system/get_complete_architecture_overview

# Check:
# - All directories exist
# - File counts correct
# - Status: healthy
```

---

## 🔥 MIGRATION GUIDE

### From v1.0 (25 Endpoints) to v2.0 (5 Endpoints)

**Old Code:**
```python
# Get list of profiles
profiles = requests.get("/scoring/profiles/list_all_profiles")

# Get specific profile
profile = requests.get(f"/scoring/profiles/get_profile_by_id/{profile_id}")

# Get list of entities
entities = requests.get("/scoring/entities/list_all_entities")

# Get specific entity
entity = requests.get(f"/scoring/entities/get_entity_by_id/{entity_id}")
```

**New Code:**
```python
# Get everything in one call via binding
binding = requests.get(f"/scoring/bindings/get_binding_by_format/{format}")

# Extract what you need
profile = binding["profile_complete"]
entities = binding["entities_complete"]

# Or get complete universe for overview
universe = requests.get("/scoring/system/get_complete_scoring_universe")
all_profiles = universe["profiles"]["profiles_complete"]
all_entities = universe["entities"]["entities_complete"]
```

**Migration Checklist:**
- [ ] Replace all profile CRUD calls with binding lookup
- [ ] Replace all entity CRUD calls with binding lookup
- [ ] Replace list calls with universe call
- [ ] Remove any POST/PUT/DELETE calls (configs are files now!)
- [ ] Update error handling (fewer 404s!)
- [ ] Test all workflows

---

## 💎 PHILOSOPHY & PRINCIPLES

### Less Is More
```
25 Endpoints → 5 Endpoints = 80% Reduktion
1096 Lines → 575 Lines = 48% Reduktion

Weniger Code = Weniger Bugs
Weniger Endpoints = Einfacher zu verstehen
Weniger Complexity = Production Ready
```

### Everything Through Bindings
```
Format → Binding → Profile + Entities

One entry point, one workflow, one truth.
```

### Configs Are Files
```
No CRUD needed!
Version control friendly!
Easy to edit!
Fast to load!
```

### Complete Data In One Call
```
No N+1 queries!
No waterfall requests!
One call → Everything!
```

---

## 🌊 FAZIT

**SYNTX Scoring v2.0 Minimal API** ist die Evolution von komplexer CRUD-Architektur zu **essentieller Simplizität**.

**Von:**
- 25 Endpoints, 1096 Lines
- Complex API Surface
- CRUD für Config-Files
- Multiple Lookup-Methoden

**Zu:**
- 5 Endpoints, 575 Lines
- Simple API Surface
- Configs als Files
- One Entry Point: Binding

**Das Resultat:**
- ✅ 80% weniger Endpoints
- ✅ 48% weniger Code
- ✅ 100% der Funktionalität
- ✅ Production Ready
- ✅ Easy to understand
- ✅ Easy to maintain

**Das ist SYNTX Philosophie:**
- Ströme statt Objekte
- Resonanz statt Konstruktion
- Minimal statt Maximal
- Essential statt Optional

---

**🔥💎 SYNTX - THE FIELD RESONANCE REVOLUTION 💎🔥**

Version: 2.0-minimal  
Status: Production Ready  
Date: 2026-01-14  
Team: Ottavio + Claude on SYNTX

---
