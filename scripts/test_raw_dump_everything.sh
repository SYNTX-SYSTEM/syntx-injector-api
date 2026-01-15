#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
#  🔥💎⚡ SYNTX COMPLETE RAW DUMP - EVERYTHING AS JSON ⚡💎🔥
# ═══════════════════════════════════════════════════════════════════════════════

set -e

TIMESTAMP=$(date +%s)
DUMP_DIR="/tmp/syntx_dump_${TIMESTAMP}"
mkdir -p "$DUMP_DIR"

echo "═══════════════════════════════════════════════════════════════"
echo "🔥 SYNTX RAW DUMP - EVERYTHING AS JSON"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Dump Directory: $DUMP_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
#  1. SERVICE STATUS
# ═══════════════════════════════════════════════════════════════════════════════

echo "1️⃣ SERVICE STATUS"
echo ""

systemctl status syntx-injector --no-pager > "$DUMP_DIR/01_service_status.txt" 2>&1
echo "✅ Saved: $DUMP_DIR/01_service_status.txt"

sudo journalctl -u syntx-injector -n 100 --no-pager > "$DUMP_DIR/02_service_logs.txt" 2>&1
echo "✅ Saved: $DUMP_DIR/02_service_logs.txt"

# ═══════════════════════════════════════════════════════════════════════════════
#  2. CONFIGURATION FILES
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "2️⃣ CONFIGURATION FILES"
echo ""

# .env file (sanitized)
if [ -f .env ]; then
    cat .env | sed 's/\(OPENAI_API_KEY=\).*/\1***REDACTED***/' > "$DUMP_DIR/03_env_file.txt"
    echo "✅ Saved: $DUMP_DIR/03_env_file.txt (API key redacted)"
fi

# Format config
cat /opt/syntx-config/formats/sigma.json > "$DUMP_DIR/04_format_sigma.json" 2>/dev/null
echo "✅ Saved: $DUMP_DIR/04_format_sigma.json"

# Binding config
cat /opt/syntx-config/scoring_bindings/sigma_binding.json > "$DUMP_DIR/05_binding_sigma.json" 2>/dev/null
echo "✅ Saved: $DUMP_DIR/05_binding_sigma.json"

# Entity config
cat /opt/syntx-config/scoring_entities/gpt4_semantic_entity.json > "$DUMP_DIR/06_entity_gpt4.json" 2>/dev/null
echo "✅ Saved: $DUMP_DIR/06_entity_gpt4.json"

# ═══════════════════════════════════════════════════════════════════════════════
#  3. MISTRAL API CALL - RAW REQUEST & RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "3️⃣ MISTRAL API CALL - RAW REQUEST & RESPONSE"
echo ""

REQUEST_PAYLOAD='{
  "prompt": "Analysiere die semantische Drift in einem neuronalen Netzwerk. Beschreibe den Mechanismus, die Frequenz und die Dichte der Verschiebung detailliert.",
  "mode": "syntex_wrapper_sigma",
  "format": "sigma",
  "max_new_tokens": 500
}'

# Save request
echo "$REQUEST_PAYLOAD" | jq '.' > "$DUMP_DIR/07_mistral_request.json"
echo "✅ Saved: $DUMP_DIR/07_mistral_request.json"

echo ""
echo "REQUEST:"
cat "$DUMP_DIR/07_mistral_request.json"

echo ""
echo "Calling API..."
START_TIME=$(date +%s%3N)

HTTP_RESPONSE=$(curl -s -w "\n---HTTP_CODE:%{http_code}---" \
  -X POST "http://localhost:8001/resonanz/chat" \
  -H "Content-Type: application/json" \
  -d "$REQUEST_PAYLOAD")

END_TIME=$(date +%s%3N)
LATENCY=$((END_TIME - START_TIME))

# Extract HTTP code
HTTP_CODE=$(echo "$HTTP_RESPONSE" | grep "^---HTTP_CODE:" | cut -d: -f2 | tr -d '-')
RESPONSE_BODY=$(echo "$HTTP_RESPONSE" | sed '/^---HTTP_CODE:/d')

# Save response
echo "$RESPONSE_BODY" > "$DUMP_DIR/08_mistral_response_raw.json"
echo "✅ Saved: $DUMP_DIR/08_mistral_response_raw.json"

# Pretty print
echo "$RESPONSE_BODY" | jq '.' > "$DUMP_DIR/09_mistral_response_pretty.json" 2>/dev/null
echo "✅ Saved: $DUMP_DIR/09_mistral_response_pretty.json"

echo ""
echo "HTTP CODE: $HTTP_CODE"
echo "LATENCY: ${LATENCY}ms"
echo ""
echo "RESPONSE:"
cat "$DUMP_DIR/09_mistral_response_pretty.json"

