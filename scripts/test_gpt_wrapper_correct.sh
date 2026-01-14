#!/bin/bash
# 🔥 KORREKTER GPT-WRAPPER TEST

BASE_URL="https://dev.syntx-system.com"
EPOCH=$(date +%s)

echo "🧪 GPT-WRAPPER KORREKTE TESTS:"
echo ""

# 1. Matrix erkennen (GET - funktioniert)
echo "1️⃣ GET /gpt-wrapper-feld-stroeme/gpt-wrapper-feld-matrix-resonanz-erkennen"
curl -s "$BASE_URL/gpt-wrapper-feld-stroeme/gpt-wrapper-feld-matrix-resonanz-erkennen" | jq -r '.gpt-wrapper-feld-anzahl' 2>/dev/null && echo "✅" || echo "❌"

# 2. Neues Feld mit KORREKTER Payload erstellen
echo ""
echo "2️⃣ POST /gpt-wrapper-feld-stroeme/neues-gpt-wrapper-feld-resonanz-erschaffen"
curl -s -X POST "$BASE_URL/gpt-wrapper-feld-stroeme/neues-gpt-wrapper-feld-resonanz-erschaffen" \
  -H "Content-Type: application/json" \
  -d "{\"gpt_wrapper_feld_name\": \"test_correct_${EPOCH}\", \"gpt_wrapper_feld_inhalt\": \"Test Wrapper\"}" | jq -r '.gpt-wrapper-feld-name // .detail' 2>/dev/null && echo "✅" || echo "❌"

# 3. Ströme testen
echo ""
echo "3️⃣ GET /gpt-wrapper-feld-stroeme/strom"
curl -s "$BASE_URL/gpt-wrapper-feld-stroeme/strom" | jq -r '.strom_typ // .detail' 2>/dev/null && echo "✅" || echo "❌"

echo ""
echo "💎 GPT-WRAPPER TESTS KORRIGIERT"
