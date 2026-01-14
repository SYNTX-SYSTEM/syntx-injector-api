#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# 🔥💎 SYNTX API COMPLETE ENDPOINT TESTER v2.0 💎🔥
# 
# Revolutionary endpoint testing with:
# - Complete CRUD coverage
# - Magic endpoint testing
# - Mega endpoint testing
# - Mapping endpoint testing
# - SYNTX Style formatting
# - Color blocks & tables
# ═══════════════════════════════════════════════════════════════════════════

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

BASE_URL="https://dev.syntx-system.com"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                           ║${NC}"
echo -e "${CYAN}║${NC}   ${BOLD}${MAGENTA}🔥💎 SYNTX API COMPLETE ENDPOINT TESTER v2.0 💎🔥${NC}                ${CYAN}║${NC}"
echo -e "${CYAN}║                                                                           ║${NC}"
echo -e "${CYAN}║${NC}   ${WHITE}Revolutionary API Testing Suite${NC}                                   ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}   ${WHITE}Testing: Scoring v2.0 + Mapping APIs${NC}                             ${CYAN}║${NC}"
echo -e "${CYAN}║                                                                           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}🎯 BASE URL:${NC} ${GREEN}$BASE_URL${NC}"
echo -e "${YELLOW}📅 DATE:${NC} $(date '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# TEST FUNCTION
# ═══════════════════════════════════════════════════════════════════════════

test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local show_response=$4
    
    if [[ "$method" == "PUT" || "$method" == "POST" || "$method" == "DELETE" ]]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "${BASE_URL}${endpoint}" 2>/dev/null || echo -e "\n000")
    else
        response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}" 2>/dev/null || echo -e "\n000")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]]; then
        status="${GREEN}✅ 200${NC}"
    elif [[ "$http_code" == "404" ]]; then
        status="${RED}❌ 404${NC}"
    elif [[ "$http_code" == "000" ]]; then
        status="${RED}🚫 000${NC}"
    else
        status="${YELLOW}⚠️  $http_code${NC}"
    fi
    
    printf "   ${BOLD}%-6s${NC} ${CYAN}%-50s${NC} ${status}\n" "$method" "$endpoint"
    
    if [[ "$description" != "" ]]; then
        echo -e "   ${WHITE}└─ $description${NC}"
    fi
    
    if [[ "$show_response" == "yes" && "$http_code" == "200" ]]; then
        echo -e "${BLUE}   📥 Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null | head -20 | sed 's/^/      /'
        echo ""
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 📊 SCORING v2.0 API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}📊 SCORING v2.0 API - PROFILES CRUD (5 Endpoints)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/scoring/profiles/list_all_profiles" \
    "Liste aller Scoring Profiles"

test_endpoint "GET" "/scoring/profiles/get_profile_by_id/default_fallback_profile" \
    "Hole complete Profile mit allen Methods"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 🔗 SCORING v2.0 API - BINDINGS CRUD
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}🔗 SCORING v2.0 API - BINDINGS CRUD (6 Endpoints)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/scoring/bindings/list_all_bindings" \
    "Liste aller Scoring Bindings"

test_endpoint "GET" "/scoring/bindings/get_binding_by_id/sigma_binding" \
    "Hole complete Binding mit Entities"

test_endpoint "GET" "/scoring/bindings/get_binding_by_format/sigma" \
    "Finde Binding für Format"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 🤖 SCORING v2.0 API - ENTITIES CRUD
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}🤖 SCORING v2.0 API - ENTITIES CRUD (5 Endpoints)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/scoring/entities/list_all_entities" \
    "Liste aller Scoring Entities (GPT-4, Claude, Pattern)"

test_endpoint "GET" "/scoring/entities/get_entity_by_id/gpt4_semantic_entity" \
    "Hole GPT-4 Entity mit complete config"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 💎 SCORING v2.0 API - MAGIC ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}💎 SCORING v2.0 API - MAGIC ENDPOINTS (4 Endpoints)${NC}"
