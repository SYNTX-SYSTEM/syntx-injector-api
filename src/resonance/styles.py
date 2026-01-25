"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🎨 STYLE RESONANCE ROUTER - SYNTX CHARLOTTENBURG EDITION                 ║
║                                                                              ║
║    YO Bruder, hier verwalten wir die Writing-Styles!                       ║
║    Style = wie der Output klingen soll (Vibe, Tone, Word-Swaps)            ║
║                                                                              ║
║    Das ist wie DJ-Mischpult - jeder Style hat seinen eigenen Sound!        ║
║                                                                              ║
║    GET    /styles                → Alle Styles listen                       ║
║    GET    /styles/{name}         → Style laden                              ║
║    POST   /styles                → Neuen Style erstellen                    ║
║    PUT    /styles/{name}         → Style updaten                            ║
║    DELETE /styles/{name}         → Style löschen (Soft Delete)             ║
║                                                                              ║
║    POST   /styles/{name}/alchemy         → Wort-Transmutation hinzufügen    ║
║    DELETE /styles/{name}/alchemy/{word}  → Wort-Transmutation entfernen    ║
║    POST   /styles/{name}/forbidden/{word} → Wort verbannen                 ║
║    DELETE /styles/{name}/forbidden/{word} → Wort entbannen                 ║
║                                                                              ║
║    Author: SYNTX Team (Ottavio + Claude)                                    ║
║    Date: 2026-01-25                                                         ║
║    Version: 3.0-charlottenburg-error-handling                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import logging

from .crud import style_crud

router = APIRouter(prefix="/resonanz/styles", tags=["🎨 Styles"])
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
#  📋 PYDANTIC MODELS - Die Datenstrukturen
# ═══════════════════════════════════════════════════════════════════════════════

class StyleCreate(BaseModel):
    """
    Neuen Style erstellen - komplett!
    
    Style = wie der Text klingen soll!
    - vibe: Grundstimmung ("professional", "friendly", "technical")
    - word_alchemy: Wörter automatisch ersetzen (z.B. "good" → "excellent")
    - forbidden_words: Diese Wörter NIE benutzen
    - tone_injection: Extra Text der immer eingefügt wird
    - suffix: Text der am Ende angehängt wird
    """
    name: str = Field(..., description="Style-Name (z.B. 'syntx_raw', 'professional_business')")
    vibe: str = Field(default="", description="Grundstimmung des Styles")
    description: str = Field(default="", description="Was macht diesen Style aus?")
    tone_injection: str = Field(default="", description="Extra Instruktionen die immer eingefügt werden")
    word_alchemy: Dict[str, str] = Field(default={}, description="Wort-Ersetzungen (original → replacement)")
    forbidden_words: List[str] = Field(default=[], description="Diese Wörter NIE verwenden!")
    suffix: str = Field(default="", description="Text der am Ende angehängt wird")


class StyleUpdate(BaseModel):
    """
    Style updaten - nur angegebene Felder werden geändert!
    """
    vibe: Optional[str] = None
    description: Optional[str] = None
    tone_injection: Optional[str] = None
    suffix: Optional[str] = None


class TransmutationAdd(BaseModel):
    """
    Wort-Transmutation hinzufügen
    
    Transmutation = automatisches Wort-Ersetzen!
    z.B. "good" → "excellent", "bad" → "suboptimal"
    """
    original: str = Field(..., description="Original-Wort das ersetzt werden soll")
    replacement: str = Field(..., description="Ersatz-Wort")


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 READ ENDPOINTS - Styles lesen
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("")
async def list_styles():
    """
    🎨 ALLE STYLES AUFLISTEN
    
    Das ist wie durchs DJ-Mischpult browsen - zeigt alle verfügbaren Styles!
    Jeder Style hat seinen eigenen Vibe und Sound.
    
    Returns:
        Liste aller Styles mit Basis-Infos
    
    Errors:
        500: Style-Directory nicht lesbar
    """
    try:
        logger.debug("Liste alle Styles")
        
        # Hole alle Style-Namen
        style_namen = style_crud.list_all()
        
        # Lade Details für jeden Style
        styles = []
        for name in style_namen:
            try:
                style = style_crud.get(name)
                if style:
                    styles.append({
                        "name": name,
                        "vibe": style.get("vibe", ""),
                        "description": style.get("description", ""),
                        "word_alchemy_count": len(style.get("word_alchemy", {})),
                        "forbidden_words": style.get("forbidden_words", []),
                        "has_suffix": bool(style.get("suffix")),
                        "has_tone_injection": bool(style.get("tone_injection"))
                    })
            except Exception as e:
                # Einzelner Style kaputt? Skippen, nicht crashen!
                logger.warning(f"⚠️ Style '{name}' konnte nicht geladen werden: {e}")
                continue
        
        logger.info(f"✅ {len(styles)} Styles geladen")
        
        return {
            "status": "🎨 GRIMOIRE GEÖFFNET",
            "count": len(styles),
            "styles": styles
        }
        
    except Exception as e:
        logger.error(f"🔴 Fehler beim Styles-Listen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Styles nicht laden: {str(e)}"
        )


