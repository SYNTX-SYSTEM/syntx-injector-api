#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🌊 SYNTX LOCAL API TESTER - ALLE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
# Startet Server automatisch, testet ALLE Endpoints, stoppt Server
# INKL. FORMAT-ENDPOINTS! 🔥
# ═══════════════════════════════════════════════════════════════

BASE_URL="http://localhost:8001"
SERVER_PID=""

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

# ═══════════════════════════════════════════════════════════════
#  🚀 SERVER MANAGEMENT
# ═══════════════════════════════════════════════════════════════

start_server() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  🚀 STARTING SYNTX SERVER...${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Kill any existing server on port 8001
    pkill -f "uvicorn src.main:app --port 8001" 2>/dev/null
    sleep 1
    
    # Start server in background
    python -m uvicorn src.main:app --port 8001 > /tmp/syntx_server.log 2>&1 &
    SERVER_PID=$!
    
    echo -e "${YELLOW}▶ Server PID: ${SERVER_PID}${NC}"
    echo -e "${YELLOW}▶ Waiting for server to start...${NC}"
    
    # Wait for server to be ready (max 10 seconds)
    for i in {1..20}; do
        if curl -s "${BASE_URL}/health" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Server is ready!${NC}"
            return 0
        fi
        sleep 0.5
    done
    
    echo -e "${RED}✕ Server failed to start!${NC}"
    echo -e "${RED}  Check /tmp/syntx_server.log for details${NC}"
    cat /tmp/syntx_server.log
    exit 1
}

stop_server() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  🛑 STOPPING SYNTX SERVER...${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ -n "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
        wait $SERVER_PID 2>/dev/null
        echo -e "${GREEN}✓ Server stopped (PID: ${SERVER_PID})${NC}"
    fi
    
    # Make sure no orphan processes
    pkill -f "uvicorn src.main:app --port 8001" 2>/dev/null
}

# Cleanup on exit (Ctrl+C or error)
cleanup() {
    echo ""
    echo -e "${YELLOW}⚠ Cleaning up...${NC}"
    stop_server
    exit 0
}
trap cleanup SIGINT SIGTERM

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
    local EXPECT_CODE=$5  # Optional: erwarteter Status Code
    
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
    
    # Check success based on expected code or default 2xx
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
echo -e "${BOLD}   🌊 LOCAL API TESTER v2.1 - MIT FORMAT SUPPORT! 🔥${NC}"
echo -e "   ${YELLOW}Base: ${BASE_URL}${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════
#  🚀 START SERVER
# ═══════════════════════════════════════════════════════════════

start_server

# ═══════════════════════════════════════════════════════════════
#  🏥 HEALTH & CONFIG
# ═══════════════════════════════════════════════════════════════

header "🏥 HEALTH & CONFIG"

test_endpoint "GET" "/health" "" "Health Check (Root)"
test_endpoint "GET" "/resonanz/health" "" "Health Check (Resonanz)"
test_endpoint "GET" "/resonanz/config/default-wrapper" "" "Get Default Wrapper"
test_endpoint "PUT" "/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma" "" "Set Default Wrapper"

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
#  📦 WRAPPERS - BESTEHENDE ENDPOINTS
# ═══════════════════════════════════════════════════════════════

header "📦 WRAPPERS - LIST & GET"

test_endpoint "GET" "/resonanz/wrappers" "" "List All Wrappers"
test_endpoint "GET" "/resonanz/wrappers?active=true" "" "Get Active Wrapper Only"
test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma" "" "Get Wrapper Detail (Sigma)"
test_endpoint "GET" "/resonanz/wrapper/nicht_existent_12345" "" "Get Non-Existent Wrapper" "404"

# ═══════════════════════════════════════════════════════════════
#  🌟 WRAPPERS - CREATE (NEU!)
# ═══════════════════════════════════════════════════════════════

header "🌟 FELD GEBURT - CREATE"

test_endpoint "POST" "/resonanz/wrapper" '{
  "name": "test_feld_crud",
  "content": "═══════════════════════════════════════════\n🌊 TEST WRAPPER FÜR CRUD OPERATIONS\n═══════════════════════════════════════════\n\nDieses Feld wurde dynamisch erstellt!\n\nEs testet:\n- POST /resonanz/wrapper (CREATE)\n- PUT /resonanz/wrapper/{name} (UPDATE)\n- DELETE /resonanz/wrapper/{name} (DELETE)\n\n💎 SYNTX POWER! 💎",
  "description": "Test Wrapper für CRUD Operations",
  "author": "SYNTX Local Tester",
  "version": "1.0",
  "tags": ["test", "crud", "dynamisch", "lokal"]
}' "CREATE: Neues Feld gebären"

test_endpoint "POST" "/resonanz/wrapper" '{
  "name": "test_feld_crud",
  "content": "Duplikat!"
}' "CREATE: Duplikat (erwartet 409)" "409"

test_endpoint "POST" "/resonanz/wrapper" '{
  "name": "test_feld_minimal",
  "content": "Minimales Feld ohne Metadata"
}' "CREATE: Minimales Feld (nur name + content)"

test_endpoint "GET" "/resonanz/wrapper/test_feld_crud" "" "GET: Neues Feld verifizieren"

