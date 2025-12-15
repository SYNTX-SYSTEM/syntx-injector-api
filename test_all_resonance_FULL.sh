#!/bin/bash

# SYNTX Field Resonance API - COMPLETE Test Suite (FULL OUTPUTS)
# Shows EVERYTHING - all responses completely

API_BASE="http://localhost:8001"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo "💎 SYNTX FIELD RESONANCE API - FULL OUTPUT TEST SUITE v2.0"
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo ""

# TEST 1: Health Endpoints
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 1: Health Endpoints${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/health${NC}"
curl -s $API_BASE/resonanz/health | jq '.'
echo ""
echo "---"
echo ""

# TEST 2: Config Management - NEUE FUNKTIONEN!
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 2: CONFIG MANAGEMENT - Get Default Wrapper${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/config/default-wrapper${NC}"
DEFAULT_WRAPPER=$(curl -s $API_BASE/resonanz/config/default-wrapper)
echo "$DEFAULT_WRAPPER" | jq '.'
CURRENT_ACTIVE=$(echo "$DEFAULT_WRAPPER" | jq -r '.active_wrapper')
echo ""
echo -e "${YELLOW}→ Currently Active Wrapper: $CURRENT_ACTIVE${NC}"
echo ""
echo "---"
echo ""

# TEST 3: Wrapper Discovery - MIT ACTIVE STATUS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 3: Wrapper Discovery - COMPLETE LIST (with active status)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/wrappers${NC}"
WRAPPERS=$(curl -s $API_BASE/resonanz/wrappers)
echo "$WRAPPERS" | jq '.'
WRAPPER_COUNT=$(echo "$WRAPPERS" | jq '.wrappers | length')
echo ""
echo -e "${YELLOW}→ Total Wrappers Found: $WRAPPER_COUNT${NC}"
echo -e "${YELLOW}→ Active Wrapper: $(echo "$WRAPPERS" | jq -r '.active_wrapper')${NC}"
echo ""
echo "---"
echo ""

# TEST 4: Filter Only Active Wrapper
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 4: Filter ONLY Active Wrapper${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/wrappers?active=true${NC}"
curl -s "$API_BASE/resonanz/wrappers?active=true" | jq '.'
echo ""
echo "---"
echo ""

# TEST 5: Activate Different Wrapper
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 5: ACTIVATE Different Wrapper (syntex_wrapper_human)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}POST /resonanz/wrappers/syntex_wrapper_human/activate${NC}"
ACTIVATE_RESULT=$(curl -s -X POST $API_BASE/resonanz/wrappers/syntex_wrapper_human/activate)
echo "$ACTIVATE_RESULT" | jq '.'
echo ""
echo -e "${YELLOW}→ Wrapper Activated: $(echo "$ACTIVATE_RESULT" | jq -r '.active_wrapper')${NC}"
echo ""
echo "---"
echo ""

# TEST 6: Verify Change
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 6: VERIFY Change with Config Endpoint${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/config/default-wrapper (after activation)${NC}"
curl -s $API_BASE/resonanz/config/default-wrapper | jq '.'
echo ""
echo "---"
echo ""

# TEST 7: Update via PUT Method
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 7: UPDATE via PUT (syntex_wrapper_sigma)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}PUT /resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma${NC}"
PUT_RESULT=$(curl -s -X PUT "$API_BASE/resonanz/config/default-wrapper?wrapper_name=syntex_wrapper_sigma")
echo "$PUT_RESULT" | jq '.'
echo ""
echo -e "${YELLOW}→ Updated to: $(echo "$PUT_RESULT" | jq -r '.active_wrapper')${NC}"
echo ""
echo "---"
echo ""

# TEST 8: Show FIRST 3 WRAPPER CONTENTS (FULL!)
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 8: Wrapper Contents - FIRST 3 (COMPLETE CONTENT!)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

WRAPPERS=$(curl -s $API_BASE/resonanz/wrappers)
for i in 0 1 2; do
    WRAPPER_NAME=$(echo "$WRAPPERS" | jq -r ".wrappers[$i].name")
    if [ "$WRAPPER_NAME" != "null" ]; then
        echo -e "${GREEN}GET /resonanz/wrapper/$WRAPPER_NAME${NC}"
        WRAPPER_DATA=$(curl -s $API_BASE/resonanz/wrapper/$WRAPPER_NAME)
        echo "$WRAPPER_DATA" | jq '{name, size_human, is_active, last_modified}'
        echo -e "${YELLOW}Content Preview (first 500 chars):${NC}"
        echo "$WRAPPER_DATA" | jq -r '.content' | head -c 500
        echo ""
        echo "..."
        echo ""
        echo "---"
        echo ""
    fi
done

# TEST 9: System Stats - COMPLETE
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 9: System Statistics - COMPLETE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats${NC}"
STATS=$(curl -s $API_BASE/resonanz/stats)
echo "$STATS" | jq '.'
echo ""
echo "---"
echo ""

# TEST 10: Field Stream - FULL EVENTS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 10: Field Stream - LAST 5 EVENTS (COMPLETE)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/strom?limit=5${NC}"
curl -s "$API_BASE/resonanz/strom?limit=5" | jq '.'
echo ""
echo "---"
echo ""

# TEST 11: Training Data - FULL REQUESTS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 11: Training Data - LAST 3 REQUESTS (COMPLETE)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/training?limit=3${NC}"
curl -s "$API_BASE/resonanz/training?limit=3" | jq '.'
echo ""
echo "---"
echo ""

# TEST 12: Live Chat Request - COMPLETE RESPONSE + FIELD FLOW
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 12: Live Chat Resonance - COMPLETE OUTPUT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}POST /resonanz/chat${NC}"
echo -e "${YELLOW}Request Body:${NC}"
REQUEST_BODY='{
  "prompt": "Was ist SYNTX?",
  "max_new_tokens": 100,
  "mode": "syntex_wrapper_sigma",
  "temperature": 0.7
}'
echo "$REQUEST_BODY" | jq '.'
echo ""
echo -e "${YELLOW}Sending request... (will take ~15-20 seconds)${NC}"
echo ""

