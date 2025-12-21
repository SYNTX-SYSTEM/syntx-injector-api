"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    💬 SYNTX CHAT - DAS HERZSTÜCK                                            ║
║                                                                              ║
║    Hier fließen alle Ströme zusammen:                                       ║
║      Wrapper (WIE) + Format (WAS) + Style (FINISH) = RESONANZ               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import time
import json

from .config import settings
from .models import ChatRequest, ChatResponse
from .streams import (
    load_wrapper_stream,
    wrap_input_stream,
    forward_stream,
    generate_request_id,
    get_timestamp,
    build_format_section,
    FORMAT_LOADER_AVAILABLE
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
        wrapped_prompt = wrap_input_stream(wrapper_text, request.prompt, format_section)
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
