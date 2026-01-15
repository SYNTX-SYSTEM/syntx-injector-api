#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
#  🔥💎⚡ SYNTX GPT AUTO-TRIGGER - COMPLETE FLOW TEST ⚡💎🔥
# ═══════════════════════════════════════════════════════════════════════════════
#
#  ZWECK:
#    Vollständiger Test des GPT Auto-Trigger Systems
#    VOLLTEXT von ALLEM - Mistral & GPT Request/Response
#
#  FLOW:
#    1. Mistral Wrapper Build (Input Kalibrierung)
#    2. Mistral API Call → VOLLTEXT REQUEST
#    3. Mistral Response → VOLLTEXT RESPONSE
#    4. File Saving (Prompt + Meta + Response)
#    5. GPT Auto-Trigger Detection
#    6. GPT Prompt Build → VOLLTEXT REQUEST
#    7. GPT API Call → VOLLTEXT RESPONSE
#    8. Drift Result → VOLLTEXT SCORES
#
#  OUTPUT:
#    📤 MISTRAL REQUEST: Kompletter JSON Payload
#    📥 MISTRAL RESPONSE: Kompletter generierter Text
#    📤 GPT REQUEST: Kompletter Prompt (System + User + Fields)
#    📥 GPT RESPONSE: Komplette Field Scores + Analysis
#    📁 Alle Files mit komplettem Inhalt
#    🚨 Alle Errors mit Stack Traces
#
#  DER STROM FLIESST. DIE FELDER RESONIEREN. KEIN DRIFT.
#
# ═══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# ─────────────────────────────────────────────────────────────────────────────
#  🎨 SYNTX CHARLOTTENBURG STYLE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
RESET='\033[0m'

print_header() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}║${RESET}${WHITE}  $1${RESET}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${MAGENTA}─────────────────────────────────────────────────────────────────────────────${RESET}"
    echo -e "${YELLOW}  $1${RESET}"
    echo -e "${MAGENTA}─────────────────────────────────────────────────────────────────────────────${RESET}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${RESET}"
}

print_error() {
    echo -e "${RED}❌ $1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${RESET}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${RESET}"
}

print_file() {
    local filepath=$1
    local description=$2
    echo ""
    echo -e "${BLUE}┌─ 📄 FILE ────────────────────────────────────────────────────────────────┐${RESET}"
    echo -e "${BLUE}│${RESET} ${WHITE}$filepath${RESET}"
    echo -e "${BLUE}│${RESET} ${CYAN}$description${RESET}"
    echo -e "${BLUE}└──────────────────────────────────────────────────────────────────────────┘${RESET}"
}

print_box() {
    local title=$1
    local content=$2
    local color=${3:-$MAGENTA}
    
    echo ""
    echo -e "${color}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${RESET}"
    echo -e "${color}┃${RESET} ${WHITE}$title${RESET}"
    echo -e "${color}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${RESET}"
    echo ""
    echo -e "${GRAY}$content${RESET}"
    echo ""
}

print_json_pretty() {
    local json=$1
    echo "$json" | jq '.' 2>/dev/null || echo "$json"
}

# ─────────────────────────────────────────────────────────────────────────────
#  ⚙️  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

API_BASE="http://localhost:8001"
TEST_PROMPT="Analysiere die semantische Drift in einem neuronalen Netzwerk während des Trainings. Erkläre den Mechanismus, die Frequenz und die Dichte der Verschiebung."
WRAPPER_MODE="syntex_wrapper_sigma"
FORMAT_NAME="sigma"
MAX_TOKENS=300

TIMESTAMP=$(date +%s)
LOG_FILE="/tmp/syntx_gpt_test_${TIMESTAMP}.log"

# ─────────────────────────────────────────────────────────────────────────────
#  🚀 MAIN TEST FLOW
# ─────────────────────────────────────────────────────────────────────────────

