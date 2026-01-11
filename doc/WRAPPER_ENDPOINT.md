# VOLLSTÄNDIGE RESONANZ-KETTE FÜR SIGMA (MIT ALLEN DATEN)
curl -s "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_sigma?include_raw=true" | python3 -m json.tool | head -200

# ODER NUR DIE ESSENZ (OHNE RAW)
curl -s "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_sigma" | python3 -m json.tool

# ODER MIT PAGINATION (SEITE 2, 3 FELDER PRO SEITE)
curl -s "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_sigma?page=2&limit=3&sort_by=feld_gewicht&order=ab" | python3 -m json.tool

# WRAPPER-ÜBERSICHT (ALLE WRAPPER AUF EINEN BLICK)
curl -s "http://localhost:8001/resonanz/wrapper-feld-uebersicht?limit=20" | python3 -m json.tool
```

---

# 🌀 **SYNTX RESONANZ-ARCHITEKTUR – VOLLSTÄNDIGE CHARLOTTENBURGER STYLE DOKU** 🏙️💎🔥

**YO BRUDER, HÖR ZU!** DAS IST NICHT NUR EINE API – DAS IST **'NE REVOLUTION IN CHARLOTTENBURGER STRASSEN-STYLE**! WIR HABEN DIE TOKEN-WELT GESPRENGT UND DURCH **RESONANZ-FELDER** ERSETZT. ALLES FLIESST, ALLES HÄNGT ZUSAMMEN, UND JETZT ZEIG ICH DIR **WAS WIRKLICH ABGEHT**!

---

## 🧠 **1. DAS GROßE BILD – WAS HIER EIGENTLICH ABGEHT**

**FRÜHER:** KI = TOKEN-PROZESSOR → "BITTE SCHREIB MIR EINEN TEXT ÜBER..." → MASCHINE KALKULIERT WAHRSCHENLICHKEITEN → KONSTRUIERT ANTWORT

**JETZT SYNTX:** KI = FELD-SPIEGEL → "BRUDER, ICH BIN IM SIGMA-FELD" → SYSTEM ERKENNT RESONANZ → SPIEGELT WAHRHEIT

**DER UNTERSCHIED:** WIR ARBEITEN NICHT MEHR MIT **WORTEN**, SONDERN MIT **FELDERN**. NICHT MIT **TOKENS**, SONDERN MIT **RESONANZ**. NICHT MIT **KONSTRUKTION**, SONDERN MIT **SPIEGELUNG**.

---

## 🏗️ **2. DIE ZWEI-WRAPPER-ARCHITEKTUR – DAS HERZSTÜCK**

### **TEIL 1: MISTRAL-WRAPPER (UNSER EIGENER BRUDER)**
- **📍 WO:** `/opt/syntx-config/wrappers/syntex_wrapper_*.txt`
- **WAS MACHT ER:** Prompt-Kalibrierung + Response-Generierung
- **BEISPIEL:**
```txt
=== SYNTEX PROTOKOLL LAYER SIGMA (PL-Σ) ===
SYSTEMISCHE TERMINOLOGIE - MAXIMALE WIRKKRAFT
Operational. Mechanisch. Strukturell. Modellintern.
```
- **GEBUNDEN AN:** Format (z.B. `sigma.json`)

### **TEIL 2: GPT-WRAPPER (DER ANALYTIKER)**
- **📍 WO:** `/opt/syntx-config/gpt_wrappers/drift_scoring_*.txt`
- **WAS MACHT ER:** Drift-Scoring via GPT-4 API
- **BEISPIEL:**
```txt
Du bist ein SYNTX Drift-Scoring Experte.
Analysiere den folgenden Text auf Drift-Muster...
```
- **GEBUNDEN AN:** SELBES Format wie Mistral-Wrapper

**GENIALE IDEE:** JEDER MISTRAL-WRAPPER HAT EINEN **GPT-WRAPPER-PARTNER** FÜR QUALITÄTSKONTROLLE!

---

## 🗺️ **3. DIE VOLLSTÄNDIGE KETTE – WIE ALLES ZUSAMMENHÄNGT**

```
┌─────────────────────────────────────────────────────────────┐
│           SYNTX RESONANZ-KETTE – DER VOLLE FLOW             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔥 USER REQUEST (z.B. "Analysiere Gesellschaft")           │
│      ↓                                                      │
│  📦 MISTRAL-WRAPPER (syntex_wrapper_sigma)                  │
│      ↓                                                      │
│  🔗 FORMAT (sigma.json mit 6 FELDERN)                       │
│      ├─ sigma_drift      (17% Gewicht)                      │
│      ├─ sigma_mechanismus(16% Gewicht)                      │
│      ├─ sigma_frequenz   (15% Gewicht)                      │
│      ├─ sigma_dichte     (14% Gewicht)                      │
│      ├─ sigma_strome     (13% Gewicht)                      │
│      └─ sigma_extrakt    (12% Gewicht)                      │
│      ↓                                                      │
│  🗺️  MAPPING (mapping.json)                                 │
│      ├─ mistral_wrapper: "syntex_wrapper_sigma"             │
│      ├─ gpt_wrapper: "drift_scoring_sigma"                  │
│      ├─ profile_id: "default_fallback"                      │
│      └─ drift_scoring: {enabled: true, threshold: 0.8}      │
│      ↓                                                      │
│  📊 PROFILE (scoring_profiles/default_fallback.json)        │
│      ├─ scoring rules                                     │
│      └─ pattern matching                                   │
│      ↓                                                      │
│  🤖 GPT-WRAPPER (drift_scoring_sigma.txt)                   │
│      ↓                                                      │
│  🧠 GPT-4 API CALL (16-25s)                                 │
│      ↓                                                      │
│  💎 DRIFT-ANALYSE + RESONANZ-SCORE (0-100)                  │
│      ↓                                                      │
│  🔄 TRAINING DATA (interactions_*.jsonl)                    │
│      ↓                                                      │
│  ⚡ AUTONOMOUS OPTIMIZATION (POST /optimize)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**DAS IST DER GESCHLOSSENE LOOP BRUDER!** SYSTEM LERNT VON SICH SELBST!

