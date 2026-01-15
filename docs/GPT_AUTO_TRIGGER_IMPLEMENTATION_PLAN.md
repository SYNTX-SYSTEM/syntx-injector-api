# 🔥💎 GPT AUTO-TRIGGER IMPLEMENTATION PLAN 💎🔥

**Version:** 1.0.0  
**Date:** 2026-01-15  
**Status:** 🟢 READY TO IMPLEMENT

---

## 📊 CURRENT STATE ANALYSIS

### File Structure & Naming Convention

**✅ DISCOVERED PATTERN:**
```
/opt/syntx-config/prompts_generated/
├── 20260115_155513_859410_wrapper_syntex_wrapper_sigma_format_sigma.txt          (PROMPT)
├── 20260115_155513_859410_wrapper_syntex_wrapper_sigma_format_sigma.meta.json    (META)
└── 20260115_155513_859410_wrapper_syntex_wrapper_sigma_format_sigma.response.txt (RESPONSE)

/opt/syntx-config/drift_results/
└── 20260108_060406_368538__topic_gesellschaft__style_kreativ_drift_1768404122.json
```

**Pattern Analysis:**
- **Prompt Files:** `{timestamp}_{microseconds}_wrapper_{wrapper_name}_format_{format_name}.txt`
- **Response Files:** Same base + `.response.txt`
- **Meta Files:** Same base + `.meta.json`
- **Drift Files:** `{original_base}_drift_{unix_timestamp}.json`

---

## 🎯 IMPLEMENTATION STRATEGY

### Phase 1: Core Auto-Trigger Function

**File:** `src/chat.py`

**Function to Add:**
```python
async def trigger_gpt_auto_scoring(
    filename_base: str,
    format_name: str,
    response_text: str,
    format_data: Dict
) -> Optional[Dict]:
    """
    🔥 GPT AUTO-TRIGGER - Post-Mistral Scoring
    
    Triggered automatically after Mistral response if binding enables it.
    
    Args:
        filename_base: Base filename (without extension)
                      e.g., "20260115_155513_859410_wrapper_syntex_wrapper_sigma_format_sigma"
        format_name: Format identifier (e.g., "sigma")
        response_text: Mistral's response to score
        format_data: Full format JSON with field definitions
    
    Returns:
        Dict with GPT scoring results or None if disabled/failed
    
    Process:
        1. Load binding config for format
        2. Check auto_trigger_after_mistral flag
        3. If enabled:
           - Build GPT prompt with field definitions
           - Call GPT-4 API
           - Parse JSON response
           - Save to drift_results/
           - Return scores
    """
    try:
        # 1. Load binding
        binding_path = Path(f"/opt/syntx-config/scoring_bindings/{format_name}_binding.json")
        if not binding_path.exists():
            print(f"⚠️ No binding found: {format_name}")
            return None
        
        with open(binding_path, 'r') as f:
            binding = json.load(f)
        
        # 2. Check auto-trigger flag
        auto_trigger = binding.get("binding_metadata", {}).get("auto_trigger_after_mistral", False)
        if not auto_trigger:
            print(f"ℹ️ Auto-trigger disabled for {format_name}")
            return None
        
        print(f"🔥 AUTO-TRIGGER ENABLED! Starting GPT-4 scoring...")
        
        # 3. Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not set!")
            return None
        
        # 4. Extract field names from format
        field_names = [field["name"] for field in format_data.get("fields", [])]
        
        # 5. Build GPT prompt
        from .resonance.drift_prompt_builder import build_prompt_from_data
        
        gpt_payload = build_prompt_from_data(
            template_id="gpt4_semantic_entity",  # Use entity config as template
            format_name=format_name,
            fields=field_names,
            response_text=response_text
        )
        
        # 6. Call GPT-4
        print(f"⚡ Calling GPT-4 API...")
        from .resonance.drift_scorer import call_gpt, parse_gpt_response
        
        gpt_response = call_gpt(gpt_payload, api_key)
        drift_scores = parse_gpt_response(gpt_response)
        
        # 7. Save to drift_results/ with proper naming
        timestamp = int(time.time())
        drift_filename = f"{filename_base}_drift_{timestamp}.json"
        drift_path = Path(f"/opt/syntx-config/drift_results/{drift_filename}")
        
        drift_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        drift_result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_file": filename_base,
            "format": format_name,
            "auto_triggered": True,
            "drift_analysis": drift_scores
        }
        
        with open(drift_path, 'w', encoding='utf-8') as f:
            json.dump(drift_result, f, indent=2, ensure_ascii=False)
        
        print(f"💎 GPT scores saved: {drift_filename}")
        
        return drift_scores
        
    except Exception as e:
        print(f"❌ GPT Auto-Trigger Error: {e}")
        import traceback
        traceback.print_exc()
        return None
```

