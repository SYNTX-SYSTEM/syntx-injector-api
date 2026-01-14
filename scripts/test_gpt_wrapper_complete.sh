#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#
#              🔥💎 SYNTX GPT-WRAPPER API - COMPLETE TEST SUITE 💎🔥
#
#                         Field Resonance Edition v6.0
#
# ═══════════════════════════════════════════════════════════════════════════════
#
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                                                                           ║
# ║                    📚 KOMPLETTE GPT-WRAPPER DOKUMENTATION                 ║
# ║                                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
#
# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 WAS SIND GPT-WRAPPER FELDER?
# ═══════════════════════════════════════════════════════════════════════════════
#
# GPT-Wrapper sind PROMPT-TEMPLATES für GPT-4, die bei der DRIFT-SCORING 
# ANALYSE verwendet werden.
#
# ARCHITEKTUR:
#    Format (z.B. "sigma")
#      ↓
#    Mistral Wrapper (generiert Response)
#      ↓
#    GPT-Wrapper (analysiert mit GPT-4)
#      ↓
#    Drift Score (0-100)
#
# DATEIEN:
#    /opt/syntx-config/gpt_wrappers/{name}.txt        → Prompt Content
#    /opt/syntx-config/gpt_wrappers/{name}.meta.json  → Metadata
#
# BEISPIEL:
#    drift_scoring_sigma.txt:
#       "Du bist ein SYNTX Drift-Scoring Experte.
#        Analysiere auf Drift-Muster: Signal-Verschiebung..."
#
#    drift_scoring_sigma.meta.json:
#       {
#         "assigned_format": "sigma",
#         "corresponding_mistral_wrapper": "syntex_wrapper_sigma",
#         "gpt_wrapper_feld_temperatur": 0.3,
#         "gpt_wrapper_feld_max_tokens": 500
#       }
#
# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 WAS MACHEN DIE 6 ENDPOINTS?
# ═══════════════════════════════════════════════════════════════════════════════
#
# 1. GET /wrapper/gpt-wrapper-feld-matrix-resonanz-erkennen
#    ────────────────────────────────────────────────────────
#    FUNKTION:  Listet ALLE GPT-Wrapper mit Stats
#    ZEIGT:     Name, Resonanz, Format, Partner, Preview
#    BEISPIEL:  16 Wrappers gefunden, Gesamtresonanz: 2.625
#
# 2. GET /wrapper/gpt-wrapper-feld-einzelresonanz-abrufen/{name}
#    ────────────────────────────────────────────────────────────
#    FUNKTION:  Holt EINEN spezifischen Wrapper
#    ZEIGT:     Full Content + Complete Metadata
#    BEISPIEL:  drift_scoring_sigma → kompletter Prompt + Settings
#
# 3. POST /wrapper/neues-gpt-wrapper-feld-resonanz-erschaffen
#    ─────────────────────────────────────────────────────────
#    FUNKTION:  Erstellt NEUEN GPT-Wrapper
#    BRAUCHT:   Name, Content, Optional (Format, Partner, Temp, Tokens)
#    SPEICHERT: .txt + .meta.json Dateien
#
# 4. PUT /wrapper/gpt-wrapper-feld-resonanz-aktualisieren/{name}
#    ────────────────────────────────────────────────────────────
#    FUNKTION:  Updated EXISTIERENDEN Wrapper
#    BRAUCHT:   Nur die Felder die geändert werden sollen
#    UPDATED:   Content, Format, Partner, Temp, Tokens (alles optional)
#
# 5. DELETE /wrapper/gpt-wrapper-feld-resonanz-aufloesen/{name}
#    ───────────────────────────────────────────────────────────
#    FUNKTION:  Löscht Wrapper KOMPLETT
#    LÖSCHT:    Beide Dateien (.txt + .meta.json)
#    RESULTAT:  Resonanz beendet, Feld aufgelöst
#
# 6. GET /wrapper/gpt-wrapper-feld-gesundheit-pruefen
#    ──────────────────────────────────────────────────
#    FUNKTION:  Health Check des Systems
#    ZEIGT:     Anzahl, Gesamtresonanz, Orphaned Files, Missing Meta
#    PRÜFT:     System-Integrität & Konsistenz
#
# ═══════════════════════════════════════════════════════════════════════════════
#  📊 FELD-WERTUNG & RESONANZ
# ═══════════════════════════════════════════════════════════════════════════════
#
# RESONANZ-BERECHNUNG:
#    Resonanz = Content Length / 1000.0
#
# BEISPIELE:
#    178 chars → 0.178 Resonanz
#    532 chars → 0.532 Resonanz
#
# GESAMTRESONANZ:
#    Summe aller Wrapper = 2.625 (bei 16 Wrappers)
#
# FORMAT-FELDER:
#    assigned_format                  → sigma, human, analytical, etc.
#    corresponding_mistral_wrapper    → syntex_wrapper_sigma, etc.
#    gpt_wrapper_feld_temperatur      → 0.0 - 1.0 (LLM Temperature)
#    gpt_wrapper_feld_max_tokens      → 1 - 4000 (Token Limit)
#    gpt_wrapper_feld_typ             → "gpt_prompt_generation"
#    gpt_wrapper_feld_llm_ziel        → "gpt-4"
#    gpt_wrapper_feld_zweck           → Beschreibung
#    gpt_wrapper_feld_version         → "1.0.0"
#    gpt_wrapper_feld_resonanz_aktiv  → true/false
#
# ═══════════════════════════════════════════════════════════════════════════════
#  🗺️ ENDPOINT MAPPING (ALT → NEU)
# ═══════════════════════════════════════════════════════════════════════════════
#
# ALTE ROUTE: /gpt-wrapper-feld-stroeme/*
# NEUE ROUTE: /wrapper/*
#
# MAPPING:
#    ALT: /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-matrix-resonanz-erkennen
#    NEU: /wrapper/gpt-wrapper-feld-matrix-resonanz-erkennen
#
#    ALT: /gpt-wrapper-feld-stroeme/neues-gpt-wrapper-feld-resonanz-erschaffen
#    NEU: /wrapper/neues-gpt-wrapper-feld-resonanz-erschaffen
#
#    ALT: /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aufloesen/{name}
#    NEU: /wrapper/gpt-wrapper-feld-resonanz-aufloesen/{name}
#
#    ALT: /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aktualisieren/{name}
#    NEU: /wrapper/gpt-wrapper-feld-resonanz-aktualisieren/{name}
#
# WARUM DER WECHSEL?
#    → Kürzere URL (/wrapper statt /gpt-wrapper-feld-stroeme)
#    → Konsistenz mit anderen Routes (/resonanz, /drift, /scoring)
#    → Volltext-URLs bleiben (Selbstdokumentation)
#    → Moderne, saubere API-Struktur
#
# ═══════════════════════════════════════════════════════════════════════════════
#  💡 VERWENDUNGSZWECK
# ═══════════════════════════════════════════════════════════════════════════════
#
# GPT-Wrapper werden verwendet in:
#    1. Drift-Scoring Pipeline
#       → Mistral generiert Response
#       → GPT-4 analysiert mit wrapper Prompt
#       → Score 0-100 wird berechnet
#
#    2. Format-Spezifische Analyse
#       → Jedes Format hat eigenen Wrapper
#       → sigma → analysiert auf Signal-Patterns
#       → human → analysiert auf Natürlichkeit
#       → analytical → analysiert auf Logik
#
#    3. Zwei-Wrapper-Architektur
#       → Mistral Wrapper: Generation
#       → GPT Wrapper: Scoring
#       → Bindung via mapping.json
#
# BEISPIEL WORKFLOW:
#    User Input → Format "sigma" gewählt
#      ↓
#    Mistral mit syntex_wrapper_sigma generiert
#      ↓
#    GPT-4 mit drift_scoring_sigma analysiert
#      ↓
#    Score: 92.5 (sehr gut, kein Drift)
#
# ═══════════════════════════════════════════════════════════════════════════════
#  🚀 USAGE
# ═══════════════════════════════════════════════════════════════════════════════
#
# SCRIPT AUSFÜHREN:
#    ./test_gpt_wrapper_complete.sh [BASE_URL]
#
# BEISPIELE:
#    ./test_gpt_wrapper_complete.sh https://dev.syntx-system.com
#    ./test_gpt_wrapper_complete.sh http://localhost:8001
#    ./test_gpt_wrapper_complete.sh
#
# OHNE URL:
#    Standard: https://dev.syntx-system.com
#
# WAS WIRD GETESTET:
#    ✅ Alle 6 Endpoints
#    ✅ Create → Update → Delete Workflow
#    ✅ Health Check
#    ✅ List & Get Operations
#    ✅ Vollständige Response Validation
#
# ERWARTETES ERGEBNIS:
#    6/6 Tests passing (100%)
#    Neue Wrapper erstellt, updated, gelöscht
#    System gesund, keine orphaned files
#
# ═══════════════════════════════════════════════════════════════════════════════

