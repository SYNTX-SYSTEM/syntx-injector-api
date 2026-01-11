from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()
MAPPING_FILE = Path("/opt/syntx-config/mapping.json")

@router.get("/format-resonanz/alle")
async def get_alle_format_mappings():
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="Mapping-Datei nicht gefunden")
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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

@router.get("/format-resonanz/statistik")
async def get_mapping_statistik():
    if not MAPPING_FILE.exists():
        raise HTTPException(status_code=404, detail="Mapping-Datei nicht gefunden")
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mappings = data.get("mappings", {})
    
    mistral_wrappers = set()
    gpt_wrappers = set()
    formate_mit_drift = 0
    resonanz_sum = 0.0
    
    for mapping in mappings.values():
        mistral = mapping.get("mistral_wrapper")
        gpt = mapping.get("gpt_wrapper")
        drift_enabled = mapping.get("drift_scoring", {}).get("enabled", False)
        resonanz = mapping.get("resonanz_score", 0.0)
        
        if mistral:
            mistral_wrappers.add(mistral)
        if gpt:
            gpt_wrappers.add(gpt)
        if drift_enabled:
            formate_mit_drift += 1
        
        resonanz_sum += float(resonanz)
    
    total_formats = len(mappings)
    
    return {
        "total_formats": total_formats,
        "formate_mit_drift": formate_mit_drift,
        "formate_ohne_drift": total_formats - formate_mit_drift,
        "wrapper_typen": {
            "mistral_wrappers": len(mistral_wrappers),
            "gpt_wrappers": len(gpt_wrappers)
        },
        "resonanz_durchschnitt": round(resonanz_sum / total_formats, 2) if total_formats > 0 else 0.0
    }

@router.get("/format-resonanz/{format_name}")
async def get_format_mapping_detail(format_name: str):
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
            "resonanz_score": mapping.get("resonanz_score", 0.0)
        }
    }
