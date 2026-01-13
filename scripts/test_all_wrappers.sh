#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# 🔥💎🌊 SYNTX MISTRAL PROMPT BUILDER - ULTIMATE DYNAMIC TEST 💎🔥🌊
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║   🔥💎 SYNTX MISTRAL PROMPT BUILDER - MEGA TEST 💎🔥                     ║"
echo "║                                                                           ║"
echo "║   Dynamically Loading ALL Format-Wrapper Combinations from API           ║"
echo "║   Validating: Prompt Generation + Storage + Metadata                     ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 STATISTICS TRACKING
# ═══════════════════════════════════════════════════════════════════════════════

TOTAL_TESTS=0
SUCCESSFUL_TESTS=0
FAILED_TESTS=0
PROMPTS_SAVED=0
START_TIME=$(date +%s)

# ═══════════════════════════════════════════════════════════════════════════════
# 🌊 LADE ALLE FORMAT-WRAPPER MAPPINGS VOM API
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔥 LADE FORMAT-WRAPPER MAPPINGS VOM API..."
echo ""

mappings=$(curl -s http://localhost:8001/mapping/formats)

if [ $? -ne 0 ]; then
  echo "❌ FEHLER: Konnte Mappings nicht laden!"
  exit 1
fi

total_formats=$(echo "$mappings" | jq -r '.total_formats')
echo "✅ $total_formats Format-Wrapper Kombinationen geladen!"
echo ""

# Extract all format names
format_list=$(echo "$mappings" | jq -r '.mappings | keys[]')

# ═══════════════════════════════════════════════════════════════════════════════
# 🔥 MAIN TEST LOOP - DYNAMISCH!
# ═══════════════════════════════════════════════════════════════════════════════

for format in $format_list; do
  TOTAL_TESTS=$((TOTAL_TESTS + 1))
  
  # Get wrapper and other details from API
  wrapper=$(echo "$mappings" | jq -r ".mappings.\"$format\".mistral_wrapper")
  gpt_wrapper=$(echo "$mappings" | jq -r ".mappings.\"$format\".gpt_wrapper")
  resonanz_score=$(echo "$mappings" | jq -r ".mappings.\"$format\".resonanz_score")
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔥 TEST #${TOTAL_TESTS}: Format=$format"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 Mistral Wrapper:  $wrapper"
  echo "🎯 GPT Wrapper:      $gpt_wrapper"
  echo "💎 Resonanz Score:   $resonanz_score"
  echo "📝 Test Prompt:      Analysiere '$format' Format Test"
  echo ""
  
  # Count prompts before
  prompts_before=$(ls -1 /opt/syntx-config/prompts_generated/*.txt 2>/dev/null | wc -l)
  
  # API Call
  echo "⚡ Sende Request..."
  response=$(curl -s -X POST http://localhost:8001/api/chat \
    -H "Content-Type: application/json" \
    -d "{
      \"prompt\": \"Analysiere das $format Format Test Scenario\",
      \"mode\": \"$wrapper\",
      \"format\": \"$format\",
      \"max_new_tokens\": 1000
    }")
  
  # Check if request succeeded
  if [ $? -eq 0 ]; then
    # Extract metadata
    request_id=$(echo "$response" | jq -r '.metadata.request_id')
    format_fields=$(echo "$response" | jq -r '.metadata.format_fields | length')
    latency=$(echo "$response" | jq -r '.metadata.latency_ms')
    response_preview=$(echo "$response" | jq -r '.response' | head -c 150)
    
    echo "✅ Response erhalten!"
    echo "   ├─ Request ID:     $request_id"
    echo "   ├─ Format Fields:  $format_fields"
    echo "   ├─ Latency:        ${latency}ms"
    echo "   └─ Preview:        ${response_preview}..."
    
    SUCCESSFUL_TESTS=$((SUCCESSFUL_TESTS + 1))
    
    # Count prompts after
    sleep 1
    prompts_after=$(ls -1 /opt/syntx-config/prompts_generated/*.txt 2>/dev/null | wc -l)
    
    if [ $prompts_after -gt $prompts_before ]; then
      echo "💾 Prompt gespeichert! (Files: $prompts_before → $prompts_after)"
      PROMPTS_SAVED=$((PROMPTS_SAVED + 1))
    else
      echo "⚠️  Prompt NICHT gespeichert!"
    fi
  else
    echo "❌ Request fehlgeschlagen!"
    FAILED_TESTS=$((FAILED_TESTS + 1))
  fi
  
  echo ""
  sleep 2
done

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 FINAL STATISTICS & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║   📊 TEST RESULTS - COMPLETE VALIDATION                                  ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 EXECUTION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Total Tests:       $TOTAL_TESTS"
echo "  ✅ Successful:     $SUCCESSFUL_TESTS"
echo "  ❌ Failed:         $FAILED_TESTS"
echo "  💾 Prompts Saved:  $PROMPTS_SAVED"
echo "  ⏱️  Duration:       ${DURATION}s"
echo ""

# Success Rate
success_rate=$(echo "scale=1; $SUCCESSFUL_TESTS * 100 / $TOTAL_TESTS" | bc)
save_rate=$(echo "scale=1; $PROMPTS_SAVED * 100 / $TOTAL_TESTS" | bc)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 PERFORMANCE METRICS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Success Rate:      ${success_rate}%"
echo "  Save Rate:         ${save_rate}%"
echo "  Avg Time/Test:     $((DURATION / TOTAL_TESTS))s"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# 💾 PROMPT STORAGE VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💾 PROMPT STORAGE VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

total_txt=$(ls -1 /opt/syntx-config/prompts_generated/*.txt 2>/dev/null | wc -l)
total_meta=$(ls -1 /opt/syntx-config/prompts_generated/*.meta.json 2>/dev/null | wc -l)

echo "  📄 Prompt Files (.txt):      $total_txt"
echo "  📋 Meta Files (.meta.json):  $total_meta"
echo ""

if [ $total_txt -gt 0 ]; then
  echo "🔥 LATEST GENERATED PROMPTS:"
  echo ""
  ls -lth /opt/syntx-config/prompts_generated/*.txt | head -5 | while read line; do
    echo "  $line"
  done
  echo ""
  
  # Show one example prompt
  latest_prompt=$(ls -t /opt/syntx-config/prompts_generated/*.txt | head -1)
  latest_meta=$(ls -t /opt/syntx-config/prompts_generated/*.meta.json | head -1)
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📄 EXAMPLE PROMPT (Latest)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "File: $(basename $latest_prompt)"
  echo "Size: $(du -h $latest_prompt | cut -f1)"
  echo ""
  echo "--- PROMPT PREVIEW (First 50 lines) ---"
  head -50 "$latest_prompt"
  echo ""
  echo "--- METADATA ---"
  cat "$latest_meta" | jq '.'
  echo ""
fi

# ═══════════════════════════════════════════════════════════════════════════════
# ✅ FINAL VERDICT
# ═══════════════════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ FINAL VERDICT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAILED_TESTS -eq 0 ] && [ $PROMPTS_SAVED -eq $TOTAL_TESTS ]; then
  echo "  🔥💎 PERFEKT! ALLE TESTS ERFOLGREICH! 💎🔥"
  echo ""
  echo "  ✅ Alle $TOTAL_TESTS Format-Wrapper Kombinationen getestet"
  echo "  ✅ Alle $PROMPTS_SAVED Prompts erfolgreich gespeichert"
  echo "  ✅ Komplette Referenz-Kette validiert"
  echo ""
  echo "  🌊 DAS HERZSTÜCK FUNKTIONIERT! 🌊"
elif [ $PROMPTS_SAVED -gt 0 ]; then
  echo "  ⚠️  TEILWEISE ERFOLGREICH"
  echo ""
  echo "  ✅ $SUCCESSFUL_TESTS/$TOTAL_TESTS Tests erfolgreich"
  echo "  💾 $PROMPTS_SAVED/$TOTAL_TESTS Prompts gespeichert"
  echo "  ❌ $FAILED_TESTS Tests fehlgeschlagen"
  echo ""
  echo "  🔧 System funktioniert, aber nicht perfekt"
else
  echo "  ❌ FEHLER - PROMPTS WERDEN NICHT GESPEICHERT!"
  echo ""
  echo "  ✅ Requests funktionieren ($SUCCESSFUL_TESTS/$TOTAL_TESTS)"
  echo "  ❌ Aber Storage schlägt fehl (0 Prompts gespeichert)"
  echo ""
  echo "  🔧 Check Service Logs für Details"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║   🔥💎🌊 SYNTX TEST COMPLETE 🌊💎🔥                                       ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""