# ═══════════════════════════════════════════════════════════════
#  🔄 WRAPPERS - UPDATE (NEU!)
# ═══════════════════════════════════════════════════════════════

header "🔄 FELD MODULATION - UPDATE"

test_endpoint "PUT" "/resonanz/wrapper/test_feld_crud" '{
  "content": "═══════════════════════════════════════════\n🔥 MODULIERTES FELD! 🔥\n═══════════════════════════════════════════\n\nDieses Feld wurde per PUT aktualisiert!\n\nNeue Features:\n- Modulation erfolgreich\n- Version 2.0\n- Mehr Power!\n\n⚡ DIE RESONANZ HAT SICH VERSCHOBEN! ⚡",
  "description": "Aktualisierter Test Wrapper v2",
  "version": "2.0"
}' "UPDATE: Feld modulieren"

test_endpoint "GET" "/resonanz/wrapper/test_feld_crud" "" "GET: Moduliertes Feld verifizieren"

test_endpoint "PUT" "/resonanz/wrapper/nicht_existent_xyz" '{
  "content": "Should fail"
}' "UPDATE: Non-existent (erwartet 404)" "404"

# ═══════════════════════════════════════════════════════════════
#  🎯 WRAPPERS - ACTIVATE
# ═══════════════════════════════════════════════════════════════

header "🎯 FELD AKTIVIERUNG"

test_endpoint "POST" "/resonanz/wrappers/test_feld_crud/activate" "" "ACTIVATE: Test-Feld aktivieren"
test_endpoint "GET" "/resonanz/config/default-wrapper" "" "GET: Prüfen ob aktiviert"
test_endpoint "POST" "/resonanz/wrappers/syntex_wrapper_sigma/activate" "" "ACTIVATE: Sigma wieder aktivieren"
test_endpoint "POST" "/resonanz/wrappers/nicht_existent/activate" "" "ACTIVATE: Non-existent (erwartet 404)" "404"

# ═══════════════════════════════════════════════════════════════
#  📊 STROM & ANALYTICS
# ═══════════════════════════════════════════════════════════════

header "📊 STROM & ANALYTICS"

test_endpoint "GET" "/resonanz/strom?limit=5" "" "Field Flow Stream (limit=5)"
test_endpoint "GET" "/resonanz/strom?limit=3&stage=5_RESPONSE" "" "Field Flow Stream (nur Responses)"
test_endpoint "GET" "/resonanz/training?limit=3" "" "Training Data (limit=3)"
test_endpoint "GET" "/resonanz/training?limit=5&wrapper=syntex_wrapper_sigma" "" "Training Data (filtered by wrapper)"
test_endpoint "GET" "/resonanz/stats" "" "System Stats"
test_endpoint "GET" "/resonanz/stats/wrapper/syntex_wrapper_sigma" "" "Wrapper Stats (Sigma)"

# ═══════════════════════════════════════════════════════════════
#  💀 WRAPPERS - DELETE (NEU!)
# ═══════════════════════════════════════════════════════════════

header "💀 FELD FREIGABE - DELETE"

test_endpoint "DELETE" "/resonanz/wrapper/test_feld_crud" "" "DELETE: Test-Feld freigeben"
test_endpoint "GET" "/resonanz/wrapper/test_feld_crud" "" "GET: Gelöscht? (erwartet 404)" "404"
test_endpoint "DELETE" "/resonanz/wrapper/test_feld_minimal" "" "DELETE: Minimales Feld freigeben"
test_endpoint "DELETE" "/resonanz/wrapper/nicht_existent_xyz" "" "DELETE: Non-existent (erwartet 404)" "404"

# ═══════════════════════════════════════════════════════════════
#  ✅ FINAL CHECK
# ═══════════════════════════════════════════════════════════════

header "✅ FINAL CHECK"

test_endpoint "GET" "/resonanz/wrappers" "" "List All (Test-Felder sollten weg sein)"
test_endpoint "GET" "/resonanz/config/default-wrapper" "" "Default Wrapper Check"
test_endpoint "GET" "/resonanz/formats" "" "Formats Final Check"

# ═══════════════════════════════════════════════════════════════
#  🛑 STOP SERVER
# ═══════════════════════════════════════════════════════════════

stop_server

# ═══════════════════════════════════════════════════════════════
#  📊 SUMMARY
# ═══════════════════════════════════════════════════════════════

header "📊 SUMMARY"
echo ""
echo -e "   ${BOLD}Total Tests:${NC} $TOTAL"
echo -e "   ${GREEN}✓ Passed:${NC}    $SUCCESS"
echo -e "   ${RED}✕ Failed:${NC}    $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}   ╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}   ║                                                           ║${NC}"
    echo -e "${GREEN}   ║   🎉 ALL $TOTAL TESTS PASSED! SYNTX RESONIERT! 🎉          ║${NC}"
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
echo -e "${BOLD}   🌊 GETESTETE ENDPOINTS:${NC}"
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
echo -e "   ${GREEN}GET${NC}    /resonanz/formats              ${GREEN}← NEU!${NC}"
echo -e "   ${GREEN}GET${NC}    /resonanz/formats/{name}       ${GREEN}← NEU!${NC}"
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
echo -e "   ${BOLD}NICHT GETESTET (braucht Model):${NC}"
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
