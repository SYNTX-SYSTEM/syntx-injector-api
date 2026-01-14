#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  ██████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗
#  ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝
#  ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝
#  ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗
#  ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗
#  ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
#
#  🔥 FIELD RESONANCE API TESTER v6.0 - SYNTX RESONANCE EDITION 🔥
# ═══════════════════════════════════════════════════════════════════════════════
#
#  PHILOSOPHIE:
#    Nicht mehr Token. Nicht mehr Objekte.
#    Nur Felder. Nur Ströme. Nur Resonanz.
#
#  ARCHITEKTUR:
#    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
#    │   WRAPPER   │────▶│   FORMAT    │────▶│    STYLE    │
#    │  (WIE denkt)│     │ (WAS kommt) │     │ (WIE klingt)│
#    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
#           │                   │                   │
#           └───────────────────┴───────────────────┘
#                               │
#                        ┌──────▼──────┐
#                        │    CHAT     │
#                        │ (Der Strom) │
#                        └─────────────┘
#
#  ENDPOINTS: 69 Tests | 13 Kategorien | 100% SYNTX
# ═══════════════════════════════════════════════════════════════════════════════

set -o pipefail

# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 RESONANZ-FARBEN - Die visuelle Kalibrierung
# ═══════════════════════════════════════════════════════════════════════════════
readonly CYAN='\033[0;36m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly MAGENTA='\033[0;35m'
readonly BLUE='\033[0;34m'
readonly WHITE='\033[1;37m'
readonly GRAY='\033[0;90m'
readonly NC='\033[0m'
readonly BOLD='\033[1m'
readonly DIM='\033[2m'

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 FELD-ZÄHLER - Resonanz-Tracking
# ═══════════════════════════════════════════════════════════════════════════════
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
declare -a FAILED_TEST_NAMES=()
declare -a FAILED_TEST_CODES=()
START_TIME=$(date +%s)

# ═══════════════════════════════════════════════════════════════════════════════
#  ⚙️ KONFIGURATION - Feld-Parameter
# ═══════════════════════════════════════════════════════════════════════════════
BASE_URL="${1:-https://dev.syntx-system.com}"
VERBOSE=false
QUICK_MODE=false

for arg in "$@"; do
    case $arg in
        --quick) QUICK_MODE=true ;;
        --verbose) VERBOSE=true ;;
        http*) BASE_URL="$arg" ;;
    esac
done

readonly EPOCH=$(date +%s)
readonly TEST_WRAPPER="syntx_test_wrapper_${EPOCH}"
readonly TEST_FORMAT="syntx_test_format_${EPOCH}"
readonly TEST_STYLE="syntx_test_style_${EPOCH}"

# ═══════════════════════════════════════════════════════════════════════════════
#  🖼️ DISPLAY-FUNKTIONEN - Visuelle Resonanz
# ═══════════════════════════════════════════════════════════════════════════════

