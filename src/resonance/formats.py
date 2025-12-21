"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    📄 FORMAT RESONANCE ROUTER - Vollständiger CRUD                          ║
║                                                                              ║
║    GET    /formats              → Liste (mit Domain-Filter)                 ║
║    GET    /formats/{name}       → Details (mit Vererbung)                   ║
║    POST   /formats              → Vollständiges Format erstellen            ║
║    POST   /formats/quick        → Schnell-Erstellung                        ║
║    PUT    /formats/{name}       → Format updaten                            ║
║    DELETE /formats/{name}       → Soft Delete                               ║
║                                                                              ║
║    POST   /formats/{name}/fields           → Feld hinzufügen               ║
║    PUT    /formats/{name}/fields/{field}   → Feld updaten                  ║
║    DELETE /formats/{name}/fields/{field}   → Feld entfernen                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from .crud import format_crud

router = APIRouter(prefix="/resonanz/formats", tags=["📄 Formats"])


# ═══════════════════════════════════════════════════════════════════════════════
#  📋 PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class FieldCreate(BaseModel):
    """Einzelnes Feld erstellen"""
    name: str = Field(..., description="Feld-Name (lowercase, underscore)")
    type: str = Field(default="text", description="text, list, rating, keywords")
    weight: int = Field(default=10, ge=0, le=100)
    description: Optional[Dict[str, str]] = Field(default={"de": "", "en": ""})

class FieldUpdate(BaseModel):
    """Feld updaten"""
    type: Optional[str] = None
    weight: Optional[int] = None
    description: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, List[str]]] = None
    keywords: Optional[Dict[str, List[str]]] = None

class FormatCreate(BaseModel):
    """Vollständiges Format erstellen"""
    name: str = Field(..., description="Format-Name")
    domain: Optional[str] = Field(default=None, description="technical, psychology, analysis...")
    extends: Optional[str] = Field(default=None, description="Parent-Format für Vererbung")
    description: Optional[Dict[str, str]] = Field(default={"de": "", "en": ""})
    wrapper: Optional[str] = Field(default=None, description="Empfohlener Wrapper")
    fields: List[FieldCreate] = Field(..., min_length=1)

class FormatQuickCreate(BaseModel):
    """Schnell-Erstellung"""
    name: str
    description_de: str = ""
    field_names: List[str] = Field(..., min_length=1)
    domain: Optional[str] = None
    wrapper: Optional[str] = None

class FormatUpdate(BaseModel):
    """Format updaten"""
    domain: Optional[str] = None
    extends: Optional[str] = None
    description: Optional[Dict[str, str]] = None
    wrapper: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 READ ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("")
async def list_formats(
    domain: Optional[str] = Query(None, description="Filter nach Domain")
):
    """
    📋 ALLE FORMATE AUFLISTEN
    
    Optional nach Domain filtern.
    """
    if domain:
        names = format_crud.list_by_domain(domain)
    else:
        names = format_crud.list_all()
    
    formats = []
    for name in names:
        fmt = format_crud.get(name)
        if fmt:
            formats.append({
                "name": name,
                "domain": fmt.get("domain"),
                "fields_count": len(fmt.get("fields", [])),
                "extends": fmt.get("extends"),
                "description": fmt.get("description", {}).get("de", ""),
                "languages": fmt.get("languages", ["de"])
            })
    
    return {
        "status": "🔥 FORMATE GELADEN",
        "count": len(formats),
        "available_domains": format_crud.get_all_domains(),
        "formats": formats
    }


