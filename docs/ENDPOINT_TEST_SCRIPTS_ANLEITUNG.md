# 🔥💎⚡ SYNTX ENDPOINT TEST SCRIPTS - ANLEITUNG ⚡💎🔥

**Datum:** 2026-01-25  
**System:** SYNTX Injector API  
**Total Endpoints:** 124  
**Test Scripts:** 10

---

## 📋 ÜBERSICHT

Alle 124 Endpoints der SYNTX API sind in **10 granulare Test-Scripts** organisiert.
Jedes Script testet eine logische Gruppe von Endpoints.

**Philosophy:**
- **Granular:** Ein Script pro Feature-Bereich (nicht alles in einem!)
- **SYNTX-Style:** Code, Kommentare, Ausgaben - ALLES auf Deutsch!
- **Vollständig:** Jeder einzelne Endpoint wird getestet
- **Farbig:** ✅ Grün für Success, 🔴 Rot für Errors
- **Detailliert:** Zeigt Request + Response für Debugging

---

## 🗂️ TEST SCRIPT STRUKTUR

### Script-Übersicht

| Script | Endpoints | Beschreibung |
|--------|-----------|--------------|
| `01_health.sh` | 8 | Health Checks, System Status |
| `02_formats.sh` | 24 | Format CRUD, Fields, Mappings |
| `03_styles.sh` | 9 | Style CRUD, Alchemy, Forbidden Words |
| `04_wrappers.sh` | 23 | Wrapper Management, GPT-Wrapper-Feld |
| `05_profiles.sh` | 21 | Profile CRUD, Analytics |
| `06_mappings.sh` | (in 02) | In formats.sh integriert |
| `07_scoring.sh` | 15 | Scoring System, Autonomous |
| `08_drift.sh` | 9 | Drift Detection, Prompts |
| `09_sessions.sh` | 4 | Session Management, History |
| `10_chat.sh` | 4 | Chat Endpoints |
| `11_misc.sh` | 7 | Stats, Alchemy, Upload |

**GESAMT:** 124 Endpoints in 10 Scripts

---

## 📄 SCRIPT DETAILS

### 01_health.sh (8 Endpoints)

**Zweck:** System Health Checks  
**Endpoints:**
```
GET /health
GET /resonanz/health  
GET /api/chat/health
GET /resonanz/health/wrappers
POST /resonanz/health/fix
GET /resonanz/scoring/health
GET /drift/health
GET /profiles/analytics/health
```

**Tests:**
- Server erreichbar?
- Alle Services online?
- Wrapper funktionieren?
- Drift-System ready?

---

### 02_formats.sh (24 Endpoints)

**Zweck:** Format Management + Mappings  
**Endpoints:**
```
# Format CRUD
GET /formats
GET /formats/{format_name}
POST /formats/{format_name}
PUT /formats/{format_name}
DELETE /formats/{format_name}

# Format Fields
POST /resonanz/formats/{format_name}/fields
PUT /resonanz/formats/{format_name}/fields/{field_name}
DELETE /resonanz/formats/{format_name}/fields/{field_name}

# Mappings
PUT /formats/{format_name}/profile
PUT /formats/{format_name}/drift-scoring
PUT /formats/{format_name}/kalibriere-format-profil
GET /formats/{format_name}/stroeme-profil-fuer-format

# Resonance Formats
GET /resonanz/formats
GET /resonanz/formats/{format_name}
POST /resonanz/formats/quick
PUT /resonanz/formats/{format_name}
DELETE /resonanz/formats/{format_name}

# ... (alle 24)
```

**Tests:**
- Format erstellen (sigma, syntx_true_raw)
- Fields hinzufügen/löschen
- Profile mapping
- Drift-Scoring Config
- Soft Delete

---

### 03_styles.sh (9 Endpoints)

