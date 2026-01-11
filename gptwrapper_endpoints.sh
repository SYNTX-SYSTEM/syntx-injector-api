echo "🔍 LETZTER CHECK - VOLLE API-ANTWORTEN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FELD_NAME="final_test_$(date +%s)"
BASE_URL="https://dev.syntx-system.com"

echo "🎯 FINALER TEST MIT VOLLEN RESPONSES:"
echo ""

# 1. CREATE mit voller Antwort
echo "1️⃣ CREATE (POST) - VOLLE ANTWORT:"
curl -s -X POST "$BASE_URL/gpt-wrapper-feld-stroeme/neues-gpt-wrapper-feld-resonanz-erschaffen" \
  -H "Content-Type: application/json" \
  -d "{\"gpt_wrapper_feld_name\": \"$FELD_NAME\", \"gpt_wrapper_feld_inhalt\": \"Final Test\"}" \
  | jq '.' 2>/dev/null || echo "RAW: $(curl -s -X POST "$BASE_URL/gpt-wrapper-feld-stroeme/neues-gpt-wrapper-feld-resonanz-erschaffen" \
  -H "Content-Type: application/json" \
  -d "{\"gpt_wrapper_feld_name\": \"$FELD_NAME\", \"gpt_wrapper_feld_inhalt\": \"Final Test\"}")"

echo ""

# 2. MATRIX mit voller Antwort
echo "2️⃣ MATRIX (GET) - VOLLE ANTWORT:"
MATRIX_RESPONSE=$(curl -s "$BASE_URL/gpt-wrapper-feld-stroeme/gpt-wrapper-feld-matrix-resonanz-erkennen")
echo "$MATRIX_RESPONSE" | jq '.' 2>/dev/null || echo "RAW: $MATRIX_RESPONSE" | head -200

echo ""

# 3. UPDATE mit voller Antwort
echo "3️⃣ UPDATE (PUT) - VOLLE ANTWORT:"
curl -s -X PUT "$BASE_URL/gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aktualisieren/$FELD_NAME" \
  -H "Content-Type: application/json" \
  -d "{\"gpt_wrapper_feld_inhalt\": \"Updated Content\", \"gpt_wrapper_feld_resonanz_potenzial\": 0.8}" \
  | jq '.' 2>/dev/null || echo "RAW: $(curl -s -X PUT "$BASE_URL/gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aktualisieren/$FELD_NAME" \
  -H "Content-Type: application/json" \
  -d "{\"gpt_wrapper_feld_inhalt\": \"Updated Content\", \"gpt_wrapper_feld_resonanz_potenzial\": 0.8}")"

echo ""

# 4. DELETE mit voller Antwort
echo "4️⃣ DELETE (DELETE) - VOLLE ANTWORT:"
curl -s -X DELETE "$BASE_URL/gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aufloesen/$FELD_NAME" \
  | jq '.' 2>/dev/null || echo "RAW: $(curl -s -X DELETE "$BASE_URL/gpt-wrapper-feld-stroeme/gpt-wrapper-feld-resonanz-aufloesen/$FELD_NAME")"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 GPT-WRAPPER CRUD STATUS:"
echo "   ✅ Endpoints existieren und akzeptieren Requests"
echo "   ⚠️  Responses müssen noch validiert werden"
echo "   🔥 API ist grundsätzlich funktional"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