@router.get("/{format_name}")
async def get_format(
    format_name: str,
    language: str = Query("de", description="Sprache für Feld-Beschreibungen"),
    resolve_inheritance: bool = Query(True, description="Vererbung auflösen?")
):
    """
    📖 FORMAT DETAILS
    
    Mit aufgelöster Vererbung (wenn extends gesetzt).
    """
    if resolve_inheritance:
        fmt = format_crud.get_with_inheritance(format_name)
    else:
        fmt = format_crud.get(format_name)
    
    if not fmt:
        raise HTTPException(status_code=404, detail=f"Format '{format_name}' nicht gefunden")
    
    # Feld-Details für gewählte Sprache aufbereiten
    fields_detailed = []
    for f in fmt.get("fields", []):
        fields_detailed.append({
            "name": f["name"],
            "type": f.get("type", "text"),
            "header": f.get("headers", {}).get(language, [f["name"].upper()])[0] if f.get("headers", {}).get(language) else f["name"].upper(),
            "description": f.get("description", {}).get(language, ""),
            "weight": f.get("weight", 10),
            "keywords": f.get("keywords", {}).get(language, [])
        })
    
    return {
        "status": "🔥 FORMAT GELADEN",
        "format": {
            "name": format_name,
            "domain": fmt.get("domain"),
            "extends": fmt.get("extends"),
            "description": fmt.get("description", {}),
            "languages": fmt.get("languages", ["de"]),
            "wrapper": fmt.get("wrapper"),
            "fields": fields_detailed,
            "_inherited_from": fmt.get("_inherited_from")
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  ✏️ CREATE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("")
async def create_format(data: FormatCreate):
    """
    ✏️ VOLLSTÄNDIGES FORMAT ERSTELLEN
    
    Mit allen Feld-Definitionen.
    """
    format_data = {
        "name": data.name,
        "domain": data.domain,
        "extends": data.extends,
        "description": data.description,
        "wrapper": data.wrapper,
        "fields": [f.model_dump() for f in data.fields]
    }
    
    success, message, result = format_crud.create(format_data)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "✨ FORMAT GEBOREN",
        "message": message,
        "format": result
    }


@router.post("/quick")
async def create_format_quick(data: FormatQuickCreate):
    """
    ⚡ SCHNELL-ERSTELLUNG
    
    Nur Name und Feldnamen - Rest wird mit Defaults gefüllt.
    """
    format_data = {
        "name": data.name,
        "domain": data.domain,
        "description": {"de": data.description_de, "en": ""},
        "wrapper": data.wrapper,
        "fields": [{"name": fn} for fn in data.field_names]
    }
    
    success, message, result = format_crud.create(format_data)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "⚡ FORMAT SCHNELL ERSTELLT",
        "message": message,
        "format": {
            "name": data.name,
            "fields": data.field_names,
            "path": f"/opt/syntx-config/formats/{data.name}.json"
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🔄 UPDATE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/{format_name}")
async def update_format(format_name: str, data: FormatUpdate):
    """
    🔄 FORMAT UPDATEN
    
    Nur die übergebenen Felder werden geändert.
    """
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    
    if not updates:
        raise HTTPException(status_code=400, detail="Keine Updates übergeben")
    
    success, message, result = format_crud.update(format_name, updates)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "🔄 FORMAT AKTUALISIERT",
        "message": message,
        "format": result
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  💀 DELETE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/{format_name}")
async def delete_format(format_name: str):
    """
    💀 FORMAT LÖSCHEN (Soft Delete)
    
    Wird als .deleted gespeichert, kann wiederhergestellt werden.
    """
    success, message = format_crud.delete(format_name)
    
    if not success:
        raise HTTPException(status_code=404, detail=message)
    
    return {
        "status": "💀 FORMAT FREIGEGEBEN",
        "message": message
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 FELD CRUD ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/{format_name}/fields")
async def add_field(format_name: str, field: FieldCreate):
    """
    ➕ FELD HINZUFÜGEN
    """
    success, message, result = format_crud.add_field(format_name, field.model_dump())
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "➕ FELD HINZUGEFÜGT",
        "message": message,
        "fields_count": len(result.get("fields", []))
    }


@router.put("/{format_name}/fields/{field_name}")
async def update_field(format_name: str, field_name: str, updates: FieldUpdate):
    """
    🔄 FELD UPDATEN
    """
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="Keine Updates übergeben")
    
    success, message, result = format_crud.update_field(format_name, field_name, update_data)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "🔄 FELD AKTUALISIERT",
        "message": message
    }


@router.delete("/{format_name}/fields/{field_name}")
async def remove_field(format_name: str, field_name: str):
    """
    ➖ FELD ENTFERNEN
    """
    success, message, result = format_crud.remove_field(format_name, field_name)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "➖ FELD ENTFERNT",
        "message": message,
        "fields_count": len(result.get("fields", []))
    }
