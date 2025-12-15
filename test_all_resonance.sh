#!/bin/bash

# SYNTX Field Resonance API - Complete Test Suite
# Tests all 8 Resonanzpunkte + Legacy Endpoints

API_BASE="http://localhost:8001"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo "💎 SYNTX FIELD RESONANCE API - COMPLETE TEST SUITE"
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo ""

# TEST 1: Health Endpoints
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 1: Health Endpoints${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/health${NC}"
curl -s $API_BASE/resonanz/health | jq '.'
echo ""

echo -e "${GREEN}GET /health (legacy)${NC}"
curl -s $API_BASE/health | jq '.'
echo ""

echo -e "${GREEN}GET /api/chat/health (legacy)${NC}"
curl -s $API_BASE/api/chat/health | jq '.'
echo ""

# TEST 2: Wrapper Discovery
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 2: Wrapper Discovery${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/wrappers${NC}"
WRAPPERS=$(curl -s $API_BASE/resonanz/wrappers)
echo "$WRAPPERS" | jq '.'
WRAPPER_COUNT=$(echo "$WRAPPERS" | jq '.wrappers | length')
echo -e "${YELLOW}→ Found $WRAPPER_COUNT wrappers${NC}"
echo ""

# Get first wrapper name for detailed test
FIRST_WRAPPER=$(echo "$WRAPPERS" | jq -r '.wrappers[0].name')
echo -e "${GREEN}GET /resonanz/wrapper/$FIRST_WRAPPER${NC}"
curl -s $API_BASE/resonanz/wrapper/$FIRST_WRAPPER | jq '{name, size_human, last_modified}'
echo ""

# TEST 3: System Stats
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 3: System Statistics${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats${NC}"
STATS=$(curl -s $API_BASE/resonanz/stats)
echo "$STATS" | jq '.'
echo ""

# If we have data, test wrapper-specific stats
TOTAL_REQUESTS=$(echo "$STATS" | jq '.total_requests')
if [ "$TOTAL_REQUESTS" -gt 0 ]; then
    echo -e "${GREEN}GET /resonanz/stats/wrapper/$FIRST_WRAPPER${NC}"
    curl -s $API_BASE/resonanz/stats/wrapper/$FIRST_WRAPPER | jq '.'
    echo ""
fi

# TEST 4: Field Stream
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 4: Field Stream (Recent Events)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/strom?limit=3${NC}"
STROM=$(curl -s "$API_BASE/resonanz/strom?limit=3")
echo "$STROM" | jq '.'
STROM_COUNT=$(echo "$STROM" | jq '.total')
echo -e "${YELLOW}→ Found $STROM_COUNT recent field events${NC}"
echo ""

# TEST 5: Training Data
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 5: Training Data${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/training?limit=3${NC}"
TRAINING=$(curl -s "$API_BASE/resonanz/training?limit=3")
echo "$TRAINING" | jq '.'
TRAINING_COUNT=$(echo "$TRAINING" | jq '.total')
echo -e "${YELLOW}→ Found $TRAINING_COUNT training requests${NC}"
echo ""

# TEST 6: Live Chat Request (SHORT!)
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 6: Live Chat Resonance (SHORT REQUEST)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}POST /resonanz/chat${NC}"
echo -e "${YELLOW}Sending: 'Test' with max_new_tokens=30${NC}"
echo ""

CHAT_RESPONSE=$(curl -s -X POST $API_BASE/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test",
    "max_new_tokens": 30,
    "mode": "syntex_wrapper_human"
  }')

echo "$CHAT_RESPONSE" | jq '{
  response: .response,
  metadata: .metadata,
  field_flow_stages: (.field_flow | length)
}'
echo ""

# Extract request_id for history lookup
REQUEST_ID=$(echo "$CHAT_RESPONSE" | jq -r '.metadata.request_id')
echo -e "${YELLOW}→ Request ID: $REQUEST_ID${NC}"
echo -e "${YELLOW}→ Field Flow Stages: $(echo "$CHAT_RESPONSE" | jq '.field_flow | length')${NC}"
echo ""

# TEST 7: Request History Lookup
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 7: Request History Lookup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/history/$REQUEST_ID${NC}"
curl -s "$API_BASE/resonanz/history/$REQUEST_ID" | jq '{
  request_id,
  total_stages,
  stages: [.stages[] | {stage: .stage, timestamp: .timestamp}]
}'
echo ""

# TEST 8: Legacy Chat Endpoint
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST 8: Legacy Chat Endpoint${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}POST /api/chat (legacy, should have field_flow now!)${NC}"
echo -e "${YELLOW}Sending: 'Legacy Test' with max_new_tokens=20${NC}"
echo ""

LEGACY_RESPONSE=$(curl -s -X POST $API_BASE/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Legacy Test",
    "max_new_tokens": 20
  }')

echo "$LEGACY_RESPONSE" | jq '{
  response: .response,
  metadata: .metadata,
  has_field_flow: (.field_flow != null),
  field_flow_stages: (.field_flow | length)
}'
echo ""

# FINAL STATS CHECK
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}FINAL: Updated System Stats${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

echo -e "${GREEN}GET /resonanz/stats (after tests)${NC}"
curl -s $API_BASE/resonanz/stats | jq '{
  total_requests,
  success_rate,
  average_latency_ms,
  wrapper_usage,
  recent_24h
}'
echo ""

# SUMMARY
echo ""
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo "💎 TEST SUITE COMPLETE!"
echo "🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊"
echo ""
echo -e "${GREEN}✅ Tested Endpoints:${NC}"
echo "   1. GET  /resonanz/health"
echo "   2. GET  /resonanz/wrappers"
echo "   3. GET  /resonanz/wrapper/{name}"
echo "   4. GET  /resonanz/strom"
echo "   5. GET  /resonanz/training"
echo "   6. GET  /resonanz/stats"
echo "   7. GET  /resonanz/stats/wrapper/{name}"
echo "   8. POST /resonanz/chat"
echo "   9. GET  /resonanz/history/{id}"
echo "   + Legacy endpoints (/health, /api/chat)"
echo ""
echo -e "${YELLOW}📊 Check logs at: /opt/syntx-config/logs/${NC}"
echo ""