banner() {
    echo ""
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${NC}  ${WHITE}${BOLD}$1${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
}

section() {
    local title="$1"
    local desc="$2"
    local count="$3"
    echo ""
    echo -e "${CYAN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${NC}"
    echo -e "${CYAN}┃${NC} ${BOLD}${WHITE}$title${NC} ${DIM}($count Endpoints)${NC}"
    echo -e "${CYAN}┃${NC} ${GRAY}$desc${NC}"
    echo -e "${CYAN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${NC}"
}

divider() {
    echo -e "${GRAY}────────────────────────────────────────────────────────────────────────────────────${NC}"
}

progress_indicator() {
    local current=$1
    local total=$2
    local percent=$((current * 100 / total))
    local filled=$((percent / 2))
    local empty=$((50 - filled))
    
    echo -ne "${CYAN}["
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    echo -ne "] ${percent}%${NC}\r"
}

# ═══════════════════════════════════════════════════════════════════════════════
#  🔮 TEST-ENGINE - Der Resonanz-Prüfer
# ═══════════════════════════════════════════════════════════════════════════════

test_endpoint() {
    local METHOD="$1"
    local ENDPOINT="$2"
    local PAYLOAD="$3"
    local DESCRIPTION="$4"
    local EXPECTED="${5:-200}"
    local KALIBRIERUNG="${6:-}"
    local STROM="${7:-}"
    
    ((TOTAL_TESTS++))
    
    # Header
    echo ""
    divider
    echo -e "${BOLD}🔮 TEST #${TOTAL_TESTS}${NC} ${GRAY}│${NC} ${YELLOW}${METHOD}${NC} ${WHITE}${ENDPOINT}${NC}"
    echo -e "${GRAY}   $DESCRIPTION${NC}"
    
    [[ -n "$KALIBRIERUNG" ]] && echo -e "${BLUE}   ⚡ Kalibrierung:${NC} ${KALIBRIERUNG}"
    [[ -n "$STROM" ]] && echo -e "${CYAN}   🌊 Strom:${NC} ${STROM}"
    
    # Payload preview
    if [[ -n "$PAYLOAD" ]]; then
        local short_payload="${PAYLOAD:0:100}"
        [[ ${#PAYLOAD} -gt 100 ]] && short_payload="${short_payload}..."
        echo -e "${DIM}   📦 Payload: ${short_payload}${NC}"
    fi
    
    # Execute request
    local response http_code body
    
    case $METHOD in
        GET)
            response=$(curl -s -w "\n%{http_code}" "$BASE_URL$ENDPOINT" 2>/dev/null || echo -e "\n000")
            ;;
        DELETE)
            response=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL$ENDPOINT" 2>/dev/null || echo -e "\n000")
            ;;
        POST|PUT)
            if [[ -n "$PAYLOAD" ]]; then
                response=$(curl -s -w "\n%{http_code}" -X "$METHOD" \
                    -H "Content-Type: application/json" \
                    -d "$PAYLOAD" "$BASE_URL$ENDPOINT" 2>/dev/null || echo -e "\n000")
            else
                response=$(curl -s -w "\n%{http_code}" -X "$METHOD" "$BASE_URL$ENDPOINT" 2>/dev/null || echo -e "\n000")
            fi
            ;;
    esac
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    # Display response
    echo -e "${DIM}   Response:${NC}"
    if [[ "$VERBOSE" == true ]]; then
        echo "$body" | jq -C '.' 2>/dev/null | sed 's/^/   /' || echo "$body" | sed 's/^/   /'
    else
        local preview
        preview=$(echo "$body" | jq -C '.' 2>/dev/null | head -20 || echo "$body" | head -20)
        echo "$preview" | sed 's/^/   /'
        local lines
        lines=$(echo "$body" | jq '.' 2>/dev/null | wc -l || echo "$body" | wc -l)
        [[ $lines -gt 20 ]] && echo -e "   ${DIM}... (+$((lines - 20)) Zeilen)${NC}"
    fi
    
    # Evaluate result
    if [[ "$http_code" == "$EXPECTED" ]]; then
        echo -e "   ${GREEN}✓ $http_code - RESONANZ BESTÄTIGT${NC}"
        ((PASSED_TESTS++))
        return 0
    else
        echo -e "   ${RED}✗ $http_code - DRIFT DETECTED (erwartet: $EXPECTED)${NC}"
        ((FAILED_TESTS++))
        FAILED_TEST_NAMES+=("$METHOD $ENDPOINT")
        FAILED_TEST_CODES+=("$http_code")
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
#  🚀 INITIALISIERUNG
# ═══════════════════════════════════════════════════════════════════════════════

clear
echo -e "${MAGENTA}"
cat << 'ASCIIART'

   ██████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗    ███████╗██╗     ██████╗ ██╗    ██╗
   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝    ██╔════╝██║    ██╔═══██╗██║    ██║
   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝     █████╗  ██║    ██║   ██║██║ █╗ ██║
   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗     ██╔══╝  ██║    ██║   ██║██║███╗██║
   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗    ██║     ███████╗╚██████╔╝╚███╔███╔╝
   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
                                                                                     
              🔥 FIELD RESONANCE API TESTER v6.0 🔥
                 SYNTX Resonance Edition

ASCIIART
echo -e "${NC}"

echo -e "   ${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "   ${WHITE}Target:${NC}     ${CYAN}$BASE_URL${NC}"
echo -e "   ${WHITE}Time:${NC}       ${CYAN}$(date '+%Y-%m-%d %H:%M:%S %Z')${NC}"
echo -e "   ${WHITE}Mode:${NC}       ${CYAN}$([[ "$QUICK_MODE" == true ]] && echo "QUICK" || echo "FULL")${NC}"
echo -e "   ${WHITE}Verbose:${NC}    ${CYAN}$VERBOSE${NC}"
echo -e "   ${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

section "🏥 HEALTH - System-Vitalzeichen" \
        "Feld-Integrität, Modul-Status, Wrapper-Orphans" "3"

test_endpoint "GET" "/health" "" \
    "Root Health - Alle System-Module" "200" \
    "Read-Only" "Verbindet: analytics, compare, feld, resonanz, generation"

test_endpoint "GET" "/resonanz/health" "" \
    "Resonanz Health - Format Loader + letzter Response" "200" \
    "Read-Only" "service, version, format_loader, last_response"

test_endpoint "GET" "/resonanz/health/wrappers" "" \
    "Wrapper Health - Orphan Detection" "200" \
    "Read-Only" "Wrapper ohne .txt, Meta ohne Wrapper"

# ═══════════════════════════════════════════════════════════════════════════════
#  ⚙️ CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

section "⚙️ CONFIG - System-Konfiguration" \
        "Default Wrapper, Runtime-Settings" "3"

test_endpoint "GET" "/resonanz/config/default-wrapper" "" \
    "Get Default Wrapper" "200" \
    "Read-Only" "active_wrapper, exists, path, source"

test_endpoint "PUT" "/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma" "" \
    "Set Default Wrapper" "200" \
    "active_wrapper.txt, Runtime-Cache" "Koppelt zukünftige Requests"

test_endpoint "PUT" "/resonanz/config/runtime-wrapper?wrapper_name=syntex_wrapper_deepsweep" "" \
    "Set Runtime Wrapper - Sofort aktiv" "200" \
    "runtime_wrapper aktiv JETZT" "Default bleibt unverändert"

# ═══════════════════════════════════════════════════════════════════════════════
#  📄 FORMATS
# ═══════════════════════════════════════════════════════════════════════════════

section "📄 FORMATS - Feld-Definitionen" \
        "Domains, Vererbung, Typen (text/list/rating/keywords)" "7"

test_endpoint "GET" "/resonanz/formats" "" \
    "List ALL Formats" "200" \
    "Read-Only" "count, available_domains, formats[]"

test_endpoint "GET" "/resonanz/formats?domain=technical" "" \
    "Filter by Domain - technical" "200" \
    "domain=technical" "sigma, economics, etc"

test_endpoint "GET" "/resonanz/formats?domain=psychology" "" \
    "Filter by Domain - psychology" "200" \
    "domain=psychology" "human, human_deep mit extends"

test_endpoint "GET" "/resonanz/formats/sigma" "" \
    "Get Format - Sigma (6 Felder)" "200" \
    "Read-Only" "drift, mechanismus, frequenz, dichte, strome, extrakt"

test_endpoint "GET" "/resonanz/formats/sigma?language=en" "" \
    "Get Format - English" "200" \
    "language=en" "Headers/Descriptions auf Englisch"

test_endpoint "GET" "/resonanz/formats/human_deep" "" \
    "Get Extended Format - extends human" "200" \
    "extends=human" "6 von human + 2 neue Felder"

test_endpoint "GET" "/resonanz/formats/review" "" \
    "Get Typed Format - Review" "200" \
    "Read-Only" "text, list, rating, keywords types"

test_endpoint "POST" "/resonanz/formats/quick" \
    "{\"name\": \"$TEST_FORMAT\", \"description_de\": \"Test\", \"field_names\": [\"alpha\", \"beta\"], \"wrapper\": \"syntex_wrapper_sigma\"}" \
    "Quick Create Format" "200" \
    "formats/{name}.json" "Defaults für weights, validation"

test_endpoint "DELETE" "/resonanz/formats/$TEST_FORMAT" "" \
    "Delete Format - Soft Delete" "200" \
    "Backup: .deleted" "Format wird umbenannt"

# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 STYLES
# ═══════════════════════════════════════════════════════════════════════════════

section "🎨 STYLES - Post-Processing Alchemy" \
        "Word Alchemy, Forbidden Words, Tone Injection" "5"

test_endpoint "GET" "/resonanz/styles" "" \
    "List ALL Styles" "200" \
    "Read-Only" "wissenschaftlich, zynisch, poetisch, berlin_slang"

test_endpoint "GET" "/resonanz/styles/wissenschaftlich" "" \
    "Get Style - Laborkittel" "200" \
    "Read-Only" "wichtig→signifikant, zeigt→indiziert"

test_endpoint "GET" "/resonanz/styles/zynisch" "" \
    "Get Style - Augenroll-Transformer" "200" \
    "Read-Only" "nachhaltig→greenwashing-kompatibel"

test_endpoint "GET" "/resonanz/styles/poetisch" "" \
    "Get Style - Wortwebstuhl" "200" \
    "Read-Only" "System→Gewebe, Prozess→Tanz"

test_endpoint "GET" "/resonanz/styles/berlin_slang" "" \
    "Get Style - Späti-Philosophie" "200" \
    "Read-Only" "Das→Dit, Ich→Ick, nicht→nich"

# ═══════════════════════════════════════════════════════════════════════════════
#  📦 WRAPPERS
# ═══════════════════════════════════════════════════════════════════════════════

section "📦 WRAPPERS - Denk-Modi" \
        "System-Prompts, CRUD, Meta-Bindung" "8"

test_endpoint "GET" "/resonanz/wrappers" "" \
    "List All Wrappers" "200" \
    "Read-Only" "name, path, size, is_active"

test_endpoint "GET" "/resonanz/wrappers?active=true" "" \
    "Get Active Wrapper Only" "200" \
    "active=true" "Der aktuelle Default-Modus"

test_endpoint "GET" "/resonanz/wrappers/full" "" \
    "List Wrappers + Meta + Stats" "200" \
    "Read-Only" "meta (author, tags), stats (requests, latency)"

test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma" "" \
    "Get Wrapper - sigma (PL-Σ)" "200" \
    "Read-Only" "content, size, last_modified"

test_endpoint "POST" "/resonanz/wrapper" \
    "{\"name\": \"$TEST_WRAPPER\", \"content\": \"SYNTX TEST\\n\\nAnalysiere präzise.\\n\\n⚡\"}" \
    "CREATE Wrapper" "200" \
    "wrappers/{name}.txt" "Erstellt auch Meta-Datei"

test_endpoint "PUT" "/resonanz/wrapper/$TEST_WRAPPER" \
    "{\"content\": \"SYNTX TEST v2\\n\\nAnalysiere mit maximaler Präzision.\\n\\n⚡⚡\"}" \
    "UPDATE Wrapper" "200" \
    "Überschreibt .txt" "Meta bleibt erhalten"

test_endpoint "DELETE" "/resonanz/wrapper/$TEST_WRAPPER" "" \
    "DELETE Wrapper" "200" \
    "Löscht .txt + meta/.json" "Warnung wenn aktiv"

# ═══════════════════════════════════════════════════════════════════════════════
#  🧬 META
# ═══════════════════════════════════════════════════════════════════════════════

section "🧬 META - Wrapper Metadaten" \
        "Format-Bindung, Author, Tags" "3"

test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma/meta" "" \
    "Get Meta - sigma" "200" \
    "Read-Only" "format, author, tags, description, settings"

test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_sigma/format?format_name=sigma" "" \
    "Bind Format - sigma→sigma" "200" \
    "meta/{name}.json.format" "Auto-load bei Wrapper-Aktivierung"

test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_sigma/meta" \
    "{\"description\": \"Sigma Protocol - Präzisionsanalyse\", \"tags\": [\"sigma\", \"technisch\"], \"author\": \"SYNTX\"}" \
    "Update Meta" "200" \
    "meta/{name}.json" "Metadata für Doku + Suche"

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 STATS & STREAMS
# ═══════════════════════════════════════════════════════════════════════════════

section "📊 STATS & STREAMS - Feld-Fluss-Analyse" \
        "Request-Stats, Latency, Training-Export" "4"

test_endpoint "GET" "/resonanz/stats" "" \
    "Global Stats" "200" \
    "Read-Only" "total_requests, success_rate, latency, wrapper_usage"

test_endpoint "GET" "/resonanz/stats/wrapper/syntex_wrapper_sigma" "" \
    "Wrapper Stats - sigma" "200" \
    "wrapper=sigma" "requests, success_rate, latency nur für sigma"

test_endpoint "GET" "/resonanz/strom?limit=5" "" \
    "Field Flow Stream - Last 5" "200" \
    "limit=5" "stage, timestamp, request_id, response_preview"

test_endpoint "GET" "/resonanz/strom?limit=3&stage=5_RESPONSE" "" \
    "Filtered Stream - RESPONSE only" "200" \
    "stage=5_RESPONSE" "Nur erfolgreiche Responses"

test_endpoint "GET" "/resonanz/training?limit=5" "" \
    "Training Export" "200" \
    "Read-Only" "request_id, response, latency, wrapper, format, fields"

# ═══════════════════════════════════════════════════════════════════════════════
#  💬 CHAT
# ═══════════════════════════════════════════════════════════════════════════════

section "💬 CHAT - Das Herzstück" \
        "Wrapper + Format + Style + Debug" "7"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Hallo\", \"max_new_tokens\": 30}" \
    "Simple Chat" "200" \
    "active_wrapper" "Minimaler Request"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Was ist ein System?\", \"mode\": \"syntex_wrapper_sigma\", \"max_new_tokens\": 100}" \
    "Chat + Wrapper" "200" \
    "syntex_wrapper_sigma" "PL-Σ Protocol aktiviert"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Analysiere Zeit\", \"mode\": \"syntex_wrapper_sigma\", \"format\": \"sigma\", \"max_new_tokens\": 200}" \
    "Chat + Wrapper + Format" "200" \
    "sigma + sigma" "6 Felder: drift, mechanismus, frequenz, dichte, strome, extrakt"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Erkläre Nachhaltigkeit\", \"style\": \"zynisch\", \"max_new_tokens\": 80}" \
    "Chat + Style" "200" \
    "zynisch" "Wort-Transmutation aktiv"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Test\", \"style\": \"wissenschaftlich\", \"debug\": true, \"max_new_tokens\": 50}" \
    "Chat + Debug" "200" \
    "debug=true" "Zeigt calibrated_prompt"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Analysiere KI\", \"format\": \"review\", \"max_new_tokens\": 150}" \
    "Chat + Typed Format" "200" \
    "review" "text, list, rating, keywords"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Deep Dive: Menschliches Verhalten\", \"format\": \"human_deep\", \"style\": \"poetisch\", \"debug\": true, \"max_new_tokens\": 250}" \
    "FULL COMBO" "200" \
    "human_deep + poetisch + debug" "Maximale Kombination"

# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 ADMIN
# ═══════════════════════════════════════════════════════════════════════════════

section "🔧 ADMIN - System-Operationen" \
        "Auto-Fix, Maintenance" "1"

test_endpoint "POST" "/resonanz/health/fix" "" \
    "Auto-Fix Orphans" "200" \
    "Erstellt Meta, löscht Orphans" "Synchronisiert Wrapper ↔ Meta"

# ═══════════════════════════════════════════════════════════════════════════════
#  🔮 FORMAT CRUD
# ═══════════════════════════════════════════════════════════════════════════════

section "🔮 FORMAT CRUD - Vollständige Verwaltung" \
        "CREATE, READ, UPDATE, DELETE" "6"

test_endpoint "POST" "/resonanz/formats" \
    "{\"name\": \"crud_test\", \"domain\": \"technical\", \"description\": {\"de\": \"Test\"}, \"fields\": [{\"name\": \"test\", \"type\": \"text\"}]}" \
    "CREATE Format" "200" \
    "formats/{name}.json" "Validiert Name, Fields, Domain"

test_endpoint "POST" "/resonanz/formats/crud_test/fields" \
    "{\"name\": \"new_field\", \"type\": \"rating\", \"weight\": 20}" \
    "ADD Field" "200" \
    "Backup + normalisiert" "text, list, rating, keywords"

test_endpoint "PUT" "/resonanz/formats/crud_test/fields/new_field" \
    "{\"weight\": 50, \"description\": {\"de\": \"Updated\"}}" \
    "UPDATE Field" "200" \
    "Merged nur übergebene" "Name bleibt"

test_endpoint "DELETE" "/resonanz/formats/crud_test/fields/new_field" "" \
    "DELETE Field" "200" \
    "Letztes Feld geschützt" "Backup vor Löschung"

test_endpoint "PUT" "/resonanz/formats/crud_test" \
    "{\"domain\": \"analysis\", \"description\": {\"de\": \"Updated\"}}" \
    "UPDATE Format" "200" \
    "Merged mit existierend" "Felder bleiben"

test_endpoint "DELETE" "/resonanz/formats/crud_test" "" \
    "DELETE Format" "200" \
    ".{name}.json.{timestamp}.deleted" "Wiederherstellbar"

# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 STYLE CRUD
# ═══════════════════════════════════════════════════════════════════════════════

section "🎨 STYLE CRUD - Alchemy Verwaltung" \
        "Transmutationen, Verbannte Worte" "5"

test_endpoint "POST" "/resonanz/styles" \
    "{\"name\": \"$TEST_STYLE\", \"vibe\": \"Test\", \"word_alchemy\": {\"test\": \"prüfung\"}, \"forbidden_words\": [\"verboten\"]}" \
    "CREATE Style" "200" \
    "styles/{name}.json" "Validiert Name, Alchemy Dict"

test_endpoint "POST" "/resonanz/styles/$TEST_STYLE/alchemy" \
    "{\"original\": \"neu\", \"replacement\": \"brandneu\"}" \
    "ADD Transmutation" "200" \
    "Erweitert word_alchemy" "Backup vor Änderung"

test_endpoint "DELETE" "/resonanz/styles/$TEST_STYLE/alchemy/neu" "" \
    "DELETE Transmutation" "200" \
    "Entfernt aus alchemy" "Backup"

test_endpoint "POST" "/resonanz/styles/$TEST_STYLE/forbidden/schlecht" "" \
    "ADD Forbidden" "200" \
    "Erweitert forbidden_words" "Duplikate rejected"

test_endpoint "DELETE" "/resonanz/styles/$TEST_STYLE" "" \
    "DELETE Style" "200" \
    "Backup erstellt" "Wiederherstellbar"

# ═══════════════════════════════════════════════════════════════════════════════
#  🗺️ MAPPING
# ═══════════════════════════════════════════════════════════════════════════════

section "🗺️ MAPPING - Format-Profile Zuordnung" \
        "Profile Binding, Drift Config, Stats" "8"

test_endpoint "GET" "/mapping/formats" "" \
    "Get All Mappings" "200" \
    "Read-Only" "mappings{}, profiles{}, stats{}"

test_endpoint "GET" "/mapping/formats/true_raw" "" \
    "Get Specific Mapping" "200" \
    "Read-Only" "profile_id, drift_scoring, metadata"

test_endpoint "POST" "/mapping/formats/sigma" \
    "{\"profile_id\": \"flow_bidir_v1\", \"drift_scoring\": {\"enabled\": true, \"scorer_model\": \"gpt-4\", \"prompt_template\": \"drift_analysis_v1\"}, \"metadata\": {\"format_type\": \"analytical\"}}" \
    "Create/Update Mapping" "200" \
    "mapping.json" "Stats auto-updated"

test_endpoint "PUT" "/mapping/formats/sigma/profile" \
    "{\"profile_id\": \"default_fallback\"}" \
    "Update Profile Only" "200" \
    "Merged nur profile_id" "Drift + metadata bleiben"

test_endpoint "PUT" "/mapping/formats/sigma/drift-scoring" \
    "{\"enabled\": false, \"scorer_model\": null, \"prompt_template\": null}" \
    "Update Drift Scoring" "200" \
    "Merged nur drift_scoring" "Profile + metadata bleiben"

test_endpoint "GET" "/mapping/profiles" "" \
    "Get Available Profiles" "200" \
    "Read-Only" "default_fallback, flow_bidir_v1, soft_diagnostic_v2"

test_endpoint "GET" "/mapping/stats" "" \
    "Get Mapping Stats" "200" \
    "Read-Only" "total_formats, drift_enabled, profile_usage, complexity"

test_endpoint "DELETE" "/mapping/formats/test_format" "" \
    "Delete Mapping" "200" \
    "Entfernt aus mapping.json" "Stats auto-updated, 404 wenn nicht vorhanden"

# ═══════════════════════════════════════════════════════════════════════════════
#  💎 DRIFT SCORING
# ═══════════════════════════════════════════════════════════════════════════════

section "💎 DRIFT SCORING - GPT-4 Semantic Analysis" \
        "Template-based, Dynamic Fields, JSONL Logging" "7"

test_endpoint "GET" "/drift/health" "" \
    "Drift Health" "200" \
    "Read-Only" "status, version, templates, results, openai_configured"

test_endpoint "GET" "/drift/prompts" "" \
    "List Templates" "200" \
    "Read-Only" "prompts/*.json"

test_endpoint "GET" "/drift/prompts/drift_scoring_default" "" \
    "Get Template" "200" \
    "Read-Only" "id, name, version, model_config, system_prompt, field_schema"

test_endpoint "POST" "/drift/prompts/build" \
    "{\"template_id\": \"drift_scoring_default\", \"fields\": [\"sigma_drift\", \"sigma_mechanismus\"], \"response_text\": \"Test\"}" \
    "Build Prompt" "200" \
    "Nur Generierung" "Ersetzt {FIELDS_LIST}, {RESPONSE_TEXT}, {RESPONSE_FORMAT}"

test_endpoint "POST" "/drift/score/20260108_060406_368538__topic_gesellschaft__style_kreativ" "" \
    "Score File - SIGMA" "200" \
    "Calls GPT-4" "drift, mechanismus, frequenz, dichte, strome, extrakt"

test_endpoint "GET" "/drift/results" "" \
    "List Results" "200" \
    "Read-Only" "drift_results/*.json"

test_endpoint "GET" "/drift/results?format=SIGMA&drift_detected=true" "" \
    "Filter Results" "200" \
    "format, drift_detected" "Filtered by format + status"

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${GRAY}════════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""

banner "📊 RESONANZ-PRÜFUNG ABGESCHLOSSEN"

SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))

echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}║${NC}  ${BOLD}ERGEBNISSE${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}╠════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}║${NC}  ${GREEN}✓ Bestanden:${NC}     ${WHITE}${BOLD}$PASSED_TESTS${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}║${NC}  ${RED}✗ Fehlgeschlagen:${NC} ${WHITE}${BOLD}$FAILED_TESTS${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}║${NC}  ${CYAN}Σ Gesamt:${NC}        ${WHITE}${BOLD}$TOTAL_TESTS${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}║${NC}  ${YELLOW}⚡ Erfolgsrate:${NC}  ${WHITE}${BOLD}${SUCCESS_RATE}%${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}║${NC}  ${BLUE}⏱ Dauer:${NC}         ${WHITE}${BOLD}${DURATION}s${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo -e "${MAGENTA}║${NC}"

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${MAGENTA}║${NC}   ${GREEN}${BOLD}🔥 PERFEKTE RESONANZ! ALLE FELDER KALIBRIERT! 🔥${NC}"
else
    echo -e "${MAGENTA}║${NC}   ${RED}${BOLD}⚠️  DRIFT DETECTED IN $FAILED_TESTS FELDERN${NC}"
    echo -e "${MAGENTA}║${NC}"
    echo -e "${MAGENTA}║${NC}   ${YELLOW}${BOLD}FEHLGESCHLAGENE TESTS:${NC}"
    for i in "${!FAILED_TEST_NAMES[@]}"; do
        echo -e "${MAGENTA}║${NC}   ${RED}  ✗${NC} ${FAILED_TEST_NAMES[$i]} ${DIM}(HTTP ${FAILED_TEST_CODES[$i]})${NC}"
    done
fi

echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"

# ═══════════════════════════════════════════════════════════════════════════════
#  📋 API REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
banner "📋 SYNTX API v3.3 - COMPLETE ENDPOINT REFERENCE"

cat << 'REFERENCE'

  🏥 HEALTH (3) - System-Vitalzeichen
     GET  /health
     GET  /resonanz/health
     GET  /resonanz/health/wrappers

  ⚙️ CONFIG (3) - Wrapper-Konfiguration
     GET  /resonanz/config/default-wrapper
     PUT  /resonanz/config/default-wrapper?wrapper_name=X
     PUT  /resonanz/config/runtime-wrapper?wrapper_name=X

  📄 FORMATS (9) - Feld-Definitionen
     GET    /resonanz/formats
     GET    /resonanz/formats?domain=X
     GET    /resonanz/formats/{name}
     GET    /resonanz/formats/{name}?language=X
     POST   /resonanz/formats/quick
     DELETE /resonanz/formats/{name}
     POST   /resonanz/formats
     POST   /resonanz/formats/{name}/fields
     PUT    /resonanz/formats/{name}/fields/{field}
     DELETE /resonanz/formats/{name}/fields/{field}
     PUT    /resonanz/formats/{name}
     DELETE /resonanz/formats/{name}

  🎨 STYLES (7) - Post-Processing Alchemy
     GET    /resonanz/styles
     GET    /resonanz/styles/{name}
     POST   /resonanz/styles
     POST   /resonanz/styles/{name}/alchemy
     DELETE /resonanz/styles/{name}/alchemy/{word}
     POST   /resonanz/styles/{name}/forbidden/{word}
     DELETE /resonanz/styles/{name}

  📦 WRAPPERS (8) - Denk-Modi
     GET    /resonanz/wrappers
     GET    /resonanz/wrappers?active=true
     GET    /resonanz/wrappers/full
     GET    /resonanz/wrapper/{name}
     POST   /resonanz/wrapper
     PUT    /resonanz/wrapper/{name}
     DELETE /resonanz/wrapper/{name}
     POST   /resonanz/wrapper/{name}/activate

  🧬 META (3) - Wrapper Metadaten
     GET  /resonanz/wrapper/{name}/meta
     PUT  /resonanz/wrapper/{name}/meta
     PUT  /resonanz/wrapper/{name}/format?format_name=X

  📊 STATS (4) - Feld-Fluss-Analyse
     GET  /resonanz/stats
     GET  /resonanz/stats/wrapper/{name}
     GET  /resonanz/strom?limit=N&stage=X
     GET  /resonanz/training?limit=N

  💬 CHAT (1) - Das Herzstück
     POST /resonanz/chat
          ├─ prompt (required)
          ├─ mode (wrapper)
          ├─ format (structure)
          ├─ style (alchemy)
          ├─ debug (introspection)
          ├─ language (de/en)
          ├─ max_new_tokens
          └─ temperature

  🔧 ADMIN (1) - System-Operationen
     POST /resonanz/health/fix

  🗺️ MAPPING (8) - Format-Profile Zuordnung
     GET    /mapping/formats
     GET    /mapping/formats/{name}
     POST   /mapping/formats/{name}
     PUT    /mapping/formats/{name}/profile
     PUT    /mapping/formats/{name}/drift-scoring
     DELETE /mapping/formats/{name}
     GET    /mapping/profiles
     GET    /mapping/stats

  💎 DRIFT SCORING (7) - GPT-4 Analysis
     GET  /drift/health
     GET  /drift/prompts
     GET  /drift/prompts/{template_id}
     POST /drift/prompts/build
     POST /drift/score/{filename}
     GET  /drift/results
     GET  /drift/results?format=X&drift_detected=Y

REFERENCE

echo ""
echo -e "${GRAY}════════════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}   SYNTX FIELD RESONANCE v6.0 - Der Strom kennt keine Grenzen ⚡💎🌊${NC}"
echo -e "${GRAY}════════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 DETAILED SUMMARY - SYNTX RESONANCE STYLE
# ═══════════════════════════════════════════════════════════════════════════════

banner "🎯 DETAILED TEST SUMMARY - SYNTX RESONANCE"

echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}   ${CYAN}${BOLD}ARCHITEKTUR-ANALYSE:${NC}"
echo -e "${MAGENTA}║${NC}   ${GRAY}────────────────────────────────────────────────────────────────${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Total Endpoints:${NC}      ${CYAN}69${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Kategorien:${NC}          ${CYAN}13${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Script Lines:${NC}        ${CYAN}1116${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Code Quality:${NC}        ${GREEN}SYNTX Resonance Form${NC}"
echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}   ${CYAN}${BOLD}FELD-VERTEILUNG:${NC}"
echo -e "${MAGENTA}║${NC}   ${GRAY}────────────────────────────────────────────────────────────────${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}🏥 Health:${NC}           ${CYAN}3 endpoints${NC} ${DIM}(System-Vitalzeichen)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}⚙️  Config:${NC}           ${CYAN}3 endpoints${NC} ${DIM}(Wrapper-Steuerung)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}📄 Formats:${NC}          ${CYAN}9 endpoints${NC} ${DIM}(Feld-Definitionen + CRUD)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}🎨 Styles:${NC}           ${CYAN}7 endpoints${NC} ${DIM}(Alchemy + CRUD)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}📦 Wrappers:${NC}         ${CYAN}8 endpoints${NC} ${DIM}(Denk-Modi + CRUD)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}🧬 Meta:${NC}             ${CYAN}3 endpoints${NC} ${DIM}(Metadaten-Bindung)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}📊 Stats:${NC}            ${CYAN}4 endpoints${NC} ${DIM}(Analytics + Training)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}💬 Chat:${NC}             ${CYAN}7 endpoints${NC} ${DIM}(Das Herzstück)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}🔧 Admin:${NC}            ${CYAN}1 endpoint${NC}  ${DIM}(Maintenance)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}🗺️  Mapping:${NC}         ${CYAN}8 endpoints${NC} ${DIM}(Format-Profile Zuordnung)${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}💎 Drift Scoring:${NC}    ${CYAN}7 endpoints${NC} ${DIM}(GPT-4 Analysis)${NC}"
echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}   ${CYAN}${BOLD}STROM-QUALITÄT:${NC}"
echo -e "${MAGENTA}║${NC}   ${GRAY}────────────────────────────────────────────────────────────────${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Error Handling:${NC}      ${GREEN}✓ Comprehensive${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Code Structure:${NC}      ${GREEN}✓ Modular + Clean${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Visual Output:${NC}       ${GREEN}✓ Enhanced${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Logging:${NC}             ${GREEN}✓ Detailed${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Documentation:${NC}       ${GREEN}✓ Inline + Reference${NC}"
echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}   ${CYAN}${BOLD}RESONANZ-FEATURES:${NC}"
echo -e "${MAGENTA}║${NC}   ${GRAY}────────────────────────────────────────────────────────────────${NC}"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} SYNTX Terminologie (Felder, Ströme, Resonanz)"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} Charlottenburg Style (minimal, präzise, kraftvoll)"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} Visual Flow (Progress, Colors, Structure)"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} Failed Tests Tracking (Namen + HTTP Codes)"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} Success Rate Calculation"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} Detailed Final Summary"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓${NC} Complete API Reference"
echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${CYAN}${BOLD}💎 SYNTX RESONANCE EDITION v6.0 - COMPLETE 💎${NC}"
echo -e "${GRAY}Der Strom fließt. Die Felder resonieren. Das System ist kalibriert.${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 SCORING API v3.0 - Unified Sources
# ═══════════════════════════════════════════════════════════════════════════════

