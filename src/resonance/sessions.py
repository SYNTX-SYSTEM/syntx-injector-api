"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    📼 SYNTX SESSIONS - STROM-REPLAY                                         ║
║                                                                              ║
║    Jede Session ist eine Strom-Einheit.                                     ║
║    Hier können wir sie zurückspulen und neu erleben.                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import json

router = APIRouter(prefix="/resonanz", tags=["resonance-sessions"])

LOG_DIR = Path("/opt/syntx-config/logs")
FLOW_LOG = LOG_DIR / "field_flow.jsonl"


@router.get("/sessions")
async def list_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    📋 SESSIONS LISTEN
    
    Zeigt alle bekannten Sessions (gruppiert nach request_id).
    """
    sessions = _extract_sessions()
    
    # Pagination
    total = len(sessions)
    paginated = sessions[offset:offset + limit]
    
    return {
        "status": "📼 SESSIONS GELADEN",
        "total": total,
        "offset": offset,
        "limit": limit,
        "sessions": paginated
    }


@router.get("/session/{request_id}")
async def get_session(request_id: str):
    """
    🔍 SESSION DETAILS
    
    Zeigt den kompletten Field Flow einer Session.
    Für Replay und Analyse.
    """
    if not FLOW_LOG.exists():
        raise HTTPException(status_code=404, detail="Keine Logs gefunden")
    
    session_events = []
    
    with open(FLOW_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry.get("request_id") == request_id:
                    session_events.append(entry)
            except:
                continue
    
    if not session_events:
        raise HTTPException(
            status_code=404, 
            detail=f"Session '{request_id}' nicht gefunden"
        )
    
    # Sortiere nach Stage
    stage_order = {
        "1_INCOMING": 1,
        "2_WRAPPERS_LOADED": 2,
        "2.5_FORMAT_LOADED": 3,
        "3_FIELD_CALIBRATED": 4,
        "4_BACKEND_FORWARD": 5,
        "5_RESPONSE": 6,
        "ERROR": 99
    }
    session_events.sort(key=lambda x: stage_order.get(x.get("stage", ""), 50))
    
    # Extrahiere Key-Infos
    incoming = next((e for e in session_events if e.get("stage") == "1_INCOMING"), {})
    response = next((e for e in session_events if e.get("stage") == "5_RESPONSE"), {})
    
    return {
        "status": "🔍 SESSION GELADEN",
        "request_id": request_id,
        "summary": {
            "prompt": incoming.get("prompt", ""),
            "wrapper": incoming.get("mode", ""),
            "format": incoming.get("format"),
            "response_preview": response.get("response", "")[:500] + "..." if response.get("response") else None,
            "latency_ms": response.get("latency_ms"),
            "timestamp": incoming.get("timestamp")
        },
        "field_flow": session_events
    }


@router.get("/session/{request_id}/replay")
async def replay_session(request_id: str):
    """
    🔄 SESSION REPLAY
    
    Gibt die Parameter zurück, um die Session neu auszuführen.
    """
    session = await get_session(request_id)
    
    incoming = next(
        (e for e in session["field_flow"] if e.get("stage") == "1_INCOMING"), 
        {}
    )
    
    if not incoming:
        raise HTTPException(
            status_code=400,
            detail="Session hat keine INCOMING Stage"
        )
    
    return {
        "status": "🔄 REPLAY READY",
        "request_id": request_id,
        "replay_params": {
            "prompt": incoming.get("prompt"),
            "mode": incoming.get("mode"),
            "format": incoming.get("format"),
            "language": incoming.get("language", "de"),
            "include_init": incoming.get("include_init", True)
        },
        "original_response": session["summary"].get("response_preview"),
        "original_latency_ms": session["summary"].get("latency_ms")
    }


def _extract_sessions() -> List[dict]:
    """
    📊 Extrahiert alle Sessions aus dem Log
    """
    if not FLOW_LOG.exists():
        return []
    
    sessions = {}
    
    with open(FLOW_LOG, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                req_id = entry.get("request_id")
                if not req_id:
                    continue
                
                if req_id not in sessions:
                    sessions[req_id] = {
                        "request_id": req_id,
                        "timestamp": entry.get("timestamp"),
                        "stages": [],
                        "prompt": None,
                        "wrapper": None,
                        "format": None,
                        "latency_ms": None
                    }
                
                stage = entry.get("stage")
                sessions[req_id]["stages"].append(stage)
                
                if stage == "1_INCOMING":
                    sessions[req_id]["prompt"] = entry.get("prompt", "")[:100]
                    sessions[req_id]["wrapper"] = entry.get("mode")
                    sessions[req_id]["format"] = entry.get("format")
                    sessions[req_id]["timestamp"] = entry.get("timestamp")
                
                if stage == "5_RESPONSE":
                    sessions[req_id]["latency_ms"] = entry.get("latency_ms")
                    
            except:
                continue
    
    # Als Liste, sortiert nach Timestamp (neueste zuerst)
    session_list = list(sessions.values())
    session_list.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return session_list
