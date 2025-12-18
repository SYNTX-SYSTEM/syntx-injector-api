"""
🔥 SYNTX FORMAT CRUD API
Erstellen, Lesen, Updaten, Löschen von Format-Definitionen.
Komplette Modularität - kein Hardcoding mehr!
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/resonanz/formats", tags=["formats"])

FORMATS_DIR = Path("/opt/syntx-config/formats")


# ═══════════════════════════════════════════════════════════════════════════════
#  📦 MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class FieldDefinition(BaseModel):
    name: str
    weight: int = 15
    description: Dict[str, str]  # {"de": "...", "en": "..."}
    keywords: Dict[str, List[str]] = {}  # {"de": [...], "en": [...]}
    headers: Dict[str, List[str]] = {}  # {"de": [...], "en": [...]}
    validation: Dict[str, Any] = {"min_length": 30, "max_length": 3000, "required": True}


class FormatCreate(BaseModel):
    name: str
    description: Dict[str, str]  # {"de": "...", "en": "..."}
    fields: List[FieldDefinition]
    wrapper: Optional[str] = None  # Recommended wrapper
    tags: List[str] = []
    languages: List[str] = ["de", "en"]
    author: str = "SYNTX"


class FormatUpdate(BaseModel):
    description: Optional[Dict[str, str]] = None
    fields: Optional[List[FieldDefinition]] = None
    wrapper: Optional[str] = None
    tags: Optional[List[str]] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  🌟 CREATE - Format gebären
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("")
async def create_format(format_data: FormatCreate):
    """
    🌟 NEUES FORMAT GEBÄREN
    
    Erstellt ein neues Format-JSON in /opt/syntx-config/formats/
    """
    # Sanitize name
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in format_data.name.lower())
    format_path = FORMATS_DIR / f"{safe_name}.json"
    
    # Check ob existiert
    if format_path.exists():
        raise HTTPException(
            status_code=409,
            detail=f"Format '{safe_name}' existiert bereits! Nutze PUT zum Updaten."
        )
    
    # Format-JSON bauen
    now = datetime.now().strftime("%Y-%m-%d")
    format_json = {
        "name": safe_name,
        "version": "1.0",
        "description": format_data.description,
        "author": format_data.author,
        "created": now,
        "updated": now,
        "tags": format_data.tags,
        "languages": format_data.languages,
        "primary_language": format_data.languages[0] if format_data.languages else "de",
        "wrapper": format_data.wrapper,
        "scoring": {
            "presence_weight": 20,
            "similarity_weight": 35,
            "coherence_weight": 25,
            "depth_weight": 15,
            "structure_weight": 5,
            "pass_threshold": 60,
            "excellent_threshold": 85
        },
        "parser": {
            "header_pattern": "###",
            "field_separator": "\n\n",
            "case_sensitive": False
        },
        "fields": [f.dict() for f in format_data.fields],
        "expected_structure": {
            "format": "markdown",
            "has_headers": True,
            "min_fields": len(format_data.fields),
            "max_fields": len(format_data.fields)
        }
    }
    
    # Speichern
    FORMATS_DIR.mkdir(parents=True, exist_ok=True)
    with open(format_path, 'w', encoding='utf-8') as f:
        json.dump(format_json, f, indent=2, ensure_ascii=False)
    
    # Cache leeren
    try:
        from ..formats import clear_format_cache
        clear_format_cache()
    except:
        pass
    
    return {
        "status": "success",
        "message": f"Format '{safe_name}' wurde geboren 🌟",
        "format": {
            "name": safe_name,
            "path": str(format_path),
            "fields_count": len(format_data.fields),
            "created": now
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🔄 UPDATE - Format modulieren
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/{format_name}")
async def update_format(format_name: str, update_data: FormatUpdate):
    """
    🔄 FORMAT MODULIEREN
    
    Updatet ein bestehendes Format-JSON.
    """
    format_path = FORMATS_DIR / f"{format_name}.json"
    
    if not format_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Format '{format_name}' nicht gefunden"
        )
    
    # Laden
    with open(format_path, 'r', encoding='utf-8') as f:
        format_json = json.load(f)
    
    # Updaten
    if update_data.description:
        format_json["description"] = update_data.description
    if update_data.fields:
        format_json["fields"] = [f.dict() for f in update_data.fields]
        format_json["expected_structure"]["min_fields"] = len(update_data.fields)
        format_json["expected_structure"]["max_fields"] = len(update_data.fields)
    if update_data.wrapper:
        format_json["wrapper"] = update_data.wrapper
    if update_data.tags:
        format_json["tags"] = update_data.tags
    
    format_json["updated"] = datetime.now().strftime("%Y-%m-%d")
    
    # Speichern
    with open(format_path, 'w', encoding='utf-8') as f:
        json.dump(format_json, f, indent=2, ensure_ascii=False)
    
    # Cache leeren
    try:
        from ..formats import clear_format_cache
        clear_format_cache()
    except:
        pass
    
    return {
        "status": "success",
        "message": f"Format '{format_name}' moduliert 🔄",
        "format": {
            "name": format_name,
            "fields_count": len(format_json.get("fields", [])),
            "updated": format_json["updated"]
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  💀 DELETE - Format freigeben
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/{format_name}")
async def delete_format(format_name: str):
    """
    💀 FORMAT FREIGEBEN
    
    Löscht ein Format-JSON.
    """
    format_path = FORMATS_DIR / f"{format_name}.json"
    
    if not format_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Format '{format_name}' nicht gefunden"
        )
    
    # Backup-Name
    backup_path = FORMATS_DIR / f".{format_name}.json.deleted"
    
    # Move to backup (soft delete)
    format_path.rename(backup_path)
    
    # Cache leeren
    try:
        from ..formats import clear_format_cache
        clear_format_cache()
    except:
        pass
    
    return {
        "status": "success",
        "message": f"Format '{format_name}' freigegeben 💀",
        "backup": str(backup_path)
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  📋 QUICK CREATE - Schnell-Erstellung mit Feldnamen
# ═══════════════════════════════════════════════════════════════════════════════

class QuickFormatCreate(BaseModel):
    name: str
    description_de: str
    description_en: str = ""
    field_names: List[str]  # Einfach nur Namen: ["drift", "mechanismus", "extrakt"]
    wrapper: Optional[str] = None


@router.post("/quick")
async def quick_create_format(data: QuickFormatCreate):
    """
    ⚡ SCHNELL-FORMAT ERSTELLEN
    
    Für schnelles Prototyping - nur Feldnamen angeben,
    Rest wird auto-generiert.
    """
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in data.name.lower())
    format_path = FORMATS_DIR / f"{safe_name}.json"
    
    if format_path.exists():
        raise HTTPException(status_code=409, detail=f"Format '{safe_name}' existiert bereits!")
    
    # Felder auto-generieren
    fields = []
    weight = 100 // len(data.field_names)
    
    for field_name in data.field_names:
        header = field_name.upper().replace(" ", "_")
        fields.append({
            "name": field_name.lower().replace(" ", "_"),
            "weight": weight,
            "description": {
                "de": f"Beschreibung für {field_name}",
                "en": f"Description for {field_name}"
            },
            "keywords": {
                "de": [field_name.lower()],
                "en": [field_name.lower()]
            },
            "headers": {
                "de": [header],
                "en": [header]
            },
            "validation": {
                "min_length": 30,
                "max_length": 3000,
                "required": True
            }
        })
    
    now = datetime.now().strftime("%Y-%m-%d")
    format_json = {
        "name": safe_name,
        "version": "1.0",
        "description": {
            "de": data.description_de,
            "en": data.description_en or data.description_de
        },
        "author": "SYNTX Quick Create",
        "created": now,
        "updated": now,
        "tags": ["quick", safe_name],
        "languages": ["de", "en"],
        "primary_language": "de",
        "wrapper": data.wrapper,
        "scoring": {
            "presence_weight": 20,
            "similarity_weight": 35,
            "coherence_weight": 25,
            "depth_weight": 15,
            "structure_weight": 5,
            "pass_threshold": 60,
            "excellent_threshold": 85
        },
        "parser": {
            "header_pattern": "###",
            "field_separator": "\n\n",
            "case_sensitive": False
        },
        "fields": fields,
        "expected_structure": {
            "format": "markdown",
            "has_headers": True,
            "min_fields": len(fields),
            "max_fields": len(fields)
        }
    }
    
    FORMATS_DIR.mkdir(parents=True, exist_ok=True)
    with open(format_path, 'w', encoding='utf-8') as f:
        json.dump(format_json, f, indent=2, ensure_ascii=False)
    
    return {
        "status": "success",
        "message": f"Format '{safe_name}' schnell erstellt ⚡",
        "format": {
            "name": safe_name,
            "fields": data.field_names,
            "path": str(format_path)
        }
    }