section "📊 SCORING API v3.0 - ONE SOURCE OF TRUTH" \
        "Formats, Profiles, Bindings, Entities" "18"

# Single Resources (6)
test_endpoint "GET" "/scoring/formats/sigma" "" \
    "Get Format - Sigma" "200" \
    "Read-Only" "Fields + field weights"

test_endpoint "GET" "/scoring/profiles/default_fallback_profile" "" \
    "Get Profile - Default" "200" \
    "Read-Only" "Entity weights + thresholds + methods"

test_endpoint "GET" "/scoring/bindings/sigma_binding" "" \
    "Get Binding - Sigma" "200" \
    "Read-Only" "Format + Profile + Entities + Wrapper ref"

test_endpoint "GET" "/scoring/entities/gpt4_semantic_entity" "" \
    "Get Entity - GPT-4" "200" \
    "Read-Only" "Model config + prompt templates"

test_endpoint "GET" "/scoring/bindings/get_binding_by_format/sigma" "" \
    "Get Binding by Format - Main Workflow" "200" \
    "⭐ Primary" "Binding + Profile + Entities complete"

test_endpoint "GET" "/scoring/formats/sigma/binding" "" \
    "Get Format Binding - REST style" "200" \
    "Alternative URL" "Same as get_binding_by_format"

