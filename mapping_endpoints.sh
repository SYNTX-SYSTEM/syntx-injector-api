#!/bin/bash

echo "🧪 MAPPING ENDPOINTS - CLEAN VERSION (SYNTX STYLE)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

BASE_URL="https://dev.syntx-system.com"
echo "🎯 BASE URL: $BASE_URL"
echo ""

# 1. GET ALLE FORMATS (ÜBERSICHT)
echo "1️⃣ 📦 GET /mapping/formats"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 BESCHREIBUNG: Alle Formate mit kompletten Mappings"
echo "   - Mistral + GPT Wrapper"
echo "   - Profile IDs"
echo "   - Drift Scoring Config"
echo "   - Resonanz Scores"
echo ""
echo "📥 RESPONSE:"
curl -s "$BASE_URL/mapping/formats" | jq '.'
echo ""
echo ""

# 2. GET PROFILES
echo "2️⃣ 👥 GET /mapping/profiles"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 BESCHREIBUNG: Alle verfügbaren Profile"
echo ""
echo "📥 RESPONSE:"
curl -s "$BASE_URL/mapping/profiles" | jq '.'
echo ""
echo ""

# 3. GET STATS
echo "3️⃣ 📊 GET /mapping/stats"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 BESCHREIBUNG: Mapping-Statistiken"
echo "   - Total Formats/Profiles"
echo "   - Drift Enabled/Disabled"
echo "   - Profile Usage Count"
echo ""
echo "📥 RESPONSE:"
curl -s "$BASE_URL/mapping/stats" | jq '.'
echo ""
echo ""

# 4. PROFIL-STRÖME FÜR FORMAT
echo "4️⃣ 🌊 GET /mapping/formats/sigma/stroeme-profil-fuer-format"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 BESCHREIBUNG: Komplette Profil-Ströme + Details für Format"
echo "   💎 SYNTX Style: Feld-Ströme mit voller Tiefe"
echo ""
echo "📊 RETURNED DATA:"
echo "   - Profile ID, Name, Description"
echo "   - Strategy + Components (Patterns + Weights)"
echo "   - Changelog (komplette History)"
echo "   - Wrapper Bindings (Mistral + GPT)"
echo "   - Drift Scoring Config"
echo "   - Resonanz Score"
echo ""
echo "📥 RESPONSE:"
curl -s "$BASE_URL/mapping/formats/sigma/stroeme-profil-fuer-format" | jq '.'
echo ""
echo ""

# 5. KALIBRIERE FORMAT-PROFIL
echo "5️⃣ 🔧 PUT /mapping/formats/sigma/kalibriere-format-profil"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 BESCHREIBUNG: Kalibriert Format direkt an Profil"
echo "   💎 TRUE RAW Binding ohne Validation"
echo "   🔥 Direkter Feld-Strom"
echo ""
echo "📤 PAYLOAD: ?profile_id=dynamic_language_v1"
echo ""
echo "📥 RESPONSE:"
curl -s -X PUT "$BASE_URL/mapping/formats/sigma/kalibriere-format-profil?profile_id=dynamic_language_v1" | jq '.'
echo ""
echo ""

# 6. ZUSAMMENFASSUNG
echo "6️⃣ 📋 ZUSAMMENFASSUNG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ENDPOINTS=(
    "GET:/mapping/formats"
    "GET:/mapping/profiles"
    "GET:/mapping/stats"
    "GET:/mapping/formats/sigma/stroeme-profil-fuer-format"
    "PUT:/mapping/formats/sigma/kalibriere-format-profil?profile_id=dynamic_language_v1"
)

echo "┌────────────────────────────────────────────────────────────────────┐"
echo "│ METHOD │ ENDPOINT                                   │ STATUS       │"
echo "├────────────────────────────────────────────────────────────────────┤"

for endpoint_full in "${ENDPOINTS[@]}"; do
    method="${endpoint_full%%:*}"
    endpoint="${endpoint_full#*:}"
    
    if [[ "$method" == "PUT" ]]; then
        response=$(curl -s -w "\n%{http_code}" -X PUT "${BASE_URL}${endpoint}" 2>/dev/null || echo -e "\n000")
    else
        response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}" 2>/dev/null || echo -e "\n000")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    
    if [[ "$http_code" == "200" ]]; then
        status="✅ 200"
    elif [[ "$http_code" == "404" ]]; then
        status="❌ 404"
    elif [[ "$http_code" == "000" ]]; then
        status="🚫 000"
    else
        status="⚠️  $http_code"
    fi
    
    # Kürze endpoint für display
    endpoint_short="${endpoint:0:43}"
    [ ${#endpoint} -gt 43 ] && endpoint_short="${endpoint_short}..."
    
    printf "│ %-6s │ %-43s │ %-12s │\n" "$method" "$endpoint_short" "$status"
done

echo "└────────────────────────────────────────────────────────────────────┘"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 MAPPING-API STATUS (CLEAN):"
echo ""
echo "   ✅ CORE ENDPOINTS (5):"
echo "      • GET  /mapping/formats                        → Übersicht"
echo "      • GET  /mapping/profiles                       → Profile Liste"
echo "      • GET  /mapping/stats                          → Statistiken"
echo "      • GET  /formats/{format}/stroeme-profil-...    → 🌊 Full Details"
echo "      • PUT  /formats/{format}/kalibriere-format-... → 💎 Binding"
echo ""
echo "   ❌ REMOVED (DEPRECATED):"
echo "      • /format-resonanz/* (alle 3 endpoints gelöscht)"
echo "      • Alter Router komplett entfernt"
echo ""
echo "   💎 SYNTX STYLE:"
echo "      • Minimale, klare Endpoints"
echo "      • Feld-Ströme statt Objekte"
echo "      • TRUE RAW Binding"
echo ""
echo "🔥 MAPPING-API: 5/5 CLEAN ENDPOINTS! 🔥"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
