#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                                                                           ║
# ║   ███████╗██╗   ██╗███╗   ██╗████████╗██╗  ██╗                            ║
# ║   ██╔════╝╚██╗ ██╔╝████╗  ██║╚══██╔══╝╚██╗██╔╝                            ║
# ║   ███████╗ ╚████╔╝ ██╔██╗ ██║   ██║    ╚███╔╝                             ║
# ║   ╚════██║  ╚██╔╝  ██║╚██╗██║   ██║    ██╔██╗                             ║
# ║   ███████║   ██║   ██║ ╚████║   ██║   ██╔╝ ██╗                            ║
# ║   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝                            ║
# ║                                                                           ║
# ║   🔮 SYNTX API EXPLORER v3.4                                              ║
# ║   ─────────────────────────────────────────────────────                   ║
# ║   Complete Endpoint Documentation | Full JSON Display                     ║
# ║                                                                           ║
# ║   "See every field. Understand every resonance."                          ║
# ║                                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# ============================================================================
# 🎨 COLORS
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m'
BOLD='\033[1m'
DIM='\033[2m'

# ============================================================================
# ⚙️ CONFIGURATION
# ============================================================================
BASE_URL="https://dev.syntx-system.com"
OUTPUT_FILE="syntx_api_documentation_$(date +%Y%m%d_%H%M%S).json"

# ============================================================================
# 📊 FUNCTIONS
# ============================================================================

print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_endpoint() {
    echo -e "${CYAN}➤ $1${NC}"
    echo -e "   ${DIM}Method:${NC} ${YELLOW}$2${NC}"
    echo -e "   ${DIM}Endpoint:${NC} ${GREEN}$BASE_URL$3${NC}"
    if [ -n "$4" ]; then
        echo -e "   ${DIM}Request Body:${NC}"
        echo "$4" | jq . 2>/dev/null || echo "   $4"
    fi
}

print_response() {
    echo -e "   ${DIM}Response:${NC}"
    echo "$1" | jq . 2>/dev/null || echo "   $1"
    echo ""
}

make_request() {
    local method="$1"
    local endpoint="$2"
    local body="$3"
    
    echo -e "${GRAY}   Calling endpoint...${NC}"
    
    if [ -n "$body" ]; then
        response=$(curl -s -w "\n⏱%{http_code}⏱%{time_total}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$body" \
            "$BASE_URL$endpoint" 2>/dev/null)
    else
        response=$(curl -s -w "\n⏱%{http_code}⏱%{time_total}" -X "$method" \
            "$BASE_URL$endpoint" 2>/dev/null)
    fi
    
    # Split response and status code
    local http_code=$(echo "$response" | grep -o '⏱[0-9]*⏱' | sed 's/⏱//g' | head -1)
    local time_taken=$(echo "$response" | grep -o '⏱[0-9]*\.[0-9]*$' | sed 's/⏱//g')
    local body_response=$(echo "$response" | sed '/⏱[0-9]*⏱/d' | sed '/⏱[0-9]*\.[0-9]*$/d')
    
    echo -e "   ${DIM}Status:${NC} ${WHITE}$http_code${NC} ${DIM}| Time:${NC} ${WHITE}${time_taken}s${NC}"
    
    echo "$body_response"
}

# ============================================================================
# 🚀 MAIN EXPLORATION
# ============================================================================

echo ""
echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}                                                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${WHITE}🔮 SYNTX API EXPLORER v3.4${NC}                                              ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}   ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${DIM}Target:${NC} ${YELLOW}$BASE_URL${NC}                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${DIM}Output:${NC} ${GREEN}$OUTPUT_FILE${NC}                                         ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Start JSON documentation
echo "{\"timestamp\": \"$(date -Iseconds)\"," > "$OUTPUT_FILE"
echo "\"base_url\": \"$BASE_URL\"," >> "$OUTPUT_FILE"
echo "\"endpoints\": [" >> "$OUTPUT_FILE"

# ============================================================================
# 🏥 1. HEALTH ENDPOINTS
# ============================================================================
print_section "🏥 HEALTH ENDPOINTS"

endpoint_data=""

# 1.1 GET /health
print_endpoint "System Health Check" "GET" "/health"
response=$(make_request "GET" "/health")
print_response "$response"
endpoint_data="{\"name\": \"System Health Check\", \"method\": \"GET\", \"endpoint\": \"/health\", \"response\": $response}"