# Extract components
echo ""
echo "Extracting response components..."

echo "$RESPONSE_BODY" | jq -r '.response' > "$DUMP_DIR/10_mistral_response_text.txt" 2>/dev/null
echo "✅ Saved: $DUMP_DIR/10_mistral_response_text.txt"

echo "$RESPONSE_BODY" | jq '.metadata' > "$DUMP_DIR/11_mistral_metadata.json" 2>/dev/null
echo "✅ Saved: $DUMP_DIR/11_mistral_metadata.json"

# ═══════════════════════════════════════════════════════════════════════════════
#  4. GENERATED FILES
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "4️⃣ GENERATED FILES (last 2 minutes)"
echo ""

# Find most recent files
PROMPTS_DIR="/opt/syntx-config/prompts_generated"
DRIFT_DIR="/opt/syntx-config/drift_results"

LATEST_PROMPT=$(find "$PROMPTS_DIR" -name "*.txt" -type f -not -name "*.response.txt" -newermt "2 minutes ago" 2>/dev/null | head -1)
LATEST_META=$(find "$PROMPTS_DIR" -name "*.meta.json" -type f -newermt "2 minutes ago" 2>/dev/null | head -1)
LATEST_RESPONSE=$(find "$PROMPTS_DIR" -name "*.response.txt" -type f -newermt "2 minutes ago" 2>/dev/null | head -1)
LATEST_DRIFT=$(find "$DRIFT_DIR" -name "*_drift_*.json" -type f -newermt "2 minutes ago" 2>/dev/null | head -1)

# Copy prompt
if [ -n "$LATEST_PROMPT" ] && [ -f "$LATEST_PROMPT" ]; then
    cp "$LATEST_PROMPT" "$DUMP_DIR/12_prompt_file.txt"
    echo "✅ Saved: $DUMP_DIR/12_prompt_file.txt"
    echo "   Source: $LATEST_PROMPT"
fi

# Copy meta
if [ -n "$LATEST_META" ] && [ -f "$LATEST_META" ]; then
    cp "$LATEST_META" "$DUMP_DIR/13_meta_file.json"
    echo "✅ Saved: $DUMP_DIR/13_meta_file.json"
    echo "   Source: $LATEST_META"
fi

# Copy response
if [ -n "$LATEST_RESPONSE" ] && [ -f "$LATEST_RESPONSE" ]; then
    cp "$LATEST_RESPONSE" "$DUMP_DIR/14_response_file.txt"
    echo "✅ Saved: $DUMP_DIR/14_response_file.txt"
    echo "   Source: $LATEST_RESPONSE"
fi

# Copy drift
if [ -n "$LATEST_DRIFT" ] && [ -f "$LATEST_DRIFT" ]; then
    cp "$LATEST_DRIFT" "$DUMP_DIR/15_drift_file.json"
    echo "✅ Saved: $DUMP_DIR/15_drift_file.json"
    echo "   Source: $LATEST_DRIFT"
fi

# ═══════════════════════════════════════════════════════════════════════════════
#  5. GPT AUTO-TRIGGER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "5️⃣ GPT AUTO-TRIGGER ANALYSIS"
echo ""

# Check if GPT was triggered in API response
GPT_TRIGGERED=$(echo "$RESPONSE_BODY" | jq '.metadata.gpt_auto_scoring // null')

if [ "$GPT_TRIGGERED" != "null" ]; then
    echo "✅ GPT Auto-Trigger was TRIGGERED in API response"
    echo "$GPT_TRIGGERED" | jq '.' > "$DUMP_DIR/16_gpt_scores_from_api.json"
    echo "✅ Saved: $DUMP_DIR/16_gpt_scores_from_api.json"
else
    echo "❌ GPT Auto-Trigger was NOT in API response"
fi

# Check service logs for GPT activity
echo ""
echo "Extracting GPT logs..."
sudo journalctl -u syntx-injector --since "2 minutes ago" --no-pager 2>/dev/null | \
  grep -E "AUTO-TRIGGER|GPT|Scoring|drift|Field|⚡|🔥|💎" > "$DUMP_DIR/17_gpt_logs.txt" 2>&1

if [ -s "$DUMP_DIR/17_gpt_logs.txt" ]; then
    echo "✅ Saved: $DUMP_DIR/17_gpt_logs.txt"
else
    echo "⚠️  No GPT logs found"
fi

# Check for errors
sudo journalctl -u syntx-injector --since "2 minutes ago" --no-pager 2>/dev/null | \
  grep -iE "error|exception|traceback|failed" > "$DUMP_DIR/18_error_logs.txt" 2>&1

if [ -s "$DUMP_DIR/18_error_logs.txt" ]; then
    echo "✅ Saved: $DUMP_DIR/18_error_logs.txt"
else
    echo "✅ No errors found"