main() {
    clear
    
    print_header "🔥💎⚡ SYNTX GPT AUTO-TRIGGER - COMPLETE FLOW TEST ⚡💎🔥"
    
    echo -e "${CYAN}┌─ Test Configuration ─────────────────────────────────────────────────────┐${RESET}"
    echo -e "${CYAN}│${RESET} API Base:     ${WHITE}$API_BASE${RESET}"
    echo -e "${CYAN}│${RESET} Wrapper:      ${WHITE}$WRAPPER_MODE${RESET}"
    echo -e "${CYAN}│${RESET} Format:       ${WHITE}$FORMAT_NAME${RESET}"
    echo -e "${CYAN}│${RESET} Max Tokens:   ${WHITE}$MAX_TOKENS${RESET}"
    echo -e "${CYAN}│${RESET} Log File:     ${WHITE}$LOG_FILE${RESET}"
    echo -e "${CYAN}└───────────────────────────────────────────────────────────────────────────┘${RESET}"
    echo ""
    echo -e "${CYAN}┌─ Test Prompt ─────────────────────────────────────────────────────────────┐${RESET}"
    echo -e "${CYAN}│${RESET} ${WHITE}$TEST_PROMPT${RESET}"
    echo -e "${CYAN}└───────────────────────────────────────────────────────────────────────────┘${RESET}"
    echo ""
    
    # Start logging
    exec > >(tee -a "$LOG_FILE")
    exec 2>&1
    
    print_info "Full log: $LOG_FILE"
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 1: PRE-FLIGHT CHECKS
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "1️⃣ PRE-FLIGHT CHECKS"
    
    check_service_running
    check_openai_key
    check_binding_config
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 2: MISTRAL API CALL - VOLLTEXT REQUEST
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "2️⃣ MISTRAL API CALL"
    
    REQUEST_PAYLOAD=$(cat <<EOF
{
  "prompt": "$TEST_PROMPT",
  "mode": "$WRAPPER_MODE",
  "format": "$FORMAT_NAME",
  "max_new_tokens": $MAX_TOKENS
}
EOF
)
    
    print_box "📤 MISTRAL REQUEST - VOLLTEXT" "$(print_json_pretty "$REQUEST_PAYLOAD")" "$BLUE"
    
    print_info "POST $API_BASE/resonanz/chat"
    print_info "Content-Type: application/json"
    echo ""
    
    RESPONSE_FILE="/tmp/syntx_response_${TIMESTAMP}.json"
    
    print_info "Sending request..."
    START_TIME=$(date +%s%3N)
    
    HTTP_CODE=$(curl -s -o "$RESPONSE_FILE" -w "%{http_code}" \
        -X POST "$API_BASE/resonanz/chat" \
        -H "Content-Type: application/json" \
        -d "$REQUEST_PAYLOAD")
    
    END_TIME=$(date +%s%3N)
    LATENCY=$((END_TIME - START_TIME))
    
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_success "HTTP $HTTP_CODE OK (${LATENCY}ms)"
    else
        print_error "HTTP $HTTP_CODE - Request failed"
        cat "$RESPONSE_FILE"
        exit 1
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 3: MISTRAL RESPONSE - VOLLTEXT
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "3️⃣ MISTRAL RESPONSE - VOLLTEXT"
    
    FULL_RESPONSE=$(cat "$RESPONSE_FILE")
    MISTRAL_RESPONSE=$(echo "$FULL_RESPONSE" | jq -r '.response')
    METADATA=$(echo "$FULL_RESPONSE" | jq '.metadata')
    GPT_SCORES=$(echo "$FULL_RESPONSE" | jq '.metadata.gpt_auto_scoring // empty')
    
    print_box "📥 MISTRAL RESPONSE - KOMPLETTER TEXT" "$MISTRAL_RESPONSE" "$GREEN"
    
    print_box "📊 RESPONSE METADATA - VOLLTEXT" "$(print_json_pretty "$METADATA")" "$CYAN"
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 4: FILE SYSTEM INSPECTION - VOLLTEXT FILES
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "4️⃣ GENERATED FILES - VOLLTEXT CONTENT"
    
    PROMPTS_DIR="/opt/syntx-config/prompts_generated"
    DRIFT_DIR="/opt/syntx-config/drift_results"
    
    # Find most recent files (within last 2 minutes)
    LATEST_PROMPT=$(find "$PROMPTS_DIR" -name "*.txt" -type f -not -name "*.response.txt" -newermt "2 minutes ago" 2>/dev/null | head -1)
    LATEST_META=$(find "$PROMPTS_DIR" -name "*.meta.json" -type f -newermt "2 minutes ago" 2>/dev/null | head -1)
    LATEST_RESPONSE=$(find "$PROMPTS_DIR" -name "*.response.txt" -type f -newermt "2 minutes ago" 2>/dev/null | head -1)
    LATEST_DRIFT=$(find "$DRIFT_DIR" -name "*_drift_*.json" -type f -newermt "2 minutes ago" 2>/dev/null | head -1)
    
    # ─────────────────────────────────────────────────────────────────────────
    #  MISTRAL PROMPT FILE - VOLLTEXT
    # ─────────────────────────────────────────────────────────────────────────
    
    if [ -n "$LATEST_PROMPT" ] && [ -f "$LATEST_PROMPT" ]; then
        print_file "$LATEST_PROMPT" "Mistral Prompt - Kompletter kalibrierter Prompt"
        
        PROMPT_CONTENT=$(cat "$LATEST_PROMPT")
        PROMPT_SIZE=$(wc -c < "$LATEST_PROMPT")
        
        print_box "📝 MISTRAL PROMPT - VOLLTEXT (${PROMPT_SIZE} bytes)" "$PROMPT_CONTENT" "$YELLOW"
    else
        print_warning "Prompt file not found (too old or not created)"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    #  META FILE - VOLLTEXT
    # ─────────────────────────────────────────────────────────────────────────
    
    if [ -n "$LATEST_META" ] && [ -f "$LATEST_META" ]; then
        print_file "$LATEST_META" "Metadata - Vollständige Request Information"
        
        META_CONTENT=$(cat "$LATEST_META" | jq '.')
        print_box "📋 METADATA FILE - VOLLTEXT" "$META_CONTENT" "$CYAN"
    else
        print_warning "Meta file not found"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    #  MISTRAL RESPONSE FILE - VOLLTEXT
    # ─────────────────────────────────────────────────────────────────────────
    
    if [ -n "$LATEST_RESPONSE" ] && [ -f "$LATEST_RESPONSE" ]; then
        print_file "$LATEST_RESPONSE" "Mistral Response - Kompletter generierter Text"
        
        RESPONSE_CONTENT=$(cat "$LATEST_RESPONSE")
        RESPONSE_SIZE=$(wc -c < "$LATEST_RESPONSE")
        
        print_box "💬 MISTRAL RESPONSE FILE - VOLLTEXT (${RESPONSE_SIZE} bytes)" "$RESPONSE_CONTENT" "$GREEN"
    else
        print_warning "Response file not found"
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 5: GPT AUTO-TRIGGER DETECTION
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "5️⃣ GPT AUTO-TRIGGER STATUS"
    
    if [ -n "$GPT_SCORES" ] && [ "$GPT_SCORES" != "null" ]; then
        print_success "GPT Auto-Scoring was TRIGGERED!"
        
        print_box "💎 GPT SCORES FROM API RESPONSE - VOLLTEXT" "$(print_json_pretty "$GPT_SCORES")" "$MAGENTA"
    else
        print_error "GPT Auto-Scoring was NOT triggered in API response"
        print_info "Checking file system for drift results..."
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 6: GPT PROMPT RECONSTRUCTION
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "6️⃣ GPT PROMPT - VOLLTEXT (RECONSTRUCTED)"
    
    # Try to extract GPT prompt info from logs
    print_info "Extracting GPT prompt from service logs..."
    
    # Get the entity config to show what GPT received
    ENTITY_FILE="/opt/syntx-config/scoring_entities/gpt4_semantic_entity.json"
    
    if [ -f "$ENTITY_FILE" ]; then
        SYSTEM_PROMPT=$(cat "$ENTITY_FILE" | jq -r '.prompt_templates.system_prompt')
        USER_TEMPLATE=$(cat "$ENTITY_FILE" | jq -r '.prompt_templates.user_prompt_template')
        MODEL=$(cat "$ENTITY_FILE" | jq -r '.llm_configuration.model')
        TEMP=$(cat "$ENTITY_FILE" | jq -r '.llm_configuration.temperature')
        
        # Get format fields
        FORMAT_FILE="/opt/syntx-config/formats/${FORMAT_NAME}.json"
        if [ -f "$FORMAT_FILE" ]; then
            FIELDS=$(cat "$FORMAT_FILE" | jq -r '.fields[].name' | paste -sd ", ")
            
            print_box "📤 GPT REQUEST - SYSTEM PROMPT (VOLLTEXT)" "$SYSTEM_PROMPT" "$BLUE"
            
            echo -e "${CYAN}┌─ GPT User Prompt Template ────────────────────────────────────────────────┐${RESET}"
            echo -e "${CYAN}│${RESET} Fields to score: ${WHITE}$FIELDS${RESET}"
            echo -e "${CYAN}│${RESET} Model: ${WHITE}$MODEL${RESET}"
            echo -e "${CYAN}│${RESET} Temperature: ${WHITE}$TEMP${RESET}"
            echo -e "${CYAN}└────────────────────────────────────────────────────────────────────────────┘${RESET}"
            echo ""
            
            # Build reconstructed user prompt
            RECONSTRUCTED_USER_PROMPT=$(echo "$USER_TEMPLATE" | \
                sed "s/{FORMAT_NAME}/$FORMAT_NAME/g" | \
                sed "s/{FIELD_DEFINITIONS}/Fields: $FIELDS/g" | \
                sed "s/{RESPONSE_TEXT}/$MISTRAL_RESPONSE/g")
            
            print_box "📤 GPT REQUEST - USER PROMPT (VOLLTEXT)" "$RECONSTRUCTED_USER_PROMPT" "$BLUE"
        fi
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 7: GPT DRIFT FILE - VOLLTEXT SCORES
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "7️⃣ GPT DRIFT FILE - VOLLTEXT SCORES"
    
    if [ -n "$LATEST_DRIFT" ] && [ -f "$LATEST_DRIFT" ]; then
        print_success "Drift file found!"
        print_file "$LATEST_DRIFT" "GPT Drift Scores - Komplette semantische Analyse"
        
        DRIFT_CONTENT=$(cat "$LATEST_DRIFT" | jq '.')
        DRIFT_SIZE=$(wc -c < "$LATEST_DRIFT")
        
        print_box "💎 GPT DRIFT SCORES FILE - VOLLTEXT (${DRIFT_SIZE} bytes)" "$DRIFT_CONTENT" "$MAGENTA"
        
        # Extract key metrics
        echo -e "${CYAN}┌─ GPT Analysis Summary ────────────────────────────────────────────────────┐${RESET}"
        
        FIELD_COUNT=$(cat "$LATEST_DRIFT" | jq '.drift_analysis.field_scores | length // 0')
        echo -e "${CYAN}│${RESET} Fields Analyzed: ${WHITE}$FIELD_COUNT${RESET}"
        
        if [ "$FIELD_COUNT" -gt 0 ]; then
            # Show individual field scores
            cat "$LATEST_DRIFT" | jq -r '.drift_analysis.field_scores | to_entries[] | "│ \(.key): \(.value.field_score // .value.score // "N/A")"' | while read line; do
                echo -e "${CYAN}$line${RESET}"
            done
            
            # Show aggregate
            OVERALL=$(cat "$LATEST_DRIFT" | jq -r '.drift_analysis.aggregate.overall // "N/A"')
            echo -e "${CYAN}│${RESET} Overall Score: ${WHITE}$OVERALL${RESET}"
        fi
        
        echo -e "${CYAN}└────────────────────────────────────────────────────────────────────────────┘${RESET}"
        
    else
        print_error "No drift file found"
        print_info "GPT scoring might have failed or been rate-limited"
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 8: SERVICE LOGS - VOLLTEXT
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "8️⃣ SERVICE LOGS - VOLLTEXT"
    
    print_info "Extracting complete GPT Auto-Trigger flow from logs..."
    
    LOGS=$(sudo journalctl -u syntx-injector --since "3 minutes ago" --no-pager 2>/dev/null | \
           grep -E "AUTO-TRIGGER|GPT|Scoring|drift|Field|⚡|🔥|💎|❌|✅" | \
           tail -50)
    
    if [ -n "$LOGS" ]; then
        print_box "📜 SERVICE LOGS - GPT AUTO-TRIGGER FLOW (last 50 lines)" "$LOGS" "$GRAY"
    else
        print_warning "No relevant logs found"
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  STAGE 9: ERROR DETECTION - VOLLTEXT
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_section "9️⃣ ERROR DETECTION - VOLLTEXT"
    
    ERROR_LOGS=$(sudo journalctl -u syntx-injector --since "3 minutes ago" --no-pager 2>/dev/null | \
                 grep -E "Error|Exception|Failed|Traceback|❌" -A 10 | \
                 tail -100)
    
    if [ -n "$ERROR_LOGS" ]; then
        print_error "Errors detected in logs!"
        print_box "🚨 ERROR LOGS - VOLLTEXT (with stack traces)" "$ERROR_LOGS" "$RED"
    else
        print_success "No errors detected!"
    fi
    
    # ═══════════════════════════════════════════════════════════════════════════
    #  FINAL SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    
    print_header "📊 COMPLETE TEST SUMMARY"
    
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}║${RESET} ${WHITE}MISTRAL FLOW${RESET}"
    echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣${RESET}"
    
    [ -n "$LATEST_PROMPT" ] && echo -e "${CYAN}║${RESET} ${GREEN}✅${RESET} Prompt File:   ${WHITE}$(basename $LATEST_PROMPT)${RESET}" || echo -e "${CYAN}║${RESET} ${RED}❌${RESET} Prompt File"
    [ -n "$LATEST_META" ] && echo -e "${CYAN}║${RESET} ${GREEN}✅${RESET} Meta File:     ${WHITE}$(basename $LATEST_META)${RESET}" || echo -e "${CYAN}║${RESET} ${RED}❌${RESET} Meta File"
    [ -n "$LATEST_RESPONSE" ] && echo -e "${CYAN}║${RESET} ${GREEN}✅${RESET} Response File: ${WHITE}$(basename $LATEST_RESPONSE)${RESET}" || echo -e "${CYAN}║${RESET} ${RED}❌${RESET} Response File"
    
    echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣${RESET}"
    echo -e "${CYAN}║${RESET} ${WHITE}GPT AUTO-TRIGGER${RESET}"
    echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣${RESET}"
    
    if [ -n "$LATEST_DRIFT" ] && [ -f "$LATEST_DRIFT" ]; then
        DRIFT_AGE=$(($(date +%s) - $(stat -c %Y "$LATEST_DRIFT")))
        if [ $DRIFT_AGE -lt 180 ]; then
            echo -e "${CYAN}║${RESET} ${GREEN}✅${RESET} Drift File:    ${WHITE}$(basename $LATEST_DRIFT)${RESET}"
            echo -e "${CYAN}║${RESET}    Created: ${WHITE}${DRIFT_AGE}s ago${RESET}"
        else
            echo -e "${CYAN}║${RESET} ${YELLOW}⚠️${RESET}  Drift File:    ${WHITE}$(basename $LATEST_DRIFT)${RESET} (old: ${DRIFT_AGE}s)"
        fi
    else
        echo -e "${CYAN}║${RESET} ${RED}❌${RESET} Drift File:    Not created"
    fi
    
    if [ -n "$GPT_SCORES" ] && [ "$GPT_SCORES" != "null" ]; then
        echo -e "${CYAN}║${RESET} ${GREEN}✅${RESET} API Response:  GPT scores included"
    else
        echo -e "${CYAN}║${RESET} ${RED}❌${RESET} API Response:  No GPT scores"
    fi
    
    echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣${RESET}"
    echo -e "${CYAN}║${RESET} ${WHITE}LOG FILES${RESET}"
    echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣${RESET}"
    echo -e "${CYAN}║${RESET} Complete Log:  ${WHITE}$LOG_FILE${RESET}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝${RESET}"
    
    echo ""
    
    print_header "🔥💎⚡ TEST COMPLETE ⚡💎🔥"
    
    echo -e "${WHITE}Full log saved to: ${CYAN}$LOG_FILE${RESET}"
    echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
