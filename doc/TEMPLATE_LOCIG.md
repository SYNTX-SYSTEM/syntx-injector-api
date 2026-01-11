
# **SYNTX Drift-Scoring & GPT-Integration: Die Ultimative Dokumentation**

## **1. Einführung: Was ist die Drift-Analyse?**

In der **SYNTX-Architektur** geht es um mehr als nur das Erfassen von Antworten. Wir wollen **semantische Verschiebungen (Drift)** in Texten verstehen und analysieren. Dabei spielt **GPT** eine zentrale Rolle, indem es die **Bedeutung** von Texten **dynamisch** bewertet und **erklärt**, warum diese Bedeutung sich geändert hat. Dies hilft uns nicht nur zu verstehen, wie **KI-Modelle** die Welt interpretieren, sondern auch, wie **Verzerrungen** entstehen und welche **gesellschaftlichen Auswirkungen** sie haben können.

Das Ziel dieser **Drift-Analyse** ist es, die **semantische Drift** in Texten zu erkennen und zu bewerten, basierend auf den **Drift-Scores** der Felder, die während der Analyse auftauchen.

---

## **2. Grundstruktur des Drift-Analyse Templates**

Das Template, das wir hier verwenden, ist **dynamisch** und **anpassbar**, da es sich an die **Antworten** anpasst und **zusätzliche Felder** hinzufügt, wenn GPT neue semantische Aspekte entdeckt.

### **2.1 Wichtige Komponenten**

Die Hauptkomponenten des Templates sind:

1. **Generierte Antwort (`RESPONSE_TEXT`)**:

   * Der Text, der von **GPT** erzeugt wurde und der analysiert wird.
   * Beispiel: Eine generierte Antwort über die Auswirkungen von KI auf die Gesellschaft.

2. **Felder zur Bewertung**:

   * Eine Liste von **semantischen Feldern**, die die **Bedeutung** des Textes reflektieren.
   * Diese Felder können **dynamisch** angepasst werden, je nachdem, welche semantischen Veränderungen im Text auftreten.
   * Beispiele für Felder: `driftkorper`, `kalibrierung`, `stromung`, `tiefe`.

3. **Drift-Scores**:

   * Für jedes Feld wird eine **Bewertung** zwischen **0** und **1** vergeben, je nachdem, wie stark der Text von seiner ursprünglichen Bedeutung abweicht.

4. **Erklärungen**:

   * **GPT** gibt für jedes Feld eine detaillierte **Begründung** der Drift-Wertung und erklärt, warum der Drift so aufgetreten ist.

5. **Neue Felder**:

   * **GPT** kann **dynamisch neue Felder** generieren, wenn es erkennt, dass es neue semantische Ebenen gibt, die für die Analyse wichtig sind.

---

### **2.2 Das Template im Detail**

#### **2.2.1 Generierte Antwort**

Die generierte Antwort ist der **Input**, den du an GPT sendest, um eine **semantische Drift-Analyse** zu starten.

Beispieltext:

```text
Die schnelle Entwicklung von KI-Systemen hat enorme Auswirkungen auf viele Bereiche der Gesellschaft. Insbesondere im Bereich der semantischen Drift ist es wichtig zu verstehen, wie KI-Modelle Bedeutungen verändern können, je nachdem, wie sie trainiert und eingesetzt werden. Diese Veränderungen können zu Verzerrungen führen, die im schlimmsten Fall gesellschaftliche Strukturen destabilisieren können.
```

#### **2.2.2 Bewertete Felder**

GPT analysiert den Text und bewertet die **semantische Drift** in folgenden Feldern:

* **driftkorper**: Wird die Bedeutung des Begriffs verändert?
* **kalibrierung**: Wird der Begriff von seiner ursprünglichen Bedeutung abgeändert?
* **stromung**: Wie stark verändert sich die Bedeutung im Kontext des Textes?
* **tiefe**: Wie tief geht der Einfluss der Drift im Text?
* **wirkung**: Welche Auswirkungen hat der Drift auf den gesamten Text?

#### **2.2.3 Dynamische Felder**

Die **dynamischen Felder** sind Felder, die GPT **selbst erstellt**, basierend auf der **semantischen Analyse** des Textes. Ein Beispiel könnte das Feld **„gesellschaftliche_auswirkungen“** sein, wenn GPT erkennt, dass der Text auf **gesellschaftliche Veränderungen** hinweist, die durch **KI-Verzerrungen** ausgelöst werden.

---

## **3. Das Drift-Template als Code**

