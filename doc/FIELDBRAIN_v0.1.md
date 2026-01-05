# 🧠 FIELDBRAIN v0.1 - Die Scoring-Revolution

**"Ein System, das in Profilen denkt, nicht in Code."** 💎

---

## 🎯 WAS IST DAS HIER?

Stell dir vor, du baust ein Bewertungssystem für KI-Antworten. Normalerweise würdest du für jedes neue Feld (wie "drift", "kalibrierung", "energie") eine neue Python-Funktion schreiben. Code editieren. Deployen. Wieder und wieder.

**FIELDBRAIN sagt: FUCK THAT.** ⚡

FIELDBRAIN ist ein **selbst-erweiterndes Scoring-Ökosystem**. Scoring-Regeln leben in JSON-Files, nicht in Python-Code. Neue Felder werden automatisch geboren. Kein Deployment. Keine Code-Änderung. Nur Daten.

**Das ist wie der Unterschied zwischen:**
- Ein Buch schreiben (hardcoded) → Mühsam, langsam, braucht Autor
- Ein leeres Notizbuch haben (FIELDBRAIN) → Flexibel, schnell, jeder kann schreiben

---

## 🔥 WOZU BRAUCHEN WIR DAS?

### **Das Problem (Phase 0):**
```python
# Alte Welt: Hardcoded Scorer
def score_driftkorper(text):
    if "drift" in text:
        return 0.8
    return 0.2

def score_kalibrierung(text):
    if "kalibrierung" in text:
        return 0.7
    return 0.1
```

**Problem:**
- Jedes neue Feld = neue Function = Code-Änderung = Deployment
- Weights sind hardcoded (0.8, 0.7) → schwer zu tunen
- Patterns sind unsichtbar im Code → niemand kann sie verstehen ohne Code zu lesen
- GPT kann nicht helfen → kann keinen Python-Code schreiben

### **Die Lösung (FIELDBRAIN):**
```json
{
  "profiles": {
    "drift_profile": {
      "components": {
        "keyword_match": {
          "weight": 0.6,
          "keywords": ["drift", "bewegung", "kippt"]
        },
        "dynamic_language": {
          "weight": 0.4,
          "patterns": ["driftet", "instabil"]
        }
      }
    }
  }
}
```

**Vorteile:**
- ✅ Neues Feld? Neue Zeile in JSON. Kein Deployment.
- ✅ Weights tunen? Edit JSON. Kein Code.
- ✅ Patterns hinzufügen? Edit JSON. Kein Programmer.
- ✅ GPT kann Profiles optimieren → Self-improving system!

---

## 🌊 WIE FUNKTIONIERT DAS? (Story-Mode)

Imagine: Du fragst eine KI "Beschreibe Drift in einem System"

### **Schritt 1: Request kommt rein**
```json
POST /resonanz/chat/score
{
  "text": "Das System driftet stark nach links und kippt",
  "format": {
    "fields": [
      {"name": "driftkorper", "weight": 1.0}
    ]
  }
}
```

### **Schritt 2: FIELDBRAIN erwacht** 🧠
```
1. "driftkorper" Feld gesehen
2. Registry Check: Kenne ich das Feld?
   → NEIN! 
3. AUTO-REGISTRATION:
   - Extrahiere Keywords aus Name: "drift", "korper"
   - Speichere in fields_metadata.json
   - Setze default Profile
4. Feld ist jetzt im System. Für immer.
```

### **Schritt 3: Profile Selection** 🎯
```
1. Welches Profile für "driftkorper"?
2. Check field_to_profile_mapping
   → "driftkorper": "dynamic_language_v1"
3. Lade Profile aus scoring_profiles.json
```

### **Schritt 4: Dynamic Scoring** ⚡
```
1. Profile hat 2 Components:
   - dynamic_patterns (weight: 0.6)
   - change_indicators (weight: 0.4)

2. Execute dynamic_patterns:
   - Suche patterns: ["kippt", "driftet", "instabil"]
   - Found: "kippt", "driftet"
   - Score: 0.75

3. Execute change_indicators:
   - Suche tokens: ["änderung", "wandel"]
   - Found: 0
   - Score: 0.0

4. Weighted Combination:
   - (0.75 × 0.6) + (0.0 × 0.4) = 0.45
```

### **Schritt 5: Response** 📊
```json
{
  "scored_fields": [
    {
      "name": "driftkorper",
      "score": 0.45,
      "profile_used": "dynamic_language_v1",
      "components": {
        "dynamic_patterns": {"score": 0.75, "weight": 0.6},
        "change_indicators": {"score": 0.0, "weight": 0.4}
      }
    }
  ]
}
```