#  🔧 HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

check_service_running() {
    if sudo systemctl is-active --quiet syntx-injector; then
        print_success "Service syntx-injector is running"
    else
        print_error "Service syntx-injector is NOT running!"
        exit 1
    fi
}

check_openai_key() {
    KEY_STATUS=$(sudo journalctl -u syntx-injector -n 100 --no-pager 2>/dev/null | grep "OPENAI_API_KEY" | tail -1)
    
    if echo "$KEY_STATUS" | grep -q "konfiguriert"; then
        print_success "OPENAI_API_KEY is configured"
    else
        print_error "OPENAI_API_KEY is NOT set!"
        echo -e "${GRAY}$KEY_STATUS${RESET}"
    fi
}

check_binding_config() {
    BINDING_FILE="/opt/syntx-config/scoring_bindings/${FORMAT_NAME}_binding.json"
    
    if [ -f "$BINDING_FILE" ]; then
        AUTO_TRIGGER=$(cat "$BINDING_FILE" | jq -r '.binding_metadata.auto_trigger_after_mistral')
        
        if [ "$AUTO_TRIGGER" = "true" ]; then
            print_success "Binding '$FORMAT_NAME' has auto_trigger enabled"
        else
            print_warning "Binding '$FORMAT_NAME' has auto_trigger DISABLED"
            print_info "Set 'auto_trigger_after_mistral: true' in: $BINDING_FILE"
        fi
    else
        print_error "Binding file not found: $BINDING_FILE"
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
#  🚀 RUN
# ─────────────────────────────────────────────────────────────────────────────

main "$@"
