"""
📊 MAPPING FORMAT RESONANZ – SYNTX v3.4
Eindeutige, präzise Mapping-Endpoints für die Zwei-Wrapper-Architektur.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List
import json
from pathlib import Path

router = APIRouter()

# 📁 MAPPING FILE PATH
MAPPING_FILE = Path("/opt/syntx-config/mapping.json")

@router.get("/format-resonanz/alle", tags=["Mapping Format Resonanz"])
async def get_alle_format_mappings():
    """
    🌀 Gibt alle Format-Mappings zurück – Mistral + GPT-4 Wrapper Matrix.
    """
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="Mapping-Datei nicht gefunden")
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extrahiere klare Struktur
    mappings = []
    for format_name, mapping in data.get("mappings", {}).items():
        mappings.append({
            "format_name": format_name,
            "mistral_wrapper": mapping.get("mistral_wrapper"),
            "gpt_wrapper": mapping.get("gpt_wrapper"),
            "drift_scoring_enabled": mapping.get("drift_scoring", {}).get("enabled", False),
            "resonanz_score": mapping.get("resonanz_score", 0.0)
        })
    
    return {
        "system": "SYNTX Mapping Format Resonanz",
        "total_formats": len(mappings),
        "mappings": mappings,
        "stats": {
            "mit_drift_scoring": sum(1 for m in mappings if m["drift_scoring_enabled"]),
            "ohne_drift_scoring": sum(1 for m in mappings if not m["drift_scoring_enabled"])
        }
    }

@router.get("/format-resonanz/{format_name}", tags=["Mapping Format Resonanz"])
async def get_format_mapping_detail(format_name: str):
    """
    🔍 Gibt detailliertes Mapping für ein spezifisches Format zurück.
    """
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="Mapping-Datei nicht gefunden")
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mapping = data.get("mappings", {}).get(format_name)
    if not mapping:
        raise HTTPException(status_code=404, detail=f"Format '{format_name}' nicht gefunden")
    
    return {
        "format_name": format_name,
        "mistral_wrapper": mapping.get("mistral_wrapper"),
        "gpt_wrapper": mapping.get("gpt_wrapper"),
        "drift_scoring": mapping.get("drift_scoring", {}),
        "metadata": {
            "resonanz_score": mapping.get("resonanz_score", 0.0),
            "erstellt": mapping.get("erstellt"),
            "geaendert": mapping.get("geaendert")
        }
    }

@router.get("/format-resonanz/statistik", tags=["Mapping Format Resonanz"])
async def get_mapping_statistik():
    """
    📈 Statistik der Mapping-Architektur.
    """
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="Mapping-Datei nicht gefunden")
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mappings = data.get("mappings", {})
    
    return {
        "total_formats": len(mappings),
        "formate_mit_drift": sum(1 for m in mappings.values() if m.get("drift_scoring", {}).get("enabled", False)),
        "formate_ohne_drift": sum(1 for m in mappings.values() if not m.get("drift_scoring", {}).get("enabled", False)),
        "wrapper_typen": {
            "mistral_wrappers": len(set(m.get("mistral_wrapper") for m in mappings.values() if m.get("mistral_wrapper"))),
            "gpt_wrappers": len(set(m.get("gpt_wrapper") for m in mappings.values() if m.get("gpt_wrapper")))
        },
        "resonanz_durchschnitt": sum(m.get("resonanz_score", 0.0) for m in mappings.values()) / max(len(mappings), 1)
    }
