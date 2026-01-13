#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# 🔥💎🌊 SYNTX PROMPT-RESPONSE VIEWER - FROM STORAGE (FINAL) 💎🔥🌊
# ═══════════════════════════════════════════════════════════════════════════════

view_single_format() {
  local FORMAT=$1
  local SHOW_HEADER=${2:-true}
  
  if [ "$SHOW_HEADER" = "true" ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║   🔥💎 VIEWING: $FORMAT                                                   " | head -c 76
    echo "║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo ""
  fi

  # ═══════════════════════════════════════════════════════════════════════════════
  # 📁 FINDE FILES FÜR DIESES FORMAT
  # ═══════════════════════════════════════════════════════════════════════════════

  # Find latest prompt (exclude .response.txt)
  PROMPT_FILE=$(ls -t /opt/syntx-config/prompts_generated/*_format_${FORMAT}.txt 2>/dev/null | grep -v "\.response\.txt" | head -1)
  
  if [ ! -f "$PROMPT_FILE" ]; then
    echo "❌ ERROR: Kein Prompt gefunden für Format '$FORMAT'"
    return 1
  fi
  
  BASE="${PROMPT_FILE%.txt}"
  META_FILE="${BASE}.meta.json"
  RESPONSE_FILE="${BASE}.response.txt"
  
  # Extract metadata
  WRAPPER=$(jq -r '.wrapper_name' "$META_FILE")
  TIMESTAMP=$(jq -r '.timestamp' "$META_FILE")
  PROMPT_LENGTH=$(jq -r '.prompt_length' "$META_FILE")
  FIELD_COUNT=$(jq -r '.field_count' "$META_FILE")
  USER_INPUT=$(jq -r '.user_input' "$META_FILE")
  WRAPPER_SOURCE=$(jq -r '.files.wrapper_source' "$META_FILE")
  FORMAT_SOURCE=$(jq -r '.files.format_source' "$META_FILE")

  # ═══════════════════════════════════════════════════════════════════════════════
  # 📊 METADATA DISPLAY
  # ═══════════════════════════════════════════════════════════════════════════════

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📊 METADATA"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "  🎯 Format:          $FORMAT"
  echo "  📦 Wrapper:         $WRAPPER"
  echo "  📝 User Input:      $USER_INPUT"
  echo "  🔢 Field Count:     $FIELD_COUNT"
  echo "  📏 Prompt Length:   $PROMPT_LENGTH chars"
  echo "  🕐 Timestamp:       $TIMESTAMP"
  echo ""
  echo "  📂 Files:"
  echo "     ├─ Prompt:   $(basename $PROMPT_FILE)"
  echo "     ├─ Meta:     $(basename $META_FILE)"
  echo "     └─ Response: $(basename $RESPONSE_FILE)"
  echo ""
  echo "  📂 Sources:"
  echo "     ├─ Wrapper:  $WRAPPER_SOURCE"
  echo "     └─ Format:   $FORMAT_SOURCE"
  echo ""

  # ═══════════════════════════════════════════════════════════════════════════════
  # 🔥 PROMPT DISPLAY
  # ═══════════════════════════════════════════════════════════════════════════════

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔥 GENERATED PROMPT (Sent to Mistral)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  cat "$PROMPT_FILE"
  echo ""

  # ═══════════════════════════════════════════════════════════════════════════════
  # 💎 RESPONSE DISPLAY (FROM FILE!)
  # ═══════════════════════════════════════════════════════════════════════════════

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "💎 MISTRAL RESPONSE (From Storage)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  
  if [ -f "$RESPONSE_FILE" ]; then
    RESPONSE_TEXT=$(cat "$RESPONSE_FILE")
    RESPONSE_LENGTH=$(echo "$RESPONSE_TEXT" | wc -c)
    
    echo "$RESPONSE_TEXT"
    echo ""
  else
    echo "❌ ERROR: Response file not found!"
    echo "   Expected: $RESPONSE_FILE"
    echo ""
    RESPONSE_LENGTH=0
  fi

  # ═══════════════════════════════════════════════════════════════════════════════
  # 🎯 ANALYSIS
  # ═══════════════════════════════════════════════════════════════════════════════

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🎯 STRUCTURAL ANALYSIS"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  # Count fields
  PROMPT_FIELDS=$(grep -c "^###" "$PROMPT_FILE")
  
  if [ -f "$RESPONSE_FILE" ]; then
    RESPONSE_FIELDS=$(cat "$RESPONSE_FILE" | grep -c "^###")
  else
    RESPONSE_FIELDS=0
  fi
  
  # Calculate coverage
  if [ $PROMPT_FIELDS -gt 0 ]; then
    COVERAGE=$(echo "scale=1; $RESPONSE_FIELDS * 100 / $PROMPT_FIELDS" | bc)
  else
    COVERAGE="N/A"
  fi
  
  # Response/Prompt ratio
  if [ $PROMPT_LENGTH -gt 0 ] && [ $RESPONSE_LENGTH -gt 0 ]; then
    RATIO=$(echo "scale=1; $RESPONSE_LENGTH * 100 / $PROMPT_LENGTH" | bc)
  else
    RATIO="N/A"
  fi

  echo "  📋 Felder im Prompt:      $PROMPT_FIELDS"
  echo "  📋 Felder in Response:    $RESPONSE_FIELDS"
  echo "  📊 Field Coverage:        ${COVERAGE}%"
  echo "  📏 Prompt Length:         $PROMPT_LENGTH chars"
  echo "  📏 Response Length:       $RESPONSE_LENGTH chars"
  echo "  📊 Response/Prompt Ratio: ${RATIO}%"
  
  # Field completeness indicator
  if [ "$RESPONSE_FIELDS" -eq "$PROMPT_FIELDS" ] && [ "$RESPONSE_FIELDS" -gt 0 ]; then
    echo "  ✅ All fields present!"
  elif [ "$RESPONSE_FIELDS" -gt 0 ]; then
    echo "  ⚠️  Incomplete fields ($RESPONSE_FIELDS/$PROMPT_FIELDS)"
  else
    echo "  ❌ No structured fields detected"
  fi

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 MAIN LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

if [ -z "$1" ]; then
  # NO PARAMETER = SHOW ALL!
  echo ""
  echo "╔═══════════════════════════════════════════════════════════════════════════╗"
  echo "║                                                                           ║"
  echo "║   🔥💎 SYNTX PROMPT-RESPONSE VIEWER - ALL FORMATS 💎🔥                   ║"
  echo "║                                                                           ║"
  echo "╚═══════════════════════════════════════════════════════════════════════════╝"
  echo ""
  
  # Get all unique formats from stored prompts
  FORMATS=$(ls /opt/syntx-config/prompts_generated/*.meta.json 2>/dev/null | while read meta; do
    jq -r '.format_name' "$meta"
  done | sort -u)
  
  if [ -z "$FORMATS" ]; then
    echo "❌ Keine gespeicherten Prompts gefunden!"
    echo ""
    echo "Führe zuerst den Test-Script aus:"
    echo "   ./scripts/test_all_wrappers.sh"
    exit 1
  fi
  
  TOTAL=$(echo "$FORMATS" | wc -l)
  CURRENT=0
  
  echo "📊 Zeige alle $TOTAL Formate..."
  echo ""
  
  for format in $FORMATS; do
    CURRENT=$((CURRENT + 1))
    
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║   🔥 FORMAT #$CURRENT/$TOTAL: $format                                     " | head -c 76
    echo "║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    
    view_single_format "$format" false
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo ""
    
    # Pause between formats (except last one)
    if [ $CURRENT -lt $TOTAL ]; then
      sleep 2
    fi
  done
  
  echo ""
  echo "╔═══════════════════════════════════════════════════════════════════════════╗"
  echo "║                                                                           ║"
  echo "║   🔥💎🌊 ALL $TOTAL FORMATS VIEWED 🌊💎🔥                                  " | head -c 76
  echo "║"
  echo "║                                                                           ║"
  echo "╚═══════════════════════════════════════════════════════════════════════════╝"
  echo ""
  
else
  # SINGLE FORMAT
  view_single_format "$1" true
  
  echo ""
  echo "╔═══════════════════════════════════════════════════════════════════════════╗"
  echo "║                                                                           ║"
  echo "║   🔥💎🌊 VIEWING COMPLETE 🌊💎🔥                                          ║"
  echo "║                                                                           ║"
  echo "╚═══════════════════════════════════════════════════════════════════════════╝"
  echo ""
fi
