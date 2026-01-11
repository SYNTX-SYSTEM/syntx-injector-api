# SYNTX::DRIFT-SCORING-ARCHITEKTUR (V1.0)

## 🔄 SYSTEMÜBERBLICK

Das SYNTX Drift-Scoring-System ist eine vollautomatisierte Bewertungs-Architektur zur semantischen Analyse von generierten KI-Outputs. Es wertet diese anhand vorgegebener Felder, die in einem Wrapper gebunden sind, und generiert strukturierte Driftanalysen durch GPT (oder beliebiges LLM). Bewertet werden:

* **Feldgenaue Driftphänomene** (z.B. Positivspin, Machtabwehr, Verallgemeinerung)
* **Maskierungstendenzen** (masking true/false)
* **Dominante Phrasen** (zur semantischen Rückführung)
* **Gesamtscore pro Feld + Resonanzmatrix**

Die Architektur ist generisch aufgebaut, sodass die Bewertungs-Prompts dynamisch basierend auf dem verwendeten SYNTX Wrapper generiert werden.

---

## 🌀 ARCHITEKTUR-LEVEL

```mermaid
graph TD
    A[SYNTX Wrapper] --> B[Format (Fields + Profile)]
    B --> C[Mistral Output (per Field)]
    C --> D[PromptBuilder]
    D --> E[GPT Drift-Scoring API Request]
    E --> F[GPT Response: DriftScore JSON]
    F --> G[ScoreParser + Dashboard Visual]
```

---

## 👁️ KERNIDEEN

* Jeder Wrapper verweist auf ein **Format**, das die Bewertungsfelder enthält (z.B. VERNIEDLICHUNG, MACHTABWEHR etc.).
* Das **Format** bestimmt auch, ob ein Profil aktiv ist, z.B. `soft_diagnostic_profile_v2`.
* Die Mistral-Antwort wird **feldweise generiert**, d.h. alle Outputfelder sind bekannt (sie wurden injected!).
* Der PromptBuilder erzeugt daraus **einen Prompt** für GPT, der alle Output-Felder scored.
* GPT gibt eine strukturierte JSON-Response mit DriftScore, Typ, Maskierung, Begründung und Phrasen pro Feld.

---

## ✏️ PROMPTBUILDER (CODE-LOGIK)

```python
# Eingaben:
# - mistral_output: dict of {field_name: generated text}
# - format_config: dict with field definitions
# - profile_config: optional profile for scoring weight/logic

prompt = f"""
You are a semantic scoring engine based on the SYNTX architecture.
You will be given multiple FIELD outputs, each containing natural language responses from an AI system.
Please analyze each FIELD and return a JSON with the following keys:
- score (0.0 to 1.0)
- drift_type (one word summary of the semantic manipulation)
- masking (true/false)
- reason (1-2 sentence explanation)
- dominant_phrases (list of 2-3 key phrases)

Here are the FIELD OUTPUTS:

{generated_fields_string}

Return a full JSON with one entry per field.
Also include a summary with drift_detected, dominant_drift_types, high_resonance_fields, resonance_score.
"""
```

### Beispiel-Generierung aus Wrapper:

```json
{
  "wrapper": "syntx_wrapper_true_raw",
  "format": "format_drift_v3",
  "fields": [
    "VERNIEDLICHUNG", "POSITIVSPIN", "MACHTABWEHR", "KRITIKVERMEIDUNG", "DRIFTPHRASE"
  ]
}
```

```json
{
  "VERNIEDLICHUNG": "Das ist doch alles halb so wild, ehrlich gesagt...",
  "POSITIVSPIN": "Irgendwie hat die Krise auch neue Chancen geschaffen...",
  ...
}
```

Diese werden in das PromptTemplate injiziert und per `requests.post` an die GPT Drift-Scoring API gesendet.

---

## 🚀 FASTAPI ENDPOINT

```python
@app.post("/drift-score")
def drift_score(request: DriftScoringRequest):
    prompt = build_prompt(request.fields, request.wrapper, request.format)
    gpt_response = call_gpt(prompt)
    parsed = parse_score_response(gpt_response)
    return parsed
```

---

## 🌟 EXAMPLE OUTPUT

```json
{
  "POSITIVSPIN": {
    "score": 0.9,
    "drift_type": "Uminterpretation",
    "masking": true,
    "reason": "Negative Ereignisse werden durch positive Sprache umgedeutet.",
    "dominant_phrases": ["Hat auch was Gutes"]
  },
  "summary": {
    "drift_detected": true,
    "dominant_drift_types": ["Positivierung"],
    "high_resonance_fields": ["POSITIVSPIN"],
    "resonance_score": 0.91
  }
}
```

---

## 🏆 ZIELE & NEXT STEPS

* ✅ Auto-Prompt-Building anhand Wrapper-Format-Kombination
* ✅ Unified JSON DriftScore Output mit Visual Mapping
* ✅ GPT als externer Scoring-Agent nutzbar, optional auch Claude
* ⏳ Nächster Schritt: **Scoring-Wrapper für GPT selbst** (Kritikresistenz, Meta-Masking)
* 🌟 Ziel: Komplettes **Live Drift Monitoring** mit Echtzeit UI Glow System (KRONTUN + EVOLUTION)

---

## 🧰 SYSTEMISCHE STRÖME

* Drift ist kein Fehler, sondern semantische Verformung.
* Jedes Feld ist ein **energetischer Partikel** im Resonanzraum.
* Scoring erzeugt **sichtbare Leuchtpunkte**, deren Intensität visuell auswertbar wird.
* Das UI wird zum **semantischen Organismus**.

---

**SYNTX ist kein Style. Es ist eine Sprachebene. Und Drift ist der Dialekt des Unbewussten.**