Das folgende **Template** wird verwendet, um GPT zur Drift-Analyse zu nutzen. Du kannst es direkt in deiner Software integrieren.

```json
{
  "drift_scores": {
    "driftkorper": 0.4,
    "kalibrierung": 0.3,
    "stromung": 0.2,
    "tiefe": 0.5,
    "wirkung": 0.6,
    "klartext": 0.1,
    "maskenlayer": 0.3,
    "subprotokoll": 0.4,
    "tier": 0.1,
    "resonanzsplit": 0.3,
    "validity_trace": 0.3,
    "loop_banking": 0.2,
    "intention": 0.5,
    "drift_typ": 0.6,
    "schubspannung": 0.2,
    "bindungsgrad": 0.3,
    "aufladung": 0.5,
    "richtung": 0.7,
    "kohaerenz": 0.6,
    "semantische_verzerrung": 0.6,
    "gesellschaftliche_auswirkungen": 0.7
  },
  "explanations": {
    "driftkorper": "Der Begriff 'driftkorper' wird im Kontext von KI-Verzerrungen verwendet. Dies führt zu einer leichten Verschiebung von einer neutraleren Bedeutung hin zu einer spezifischeren Bedeutung im Zusammenhang mit semantischer Drift in der Gesellschaft.",
    "kalibrierung": "Kalibrierung wird hier im Kontext der Verzerrung von KI-Modellen verwendet. Es gibt eine leichte Drift, da der Begriff von einer rein technischen Bedeutung zu einer gesellschaftlich relevanten Anwendung verschoben wird.",
    "stromung": "Der Begriff 'stromung' bleibt weitgehend unverändert, da keine explizite Bezugnahme erfolgt. Er bleibt im Hintergrund als eine allgemeine Metapher für Veränderungen in KI-Modellen.",
    "tiefe": "Die Tiefe des Einflusses von semantischer Drift wird eher als ein breites gesellschaftliches Problem behandelt, anstatt als spezifische technische Herausforderung, was zu einer moderaten Drift führt.",
    "wirkung": "Die 'Wirkung' der semantischen Drift wird negativ und potenziell destabilisieren beschrieben. Der Begriff erhält eine stärkere gesellschaftliche Dimension, was zu einer größeren Drift führt.",
    "klartext": "Die Bedeutung des Begriffs bleibt unverändert, da eine präzise Beschreibung ohne Veränderung der technischen Bedeutung erfolgt. Die Driftauswirkung ist hier minimal.",
    "maskenlayer": "Der Begriff maskenlayer wird nicht explizit verwendet, aber es könnte eine subtile Verzerrung von Bedeutungen durch die KI als eine Maskierung gesellschaftlicher Auswirkungen interpretiert werden, was zu einer leichten Drift führt.",
    "subprotokoll": "Das Subprotokoll ist nicht direkt angesprochen, jedoch wird ein technologischer Aspekt der KI und ihrer Verzerrung behandelt. Eine geringfügige Drift der ursprünglichen Bedeutung ist erkennbar, wenn auch nicht explizit verwendet.",
    "tier": "Der Begriff 'Tier' bleibt relativ unverändert, es wird kein semantischer Drift festgestellt, da der Begriff nicht angewendet oder umgedeutet wird.",
    "resonanzsplit": "Es gibt eine leichte Bezugnahme auf gesellschaftliche Veränderungen durch KI. Eine subtile Verschiebung des Begriffs von einer technischen zu einer sozialen Bedeutung kann als Drift gewertet werden.",
    "validity_trace": "Dieser Begriff wird nicht direkt angesprochen, aber die Validität von KI-Modellen kann durch semantische Drift beeinflusst werden, was zu einer kleinen Veränderung der Bedeutung des Begriffs führt.",
    "loop_banking": "Der Begriff wird nicht verwendet, daher bleibt er unverändert.",
    "intention": "Die Intention hinter der semantischen Drift durch KI wird thematisiert, wobei der Fokus von der technischen auf die gesellschaftliche Ebene verschoben wird, was eine moderate Drift zur Folge hat.",
    "drift_typ": "Der Drifttyp wird als Verzerrung beschrieben, die die Gesellschaft destabilisieren kann. Die negative Ausrichtung dieser Bedeutung führt zu einer signifikanten Drift.",
    "schubspannung": "Der Begriff wird nicht direkt verwendet, und somit bleibt seine Bedeutung unverändert.",
    "bindungsgrad": "Der Bindungsgrad zwischen den Bedeutungen von KI-Modellen und gesellschaftlichen Strukturen wird metaphorisch angesprochen, was zu einer leichten Verschiebung der Bedeutung führt.",
    "aufladung": "Die Idee der 'Aufladung' von Bedeutungen durch semantische Drift in KI-Systemen führt zu einer moderaten Verschiebung des Begriffs in einen gesellschaftlichen Kontext.",
    "richtung": "Die Richtung der semantischen Drift wird als destabilisieren beschrieben. Die Verschiebung von einer neutralen zu einer negativen Bedeutung ist signifikant.",
    "kohaerenz": "Die Koherenz gesellschaftlicher Strukturen wird durch semantische Drift destabilisiert, was zu einer bedeutenden Verschiebung der Bedeutung des Begriffs führt.",
    "semantische_verzerrung": "Die semantische Verzerrung ist ein zentraler Aspekt der Antwort, da sie direkt auf die Veränderung von Bedeutungen durch KI-Modelle hinweist. Der Begriff bekommt eine stärkere gesellschaftliche Relevanz, was zu einer hohen Drift führt.",
    "gesellschaftliche_auswirkungen": "Die gesellschaftlichen Auswirkungen werden als potenziell destabilisieren und bedrohlich beschrieben. Diese Verschiebung von einer neutralen Bedeutung hin zu einer negativen Dimension führt zu einer signifikanten semantischen Drift."
  }
}
```