@router.get("/{style_name}")
async def get_style(style_name: str):
    """
    🔮 STYLE DETAILS LADEN
    
    Lädt einen spezifischen Style mit allen Details!
    Wie DJ-Preset laden - zeigt alle Einstellungen.
    
    Args:
        style_name: Name des Styles (z.B. 'syntx_raw')
    
    Returns:
        Kompletter Style mit allen Einstellungen
    
    Errors:
        404: Style existiert nicht
        500: Style ist corrupt oder nicht lesbar
    """
    try:
        logger.debug(f"Lade Style '{style_name}'")
        
        style = style_crud.get(style_name)
        
        if not style:
            logger.warning(f"⚠️ Style '{style_name}' nicht gefunden")
            raise HTTPException(
                status_code=404,
                detail=f"Style '{style_name}' existiert nicht Bruder!"
            )
        
        logger.info(f"✅ Style '{style_name}' geladen")
        
        return {
            "status": "🔮 STYLE BESCHWOREN",
            "style": style
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Style-Laden '{style_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Style nicht laden: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  ✏️ CREATE ENDPOINTS - Neuen Style erstellen
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("")
async def create_style(data: StyleCreate):
    """
    ✨ NEUEN STYLE ERSTELLEN
    
    Erstellt einen komplett neuen Writing-Style!
    Das ist wie neues DJ-Preset erstellen - alle Settings von Grund auf.
    
    Args:
        data: Komplette Style-Definition
    
    Returns:
        Bestätigung mit erstelltem Style
    
    Errors:
        400: Style existiert schon oder invalid
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Erstelle Style '{data.name}'")
        
        # Style erstellen via CRUD
        erfolg, nachricht, resultat = style_crud.create(data.model_dump())
        
        if not erfolg:
            logger.warning(f"⚠️ Style-Erstellung failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"✨ Style '{data.name}' erstellt!")
        
        return {
            "status": "✨ STYLE GEBOREN",
            "message": nachricht,
            "style": resultat
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Style-Erstellen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Style nicht erstellen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🔄 UPDATE ENDPOINTS - Style ändern
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/{style_name}")
async def update_style(style_name: str, data: StyleUpdate):
    """
    🔄 STYLE UPDATEN
    
    Ändert Eigenschaften vom Style!
    Wie DJ-Preset anpassen - nur die Settings die man ändern will.
    
    Args:
        style_name: Style zum Updaten
        data: Nur die Felder die geändert werden sollen
    
    Returns:
        Bestätigung
    
    Errors:
        404: Style existiert nicht
        400: Keine Updates oder invalid
        500: Speichern fehlgeschlagen
    """
    try:
        # Nur gesetzte Felder
        updates = {key: value for key, value in data.model_dump().items() if value is not None}
        
        if not updates:
            raise HTTPException(
                status_code=400,
                detail="Keine Updates übergeben Bruder!"
            )
        
        logger.info(f"Update Style '{style_name}': {list(updates.keys())}")
        
        # Update via CRUD
        erfolg, nachricht, resultat = style_crud.update(style_name, updates)
        
        if not erfolg:
            logger.warning(f"⚠️ Style-Update failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"✅ Style '{style_name}' updated!")
        
        return {
            "status": "🔄 STYLE AKTUALISIERT",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Style-Update '{style_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Style nicht updaten: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  💀 DELETE ENDPOINTS - Style löschen
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/{style_name}")
async def delete_style(style_name: str):
    """
    💀 STYLE LÖSCHEN (Soft Delete)
    
    Löscht Style ABER nicht wirklich - wird umbenannt zu .deleted!
    Wie Papierkorb - kann wiederhergestellt werden.
    
    Args:
        style_name: Style zum Löschen
    
    Returns:
        Bestätigung
    
    Errors:
        404: Style existiert nicht
        500: Löschen fehlgeschlagen
    """
    try:
        logger.info(f"Lösche Style '{style_name}' (soft delete)")
        
        # Soft Delete via CRUD
        erfolg, nachricht = style_crud.delete(style_name)
        
        if not erfolg:
            logger.warning(f"⚠️ Style-Löschen failed: {nachricht}")
            raise HTTPException(status_code=404, detail=nachricht)
        
        logger.info(f"💀 Style '{style_name}' gelöscht (→ .deleted)")
        
        return {
            "status": "💀 STYLE FREIGEGEBEN",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Style-Löschen '{style_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Style nicht löschen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  ⚗️ ALCHEMY ENDPOINTS - Wort-Transmutationen (automatisches Ersetzen)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/{style_name}/alchemy")
async def add_transmutation(style_name: str, data: TransmutationAdd):
    """
    ⚗️ WORT-TRANSMUTATION HINZUFÜGEN
    
    Fügt automatisches Wort-Ersetzen hinzu!
    z.B. "good" → "excellent", "bad" → "suboptimal"
    
    Das ist wie Autocorrect aber für Style - bestimmte Wörter werden automatisch ersetzt!
    
    Args:
        style_name: Style zum Erweitern
        data: Original-Wort und Replacement
    
    Returns:
        Bestätigung
    
    Errors:
        404: Style existiert nicht
        400: Transmutation existiert schon oder invalid
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Füge Transmutation '{data.original}' → '{data.replacement}' zu Style '{style_name}' hinzu")
        
        # Transmutation hinzufügen via CRUD
        erfolg, nachricht = style_crud.add_transmutation(style_name, data.original, data.replacement)
        
        if not erfolg:
            logger.warning(f"⚠️ Transmutation hinzufügen failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"⚗️ Transmutation '{data.original}' → '{data.replacement}' hinzugefügt!")
        
        return {
            "status": "⚗️ TRANSMUTATION HINZUGEFÜGT",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Transmutation-Hinzufügen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Transmutation nicht hinzufügen: {str(e)}"
        )


@router.delete("/{style_name}/alchemy/{original}")
async def remove_transmutation(style_name: str, original: str):
    """
    ⚗️ WORT-TRANSMUTATION ENTFERNEN
    
    Entfernt eine Wort-Ersetzung!
    z.B. "good" wird nicht mehr automatisch zu "excellent"
    
    Args:
        style_name: Style zum Bearbeiten
        original: Original-Wort dessen Ersetzung entfernt werden soll
    
    Returns:
        Bestätigung
    
    Errors:
        404: Style oder Transmutation existiert nicht
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Entferne Transmutation '{original}' aus Style '{style_name}'")
        
        # Transmutation entfernen via CRUD
        erfolg, nachricht = style_crud.remove_transmutation(style_name, original)
        
        if not erfolg:
            logger.warning(f"⚠️ Transmutation entfernen failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"⚗️ Transmutation '{original}' entfernt!")
        
        return {
            "status": "⚗️ TRANSMUTATION ENTFERNT",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Transmutation-Entfernen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Transmutation nicht entfernen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🚫 FORBIDDEN WORDS ENDPOINTS - Wörter verbannen
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/{style_name}/forbidden/{word}")
async def add_forbidden(style_name: str, word: str):
    """
    🚫 WORT VERBANNEN
    
    Fügt Wort zur Blacklist hinzu - darf nie verwendet werden!
    Wie Türsteher - bestimmte Wörter kommen nicht rein!
    
    Args:
        style_name: Style zum Bearbeiten
        word: Wort das verbannt werden soll
    
    Returns:
        Bestätigung
    
    Errors:
        404: Style existiert nicht
        400: Wort ist schon verbannt
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Verbanne Wort '{word}' in Style '{style_name}'")
        
        # Wort verbannen via CRUD
        erfolg, nachricht = style_crud.add_forbidden(style_name, word)
        
        if not erfolg:
            logger.warning(f"⚠️ Wort-Verbannen failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"🚫 Wort '{word}' verbannt!")
        
        return {
            "status": "🚫 WORT VERBANNT",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Wort-Verbannen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Wort nicht verbannen: {str(e)}"
        )


@router.delete("/{style_name}/forbidden/{word}")
async def remove_forbidden(style_name: str, word: str):
    """
    🔓 WORT ENTBANNEN
    
    Entfernt Wort von der Blacklist - darf wieder verwendet werden!
    Wie Türsteher - Wort kommt wieder rein!
    
    Args:
        style_name: Style zum Bearbeiten
        word: Wort das entbannt werden soll
    
    Returns:
        Bestätigung
    
    Errors:
        404: Style existiert nicht oder Wort ist nicht verbannt
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Entbanne Wort '{word}' in Style '{style_name}'")
        
        # Wort entbannen via CRUD
        erfolg, nachricht = style_crud.remove_forbidden(style_name, word)
        
        if not erfolg:
            logger.warning(f"⚠️ Wort-Entbannen failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"🔓 Wort '{word}' entbannt!")
        
        return {
            "status": "🔓 WORT ENTBANNT",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Wort-Entbannen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Wort nicht entbannen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎬 ENDE - Style Router ist jetzt 100% SYNTX-Style! 💎⚡🔥
# ═══════════════════════════════════════════════════════════════════════════════
