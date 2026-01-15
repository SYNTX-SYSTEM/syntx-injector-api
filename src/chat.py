"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    💬 SYNTX CHAT - DAS HERZSTÜCK                                            ║
║                                                                              ║
║    Hier fließen alle Ströme zusammen:                                       ║
║      Wrapper (WIE) + Format (WAS) + Style (FINISH) = RESONANZ               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
import os
from datetime import datetime
from pathlib import Path
import time
import json
from typing import Dict, Optional, List

from .config import settings
from .models import ChatRequest, ChatResponse
from .streams import (
    load_wrapper_stream,
    wrap_input_stream,
    forward_stream,
    generate_request_id,
    get_timestamp,
    build_format_section,
    FORMAT_LOADER_AVAILABLE,
    save_mistral_response
)

router = APIRouter(tags=["chat"])

# Style Alchemist
try:
    from .styles import apply_style_magic
    STYLE_AVAILABLE = True
except ImportError:
    STYLE_AVAILABLE = False


def log_stage(stage: str, data: dict):
    """📝 Stage Logging"""
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = settings.log_dir / "field_flow.jsonl"
    with open(log_file, 'a', encoding='utf-8') as f:
        log_entry = {"stage": stage, "timestamp": get_timestamp(), **data}
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


@router.post("/api/chat", response_model=ChatResponse)


