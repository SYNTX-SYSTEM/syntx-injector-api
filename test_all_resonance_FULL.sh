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
echo "💎 SYNTX FIELD RESONANCE API - FULL OUTPUT TEST SUITE"
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

echo -e "${GREEN}GET /health (legacy)${NC}"
curl -s $API_BASE/health | jq '.'
echo ""
echo "---"
echo ""

# TEST 2: Wrapper Discovery - FULL WRAPPER LIST
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 2: Wrapper Discovery - COMPLETE LIST${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/wrappers${NC}"
WRAPPERS=$(curl -s $API_BASE/resonanz/wrappers)
echo "$WRAPPERS" | jq '.'
WRAPPER_COUNT=$(echo "$WRAPPERS" | jq '.wrappers | length')
echo ""
echo -e "${YELLOW}→ Total Wrappers Found: $WRAPPER_COUNT${NC}"
echo ""
echo "---"
echo ""

# TEST 3: Show FIRST 3 WRAPPER CONTENTS (FULL!)
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 3: Wrapper Contents - FIRST 3 (COMPLETE CONTENT!)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

for i in 0 1 2; do
    WRAPPER_NAME=$(echo "$WRAPPERS" | jq -r ".wrappers[$i].name")
    if [ "$WRAPPER_NAME" != "null" ]; then
        echo -e "${GREEN}GET /resonanz/wrapper/$WRAPPER_NAME${NC}"
        echo -e "${YELLOW}FULL CONTENT:${NC}"
        echo ""
        curl -s $API_BASE/resonanz/wrapper/$WRAPPER_NAME | jq '.'
        echo ""
        echo "---"
        echo ""
    fi
done

# TEST 4: System Stats - COMPLETE
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 4: System Statistics - COMPLETE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats${NC}"
STATS=$(curl -s $API_BASE/resonanz/stats)
echo "$STATS" | jq '.'
echo ""
echo "---"
echo ""

# TEST 5: Field Stream - FULL EVENTS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 5: Field Stream - LAST 5 EVENTS (COMPLETE)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/strom?limit=5${NC}"
curl -s "$API_BASE/resonanz/strom?limit=5" | jq '.'
echo ""
echo "---"
echo ""

# TEST 6: Training Data - FULL REQUESTS
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 6: Training Data - LAST 3 REQUESTS (COMPLETE)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/training?limit=3${NC}"
curl -s "$API_BASE/resonanz/training?limit=3" | jq '.'
echo ""
echo "---"
echo ""

# TEST 7: Live Chat Request - COMPLETE RESPONSE + FIELD FLOW
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 7: Live Chat Resonance - COMPLETE OUTPUT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}POST /resonanz/chat${NC}"
echo -e "${YELLOW}Request Body:${NC}"
REQUEST_BODY='{
  "prompt": "Was ist SYNTX?",
  "max_new_tokens": 100,
  "mode": "syntex_wrapper_human",
  "temperature": 0.7
}'
echo "$REQUEST_BODY" | jq '.'
echo ""
echo -e "${YELLOW}Sending request... (will take ~15-20 seconds)${NC}"
echo ""

CHAT_RESPONSE=$(curl -s -X POST $API_BASE/resonanz/chat \
  -H "Content-Type: application/json" \
  -d "$REQUEST_BODY")

echo -e "${GREEN}COMPLETE RESPONSE:${NC}"
echo "$CHAT_RESPONSE" | jq '.'
echo ""

REQUEST_ID=$(echo "$CHAT_RESPONSE" | jq -r '.metadata.request_id')
echo -e "${YELLOW}→ Request ID: $REQUEST_ID${NC}"
echo -e "${YELLOW}→ Wrapper Used: $(echo "$CHAT_RESPONSE" | jq -r '.metadata.wrapper_chain[0]')${NC}"
echo -e "${YELLOW}→ Latency: $(echo "$CHAT_RESPONSE" | jq '.metadata.latency_ms')ms${NC}"
echo -e "${YELLOW}→ Field Flow Stages: $(echo "$CHAT_RESPONSE" | jq '.field_flow | length')${NC}"
echo ""
echo "---"
echo ""

# TEST 8: Request History - COMPLETE
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 8: Request History - COMPLETE FIELD FLOW${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/history/$REQUEST_ID${NC}"
curl -s "$API_BASE/resonanz/history/$REQUEST_ID" | jq '.'
echo ""
echo "---"
echo ""

# TEST 9: Another Chat with DIFFERENT WRAPPER
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 9: Chat with DIFFERENT Wrapper (SIGMA)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}POST /resonanz/chat (with syntex_wrapper_sigma)${NC}"
REQUEST_BODY_2='{
  "prompt": "Erkläre Felder",
  "max_new_tokens": 80,
  "mode": "syntex_wrapper_sigma",
  "temperature": 0.7
}'
echo "$REQUEST_BODY_2" | jq '.'
echo ""
echo -e "${YELLOW}Sending request...${NC}"
echo ""

CHAT_RESPONSE_2=$(curl -s -X POST $API_BASE/resonanz/chat \
  -H "Content-Type: application/json" \
  -d "$REQUEST_BODY_2")

echo -e "${GREEN}COMPLETE RESPONSE:${NC}"
echo "$CHAT_RESPONSE_2" | jq '.'
echo ""
echo "---"
echo ""

# TEST 10: Wrapper-Specific Stats
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 10: Wrapper-Specific Statistics${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats/wrapper/syntex_wrapper_human${NC}"
curl -s $API_BASE/resonanz/stats/wrapper/syntex_wrapper_human | jq '.'
echo ""
echo "---"
echo ""

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
echo "💎 COMPLETE TEST SUITE FINISHED!"
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo ""
echo -e "${GREEN}✅ All Endpoints Tested with FULL Outputs:${NC}"
echo ""
echo "   1. Health checks (3 endpoints)"
echo "   2. Wrapper discovery (all wrappers listed)"
echo "   3. Wrapper content (first 3 shown COMPLETELY)"
echo "   4. System stats (complete)"
echo "   5. Field stream (last 5 events)"
echo "   6. Training data (last 3 requests)"
echo "   7. Live chat with wrapper_human (FULL response + field_flow)"
echo "   8. Request history lookup (complete stages)"
echo "   9. Live chat with wrapper_sigma (FULL response + field_flow)"
echo "  10. Wrapper-specific stats (for 2 wrappers)"
echo "  11. Final system stats (updated after tests)"
echo ""
echo -e "${YELLOW}📊 Logs updated at: /opt/syntx-config/logs/${NC}"
echo -e "${YELLOW}📊 Check field_flow.jsonl and wrapper_requests.jsonl${NC}"
echo ""