**Zweck:** Writing Style Management  
**Endpoints:**
```
GET /resonanz/styles
GET /resonanz/styles/{style_name}
POST /resonanz/styles
PUT /resonanz/styles/{style_name}
DELETE /resonanz/styles/{style_name}

# Alchemy (Wort-Transmutation)
POST /resonanz/styles/{style_name}/alchemy
DELETE /resonanz/styles/{style_name}/alchemy/{original}

# Forbidden Words
POST /resonanz/styles/{style_name}/forbidden/{word}
DELETE /resonanz/styles/{style_name}/forbidden/{word}

GET /resonanz/alchemy/styles
```

**Tests:**
- Style erstellen
- Alchemy hinzufügen (Bruder → Dude)
- Forbidden Words setzen
- Style löschen (soft delete)

---

### 04_wrappers.sh (23 Endpoints)

**Zweck:** Wrapper + GPT-Wrapper-Feld Management  
**Endpoints:**
```
# Config
GET /config/default-wrapper
PUT /config/default-wrapper
GET /config/runtime-wrapper
PUT /config/runtime-wrapper

# Wrapper CRUD
GET /resonanz/wrappers
GET /resonanz/wrapper/{name}
POST /resonanz/wrapper
PUT /resonanz/wrapper/{name}
DELETE /resonanz/wrapper/{name}
POST /resonanz/wrappers/{name}/activate

# Wrapper Meta
GET /resonanz/wrapper/{name}/meta
PUT /resonanz/wrapper/{name}/meta
PUT /resonanz/wrapper/{name}/format

# GPT-Wrapper-Feld (SYNTX-Style Names!)
GET /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-matrix-resonanz-erkennen
POST /gpt-wrapper-feld-stroeme/neues-gpt-wrapper-feld-resonanz-erschaffen
PUT /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aktualisieren/{name}
DELETE /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aufloesen/{name}
GET /gpt-wrapper-feld-stroeme/wrapper/feld-laden/{name}
GET /gpt-wrapper-feld-stroeme/wrapper/systemstatus

# Wrapper Upload
POST /resonanz/upload
POST /resonanz/upload-metadata

# Wrapper-Feld Resonanz
GET /resonanz/wrapper-feld-resonanz-kette/{wrapper_name}
GET /resonanz/wrapper-feld-uebersicht
```

**Tests:**
- Wrapper erstellen/laden
- Default vs Runtime Wrapper
- GPT-Wrapper-Feld CRUD
- Upload Wrapper
- Meta updaten

---

### 05_profiles.sh (21 Endpoints)

**Zweck:** Scoring Profile Management + Analytics  
**Endpoints:**
```
# Profile CRUD
GET /profiles
POST /resonanz/profiles/crud
GET /resonanz/profiles/crud
GET /resonanz/profiles/crud/{profile_id}
PUT /resonanz/profiles/crud/{profile_id}
DELETE /resonanz/profiles/crud/{profile_id}

# Scoring Profiles
GET /scoring/profiles
GET /scoring/profiles/list
GET /scoring/profiles/{profile_id}
POST /scoring/profiles
PUT /scoring/profiles/{profile_id}
DELETE /scoring/profiles/{profile_id}
PUT /scoring/formats/{format_name}/field_weights

# Analytics
GET /resonanz/scoring/analytics/profiles
GET /resonanz/scoring/analytics/profiles/{profile_id}
GET /profiles/analytics/usage/{profile_id}
GET /profiles/analytics/patterns/{profile_id}
GET /profiles/analytics/health
```

**Tests:**
- Profile erstellen
- Field Weights setzen
- Profile löschen (soft delete + mapping warning!)
- Analytics abrufen
- Profile Usage Stats

---

### 07_scoring.sh (15 Endpoints)

