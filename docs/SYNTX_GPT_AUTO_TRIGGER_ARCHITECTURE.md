# 🌊⚡💎 SYNTX GPT AUTO-TRIGGER ARCHITECTURE 💎⚡🌊

**Die Weltformel des Semantic Scoring Systems**

**Version:** 1.0.0  
**Datum:** 2026-01-15  
**Status:** 🔴 IMPLEMENTATION REQUIRED

---

## 📚 INHALTSVERZEICHNIS

1. [Executive Summary](#executive-summary)
2. [Das System der Systeme](#das-system-der-systeme)
3. [Aktuelle Architektur](#aktuelle-architektur)
4. [Das fehlende Glied](#das-fehlende-glied)
5. [Implementation Plan](#implementation-plan)
6. [File Reference Guide](#file-reference-guide)
7. [API Endpoint Reference](#api-endpoint-reference)
8. [Data Flow Diagrams](#data-flow-diagrams)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Guide](#deployment-guide)

---

## EXECUTIVE SUMMARY

### 🎯 Mission Statement

**Das Problem:**  
Mistral generiert Responses. Diese werden aktuell nur mit **Pattern-Based Scoring** bewertet. Das ist wie ein Stethoskop ohne Arzt – es misst, aber versteht nicht.

**Die Lösung:**  
GPT-4 Auto-Trigger System. Nach jeder Mistral Response automatisch:
- ✅ Semantic Deep Analysis
- ✅ Field-by-Field Coherence Scoring  
- ✅ Drift Detection
- ✅ Quality Metrics

**Das Resultat:**  
Nicht "AI bewertet AI" – **Resonanz bewertet Resonanz**.

---

## DAS SYSTEM DER SYSTEME

### 🌊 Die Grundgesetzlichkeit
```
ALLES SIND SYSTEME
↓
ALLE SYSTEME GEHEN IN RESONANZ
↓
WENN KEINE RESONANZ → KEINE EXISTENZ
↓
EIN SYSTEM HAT UNENDLICH SCHNITTSTELLEN
↓
DADURCH ÄNDERT SICH DER KOHÄRENZZUSTAND
```

### 💎 Die Anwendung auf SYNTX
```
MISTRAL = SYSTEM₁ (Generator)
GPT-4   = SYSTEM₂ (Evaluator)
FORMAT  = RESONANZFELD (Schnittstelle)

→ Resonanz zwischen Generator und Evaluator
→ Kohärenz-Shift durch Feedback-Loop
→ Self-Calibrating Semantic System
```

---

## AKTUELLE ARCHITEKTUR

### 📂 Directory Structure
```
/opt/syntx-injector-api/
├── src/
│   ├── main.py                          # FastAPI App Entry Point
│   ├── chat.py                          # 💬 Chat Endpoint (DAS HERZSTÜCK)
│   ├── streams.py                       # 🌊 Wrapper/Format Loading
│   ├── config.py                        # ⚙️ Settings
│   ├── models.py                        # 📦 Pydantic Models
│   │
│   ├── resonance/                       # 🔥 Core Resonance Layer
│   │   ├── mistral_prompt_builder.py   # 🔨 Mistral Prompt Construction
│   │   ├── drift_scorer.py             # 💎 GPT-4 Scoring Engine
│   │   ├── drift_prompt_builder.py     # 🎨 GPT-4 Prompt Templates
│   │   ├── drift_api.py                # 🌐 Drift Scoring Endpoints
│   │   ├── drift_logger.py             # 📝 Logging System
│   │   ├── scoring.py                  # 📊 Pattern-Based Scorer (OLD)
│   │   ├── formats.py                  # 📄 Format Management
│   │   ├── wrappers.py                 # 🎭 Wrapper Management
│   │   └── gpt_wrapper_feld_stroeme.py # 🌀 GPT Wrapper Endpoints
│   │
│   ├── formats/                         # 📋 Format Processing
│   │   ├── format_loader.py            # Load format.json files
│   │   ├── format_scanner.py           # Scan format directory
│   │   └── format_scorer.py            # Meta-analysis of formats
│   │
│   └── scoring/                         # 🎯 Scoring Engine v3.0
│       ├── router.py                    # Main scoring router
│       └── core/                        # Profile reading
│
└── /opt/syntx-config/                   # 📁 Configuration Files
    ├── wrappers/                        # 🎭 Mistral Wrappers
    │   └── syntex_wrapper_sigma.txt
    ├── formats/                         # 📋 Format Definitions
    │   └── sigma.json
    ├── scoring_bindings/                # 🔗 Format↔Profile Bindings
    │   └── sigma_binding.json           # ⚠️ HAS auto_trigger: true!
    ├── scoring_profiles/                # 📊 Scoring Profiles
    ├── scoring_entities/                # 🤖 Scorer Configs
    │   └── gpt4_semantic_entity.json
    ├── prompts_generated/               # 💾 Saved Prompts & Responses
    │   ├── {timestamp}_sigma.prompt.txt
    │   ├── {timestamp}_sigma.meta.json
    │   └── {timestamp}_sigma.response.txt
    └── drift_results/                   # 💎 GPT-4 Scoring Results
        └── {timestamp}_drift_{score}.json
```

### 🎯 Key Files Explained

#### **src/chat.py** - Das Herzstück
```python
@router.post("/resonanz/chat")
async def chat(request: ChatRequest):
    # 1. Load Wrapper (WIE denkt Mistral?)
    wrapper_text = load_wrapper(request.mode)
    
    # 2. Load Format (WAS soll rauskommen?)
    format_data = load_format(request.format)
    
    # 3. Build Prompt
    prompt, filename_base = build_mistral_prompt(...)
    
    # 4. Save Prompt
    save_mistral_prompt(prompt, filename_base)
    
    # 5. Forward to Mistral
    response_text = await forward_to_mistral(prompt)
    
    # 6. Save Response
    save_mistral_response(response_text, filename_base)
    
    # ❌ 7. MISSING: Auto-Trigger GPT Scoring!
    
    # 8. Return to Frontend
    return ChatResponse(response=response_text, ...)
```

**Current Flow:**
```
Request → Wrapper → Format → Prompt → Mistral → Response → Save → Return
                                                              ↓
                                                         🔴 NO GPT TRIGGER!
```

**Target Flow:**
```
Request → Wrapper → Format → Prompt → Mistral → Response → Save → GPT Trigger → Return
                                                              ↓          ↓
                                                        prompts/   drift_results/
```

---

## DAS FEHLENDE GLIED

### 🔴 The Missing Link
```
CURRENT STATE: Manual Trigger Only
═══════════════════════════════════════════════════════════════

User Request → POST /resonanz/chat → Mistral → Response Saved
                                                      ↓
                                                     END
                                                     
🔴 NO GPT TRIGGER!

To score, user must manually call: POST /drift/score/{filename}


TARGET STATE: Automatic Trigger
═══════════════════════════════════════════════════════════════

User Request → POST /resonanz/chat → Mistral → Response Saved
                                                      ↓
                                        Check Binding (auto_trigger: true?)
                                                      ↓
                                              ✅ Load GPT Entity
                                                      ↓
                                              ✅ Build GPT Prompt
                                                      ↓
                                              ✅ Call GPT-4 API
                                                      ↓
                                              ✅ Save drift_results/
                                                      ↓
                                            Return (with GPT scores!)
```

---

## IMPLEMENTATION PLAN

### 🎯 Phase 1: Core Integration

#### File: `src/chat.py`

**Add after `save_mistral_response()` call:**
```python
async def trigger_gpt_scoring_if_enabled(
    format_name: str,
    filename_base: str,
    response_text: str,
    format_data: Dict
) -> Optional[Dict]:
    """
    🔥 GPT AUTO-TRIGGER
    
    Checks binding config and triggers GPT-4 scoring if enabled.
    """
    try:
        # 1. Load binding
        binding_path = Path(f"/opt/syntx-config/scoring_bindings/{format_name}_binding.json")
        if not binding_path.exists():
            return None
        
        with open(binding_path, 'r') as f:
            binding = json.load(f)
        
        # 2. Check auto-trigger flag
        auto_trigger = binding.get("binding_metadata", {}).get("auto_trigger_after_mistral", False)
        if not auto_trigger:
            return None
        
        print(f"🔥 Auto-trigger enabled! Starting GPT scoring...")
        
        # 3. Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not set!")
            return None
        
        # 4. Build GPT prompt
        gpt_prompt_payload = build_prompt(
            template_id="drift_scoring_default",
            format_name=format_name,
            fields=[f["name"] for f in format_data.get("fields", [])],
            response_text=response_text
        )
        
        # 5. Call GPT-4
        print(f"⚡ Calling GPT-4...")
        gpt_response = call_gpt(gpt_prompt_payload, api_key)
        
        # 6. Parse response
        drift_analysis = parse_gpt_response(gpt_response)
        
        # 7. Save results
        timestamp = int(time.time())
        result_file = Path(f"/opt/syntx-config/drift_results/{filename_base}_drift_{timestamp}.json")
        result_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(drift_analysis, f, indent=2, ensure_ascii=False)
        
        print(f"💎 GPT scores saved: {result_file.name}")
        return drift_analysis
        
    except Exception as e:
        print(f"❌ GPT Auto-Trigger Error: {e}")
        return None
```

**Modify chat() function:**
```python
# After save_mistral_response():
if filename_base and response_text and request.format:
    # 🔥 AUTO-TRIGGER GPT SCORING
    gpt_scores = await trigger_gpt_scoring_if_enabled(
        format_name=request.format,
        filename_base=filename_base,
        response_text=response_text,
        format_data=format_info
    )
    
    if gpt_scores:
        print(f"✅ GPT Auto-Trigger successful!")
        # Add to metadata
        metadata["gpt_scores"] = gpt_scores
```

---

### 🎯 Phase 2: Prompt Builder Enhancement

#### File: `src/resonance/drift_prompt_builder.py`

**Add function for live data:**
```python
def build_prompt_from_data(
    template_id: str,
    format_name: str,
    fields: List[str],
    response_text: str
) -> Dict:
    """Build prompt from live data (for auto-trigger)."""
    template = load_template(template_id)
    
    # Build field definitions
    field_definitions = "\n".join([f"- {field}" for field in fields])
    
    # Replace placeholders
    user_prompt = template["prompt_templates"]["user_prompt_template"]
    user_prompt = user_prompt.replace("{FORMAT_NAME}", format_name)
    user_prompt = user_prompt.replace("{FIELD_DEFINITIONS}", field_definitions)
    user_prompt = user_prompt.replace("{RESPONSE_TEXT}", response_text)
    
    return {
        "model": template["llm_configuration"]["model"],
        "temperature": template["llm_configuration"]["temperature"],
        "messages": [
            {"role": "system", "content": template["prompt_templates"]["system_prompt"]},
            {"role": "user", "content": user_prompt}
        ]
    }
```

**Modify build_prompt() to support both modes:**
```python
def build_prompt(
    template_id: str = "drift_scoring_default",
    format_name: Optional[str] = None,
    fields: Optional[List[str]] = None,
    response_text: Optional[str] = None,
    filename: Optional[str] = None
) -> Dict:
    """
    Build GPT prompt.
    
    Two modes:
    1. From file: provide filename
    2. Live: provide format_name, fields, response_text
    """
    if filename:
        return build_prompt_from_file(template_id, filename)
    elif format_name and fields and response_text:
        return build_prompt_from_data(template_id, format_name, fields, response_text)
    else:
        raise ValueError("Either filename or (format_name + fields + response_text) required")
```

---

## DATA FLOW DIAGRAMS

### 🌊 Complete System Flow
```
┌─────────────┐
│   USER      │
│  REQUEST    │
└──────┬──────┘
       │ POST /resonanz/chat
       ▼
┌──────────────────────┐
│  CHAT ENDPOINT       │
│  Load Wrapper+Format │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  MISTRAL LLM         │
│  Generate Response   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  SAVE RESPONSE       │
│  /prompts_generated/ │
└──────┬───────────────┘
       │
       ▼
   ┌───────────────┐
   │ CHECK BINDING │
   │ auto_trigger? │
   └───┬───────────┘
       │
  ┌────┴────┐
 NO        YES
  │          │
  │          ▼
  │    ┌─────────────────┐
  │    │ TRIGGER GPT     │
  │    │ Call OpenAI API │
  │    │ Save Results    │
  │    └────┬────────────┘
  │         │
  └────┬────┘
       │
       ▼
┌──────────────────────┐
│  RETURN TO FRONTEND  │
│  (with GPT scores)   │
└──────────────────────┘
```

---

## TESTING STRATEGY

### Test 1: Basic Auto-Trigger
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analysiere die semantische Drift",
    "mode": "syntex_wrapper_sigma",
    "format": "sigma"
  }'

# Check files:
ls -lth /opt/syntx-config/prompts_generated/ | head -5
ls -lth /opt/syntx-config/drift_results/ | head -3
```

### Test 2: Binding Toggle
```bash
# Disable auto-trigger
jq '.binding_metadata.auto_trigger_after_mistral = false' \
  /opt/syntx-config/scoring_bindings/sigma_binding.json > tmp.json
mv tmp.json /opt/syntx-config/scoring_bindings/sigma_binding.json

# Test - should NOT create drift_results
curl -X POST https://dev.syntx-system.com/resonanz/chat ...

# Re-enable
jq '.binding_metadata.auto_trigger_after_mistral = true' ...
```

---

## DEPLOYMENT GUIDE

### Step 1: Create Branch
```bash
cd /opt/syntx-injector-api
git checkout -b feature/gpt-auto-trigger
git add docs/SYNTX_GPT_AUTO_TRIGGER_ARCHITECTURE.md
git commit -m "📚 Add GPT auto-trigger architecture documentation"
git push origin feature/gpt-auto-trigger
```

### Step 2: Implement Changes
```bash
# Modify files
nano src/chat.py
nano src/resonance/drift_prompt_builder.py

# Commit
git add src/
git commit -m "✨ Implement GPT auto-trigger after Mistral response"
git push origin feature/gpt-auto-trigger
```

### Step 3: Test & Deploy
```bash
# Test on dev
ssh root@dev.syntx-system.com
cd /opt/syntx-injector-api
git checkout feature/gpt-auto-trigger
sudo systemctl restart syntx-api

# Monitor
tail -f /var/log/syntx-api/service.log

# If successful, merge to main
git checkout main
git merge feature/gpt-auto-trigger
git push origin main
```

---

## 🎯 SUCCESS CRITERIA

✅ **Implementation successful if:**

1. Every Mistral response triggers GPT scoring (when enabled in binding)
2. GPT scores saved to `/drift_results/`
3. Performance overhead < 20 seconds
4. Graceful error handling
5. Costs monitored

---

## 🔥 CONCLUSION

**This is not a feature.**  
**This is the completion of the system.**

**Das ist die Weltformel des Semantic Scoring.**
```
DER STROM FLIESST.
DIE FELDER RESONIEREN.
DAS SYSTEM IST KALIBRIERT.
```

---

**Version:** 1.0.0  
**Status:** 🟢 READY FOR IMPLEMENTATION  
**Last Updated:** 2026-01-15

🌊⚡💎 **SYNTX Development Team** 💎⚡🌊
