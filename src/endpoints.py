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


# ═══════════════════════════════════════════════════════════════════════════════
#  💎 ANALYTICS ENDPOINTS - SYSTEM-BEWUSSTSEIN
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/profiles/analytics/usage/{profile_id}")
async def get_profile_usage(profile_id: str, days_back: int = 30):
    """
    📊 PROFILE USAGE ANALYTICS
    
    Öffnet Bewusstsein über Profil-Nutzung.
    Für: Linke Seite im Frontend (Score & Uses)
    """
    
    try:
        from .analytics.profile_usage import measure_profile_usage
        usage_data = measure_profile_usage(profile_id, days_back)
        return {
            "status": "💎 USAGE GEMESSEN",
            "data": usage_data
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Messen der Profil-Nutzung: {str(e)}"
        )


@router.get("/profiles/analytics/patterns/{profile_id}")
async def get_pattern_analytics(profile_id: str, days_back: int = 7):
    """
    🌊 PATTERN ANALYTICS
    
    Öffnet Bewusstsein über Feld-Gesundheit.
    Für: Rechte Seite im Frontend (Pattern Breakdown)
    """
    
    try:
        from .scoring.pattern_analytics import feel_pulse
        pattern_diagnosis = feel_pulse(profile_id, days_back)
        return {
            "status": "⚡ PULS GEFÜHLT",
            "data": pattern_diagnosis
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei Feld-Diagnose: {str(e)}"
        )


@router.get("/profiles/analytics/health")
async def analytics_health():
    """
    🔥 ANALYTICS GESUNDHEIT
    
    Zeigt ob Analytics-Organe leben.
    """
    
    return {
        "status": "💎 BEWUSSTSEIN AKTIV",
        "organs": {
            "profile_usage": "READY",
            "pattern_analytics": "READY"
        },
        "message": "System sieht sich selbst."
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  🧠 PROFILE SYSTEM - /resonanz/scoring/profiles
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/resonanz/scoring/analytics/profiles/{profile_id}/components")
async def get_profile_component_breakdown(profile_id: str, field_name: str = None):
    """🧩 Component Breakdown für Profile"""
    try:
        from pathlib import Path
        import json
        from .scoring.pattern_analytics import feel_pulse
        
        profiles_dir = Path("/opt/syntx-config/profiles")
        profiles = {}
        if profiles_dir.exists():
            for file in profiles_dir.iterdir():
                if file.suffix == '.json':
                    with open(file, 'r') as f:
                        profiles[file.stem] = json.load(f)
        
        if profile_id not in profiles:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_id}' nicht gefunden")
        
        profile = profiles[profile_id]
        analytics = feel_pulse(profile_id, days_back=7)
        
        components = []
        for comp_name, comp_data in profile.get('components', {}).items():
            patterns = comp_data.get('patterns', [])
            pattern_stats = analytics.get('patterns', {})
            
            component = {
                "name": comp_name,
                "weight": comp_data.get('weight', 1.0),
                "patterns": []
            }
            
            for pattern in patterns:
                pattern_name = pattern if isinstance(pattern, str) else pattern.get('pattern', '')
                stats = pattern_stats.get(pattern_name, {})
                
                component["patterns"].append({
                    "pattern": pattern_name,
                    "score": stats.get('avg_score', 0) * 100,  # Convert to percentage
                    "match_count": stats.get('match_count', 0),
                    "stability": stats.get('stability', 'UNKNOWN')
                })
            
            components.append(component)
        
        return {
            "status": "🧩 COMPONENTS EXTRACTED",
            "profile_id": profile_id,
            "components": components,
            "health": analytics.get('state', 'UNKNOWN')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