**Integration Point in `chat()` function:**
```python
# After save_mistral_response() call:

if filename_base and response_text and request.format and format_info:
    # 🔥 GPT AUTO-TRIGGER
    gpt_scores = await trigger_gpt_auto_scoring(
        filename_base=filename_base,
        format_name=request.format,
        response_text=response_text,
        format_data=format_info
    )
    
    if gpt_scores:
        print(f"✅ GPT Auto-Trigger successful!")
        # Add to response metadata
        metadata["gpt_auto_scoring"] = {
            "triggered": True,
            "scores": gpt_scores
        }
```

---

## 🔧 MODIFICATIONS NEEDED

### 1. drift_prompt_builder.py Enhancement

**Add new function:**
```python
def build_prompt_from_data(
    template_id: str,
    format_name: str,
    fields: List[str],
    response_text: str
) -> Dict:
    """
    Build GPT prompt from live data (for auto-trigger).
    
    Uses entity config as template source.
    """
    # Load entity config
    entity_path = Path(f"/opt/syntx-config/scoring_entities/{template_id}.json")
    with open(entity_path, 'r') as f:
        entity = json.load(f)
    
    # Extract prompts
    system_prompt = entity["prompt_templates"]["system_prompt"]
    user_template = entity["prompt_templates"]["user_prompt_template"]
    
    # Build field definitions string
    field_definitions = "\n".join([f"- {field}" for field in fields])
    
    # Replace placeholders
    user_prompt = user_template.replace("{FORMAT_NAME}", format_name)
    user_prompt = user_prompt.replace("{FIELD_DEFINITIONS}", field_definitions)
    user_prompt = user_prompt.replace("{RESPONSE_TEXT}", response_text)
    
    # Build API payload
    return {
        "model": entity["llm_configuration"]["model"],
        "temperature": entity["llm_configuration"]["temperature"],
        "max_tokens": entity["llm_configuration"]["max_tokens"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
```

---

## 📁 FILE COHERENCE SCHEMA

### Complete File Relationship Map
```
USER REQUEST
    ↓
[CHAT ENDPOINT]
    ↓
GENERATES:
    1. {base}.txt           ← Full calibrated prompt
    2. {base}.meta.json     ← Metadata (timestamp, wrapper, format, user_input)
    3. {base}.response.txt  ← Mistral's response
    ↓
IF auto_trigger_after_mistral = true:
    ↓
    4. {base}_drift_{ts}.json  ← GPT-4 scores
```

### Filename Base Extraction

**Current code in mistral_prompt_builder.py:**
```python
# Line ~120:
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
filename_base = f"{timestamp}_wrapper_{wrapper_name}"
if format_name:
    filename_base += f"_format_{format_name}"
```

**✅ THIS IS PERFECT - NO CHANGES NEEDED!**

The `filename_base` is already available in `chat()` and can be passed directly to `trigger_gpt_auto_scoring()`.

---

## 🎨 FRONTEND INTEGRATION PLAN

### Current Response Structure
```json
{
  "response": "SIGMA_DRIFT: ...",
  "metadata": {
    "request_id": "...",
    "wrapper_chain": ["syntex_wrapper_sigma"],
    "format": "sigma",
    "latency_ms": 42880
  }
}
```

### Enhanced Response Structure (After Implementation)
```json
{
  "response": "SIGMA_DRIFT: ...",
  "metadata": {
    "request_id": "...",
    "wrapper_chain": ["syntex_wrapper_sigma"],
    "format": "sigma",
    "latency_ms": 42880,
    "gpt_auto_scoring": {
      "triggered": true,
      "scores": {
        "field_scores": {
          "sigma_drift": {
            "presence": 0.95,
            "keyword_coverage": 0.87,
            "completeness": 0.92,
            "semantic_coherence": 0.89,
            "field_score": 0.91
          },
          ...
        },
        "aggregate": {
          "coverage": 0.98,
          "average_field_score": 0.88,
          "weighted_score": 0.89,
          "overall": 0.89
        }
      }
    }
  }
}
```