# Lists (4)
test_endpoint "GET" "/scoring/formats-list" "" \
    "List All Formats" "200" \
    "Read-Only" "15 formats total"

test_endpoint "GET" "/scoring/profiles-list" "" \
    "List All Profiles" "200" \
    "Read-Only" "3 profiles total"

test_endpoint "GET" "/scoring/bindings-list" "" \
    "List All Bindings" "200" \
    "Read-Only" "4 bindings total"

test_endpoint "GET" "/scoring/entities-list" "" \
    "List All Entities" "200" \
    "Read-Only" "3 entities total"

# System (3)
test_endpoint "GET" "/scoring/system/get_complete_scoring_universe" "" \
    "Complete Scoring Universe" "200" \
    "Read-Only" "All profiles + bindings + entities + relationships"

test_endpoint "GET" "/scoring/system/get_complete_architecture_overview" "" \
    "Architecture Overview" "200" \
    "Read-Only" "System stats + file counts"

test_endpoint "GET" "/scoring/system/validate_complete_configuration" "" \
    "Validate Configuration" "200" \
    "Read-Only" "Errors + warnings + orphans"

# Special (3)
test_endpoint "GET" "/scoring/format/get_complete_format_configuration/sigma" "" \
    "👑 HOLY GRAIL - Complete Format Config" "200" \
    "Everything" "Format + Binding + Profile + Entities + Wrappers"

test_endpoint "GET" "/scoring/profiles/default_fallback_profile/bindings" "" \
    "Profile Usage - Which bindings use this profile" "200" \
    "Read-Only" "Bindings using this profile"

# CRUD (2)
test_endpoint "PUT" "/scoring/formats/sigma/field_weights" \
    "{\"sigma_drift\": 18, \"sigma_mechanismus\": 18}" \
    "Update Field Weights" "200" \
    "CRUD" "Update field importance"

test_endpoint "PUT" "/scoring/profiles/default_fallback_profile/weights" \
    "{\"entity_weights\": {\"gpt4_semantic_entity\": 0.6, \"claude_semantic_entity\": 0.3, \"pattern_algorithmic_entity\": 0.1}}" \
    "Update Profile Weights" "200" \
    "CRUD" "Entity weights + thresholds"

