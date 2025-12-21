"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🔀 SYNTX DIFF - PARALLELWELT-VISUALISIERUNG                              ║
║                                                                              ║
║    Gleicher Prompt. Verschiedene Wrapper. Side-by-Side.                     ║
║    Zeigt wie der WRAPPER das DENKEN verändert.                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import time

router = APIRouter(prefix="/resonanz", tags=["resonance-diff"])


class DiffRequest(BaseModel):
    """Wrapper-Vergleichs-Request"""
    prompt: str
    wrappers: List[str]  # z.B. ["syntex_wrapper_sigma", "syntex_wrapper_human"]
    format: Optional[str] = None
    style: Optional[str] = None
    max_new_tokens: int = 200
    temperature: float = 0.7


class DiffComparison(BaseModel):
    """Einzelner Wrapper-Output"""
    wrapper: str
    response: str
    latency_ms: int
    format_fields: List[str] = []


class DiffResponse(BaseModel):
    """Vergleichs-Ergebnis"""
    prompt: str
    comparisons: List[DiffComparison]
    diff_analysis: dict


@router.post("/chat/diff", response_model=DiffResponse)
async def compare_wrappers(request: DiffRequest):
    """
    🔀 WRAPPER DIFF - Parallelwelt-Vergleich
    
    Sendet den GLEICHEN Prompt an VERSCHIEDENE Wrapper.
    Zeigt Side-by-Side wie sich das Denken unterscheidet.
    """
    from ..chat import chat
    from ..models import ChatRequest
    
    if len(request.wrappers) < 2:
        raise HTTPException(
            status_code=400, 
            detail="Mindestens 2 Wrapper für Vergleich nötig"
        )
    
    if len(request.wrappers) > 5:
        raise HTTPException(
            status_code=400,
            detail="Maximal 5 Wrapper pro Vergleich"
        )
    
    comparisons = []
    
    # Sequentiell ausführen (könnte auch parallel sein)
    for wrapper_name in request.wrappers:
        start = time.time()
        
        try:
            chat_request = ChatRequest(
                prompt=request.prompt,
                mode=wrapper_name,
                format=request.format,
                style=request.style,
                max_new_tokens=request.max_new_tokens,
                temperature=request.temperature
            )
            
            result = await chat(chat_request)
            latency = int((time.time() - start) * 1000)
            
            comparisons.append(DiffComparison(
                wrapper=wrapper_name,
                response=result.response,
                latency_ms=latency,
                format_fields=result.metadata.get("format_fields", [])
            ))
            
        except Exception as e:
            comparisons.append(DiffComparison(
                wrapper=wrapper_name,
                response=f"❌ ERROR: {str(e)}",
                latency_ms=0,
                format_fields=[]
            ))
    
    # Diff-Analyse
    diff_analysis = _analyze_diff(comparisons)
    
    return DiffResponse(
        prompt=request.prompt,
        comparisons=comparisons,
        diff_analysis=diff_analysis
    )


def _analyze_diff(comparisons: List[DiffComparison]) -> dict:
    """
    📊 Analysiert Unterschiede zwischen Wrapper-Outputs
    """
    if len(comparisons) < 2:
        return {"error": "Nicht genug Vergleiche"}
    
    responses = [c.response for c in comparisons if not c.response.startswith("❌")]
    
    if len(responses) < 2:
        return {"error": "Nicht genug erfolgreiche Responses"}
    
    # Einfache Längenanalyse
    lengths = [len(r) for r in responses]
    avg_length = sum(lengths) / len(lengths)
    
    # Latenz-Analyse
    latencies = [c.latency_ms for c in comparisons if c.latency_ms > 0]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    # Wrapper mit längster/kürzester Antwort
    sorted_by_length = sorted(comparisons, key=lambda x: len(x.response))
    
    return {
        "total_comparisons": len(comparisons),
        "successful": len(responses),
        "avg_response_length": int(avg_length),
        "avg_latency_ms": int(avg_latency),
        "shortest_response": {
            "wrapper": sorted_by_length[0].wrapper,
            "length": len(sorted_by_length[0].response)
        },
        "longest_response": {
            "wrapper": sorted_by_length[-1].wrapper,
            "length": len(sorted_by_length[-1].response)
        }
    }
