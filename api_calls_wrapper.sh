#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  ╔═╗╦ ╦╔╗╔╔╦╗═╗ ╦  ╔═╗╔═╗╦  ╔╦╗  ╔═╗╔═╗╔═╗╔═╗╔╗╔╔═╗╔╗╔╔═╗╔═╗
#  ╚═╗╚╦╝║║║ ║ ╔╩╦╝  ╠╣ ║╣ ║   ║║  ╠╦╝║╣ ╚═╗║ ║║║║╠═╣║║║║  ║╣ 
#  ╚═╝ ╩ ╝╚╝ ╩ ╩ ╚═  ╚  ╚═╝╩═╝═╩╝  ╩╚═╚═╝╚═╝╚═╝╝╚╝╩ ╩╝╚╝╚═╝╚═╝
# ═══════════════════════════════════════════════════════════════════════════════
#
#  🔥 SYNTX FIELD RESONANCE TESTER v5.0 - DER ULTIMATIVE STROM-PRÜFER
#
#  ══════════════════════════════════════════════════════════════════════════════
#  ARCHITEKTUR:
#  
#    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
#    │   WRAPPER   │────▶│   FORMAT    │────▶│    STYLE    │
#    │  (WIE denkt │     │ (WAS kommt  │     │ (WIE klingt │
#    │   das LLM?) │     │    raus?)   │     │     es?)    │
#    └─────────────┘     └─────────────┘     └─────────────┘
#           │                   │                   │
#           └───────────────────┴───────────────────┘
#                               │
#                        ┌──────▼──────┐
#                        │    CHAT     │
#                        │ (Der Strom) │
#                        └─────────────┘
#
#  ══════════════════════════════════════════════════════════════════════════════
#  ENDPOINTS ÜBERSICHT:
#
#  🏥 HEALTH (3)      - System-Vitalzeichen, Wrapper-Orphan-Detection
#  ⚙️ CONFIG (2)      - Default Wrapper, Runtime-Konfiguration  
#  📄 FORMATS (7)     - Feld-Definitionen, Domains, Vererbung, Typen
#  🎨 STYLES (2)      - Style Alchemy, Word Transmutation
#  📦 WRAPPERS (8)    - Denk-Modi CRUD, Meta, Aktivierung
#  📊 STATS (4)       - Feld-Fluss-Analyse, Training-Export
#  💬 CHAT (6)        - Das Herzstück mit allen Kombinationen
#  🔧 ADMIN (1)       - Auto-Fix, Maintenance
#
#  GESAMT: 33 Endpoints | 45+ Test-Szenarien
#  ══════════════════════════════════════════════════════════════════════════════
#
#  USAGE:
#    ./api_calls_wrapper.sh                    # Default: https://dev.syntx-system.com
#    ./api_calls_wrapper.sh http://localhost:8001  # Lokal testen
#    ./api_calls_wrapper.sh --quick            # Nur kritische Tests
#    ./api_calls_wrapper.sh --verbose          # Volle Response-Ausgabe
#
# ═══════════════════════════════════════════════════════════════════════════════

set -o pipefail

# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 FARB-ALCHEMIE - Der visuelle Strom
# ═══════════════════════════════════════════════════════════════════════════════
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 FELD-ZÄHLER - Resonanz-Statistik
# ═══════════════════════════════════════════════════════════════════════════════
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0
START_TIME=$(date +%s)

# ═══════════════════════════════════════════════════════════════════════════════
#  ⚙️ KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
BASE_URL="${1:-https://dev.syntx-system.com}"
VERBOSE="${2:-false}"
QUICK_MODE=false

# Parse Args
for arg in "$@"; do
    case $arg in
        --quick) QUICK_MODE=true ;;
        --verbose) VERBOSE=true ;;
        http*) BASE_URL="$arg" ;;
    esac
done

# 🧪 Temporäre Test-Ressourcen
EPOCH=$(date +%s)
TEST_WRAPPER="syntx_fieldtest_${EPOCH}"
TEST_FORMAT="syntx_formattest_${EPOCH}"

# ═══════════════════════════════════════════════════════════════════════════════
#  🖼️ DISPLAY-FUNKTIONEN - Visuelle Resonanz
# ═══════════════════════════════════════════════════════════════════════════════