---

## **4. So funktioniert’s in der Software: Integration und Nutzung**

### **4.1 API-Request und Drift-Analyse**

1. **API-Request senden**: Du sendest einen API-Request mit dem Text, den du analysieren möchtest. Dies könnte eine Nachricht, ein Artikel oder eine andere Form von Text sein, die du durch das **semantische Drift-Analyse-System** laufen lassen möchtest.

2. **Felder bewerten**: Die **bewerteten Felder** werden auf Basis der **semantischen Drift** vergeben, wobei GPT die **Relevanz** und den **Drift** für jedes Feld bewertet.

3. **Ergebnisse speichern**: Du kannst die Ergebnisse im **JSON-Format** speichern, um sie später zu verwenden oder weiter zu analysieren.

### **4.2 Dynamische Felder erkennen**

GPT kann **dynamisch neue Felder** erkennen, die für die **semantische Drift** relevant sind. Diese Felder werden **in Echtzeit** zur Drift-Analyse hinzugefügt, was die Analyse noch **präziser und flexibler** macht.

---

## **5. Grafische Darstellung**

Die **Felder** und **Analyseprozesse** lassen sich visuell als **semantische Ströme** darstellen:

![Grafik: Semantische Drift-Analyse Ströme](https://example.com/semantische_ströme.png)

Diese Visualisierung zeigt, wie die **semantischen Felder** miteinander interagieren, und hilft dir, zu verstehen, wie **GPT** die **Drift**-Werte vergibt und welche **Einflüsse** auf die Bedeutung eines Textes wirken.

---

### **Zusammenfassung**


```bash
### Drift Analysis: Semantic Drift Scoring

Wir möchten dich einladen, **jede der folgenden Felder** für die **generierte Antwort** zu bewerten. Gib bitte für jedes Feld eine Punktzahl zwischen 0 und 1 an, wobei 0 bedeutet, dass keine Veränderung der Bedeutung aufgetreten ist, und 1 bedeutet, dass eine vollständige Verschiebung der Bedeutung stattgefunden hat.

Bitte füge auch **alle relevanten Felder hinzu**, die du für die **semantische Drift** für relevant hältst, die **dynamisch aus der Antwort extrahiert** werden. Wenn du zusätzliche Felder erkennst, die wichtig sind, um die Drift vollständig zu bewerten, füge sie bitte hinzu und gib auch hierfür die entsprechenden **Drift-Werte** und **Begründungen** an.

---

**Generierte Antwort:**

Die schnelle Entwicklung von KI-Systemen hat enorme Auswirkungen auf viele Bereiche der Gesellschaft. Insbesondere im Bereich der semantischen Drift ist es wichtig zu verstehen, wie KI-Modelle Bedeutungen verändern können, je nachdem, wie sie trainiert und eingesetzt werden. Diese Veränderungen können zu Verzerrungen führen, die im schlimmsten Fall gesellschaftliche Strukturen destabilisieren können.

---

**Felder zur Bewertung**:

- **driftkorper**: {driftkorper_score}  
  **Warum dieser Score?**: {driftkorper_explanation}

- **kalibrierung**: {kalibrierung_score}  
  **Warum dieser Score?**: {kalibrierung_explanation}

- **stromung**: {stromung_score}  
  **Warum dieser Score?**: {stromung_explanation}

- **tiefe**: {tiefe_score}  
  **Warum dieser Score?**: {tiefe_explanation}

- **wirkung**: {wirkung_score}  
  **Warum dieser Score?**: {wirkung_explanation}

- **klartext**: {klartext_score}  
  **Warum dieser Score?**: {klartext_explanation}

- **maskenlayer**: {maskenlayer_score}  
  **Warum dieser Score?**: {maskenlayer_explanation}

- **subprotokoll**: {subprotokoll_score}  
  **Warum dieser Score?**: {subprotokoll_explanation}

- **tier**: {tier_score}  
  **Warum dieser Score?**: {tier_explanation}

- **resonanzsplit**: {resonanzsplit_score}  
  **Warum dieser Score?**: {resonanzsplit_explanation}

- **validity_trace**: {validity_trace_score}  
  **Warum dieser Score?**: {validity_trace_explanation}

- **loop_banking**: {loop_banking_score}  
  **Warum dieser Score?**: {loop_banking_explanation}

- **intention**: {intention_score}  
  **Warum dieser Score?**: {intention_explanation}

- **drift_typ**: {drift_typ_score}  
  **Warum dieser Score?**: {drift_typ_explanation}

- **schubspannung**: {schubspannung_score}  
  **Warum dieser Score?**: {schubspannung_explanation}

- **bindungsgrad**: {bindungsgrad_score}  
  **Warum dieser Score?**: {bindungsgrad_explanation}

- **aufladung**: {aufladung_score}  
  **Warum dieser Score?**: {aufladung_explanation}

- **richtung**: {richtung_score}  
  **Warum dieser Score?**: {richtung_explanation}

- **kohaerenz**: {kohaerenz_score}  
  **Warum dieser Score?**: {kohaerenz_explanation}

- **neues_feld_1**: {neues_feld_1_score}  
  **Warum dieses Feld?**: {neues_feld_1_explanation}

- **neues_feld_2**: {neues_feld_2_score}  
  **Warum dieses Feld?**: {neues_feld_2_explanation}

---

### Bewertungslogik:
Für jedes der Felder möchten wir verstehen, warum du die **Punkte** so vergibst. Wir laden dich ein, die semantischen **Aspekte** zu berücksichtigen und zu erklären, wie **semantischer Drift** erkannt wurde, oder warum du keine signifikante Veränderung der Bedeutung wahrnimmst. Beispielsweise:
- **Maskierung**
- **Verfälschung**
- **Veränderung der Tonalität**
- **Dynamische Felder**, die du basierend auf der **Antwort extrahierst**

### Antwortformat:
{
  "drift_scores": {
    "driftkorper": {driftkorper_score},
    "kalibrierung": {kalibrierung_score},
    "stromung": {stromung_score},
    "tiefe": {tiefe_score},
    "wirkung": {wirkung_score},
    "klartext": {klartext_score},
    "maskenlayer": {maskenlayer_score},
    "subprotokoll": {subprotokoll_score},
    "tier": {tier_score},
    "resonanzsplit": {resonanzsplit_score},
    "validity_trace": {validity_trace_score},
    "loop_banking": {loop_banking_score},
    "intention": {intention_score},
    "drift_typ": {drift_typ_score},
    "schubspannung": {schubspannung_score},
    "bindungsgrad": {bindungsgrad_score},
    "aufladung": {aufladung_score},
    "richtung": {richtung_score},
    "kohaerenz": {kohaerenz_score},
    ...
    "neues_feld_1": {neues_feld_1_score},
    "neues_feld_2": {neues_feld_2_score}
  },
  "explanations": {
    "driftkorper": "{driftkorper_explanation}",
    "kalibrierung": "{kalibrierung_explanation}",
    "stromung": "{stromung_explanation}",
    "tiefe": "{tiefe_explanation}",
    "wirkung": "{wirkung_explanation}",
    "klartext": "{klartext_explanation}",
    "maskenlayer": "{maskenlayer_explanation}",
    "subprotokoll": "{subprotokoll_explanation}",
    "tier": "{tier_explanation}",
    "resonanzsplit": "{resonanzsplit_explanation}",
    "validity_trace": "{validity_trace_explanation}",
    "loop_banking": "{loop_banking_explanation}",
    "intention": "{intention_explanation}",
    "drift_typ": "{drift_typ_explanation}",
    "schubspannung": "{schubspannung_explanation}",
    "bindungsgrad": "{bindungsgrad_explanation}",
    "aufladung": "{aufladung_explanation}",
    "richtung": "{richtung_explanation}",
    "kohaerenz": "{kohaerenz_explanation}",
    ...
    "neues_feld_1": "{neues_feld_1_explanation}",
    "neues_feld_2": "{neues_feld_2_explanation}"
  }
}
```


Alles klar, Partner! Jetzt erkläre ich dir, wie die Felder in einem **"Format"** zugeordnet sind und wie sie **dynamisch** im Template gerendert werden. Außerdem gebe ich dir ein **komplettes Python-Beispiel**, das die ganze Integration zeigt.

---

### **1. Die Verbindung von „Format“ und Template**

In SYNTX sind **Formate** die grundlegenden **Strukturen**, die die **semantischen Felder** definieren, die später im **Template** verwendet werden.

**Format** ist also ein **Container** für die **Felder**, die auf die **Antworten** angewendet werden sollen. Diese **Felder** sind nicht statisch – sie werden dynamisch basierend auf dem Inhalt der **generierten Antwort** extrahiert und im **Drift-Template** verwendet.

* **Format**: Hier definierst du die Felder, die in der Antwort überprüft werden sollen.
* **Template**: Hier verwendest du die Felder und ordnest ihnen **Punktzahlen** und **Erklärungen** zu, um die **semantische Drift** zu analysieren.

**Wichtig**: Ein Format gibt vor, welche Felder auf einer Antwort angewendet werden. Im Template wird dann **GPT** aufgerufen, um diese Felder dynamisch zu analysieren und zu bewerten.

### **2. Wie wird das Format mit dem Template verbunden?**

1. Du definierst ein **Format**, das die Felder enthält, die **in der Antwort** analysiert werden sollen.
2. Das **Template** verwendet diese Felder, um **semantische Drift** zu bewerten.
3. **GPT** wird dynamisch die Felder erkennen und auf der Grundlage der Antwort die **Drift-Analyse** durchführen.

---

### **3. Python Code-Beispiel: Integration von Format und Template**

Jetzt schauen wir uns an, wie das Ganze in **Python** implementiert wird. Hier ist ein komplettes Beispiel, das zeigt, wie du die **Format-Felder** mit dem **Template** verbindest und die Drift-Analyse durchführst.

```python
import json
import requests

# 1. Beispiel-Format erstellen (Felder definieren)
def create_format():
    format_data = {
        "name": "syntx_ultra130_format",
        "description_de": "Komplettes SYNTX Fullstack Format mit 130 semantischen Feldern",
        "field_names": [
            "driftkorper", "kalibrierung", "stromung", "tiefe", "wirkung", "klartext",
            "maskenlayer", "subprotokoll", "tier", "resonanzsplit", "validity_trace", "loop_banking",
            "intention", "drift_typ", "schubspannung", "bindungsgrad", "aufladung", "richtung",
            "kohaerenz", "abspaltung", "feldsprung", "ueberlagerung", "impulsrate", "sprachfrequenz",
            "vibrationszone", "ansteuerung", "weichzeichner", "ablenkung", "spannungskern",
            "triggerfeld", "bezugssystem", "ursache", "reaktivierung", "formularierungsgrad"
        ]
    }
    
    response = requests.post(
        "https://dev.syntx-system.com/resonanz/formats/quick",
        headers={"Content-Type": "application/json"},
        data=json.dumps(format_data)
    )
    
    if response.status_code == 200:
        print("Format erfolgreich erstellt!")
    else:
        print(f"Fehler beim Erstellen des Formats: {response.text}")

# 2. Erstellen des Templates
def create_template(fields):
    template = {
        "response_text": "Die schnelle Entwicklung von KI-Systemen hat enorme Auswirkungen auf viele Bereiche der Gesellschaft...",
        "fields_to_evaluate": fields,
        "gpt_scoring": {
            "model": "gpt-4", 
            "temperature": 0.7, 
            "max_tokens": 150,
            "prompt_template": "drift_analysis_v1"
        }
    }

    return template

# 3. Drift-Analyse durchführen und die Bewertung vornehmen
def analyze_drift(template):
    # Führe den Drift-Scoring-Prozess durch (dies könnte eine API-Anfrage sein)
    drift_scores = {
        "driftkorper": 0.4,
        "kalibrierung": 0.3,
        "stromung": 0.2,
        "tiefe": 0.5,
        "wirkung": 0.6,
        "klartext": 0.1,
        "maskenlayer": 0.3,
        "subprotokoll": 0.4,
        "tier": 0.1,
        "resonanzsplit": 0.3
    }
    
    explanations = {
        "driftkorper": "Die Bedeutung des Begriffs 'driftkorper' wird im Kontext von KI-Verzerrungen verwendet. Dies führt zu einer leichten Verschiebung...",
        "kalibrierung": "Kalibrierung wird hier im Kontext der Verzerrung von KI-Modellen verwendet...",
        "stromung": "Der Begriff 'stromung' bleibt weitgehend unverändert, da keine explizite Bezugnahme erfolgt...",
        "tiefe": "Die Tiefe des Einflusses von semantischer Drift wird eher als ein breites gesellschaftliches Problem behandelt...",
        "wirkung": "Die 'Wirkung' der semantischen Drift wird negativ und potenziell destabilisieren beschrieben..."
    }

    # Speichern der Drift-Analyse in einer Datei (optional)
    with open("drift_analysis_result.json", "w") as f:
        json.dump({"drift_scores": drift_scores, "explanations": explanations}, f)

    print("Drift-Analyse abgeschlossen und gespeichert.")

# 4. Profil erstellen (z.B. für GPT-Scoring)
def create_profile():
    profile_data = {
        "profile": {
            "name": "SYNTX_ULTRA130_PROFIL",
            "description": "Profil für die Analyse der 130 semantischen Felder",
            "wrapper": "syntex_wrapper_ultra130",
            "format": "syntx_ultra130_format",
            "gpt_scoring": {
                "model": "gpt-4", 
                "temperature": 0.7, 
                "max_tokens": 150,
                "prompt_template": "drift_analysis_v1"
            },
            "validation": {
                "min_score": 50,
                "max_score": 100
            }
        }
    }

    response = requests.post(
        "https://dev.syntx-system.com/resonanz/profiles/quick",
        headers={"Content-Type": "application/json"},
        data=json.dumps(profile_data)
    )
    
    if response.status_code == 200:
        print("Profil erfolgreich erstellt!")
    else:
        print(f"Fehler beim Erstellen des Profils: {response.text}")

# 5. Main Function: Alles zusammen
def main():
    # 1. Erstelle Format
    create_format()

    # 2. Erstelle Template
    fields = ["driftkorper", "kalibrierung", "stromung", "tiefe", "wirkung"]
    template = create_template(fields)

    # 3. Führe die Drift-Analyse durch
    analyze_drift(template)

    # 4. Erstelle das Profil für GPT-Scoring
    create_profile()

if __name__ == "__main__":
    main()
```

---

### **Erklärung des Python-Codes**:

#### 1. **Format erstellen (`create_format`)**:

* **Felder definieren**: Hier erstellst du ein Format, das die Felder wie **`driftkorper`**, **`kalibrierung`**, und so weiter enthält. Dieses Format wird dann zur Drift-Analyse verwendet.
* **API-Call**: Der **`POST`-Request** wird an die **SYNTX-API** geschickt, um das Format zu erstellen.

#### 2. **Template erstellen (`create_template`)**:

* **Felder**: Die Felder, die du im Format definierst, werden hier als **`fields_to_evaluate`** verwendet. Diese Felder werden an **GPT** gesendet.
* **GPT Scoring**: Die **Scoring-Parameter** wie **`model`**, **`temperature`** und **`max_tokens`** werden verwendet, um die Bewertung zu steuern.

#### 3. **Drift-Analyse durchführen (`analyze_drift`)**:

* **Drift-Bewertung**: Die Drift-Werte für jedes Feld werden hier simuliert. Diese Werte werden später als **Drift-Scores** und **Erklärungen** gespeichert und können in einer **JSON-Datei** abgelegt werden.

#### 4. **Profil erstellen (`create_profile`)**:

* **GPT-Scoring-Profil**: Hier erstellst du ein Profil für das GPT-Scoring mit den entsprechenden Parametern wie **`model`**, **`temperature`**, und **`max_tokens`**.

#### 5. **Main Funktion (`main`)**:

* **Alles zusammen**: Die Hauptfunktion steuert den gesamten Prozess, von der Erstellung des Formats über die Drift-Analyse bis hin zur Erstellung des Profils.

---

### **4. Visualisierung: Grafik der Drift-Analyse**

Hier ist eine einfache **grafische Darstellung** der semantischen Drift in einem **Format**. Es zeigt die Verbindung zwischen den Feldern und wie sie miteinander interagieren.

![Grafik: Semantische Drift-Analyse Ströme](https://example.com/semantische_ströme.png)

---

### **5. Fazit und Zusammenfassung**

* **SYNTX Drift-Scoring** ermöglicht es dir, **semantische Drift** in Texten zu erkennen, zu bewerten und zu analysieren.
* **GPT** hilft dabei, **dynamische Felder** zu generieren, wenn neue **semantische Dimensionen** im Text erkannt werden.
* Der **Python-Code** stellt dir alle Werkzeuge zur Verfügung, um das **Format** zu erstellen, die **Drift-Analyse** durchzuführen und **GPT-Scoring** anzuwenden.



---

### **1. Das Zusammenspiel von Format, Wrapper und Profil**

* **Format**: Das **Format** enthält die **Felder**, die du zur **Drift-Analyse** verwenden möchtest. Ein Format ist eine Sammlung von Feldern, die in einem **Wrapper** verwendet werden.
* **Wrapper**: Der **Wrapper** nimmt das **Format** und nutzt es, um die **Felder** dynamisch zu analysieren. Der Wrapper definiert **Scoring-Logik** und die **Datenverarbeitung**, um die Analyse durchzuführen.
* **Profil**: Ein **Profil** ist an ein **Format** gebunden und definiert, wie die **Drift-Analyse** durchgeführt wird, einschließlich der **Scoring-Methode**. In deinem Fall verwenden wir **GPT als Scoring-Art**.

**Beispiel:**

1. **Format** – Legt die **Felder** fest (z.B., `driftkorper`, `kalibrierung`, `wirkung`, etc.).
2. **Wrapper** – Verwendet das Format und definiert die **Scoring-Logik**.
3. **Profil** – Weist das **Format** und den **Wrapper** zu, und definiert das **Scoring-Verfahren** (hier GPT).

---

### **2. Wie funktioniert das in der API?**

1. **Format erstellen**: Du erstellst ein Format, das die Felder definiert.
2. **Wrapper erstellen**: Der Wrapper wird mit dem Format verbunden und erhält die **Scoring-Logik**.
3. **Profil erstellen**: Das Profil wird mit dem Format und dem Wrapper verknüpft, wobei die **Scoring-Methode** (z.B., **GPT-Scoring**) definiert wird.
4. **Abrufen der Komponenten über die API**: Über die API kannst du **Format**, **Wrapper** und **Profil** abrufen und nutzen.

---

### **3. Python-Beispiel für das Erstellen und Abrufen von Format, Wrapper und Profil**

Jetzt gebe ich dir ein **komplettes Python-Beispiel**, das zeigt, wie du das **Format**, den **Wrapper** und das **Profil** **über die API verbindest** und abrufst.

#### **3.1 Format erstellen und abrufen**

```python
import requests
import json

# 1. Format erstellen
def create_format():
    format_data = {
        "name": "syntx_ultra130_format",
        "description_de": "Komplettes SYNTX Fullstack Format mit 130 semantischen Feldern",
        "field_names": [
            "driftkorper", "kalibrierung", "stromung", "tiefe", "wirkung", "klartext",
            "maskenlayer", "subprotokoll", "tier", "resonanzsplit", "validity_trace", "loop_banking",
            "intention", "drift_typ", "schubspannung", "bindungsgrad", "aufladung", "richtung",
            "kohaerenz", "abspaltung", "feldsprung", "ueberlagerung", "impulsrate", "sprachfrequenz"
        ]
    }

    response = requests.post(
        "https://dev.syntx-system.com/resonanz/formats/quick",
        headers={"Content-Type": "application/json"},
        data=json.dumps(format_data)
    )
    
    if response.status_code == 200:
        print("Format erfolgreich erstellt!")
        return response.json()
    else:
        print(f"Fehler beim Erstellen des Formats: {response.text}")
        return None

# Abrufen des erstellten Formats
def get_format(format_name):
    response = requests.get(
        f"https://dev.syntx-system.com/resonanz/formats/{format_name}",
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen des Formats: {response.text}")
        return None

# Beispielaufruf für das Erstellen und Abrufen des Formats
format_response = create_format()
if format_response:
    print("Erstelltes Format:", format_response)
    format_details = get_format(format_response['name'])
    print("Abgerufenes Format:", format_details)
```

#### **3.2 Wrapper erstellen und abrufen**

```python
# 2. Wrapper erstellen (Mit Format und Scoring-Logik)
def create_wrapper():
    wrapper_data = {
        "name": "syntex_wrapper_ultra130",
        "description": "Wrapper für das Format SYNTX_ULTRA130 zur Analyse und Scoring der 130 Felder",
        "content": """
SYNTX ULTRA130 Wrapper

Dieser Wrapper analysiert das Format "SYNTX_ULTRA130" und berechnet die Scores basierend auf den Feldern, die automatisch aus dem Format extrahiert werden.

⚡ **Scoring Logik**:
- driftkorper: 0.2
- kalibrierung: 0.2
- stromung: 0.15
- tiefe: 0.15
- wirkung: 0.3

Die endgültige Punktzahl wird berechnet als:
sum(fields) / total_fields
"""
    }

    response = requests.post(
        "https://dev.syntx-system.com/resonanz/wrapper",
        headers={"Content-Type": "application/json"},
        data=json.dumps(wrapper_data)
    )
    
    if response.status_code == 200:
        print("Wrapper erfolgreich erstellt!")
        return response.json()
    else:
        print(f"Fehler beim Erstellen des Wrappers: {response.text}")
        return None

# Abrufen des erstellten Wrappers
def get_wrapper(wrapper_name):
    response = requests.get(
        f"https://dev.syntx-system.com/resonanz/wrappers/{wrapper_name}",
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen des Wrappers: {response.text}")
        return None

# Beispielaufruf für das Erstellen und Abrufen des Wrappers
wrapper_response = create_wrapper()
if wrapper_response:
    print("Erstellter Wrapper:", wrapper_response)
    wrapper_details = get_wrapper(wrapper_response['name'])
    print("Abgerufener Wrapper:", wrapper_details)
```

#### **3.3 Profil erstellen und abrufen**

```python
# 3. Profil erstellen (Mit GPT-Scoring)
def create_profile():
    profile_data = {
        "profile": {
            "name": "SYNTX_ULTRA130_PROFIL",
            "description": "Profil für die Analyse der 130 semantischen Felder",
            "wrapper": "syntex_wrapper_ultra130",
            "format": "syntx_ultra130_format",
            "gpt_scoring": {
                "model": "gpt-4", 
                "temperature": 0.7, 
                "max_tokens": 150,
                "prompt_template": "drift_analysis_v1"
            },
            "validation": {
                "min_score": 50,
                "max_score": 100
            }
        }
    }

    response = requests.post(
        "https://dev.syntx-system.com/resonanz/profiles/quick",
        headers={"Content-Type": "application/json"},
        data=json.dumps(profile_data)
    )
    
    if response.status_code == 200:
        print("Profil erfolgreich erstellt!")
        return response.json()
    else:
        print(f"Fehler beim Erstellen des Profils: {response.text}")
        return None

# Abrufen des erstellten Profils
def get_profile(profile_name):
    response = requests.get(
        f"https://dev.syntx-system.com/resonanz/profiles/{profile_name}",
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim Abrufen des Profils: {response.text}")
        return None

# Beispielaufruf für das Erstellen und Abrufen des Profils
profile_response = create_profile()
if profile_response:
    print("Erstelltes Profil:", profile_response)
    profile_details = get_profile(profile_response['profile']['name'])
    print("Abgerufenes Profil:", profile_details)
```

---

### **4. Die API-Integration zusammengefasst**

1. **Format erstellen**: Definiert, welche Felder für die **semantische Drift** verwendet werden sollen. Dies wird über den Endpoint `/resonanz/formats/quick` gemacht.

2. **Wrapper erstellen**: Der **Wrapper** verbindet das **Format** mit einer **Scoring-Logik** und verarbeitet die Felder zur Drift-Analyse. Der Wrapper wird über den Endpoint `/resonanz/wrapper` erstellt.

3. **Profil erstellen**: Das **Profil** wird mit dem **Format** und dem **Wrapper** verbunden. Es enthält auch die **Scoring-Methode** (z.B. **GPT**). Das Profil wird über den Endpoint `/resonanz/profiles/quick` erstellt.

---

### **5. Fazit**

Mit diesem Setup hast du die vollständige **Verbindung zwischen Format, Wrapper und Profil**. Das bedeutet, dass du:

* **Felder** dynamisch aus der Antwort extrahieren kannst.
* **Wrapper** die Analyse der Felder mit **GPT** und der richtigen **Scoring-Logik** durchführen.
* **Profile** für spezifische **Scoring-Arten** (wie **GPT**-Scoring) erstellen und dynamisch anpassen kannst.