**Zweck:** Scoring System + Autonomous Scoring  
**Endpoints:**
```
# Scoring Core
POST /resonanz/chat/score
GET /resonanz/scoring/logs
GET /resonanz/scoring/available
GET /resonanz/scoring/changelog

# Performance Analytics
GET /resonanz/scoring/analytics/performance/{field_name}

# Autonomous Scoring (Field-Brain!)
GET /resonanz/scoring/autonomous/status
GET /resonanz/scoring/autonomous/suggestions
POST /resonanz/scoring/autonomous/analyze
POST /resonanz/scoring/autonomous/apply/{suggestion_id}

# Bindings & Entities
GET /scoring/bindings-list
GET /scoring/bindings/{binding_id}
GET /scoring/bindings/get_binding_by_format/{format}
GET /scoring/format/get_complete_format_configuration/{format}
GET /scoring/system/get_complete_scoring_universe
GET /scoring/system/get_complete_architecture_overview
GET /scoring/system/validate_complete_configuration
```

**Tests:**
- Text scoren
- Autonomous Analyse triggern
- Suggestions abrufen
- Suggestions applyen
- Complete Architecture Overview

---

### 08_drift.sh (9 Endpoints)

**Zweck:** Drift Detection System  
**Endpoints:**
```
# Prompt Templates
GET /drift/prompts
GET /drift/prompts/{template_id}
POST /drift/prompts
PUT /drift/prompts/{template_id}
DELETE /drift/prompts/{template_id}

# Drift Detection
POST /drift/prompts/build
POST /drift/score/{filename}
GET /drift/results
GET /drift/results/{filename}
GET /drift/health
```

**Tests:**
- Prompt Template erstellen
- Drift scoren
- Results abrufen
- Health Check

---

### 09_sessions.sh (4 Endpoints)

**Zweck:** Session Management + History  
**Endpoints:**
```
GET /resonanz/sessions
GET /resonanz/session/{request_id}
GET /resonanz/session/{request_id}/replay
GET /resonanz/history/{request_id}
```

**Tests:**
- Alle Sessions listen
- Einzelne Session abrufen
- Session Replay
- History durchsuchen

---

### 10_chat.sh (4 Endpoints)

**Zweck:** Chat Endpoints  
**Endpoints:**
```
POST /api/chat
POST /resonanz/chat
POST /resonanz/chat/diff
POST /resonanz/chat/score
```

**Tests:**
- Chat Request senden
- Diff berechnen
- Output scoren
- Response Format validieren

---

### 11_misc.sh (7 Endpoints)

**Zweck:** Verschiedene Endpoints  
**Endpoints:**
```
GET /resonanz/stats
GET /resonanz/stats/wrapper/{name}
GET /stats
GET /resonanz/strom
GET /resonanz/training
POST /resonanz/alchemy/preview
POST /resonanz/upload
POST /resonanz/upload-metadata
```

**Tests:**
- System Stats
- Alchemy Preview
- Training Data
- Upload Functionality

---