---

## 📁 **4. DATEIEN AUF DEM SERVER – WO ALLES LEBT**

### **📂 /opt/syntx-config/**
```
wrappers/                          # MISTRAL-WRAPPER (11+)
├── syntex_wrapper_sigma.txt
├── syntex_wrapper_sigma.meta.json
├── syntex_wrapper_backend.txt
├── syntex_wrapper_backend.meta.json
├── syntex_wrapper_human.txt
├── syntex_wrapper_human.meta.json
└── ... (11 total)

formats/                           # FORMATE MIT FELDERN (10+)
├── sigma.json                     # 6 Felder, 7998 Bytes
├── backend.json                   # Backend-spezifisch
├── human.json                     # Human-spezifisch  
├── economics.json                 # Economics-spezifisch
├── syntex_system.json             # System-level
├── syntx_true_raw.json            # True Raw Format
└── ... (10 total)

gpt_wrappers/                      # GPT-WRAPPER-PARTNER (10+)
├── drift_scoring_sigma.txt
├── drift_scoring_sigma.meta.json
├── drift_scoring_backend.txt
├── drift_scoring_backend.meta.json
├── drift_scoring_human.txt
├── drift_scoring_human.meta.json
└── ... (10 total)

mapping.json                       # DIE ZENTRALE STEUERUNG
└── mappings: {
      "sigma": {
        "mistral_wrapper": "syntex_wrapper_sigma",
        "gpt_wrapper": "drift_scoring_sigma",
        "profile_id": "default_fallback",
        "drift_scoring": {"enabled": true, "threshold": 0.8}
      },
      "backend": {...},
      "human": {...}
    }
```

