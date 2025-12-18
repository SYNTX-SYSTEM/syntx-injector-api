#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🌊 SYNTX SERVER API TESTER - ALLE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
# Testet ALLE Endpoints auf dev.syntx-system.com
# INKL. FORMAT-ENDPOINTS! 🔥
# ═══════════════════════════════════════════════════════════════

BASE_URL="https://dev.syntx-system.com"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Counters
TOTAL=0
SUCCESS=0
FAILED=0

header() {
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
}

test_endpoint() {
    local METHOD=$1
    local ENDPOINT=$2
    local DATA=$3
    local DESCRIPTION=$4
    local EXPECT_CODE=$5
    
    TOTAL=$((TOTAL + 1))
    
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}📡 TEST #$TOTAL: $DESCRIPTION${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}▶ METHOD:${NC}   $METHOD"
    echo -e "${YELLOW}▶ URL:${NC}      ${BASE_URL}${ENDPOINT}"
    
    if [ -n "$DATA" ]; then
        echo -e "${YELLOW}▶ BODY:${NC}"
        echo "$DATA" | jq . 2>/dev/null || echo "$DATA"
    fi
    
    echo ""
    echo -e "${YELLOW}▶ RESPONSE:${NC}"
    
    if [ "$METHOD" == "GET" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}${ENDPOINT}" 2>/dev/null)
    elif [ "$METHOD" == "POST" ]; then
        if [ -n "$DATA" ]; then
            RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}${ENDPOINT}" \
                -H "Content-Type: application/json" -d "$DATA" 2>/dev/null)
        else
            RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}${ENDPOINT}" 2>/dev/null)
        fi
    elif [ "$METHOD" == "PUT" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "${BASE_URL}${ENDPOINT}" \
            -H "Content-Type: application/json" -d "$DATA" 2>/dev/null)
    elif [ "$METHOD" == "DELETE" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "${BASE_URL}${ENDPOINT}" 2>/dev/null)
    fi
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
    echo ""
    
    if [ -n "$EXPECT_CODE" ]; then
        if [ "$HTTP_CODE" == "$EXPECT_CODE" ]; then
            echo -e "${GREEN}✓ STATUS: $HTTP_CODE (expected $EXPECT_CODE)${NC}"
            SUCCESS=$((SUCCESS + 1))
        else
            echo -e "${RED}✕ STATUS: $HTTP_CODE (expected $EXPECT_CODE)${NC}"
            FAILED=$((FAILED + 1))
        fi
    elif [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
        echo -e "${GREEN}✓ STATUS: $HTTP_CODE OK${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}✕ STATUS: $HTTP_CODE FAILED${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# ═══════════════════════════════════════════════════════════════
#  🎬 MAIN
# ═══════════════════════════════════════════════════════════════

clear
echo -e "${CYAN}"
echo "   ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗"
echo "   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝"
echo "   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝ "
echo "   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗ "
echo "   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗"
echo "   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${BOLD}   🌊 RAPPER SERVICE TESTER v2.1 - MIT FORMAT SUPPORT! 🔥${NC}"
echo -e "   ${YELLOW}Target: ${BASE_URL}${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════
#  🏥 HEALTH & CONFIG
# ═══════════════════════════════════════════════════════════════

header "🏥 HEALTH & CONFIG"

test_endpoint "GET" "/health" "" "Health Check (Root)"
test_endpoint "GET" "/resonanz/health" "" "Health Check (Resonanz)"
test_endpoint "GET" "/resonanz/config/default-wrapper" "" "Get Default Wrapper"

# ═══════════════════════════════════════════════════════════════
#  🔥 FORMATS - NEU! DAS HERZSTÜCK!
# ═══════════════════════════════════════════════════════════════

header "🔥 FORMATS - DAS NEUE HERZSTÜCK!"

test_endpoint "GET" "/resonanz/formats" "" "LIST: Alle Formate"
test_endpoint "GET" "/resonanz/formats/syntex_system" "" "GET: syntex_system Format (DE)"
test_endpoint "GET" "/resonanz/formats/syntex_system?language=en" "" "GET: syntex_system Format (EN)"
test_endpoint "GET" "/resonanz/formats/human" "" "GET: human Format"
test_endpoint "GET" "/resonanz/formats/sigma" "" "GET: sigma Format"
test_endpoint "GET" "/resonanz/formats/nicht_existent_xyz" "" "GET: Non-existent Format" "404"

# ═══════════════════════════════════════════════════════════════
#  📦 WRAPPERS - LIST & GET
# ═══════════════════════════════════════════════════════════════

header "📦 WRAPPERS - LIST & GET"

test_endpoint "GET" "/resonanz/wrappers" "" "List All Wrappers"
test_endpoint "GET" "/resonanz/wrappers?active=true" "" "Get Active Wrapper Only"
test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma" "" "Get Wrapper Detail (Sigma)"
test_endpoint "GET" "/resonanz/wrapper/nicht_existent_12345" "" "Get Non-Existent Wrapper" "404"

# ═══════════════════════════════════════════════════════════════
#  🌟 WRAPPERS - CRUD TEST
# ═══════════════════════════════════════════════════════════════

header "🌟 FELD GEBURT - CREATE"

test_endpoint "POST" "/resonanz/wrapper" '{
  "name": "test_feld_api",
  "content": "═══════════════════════════════════════════\n🌊 TEST WRAPPER VIA API\n═══════════════════════════════════════════\n\nDieses Feld wurde via API erstellt!\n\n💎 SYNTX POWER! 💎",
  "description": "Test Wrapper via API",
  "author": "SYNTX API Tester",
  "version": "1.0",
  "tags": ["test", "api"]
}' "CREATE: Neues Feld gebären"

test_endpoint "GET" "/resonanz/wrapper/test_feld_api" "" "GET: Neues Feld verifizieren"