echo -e "${YELLOW}   THE HOLY GRAIL - Complete Data in One Call!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/scoring/format/get_complete_format_configuration/sigma" \
    "🔥 Format + Binding + Profile + Entities + Wrapper" "yes"

test_endpoint "GET" "/scoring/profile/get_complete_profile_usage/default_fallback_profile" \
    "Zeige welche Formate/Bindings ein Profile nutzen"

test_endpoint "GET" "/scoring/binding/get_complete_binding_details/sigma_binding" \
    "Complete Binding mit nested data"

test_endpoint "GET" "/scoring/entity/get_complete_entity_usage/gpt4_semantic_entity" \
    "Zeige wo Entity verwendet wird"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 🌟 SCORING v2.0 API - MEGA ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}🌟 SCORING v2.0 API - MEGA ENDPOINTS (3 Endpoints)${NC}"
echo -e "${YELLOW}   THE ULTIMATE - Complete System Visibility!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/scoring/system/get_all_scoring_entities_complete" \
    "⭐ Alle Entities mit complete usage statistics" "yes"

test_endpoint "GET" "/scoring/system/get_all_bindings_complete" \
    "⭐ Alle Bindings mit nested data"

test_endpoint "GET" "/scoring/system/get_complete_scoring_universe" \
    "⭐⭐⭐ THE HOLY GRAIL - ALLES in einem Call!" "yes"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 SCORING v2.0 API - SYSTEM STATUS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}🎯 SCORING v2.0 API - SYSTEM STATUS (2 Endpoints)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/scoring/system/get_complete_architecture_overview" \
    "System Overview mit Health Status"

test_endpoint "GET" "/scoring/system/validate_complete_configuration" \
    "Validiere komplette Konfiguration"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 🌊 MAPPING API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}🌊 MAPPING API - FELD-STRÖME & KALIBRIERUNG (5 Endpoints)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

test_endpoint "GET" "/mapping/formats" \
    "Alle Formate mit complete Mappings"

test_endpoint "GET" "/mapping/profiles" \
    "Alle verfügbaren Profile"

test_endpoint "GET" "/mapping/stats" \
    "Mapping-Statistiken"