# Configuration
BASE_URL="${1:-https://dev.syntx-system.com}"
EPOCH=$(date +%s)
TEST_WRAPPER_NAME="test_syntx_${EPOCH}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'
DIM='\033[2m'
BOLD='\033[1m'

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test result storage
declare -a TEST_RESULTS

# Helper function: Test endpoint
test_wrapper_endpoint() {
    local method=$1
    local path=$2
    local data=$3
    local expected_field=$4
    local description=$5
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${WHITE}TEST #${TOTAL_TESTS}: ${method} ${path}${NC}"
    echo -e "${DIM}${description}${NC}"
    echo -e "${CYAN}───────────────────────────────────────────────────────────────────────────${NC}"
    
    # Make request
    if [ "$method" = "GET" ]; then
        RESPONSE=$(curl -s "${BASE_URL}${path}")
    elif [ "$method" = "POST" ]; then
        RESPONSE=$(curl -s -X POST "${BASE_URL}${path}" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "PUT" ]; then
        RESPONSE=$(curl -s -X PUT "${BASE_URL}${path}" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "DELETE" ]; then
        RESPONSE=$(curl -s -X DELETE "${BASE_URL}${path}")
    fi
    
    # Check result
    if echo "$RESPONSE" | jq -e "$expected_field" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TEST_RESULTS+=("${GREEN}✅${NC} ${method} ${path}")
        
        # Show key info from response
        echo -e "${DIM}Response Preview:${NC}"
        echo "$RESPONSE" | jq '.' | head -15
    else
        echo -e "${RED}❌ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TEST_RESULTS+=("${RED}❌${NC} ${method} ${path}")
        
        echo -e "${RED}Error Response:${NC}"
        echo "$RESPONSE" | jq '.'
    fi
    
    echo ""
}