# ═══════════════════════════════════════════════════════════════════════════════
#  🔥💎 GPT AUTO-TRIGGER SYSTEM 💎🔥
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_gpt_auto_scoring(
    filename_base: str,
    format_name: str,
    response_text: str,
    format_data: Dict
) -> Optional[Dict]:
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║              🔥 GPT AUTO-TRIGGER - POST-MISTRAL SCORING 🔥               ║
    ║                                                                           ║
    ║                    DER STROM BEWERTET DEN STROM                          ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    ZWECK:
        Automatisches GPT-4 Scoring nach Mistral Response
        Wenn Binding es aktiviert hat: auto_trigger_after_mistral = true
        
    PARAMETER:
        filename_base: Base Filename ohne Extension
                      (z.B. "20260115_155513_859410_wrapper_syntex_wrapper_sigma_format_sigma")
        format_name: Format Identifier (z.B. "sigma")
        response_text: Mistral's generierter Response
        format_data: Vollständiges Format JSON mit Field Definitions
        
    RÜCKGABE:
        Dict mit GPT Scoring Results oder None (wenn disabled/failed)
        
    PROZESS:
        1. Load Binding Config für Format
        2. Check auto_trigger_after_mistral Flag
        3. Wenn enabled:
           - Build GPT Prompt mit Field Definitions
           - Call GPT-4 API
           - Parse JSON Response
           - Save to drift_results/
           - Return Scores
           
    FELD-KOHÄRENZ:
        Filename Base wird unverändert verwendet
        Drift File: {filename_base}_drift_{unix_timestamp}.json
        
    FEHLER-BEHANDLUNG:
        Graceful Degradation - Mistral Response kehrt trotzdem zurück
        Alle Errors werden geloggt aber nicht geworfen
        
    RESONANZ-FLUSS:
        Binding Check → GPT Prompt Build → API Call → Parse → Save → Return
    """
    try:
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 1: BINDING CONFIGURATION LOADING
        # ─────────────────────────────────────────────────────────────────────
        
        binding_path = Path(f"/opt/syntx-config/scoring_bindings/{format_name}_binding.json")
        
        if not binding_path.exists():
            print(f"⚠️  Auto-Trigger: Kein Binding für Format '{format_name}'")
            return None
        
        with open(binding_path, 'r', encoding='utf-8') as f:
            binding = json.load(f)
        
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 2: AUTO-TRIGGER FLAG CHECK
        # ─────────────────────────────────────────────────────────────────────
        
        auto_trigger = binding.get("binding_metadata", {}).get("auto_trigger_after_mistral", False)
        
        if not auto_trigger:
            print(f"ℹ️  Auto-Trigger deaktiviert für Format '{format_name}'")
            return None
        
        print(f"🔥 AUTO-TRIGGER ENABLED! Starting GPT-4 Field Scoring...")
        
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 3: API KEY VALIDATION
        # ─────────────────────────────────────────────────────────────────────
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY nicht gesetzt! GPT Auto-Trigger abgebrochen.")
            return None
        
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 4: FIELD EXTRACTION & FORMAT LOADING
        # ─────────────────────────────────────────────────────────────────────
        
        # Load format JSON directly (format_data might be a string from build_format_section)
        format_json_path = Path(f"/opt/syntx-config/formats/{format_name}.json")
        
        if not format_json_path.exists():
            print(f"⚠️  Format JSON nicht gefunden: {format_name}")
            return None
        
        with open(format_json_path, 'r', encoding='utf-8') as f:
            format_json = json.load(f)
        
        field_names = [field["name"] for field in format_json.get("fields", [])]
        
        if not field_names:
            print(f"⚠️  Keine Fields in Format '{format_name}' gefunden")
            return None
        
        print(f"📊 Scoring {len(field_names)} Fields: {', '.join(field_names)}")
        
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 5: GPT PROMPT BUILD
        # ─────────────────────────────────────────────────────────────────────
        
        from .resonance.drift_prompt_builder import build_prompt_from_data
        
        gpt_payload = build_prompt_from_data(
            template_id="gpt4_semantic_entity",
            format_name=format_name,
            fields=field_names,
            response_text=response_text
        )
        
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 6: GPT-4 API CALL
        # ─────────────────────────────────────────────────────────────────────
        
        print(f"⚡ Calling GPT-4 API for semantic field analysis...")
        
        from .resonance.drift_scorer import call_gpt, parse_gpt_response
        
        gpt_response = call_gpt(gpt_payload, api_key)
        drift_scores = parse_gpt_response(gpt_response)
        
        # ─────────────────────────────────────────────────────────────────────
        #  STAGE 7: RESULT PERSISTENCE
        # ─────────────────────────────────────────────────────────────────────
        
        timestamp = int(time.time())
        drift_filename = f"{filename_base}_drift_{timestamp}.json"
        drift_path = Path(f"/opt/syntx-config/drift_results/{drift_filename}")
        
        drift_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build Complete Drift Result
        drift_result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_file": filename_base,
            "format": format_name,
            "auto_triggered": True,
            "drift_analysis": drift_scores
        }
        
        with open(drift_path, 'w', encoding='utf-8') as f:
            json.dump(drift_result, f, indent=2, ensure_ascii=False)
        
        print(f"💎 GPT Scores gespeichert: {drift_filename}")
        print(f"✅ Auto-Trigger erfolgreich abgeschlossen!")
        
        return drift_scores
        
    except Exception as e:
        print(f"❌ GPT Auto-Trigger Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def chat(request: ChatRequest):
    """
    💬 CHAT - Das Herzstück
    
    mode   = WIE denkt das Modell? (Wrapper)
    format = WAS kommt raus? (Format)
    style  = WIE klingt es? (Post-Processing)
    """
    request_id = generate_request_id()
    start_time = time.time()
    field_flow = []
    format_info = {}
    
    try:
        # STAGE 1: INCOMING
        log_stage("1_INCOMING", {
            "request_id": request_id,
            "prompt": request.prompt,
            "mode": request.mode,
            "format": request.format,
            "style": request.style
        })
        
        # STAGE 2: LOAD WRAPPER
        wrapper_text, wrapper_chain = await load_wrapper_stream(
            request.mode,
            request.include_init,
            request.include_terminology
        )
        log_stage("2_WRAPPERS_LOADED", {
            "request_id": request_id,
            "chain": wrapper_chain
        })
        
        # STAGE 2.5: LOAD FORMAT
        format_section = ""
        if request.format:
            format_section, format_info = build_format_section(
                request.format, 
                request.language
            )
            log_stage("2.5_FORMAT_LOADED", {
                "request_id": request_id,
                "format": request.format,
                "fields": format_info.get("fields", [])
            })
        
        # STAGE 3: CALIBRATE
        wrapped_prompt, filename_base = wrap_input_stream(wrapper_text, request.prompt, format_section, wrapper_name=request.mode, format_name=request.format)
        log_stage("3_FIELD_CALIBRATED", {
            "request_id": request_id,
            "total_length": len(wrapped_prompt)
        })
        
        # STAGE 4: FORWARD
        backend_params = {
            "max_new_tokens": request.max_new_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "do_sample": request.do_sample
        }
        log_stage("4_BACKEND_FORWARD", {
            "request_id": request_id,
            "backend_url": settings.backend_url,
            "model": settings.model_name
        })
        
        response_text = await forward_stream(wrapped_prompt, backend_params)
        
        # 💎 SAVE RESPONSE
        if filename_base and response_text:
            try:
                response_file = save_mistral_response(response_text, filename_base)
                print(f"💎 Response gespeichert: {filename_base}.response.txt")

                # ═══════════════════════════════════════════════════════════
                #  🔥 GPT AUTO-TRIGGER AFTER MISTRAL RESPONSE
                # ═══════════════════════════════════════════════════════════
                
                if request.format and format_info:
                    gpt_scores = await trigger_gpt_auto_scoring(
                        filename_base=filename_base,
                        format_name=request.format,
                        response_text=response_text,
                        format_data=format_info
                    )
                    
                    if gpt_scores:
                        print(f"✅ GPT Auto-Trigger erfolgreich!")
                        # Add to metadata for frontend
                        metadata["gpt_auto_scoring"] = {
                            "triggered": True,
                            "scores": gpt_scores
                        }
            except Exception as e:
                print(f"⚠️ Response Save Error: {e}")
        
        # STAGE 5: RESPONSE
        latency_ms = int((time.time() - start_time) * 1000)
        log_stage("5_RESPONSE", {
            "request_id": request_id,
            "response": response_text,
            "latency_ms": latency_ms,
            "wrapper_chain": wrapper_chain,
            "format": request.format,
            "format_fields": format_info.get("fields", [])
        })
        
        # STAGE 5.5: STYLE ALCHEMY
        final_response = response_text
        style_info = None
        if request.style and STYLE_AVAILABLE:
            final_response, style_info = apply_style_magic(response_text, request.style)
        
        return ChatResponse(
            response=final_response,
            metadata={
                "request_id": request_id,
                "wrapper_chain": wrapper_chain,
                "format": request.format,
                "format_fields": format_info.get("fields", []),
                "style": request.style,
                "latency_ms": latency_ms
            },
            field_flow=field_flow,
            debug_info={"prompt_len": len(wrapped_prompt)} if request.debug else None,
            style_info=style_info
        )
        
    except Exception as e:
        log_stage("ERROR", {"request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resonanz/chat", response_model=ChatResponse)
async def resonance_chat(request: ChatRequest):
    """💬 Alias zu /api/chat"""
    return await chat(request)