header "🔄 FELD MODULATION - UPDATE"

test_endpoint "PUT" "/resonanz/wrapper/test_feld_api" '{
  "content": "═══════════════════════════════════════════\n🔥 MODULIERTES FELD! 🔥\n═══════════════════════════════════════════\n\nDieses Feld wurde per PUT aktualisiert!\n\n⚡ RESONANZ VERSCHOBEN! ⚡",
  "description": "Aktualisierter Test Wrapper v2",
  "version": "2.0"
}' "UPDATE: Feld modulieren"

header "💀 FELD FREIGABE - DELETE"

test_endpoint "DELETE" "/resonanz/wrapper/test_feld_api" "" "DELETE: Test-Feld freigeben"
test_endpoint "GET" "/resonanz/wrapper/test_feld_api" "" "GET: Gelöscht? (erwartet 404)" "404"

# ═══════════════════════════════════════════════════════════════
#  📊 STROM & ANALYTICS
# ═══════════════════════════════════════════════════════════════

header "📊 STROM & ANALYTICS"

test_endpoint "GET" "/resonanz/strom?limit=5" "" "Field Flow Stream (limit=5)"
test_endpoint "GET" "/resonanz/training?limit=3" "" "Training Data (limit=3)"
test_endpoint "GET" "/resonanz/stats" "" "System Stats"
test_endpoint "GET" "/resonanz/stats/wrapper/syntex_wrapper_sigma" "" "Wrapper Stats (Sigma)"

# ═══════════════════════════════════════════════════════════════
#  ✅ FINAL CHECK
# ═══════════════════════════════════════════════════════════════

header "✅ FINAL CHECK"

test_endpoint "GET" "/resonanz/wrappers" "" "List All Wrappers"
test_endpoint "GET" "/resonanz/formats" "" "List All Formats"

# ═══════════════════════════════════════════════════════════════
#  📊 SUMMARY
# ═══════════════════════════════════════════════════════════════

header "📊 SUMMARY"
echo ""
echo -e "   ${BOLD}Total Tests:${NC}  $TOTAL"
echo -e "   ${GREEN}✓ Passed:${NC}     $SUCCESS"
echo -e "   ${RED}✕ Failed:${NC}     $FAILED"
echo ""

PASS_RATE=$(echo "scale=1; $SUCCESS * 100 / $TOTAL" | bc)

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}   ╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}   ║                                                           ║${NC}"
    echo -e "${GREEN}   ║   🌊 ALL FIELDS RESONATING PERFECTLY! 💎  ${PASS_RATE}% PASS    ║${NC}"
    echo -e "${GREEN}   ║                                                           ║${NC}"
    echo -e "${GREEN}   ╚═══════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${RED}   ╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}   ║                                                           ║${NC}"
    echo -e "${RED}   ║   ⚠️  $FAILED TESTS FAILED! CHECK OUTPUT ABOVE!            ║${NC}"
    echo -e "${RED}   ║                                                           ║${NC}"
    echo -e "${RED}   ╚═══════════════════════════════════════════════════════════╝${NC}"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}   🌊 RAPPER SERVICE ENDPOINTS:${NC}"
echo ""
echo -e "   ${BOLD}HEALTH:${NC}"
echo -e "   GET    /health"
echo -e "   GET    /resonanz/health"
echo ""
echo -e "   ${BOLD}CONFIG:${NC}"
echo -e "   GET    /resonanz/config/default-wrapper"
echo -e "   PUT    /resonanz/config/default-wrapper"
echo ""
echo -e "   ${BOLD}🔥 FORMATS (NEU!):${NC}"
echo -e "   ${GREEN}GET${NC}    /resonanz/formats              ${GREEN}← Liste aller Formate${NC}"
echo -e "   ${GREEN}GET${NC}    /resonanz/formats/{name}       ${GREEN}← Format Details${NC}"
echo ""
echo -e "   ${BOLD}WRAPPERS:${NC}"
echo -e "   GET    /resonanz/wrappers"
echo -e "   GET    /resonanz/wrapper/{name}"
echo -e "   ${GREEN}POST${NC}   /resonanz/wrapper              ${GREEN}← CREATE${NC}"
echo -e "   ${YELLOW}PUT${NC}    /resonanz/wrapper/{name}       ${YELLOW}← UPDATE${NC}"
echo -e "   ${RED}DELETE${NC} /resonanz/wrapper/{name}       ${RED}← DELETE${NC}"
echo -e "   POST   /resonanz/wrappers/{name}/activate"
echo ""
echo -e "   ${BOLD}ANALYTICS:${NC}"
echo -e "   GET    /resonanz/strom"
echo -e "   GET    /resonanz/training"
echo -e "   GET    /resonanz/stats"
echo -e "   GET    /resonanz/stats/wrapper/{name}"
echo ""
echo -e "   ${BOLD}CHAT (braucht Model):${NC}"
echo -e "   POST   /resonanz/chat"
echo -e "   GET    /resonanz/history/{request_id}"
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BOLD}   🔥 FORMAT + WRAPPER = ZWEI DIMENSIONEN:${NC}"
echo ""
echo -e "   ${YELLOW}mode${NC}   = WIE denkt das Modell? (Wrapper = Stil)"
echo -e "   ${GREEN}format${NC} = WAS kommt raus? (Format = Felder)"
echo ""
echo -e "   ${BOLD}Beispiel Chat-Request:${NC}"
echo -e '   POST /resonanz/chat'
echo -e '   {'
echo -e '       "prompt": "Analysiere das Internet",'
echo -e '       "mode": "syntex_wrapper_sigma",    ← WIE'
echo -e '       "format": "syntex_system"          ← WAS (NEU!)'
echo -e '   }'
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