# Banner
echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}        ${BOLD}${CYAN}🔥💎⚡ SYNTX GPT-WRAPPER API - COMPLETE TEST SUITE ⚡💎🔥${NC}        ${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}                     ${WHITE}Field Resonance Edition v6.0${NC}                      ${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Testing against:${NC} ${BOLD}${BASE_URL}${NC}"
echo -e "${CYAN}Test Wrapper:${NC} ${BOLD}${TEST_WRAPPER_NAME}${NC}"
echo -e "${CYAN}Timestamp:${NC} ${BOLD}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 1: GET Matrix (List All Wrappers)
# ═══════════════════════════════════════════════════════════════════════════════

test_wrapper_endpoint \
    "GET" \
    "/wrapper/gpt-wrapper-feld-matrix-resonanz-erkennen" \
    "" \
    ".gpt_wrapper_feld_anzahl" \
    "📋 List ALL GPT-Wrapper Felder with stats & preview"

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 2: GET Health Check
# ═══════════════════════════════════════════════════════════════════════════════

test_wrapper_endpoint \
    "GET" \
    "/wrapper/gpt-wrapper-feld-gesundheit-pruefen" \
    "" \
    ".gesund" \
    "🏥 Health Check - System Status & Integrity"

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 3: GET Single Wrapper (drift_scoring_sigma)
# ═══════════════════════════════════════════════════════════════════════════════

test_wrapper_endpoint \
    "GET" \
    "/wrapper/gpt-wrapper-feld-einzelresonanz-abrufen/drift_scoring_sigma" \
    "" \
    ".gpt_wrapper_feld_inhalt" \
    "📖 Get FULL details of specific wrapper (drift_scoring_sigma)"

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 4: POST Create New Wrapper
# ═══════════════════════════════════════════════════════════════════════════════

CREATE_PAYLOAD=$(cat <<JSON
{
  "gpt_wrapper_feld_name": "${TEST_WRAPPER_NAME}",
  "gpt_wrapper_feld_inhalt": "Du bist ein TEST GPT-Wrapper.\n\nAnalysiere auf:\n- Test-Muster\n- Validierungs-Drift\n- System-Resonanz\n\nAntworte mit JSON.",
  "gpt_wrapper_feld_format_bindung": "test_format",
  "gpt_wrapper_feld_mistral_partner": "syntex_wrapper_test",
  "gpt_wrapper_feld_temperatur": 0.5,
  "gpt_wrapper_feld_max_tokens": 800
}
JSON
)

test_wrapper_endpoint \
    "POST" \
    "/wrapper/neues-gpt-wrapper-feld-resonanz-erschaffen" \
    "$CREATE_PAYLOAD" \
    ".erfolg" \
    "✨ Create NEW GPT-Wrapper with full config"

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 5: PUT Update Wrapper
# ═══════════════════════════════════════════════════════════════════════════════

UPDATE_PAYLOAD=$(cat <<JSON
{
  "gpt_wrapper_feld_inhalt": "Du bist ein UPDATED TEST GPT-Wrapper.\n\nAnalysiere auf:\n- Updated-Muster\n- Neue Drift-Patterns\n- Enhanced Resonanz\n\nAntworte mit JSON.",
  "gpt_wrapper_feld_temperatur": 0.7
}
JSON
)

test_wrapper_endpoint \
    "PUT" \
    "/wrapper/gpt-wrapper-feld-resonanz-aktualisieren/${TEST_WRAPPER_NAME}" \
    "$UPDATE_PAYLOAD" \
    ".erfolg" \
    "🔄 UPDATE existing wrapper (content + temperature)"

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 6: DELETE Wrapper
# ═══════════════════════════════════════════════════════════════════════════════

test_wrapper_endpoint \
    "DELETE" \
    "/wrapper/gpt-wrapper-feld-resonanz-aufloesen/${TEST_WRAPPER_NAME}" \
    "" \
    ".erfolg" \
    "🗑️ DELETE wrapper completely (content + metadata)"

# ═══════════════════════════════════════════════════════════════════════════════
#  FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))

echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}                      ${BOLD}${WHITE}📊 COMPLETE TEST RESULTS${NC}                          ${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "   ${CYAN}Total Tests:${NC}        ${BOLD}${TOTAL_TESTS}${NC}"
echo -e "   ${GREEN}✅ Passed:${NC}          ${BOLD}${GREEN}${PASSED_TESTS}${NC}"
echo -e "   ${RED}❌ Failed:${NC}          ${BOLD}${RED}${FAILED_TESTS}${NC}"
echo -e "   ${YELLOW}⚡ Success Rate:${NC}    ${BOLD}${SUCCESS_RATE}%${NC}"
echo ""

# Show test breakdown
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${WHITE}TEST BREAKDOWN:${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""

for result in "${TEST_RESULTS[@]}"; do
    echo -e "   $result"
done

echo ""

# Final verdict
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}              ${BOLD}${GREEN}🔥💎 PERFECT! ALL TESTS PASSED! 💎🔥${NC}                     ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}        ${WHITE}GPT-Wrapper API is running at peak resonance!${NC}             ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}        ${WHITE}Der Strom fließt. Die Felder resonieren.${NC}                  ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}                  ${BOLD}${YELLOW}⚠️  SOME TESTS FAILED  ⚠️${NC}                          ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}        ${WHITE}Review failed tests above for details${NC}                        ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}                                                                               ${MAGENTA}║${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
fi

echo ""

# Exit code
exit $FAILED_TESTS