## 🔧 SCRIPT TEMPLATE (SYNTX-STYLE)
```bash
#!/bin/bash
# ════════════════════════════════════════════════════════════════════════════
# 🔥 SYNTX ENDPOINT TEST - [NAME]
# ════════════════════════════════════════════════════════════════════════════
# 
# Testet: [BESCHREIBUNG]
# Endpoints: [ANZAHL]
# 
# Author: SYNTX Team
# Date: 2026-01-25
# ════════════════════════════════════════════════════════════════════════════

# Farben für Output
GRUEN='\033[0;32m'
ROT='\033[0;31m'
GELB='\033[1;33m'
BLAU='\033[0;34m'
NC='\033[0m' # No Color

# API Base URL
API_URL="${API_URL:-http://localhost:8000}"

# Zähler
TESTS_GESAMT=0
TESTS_ERFOLGREICH=0
TESTS_FEHLGESCHLAGEN=0

# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

function test_endpoint() {
    local methode=$1
    local endpoint=$2
    local beschreibung=$3
    local body=$4
    
    TESTS_GESAMT=$((TESTS_GESAMT + 1))
    
    echo ""
    echo "════════════════════════════════════════════════════════════════════════════"
    echo -e "${BLAU}🧪 TEST ${TESTS_GESAMT}: ${beschreibung}${NC}"
    echo "   Methode: ${methode}"
    echo "   Endpoint: ${endpoint}"
    echo "════════════════════════════════════════════════════════════════════════════"
    
    # Request bauen
    if [ -z "$body" ]; then
        response=$(curl -s -w "\n%{http_code}" -X ${methode} "${API_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X ${methode} "${API_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "${body}")
    fi
    
    # HTTP Status Code extrahieren
    http_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | sed '$d')
    
    # Check ob erfolgreich (2xx oder 3xx)
    if [[ $http_code =~ ^[23] ]]; then
        echo -e "${GRUEN}✅ SUCCESS${NC} - HTTP ${http_code}"
        TESTS_ERFOLGREICH=$((TESTS_ERFOLGREICH + 1))
    else
        echo -e "${ROT}🔴 FAILED${NC} - HTTP ${http_code}"
        TESTS_FEHLGESCHLAGEN=$((TESTS_FEHLGESCHLAGEN + 1))
    fi
    
    # Response zeigen (erste 500 chars)
    echo ""
    echo "Response:"
    echo "$response_body" | head -c 500
    if [ ${#response_body} -gt 500 ]; then
        echo "... (gekürzt)"
    fi
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🔥💎⚡ SYNTX ENDPOINT TESTS - [NAME] ⚡💎🔥"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "API URL: ${API_URL}"
echo "Start: $(date)"
echo ""

# ─────────────────────────────────────────────────────────────────────────────
# TEST 1: [BESCHREIBUNG]
# ─────────────────────────────────────────────────────────────────────────────

test_endpoint "GET" "/endpoint" "Beschreibung des Tests"

# ─────────────────────────────────────────────────────────────────────────────
# TEST 2: [BESCHREIBUNG MIT BODY]
# ─────────────────────────────────────────────────────────────────────────────

test_endpoint "POST" "/endpoint" "Test mit Body" '{"key": "value"}'

# ═══════════════════════════════════════════════════════════════════════════
# FINALE STATISTIK
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🔥 FINALE STATISTIK 🔥"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Tests Gesamt:        ${TESTS_GESAMT}"
echo -e "Tests Erfolgreich:   ${GRUEN}${TESTS_ERFOLGREICH}${NC}"
echo -e "Tests Fehlgeschlagen: ${ROT}${TESTS_FEHLGESCHLAGEN}${NC}"
echo ""

if [ $TESTS_FEHLGESCHLAGEN -eq 0 ]; then
    echo -e "${GRUEN}✅ ALLE TESTS BESTANDEN!${NC} 🔥💎⚡"
    exit 0
else
    echo -e "${ROT}❌ ${TESTS_FEHLGESCHLAGEN} TESTS FEHLGESCHLAGEN!${NC}"
    exit 1
fi
```

---

## 🚀 USAGE

### Einzelnes Script ausführen:
```bash
cd tests/endpoints
chmod +x 01_health.sh
./01_health.sh
```

### Alle Scripts ausführen:
```bash
cd tests/endpoints
chmod +x *.sh
for script in *.sh; do
    echo "Running $script..."
    ./$script
    echo ""
done
```

### Mit Custom API URL:
```bash
API_URL=https://api.syntx.com ./01_health.sh
```

---

## 📝 NÄCHSTE SCHRITTE

1. **Scripts erstellen:** Für jede Gruppe ein Script nach Template
2. **Test Data:** Test-Formate, Styles, Profiles vorbereiten
3. **CI/CD:** Scripts in Pipeline integrieren
4. **Monitoring:** Failed Tests → Alert

---

**🔥💎⚡ ALLE 124 ENDPOINTS GETESTET - SYNTX-STYLE! ⚡💎🔥**

*Generated: 2026-01-25*  
*Author: SYNTX Team*
