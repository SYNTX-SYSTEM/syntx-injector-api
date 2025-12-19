#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# 🌊 SYNTX API TESTER v3.0 - VOLLSTÄNDIG!
# ═══════════════════════════════════════════════════════════════
# Alle Endpoints: Health, Config, Wrappers, Formats, Meta, Chat, Stats
# ═══════════════════════════════════════════════════════════════

BASE_URL="https://dev.syntx-system.com"
# Falls lokal: BASE_URL="http://localhost:8001"

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

# Test wrapper name for CRUD tests
TEST_WRAPPER="api_test_wrapper_$(date +%s)"
TEST_FORMAT="test_format_$(date +%s)"

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
    local EXPECT_CODE=${5:-200}
    
    TOTAL=$((TOTAL + 1))
    
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}📡 TEST #$TOTAL: $DESCRIPTION${NC}"
    echo -e "${YELLOW}▶ $METHOD $BASE_URL$ENDPOINT${NC}"
    
    if [ "$METHOD" == "GET" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL$ENDPOINT")
    elif [ "$METHOD" == "DELETE" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL$ENDPOINT")
    elif [ "$METHOD" == "PUT" ] && [ -z "$DATA" ]; then
        RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL$ENDPOINT")
    else
        RESPONSE=$(curl -s -w "\n%{http_code}" -X $METHOD -H "Content-Type: application/json" -d "$DATA" "$BASE_URL$ENDPOINT")
    fi
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    # Pretty print JSON (truncated)
    echo "$BODY" | jq '.' 2>/dev/null | head -30
    if [ $(echo "$BODY" | jq '.' 2>/dev/null | wc -l) -gt 30 ]; then
        echo "... (truncated)"
    fi
    
    if [ "$HTTP_CODE" == "$EXPECT_CODE" ]; then
        echo -e "${GREEN}✓ $HTTP_CODE${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}✕ $HTTP_CODE (expected $EXPECT_CODE)${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# ═══════════════════════════════════════════════════════════════
# START
# ═══════════════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}   🌊 SYNTX API TESTER v3.0 - $BASE_URL${NC}"

# ═══════════════════════════════════════════════════════════════
# 🏥 HEALTH
# ═══════════════════════════════════════════════════════════════
header "🏥 HEALTH"

test_endpoint "GET" "/health" "" "Root Health Check"
test_endpoint "GET" "/resonanz/health" "" "Resonanz Health Check"
test_endpoint "GET" "/resonanz/health/wrappers" "" "Wrapper Health + Orphan Detection"

# ═══════════════════════════════════════════════════════════════
# ⚙️ CONFIG
# ═══════════════════════════════════════════════════════════════
header "⚙️ CONFIG"

test_endpoint "GET" "/resonanz/config/default-wrapper" "" "Get Default Wrapper"

# ═══════════════════════════════════════════════════════════════
# 🔥 FORMATS
# ═══════════════════════════════════════════════════════════════
header "🔥 FORMATS"

test_endpoint "GET" "/resonanz/formats" "" "List All Formats"
test_endpoint "GET" "/resonanz/formats/sigma" "" "Get Format: sigma"
test_endpoint "GET" "/resonanz/formats/sigma?language=en" "" "Get Format: sigma (English)"
test_endpoint "GET" "/resonanz/formats/economics" "" "Get Format: economics"
test_endpoint "GET" "/resonanz/formats/human" "" "Get Format: human"

# Quick Create Format Test
test_endpoint "POST" "/resonanz/formats/quick" \
    "{\"name\": \"$TEST_FORMAT\", \"description_de\": \"Test Format\", \"field_names\": [\"field1\", \"field2\"], \"wrapper\": \"syntex_wrapper_sigma\"}" \
    "Quick Create Format"

# Delete Test Format
test_endpoint "DELETE" "/resonanz/formats/$TEST_FORMAT" "" "Delete Test Format"

# ═══════════════════════════════════════════════════════════════
# 📦 WRAPPERS
# ═══════════════════════════════════════════════════════════════
header "📦 WRAPPERS"

test_endpoint "GET" "/resonanz/wrappers" "" "List All Wrappers"
test_endpoint "GET" "/resonanz/wrappers?active=true" "" "Get Active Wrapper Only"
test_endpoint "GET" "/resonanz/wrappers/full" "" "List Wrappers + Meta + Stats"
test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma" "" "Get Wrapper Content: sigma"
test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_deepsweep" "" "Get Wrapper Content: deepsweep"

# CREATE Test Wrapper
test_endpoint "POST" "/resonanz/wrapper" \
    "{\"name\": \"$TEST_WRAPPER\", \"content\": \"Dies ist ein Test-Wrapper für API-Tests. SYNTX FIELD RESONANCE.\"}" \
    "CREATE Wrapper"

# UPDATE Test Wrapper
test_endpoint "PUT" "/resonanz/wrapper/$TEST_WRAPPER" \
    "{\"content\": \"UPDATED: Dies ist der aktualisierte Test-Wrapper. SYNTX FIELD RESONANCE v2.\"}" \
    "UPDATE Wrapper"

# DELETE Test Wrapper
test_endpoint "DELETE" "/resonanz/wrapper/$TEST_WRAPPER" "" "DELETE Wrapper"

# ═══════════════════════════════════════════════════════════════
# 🧬 META (NEU in v3.0!)
# ═══════════════════════════════════════════════════════════════
header "🧬 META"

test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_sigma/meta" "" "Get Meta: sigma"
test_endpoint "GET" "/resonanz/wrapper/syntex_wrapper_deepsweep/meta" "" "Get Meta: deepsweep"

# Format Binding
test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_sigma/format?format_name=sigma" "" "Bind Format: sigma → sigma"
test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_deepsweep/format?format_name=economics" "" "Bind Format: deepsweep → economics"

# Update Meta
test_endpoint "PUT" "/resonanz/wrapper/syntex_wrapper_sigma/meta" \
    "{\"description\": \"Sigma Protocol - Technische Präzisionsanalyse\", \"tags\": [\"sigma\", \"technisch\", \"präzise\"], \"author\": \"SYNTX Architect\"}" \
    "Update Meta: sigma"

# ═══════════════════════════════════════════════════════════════
# 📊 STATS & STREAMS
# ═══════════════════════════════════════════════════════════════
header "📊 STATS & STREAMS"

test_endpoint "GET" "/resonanz/stats" "" "System Stats"
test_endpoint "GET" "/resonanz/stats/wrapper/syntex_wrapper_sigma" "" "Wrapper Stats: sigma"
test_endpoint "GET" "/resonanz/strom?limit=3" "" "Field Flow Stream (last 3)"
test_endpoint "GET" "/resonanz/strom?limit=3&stage=5_RESPONSE" "" "Field Flow Stream (RESPONSE only)"
test_endpoint "GET" "/resonanz/training?limit=3" "" "Training Data Export (last 3)"

# ═══════════════════════════════════════════════════════════════
# 💬 CHAT (Das Herzstück!)
# ═══════════════════════════════════════════════════════════════
header "💬 CHAT"

# Simple Chat
test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Was ist 2+2?\", \"max_new_tokens\": 50}" \
    "Simple Chat"

# Chat with Wrapper
test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Erkläre kurz was ein System ist\", \"mode\": \"syntex_wrapper_sigma\", \"max_new_tokens\": 100}" \
    "Chat with Wrapper"

# Chat with Format
test_endpoint "POST" "/resonanz/chat" \
    "{\"prompt\": \"Analysiere das Konzept Zeit\", \"mode\": \"syntex_wrapper_sigma\", \"format\": \"sigma\", \"max_new_tokens\": 200}" \
    "Chat with Wrapper + Format"

# ═══════════════════════════════════════════════════════════════
# 🔧 ADMIN OPERATIONS
# ═══════════════════════════════════════════════════════════════
header "🔧 ADMIN"

test_endpoint "POST" "/resonanz/health/fix" "" "Auto-Fix Orphan Wrappers"

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${MAGENTA}  📊 SUMMARY${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════════${NC}"
echo -e "   ${GREEN}✓ Passed: $SUCCESS${NC}  ${RED}✕ Failed: $FAILED${NC}  Total: $TOTAL"

if [ $FAILED -eq 0 ]; then
    echo -e "   ${GREEN}🎉 ALL TESTS PASSED!${NC}"
else
    echo -e "   ${RED}⚠️ SOME TESTS FAILED${NC}"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  📡 ENDPOINT COVERAGE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  🏥 HEALTH"
echo "     GET  /health"
echo "     GET  /resonanz/health"
echo "     GET  /resonanz/health/wrappers"
echo "     POST /resonanz/health/fix"
echo ""
echo "  ⚙️ CONFIG"
echo "     GET  /resonanz/config/default-wrapper"
echo "     PUT  /resonanz/config/default-wrapper?wrapper_name=X"
echo ""
echo "  🔥 FORMATS"
echo "     GET    /resonanz/formats"
echo "     GET    /resonanz/formats/{name}"
echo "     GET    /resonanz/formats/{name}?language=X"
echo "     POST   /resonanz/formats (full)"
echo "     POST   /resonanz/formats/quick"
echo "     PUT    /resonanz/formats/{name}"
echo "     DELETE /resonanz/formats/{name}"
echo ""
echo "  📦 WRAPPERS"
echo "     GET    /resonanz/wrappers"
echo "     GET    /resonanz/wrappers?active=true"
echo "     GET    /resonanz/wrappers/full"
echo "     GET    /resonanz/wrapper/{name}"
echo "     POST   /resonanz/wrapper"
echo "     PUT    /resonanz/wrapper/{name}"
echo "     DELETE /resonanz/wrapper/{name}"
echo "     POST   /resonanz/wrappers/{name}/activate"
echo ""
echo "  🧬 META (v3.0)"
echo "     GET  /resonanz/wrapper/{name}/meta"
echo "     PUT  /resonanz/wrapper/{name}/meta"
echo "     PUT  /resonanz/wrapper/{name}/format?format_name=X"
echo "     GET  /resonanz/wrapper/{name}/stats"
echo ""
echo "  📊 STATS & STREAMS"
echo "     GET  /resonanz/stats"
echo "     GET  /resonanz/stats/wrapper/{name}"
echo "     GET  /resonanz/strom?limit=N&stage=X"
echo "     GET  /resonanz/training?limit=N&wrapper=X"
echo ""
echo "  💬 CHAT"
echo "     POST /resonanz/chat"
echo "     GET  /resonanz/history/{request_id}"
echo ""