# Großes Banner
banner() {
    echo ""
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${NC}  ${WHITE}${BOLD}$1${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
}

# Section Header mit Beschreibung
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

# Trennlinie
divider() {
    echo -e "${GRAY}────────────────────────────────────────────────────────────────────────────────────${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
#  🔮 TEST-ENGINE - Der Resonanz-Prüfer
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR DES TEST-AUFRUFS:
#  
#    test_endpoint "METHOD" "ENDPOINT" "PAYLOAD" "BESCHREIBUNG" "ERWARTETER_CODE"
#                     │          │          │            │               │
#                     │          │          │            │               └── HTTP Status (default: 200)
#                     │          │          │            └── Was der Test prüft
#                     │          │          └── JSON Body für POST/PUT
#                     │          └── API Pfad
#                     └── GET/POST/PUT/DELETE
#
#  FELD-FLOW:
#    1. Request senden
#    2. Response parsen
#    3. Status prüfen
#    4. Statistik updaten
#    5. Visuelle Ausgabe
#
# ═══════════════════════════════════════════════════════════════════════════════

test_endpoint() {
    local METHOD="$1"
    local ENDPOINT="$2"
    local PAYLOAD="$3"
    local DESCRIPTION="$4"
    local EXPECTED="${5:-200}"
    local KALIBRIERUNG="$6"
    local STROM_KOPPLUNG="$7"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    # Header
    echo ""
    divider
    echo -e "${BOLD}🔮 TEST #${TOTAL_TESTS}${NC} ${GRAY}│${NC} ${YELLOW}${METHOD}${NC} ${WHITE}${ENDPOINT}${NC}"
    echo -e "${GRAY}   ${DESCRIPTION}${NC}"
    
    # Kalibrierung + Strom-Kopplung anzeigen
    [ -n "$KALIBRIERUNG" ] && echo -e "${BLUE}   ⚡ Kalibrierung: ${KALIBRIERUNG}${NC}"
    [ -n "$STROM_KOPPLUNG" ] && echo -e "${CYAN}   🌊 Strom-Kopplung: ${STROM_KOPPLUNG}${NC}"
    
    # Payload anzeigen (gekürzt)
    if [ -n "$PAYLOAD" ]; then
        local SHORT_PAYLOAD=$(echo "$PAYLOAD" | head -c 100)
        [ ${#PAYLOAD} -gt 100 ] && SHORT_PAYLOAD="${SHORT_PAYLOAD}..."
        echo -e "${DIM}   📦 Payload: ${SHORT_PAYLOAD}${NC}"
    fi
    
    # Request ausführen
    local RESPONSE=""
    local HTTP_CODE=""
    
    case $METHOD in
        GET)
            RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL$ENDPOINT" 2>/dev/null)
            ;;
        DELETE)
            RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL$ENDPOINT" 2>/dev/null)
            ;;
        POST|PUT)
            if [ -n "$PAYLOAD" ]; then
                RESPONSE=$(curl -s -w "\n%{http_code}" -X $METHOD \
                    -H "Content-Type: application/json" \
                    -d "$PAYLOAD" "$BASE_URL$ENDPOINT" 2>/dev/null)
            else
                RESPONSE=$(curl -s -w "\n%{http_code}" -X $METHOD "$BASE_URL$ENDPOINT" 2>/dev/null)
            fi
            ;;
    esac
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    local BODY=$(echo "$RESPONSE" | sed '$d')
    
    # Response anzeigen
    echo -e "${DIM}   Response:${NC}"
    if [ "$VERBOSE" = true ]; then
        echo "$BODY" | jq -C '.' 2>/dev/null | sed 's/^/   /'
    else
        echo "$BODY" | jq -C '.' 2>/dev/null | head -20 | sed 's/^/   /'
        local LINES=$(echo "$BODY" | jq '.' 2>/dev/null | wc -l)
        [ "$LINES" -gt 20 ] && echo -e "   ${DIM}... (+$((LINES - 20)) Zeilen)${NC}"
    fi
    
    # Ergebnis
    if [ "$HTTP_CODE" = "$EXPECTED" ]; then
        echo -e "   ${GREEN}✓ $HTTP_CODE - RESONANZ BESTÄTIGT${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "   ${RED}✗ $HTTP_CODE - DRIFT DETECTED (erwartet: $EXPECTED)${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
#  🚀 INITIALISIERUNG - Der Strom beginnt zu fließen
# ═══════════════════════════════════════════════════════════════════════════════

clear
echo ""
echo -e "${MAGENTA}"
cat << 'ASCIIART'

   ██████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗    ███████╗██╗     ██████╗ ██╗    ██╗
   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝    ██╔════╝██║    ██╔═══██╗██║    ██║
   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝     █████╗  ██║    ██║   ██║██║ █╗ ██║
   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗     ██╔══╝  ██║    ██║   ██║██║███╗██║
   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗    ██║     ███████╗╚██████╔╝╚███╔███╔╝
   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
                                                                                     
              🔥 FIELD RESONANCE API TESTER v5.0 🔥
                 Der ultimative Strom-Prüfer

ASCIIART
echo -e "${NC}"

echo -e "   ${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "   ${WHITE}Target:${NC}     ${CYAN}$BASE_URL${NC}"
echo -e "   ${WHITE}Timestamp:${NC}  ${CYAN}$(date '+%Y-%m-%d %H:%M:%S %Z')${NC}"
echo -e "   ${WHITE}Mode:${NC}       ${CYAN}$([ "$QUICK_MODE" = true ] && echo "QUICK" || echo "FULL")${NC}"
echo -e "   ${WHITE}Verbose:${NC}    ${CYAN}$VERBOSE${NC}"
echo -e "   ${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 HEALTH ENDPOINTS - System-Vitalzeichen
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Diese Endpoints prüfen die Gesundheit des SYNTX-Systems.
#    Sie kalibrieren NICHT, sie MESSEN den aktuellen Feld-Zustand.
#
#  STRÖME:
#    /health → Alle Module (analytics, compare, feld, resonanz, generation)
#    /resonanz/health → Nur Resonanz-Subsystem + letzter Response
#    /resonanz/health/wrappers → Wrapper-Integrität + Orphan-Detection
#
# ═══════════════════════════════════════════════════════════════════════════════

section "🏥 HEALTH - System-Vitalzeichen" \
        "Prüft Feld-Integrität, Modul-Status, Wrapper-Orphans" \
        "3"

test_endpoint "GET" "/health" "" \
    "Root Health - Alle System-Module" \
    "200" \
    "Keine (Read-Only)" \
    "Verbindet: analytics, compare, feld, resonanz, generation, predictions"

test_endpoint "GET" "/resonanz/health" "" \
    "Resonanz Health - Format Loader Status + letzter Response" \
    "200" \
    "Keine (Read-Only)" \
    "Zeigt: service, version, format_loader, last_response mit latency"

test_endpoint "GET" "/resonanz/health/wrappers" "" \
    "Wrapper Health - Orphan Detection, Healthy/Orphan Split" \
    "200" \
    "Keine (Read-Only)" \
    "Prüft: Wrapper ohne .txt, Meta ohne Wrapper, Wrapper-Total"

# ═══════════════════════════════════════════════════════════════════════════════
#  ⚙️ CONFIG ENDPOINTS - System-Konfiguration
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Der Default-Wrapper bestimmt WIE das LLM denkt, wenn kein
#    expliziter mode= Parameter übergeben wird.
#
#  STRÖME:
#    GET  → Liest aktiven Wrapper aus /opt/syntx-config/active_wrapper.txt
#    PUT  → Setzt neuen Default und schreibt in active_wrapper.txt
#
# ═══════════════════════════════════════════════════════════════════════════════

section "⚙️ CONFIG - System-Konfiguration" \
        "Default Wrapper, Runtime-Settings, Fallback-Modi" \
        "2"

test_endpoint "GET" "/resonanz/config/default-wrapper" "" \
    "Get Default Wrapper - Welcher Wrapper ist aktiv?" \
    "200" \
    "Keine (Read-Only)" \
    "Liest: active_wrapper, exists, path, source (file/runtime/env)"

test_endpoint "PUT" "/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma" "" \
    "Set Default Wrapper - Wrapper aktivieren (temporär)" \
    "200" \
    "Setzt: active_wrapper.txt, Runtime-Cache" \
    "Koppelt alle zukünftigen Requests an diesen Wrapper"

# ═══════════════════════════════════════════════════════════════════════════════
#  📄 FORMAT ENDPOINTS - Feld-Definitionen
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Formate definieren WAS aus dem LLM rauskommt.
#    Sie strukturieren den Output in definierte Felder.
#
#    FORMAT = {
#      name: "sigma",
#      domain: "technical",       ← Kategorisierung
#      extends: "base_format",    ← Vererbung
#      fields: [
#        {name: "drift", type: "text", ...},      ← Freitext
#        {name: "rating", type: "rating", ...},   ← Skala 1-10
#        {name: "tags", type: "keywords", ...},   ← Komma-separiert
#        {name: "pros", type: "list", ...}        ← Bullet Points
#      ]
#    }
#
#  STRÖME:
#    GET /formats           → Liste mit Domain-Filter
#    GET /formats/{name}    → Details mit Vererbungs-Auflösung
#    POST /formats/quick    → Schnell-Erstellung
#    DELETE /formats/{name} → Soft-Delete mit Backup
#
# ═══════════════════════════════════════════════════════════════════════════════

section "📄 FORMATS - Feld-Definitionen" \
        "Domains, Vererbung (extends), Feld-Typen (text/list/rating/keywords)" \
        "7"

test_endpoint "GET" "/resonanz/formats" "" \
    "List ALL Formats - Alle verfügbaren Feld-Strukturen" \
    "200" \
    "Keine (Read-Only)" \
    "Liefert: count, available_domains, formats[] mit fields_count"

test_endpoint "GET" "/resonanz/formats?domain=technical" "" \
    "Filter by Domain - Nur technische Formate (sigma, economics)" \
    "200" \
    "Filter: domain=technical" \
    "Domains: technical, psychology, analysis, raw"

test_endpoint "GET" "/resonanz/formats?domain=psychology" "" \
    "Filter by Domain - Nur psychologische Formate (human, human_deep)" \
    "200" \
    "Filter: domain=psychology" \
    "Inkludiert: Formate mit extends (Vererbung aufgelöst)"

test_endpoint "GET" "/resonanz/formats/sigma" "" \
    "Get Format Details - Sigma (6 Felder, technisch)" \
    "200" \
    "Keine (Read-Only)" \
    "Felder: sigma_drift, sigma_mechanismus, sigma_frequenz, sigma_dichte, sigma_strome, sigma_extrakt"

test_endpoint "GET" "/resonanz/formats/sigma?language=en" "" \
    "Get Format (English) - Mehrsprachige Feld-Beschreibungen" \
    "200" \
    "Language: en" \
    "Headers/Descriptions werden auf Englisch geliefert"

test_endpoint "GET" "/resonanz/formats/human_deep" "" \
    "Get Extended Format - human_deep extends human (8 Felder)" \
    "200" \
    "Vererbung: extends=human" \
    "6 Felder von human + 2 neue (unterbewusstsein, schattenarbeit)"

test_endpoint "GET" "/resonanz/formats/review" "" \
    "Get Typed Format - Review mit allen Feld-Typen" \
    "200" \
    "Keine (Read-Only)" \
    "Typen: text (zusammenfassung), list (pro_contra), rating (bewertung), keywords (tags)"

test_endpoint "POST" "/resonanz/formats/quick" \
    "{\"name\": \"$TEST_FORMAT\", \"description_de\": \"API Test Format\", \"field_names\": [\"alpha\", \"beta\", \"gamma\"], \"wrapper\": \"syntex_wrapper_sigma\"}" \
    "Quick Create Format - Schnell-Erstellung mit Defaults" \
    "200" \
    "Schreibt: /opt/syntx-config/formats/{name}.json" \
    "Erstellt Format mit Standardwerten für weights, validation, keywords"

test_endpoint "DELETE" "/resonanz/formats/$TEST_FORMAT" "" \
    "Delete Format - Soft-Delete mit Backup" \
    "200" \
    "Backup: .{name}.json.deleted" \
    "Format wird umbenannt, nicht gelöscht"

# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 STYLE ENDPOINTS - Post-Processing Alchemy
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Styles transformieren den Output NACH der LLM-Generierung.
#    Sie ändern WIE der Text KLINGT, nicht WAS drin steht.
#
#    STYLE = {
#      name: "zynisch",
#      vibe: "Der Augenroll-Transformer",
#      word_alchemy: {               ← Wort-Transmutation
#        "wichtig": "angeblich wichtig",
#        "Experten": "selbsternannte Experten"
#      },
#      forbidden_words: ["mega"],    ← Verbannte Worte
#      tone_injection: "...",        ← Pre-LLM Injection (optional)
#      suffix: "..."                 ← Post-LLM Anhang
#    }
#
#  STRÖME:
#    GET /styles        → Liste aller Styles mit Vibe + Alchemy-Count
#    GET /styles/{name} → Vollständige Style-Definition
#
# ═══════════════════════════════════════════════════════════════════════════════

section "🎨 STYLES - Post-Processing Alchemy" \
        "Word Alchemy, Forbidden Words, Tone Injection, Suffixes" \
        "2"

test_endpoint "GET" "/resonanz/styles" "" \
    "List ALL Styles - Grimoire öffnen" \
    "200" \
    "Keine (Read-Only)" \
    "Styles: wissenschaftlich, zynisch, poetisch, berlin_slang"

test_endpoint "GET" "/resonanz/styles/wissenschaftlich" "" \
    "Get Style: wissenschaftlich - Der Laborkittel des Outputs" \
    "200" \
    "Keine (Read-Only)" \
    "Transmutiert: wichtig→signifikant, zeigt→indiziert, Problem→Problemstellung"

test_endpoint "GET" "/resonanz/styles/zynisch" "" \
    "Get Style: zynisch - Der Augenroll-Transformer" \
    "200" \
    "Keine (Read-Only)" \
    "Transmutiert: nachhaltig→greenwashing-kompatibel, innovativ→mit neuem Buzzword versehen"

test_endpoint "GET" "/resonanz/styles/poetisch" "" \
    "Get Style: poetisch - Der Wortwebstuhl" \
    "200" \
    "Keine (Read-Only)" \
    "Transmutiert: System→Gewebe, Prozess→Tanz, Daten→Tropfen im Strom"

test_endpoint "GET" "/resonanz/styles/berlin_slang" "" \
    "Get Style: berlin_slang - Späti-Philosophie um 3 Uhr nachts" \
    "200" \
    "Keine (Read-Only)" \
    "Transmutiert: Das→Dit, Ich→Ick, nicht→nich, etwas→wat"

# ═══════════════════════════════════════════════════════════════════════════════
#  📦 WRAPPER ENDPOINTS - Denk-Modi (WIE denkt das LLM?)
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Wrappers sind System-Prompts die VOR dem User-Prompt injiziert werden.
#    Sie bestimmen die DENKWEISE und TONALITÄT des LLMs.
#
#    WRAPPER-FLOW:
#      1. User sendet prompt + mode="syntex_wrapper_sigma"
#      2. System lädt /opt/syntx-config/wrappers/syntex_wrapper_sigma.txt
#      3. Wrapper-Text wird vor User-Prompt gesetzt
#      4. Kombinierter Prompt geht ans LLM
#
#  STRÖME:
#    GET    /wrappers           → Liste aller Wrapper
#    GET    /wrappers?active=true → Nur aktiver Wrapper
#    GET    /wrappers/full      → Mit Meta + Stats
#    GET    /wrapper/{name}     → Content + Metadaten
#    POST   /wrapper            → Neuen Wrapper erstellen
#    PUT    /wrapper/{name}     → Wrapper updaten
#    DELETE /wrapper/{name}     → Wrapper löschen
#    POST   /wrapper/{name}/activate → Als Default setzen
#
# ═══════════════════════════════════════════════════════════════════════════════

section "📦 WRAPPERS - Denk-Modi" \
        "System-Prompts, Content CRUD, Meta-Bindung, Aktivierung" \
        "8"

test_endpoint "GET" "/resonanz/wrappers" "" \
    "List All Wrappers - Alle verfügbaren Denk-Modi" \
    "200" \
    "Keine (Read-Only)" \
    "Liefert: name, path, size_bytes, is_active für jeden Wrapper"

test_endpoint "GET" "/resonanz/wrappers?active=true" "" \
    "Get Active Wrapper Only - Der aktuelle Default-Modus" \
    "200" \
    "Filter: active=true" \
    "Zeigt nur den Wrapper der bei mode=null verwendet wird"

test_endpoint "GET" "/resonanz/wrappers/full" "" \
    "List Wrappers + Meta + Stats - Vollständige Übersicht" \
    "200" \
    "Keine (Read-Only)" \
    "Inkludiert: meta (author, tags), stats (requests, latency)"

test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma" "" \
    "Get Wrapper Content - sigma (PL-Σ Protocol)" \
    "200" \
    "Keine (Read-Only)" \
    "Liefert: content (der System-Prompt), size, last_modified"

test_endpoint "POST" "/resonanz/wrapper" \
    "{\"name\": \"$TEST_WRAPPER\", \"content\": \"SYNTX FIELD TEST WRAPPER\\n\\nDu bist ein Test-System.\\nAnalysiere präzise und strukturiert.\\n\\nDER STROM FLIESST. ⚡\"}" \
    "CREATE Wrapper - Neuen Denk-Modus gebären" \
    "200" \
    "Schreibt: /opt/syntx-config/wrappers/{name}.txt" \
    "Erstellt auch Meta-Datei: /opt/syntx-config/wrappers/meta/{name}.json"

test_endpoint "PUT" "/resonanz/wrapper/$TEST_WRAPPER" \
    "{\"content\": \"SYNTX FIELD TEST WRAPPER v2.0\\n\\nDu bist ein verbessertes Test-System.\\nAnalysiere mit maximaler Präzision.\\n\\nRESO NANZ VERSTÄRKT. ⚡⚡\"}" \
    "UPDATE Wrapper - Denk-Modus modulieren" \
    "200" \
    "Überschreibt: .txt Datei" \
    "Meta bleibt erhalten, only content changes"

test_endpoint "DELETE" "/resonanz/wrapper/$TEST_WRAPPER" "" \
    "DELETE Wrapper - Denk-Modus freigeben" \
    "200" \
    "Löscht: .txt + meta/.json" \
    "Warnung wenn Wrapper aktiv war"

# ═══════════════════════════════════════════════════════════════════════════════
#  🧬 META ENDPOINTS - Wrapper Metadaten
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Meta-Daten sind zusätzliche Informationen über Wrapper:
#    - Format-Bindung (welches Format gehört zu welchem Wrapper)
#    - Author, Tags, Description
#    - Settings (max_tokens, temperature defaults)
#
#  STRÖME:
#    GET  /wrapper/{name}/meta  → Meta-Daten lesen
#    PUT  /wrapper/{name}/meta  → Meta-Daten updaten
#    PUT  /wrapper/{name}/format → Format-Bindung setzen
#
# ═══════════════════════════════════════════════════════════════════════════════

section "🧬 META - Wrapper Metadaten" \
        "Format-Bindung, Author, Tags, Settings" \
        "3"

test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma/meta" "" \
    "Get Meta - sigma Wrapper Metadaten" \
    "200" \
    "Keine (Read-Only)" \
    "Zeigt: format, author, tags, description, settings"

test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_sigma/format?format_name=sigma" "" \
    "Bind Format - sigma Wrapper an sigma Format binden" \
    "200" \
    "Schreibt: meta/{name}.json.format" \
    "Format wird automatisch geladen wenn Wrapper aktiviert"

test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_sigma/meta" \
    "{\"description\": \"Sigma Protocol - Technische Präzisionsanalyse für Systemarchitektur\", \"tags\": [\"sigma\", \"technisch\", \"präzise\", \"systemisch\"], \"author\": \"SYNTX Architect\"}" \
    "Update Meta - Beschreibung und Tags setzen" \
    "200" \
    "Schreibt: meta/{name}.json" \
    "Metadata für Dokumentation und Suche"

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 STATS & STREAMS - Feld-Fluss-Analyse
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Stats sammeln Metriken über alle Requests.
#    Streams zeigen den Feld-Flow für Debugging und Training.
#
#    STAGES:
#      1_INCOMING      → Request empfangen
#      2_WRAPPERS      → Wrapper geladen
#      2.5_FORMAT      → Format geladen
#      3_CALIBRATED    → Prompt kalibriert
#      4_BACKEND       → An LLM gesendet
#      5_RESPONSE      → Antwort erhalten
#      5.5_STYLE       → Style angewendet
#
#  STRÖME:
#    GET /stats              → Globale Statistiken
#    GET /stats/wrapper/{n}  → Pro-Wrapper Statistiken
#    GET /strom              → Feld-Flow Events
#    GET /training           → Training Data Export
#
# ═══════════════════════════════════════════════════════════════════════════════

section "📊 STATS & STREAMS - Feld-Fluss-Analyse" \
        "Request-Statistiken, Latency, Wrapper-Usage, Training-Export" \
        "4"

test_endpoint "GET" "/resonanz/stats" "" \
    "Global Stats - Alle Requests, Latency, Wrapper-Usage" \
    "200" \
    "Keine (Read-Only)" \
    "Zeigt: total_requests, success_rate, avg/median/min/max latency, wrapper_usage{}"

test_endpoint "GET" "/resonanz/stats/wrapper/syntex_wrapper_sigma" "" \
    "Wrapper Stats - Statistiken für sigma Wrapper" \
    "200" \
    "Filter: wrapper=sigma" \
    "Zeigt: requests, success_rate, latency stats NUR für diesen Wrapper"

test_endpoint "GET" "/resonanz/strom?limit=5" "" \
    "Field Flow Stream - Letzte 5 Feld-Events" \
    "200" \
    "Filter: limit=5" \
    "Zeigt: stage, timestamp, request_id, response_preview für jedes Event"

test_endpoint "GET" "/resonanz/strom?limit=3&stage=5_RESPONSE" "" \
    "Filtered Stream - Nur RESPONSE Stage Events" \
    "200" \
    "Filter: stage=5_RESPONSE" \
    "Nur erfolgreiche Responses, keine Zwischen-Stages"

test_endpoint "GET" "/resonanz/training?limit=5" "" \
    "Training Export - Daten für Fine-Tuning" \
    "200" \
    "Keine (Read-Only)" \
    "Format: request_id, response, latency, wrapper_chain, format, format_fields"

# ═══════════════════════════════════════════════════════════════════════════════
#  💬 CHAT ENDPOINTS - Das Herzstück
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ARCHITEKTUR:
#    Der Chat-Endpoint ist der KERN des SYNTX-Systems.
#    Hier fließen ALLE Ströme zusammen:
#
#    ┌──────────────────────────────────────────────────────────────────────┐
#    │  POST /resonanz/chat                                                 │
#    │                                                                       │
#    │  {                                                                   │
#    │    "prompt": "...",        ← Was der User fragt                     │
#    │    "mode": "wrapper",       ← WIE das LLM denkt (Wrapper)           │
#    │    "format": "sigma",       ← WAS rauskommt (Feld-Struktur)         │
#    │    "style": "zynisch",      ← WIE es klingt (Post-Processing)       │
#    │    "debug": true,           ← Zeigt calibrated_prompt               │
#    │    "language": "de",        ← Sprache für Format-Felder             │
#    │    "max_new_tokens": 500,   ← LLM Parameter                         │
#    │    "temperature": 0.7       ← Kreativität                           │
#    │  }                                                                   │
#    │                                                                       │
#    │  FLOW:                                                               │
#    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
#    │  │ STAGE 1 │→│ STAGE 2 │→│STAGE 2.5│→│ STAGE 3 │→│ STAGE 4 │        │
#    │  │INCOMING │ │ WRAPPER │ │ FORMAT  │ │CALIBRATE│ │ BACKEND │        │
#    │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
#    │       │                                               │              │
#    │       │     ┌─────────┐ ┌─────────┐                  │              │
#    │       └─────│STAGE 5.5│←│ STAGE 5 │←─────────────────┘              │
#    │             │  STYLE  │ │RESPONSE │                                  │
#    │             └─────────┘ └─────────┘                                  │
#    │                   │                                                  │
#    │                   ▼                                                  │
#    │             ┌─────────┐                                              │
#    │             │ RETURN  │ → response, metadata, field_flow,           │
#    │             └─────────┘    debug_info, style_info                   │
#    └──────────────────────────────────────────────────────────────────────┘
#
# ═══════════════════════════════════════════════════════════════════════════════

section "💬 CHAT - Das Herzstück" \
        "Alle Ströme fließen hier zusammen: Wrapper + Format + Style + Debug" \
        "6"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Hallo\", \"max_new_tokens\": 30}" \
    "Simple Chat - Nur Prompt, Default Wrapper" \
    "200" \
    "Wrapper: active_wrapper (aus config)" \
    "Minimaler Request, testet Grundfunktion"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Was ist ein System?\", \"mode\": \"syntex_wrapper_sigma\", \"max_new_tokens\": 100}" \
    "Chat + Wrapper - Expliziter Denk-Modus" \
    "200" \
    "Wrapper: syntex_wrapper_sigma" \
    "PL-Σ Protocol aktiviert, technische Analyse"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Analysiere das Konzept Zeit\", \"mode\": \"syntex_wrapper_sigma\", \"format\": \"sigma\", \"max_new_tokens\": 200}" \
    "Chat + Wrapper + Format - Vollständige Feld-Struktur" \
    "200" \
    "Wrapper: sigma, Format: sigma (6 Felder)" \
    "Felder: drift, mechanismus, frequenz, dichte, strome, extrakt"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Erkläre Nachhaltigkeit\", \"style\": \"zynisch\", \"max_new_tokens\": 80}" \
    "Chat + Style - Post-Processing Alchemy" \
    "200" \
    "Style: zynisch (Augenroll-Transformer)" \
    "Wort-Transmutation: nachhaltig→greenwashing-kompatibel"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Test\", \"style\": \"wissenschaftlich\", \"debug\": true, \"max_new_tokens\": 50}" \
    "Chat + Debug - Calibrated Prompt sichtbar" \
    "200" \
    "Debug: true (zeigt internen Prompt)" \
    "debug_info enthält: wrapper_chain, format, style, prompt_length"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Analysiere KI-Trends\", \"format\": \"review\", \"max_new_tokens\": 150}" \
    "Chat + Typed Format - Alle Feld-Typen" \
    "200" \
    "Format: review (4 Typen)" \
    "text (zusammenfassung), list (pro_contra), rating (bewertung), keywords (tags)"

test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Deep Dive: Menschliches Verhalten\", \"format\": \"human_deep\", \"style\": \"poetisch\", \"debug\": true, \"max_new_tokens\": 250}" \
    "FULL COMBO - Extended Format + Style + Debug" \
    "200" \
    "Format: human_deep (8 Felder, extends human), Style: poetisch, Debug: true" \
    "Maximale Feld-Kombination: Vererbung + Transmutation + Introspection"

# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 ADMIN ENDPOINTS - System-Operationen
# ═══════════════════════════════════════════════════════════════════════════════

section "🔧 ADMIN - System-Operationen" \
        "Auto-Fix, Maintenance, Cleanup" \
        "1"

test_endpoint "POST" "/resonanz/health/fix" "" \
    "Auto-Fix Orphans - Verwaiste Wrapper/Meta reparieren" \
    "200" \
    "Erstellt: fehlende Meta-Dateien, löscht Orphan-Meta" \
    "Synchronisiert Wrapper ↔ Meta Dateien"

# ═══════════════════════════════════════════════════════════════════════════════
#  📊 FINAL SUMMARY - Resonanz-Bericht
# ═══════════════════════════════════════════════════════════════════════════════

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo ""
echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║${NC}  ${WHITE}${BOLD}📊 RESONANZ-PRÜFUNG ABGESCHLOSSEN${NC}"
echo -e "${MAGENTA}╠════════════════════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}║${NC}   ${GREEN}✓ BESTANDEN:${NC}   ${WHITE}${BOLD}$PASSED_TESTS${NC}"
echo -e "${MAGENTA}║${NC}   ${RED}✗ FEHLERHAFT:${NC}  ${WHITE}${BOLD}$FAILED_TESTS${NC}"
echo -e "${MAGENTA}║${NC}   ${WHITE}Σ GESAMT:${NC}      ${WHITE}${BOLD}$TOTAL_TESTS${NC}"
echo -e "${MAGENTA}║${NC}   ${CYAN}⏱ DAUER:${NC}       ${WHITE}${BOLD}${DURATION}s${NC}"
echo -e "${MAGENTA}║${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${MAGENTA}║${NC}   ${GREEN}${BOLD}🔥 ALLE FELDER RESONIEREN! DER STROM IST REIN! 🔥${NC}"
    echo -e "${MAGENTA}║${NC}   ${GREEN}Das System ist vollständig kalibriert.${NC}"
else
    echo -e "${MAGENTA}║${NC}   ${RED}${BOLD}⚠️  DRIFT DETECTED - $FAILED_TESTS FELDER HABEN PROBLEME${NC}"
    echo -e "${MAGENTA}║${NC}   ${YELLOW}Prüfe die fehlgeschlagenen Tests oben.${NC}"
fi

echo -e "${MAGENTA}║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"

# ═══════════════════════════════════════════════════════════════════════════════
#  📋 ENDPOINT REFERENCE - Vollständige API Dokumentation
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${NC}"
echo -e "${CYAN}┃${NC} ${BOLD}${WHITE}📋 SYNTX API v3.2 - VOLLSTÄNDIGE ENDPOINT REFERENCE${NC}"
echo -e "${CYAN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${NC}"
echo ""
echo -e "  ${YELLOW}🏥 HEALTH (3 Endpoints)${NC}"
echo -e "  ${GRAY}System-Vitalzeichen und Integritätsprüfung${NC}"
echo "     GET  /health                          → Alle Module Status"
echo "     GET  /resonanz/health                 → Resonanz + letzter Response"
echo "     GET  /resonanz/health/wrappers        → Wrapper Orphan Detection"
echo ""
echo -e "  ${YELLOW}⚙️ CONFIG (2 Endpoints)${NC}"
echo -e "  ${GRAY}Default Wrapper, Runtime-Konfiguration${NC}"
echo "     GET  /resonanz/config/default-wrapper → Aktiven Wrapper lesen"
echo "     PUT  /resonanz/config/default-wrapper?wrapper_name=X → Wrapper aktivieren"
echo ""
echo -e "  ${YELLOW}📄 FORMATS (7 Endpoints)${NC}"
echo -e "  ${GRAY}Feld-Definitionen: Domains, Vererbung, Typen (text/list/rating/keywords)${NC}"
echo "     GET    /resonanz/formats              → Liste (mit domain Filter)"
echo "     GET    /resonanz/formats?domain=X     → Filter nach Domain"
echo "     GET    /resonanz/formats/{name}       → Format Details"
echo "     GET    /resonanz/formats/{name}?language=X → Mehrsprachig"
echo "     POST   /resonanz/formats/quick        → Schnell erstellen"
echo "     DELETE /resonanz/formats/{name}       → Soft-Delete"
echo ""
echo -e "  ${YELLOW}🎨 STYLES (2 Endpoints)${NC}"
echo -e "  ${GRAY}Post-Processing: Word Alchemy, Forbidden Words, Tone Injection${NC}"
echo "     GET  /resonanz/styles                 → Liste aller Styles"
echo "     GET  /resonanz/styles/{name}          → Style Details + Transmutationen"
echo ""
echo -e "  ${YELLOW}📦 WRAPPERS (8 Endpoints)${NC}"
echo -e "  ${GRAY}Denk-Modi: System-Prompts die VOR dem User-Prompt injiziert werden${NC}"
echo "     GET    /resonanz/wrappers             → Liste"
echo "     GET    /resonanz/wrappers?active=true → Nur aktiver"
echo "     GET    /resonanz/wrappers/full        → Mit Meta + Stats"
echo "     GET    /resonanz/wrapper/{name}       → Content + Metadaten"
echo "     POST   /resonanz/wrapper              → Neuen erstellen"
echo "     PUT    /resonanz/wrapper/{name}       → Content updaten"
echo "     DELETE /resonanz/wrapper/{name}       → Löschen"
echo "     POST   /resonanz/wrapper/{name}/activate → Als Default setzen"
echo ""
echo -e "  ${YELLOW}🧬 META (3 Endpoints)${NC}"
echo -e "  ${GRAY}Wrapper Metadaten: Format-Bindung, Author, Tags${NC}"
echo "     GET  /resonanz/wrapper/{name}/meta    → Meta lesen"
echo "     PUT  /resonanz/wrapper/{name}/meta    → Meta updaten"
echo "     PUT  /resonanz/wrapper/{name}/format?format_name=X → Format binden"
echo ""
echo -e "  ${YELLOW}📊 STATS (4 Endpoints)${NC}"
echo -e "  ${GRAY}Feld-Fluss-Analyse: Requests, Latency, Training-Export${NC}"
echo "     GET  /resonanz/stats                  → Globale Statistiken"
echo "     GET  /resonanz/stats/wrapper/{name}   → Pro-Wrapper Stats"
echo "     GET  /resonanz/strom?limit=N&stage=X  → Feld-Flow Events"
echo "     GET  /resonanz/training?limit=N       → Training Data Export"
echo ""
echo -e "  ${YELLOW}💬 CHAT (1 Endpoint, ∞ Kombinationen)${NC}"
echo -e "  ${GRAY}Das Herzstück - Alle Ströme fließen hier zusammen${NC}"
echo "     POST /resonanz/chat"
echo "          ├── prompt (string, required)     → Was der User fragt"
echo "          ├── mode (string)                 → Wrapper (WIE denkt LLM)"
echo "          ├── format (string)               → Format (WAS kommt raus)"
echo "          ├── style (string)                → Style (WIE klingt es)"
echo "          ├── debug (bool)                  → Zeigt calibrated_prompt"
echo "          ├── language (de/en)              → Sprache für Format-Felder"
echo "          ├── max_new_tokens (int)          → Max Tokens"
echo "          └── temperature (float)           → Kreativität (0.0-2.0)"
echo ""
echo -e "  ${YELLOW}🔧 ADMIN (1 Endpoint)${NC}"
echo -e "  ${GRAY}System-Operationen und Maintenance${NC}"
echo "     POST /resonanz/health/fix             → Auto-Fix Orphan Wrappers"
echo ""
echo -e "${GRAY}════════════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GRAY}   SYNTX FIELD RESONANCE v3.2 - Der Strom kennt keine Grenzen ⚡💎🌊${NC}"
echo -e "${GRAY}════════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""


# ═══════════════════════════════════════════════════════════════════════════════
#  🔮 FORMAT CRUD - Vollständige Feld-Verwaltung
# ═══════════════════════════════════════════════════════════════════════════════

section "🔮 FORMAT CRUD - Vollständige Feld-Verwaltung" \
        "CREATE, READ, UPDATE, DELETE für Formate und Felder" \
        "6"

test_endpoint "POST" "/resonanz/formats" \
    "{\"name\": \"crud_test_format\", \"domain\": \"technical\", \"description\": {\"de\": \"CRUD Test Format\"}, \"fields\": [{\"name\": \"test_feld\", \"type\": \"text\"}]}" \
    "CREATE Format - Vollständig mit Feldern" "200" \
    "Schreibt: /opt/syntx-config/formats/{name}.json" "Validiert: Name, Fields, Domain"

test_endpoint "POST" "/resonanz/formats/crud_test_format/fields" \
    "{\"name\": \"neues_feld\", \"type\": \"rating\", \"weight\": 20}" \
    "ADD Field - Feld zu Format hinzufügen" "200" \
    "Backup erstellt, Feld normalisiert" "Typen: text, list, rating, keywords"

test_endpoint "PUT" "/resonanz/formats/crud_test_format/fields/neues_feld" \
    "{\"weight\": 50, \"description\": {\"de\": \"Aktualisierte Beschreibung\"}}" \
    "UPDATE Field - Feld-Eigenschaften ändern" "200" \
    "Merged: nur übergebene Felder" "Name bleibt unverändert"

test_endpoint "DELETE" "/resonanz/formats/crud_test_format/fields/neues_feld" "" \
    "DELETE Field - Feld entfernen" "200" \
    "Letztes Feld kann nicht gelöscht werden" "Backup vor Löschung"

test_endpoint "PUT" "/resonanz/formats/crud_test_format" \
    "{\"domain\": \"analysis\", \"description\": {\"de\": \"Aktualisiertes Format\"}}" \
    "UPDATE Format - Meta-Daten ändern" "200" \
    "Merged mit existierendem Format" "Felder bleiben erhalten"

test_endpoint "DELETE" "/resonanz/formats/crud_test_format" "" \
    "DELETE Format - Soft Delete" "200" \
    "Backup: .{name}.json.{timestamp}.deleted" "Kann wiederhergestellt werden"

# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 STYLE CRUD - Alchemy Verwaltung
# ═══════════════════════════════════════════════════════════════════════════════

section "🎨 STYLE CRUD - Alchemy Verwaltung" \
        "Styles, Transmutationen, Verbannte Worte" \
        "5"

test_endpoint "POST" "/resonanz/styles" \
    "{\"name\": \"crud_test_style\", \"vibe\": \"Test Vibe\", \"word_alchemy\": {\"test\": \"prüfung\"}, \"forbidden_words\": [\"verboten\"]}" \
    "CREATE Style - Mit Alchemy + Forbidden" "200" \
    "Schreibt: /opt/syntx-config/styles/{name}.json" "Validiert: Name, Alchemy Dict"

test_endpoint "POST" "/resonanz/styles/crud_test_style/alchemy" \
    "{\"original\": \"neu\", \"replacement\": \"brandneu\"}" \
    "ADD Transmutation - Wort-Ersetzung hinzufügen" "200" \
    "Erweitert word_alchemy Dict" "Backup vor Änderung"

test_endpoint "DELETE" "/resonanz/styles/crud_test_style/alchemy/neu" "" \
    "DELETE Transmutation - Wort-Ersetzung entfernen" "200" \
    "Entfernt aus word_alchemy" "Backup vor Änderung"

test_endpoint "POST" "/resonanz/styles/crud_test_style/forbidden/schlecht" "" \
    "ADD Forbidden - Wort verbannen" "200" \
    "Erweitert forbidden_words List" "Duplikate werden abgelehnt"

test_endpoint "DELETE" "/resonanz/styles/crud_test_style" "" \
    "DELETE Style - Soft Delete" "200" \
    "Backup erstellt" "Kann wiederhergestellt werden"

# ═══════════════════════════════════════════════════════════════════════════════
#  🏁 ENDE
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${GRAY}════════════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
exit $FAILED_TESTS