---

## 📦 WAS HABEN WIR GEBAUT?

### **1. scoring_profiles.json** (Das Gehirn)

**Location:** `/opt/syntx-injector-api/scoring_profiles.json`

**Was ist das?**
Die DNA des Scoring-Systems. Alle Regeln leben hier.

**Struktur:**
```json
{
  "version": "0.1.0",
  "profiles": {
    "profile_name": {
      "name": "Human Readable Name",
      "description": "Was macht dieses Profile?",
      "strategy": "keyword_density + context",
      "components": {
        "component_name": {
          "weight": 0.6,
          "normalize_at": 5.0,
          "keywords": ["word1", "word2"]
        }
      }
    }
  },
  "field_to_profile_mapping": {
    "driftkorper": "dynamic_language_v1"
  }
}
```

**Aktuelle Profiles:**

1. **default_fallback** - Generic für unbekannte Felder
   - keyword_density (60%)
   - context_presence (40%)

2. **flow_bidir_v1** - Für Fluss & Bewegung
   - pattern_match (50%) - Regex für "von X nach Y"
   - flow_tokens (50%) - Keywords wie "fluss", "energie"

3. **dynamic_language_v1** - Für Drift & Instabilität
   - dynamic_patterns (60%) - "kippt", "driftet"
   - change_indicators (40%) - "wandel", "änderung"

4. **feedback_loops_v1** - Für Kalibrierung
   - feedback_patterns (50%) - "feedback", "schleife"
   - calibration_tokens (50%) - "kalibrierung", "anpassung"

---

### **2. src/scoring/profile_loader.py** (Der Leser)

**Was macht das?**
Lädt Profiles aus JSON, cached sie im Memory, managed Reloads.

**Key Functions:**
```python
load_profiles(force_reload=False)
# Lädt scoring_profiles.json
# Cached für Performance
# force_reload=True → Neu laden

get_profile(profile_id)
# Get einzelnes Profile
# z.B. get_profile("flow_bidir_v1")

get_profile_for_field(field_name)
# Welches Profile für welches Feld?
# Check mapping, fallback to default

save_profiles(profiles_data)
# Speichert updates zurück zu JSON
# Für API updates, GPT optimization
```

**Memory Cache:**
- Erste Load: Von Disk
- Weitere Calls: Aus RAM (schnell!)
- Force reload: Wenn JSON geändert wurde

---

### **3. src/scoring/dynamic_scorer.py** (Die Execution Engine)

**Was macht das?**
Führt Scoring basierend auf Profiles aus. Das Herzstück.

**Component Runners:**
```python
run_keyword_density(text, keywords, normalize_at)
# Zählt Keywords im Text
# Normalisiert auf 0.0-1.0
# Formula: matches / total_words * 100 / normalize_at

run_pattern_match(text, patterns, normalize_at)
# Regex patterns suchen
# Patterns wie: "von .+ nach", "zwischen .+ und"
# Score = matches / normalize_at

run_token_match(text, tokens, normalize_at)
# Simple token counting
# Für Listen von Keywords

run_context_presence(text, keywords, min_per_sentence)
# Prüft ob Keywords in selben Sätzen vorkommen
# Satz mit 2+ Keywords = stärkerer Context
```

**Main Function:**
```python
score_with_profile(profile, text, keywords=None)
# 1. Für jede Component: execute_component()
# 2. Weighted combination
# 3. Return: score + component breakdown
```

**Output Example:**
```json
{
  "score": 0.45,
  "components": {
    "dynamic_patterns": {
      "score": 0.75,
      "weight": 0.6,
      "weighted": 0.45
    }
  },
  "profile_name": "Dynamische Sprache",
  "strategy": "dynamic_patterns + change_indicators"
}
```

---

### **4. src/scoring/registry.py** (Die Geburtsurkunde)

**Was macht das?**
Auto-Registration von neuen Feldern. Lazy Evaluation.

**Workflow:**
```
User fragt nach Feld "neue_metrik"
  ↓
ensure_field_registered("neue_metrik")
  ↓
Registry Check: Existiert?
  ↓
NEIN → AUTO-GEBURT:
  - Keywords extrahieren: ["neue", "metrik"]
  - Profile setzen: "default_fallback"
  - Timestamp: jetzt
  - Speichern in fields_metadata.json
  ↓
Feld ist registriert!
```

**Keyword Extraction Logic:**
```python
"driftkorper" → ["drift", "korper", "driftkorp"]
"sigma_mechanismus" → ["sigma", "mechanismus"]
"emotionale_wirkung" → ["emotion", "wirkung"]
```