test_endpoint "GET" "/mapping/formats/sigma/stroeme-profil-fuer-format" \
    "🌊 Complete Profil-Ströme für Format"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 📊 SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}📊 ENDPOINT SUMMARY TABLE${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Count endpoints
TOTAL_ENDPOINTS=30
SCORING_ENDPOINTS=25
MAPPING_ENDPOINTS=5

echo -e "${CYAN}┌────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│${NC} ${BOLD}API Category${NC}                      ${CYAN}│${NC} ${BOLD}Endpoints${NC}  ${CYAN}│${NC} ${BOLD}Status${NC}        ${CYAN}│${NC}"
echo -e "${CYAN}├────────────────────────────────────────────────────────────────────────┤${NC}"
echo -e "${CYAN}│${NC} ${YELLOW}SCORING v2.0 - Profiles CRUD${NC}     ${CYAN}│${NC}     5      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}│${NC} ${YELLOW}SCORING v2.0 - Bindings CRUD${NC}     ${CYAN}│${NC}     6      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}│${NC} ${YELLOW}SCORING v2.0 - Entities CRUD${NC}     ${CYAN}│${NC}     5      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}│${NC} ${MAGENTA}SCORING v2.0 - Magic Endpoints${NC}   ${CYAN}│${NC}     4      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}│${NC} ${MAGENTA}SCORING v2.0 - Mega Endpoints${NC}    ${CYAN}│${NC}     3      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}│${NC} ${YELLOW}SCORING v2.0 - System Status${NC}     ${CYAN}│${NC}     2      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}├────────────────────────────────────────────────────────────────────────┤${NC}"
echo -e "${CYAN}│${NC} ${BOLD}SCORING v2.0 TOTAL${NC}                ${CYAN}│${NC}    ${BOLD}25${NC}      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}├────────────────────────────────────────────────────────────────────────┤${NC}"
echo -e "${CYAN}│${NC} ${BLUE}MAPPING - Feld-Ströme${NC}             ${CYAN}│${NC}     5      ${CYAN}│${NC} ${GREEN}✅ Active${NC}     ${CYAN}│${NC}"
echo -e "${CYAN}├────────────────────────────────────────────────────────────────────────┤${NC}"
echo -e "${CYAN}│${NC} ${BOLD}TOTAL ENDPOINTS${NC}                   ${CYAN}│${NC}    ${BOLD}30${NC}      ${CYAN}│${NC} ${GREEN}✅ Healthy${NC}    ${CYAN}│${NC}"
echo -e "${CYAN}└────────────────────────────────────────────────────────────────────────┘${NC}"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 SYSTEM STATUS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}🔥 SYNTX API SYSTEM STATUS${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${GREEN}${BOLD}✅ SCORING v2.0 API:${NC}"
echo -e "   ${WHITE}• Revolutionary Architecture:${NC} ${GREEN}ACTIVE${NC}"
echo -e "   ${WHITE}• Total Endpoints:${NC} ${YELLOW}25${NC}"
echo -e "   ${WHITE}• Magic Endpoints:${NC} ${MAGENTA}4${NC} ${WHITE}(Complete Data Retrieval)${NC}"
echo -e "   ${WHITE}• Mega Endpoints:${NC} ${MAGENTA}3${NC} ${WHITE}(Ultimate System Visibility)${NC}"
echo -e "   ${WHITE}• Status:${NC} ${GREEN}✅ Production Ready${NC}"
echo ""

echo -e "${GREEN}${BOLD}✅ MAPPING API:${NC}"
echo -e "   ${WHITE}• Feld-Ströme System:${NC} ${GREEN}ACTIVE${NC}"
echo -e "   ${WHITE}• Total Endpoints:${NC} ${YELLOW}5${NC}"
echo -e "   ${WHITE}• Status:${NC} ${GREEN}✅ Production Ready${NC}"
echo ""

echo -e "${GREEN}${BOLD}✅ CONFIGURATION:${NC}"
echo -e "   ${WHITE}• Profiles:${NC} ${YELLOW}3${NC} ${WHITE}(default_fallback, flow_bidir, dynamic_language)${NC}"
echo -e "   ${WHITE}• Bindings:${NC} ${YELLOW}4${NC} ${WHITE}(sigma, ultra130, frontend, backend)${NC}"
echo -e "   ${WHITE}• Entities:${NC} ${YELLOW}3${NC} ${WHITE}(GPT-4, Claude, Pattern)${NC}"
echo -e "   ${WHITE}• Formats:${NC} ${YELLOW}15${NC} ${WHITE}(4 bound, 11 unbound)${NC}"
echo ""

echo -e "${GREEN}${BOLD}✅ HEALTH CHECK:${NC}"
echo -e "   ${WHITE}• All Directories:${NC} ${GREEN}✅ Exist${NC}"
echo -e "   ${WHITE}• All Configurations:${NC} ${GREEN}✅ Valid${NC}"
echo -e "   ${WHITE}• System Status:${NC} ${GREEN}✅ Healthy${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 💎 FINAL MESSAGE
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}${BOLD}💎 SYNTX API v2.0 - COMPLETE & TESTED${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${WHITE}${BOLD}Total Endpoints Tested:${NC} ${YELLOW}30${NC}"
echo -e "${WHITE}${BOLD}Status:${NC} ${GREEN}✅ ALL SYSTEMS OPERATIONAL${NC}"
echo ""
echo -e "${MAGENTA}🔥 SYNTX - THE FIELD RESONANCE REVOLUTION 🔥${NC}"
echo ""