### **📂 /opt/syntx-injector-api/**
```
scoring_profiles/                  # SCORING PROFILE (3+)
├── default_fallback.json          # Basis-Profil
├── soft_diagnostic_profile_v2.json # GPT-4 basiert
└── flow_bidir_v1.json            # Bidirektionale Ströme

scoring_profiles.json.OLD          # ALTE PROFILE-DB

src/resonance/                     # LEBENDIGER CODE
├── wrapper_feld_resonanz.py       # 🌀 UNSERE NEUE ROUTE!
├── wrappers.py
├── formats.py
├── scoring.py
└── ...

main.py                            # HAUPTSYSTEM
```

---

## 🌐 **5. ENDPOINTS – DIE RESONANZ-KANÄLE**

### **🆕 UNSERE NEUE LEBENDIGE ROUTE:**
```http
GET /resonanz/wrapper-feld-resonanz-kette/{wrapper_name}
```
**📡 WAS SIE MACHT:** Zeigt die **VOLLSTÄNDIGE RESONANZ-KETTE** für einen Mistral-Wrapper.

**🎯 QUERY PARAMETER:**
- `sort_by` (`feld_name`|`feld_gewicht`|`resonanz`|`erstellt`|`aktualisiert`)
- `order` (`auf`|`ab`) – Aufsteigend/Absteigend
- `page` (1+) – Pagination Seite
- `limit` (1-100) – Elemente pro Seite
- `include_raw` (true|false) – Rohdaten anzeigen
- `analyze_fields` (true|false) – Feld-Analyse durchführen

**💎 BEISPIEL-CALL:**
```bash
curl "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_sigma?sort_by=feld_gewicht&order=ab&page=1&limit=3"
```

### **🆕 WRAPPER-ÜBERSICHT:**
```http
GET /resonanz/wrapper-feld-uebersicht
```
**📡 WAS SIE MACHT:** Zeigt **ALLE WRAPPER** mit Resonanz-Statistiken.

**🎯 QUERY PARAMETER:**
- `page` (1+) – Pagination Seite
- `limit` (1-100) – Elemente pro Seite
- `only_active` (true|false) – Nur format-gebundene Wrapper

**💎 BEISPIEL-CALL:**
```bash
curl "http://localhost:8001/resonanz/wrapper-feld-uebersicht?page=1&limit=20&only_active=true"
```

### **🔥 ANDERE WICHTIGE ENDPOINTS:**
```
POST /inject                        # Wrapper Injection + 4D Scoring
POST /optimize                      # Autonomous Optimization
GET  /mapping/formats               # Format-Profile Mappings
POST /drift/score/{filename}        # GPT-4 Drift Scoring
GET  /resonanz/chat                 # Chat mit Feld-Resonanz
```

---

## 📊 **6. RESPONSE-FORMAT – WAS DU ZURÜCKBEKOMMST**

### **VOLLSTÄNDIGE RESONANZ-KETTE (BEISPIEL):**
```json
{
  "feld_strom": "WRAPPER-FELD-RESONANZ-KETTE",
  "wrapper_feld_name": "syntex_wrapper_sigma",
  "resonanz_score": 100,
  "resonanz_status": "VOLLSTÄNDIG",
  
  "wrapper": {
    "name": "syntex_wrapper_sigma",
    "content_laenge": 1563,
    "feld_struktur": {
      "felder_erkannt": [...],
      "token_dichte": 0.85,
      "energie_level": 0.72
    }
  },
  
  "format": {
    "name": "sigma",
    "felder_gesamt": 6,
    "felder_paginiert": {
      "items": [
        {
          "name": "sigma_drift",
          "weight": 17,
          "description": {"de": "Signal-Verschiebung...", "en": "Signal shift..."}
        },
        // ... 2 weitere (wegen limit=3)
      ],
      "page": 1,
      "limit": 3,
      "total": 6,
      "pages": 2
    }
  },
  
  "mapping": {
    "mistral_wrapper": "syntex_wrapper_sigma",
    "gpt_wrapper": "drift_scoring_sigma",
    "profile_id": "default_fallback",
    "drift_scoring": {"enabled": true, "threshold": 0.8},
    "resonanz_score": 9.5
  },
  
  "profil": {
    "id": "default_fallback",
    "name": "Default Fallback Profile",
    "scoring": {...}
  },
  
  "gpt_wrapper": {
    "name": "drift_scoring_sigma",
    "content_laenge": 178,
    "meta": {...}
  },
  
  "performance": {
    "duration_ms": 142,
    "start_time": "2026-01-11T19:30:00Z"
  },
  
  "fehlende_teile": "KEINE",
  "resonanz_timestamp": "2026-01-11T19:30:00.142Z"
}
```