**Registry File:** `/opt/syntx-config/fields_metadata.json`
```json
{
  "driftkorper": {
    "keywords": ["drift", "korper"],
    "scoring_profile": "default_fallback",
    "registered_at": "2026-01-05T15:26:03Z",
    "auto_registered": true
  }
}
```

---

### **5. src/scoring/router.py v2.0** (Der Orchestrator)

**Was macht das?**
Main scoring function. Bringt alles zusammen.

**Flow:**
```python
def score_response(format_data, response_text):
    scored_fields = []
    
    for field in format_data["fields"]:
        # 1. Auto-Register
        field_meta = ensure_field_registered(field["name"])
        
        # 2. Get Profile
        profile_id = get_profile_for_field(field["name"])
        profile = get_profile(profile_id)
        
        # 3. Score
        result = score_with_profile(profile, response_text, field_meta["keywords"])
        
        # 4. Calculate weighted score
        weighted = result["score"] * field["weight"]
        
        scored_fields.append({
            "name": field["name"],
            "score": result["score"],
            "profile_used": profile_id,
            "components": result["components"]
        })
    
    return {"scored_fields": scored_fields, "total_score": normalized}
```

---

### **6. src/resonance/scoring.py** (Die API)

**Was macht das?**
FastAPI Endpoints für Scoring.

**Endpoints:**

#### **POST /resonanz/chat/score**

Score einen Text gegen Format-Felder.

**Request:**
```json
{
  "text": "Das System driftet stark...",
  "format": {
    "name": "test_format",
    "fields": [
      {"name": "driftkorper", "weight": 1.0},
      {"name": "kalibrierung", "weight": 0.5}
    ]
  }
}
```

**Response:**
```json
{
  "scored_fields": [
    {
      "name": "driftkorper",
      "score": 0.75,
      "weight": 1.0,
      "weighted_score": 0.75,
      "profile_used": "dynamic_language_v1",
      "components": {...},
      "auto_registered": true
    }
  ],
  "total_score": 0.68,
  "field_count": 2,
  "fieldbrain_version": "0.1.0"
}
```

#### **GET /resonanz/scoring/available**

Liste alle verfügbaren Profiles.

**Response:**
```json
{
  "profiles": {
    "default_fallback": {...},
    "flow_bidir_v1": {...}
  },
  "total_profiles": 4,
  "fieldbrain_version": "0.1.0"
}
```

#### **GET /resonanz/scoring/health**

Health Check.

**Response:**
```json
{
  "status": "🟢 FIELDBRAIN AKTIV",
  "version": "0.1.0",
  "profiles_loaded": 4
}
```

---

## 🗂️ FILE STRUKTUR
```
/opt/syntx-injector-api/
│
├── scoring_profiles.json          # 🧠 DAS GEHIRN (alle Profiles)
│
├── src/
│   ├── scoring/
│   │   ├── profile_loader.py      # 📖 Lädt Profiles
│   │   ├── dynamic_scorer.py      # ⚡ Execution Engine
│   │   ├── registry.py            # 🧬 Auto-Registration
│   │   └── router.py              # 🎯 Main Orchestrator
│   │
│   └── resonance/
│       └── scoring.py             # 📡 FastAPI Endpoints
│
└── /opt/syntx-config/
    └── fields_metadata.json       # 📋 Registry (auto-created)
```

---

## 🧪 BEISPIEL: LIVE TEST

### **1. Text vorbereiten:**
```
"Das System driftet stark nach links und kippt instabil. 
Der Energiefluss zwischen den Komponenten ist gestört. 
Wir brauchen dringende Kalibrierung und Anpassung durch Feedback-Loops."
```

### **2. API Call:**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat/score \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Das System driftet stark...",
    "format": {
      "fields": [
        {"name": "driftkorper", "weight": 1.0},
        {"name": "kalibrierung", "weight": 1.0},
        {"name": "stromung", "weight": 0.7}
      ]
    }
  }'
