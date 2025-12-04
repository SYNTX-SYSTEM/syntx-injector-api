"""
SYNTX Wrapper Service - Stream Functions

Modified for Ollama backend support.
"""
import httpx
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import uuid

from .config import settings


async def load_wrapper_stream(
    mode: str,
    include_init: bool,
    include_terminology: bool
) -> tuple[str, List[str]]:
    """Load and combine wrapper files."""
    wrapper_texts: List[str] = []
    wrapper_chain: List[str] = []
    
    if include_init:
        init_text = await _read_wrapper_file("syntx_init")
        if init_text:
            wrapper_texts.append(init_text)
            wrapper_chain.append("syntx_init")
    
    if include_terminology:
        term_text = await _read_wrapper_file("terminology")
        if term_text:
            wrapper_texts.append(term_text)
            wrapper_chain.append("terminology")
    
    mode_text = await _read_wrapper_file(mode)
    if mode_text:
        wrapper_texts.append(mode_text)
        wrapper_chain.append(mode)
    elif not wrapper_texts:
        fallback_text = await _read_wrapper_file(settings.fallback_mode)
        if fallback_text:
            wrapper_texts.append(fallback_text)
            wrapper_chain.append(f"{settings.fallback_mode} (fallback)")
    
    combined_wrapper = "\n\n".join(wrapper_texts)
    return combined_wrapper, wrapper_chain


async def _read_wrapper_file(wrapper_name: str) -> str:
    """Read a single wrapper file from disk."""
    wrapper_path = settings.wrapper_dir / f"{wrapper_name}.txt"
    
    try:
        with open(wrapper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if settings.log_to_console:
            print(f"✅ Loaded wrapper: {wrapper_name} ({len(content)} chars)")
        
        return content
        
    except FileNotFoundError:
        if settings.log_to_console:
            print(f"⚠️  Wrapper not found: {wrapper_name}")
        return ""
        
    except Exception as e:
        if settings.log_to_console:
            print(f"❌ Error loading wrapper {wrapper_name}: {e}")
        return ""


def wrap_input_stream(wrapper_text: str, user_input: str) -> str:
    """Wrap user input with loaded wrapper text."""
    return f"{wrapper_text}\n{user_input}"


async def forward_stream(
    wrapped_prompt: str,
    backend_params: Dict[str, Any]
) -> str:
    """
    Forward wrapped prompt to Ollama backend and get response.
    
    MODIFIED FOR OLLAMA SUPPORT!
    """
    # Build Ollama-specific payload
    payload = {
        "model": settings.model_name,
        "prompt": wrapped_prompt,
        "stream": False,
        "options": {
            "temperature": backend_params.get("temperature", 0.7),
            "num_predict": backend_params.get("max_new_tokens", 1000)
        }
    }
    
    # Build headers
    headers = {"Content-Type": "application/json"}
    if settings.backend_bearer_token:
        headers["Authorization"] = f"Bearer {settings.backend_bearer_token}"
    
    # Forward to Ollama backend
    async with httpx.AsyncClient(timeout=settings.backend_timeout) as client:
        response = await client.post(
            settings.backend_url,
            json=payload,
            headers=headers
        )
        
        # Raise for HTTP errors
        response.raise_for_status()
        
        # Parse Ollama response format
        response_data = response.json()
        
        # Ollama returns: {"model": "...", "response": "text", "done": true}
        if isinstance(response_data, dict) and "response" in response_data:
            return response_data["response"]
        else:
            return str(response_data)


async def log_stream(log_data: Dict[str, Any]) -> None:
    """Log request/response data to files."""
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    
    jsonl_path = settings.log_dir / "wrapper_requests.jsonl"
    with open(jsonl_path, 'a', encoding='utf-8') as f:
        import json
        f.write(json.dumps(log_data, ensure_ascii=False) + '\n')
    
    if settings.log_to_console:
        log_line = (
            f"[{log_data['timestamp']}] "
            f"mode={log_data['mode']} "
            f"chain={log_data['wrapper_chain']} "
            f"latency={log_data.get('total_latency_ms', 'N/A')}ms "
            f"success={log_data.get('success', False)}"
        )
        print(log_line)
    
    human_log_path = settings.log_dir / "service.log"
    with open(human_log_path, 'a', encoding='utf-8') as f:
        f.write(f"{log_data}\n")


def generate_request_id() -> str:
    """Generate unique request ID for tracing."""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + 'Z'