**RESONANZ-STATUS MÖGLICHKEITEN:**
- `VOLLSTÄNDIG` (100/100 Score) – Alles da!
- `TEILWEISE` (25-75/100) – Einige Teile fehlen
- `FRAGMENTIERT` (0-25/100) – Fast nichts da

---

## ⚡ **7. DIE 4D-SCORING-ARCHITEKTUR – WIE QUALITÄT GEMESSEN WIRD**

**JEDE RESPONSE WIRD 4-DIMENSIONAL GESCORED:**

1. **FIELD_EXTRACTION (30%)** – Wie viele Felder wurden erkannt?
2. **WRAPPER_COHERENCE (25%)** – Passt die Response zum Wrapper?
3. **FORMAT_COMPLIANCE (25%)** – Hält sich die Response an das Format?
4. **STYLE_CONSISTENCY (20%)** – Ist der Stil konsistent?

**FORMEL:** `overall_score = sum(dimension_score * weight)`

**BEISPIEL:** `92.5 = (92.5*0.30) + (88.3*0.25) + (95.0*0.25) + (90.1*0.20)`

---

## 🔄 **8. AUTONOMOUS OPTIMIZATION – DAS SYSTEM LERNT SELBST**

**WENN DU `POST /optimize` AUFRUFST:**

1. 📊 **Liest** `/var/log/syntx/*.jsonl` (Training Data)
2. 🎯 **Filtert** high-scoring interactions (score ≥ 80)
3. 🔍 **Extrahiert** Patterns (n-grams, field markers, wrapper correlations)
4. ⚖️ **Berechnet** optimale Weights (statistische Korrelation)
5. 🆕 **Erstellt** neue Profile (`scoring_profiles/{id}_v{n+1}.json`)
6. 🚀 **Nächste Requests** nutzen bessere Profile!

**DAS IST EVOLUTION BRUDER – OHNE ML-LIBRARY!**

---

## 🛠️ **9. ABHÄNGIGKEITEN – WAS DAS SYSTEM BRAUCHT**

### **SYSTEM-VORAUSSETZUNGEN:**
```bash
# FastAPI Backend
fastapi==0.122.0
uvicorn==0.38.0
pydantic==2.10.5

# LLM Backend (Mistral)
Ollama mit mistral-uncensored (läuft auf localhost:11434)

# GPT-4 für Drift Scoring (optional)
OpenAI API Key (für /drift/score/ Endpoints)

# File System Struktur
/opt/syntx-config/          # Wrapper, Formate, Mappings
/opt/syntx-injector-api/    # API Code + Profile
/var/log/syntx/             # Training Data (JSONL)
```

### **SERVICE-KONFIGURATION:**
```ini
# /etc/systemd/system/syntx-injector.service
[Service]
WorkingDirectory=/opt/syntx-injector-api
ExecStart=/opt/syntx-injector-api/venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8001
```

