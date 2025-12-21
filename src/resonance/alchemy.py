"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ⚗️ SYNTX ALCHEMY PREVIEW - LIVE WORT-TRANSMUTATION                       ║
║                                                                              ║
║    Zeigt LIVE wie der Style-Alchemist Wörter verwandelt.                    ║
║    Mit Position-Mapping für Frontend-Highlighting.                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import json
import re

router = APIRouter(prefix="/resonanz", tags=["resonance-alchemy"])

STYLES_DIR = Path("/opt/syntx-config/styles")


class AlchemyPreviewRequest(BaseModel):
    """Alchemy Preview Request"""
    text: str
    style: str


class Transformation(BaseModel):
    """Eine einzelne Wort-Transmutation"""
    original: str
    replacement: str
    start_pos: int
    end_pos: int
    type: str  # "alchemy" oder "forbidden"


class AlchemyPreviewResponse(BaseModel):
    """Alchemy Preview mit allen Transformationen"""
    original: str
    transformed: str
    style: str
    transformations: List[Transformation]
    stats: dict


@router.post("/alchemy/preview", response_model=AlchemyPreviewResponse)
async def preview_alchemy(request: AlchemyPreviewRequest):
    """
    ⚗️ ALCHEMY PREVIEW
    
    Zeigt live wie ein Text durch den Style transmutiert wird.
    Gibt Position-Mapping für Frontend-Highlighting zurück.
    """
    style = _load_style(request.style)
    if not style:
        raise HTTPException(
            status_code=404,
            detail=f"Style '{request.style}' nicht im Grimoire"
        )
    
    text = request.text
    transformations = []
    
    # 1. WORD ALCHEMY - Wörter ersetzen
    word_alchemy = style.get("word_alchemy", {})
    transformed = text
    offset = 0  # Track position changes
    
    for original, replacement in word_alchemy.items():
        # Finde alle Vorkommen (case-insensitive)
        pattern = re.compile(re.escape(original), re.IGNORECASE)
        
        for match in pattern.finditer(text):
            start = match.start()
            end = match.end()
            
            transformations.append(Transformation(
                original=match.group(),
                replacement=replacement,
                start_pos=start,
                end_pos=end,
                type="alchemy"
            ))
    
    # Jetzt tatsächlich ersetzen (von hinten nach vorne für korrekte Positionen)
    for original, replacement in word_alchemy.items():
        transformed = re.sub(
            re.escape(original), 
            replacement, 
            transformed, 
            flags=re.IGNORECASE
        )
    
    # 2. FORBIDDEN WORDS - Wörter entfernen
    forbidden = style.get("forbidden_words", [])
    
    for word in forbidden:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        
        for match in pattern.finditer(text):
            transformations.append(Transformation(
                original=match.group(),
                replacement="[ENTFERNT]",
                start_pos=match.start(),
                end_pos=match.end(),
                type="forbidden"
            ))
        
        # Entferne aus transformed
        transformed = re.sub(
            r'\s*' + re.escape(word) + r'\s*',
            ' ',
            transformed,
            flags=re.IGNORECASE
        ).strip()
    
    # 3. SUFFIX hinzufügen
    suffix = style.get("suffix", "")
    if suffix:
        transformed = transformed.rstrip() + " " + suffix
    
    # Sortiere Transformationen nach Position
    transformations.sort(key=lambda x: x.start_pos)
    
    # Stats
    stats = {
        "alchemy_count": len([t for t in transformations if t.type == "alchemy"]),
        "forbidden_count": len([t for t in transformations if t.type == "forbidden"]),
        "original_length": len(text),
        "transformed_length": len(transformed),
        "has_suffix": bool(suffix),
        "has_tone_injection": bool(style.get("tone_injection"))
    }
    
    return AlchemyPreviewResponse(
        original=request.text,
        transformed=transformed,
        style=request.style,
        transformations=transformations,
        stats=stats
    )


@router.get("/alchemy/styles")
async def list_alchemy_styles():
    """
    📋 ALLE STYLES MIT ALCHEMY-INFO
    
    Zeigt welche Styles welche Transmutationen haben.
    """
    if not STYLES_DIR.exists():
        return {"styles": []}
    
    styles = []
    
    for style_file in STYLES_DIR.glob("*.json"):
        try:
            style = json.loads(style_file.read_text(encoding='utf-8'))
            styles.append({
                "name": style_file.stem,
                "vibe": style.get("vibe", ""),
                "alchemy_count": len(style.get("word_alchemy", {})),
                "forbidden_count": len(style.get("forbidden_words", [])),
                "has_suffix": bool(style.get("suffix")),
                "has_tone": bool(style.get("tone_injection"))
            })
        except:
            continue
    
    return {
        "status": "⚗️ GRIMOIRE GEÖFFNET",
        "count": len(styles),
        "styles": styles
    }


def _load_style(name: str) -> Optional[dict]:
    """Lädt einen Style aus dem Grimoire"""
    style_path = STYLES_DIR / f"{name}.json"
    
    if not style_path.exists():
        return None
    
    try:
        return json.loads(style_path.read_text(encoding='utf-8'))
    except:
        return None
