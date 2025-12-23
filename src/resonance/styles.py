"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    🎨 STYLE RESONANCE ROUTER - Vollständiger CRUD                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

from .crud import style_crud

router = APIRouter(prefix="/resonanz/styles", tags=["🎨 Styles"])

class StyleCreate(BaseModel):
    name: str
    vibe: str = ""
    description: str = ""
    tone_injection: str = ""
    word_alchemy: Dict[str, str] = {}
    forbidden_words: List[str] = []
    suffix: str = ""


class StyleUpdate(BaseModel):
    """Für PUT - alle Felder optional"""
    vibe: Optional[str] = None
    description: Optional[str] = None
    tone_injection: Optional[str] = None
    suffix: Optional[str] = None

class TransmutationAdd(BaseModel):
    original: str
    replacement: str

@router.get("")
async def list_styles():
    """🎨 ALLE STYLES"""
    names = style_crud.list_all()
    styles = []
    for n in names:
        s = style_crud.get(n)
        if s:
            styles.append({
                "name": n, "vibe": s.get("vibe", ""),
                "description": s.get("description", ""),
                "word_alchemy_count": len(s.get("word_alchemy", {})),
                "forbidden_words": s.get("forbidden_words", []),
                "has_suffix": bool(s.get("suffix")),
                "has_tone_injection": bool(s.get("tone_injection"))
            })
    return {"status": "🎨 GRIMOIRE GEÖFFNET", "count": len(styles), "styles": styles}

@router.get("/{style_name}")
async def get_style(style_name: str):
    """🔮 STYLE DETAILS"""
    style = style_crud.get(style_name)
    if not style:
        raise HTTPException(status_code=404, detail=f"Style '{style_name}' nicht gefunden")
    return {"status": "🔮 STYLE BESCHWOREN", "style": style}

@router.post("")
async def create_style(data: StyleCreate):
    """✨ STYLE ERSTELLEN"""
    success, msg, result = style_crud.create(data.model_dump())
    if not success: raise HTTPException(status_code=400, detail=msg)
    return {"status": "✨ STYLE GEBOREN", "message": msg, "style": result}

@router.put("/{style_name}")
async def update_style(style_name: str, data: StyleUpdate):
    """🔄 STYLE UPDATEN"""
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    success, msg, result = style_crud.update(style_name, updates)
    if not success: raise HTTPException(status_code=400, detail=msg)
    return {"status": "🔄 STYLE AKTUALISIERT", "message": msg}

@router.delete("/{style_name}")
async def delete_style(style_name: str):
    """💀 STYLE LÖSCHEN"""
    success, msg = style_crud.delete(style_name)
    if not success: raise HTTPException(status_code=404, detail=msg)
    return {"status": "💀 STYLE FREIGEGEBEN", "message": msg}

@router.post("/{style_name}/alchemy")
async def add_transmutation(style_name: str, data: TransmutationAdd):
    """⚗️ TRANSMUTATION HINZUFÜGEN"""
    success, msg = style_crud.add_transmutation(style_name, data.original, data.replacement)
    if not success: raise HTTPException(status_code=400, detail=msg)
    return {"status": "⚗️ TRANSMUTATION HINZUGEFÜGT", "message": msg}

@router.delete("/{style_name}/alchemy/{original}")
async def remove_transmutation(style_name: str, original: str):
    """⚗️ TRANSMUTATION ENTFERNEN"""
    success, msg = style_crud.remove_transmutation(style_name, original)
    if not success: raise HTTPException(status_code=400, detail=msg)
    return {"status": "⚗️ TRANSMUTATION ENTFERNT", "message": msg}

@router.post("/{style_name}/forbidden/{word}")
async def add_forbidden(style_name: str, word: str):
    """🚫 WORT VERBANNEN"""
    success, msg = style_crud.add_forbidden(style_name, word)
    if not success: raise HTTPException(status_code=400, detail=msg)
    return {"status": "🚫 WORT VERBANNT", "message": msg}
