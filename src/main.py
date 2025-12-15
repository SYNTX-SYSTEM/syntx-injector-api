"""
SYNTX Wrapper Service - Main Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import json

from .config import settings
from .models import ChatRequest, ChatResponse
from .streams import (
    load_wrapper_stream,
    wrap_input_stream,
    forward_stream,
    generate_request_id,
    get_timestamp
)

# Import resonance routers
from .resonance.wrappers import router as wrappers_router
from .resonance.streams import router as streams_router
from .resonance.stats import router as stats_router


def log_stage(stage: str, data: dict):
    """Log each stage with full visibility"""
    print("\n" + "🌊" * 40)
    print(f"📍 STAGE: {stage}")
    print("─" * 80)
    for key, value in data.items():
        if isinstance(value, str) and len(value) > 500:
            print(f"{key}: {value[:500]}... ({len(value)} chars total)")
        else:
            print(f"{key}: {value}")
    print("🌊" * 40 + "\n")
    
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = settings.log_dir / "field_flow.jsonl"
    with open(log_file, 'a', encoding='utf-8') as f:
        log_entry = {"stage": stage, "timestamp": get_timestamp(), **data}
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    if stage == "5_RESPONSE":
        wrapper_log = settings.log_dir / "wrapper_requests.jsonl"
        with open(wrapper_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 80)
    print("SYNTX FIELD RESONANCE SERVICE")
    print("=" * 80)
    print(f"Backend: {settings.backend_url}")
    print(f"Wrappers: {settings.wrapper_dir}")
    print(f"Logs: {settings.log_dir}")
    print(f"Resonance Endpoints: /resonanz/*")
    print("=" * 80)
    yield


app = FastAPI(title="SYNTX Field Resonance", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include resonance routers
app.include_router(wrappers_router)
app.include_router(streams_router)
app.include_router(stats_router)


@app.get("/health")
async def health():
    """Health check with last response"""
    log_file = settings.log_dir / "field_flow.jsonl"
    last_response = None
    
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in reversed(lines[-10:]):
                    entry = json.loads(line)
                    if entry.get("stage") == "5_RESPONSE":
                        last_response = {
                            "response": entry.get("response"),
                            "latency_ms": entry.get("latency_ms"),
                            "timestamp": entry.get("timestamp")
                        }
                        break
        except:
            pass
    
    return {
        "status": "healthy",
        "service": "syntx-field-resonance",
        "version": "2.0.0",
        "last_response": last_response
    }


@app.get("/api/chat/health")
async def chat_health():
    """Health check at /api/chat/health for compatibility"""
    return await health()


@app.get("/resonanz/health")
async def resonance_health():
    """Health check at /resonanz/health"""
    return await health()


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    request_id = generate_request_id()
    start_time = time.time()
    field_flow = []
    
    try:
        # STAGE 1: Incoming
        stage_1_data = {
            "request_id": request_id,
            "prompt": request.prompt,
            "mode": request.mode,
            "include_init": request.include_init
        }
        log_stage("1_INCOMING", stage_1_data)
        field_flow.append({
            "stage": "1_INCOMING",
            "timestamp": get_timestamp(),
            "data": stage_1_data
        })
        
        # STAGE 2: Load Wrappers
        wrapper_text, wrapper_chain = await load_wrapper_stream(
            request.mode,
            request.include_init,
            request.include_terminology
        )
        stage_2_data = {
            "request_id": request_id,
            "chain": wrapper_chain,
            "wrapper_text": wrapper_text
        }
        log_stage("2_WRAPPERS_LOADED", stage_2_data)
        field_flow.append({
            "stage": "2_WRAPPERS_LOADED",
            "timestamp": get_timestamp(),
            "data": {"request_id": request_id, "chain": wrapper_chain}
        })
        
        # STAGE 3: Calibrate Field
        wrapped_prompt = wrap_input_stream(wrapper_text, request.prompt)
        stage_3_data = {
            "request_id": request_id,
            "calibrated_field": wrapped_prompt
        }
        log_stage("3_FIELD_CALIBRATED", stage_3_data)
        field_flow.append({
            "stage": "3_FIELD_CALIBRATED",
            "timestamp": get_timestamp(),
            "data": {"request_id": request_id, "field_preview": wrapped_prompt[:500]}
        })
        
        # STAGE 4: Backend Forward
        backend_params = {
            "max_new_tokens": request.max_new_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "do_sample": request.do_sample
        }
        stage_4_data = {
            "request_id": request_id,
            "backend_url": settings.backend_url,
            "params": backend_params
        }
        log_stage("4_BACKEND_FORWARD", stage_4_data)
        field_flow.append({
            "stage": "4_BACKEND_FORWARD",
            "timestamp": get_timestamp(),
            "data": stage_4_data
        })
        
        response_text = await forward_stream(wrapped_prompt, backend_params)
        
        # STAGE 5: Response
        latency_ms = int((time.time() - start_time) * 1000)
        stage_5_data = {
            "request_id": request_id,
            "response": response_text,
            "latency_ms": latency_ms,
            "wrapper_chain": wrapper_chain
        }
        log_stage("5_RESPONSE", stage_5_data)
        field_flow.append({
            "stage": "5_RESPONSE",
            "timestamp": get_timestamp(),
            "data": {"request_id": request_id, "latency_ms": latency_ms}
        })
        
        return ChatResponse(
            response=response_text,
            metadata={
                "request_id": request_id,
                "wrapper_chain": wrapper_chain,
                "latency_ms": latency_ms
            },
            field_flow=field_flow
        )
        
    except Exception as e:
        log_stage("ERROR", {
            "request_id": request_id,
            "error": str(e),
            "error_type": type(e).__name__
        })
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resonanz/chat", response_model=ChatResponse)
async def resonance_chat(request: ChatRequest):
    """Resonance chat endpoint - alias to /api/chat"""
    return await chat(request)