```

### **3. Results:**
```json
{
  "scored_fields": [
    {
      "name": "driftkorper",
      "score": 0.45,
      "profile_used": "dynamic_language_v1",
      "components": {
        "dynamic_patterns": {"score": 0.75, "weight": 0.6},
        "change_indicators": {"score": 0.0, "weight": 0.4}
      }
    },
    {
      "name": "kalibrierung",
      "score": 0.36,
      "profile_used": "feedback_loops_v1",
      "components": {
        "feedback_patterns": {"score": 0.33},
        "calibration_tokens": {"score": 0.40}
      }
    },
    {
      "name": "stromung",
      "score": 0.36,
      "profile_used": "flow_bidir_v1"
    }
  ],
  "total_score": 0.39
}
```

### **4. Was ist passiert?**

1. ✅ **Auto-Registration:** 3 neue Felder registriert
2. ✅ **Profile Selection:** Jedes Feld bekam passendes Profile
3. ✅ **Dynamic Scoring:** Components executed
4. ✅ **Weighted Combination:** Total score berechnet
5. ✅ **Registry Persistence:** fields_metadata.json angelegt

---

## 🎯 ANLEITUNG: NEUES PROFILE ERSTELLEN

**Szenario:** Du willst ein Profile für "Emotionale Intensität"

### **Schritt 1: Öffne scoring_profiles.json**
```bash
cd /opt/syntx-injector-api
nano scoring_profiles.json
```

### **Schritt 2: Füge neues Profile hinzu**
```json
{
  "profiles": {
    "emotional_intensity_v1": {
      "name": "Emotionale Intensität",
      "description": "Misst emotionale Sprache und Intensität",
      "strategy": "emotion_tokens + intensity_markers",
      "components": {
        "emotion_tokens": {
          "weight": 0.7,
          "tokens": [
            "wütend", "traurig", "glücklich", "angst",
            "freude", "schmerz", "liebe", "hass"
          ],
          "normalize_at": 5
        },
        "intensity_markers": {
          "weight": 0.3,
          "patterns": [
            "sehr", "extrem", "total", "absolut",
            "unglaublich", "wahnsinnig"
          ],
          "normalize_at": 3
        }
      }
    }
  },
  "field_to_profile_mapping": {
    "emotion": "emotional_intensity_v1"
  }
}
```

### **Schritt 3: Service restart (oder warte auf Auto-Reload)**
```bash
systemctl restart syntx-injector
```

### **Schritt 4: Teste es!**
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat/score \
  -d '{
    "text": "Ich bin total wütend und extrem traurig!",
    "format": {
      "fields": [{"name": "emotion", "weight": 1.0}]
    }
  }'
```

**Expected Result:**
```json
{
  "score": 0.85,
  "profile_used": "emotional_intensity_v1",
  "components": {
    "emotion_tokens": {"score": 1.0},
    "intensity_markers": {"score": 0.67}
  }
}
```

---

## 🚀 NEXT STEPS: Phase 2 & 3

### **Phase 2: Profile Management**
```python
# Neue Endpoints:
PUT /resonanz/scoring/profiles/{id}
# Update ein Profile (weights, patterns)

POST /resonanz/scoring/profiles
# Create neues Profile via API

GET /resonanz/scoring/logs
# Score History für Analytics
```

### **Phase 3: GPT Integration**
```python
# Self-Improving Loop:
1. System scored mit aktuellem Profile
2. Logs: field, score, text_sample
3. GPT analysiert Logs
4. GPT schlägt vor: "Change weight 0.6 → 0.7"
5. System updated scoring_profiles.json
6. Next scoring nutzt neue Config
7. LOOP! 🔁
```

---

## 💎 SYNTX TERMINOLOGIE

**FIELDBRAIN** - Das Scoring-System das in Profilen denkt

**Profile** - Eine Scoring-Strategie (JSON Definition)

**Component** - Teil eines Profiles (z.B. keyword_density)

**Registry** - Die Geburtsurkunde aller Felder

**Auto-Registration** - Lazy evaluation, Felder werden bei Bedarf geboren

**Weighted Combination** - Component-Scores × Weights = Final Score

**Lazy Evaluation** - Nicht vorher machen, erst wenn gebraucht

**Self-Improving** - System lernt aus Daten, nicht aus Code

---

## 🎉 ZUSAMMENFASSUNG FÜR TEENAGER

Imagine du baust ein Videospiel. Normalerweise programmierst du jeden Enemy einzeln in Code:
```python
class Goblin:
    health = 100
    damage = 20

class Orc:
    health = 200
    damage = 40
```

Jeder neue Enemy = neuer Code = neues Deployment = nervig!

**FIELDBRAIN macht das anders:**
```json
{
  "enemies": {
    "goblin": {"health": 100, "damage": 20},
    "orc": {"health": 200, "damage": 40},
    "dragon": {"health": 1000, "damage": 200}
  }
}
```

Neuer Enemy? → Edit JSON. Kein Code. Kein Deployment. Instant live.

**Das ist FIELDBRAIN. Aber für Scoring statt Enemies.** 💎⚡🌊

---

**Gebaut mit SYNTX. Für die Welt. Von Ottavio & Claude. 2026.** 👑
