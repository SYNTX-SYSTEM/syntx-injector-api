#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🌊 SYNTX SERVER API TESTER - ALLE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
# Testet ALLE Endpoints auf dem PRODUCTION Server
# Inkl. Chat-Endpoint (braucht Model)
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

clear
echo -e "${CYAN}"
echo "   ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗"
echo "   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝"
echo "   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝ "
echo "   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗ "
echo "   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗"
echo "   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${BOLD}   🌊 SERVER API TESTER - ALLE ENDPOINTS${NC}"
echo -e "   ${YELLOW}Base: ${BASE_URL}${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════
#  🏥 HEALTH & CONFIG
# ═══════════════════════════════════════════════════════════════

header "🏥 HEALTH & CONFIG"

test_endpoint "GET" "/health" "" "Health Check (Root)"
test_endpoint "GET" "/resonanz/health" "" "Health Check (Resonanz)"
test_endpoint "GET" "/resonanz/config/default-wrapper" "" "Get Default Wrapper"
test_endpoint "PUT" "/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma" "" "Set Default Wrapper"

# ═══════════════════════════════════════════════════════════════
#  📦 WRAPPERS - LIST & GET
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
  "name": "test_feld_server",
  "content": "═══════════════════════════════════════════\n🌊 SERVER TEST WRAPPER\n═══════════════════════════════════════════\n\nDieses Feld wurde auf dem SERVER erstellt!\n\n💎 SYNTX POWER! 💎",
  "description": "Server Test Wrapper",
  "author": "SYNTX Server Tester",
  "version": "1.0",
  "tags": ["test", "server", "crud"]
}' "CREATE: Neues Feld gebären"

test_endpoint "POST" "/resonanz/wrapper" '{
  "name": "test_feld_server",
  "content": "Duplikat!"
}' "CREATE: Duplikat (erwartet 409)" "409"

test_endpoint "GET" "/resonanz/wrapper/test_feld_server" "" "GET: Neues Feld verifizieren"

# ═══════════════════════════════════════════════════════════════
#  🔄 WRAPPERS - UPDATE (NEU!)
# ═══════════════════════════════════════════════════════════════

header "🔄 FELD MODULATION - UPDATE"

test_endpoint "PUT" "/resonanz/wrapper/test_feld_server" '{
  "content": "═══════════════════════════════════════════\n🔥 MODULIERTES SERVER FELD! 🔥\n═══════════════════════════════════════════\n\nDieses Feld wurde per PUT aktualisiert!\n\n⚡ RESONANZ VERSCHOBEN! ⚡",
  "description": "Aktualisierter Server Wrapper v2",
  "version": "2.0"
}' "UPDATE: Feld modulieren"

test_endpoint "GET" "/resonanz/wrapper/test_feld_server" "" "GET: Moduliertes Feld verifizieren"

test_endpoint "PUT" "/resonanz/wrapper/nicht_existent_xyz" '{
  "content": "Should fail"
}' "UPDATE: Non-existent (erwartet 404)" "404"

# ═══════════════════════════════════════════════════════════════
#  🎯 WRAPPERS - ACTIVATE
# ═══════════════════════════════════════════════════════════════

header "🎯 FELD AKTIVIERUNG"

test_endpoint "POST" "/resonanz/wrappers/test_feld_server/activate" "" "ACTIVATE: Test-Feld aktivieren"
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
#  💬 CHAT & HISTORY
# ═══════════════════════════════════════════════════════════════

header "💬 CHAT & HISTORY"

echo -e "${YELLOW}⏳ Chat dauert 15-30 Sekunden...${NC}"
test_endpoint "POST" "/resonanz/chat" '{"prompt":"Was ist SYNTX?","mode":"syntex_wrapper_sigma","max_new_tokens":100}' "Chat Request"

# Extract request_id for history test
REQUEST_ID=$(echo "$BODY" | jq -r '.metadata.request_id' 2>/dev/null)
if [ -n "$REQUEST_ID" ] && [ "$REQUEST_ID" != "null" ]; then
    test_endpoint "GET" "/resonanz/history/${REQUEST_ID}" "" "Request History"
fi

# ═══════════════════════════════════════════════════════════════
#  💀 WRAPPERS - DELETE (NEU!)
# ═══════════════════════════════════════════════════════════════

header "💀 FELD FREIGABE - DELETE"

test_endpoint "DELETE" "/resonanz/wrapper/test_feld_server" "" "DELETE: Test-Feld freigeben"
test_endpoint "GET" "/resonanz/wrapper/test_feld_server" "" "GET: Gelöscht? (erwartet 404)" "404"
test_endpoint "DELETE" "/resonanz/wrapper/nicht_existent_xyz" "" "DELETE: Non-existent (erwartet 404)" "404"

# ═══════════════════════════════════════════════════════════════
#  ✅ FINAL CHECK
# ═══════════════════════════════════════════════════════════════

header "✅ FINAL CHECK"

test_endpoint "GET" "/resonanz/wrappers" "" "List All (Test-Feld sollte weg sein)"
test_endpoint "GET" "/resonanz/config/default-wrapper" "" "Default Wrapper Check"

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
echo -e "   ${BOLD}WRAPPERS:${NC}"
echo -e "   GET    /resonanz/wrappers"
echo -e "   GET    /resonanz/wrapper/{name}"
echo -e "   ${GREEN}POST${NC}   /resonanz/wrapper              ${GREEN}← NEU!${NC}"
echo -e "   ${YELLOW}PUT${NC}    /resonanz/wrapper/{name}       ${YELLOW}← NEU!${NC}"
echo -e "   ${RED}DELETE${NC} /resonanz/wrapper/{name}       ${RED}← NEU!${NC}"
echo -e "   POST   /resonanz/wrappers/{name}/activate"
echo ""
echo -e "   ${BOLD}ANALYTICS:${NC}"
echo -e "   GET    /resonanz/strom"
echo -e "   GET    /resonanz/training"
echo -e "   GET    /resonanz/stats"
echo -e "   GET    /resonanz/stats/wrapper/{name}"
echo ""
echo -e "   ${BOLD}CHAT:${NC}"
echo -e "   POST   /resonanz/chat"
echo -e "   GET    /resonanz/history/{request_id}"
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