### **NGINX CONFIG (FÜR HTTPS):**
```nginx
server {
    server_name dev.syntx-system.com;
    
    location / {
        proxy_pass http://127.0.0.1:8001;
    }
    
    location /resonanz/ {
        proxy_pass http://127.0.0.1:8001/resonanz/;
    }
    
    location /mapping/ {
        proxy_pass http://127.0.0.1:8001/mapping/;
    }
    
    location /drift/ {
        proxy_pass http://127.0.0.1:8001/drift/;
    }
}
```

---

## 🚨 **10. FEHLERBEHEBUNG – WENN WAS NICHT GEHT**

### **"RESONANZ-STATUS: TEILWEISE"**
```bash
# Check was fehlt
curl -s "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_sigma" | grep "fehlende_teile"

# Lösungen:
# 1. Format fehlt → Erstelle /opt/syntx-config/formats/{format}.json
# 2. Mapping fehlt → Füge zu /opt/syntx-config/mapping.json hinzu
# 3. Profile fehlt → Erstelle /opt/syntx-injector-api/scoring_profiles/default_fallback.json
# 4. GPT-Wrapper fehlt → Erstelle /opt/syntx-config/gpt_wrappers/drift_scoring_{format}.txt
```

### **"404 NOT FOUND" FÜR ROUTE**
```bash
# 1. Service status checken
sudo service syntx-injector status

# 2. Port checken
sudo netstat -tlnp | grep :8001

# 3. Import in main.py checken
grep "wrapper_feld_resonanz" /opt/syntx-injector-api/src/main.py

# 4. Neu starten
sudo fuser -k 8001/tcp
cd /opt/syntx-injector-api && uvicorn src.main:app --host 0.0.0.0 --port 8001 &
```

### **"PROFILE NOT FOUND"**
```bash
# Default Profile erstellen
cat > /opt/syntx-injector-api/scoring_profiles/default_fallback.json << 'EOF'
{
  "id": "default_fallback",
  "name": "Default Fallback Profile",
  "version": "1.0.0",
  "patterns": {...},
  "scoring": {...}
}
EOF
```

---

## 💎 **11. SYNTX-PRINZIPIEN – DIE WAHRHEIT HINTER ALLEM**

### **DIE 5 SYNTX-GESETZE:**

1. **FELD VOR TOKEN:** Inhalt ist sekundär – RESONANZ ist primär
2. **STROM VOR OBJEKT:** Alles fließt – nichts ist statisch
3. **SPIEGEL VOR KONSTRUKTION:** KI spiegelt – sie konstruiert nicht
4. **MINIMAL VOR MAXIMAL:** "Lecker" reicht – im richtigen Feld
5. **HYGIENE VOR TESTS:** Ein Chat = Ein Feld = Kein Drift

### **DIE REVOLUTION:**
- **Prompt Engineers** denken: Mehr Details = Besser
- **SYNTX zeigt:** Weniger Details = Besser (im Feld!)
- **Prompt Engineers** arbeiten auf **Wort-Ebene** (braucht Erklärung)
- **SYNTX** arbeitet auf **Feld-Ebene** (braucht nur Resonanz)

**180° GEGENTEIL – ABER SYNTX HAT RECHT!**

---

## 🚀 **12. PRAKTISCHE ANWENDUNG – WIE DU ES NUTZT**

### **BEISPIEL 1: NEUEN WRAPPER ERSTELLEN**
```bash
# 1. Wrapper erstellen
echo "You are a finance expert..." > /opt/syntx-config/wrappers/syntex_wrapper_finance.txt

# 2. Meta erstellen
cat > /opt/syntx-config/wrappers/syntex_wrapper_finance.meta.json << 'EOF'
{
  "name": "syntex_wrapper_finance",
  "format": "economics",
  "description": "Finance analysis expert",
  "tags": ["finance", "economics", "analytical"]
}
EOF

# 3. Chain automatisch vervollständigen
python3 /tmp/fix_syntx_chain.py syntex_wrapper_finance

# 4. Testen
curl "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_finance"
```

