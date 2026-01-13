#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# 🔥💎🌊 SYNTX COMPLETE PROMPT ANALYZER - READ ALL STORAGE 💎🔥🌊
# ═══════════════════════════════════════════════════════════════════════════════

PROMPTS_DIR="/opt/syntx-config/prompts_generated"

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║   🔥💎 SYNTX COMPLETE STORAGE ANALYZER 💎🔥                              ║"
echo "║                                                                           ║"
echo "║   Reading ALL prompts, metas, and responses from storage                 ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 GLOBAL STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

TOTAL_PROMPTS=$(ls -1 "$PROMPTS_DIR"/*.txt 2>/dev/null | grep -v "\.response\.txt" | wc -l)
TOTAL_METAS=$(ls -1 "$PROMPTS_DIR"/*.meta.json 2>/dev/null | wc -l)
TOTAL_RESPONSES=$(ls -1 "$PROMPTS_DIR"/*.response.txt 2>/dev/null | wc -l)
TOTAL_FILES=$(($TOTAL_PROMPTS + $TOTAL_METAS + $TOTAL_RESPONSES))

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 GLOBAL STORAGE STATISTICS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📄 Total Prompts:   $TOTAL_PROMPTS"
echo "  📋 Total Metas:     $TOTAL_METAS"
echo "  💎 Total Responses: $TOTAL_RESPONSES"
echo "  📦 Total Files:     $TOTAL_FILES"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 ANALYZE EACH TRIPLET
# ═══════════════════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 ANALYZING ALL TRIPLETS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TOTAL_PROMPT_CHARS=0
TOTAL_RESPONSE_CHARS=0
TOTAL_FIELDS_REQUESTED=0
TOTAL_FIELDS_FILLED=0

# Get all unique formats
FORMATS=$(ls "$PROMPTS_DIR"/*.meta.json 2>/dev/null | while read meta; do
  jq -r '.format_name' "$meta"
done | sort -u)

for format in $FORMATS; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔥 FORMAT: $format"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # Find files for this format
  PROMPT_FILE=$(ls -t "$PROMPTS_DIR"/*_format_${format}.txt 2>/dev/null | grep -v "\.response\.txt" | head -1)
  
  if [ ! -f "$PROMPT_FILE" ]; then
    echo "⚠️  No files found for format: $format"
    echo ""
    continue
  fi
  
  BASE="${PROMPT_FILE%.txt}"
  META_FILE="${BASE}.meta.json"
  RESPONSE_FILE="${BASE}.response.txt"
  
  # Extract metadata
  WRAPPER=$(jq -r '.wrapper_name' "$META_FILE")
  TIMESTAMP=$(jq -r '.timestamp' "$META_FILE")
  USER_INPUT=$(jq -r '.user_input' "$META_FILE")
  WRAPPER_SOURCE=$(jq -r '.files.wrapper_source' "$META_FILE")
  FORMAT_SOURCE=$(jq -r '.files.format_source' "$META_FILE")
  
  # File sizes
  PROMPT_SIZE=$(wc -c < "$PROMPT_FILE")
  RESPONSE_SIZE=0
  if [ -f "$RESPONSE_FILE" ]; then
    RESPONSE_SIZE=$(wc -c < "$RESPONSE_FILE")
  fi
  
  # Count fields
  PROMPT_FIELDS=$(grep -c "^###" "$PROMPT_FILE")
  RESPONSE_FIELDS=0
  if [ -f "$RESPONSE_FILE" ]; then
    RESPONSE_FIELDS=$(cat "$RESPONSE_FILE" | grep -c "^###")
  fi
  
  # Calculate coverage
  COVERAGE=0
  if [ $PROMPT_FIELDS -gt 0 ]; then
    COVERAGE=$(echo "scale=1; $RESPONSE_FIELDS * 100 / $PROMPT_FIELDS" | bc)
  fi
  
  # Accumulate totals
  TOTAL_PROMPT_CHARS=$((TOTAL_PROMPT_CHARS + PROMPT_SIZE))
  TOTAL_RESPONSE_CHARS=$((TOTAL_RESPONSE_CHARS + RESPONSE_SIZE))
  TOTAL_FIELDS_REQUESTED=$((TOTAL_FIELDS_REQUESTED + PROMPT_FIELDS))
  TOTAL_FIELDS_FILLED=$((TOTAL_FIELDS_FILLED + RESPONSE_FIELDS))
  
  echo ""
  echo "  📦 Wrapper:         $WRAPPER"
  echo "  📝 User Input:      $USER_INPUT"
  echo "  🕐 Timestamp:       $TIMESTAMP"
  echo ""
  echo "  📂 Files:"
  echo "     ├─ Prompt:   $(basename $PROMPT_FILE) (${PROMPT_SIZE} bytes)"
  if [ -f "$RESPONSE_FILE" ]; then
    echo "     ├─ Response: $(basename $RESPONSE_FILE) (${RESPONSE_SIZE} bytes)"
  else
    echo "     ├─ Response: ❌ MISSING"
  fi
  echo "     └─ Meta:     $(basename $META_FILE)"
  echo ""
  echo "  📊 Field Analysis:"
  echo "     ├─ Fields Requested:  $PROMPT_FIELDS"
  echo "     ├─ Fields Filled:     $RESPONSE_FIELDS"
  echo "     └─ Coverage:          ${COVERAGE}%"
  echo ""
  echo "  📂 Source References:"
  echo "     ├─ Wrapper:  $WRAPPER_SOURCE"
  echo "     └─ Format:   $FORMAT_SOURCE"
  echo ""
  
  # Show prompt snippet
  echo "  🔥 PROMPT SNIPPET (First 200 chars):"
  echo "  ┌─────────────────────────────────────────────────────────────────────┐"
  head -c 200 "$PROMPT_FILE" | sed 's/^/  │ /'
  echo "..."
  echo "  └─────────────────────────────────────────────────────────────────────┘"
  echo ""
  
  # Show response snippet
  if [ -f "$RESPONSE_FILE" ]; then
    echo "  💎 RESPONSE SNIPPET (First 200 chars):"
    echo "  ┌─────────────────────────────────────────────────────────────────────┐"
    head -c 200 "$RESPONSE_FILE" | sed 's/^/  │ /'
    echo "..."
    echo "  └─────────────────────────────────────────────────────────────────────┘"
  else
    echo "  💎 RESPONSE: ❌ NOT FOUND"
  fi
  echo ""
  
done

# ═══════════════════════════════════════════════════════════════════════════════
# 📈 AGGREGATE STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║   📈 AGGREGATE STATISTICS                                                ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SIZE STATISTICS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Total Prompt Size:   $TOTAL_PROMPT_CHARS bytes"
echo "  Total Response Size: $TOTAL_RESPONSE_CHARS bytes"
if [ $TOTAL_PROMPTS -gt 0 ]; then
  AVG_PROMPT=$((TOTAL_PROMPT_CHARS / TOTAL_PROMPTS))
  echo "  Avg Prompt Size:     $AVG_PROMPT bytes"
fi
if [ $TOTAL_RESPONSES -gt 0 ]; then
  AVG_RESPONSE=$((TOTAL_RESPONSE_CHARS / TOTAL_RESPONSES))
  echo "  Avg Response Size:   $AVG_RESPONSE bytes"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 FIELD STATISTICS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Total Fields Requested: $TOTAL_FIELDS_REQUESTED"
echo "  Total Fields Filled:    $TOTAL_FIELDS_FILLED"
if [ $TOTAL_FIELDS_REQUESTED -gt 0 ]; then
  OVERALL_COVERAGE=$(echo "scale=1; $TOTAL_FIELDS_FILLED * 100 / $TOTAL_FIELDS_REQUESTED" | bc)
  echo "  Overall Coverage:       ${OVERALL_COVERAGE}%"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 FORMAT BREAKDOWN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
for format in $FORMATS; do
  PROMPT_FILE=$(ls -t "$PROMPTS_DIR"/*_format_${format}.txt 2>/dev/null | grep -v "\.response\.txt" | head -1)
  if [ -f "$PROMPT_FILE" ]; then
    WRAPPER=$(jq -r '.wrapper_name' "${PROMPT_FILE%.txt}.meta.json")
    echo "  • $format → $WRAPPER"
  fi
done
echo ""

echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║   🔥💎🌊 ANALYSIS COMPLETE 🌊💎🔥                                         ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""