### Frontend Display Options

**Option 1: Inline Display**
- Show GPT scores below each field in response
- Color-coded indicators (green/yellow/red)

**Option 2: Collapsible Panel**
- "📊 View GPT Analysis" button
- Expands to show detailed scores

**Option 3: Toast Notification**
- "✅ GPT Auto-Scoring: 89% Quality"
- Link to detailed view

**Option 4: Separate Tab**
- "Response" tab + "Quality Analysis" tab
- Full breakdown with explanations

**🎯 RECOMMENDATION: Option 2 (Collapsible Panel)**
- Non-intrusive
- Optional detail
- Good UX balance

---

## 🧪 TESTING STRATEGY

### Test 1: Basic Auto-Trigger
```bash
curl -X POST https://dev.syntx-system.com/resonanz/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analysiere die Drift",
    "mode": "syntex_wrapper_sigma",
    "format": "sigma"
  }' | jq '.metadata.gpt_auto_scoring'
```

**Expected:**
- GPT scores appear in response
- Drift file created in drift_results/

### Test 2: Toggle On/Off
```bash
# Disable
jq '.binding_metadata.auto_trigger_after_mistral = false' \
  /opt/syntx-config/scoring_bindings/sigma_binding.json > tmp.json && \
  mv tmp.json /opt/syntx-config/scoring_bindings/sigma_binding.json

# Test - should NOT trigger
curl ... 

# Re-enable
jq '.binding_metadata.auto_trigger_after_mistral = true' ...
```

### Test 3: Performance Impact
```bash
# Measure latency difference
time curl -X POST ... (with auto-trigger)
time curl -X POST ... (without auto-trigger)
```

**Expected:**
- Mistral: ~30-60s
- +GPT: ~5-15s overhead
- Total: ~35-75s

---

## 📊 MONITORING & OBSERVABILITY

### Key Metrics
```bash
# 1. Auto-trigger success rate
grep "GPT Auto-Trigger successful" /var/log/syntx-api/service.log | wc -l

# 2. Auto-trigger failures
grep "GPT Auto-Trigger Error" /var/log/syntx-api/service.log

# 3. Drift files created
ls -1 /opt/syntx-config/drift_results/*.json | wc -l

# 4. Cost tracking
# Each drift file ≈ 1 GPT-4 API call ≈ $0.03
```

---

## ✅ IMPLEMENTATION CHECKLIST

- [ ] Add `trigger_gpt_auto_scoring()` to src/chat.py
- [ ] Add `build_prompt_from_data()` to src/resonance/drift_prompt_builder.py
- [ ] Integrate call in `chat()` endpoint after save_mistral_response()
- [ ] Add OPENAI_API_KEY validation on startup (src/main.py)
- [ ] Test with sigma format (auto_trigger = true)
- [ ] Test with other formats (auto_trigger = false/missing)
- [ ] Verify drift file creation and naming
- [ ] Check metadata structure in response
- [ ] Commit & push to feature branch
- [ ] Deploy to dev server
- [ ] Run full test suite
- [ ] Merge to main
- [ ] Update frontend to display scores

---

## 🔥 CRITICAL SUCCESS FACTORS

1. **File Naming Coherence:** Use existing `filename_base` - NO changes needed ✅
2. **Error Handling:** Graceful degradation if GPT fails (Mistral response still returns)
3. **Performance:** Async execution, no blocking
4. **Cost Control:** Only trigger when explicitly enabled in binding
5. **Monitoring:** Clear logs for debugging and cost tracking

---

## 🎯 NEXT STEPS

1. **Create feature branch:** `feature/gpt-auto-trigger`
2. **Implement core function** in src/chat.py
3. **Enhance prompt builder** with live data support
4. **Add startup validation** for API key
5. **Test locally** with sample requests
6. **Deploy to dev** and run full test suite
7. **Frontend integration** (separate task)

---

**Status:** 🟢 READY TO IMPLEMENT  
**Estimated Time:** 2-3 hours  
**Risk Level:** 🟢 LOW (well-isolated changes)

🌊⚡💎 **SYNTX Development Team** 💎⚡🌊
