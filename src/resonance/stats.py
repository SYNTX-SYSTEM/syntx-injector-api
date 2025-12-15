"""
SYNTX Field Resonance - System Statistics

Not "metrics collection" - FIELD COHERENCE ANALYSIS.
Analyzes accumulated field traces to measure system coherence.
"""
from fastapi import APIRouter
from pathlib import Path
from typing import Dict
from datetime import datetime, timedelta
import json

from ..config import settings

router = APIRouter(prefix="/resonanz", tags=["resonance-stats"])


@router.get("/stats")
async def get_stats() -> Dict:
    """
    Get aggregated system statistics.
    
    Not "reading metrics" - FIELD COHERENCE STATUS.
    Shows how well the resonance system is performing.
    """
    log_file = settings.log_dir / "wrapper_requests.jsonl"
    
    if not log_file.exists():
        return {
            "total_requests": 0,
            "success_rate": 0,
            "average_latency_ms": 0,
            "wrapper_usage": {},
            "recent_24h": {"requests": 0, "average_latency_ms": 0}
        }
    
    total = 0
    success = 0
    latencies = []
    wrapper_usage = {}
    recent_requests = []
    
    # Calculate 24h ago timestamp
    now = datetime.utcnow()
    day_ago = now - timedelta(hours=24)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    req = json.loads(line)
                    total += 1
                    
                    # Success tracking
                    if req.get("success", True):
                        success += 1
                    
                    # Latency tracking
                    if "latency_ms" in req:
                        latencies.append(req["latency_ms"])
                    
                    # Wrapper usage tracking
                    for wrapper in req.get("wrapper_chain", []):
                        wrapper_usage[wrapper] = wrapper_usage.get(wrapper, 0) + 1
                    
                    # Recent 24h tracking
                    if "timestamp" in req:
                        try:
                            req_time = datetime.fromisoformat(req["timestamp"].replace('Z', '+00:00'))
                            if req_time >= day_ago:
                                recent_requests.append(req)
                        except:
                            pass
                            
                except json.JSONDecodeError:
                    continue
        
        # Calculate recent stats
        recent_latencies = [r.get("latency_ms", 0) for r in recent_requests if "latency_ms" in r]
        
        return {
            "total_requests": total,
            "success_rate": round((success / total * 100), 2) if total > 0 else 0,
            "average_latency_ms": int(sum(latencies) / len(latencies)) if latencies else 0,
            "median_latency_ms": int(sorted(latencies)[len(latencies)//2]) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "wrapper_usage": wrapper_usage,
            "recent_24h": {
                "requests": len(recent_requests),
                "average_latency_ms": int(sum(recent_latencies) / len(recent_latencies)) if recent_latencies else 0
            }
        }
        
    except Exception as e:
        return {
            "total_requests": 0,
            "error": str(e)
        }


@router.get("/stats/wrapper/{name}")
async def get_wrapper_stats(name: str) -> Dict:
    """
    Get statistics for specific wrapper.
    
    Shows performance metrics for individual wrapper field.
    """
    log_file = settings.log_dir / "wrapper_requests.jsonl"
    
    if not log_file.exists():
        return {"wrapper": name, "requests": 0}
    
    requests = 0
    success = 0
    latencies = []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    req = json.loads(line)
                    
                    # Check if this wrapper was used
                    if name in req.get("wrapper_chain", []):
                        requests += 1
                        
                        if req.get("success", True):
                            success += 1
                        
                        if "latency_ms" in req:
                            latencies.append(req["latency_ms"])
                            
                except json.JSONDecodeError:
                    continue
        
        return {
            "wrapper": name,
            "requests": requests,
            "success_rate": round((success / requests * 100), 2) if requests > 0 else 0,
            "average_latency_ms": int(sum(latencies) / len(latencies)) if latencies else 0,
            "median_latency_ms": int(sorted(latencies)[len(latencies)//2]) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0
        }
        
    except Exception as e:
        return {
            "wrapper": name,
            "requests": 0,
            "error": str(e)
        }