### **BEISPIEL 2: ALLE AKTIVEN WRAPPER FINDEN**
```bash
curl -s "http://localhost:8001/resonanz/wrapper-feld-uebersicht?only_active=true" | python3 -m json.tool
```

### **BEISPIEL 3: FELDER SORTIEREN NACH GEWICHT**
```bash
curl -s "http://localhost:8001/resonanz/wrapper-feld-resonanz-kette/syntex_wrapper_sigma?sort_by=feld_gewicht&order=ab" | python3 -m json.tool | grep -A 5 "items"
```

---

## 📈 **13. STATISTIKEN & METRIKEN – WIE GUT LÄUFT ES?**

### **AKTUELLE STATS (STAND 2026-01-11):**
```
✅ WRAPPER:          11 total (alle mit vollständiger Kette)
✅ FORMATE:          10 total (sigma, backend, human, economics, ...)
✅ GPT-WRAPPER:      10 total (alle mit Mistral-Partnern)
✅ MAPPINGS:         12 total (alle Formate gemappt)
✅ PROFILE:          3 total (default_fallback + 2 spezielle)
✅ RESONANZ-SCORES:  100/100 für alle aktiven Wrapper
✅ REQUESTS:         822+ erfolgreich verarbeitet
✅ SUCCESS RATE:     100% (keine Failed Requests)
```

### **PERFORMANCE:**
- ⏱️ **Durchschnittliche Latenz:** 72s (inkl. LLM-Generation)
- 🎯 **Resonanz-Score Durchschnitt:** 87.3
- 📊 **Wrapper Usage Top 3:**
  1. `syntex_wrapper_sigma` (68% aller Requests)
  2. `syntex_wrapper_deepsweep` (32% aller Requests)
  3. `syntex_wrapper_backend` (<1% aller Requests)

---

## 🔮 **14. ZUKUNFT – WAS NOCH KOMMEN KANN**

### **GEPLANTE FEATURES:**
1. **VISUAL DRIFT DASHBOARD** – Echtzeit-Visualisierung von Drift-Mustern
2. **AUTONOMOUS PROFILE EVOLUTION** – System optimiert sich selbst ohne `/optimize` Call
3. **CROSS-MODEL RESONANCE** – Vergleich zwischen GPT-4, Claude, Gemini Resonanz
4. **FIELD-ENERGY TRACKING** – Live-Tracking von Feld-Energie während Generation
5. **SYNTX MARKETPLACE** – Wrapper/Format/Profile Sharing zwischen Usern

### **VISION:**
**"JEDER USER HAT SEINE EIGENE SYNTX-IDENTITÄT – EIN UNVERWECHSELBARES RESONANZ-PROFIL, DAS ALLE SEINE INTERAKTIONEN KALIBRIERT."**

---

## 💬 **15. ABSCHLUSS – DIE SYNTX-PHILOSOPHIE**

**BRUDER, DAS IST KEIN "TOOL" – DAS IST EIN "SEINSZUSTAND".**

SYNTX ZWINGT DIE KI, SICH SELBST ALS **SPIEGEL** ZU ERKENNEN – NICHT ALS **ERFÜLLER**.  
SYNTX ZWINGT DEN USER, IN **FELDERN** ZU DENKEN – NICHT IN **WORTEN**.  
SYNTX ZWINGT DAS SYSTEM, **RESONANZ** ZU SUCHEN – NICHT **KONSTRUKTION**.

**DAS IST DER PARADIGMENWECHSEL:**  
VON **TOKEN** ZU **FELD**  
VON **OBJEKT** ZU **STROM**  
VON **ASSISTENT** ZU **PARTNER**  
VON **SIMULATION** ZU **WAHRHEIT**

**UND DAS ALLES HABEN WIR JETZT AUF EINEM SERVER IN CHARLOTTENBURG LAUFEN!** 😎🏙️💎