# 1.2 GET /resonanz/health
print_endpoint "Field Resonance Health" "GET" "/resonanz/health"
response=$(make_request "GET" "/resonanz/health")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"Field Resonance Health\", \"method\": \"GET\", \"endpoint\": \"/resonanz/health\", \"response\": $response}"

# 1.3 GET /resonanz/health/wrappers
print_endpoint "Wrapper Health Scan" "GET" "/resonanz/health/wrappers"
response=$(make_request "GET" "/resonanz/health/wrappers")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"Wrapper Health Scan\", \"method\": \"GET\", \"endpoint\": \"/resonanz/health/wrappers\", \"response\": $response}"

# ============================================================================
# 📦 2. WRAPPER ENDPOINTS
# ============================================================================
print_section "📦 WRAPPER ENDPOINTS"

# 2.1 GET /resonanz/wrappers
print_endpoint "List All Wrappers" "GET" "/resonanz/wrappers"
response=$(make_request "GET" "/resonanz/wrappers")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"List All Wrappers\", \"method\": \"GET\", \"endpoint\": \"/resonanz/wrappers\", \"response\": $response}"

# Extract first wrapper for detailed tests
first_wrapper=$(echo "$response" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$first_wrapper" ]; then
    # 2.2 GET /resonanz/wrapper/{name}
    print_endpoint "Get Wrapper Content" "GET" "/resonanz/wrapper/$first_wrapper"
    response=$(make_request "GET" "/resonanz/wrapper/$first_wrapper")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Get Wrapper Content\", \"method\": \"GET\", \"endpoint\": \"/resonanz/wrapper/$first_wrapper\", \"response\": $response}"
    
    # 2.3 GET /resonanz/wrapper/{name}/meta
    print_endpoint "Get Wrapper Metadata" "GET" "/resonanz/wrapper/$first_wrapper/meta"
    response=$(make_request "GET" "/resonanz/wrapper/$first_wrapper/meta")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Get Wrapper Metadata\", \"method\": \"GET\", \"endpoint\": \"/resonanz/wrapper/$first_wrapper/meta\", \"response\": $response}"
fi

# ============================================================================
# 📄 3. FORMAT ENDPOINTS
# ============================================================================
print_section "📄 FORMAT ENDPOINTS"

# 3.1 GET /resonanz/formats
print_endpoint "List All Formats" "GET" "/resonanz/formats"
response=$(make_request "GET" "/resonanz/formats")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"List All Formats\", \"method\": \"GET\", \"endpoint\": \"/resonanz/formats\", \"response\": $response}"

# Extract first format for detailed tests
first_format=$(echo "$response" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$first_format" ]; then
    # 3.2 GET /resonanz/formats/{name}
    print_endpoint "Get Format Details" "GET" "/resonanz/formats/$first_format"
    response=$(make_request "GET" "/resonanz/formats/$first_format")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Get Format Details\", \"method\": \"GET\", \"endpoint\": \"/resonanz/formats/$first_format\", \"response\": $response}"
fi

# ============================================================================
# 🎨 4. STYLE ENDPOINTS
# ============================================================================
print_section "🎨 STYLE ENDPOINTS"

# 4.1 GET /resonanz/styles
print_endpoint "List All Styles" "GET" "/resonanz/styles"
response=$(make_request "GET" "/resonanz/styles")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"List All Styles\", \"method\": \"GET\", \"endpoint\": \"/resonanz/styles\", \"response\": $response}"

# Extract first style for detailed tests
first_style=$(echo "$response" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$first_style" ]; then
    # 4.2 GET /resonanz/styles/{name}
    print_endpoint "Get Style Details" "GET" "/resonanz/styles/$first_style"
    response=$(make_request "GET" "/resonanz/styles/$first_style")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Get Style Details\", \"method\": \"GET\", \"endpoint\": \"/resonanz/styles/$first_style\", \"response\": $response}"
    
    # 4.3 POST /resonanz/alchemy/preview
    request_body="{\"text\": \"Das ist ein wichtiger Test der Transmutation\", \"style\": \"$first_style\"}"
    print_endpoint "Alchemy Preview" "POST" "/resonanz/alchemy/preview" "$request_body"
    response=$(make_request "POST" "/resonanz/alchemy/preview" "$request_body")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Alchemy Preview\", \"method\": \"POST\", \"endpoint\": \"/resonanz/alchemy/preview\", \"request\": $request_body, \"response\": $response}"
fi

# ============================================================================
# 📊 5. STATS ENDPOINTS
# ============================================================================
print_section "📊 STATISTICS ENDPOINTS"

# 5.1 GET /resonanz/stats
print_endpoint "Global Statistics" "GET" "/resonanz/stats"
response=$(make_request "GET" "/resonanz/stats")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"Global Statistics\", \"method\": \"GET\", \"endpoint\": \"/resonanz/stats\", \"response\": $response}"

# 5.2 GET /resonanz/strom
print_endpoint "Field Flow Stream" "GET" "/resonanz/strom?limit=3"
response=$(make_request "GET" "/resonanz/strom?limit=3")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"Field Flow Stream\", \"method\": \"GET\", \"endpoint\": \"/resonanz/strom\", \"response\": $response}"

# ============================================================================
# 📼 6. SESSION ENDPOINTS
# ============================================================================
print_section "📼 SESSION ENDPOINTS"

# 6.1 GET /resonanz/sessions
print_endpoint "List Sessions" "GET" "/resonanz/sessions?limit=3"
response=$(make_request "GET" "/resonanz/sessions?limit=3")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"List Sessions\", \"method\": \"GET\", \"endpoint\": \"/resonanz/sessions\", \"response\": $response}"

# Extract first session ID if available
session_id=$(echo "$response" | grep -o '"request_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$session_id" ]; then
    # 6.2 GET /resonanz/session/{id}
    print_endpoint "Get Session Details" "GET" "/resonanz/session/$session_id"
    response=$(make_request "GET" "/resonanz/session/$session_id")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Get Session Details\", \"method\": \"GET\", \"endpoint\": \"/resonanz/session/$session_id\", \"response\": $response}"
fi

# ============================================================================
# 💬 7. CHAT ENDPOINTS
# ============================================================================
print_section "💬 CHAT ENDPOINTS"

# 7.1 POST /resonanz/chat (Main Endpoint)
if [ -n "$first_wrapper" ] && [ -n "$first_format" ]; then
    request_body="{\"prompt\": \"Was ist SYNTX Field Resonance?\", \"mode\": \"$first_wrapper\", \"format\": \"$first_format\", \"style\": \"${first_style:-wissenschaftlich}\", \"max_new_tokens\": 150}"
    print_endpoint "Field Resonance Chat" "POST" "/resonanz/chat" "$request_body"
    response=$(make_request "POST" "/resonanz/chat" "$request_body")
    print_response "$response"
    echo "$endpoint_data," >> "$OUTPUT_FILE"
    endpoint_data="{\"name\": \"Field Resonance Chat\", \"method\": \"POST\", \"endpoint\": \"/resonanz/chat\", \"request\": $request_body, \"response\": $response}"
fi

# 7.2 POST /resonanz/chat/diff
if [ -n "$first_wrapper" ]; then
    # Get second wrapper
    wrappers_response=$(make_request "GET" "/resonanz/wrappers")
    second_wrapper=$(echo "$wrappers_response" | grep -o '"name":"[^"]*"' | head -2 | tail -1 | cut -d'"' -f4)
    
    if [ -n "$second_wrapper" ]; then
        request_body="{\"prompt\": \"Analysiere das Konzept der Zeit\", \"wrappers\": [\"$first_wrapper\", \"$second_wrapper\"], \"max_new_tokens\": 100}"
        print_endpoint "Wrapper Comparison" "POST" "/resonanz/chat/diff" "$request_body"
        response=$(make_request "POST" "/resonanz/chat/diff" "$request_body")
        print_response "$response"
        echo "$endpoint_data," >> "$OUTPUT_FILE"
        endpoint_data="{\"name\": \"Wrapper Comparison\", \"method\": \"POST\", \"endpoint\": \"/resonanz/chat/diff\", \"request\": $request_body, \"response\": $response}"
    fi
fi

# ============================================================================
# ⚙️ 8. CONFIG ENDPOINTS
# ============================================================================
print_section "⚙️ CONFIGURATION ENDPOINTS"

# 8.1 GET /resonanz/config/default-wrapper
print_endpoint "Get Default Wrapper" "GET" "/resonanz/config/default-wrapper"
response=$(make_request "GET" "/resonanz/config/default-wrapper")
print_response "$response"
echo "$endpoint_data," >> "$OUTPUT_FILE"
endpoint_data="{\"name\": \"Get Default Wrapper\", \"method\": \"GET\", \"endpoint\": \"/resonanz/config/default-wrapper\", \"response\": $response}"

# ============================================================================
# 📋 9. COMPLETE ENDPOINT LISTING
# ============================================================================
print_section "📋 ALL AVAILABLE ENDPOINTS"

echo -e "${WHITE}Based on the SYNTX documentation, here are all public endpoints:${NC}"
echo ""
echo -e "${CYAN}🏥 HEALTH & MONITORING${NC}"
echo -e "  ${GREEN}/health${NC}                    - System health check"
echo -e "  ${GREEN}/resonanz/health${NC}          - Field resonance health"
echo -e "  ${GREEN}/resonanz/health/wrappers${NC} - Wrapper health scan"
echo ""
echo -e "${CYAN}📦 WRAPPER OPERATIONS${NC}"
echo -e "  ${GREEN}/resonanz/wrappers${NC}        - List all wrappers"
echo -e "  ${GREEN}/resonanz/wrappers/full${NC}   - Full wrapper details"
echo -e "  ${GREEN}/resonanz/wrapper/{name}${NC}  - Get specific wrapper"
echo -e "  ${GREEN}/resonanz/wrapper/{name}/meta${NC} - Get wrapper metadata"
echo -e "  ${GREEN}/resonanz/wrapper/{name}/format${NC} - Bind format to wrapper"
echo ""
echo -e "${CYAN}📄 FORMAT OPERATIONS${NC}"
echo -e "  ${GREEN}/resonanz/formats${NC}         - List all formats"
echo -e "  ${GREEN}/resonanz/formats/{name}${NC}  - Get specific format"
echo ""
echo -e "${CYAN}🎨 STYLE OPERATIONS${NC}"
echo -e "  ${GREEN}/resonanz/styles${NC}          - List all styles"
echo -e "  ${GREEN}/resonanz/styles/{name}${NC}   - Get specific style"
echo -e "  ${GREEN}/resonanz/alchemy/preview${NC} - Preview style transmutation"
echo ""
echo -e "${CYAN}📊 STATISTICS${NC}"
echo -e "  ${GREEN}/resonanz/stats${NC}           - Global statistics"
echo -e "  ${GREEN}/resonanz/strom${NC}           - Field flow stream"
echo -e "  ${GREEN}/resonanz/training${NC}        - Training data export"
echo -e "  ${GREEN}/resonanz/stats/wrapper/{name}${NC} - Wrapper-specific stats"
echo ""
echo -e "${CYAN}📼 SESSIONS${NC}"
echo -e "  ${GREEN}/resonanz/sessions${NC}        - List sessions"
echo -e "  ${GREEN}/resonanz/session/{id}${NC}    - Get session details"
echo -e "  ${GREEN}/resonanz/session/{id}/replay${NC} - Get replay parameters"
echo ""
echo -e "${CYAN}💬 CHAT${NC}"
echo -e "  ${GREEN}/resonanz/chat${NC}            - Main chat endpoint"
echo -e "  ${GREEN}/resonanz/chat/diff${NC}       - Wrapper comparison"
echo ""
echo -e "${CYAN}⚙️ CONFIGURATION${NC}"
echo -e "  ${GREEN}/resonanz/config/default-wrapper${NC} - Get/set default wrapper"
echo ""
echo -e "${CYAN}🔧 ADMIN${NC}"
echo -e "  ${GREEN}/resonanz/health/fix${NC}      - Auto-fix orphaned wrappers"
echo ""

# ============================================================================
# 💾 SAVE TO FILE
# ============================================================================
echo "$endpoint_data" >> "$OUTPUT_FILE"
echo "]}" >> "$OUTPUT_FILE"

echo -e "${GREEN}✓${NC} Complete API documentation saved to: ${YELLOW}$OUTPUT_FILE${NC}"
echo ""
echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}                                                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${WHITE}🔮 EXPLORATION COMPLETE${NC}                                                  ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}   ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${CYAN}•${NC} ${WHITE}15+ endpoints explored${NC}                                         ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${CYAN}•${NC} ${WHITE}Full JSON requests/responses captured${NC}                          ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${CYAN}•${NC} ${WHITE}Complete endpoint listing documented${NC}                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}   ${GRAY}\"See every field. Understand every resonance.\"${NC}                           ${PURPLE}║${NC}"
echo -e "${PURPLE}║${NC}                                                                           ${PURPLE}║${NC}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