CHAT_RESPONSE=$(curl -s -X POST $API_BASE/resonanz/chat \
  -H "Content-Type: application/json" \
  -d "$REQUEST_BODY")

echo -e "${GREEN}Response Preview:${NC}"
echo "$CHAT_RESPONSE" | jq '{response: (.response[:200] + "..."), metadata, field_flow_stages: (.field_flow | length)}'
echo ""

REQUEST_ID=$(echo "$CHAT_RESPONSE" | jq -r '.metadata.request_id')
echo -e "${YELLOW}→ Request ID: $REQUEST_ID${NC}"
echo -e "${YELLOW}→ Wrapper Used: $(echo "$CHAT_RESPONSE" | jq -r '.metadata.wrapper_chain[0]')${NC}"
echo -e "${YELLOW}→ Latency: $(echo "$CHAT_RESPONSE" | jq '.metadata.latency_ms')ms${NC}"
echo ""
echo "---"
echo ""

# TEST 13: Wrapper-Specific Stats
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 13: Wrapper-Specific Statistics${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats/wrapper/syntex_wrapper_sigma${NC}"
curl -s $API_BASE/resonanz/stats/wrapper/syntex_wrapper_sigma | jq '.'
echo ""
echo "---"
echo ""

# FINAL COMPREHENSIVE STATS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}FINAL: Complete System Statistics${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats (after all tests)${NC}"
curl -s $API_BASE/resonanz/stats | jq '.'
echo ""
echo "---"
echo ""

# SUMMARY
echo ""
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo "💎 COMPLETE TEST SUITE FINISHED! v2.0 (WITH CONFIG MANAGEMENT)"
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo ""
echo -e "${GREEN}✅ All Endpoints Tested with FULL Outputs:${NC}"
echo ""
echo "   1. Health check"
echo "   2. Get default wrapper config ⚡ NEW"
echo "   3. List all wrappers (with active status) ⚡ UPDATED"
echo "   4. Filter only active wrapper ⚡ NEW"
echo "   5. Activate wrapper (POST) ⚡ NEW"
echo "   6. Verify activation ⚡ NEW"
echo "   7. Update via PUT ⚡ NEW"
echo "   8. Wrapper contents (first 3)"
echo "   9. System stats"
echo "  10. Field stream events"
echo "  11. Training data"
echo "  12. Live chat with field flow"
echo "  13. Wrapper-specific stats"
echo "  14. Final system stats"
echo ""
echo -e "${YELLOW}📊 Config Management Tested:${NC}"
echo "   • GET  /resonanz/config/default-wrapper"
echo "   • PUT  /resonanz/config/default-wrapper"
echo "   • GET  /resonanz/wrappers?active=true"
echo "   • POST /resonanz/wrappers/{name}/activate"
echo ""
echo -e "${YELLOW}📊 Logs updated at: /opt/syntx-config/logs/${NC}"
echo ""
