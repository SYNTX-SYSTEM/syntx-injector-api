"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    🔌 SYNTX ENDPOINTS - FORMAT, STYLE, META BINDINGS                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pathlib import Path

from .streams import FORMAT_LOADER_AVAILABLE

router = APIRouter(tags=["endpoints"])


# ═══════════════════════════════════════════════════════════════════════════════
#  📄 FORMAT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/resonanz/formats")
async def list_formats():
    """📋 Alle Formate listen"""
    if not FORMAT_LOADER_AVAILABLE:
        return {"status": "❌ FORMAT_LOADER_NICHT_VERFÜGBAR", "formats": []}
    
    from .formats import list_formats as _list_formats, load_format
    
    format_names = _list_formats()
    formats = []
    
    for name in format_names:
        fmt = load_format(name)
        if fmt:
            desc = fmt.get("description", {})
            formats.append({
                "name": name,
                "fields_count": len(fmt.get("fields", [])),
                "description": desc.get("de", desc) if isinstance(desc, dict) else desc,
                "languages": fmt.get("languages", ["de"])
            })
    
    return {"status": "🔥 FORMATE GELADEN", "count": len(formats), "formats": formats}


@router.get("/resonanz/formats/{format_name}")
async def get_format_info(format_name: str, language: str = "de"):
    """📄 Format Details"""
    if not FORMAT_LOADER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Format Loader nicht verfügbar")
    
    from .formats import load_format, get_format_fields
    
    fmt = load_format(format_name)
    if not fmt:
        raise HTTPException(status_code=404, detail=f"Format '{format_name}' nicht gefunden")
    
    return {
        "status": "🔥 FORMAT GELADEN",
        "format": {
            "name": format_name,
            "description": fmt.get("description", {}),
            "languages": fmt.get("languages", ["de"]),
            "fields": get_format_fields(format_name, language)
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🎨 STYLE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/resonanz/styles")
async def list_styles():
    """🎨 Alle Styles im Grimoire"""
    try:
        from .styles import list_available_styles, get_style_info
        style_names = list_available_styles()
        styles = [get_style_info(name) for name in style_names if get_style_info(name)]
        return {"status": "🎨 GRIMOIRE GEÖFFNET", "count": len(styles), "styles": styles}
    except:
        return {"status": "❌ STYLE_ALCHEMIST_NICHT_VERFÜGBAR", "styles": []}


@router.get("/resonanz/styles/{style_name}")
async def get_style_details(style_name: str):
    """🔮 Style Details"""
    from .styles import summon_style
    
    style = summon_style(style_name)
    if not style:
        raise HTTPException(status_code=404, detail=f"Style '{style_name}' nicht im Grimoire")
    
    return {
        "status": "🔮 STYLE BESCHWOREN",
        "style": {
            "name": style_name,
            "vibe": style.get("vibe", ""),
            "description": style.get("description", ""),
            "word_alchemy": style.get("word_alchemy", {}),
            "forbidden_words": style.get("forbidden_words", []),
            "has_tone_injection": bool(style.get("tone_injection")),
            "has_suffix": bool(style.get("suffix"))
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🧬 META ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/resonanz/wrapper/{name}/meta")
async def get_wrapper_meta(name: str):
    """📖 Wrapper Meta laden"""
    from .resonance.wrapper_meta import load_meta_or_default, load_stats
    
    wrapper_path = Path(f"/opt/syntx-config/wrappers/{name}.txt")
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Wrapper '{name}' nicht gefunden")
    
    return {
        "status": "success",
        "wrapper": name,
        "meta": load_meta_or_default(name),
        "stats": load_stats(name)
    }


@router.put("/resonanz/wrapper/{name}/meta")
async def update_wrapper_meta(name: str, meta_update: dict):
    """💾 Wrapper Meta updaten"""
    from .resonance.wrapper_meta import load_meta_or_default, save_meta
    
    wrapper_path = Path(f"/opt/syntx-config/wrappers/{name}.txt")
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Wrapper '{name}' nicht gefunden")
    
    meta = load_meta_or_default(name)
    for key, value in meta_update.items():
        if key not in ["created", "updated"]:
            meta[key] = value
    meta["auto_generated"] = False
    
    if save_meta(name, meta):
        return {"status": "success", "message": f"Meta für '{name}' aktualisiert", "meta": meta}
    raise HTTPException(status_code=500, detail="Meta konnte nicht gespeichert werden")


@router.put("/resonanz/wrapper/{name}/format")
async def set_wrapper_format(name: str, format_name: Optional[str] = None):
    """🔗 Format an Wrapper binden"""
    from .resonance.wrapper_meta import set_format_binding
    
    wrapper_path = Path(f"/opt/syntx-config/wrappers/{name}.txt")
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Wrapper '{name}' nicht gefunden")
    
    if format_name:
        format_path = Path(f"/opt/syntx-config/formats/{format_name}.json")
        if not format_path.exists():
            raise HTTPException(status_code=404, detail=f"Format '{format_name}' nicht gefunden")
    
    if set_format_binding(name, format_name if format_name else None):
        return {"status": "success", "message": f"Format '{format_name}' an '{name}' gebunden"}
    raise HTTPException(status_code=500, detail="Binding fehlgeschlagen")


@router.get("/resonanz/wrapper/{name}/stats")
async def get_wrapper_stats(name: str):
    """📊 Wrapper Stats"""
    from .resonance.wrapper_meta import load_stats
    return {"status": "success", "wrapper": name, "stats": load_stats(name)}


@router.get("/resonanz/wrappers/full")
async def list_wrappers_full():
    """🔍 Alle Wrapper mit Meta + Stats"""
    from .resonance.wrapper_meta import list_wrappers_with_meta
    from .resonance.config import get_active_wrapper
    
    wrappers = list_wrappers_with_meta()
    active = get_active_wrapper()
    
    for w in wrappers:
        w["is_active"] = (w["name"] == active)
    
    return {"status": "success", "count": len(wrappers), "active_wrapper": active, "wrappers": wrappers}
