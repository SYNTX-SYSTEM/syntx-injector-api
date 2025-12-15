"""
SYNTX Field Resonance - Stream Access

Not "log reading" - FIELD TRACE ACCESS.
Every field flow leaves a trace, this makes traces visible.
"""
from fastapi import APIRouter
from pathlib import Path
from typing import List, Dict, Optional, Any
import json

from ..config import settings

router = APIRouter(prefix="/resonanz", tags=["resonance-streams"])


@router.get("/strom")
async def get_field_stream(limit: int = 20, stage: str = "all") -> Dict[str, Any]:
    """
    Get recent field flow events.
    
    Not "reading logs" - FIELD TRACE ACCESS.
    Shows how fields flowed through the system.
    """
    log_file = settings.log_dir / "field_flow.jsonl"
    
    if not log_file.exists():
        return {"events": [], "total": 0}
    
    events = []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Read from end, collect last N events
            for line in reversed(lines[-limit * 5:]):
                try:
                    event = json.loads(line)
                    
                    # Filter by stage if specified
                    if stage == "all" or event.get("stage") == stage:
                        events.append(event)
                        
                        if len(events) >= limit:
                            break
                            
                except json.JSONDecodeError:
                    continue
        
        return {
            "events": events[:limit],
            "total": len(events),
            "stage_filter": stage
        }
        
    except Exception as e:
        return {
            "events": [],
            "total": 0,
            "error": str(e)
        }


@router.get("/training")
async def get_training_data(
    limit: int = 100, 
    wrapper: str = "all",
    success_only: bool = False
) -> Dict[str, Any]:
    """
    Get training data (request/response pairs).
    
    Not "reading logs" - TRAINING FIELD ACCESS.
    Shows accumulated resonance traces for model training.
    """
    log_file = settings.log_dir / "wrapper_requests.jsonl"
    
    if not log_file.exists():
        return {"requests": [], "total": 0}
    
    requests = []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Read from end
            for line in reversed(lines[-limit * 2:]):
                try:
                    req = json.loads(line)
                    
                    # Filter by wrapper if specified
                    if wrapper != "all":
                        wrapper_chain = req.get("wrapper_chain", [])
                        if wrapper not in wrapper_chain:
                            continue
                    
                    # Filter by success if specified
                    if success_only and not req.get("success", True):
                        continue
                    
                    requests.append(req)
                    
                    if len(requests) >= limit:
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        return {
            "requests": requests[:limit],
            "total": len(requests),
            "filters": {
                "wrapper": wrapper,
                "success_only": success_only
            }
        }
        
    except Exception as e:
        return {
            "requests": [],
            "total": 0,
            "error": str(e)
        }


@router.get("/history/{request_id}")
async def get_request_history(request_id: str) -> Dict:
    """
    Get complete field flow for specific request.
    
    Returns all 5 stages for given request_id.
    """
    log_file = settings.log_dir / "field_flow.jsonl"
    
    if not log_file.exists():
        return {"stages": [], "request_id": request_id}
    
    stages = []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get("request_id") == request_id:
                        stages.append(event)
                except json.JSONDecodeError:
                    continue
        
        return {
            "request_id": request_id,
            "stages": sorted(stages, key=lambda x: x.get("stage", "")),
            "total_stages": len(stages)
        }
        
    except Exception as e:
        return {
            "request_id": request_id,
            "stages": [],
            "error": str(e)
        }
