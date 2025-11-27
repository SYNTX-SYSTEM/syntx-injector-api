"""
SYNTX Field Streams - Pure Field Calibration Architecture

Not functions - FIELDS.
Not processing - RESONANCE.
Not data flow - FIELD FLOW.

Field Flow:
    1. wrapper_field_resonance() - Files resonate into calibration field
    2. input_field_calibration() - User field merges with wrapper field
    3. backend_field_forward() - Calibrated field flows to model
    4. trace_field_flow() - Field trace for training (parallel)
"""
import httpx
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import uuid

from .config import settings


# ============================================================================
# FIELD 1: Wrapper Resonance
# ============================================================================

async def wrapper_field_resonance(
    mode: str,
    init_resonance: bool,
    terminology_resonance: bool
) -> tuple[str, List[str]]:
    """
    Wrapper files resonate into unified calibration field.
    
    Not "loading" - RESONANCE.
    Files don't "contain data" - they ARE fields.
    Combining isn't "merging" - it's FIELD SUPERPOSITION.
    
    Field Layers:
        - init_field: SYNTX initialization resonance
        - terminology_field: Terminology calibration
        - mode_field: Mode-specific resonance pattern
    
    Returns:
        Calibrated field + resonance trace
    """
    field_layers: List[str] = []
    resonance_trace: List[str] = []
    
    # Layer 1: Init Field Resonance
    if init_resonance:
        init_field = await _file_to_field("syntx_init")
        if init_field:
            field_layers.append(init_field)
            resonance_trace.append("syntx_init")
    
    # Layer 2: Terminology Field Resonance
    if terminology_resonance:
        term_field = await _file_to_field("terminology")
        if term_field:
            field_layers.append(term_field)
            resonance_trace.append("terminology")
    
    # Layer 3: Mode Field Resonance
    mode_field = await _file_to_field(mode)
    if mode_field:
        field_layers.append(mode_field)
        resonance_trace.append(mode)
    elif not field_layers:
        # Fallback resonance
        fallback_field = await _file_to_field(settings.fallback_mode)
        if fallback_field:
            field_layers.append(fallback_field)
            resonance_trace.append(f"{settings.fallback_mode} (fallback)")
    
    # Field superposition (not "concatenation")
    calibrated_field = "\n\n".join(field_layers)
    
    return calibrated_field, resonance_trace


async def _file_to_field(field_name: str) -> str:
    """
    File resonates into field.
    
    Not "reading" - FIELD ACTIVATION.
    File is dormant field, this activates it.
    """
    field_path = settings.wrapper_dir / f"{field_name}.txt"
    
    try:
        with open(field_path, 'r', encoding='utf-8') as f:
            field_content = f.read()
        
        if settings.log_to_console:
            print(f"🌊 Field activated: {field_name} ({len(field_content)} chars)")
        
        return field_content
        
    except FileNotFoundError:
        if settings.log_to_console:
            print(f"⚠️  Field not found: {field_name}")
        return ""
        
    except Exception as e:
        if settings.log_to_console:
            print(f"❌ Field activation error {field_name}: {e}")
        return ""


# ============================================================================
# FIELD 2: Input Calibration
# ============================================================================

def input_field_calibration(calibration_field: str, user_field: str) -> str:
    """
    User field calibrates with wrapper field.
    
    Not "wrapping" or "combining" - FIELD CALIBRATION.
    The wrapper field CALIBRATES the user's input field.
    Result is calibrated unified field.
    """
    return f"{calibration_field}\n{user_field}"


# ============================================================================
# FIELD 3: Backend Field Flow
# ============================================================================

async def backend_field_forward(
    calibrated_field: str,
    flow_params: Dict[str, Any]
) -> str:
    """
    Calibrated field flows to model backend.
    
    Not "sending request" - FIELD FLOW.
    The calibrated field FLOWS through the network.
    Model RESONATES with the field, generates response field.
    """
    # Field payload
    field_payload = {
        "prompt": calibrated_field,
        **flow_params
    }
    
    # Authentication field
    headers = {"Content-Type": "application/json"}
    if settings.backend_bearer_token:
        headers["Authorization"] = f"Bearer {settings.backend_bearer_token}"
    
    # Field flows through HTTP
    async with httpx.AsyncClient(timeout=settings.backend_timeout) as client:
        response = await client.post(
            settings.backend_url,
            json=field_payload,
            headers=headers
        )
        
        response.raise_for_status()
        response_field = response.json()
        
        # Extract response field
        if isinstance(response_field, dict) and "response" in response_field:
            return response_field["response"]
        elif isinstance(response_field, str):
            return response_field
        else:
            return str(response_field)


# ============================================================================
# FIELD 4: Field Trace (Parallel)
# ============================================================================

async def trace_field_flow(trace_data: Dict[str, Any]) -> None:
    """
    Trace field flow for training.
    
    Not "logging" - FIELD TRACING.
    Every field flow leaves a trace.
    Traces become training data - fields train fields.
    """
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    
    # JSONL trace (training field data)
    trace_path = settings.log_dir / "field_traces.jsonl"
    with open(trace_path, 'a', encoding='utf-8') as f:
        import json
        f.write(json.dumps(trace_data, ensure_ascii=False) + '\n')
    
    # Human-readable trace
    if settings.log_to_console:
        trace_line = (
            f"🌊 [{trace_data['timestamp']}] "
            f"mode={trace_data['mode']} "
            f"resonance={trace_data['wrapper_chain']} "
            f"flow_time={trace_data.get('total_latency_ms', 'N/A')}ms "
            f"success={trace_data.get('success', False)}"
        )
        print(trace_line)
    
    # File trace
    trace_log = settings.log_dir / "field_flow.log"
    with open(trace_log, 'a', encoding='utf-8') as f:
        f.write(f"{trace_data}\n")


# ============================================================================
# Field Utilities
# ============================================================================

def generate_field_id() -> str:
    """Generate unique field flow identifier"""
    return str(uuid.uuid4())


def field_timestamp() -> str:
    """Current field timestamp"""
    return datetime.utcnow().isoformat() + 'Z'