fi

# ═══════════════════════════════════════════════════════════════════════════════
#  6. GPT REQUEST RECONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "6️⃣ GPT REQUEST RECONSTRUCTION"
echo ""

if [ -f "$DUMP_DIR/14_response_file.txt" ] && [ -f /opt/syntx-config/scoring_entities/gpt4_semantic_entity.json ]; then
    
    SYSTEM_PROMPT=$(cat /opt/syntx-config/scoring_entities/gpt4_semantic_entity.json | jq -r '.prompt_templates.system_prompt')
    USER_TEMPLATE=$(cat /opt/syntx-config/scoring_entities/gpt4_semantic_entity.json | jq -r '.prompt_templates.user_prompt_template')
    
    # Build GPT request payload
    cat > "$DUMP_DIR/19_gpt_request_reconstructed.json" << EOFREQ
{
  "model": "gpt-4",
  "temperature": 0.1,
  "max_tokens": 2000,
  "messages": [
    {
      "role": "system",
      "content": $(echo "$SYSTEM_PROMPT" | jq -Rs '.')
    },
    {
      "role": "user",
      "content": "Format: sigma\nFields: sigma_drift, sigma_mechanismus, sigma_frequenz, sigma_dichte, sigma_strome, sigma_extrakt\n\nResponse to analyze:\n$(cat "$DUMP_DIR/14_response_file.txt" | head -c 500)"
    }
  ]
}
EOFREQ
    
    echo "✅ Saved: $DUMP_DIR/19_gpt_request_reconstructed.json"
fi

# ═══════════════════════════════════════════════════════════════════════════════
#  7. SUMMARY JSON
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "7️⃣ CREATING SUMMARY JSON"
echo ""

cat > "$DUMP_DIR/00_SUMMARY.json" << EOFSUMMARY
{
  "timestamp": "$(date -Iseconds)",
  "dump_directory": "$DUMP_DIR",
  "test_details": {
    "api_endpoint": "http://localhost:8001/resonanz/chat",
    "wrapper": "syntex_wrapper_sigma",
    "format": "sigma",
    "http_code": $HTTP_CODE,
    "latency_ms": $LATENCY
  },
  "files_generated": {
    "service_status": "01_service_status.txt",
    "service_logs": "02_service_logs.txt",
    "env_file": "03_env_file.txt",
    "format_config": "04_format_sigma.json",
    "binding_config": "05_binding_sigma.json",
    "entity_config": "06_entity_gpt4.json",
    "mistral_request": "07_mistral_request.json",
    "mistral_response_raw": "08_mistral_response_raw.json",
    "mistral_response_pretty": "09_mistral_response_pretty.json",
    "mistral_response_text": "10_mistral_response_text.txt",
    "mistral_metadata": "11_mistral_metadata.json",
    "prompt_file": "12_prompt_file.txt",
    "meta_file": "13_meta_file.json",
    "response_file": "14_response_file.txt",
    "drift_file": "15_drift_file.json",
    "gpt_scores": "16_gpt_scores_from_api.json",
    "gpt_logs": "17_gpt_logs.txt",
    "error_logs": "18_error_logs.txt",
    "gpt_request_reconstructed": "19_gpt_request_reconstructed.json"
  },
  "source_files": {
    "prompt": "$LATEST_PROMPT",
    "meta": "$LATEST_META",
    "response": "$LATEST_RESPONSE",
    "drift": "$LATEST_DRIFT"
  },
  "status": {
    "gpt_triggered_in_api": $([ "$GPT_TRIGGERED" != "null" ] && echo "true" || echo "false"),
    "drift_file_exists": $([ -n "$LATEST_DRIFT" ] && echo "true" || echo "false"),
    "errors_detected": $([ -s "$DUMP_DIR/18_error_logs.txt" ] && echo "true" || echo "false")
  }
}
EOFSUMMARY

echo "✅ Saved: $DUMP_DIR/00_SUMMARY.json"

# ═══════════════════════════════════════════════════════════════════════════════
#  8. FINAL OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ COMPLETE DUMP FINISHED"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Dump Directory: $DUMP_DIR"
echo ""
echo "Files:"
ls -lh "$DUMP_DIR" | tail -n +2

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
cat "$DUMP_DIR/00_SUMMARY.json" | jq '.'

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "View all files with:"
echo "  ls -la $DUMP_DIR"
echo ""
echo "View summary:"
echo "  cat $DUMP_DIR/00_SUMMARY.json | jq '.'"
echo ""
echo "View Mistral response:"
echo "  cat $DUMP_DIR/10_mistral_response_text.txt"
echo ""
echo "View GPT logs:"
echo "  cat $DUMP_DIR/17_gpt_logs.txt"
echo ""
echo "═══════════════════════════════════════════════════════════════"
