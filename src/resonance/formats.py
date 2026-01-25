"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    📄 FORMAT RESONANCE ROUTER - SYNTX CHARLOTTENBURG EDITION                ║
║                                                                              ║
║    YO Bruder, hier verwalten wir die Format-Definitionen!                  ║
║    Format = wie die Daten strukturiert sein müssen (Felder, Typen, etc.)   ║
║                                                                              ║
║    Das ist wie Bauplan für Dokumente - jedes Format hat seine Felder!      ║
║                                                                              ║
║    GET    /formats              → Alle Formate listen (filterable)          ║
║    GET    /formats/{name}       → Ein Format laden (mit Vererbung)          ║
║    POST   /formats              → Neues Format erstellen (komplett)         ║
║    POST   /formats/quick        → Schnell-Erstellung (nur das Wichtigste)  ║
║    PUT    /formats/{name}       → Format updaten                            ║
║    DELETE /formats/{name}       → Format löschen (Soft Delete)             ║
║                                                                              ║
║    POST   /formats/{name}/fields           → Feld hinzufügen                ║
║    PUT    /formats/{name}/fields/{field}   → Feld updaten                  ║
║    DELETE /formats/{name}/fields/{field}   → Feld entfernen                ║
║                                                                              ║
║    Author: SYNTX Team (Ottavio + Claude)                                    ║
║    Date: 2026-01-25                                                         ║
║    Version: 3.0-charlottenburg-error-handling                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import json
from pathlib import Path
from datetime import datetime

from .crud import format_crud

router = APIRouter(prefix="/resonanz/formats", tags=["📄 Formats"])
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
#  📋 PYDANTIC MODELS - Die Datenstrukturen
# ═══════════════════════════════════════════════════════════════════════════════

class FieldCreate(BaseModel):
    """
    Einzelnes Feld für Format erstellen
    
    Ein Feld ist wie eine Spalte in Excel - hat Name, Typ, Gewichtung!
    """
    name: str = Field(..., description="Feld-Name (lowercase, underscore)")
    type: str = Field(default="text", description="text, list, rating, keywords")
    weight: int = Field(default=10, ge=0, le=100, description="Wie wichtig ist dieses Feld? 0-100")
    description: Optional[Dict[str, str]] = Field(default={"de": "", "en": ""}, description="Beschreibung in verschiedenen Sprachen")


class FieldUpdate(BaseModel):
    """
    Feld updaten - nur die angegebenen Felder werden geändert!
    """
    type: Optional[str] = None
    weight: Optional[int] = None
    description: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, List[str]]] = None
    keywords: Optional[Dict[str, List[str]]] = None


class FormatCreate(BaseModel):
    """
    Vollständiges Format erstellen mit allen Details
    
    Das ist wie komplettes Formular ausfüllen - alles angeben!
    """
    name: str = Field(..., description="Format-Name (z.B. 'sigma', 'syntx_true_raw')")
    domain: Optional[str] = Field(default=None, description="Domain wie 'technical', 'psychology', 'analysis'")
    extends: Optional[str] = Field(default=None, description="Parent-Format für Vererbung (erbt dann dessen Felder)")
    description: Optional[Dict[str, str]] = Field(default={"de": "", "en": ""}, description="Was ist das für ein Format?")
    wrapper: Optional[str] = Field(default=None, description="Empfohlener Wrapper (z.B. 'mistral_deep_analysis')")
    fields: List[FieldCreate] = Field(..., min_length=1, description="Mindestens 1 Feld muss angegeben werden!")


class FormatQuickCreate(BaseModel):
    """
    Schnell-Erstellung - nur das Nötigste angeben!
    
    Wie Express-Formular - Name + Felder reichen, Rest wird mit Defaults gefüllt.
    """
    name: str
    description_de: str = ""
    field_names: List[str] = Field(..., min_length=1, description="Liste der Feldnamen")
    domain: Optional[str] = None
    wrapper: Optional[str] = None


class FormatUpdate(BaseModel):
    """
    Format updaten - nur angegebene Felder werden geändert!
    """
    domain: Optional[str] = None
    extends: Optional[str] = None
    description: Optional[Dict[str, str]] = None
    wrapper: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 READ ENDPOINTS - Formate lesen
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("")
async def list_formats(
    domain: Optional[str] = Query(None, description="Filter nach Domain (z.B. 'technical')")
):
    """
    📋 ALLE FORMATE AUFLISTEN
    
    Das ist wie ins Telefonbuch gucken - zeigt alle Formate die wir haben!
    Optional kann man nach Domain filtern (z.B. nur 'technical' Formate).
    
    Args:
        domain: Optional filter nach Domain
    
    Returns:
        Liste aller Formate mit Basis-Infos (Name, Domain, Anzahl Felder, etc.)
    
    Errors:
        500: Wenn Format-Directory nicht lesbar ist
    """
    try:
        # Hole Format-Namen (gefiltert oder alle)
        if domain:
            logger.debug(f"Liste Formate für Domain: {domain}")
            format_namen = format_crud.list_by_domain(domain)
        else:
            logger.debug("Liste alle Formate")
            format_namen = format_crud.list_all()
        
        # Lade Details für jedes Format
        formate = []
        for name in format_namen:
            try:
                fmt = format_crud.get(name)
                if fmt:
                    formate.append({
                        "name": name,
                        "domain": fmt.get("domain"),
                        "fields_count": len(fmt.get("fields", [])),
                        "extends": fmt.get("extends"),
                        "description": fmt.get("description", {}).get("de", ""),
                        "languages": fmt.get("languages", ["de"])
                    })
            except Exception as e:
                # Einzelnes Format kaputt? Skippen, nicht komplette Liste crashen!
                logger.warning(f"⚠️ Format '{name}' konnte nicht geladen werden: {e}")
                continue
        
        logger.info(f"✅ {len(formate)} Formate geladen")
        
        return {
            "status": "🔥 FORMATE GELADEN",
            "count": len(formate),
            "available_domains": format_crud.get_all_domains(),
            "formats": formate
        }
        
    except Exception as e:
        logger.error(f"🔴 Fehler beim Formate-Listen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Formate nicht laden: {str(e)}"
        )


@router.get("/{format_name}")
async def get_format(
    format_name: str,
    language: str = Query("de", description="Sprache für Feld-Beschreibungen"),
    resolve_inheritance: bool = Query(True, description="Vererbung auflösen? (wenn Format von anderem erbt)")
):
    """
    📖 FORMAT DETAILS LADEN
    
    Lädt ein spezifisches Format mit allen Details!
    Wie Akte rausholen - zeigt alles was drin ist.
    
    Vererbung = Format kann von anderem Format erben (dann kriegt's dessen Felder)
    z.B. 'sigma_extended' erbt von 'sigma' → hat automatisch alle sigma-Felder!
    
    Args:
        format_name: Name des Formats (z.B. 'sigma')
        language: Sprache für Beschreibungen ('de' oder 'en')
        resolve_inheritance: Soll Vererbung aufgelöst werden?
    
    Returns:
        Komplettes Format mit allen Feldern und Details
    
    Errors:
        404: Format existiert nicht
        500: Format ist corrupt oder nicht lesbar
    """
    try:
        # Lade Format (mit oder ohne Vererbung)
        if resolve_inheritance:
            logger.debug(f"Lade Format '{format_name}' mit Vererbung")
            fmt = format_crud.get_with_inheritance(format_name)
        else:
            logger.debug(f"Lade Format '{format_name}' ohne Vererbung")
            fmt = format_crud.get(format_name)
        
        # Check ob Format existiert
        if not fmt:
            logger.warning(f"⚠️ Format '{format_name}' nicht gefunden")
            raise HTTPException(
                status_code=404, 
                detail=f"Format '{format_name}' existiert nicht Bruder!"
            )
        
        # Feld-Details für gewählte Sprache aufbereiten
        felder_details = []
        for feld in fmt.get("fields", []):
            try:
                felder_details.append({
                    "name": feld["name"],
                    "type": feld.get("type", "text"),
                    "header": feld.get("headers", {}).get(language, [feld["name"].upper()])[0] 
                             if feld.get("headers", {}).get(language) 
                             else feld["name"].upper(),
                    "description": feld.get("description", {}).get(language, ""),
                    "weight": feld.get("weight", 10),
                    "keywords": feld.get("keywords", {}).get(language, [])
                })
            except Exception as e:
                # Einzelnes Feld kaputt? Warning loggen, aber weiter machen
                logger.warning(f"⚠️ Feld '{feld.get('name', 'unknown')}' hat Fehler: {e}")
                continue
        
        logger.info(f"✅ Format '{format_name}' geladen mit {len(felder_details)} Feldern")
        
        return {
            "status": "🔥 FORMAT GELADEN",
            "format": {
                "name": format_name,
                "domain": fmt.get("domain"),
                "extends": fmt.get("extends"),
                "description": fmt.get("description", {}),
                "languages": fmt.get("languages", ["de"]),
                "wrapper": fmt.get("wrapper"),
                "fields": felder_details,
                "_inherited_from": fmt.get("_inherited_from")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Format-Laden '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Format nicht laden: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  ✏️ CREATE ENDPOINTS - Neue Formate erstellen
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("")
async def create_format(data: FormatCreate):
    """
    ✏️ VOLLSTÄNDIGES FORMAT ERSTELLEN
    
    Das ist wie neues Formular-Template erstellen!
    Alles wird angegeben - Name, Domain, alle Felder mit Details.
    
    Args:
        data: Komplette Format-Definition
    
    Returns:
        Bestätigung mit erstelltem Format
    
    Errors:
        400: Format existiert schon oder Validation failed
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Erstelle Format '{data.name}' mit {len(data.fields)} Feldern")
        
        # Baue Format-Datenstruktur
        format_daten = {
            "name": data.name,
            "domain": data.domain,
            "extends": data.extends,
            "description": data.description,
            "wrapper": data.wrapper,
            "fields": [feld.model_dump() for feld in data.fields]
        }
        
        # Erstellen via CRUD
        erfolg, nachricht, resultat = format_crud.create(format_daten)
        
        if not erfolg:
            logger.warning(f"⚠️ Format-Erstellung failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"✅ Format '{data.name}' erfolgreich erstellt!")
        
        return {
            "status": "✨ FORMAT GEBOREN",
            "message": nachricht,
            "format": resultat
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Format-Erstellen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Format nicht erstellen: {str(e)}"
        )


@router.post("/quick")
async def create_format_quick(data: FormatQuickCreate):
    """
    ⚡ SCHNELL-ERSTELLUNG - Nur das Nötigste!
    
    Das ist Express-Mode - nur Name und Feldnamen angeben!
    Rest wird mit sinnvollen Defaults gefüllt.
    Wie Express-Checkout - schnell durchklicken statt alles ausfüllen!
    
    Args:
        data: Minimale Format-Info (Name + Feldnamen reichen)
    
    Returns:
        Bestätigung mit erstelltem Format
    
    Errors:
        400: Format existiert schon oder invalid
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Quick-Erstelle Format '{data.name}' mit {len(data.field_names)} Feldern")
        
        # Baue Format mit Defaults
        format_daten = {
            "name": data.name,
            "domain": data.domain,
            "description": {"de": data.description_de, "en": ""},
            "wrapper": data.wrapper,
            "fields": [{"name": feldname} for feldname in data.field_names]
        }
        
        # Erstellen via CRUD
        erfolg, nachricht, resultat = format_crud.create(format_daten)
        
        if not erfolg:
            logger.warning(f"⚠️ Quick-Format-Erstellung failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"⚡ Format '{data.name}' quick-erstellt!")
        
        return {
            "status": "⚡ FORMAT SCHNELL ERSTELLT",
            "message": nachricht,
            "format": {
                "name": data.name,
                "fields": data.field_names,
                "path": f"/opt/syntx-config/formats/{data.name}.json"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Quick-Format-Erstellen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Format nicht quick-erstellen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🔄 UPDATE ENDPOINTS - Formate ändern
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/{format_name}")
async def update_format(format_name: str, data: FormatUpdate):
    """
    🔄 FORMAT UPDATEN
    
    Ändert einzelne Eigenschaften vom Format!
    Wie Formular-Korrektur - nur die Fehler ausbessern, Rest bleibt.
    
    Args:
        format_name: Format zum Updaten
        data: Nur die Felder die geändert werden sollen
    
    Returns:
        Bestätigung mit geupdatetem Format
    
    Errors:
        404: Format existiert nicht
        400: Validation failed oder keine Updates
        500: Speichern fehlgeschlagen
    """
    try:
        # Nur Felder die gesetzt sind (nicht None)
        updates = {key: value for key, value in data.model_dump().items() if value is not None}
        
        if not updates:
            raise HTTPException(
                status_code=400, 
                detail="Keine Updates übergeben Bruder! Was soll ich denn updaten?"
            )
        
        logger.info(f"Update Format '{format_name}': {list(updates.keys())}")
        
        # Update via CRUD
        erfolg, nachricht, resultat = format_crud.update(format_name, updates)
        
        if not erfolg:
            logger.warning(f"⚠️ Format-Update failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"✅ Format '{format_name}' updated!")
        
        return {
            "status": "🔄 FORMAT AKTUALISIERT",
            "message": nachricht,
            "format": resultat
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Format-Update '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Format nicht updaten: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  💀 DELETE ENDPOINTS - Format löschen
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/{format_name}")
async def delete_format(format_name: str):
    """
    💀 FORMAT LÖSCHEN (Soft Delete + Mapping Cleanup)
    
    Löscht Format ABER nicht wirklich - wird nur umbenannt zu .deleted!
    WICHTIG: Cleaned auch alle Mappings die auf dieses Format zeigen!
    
    Das ist wie Wohnung kündigen - nicht nur Schlüssel abgeben,
    sondern auch Name aus dem Klingelschild nehmen!
    
    Args:
        format_name: Format zum Löschen
    
    Returns:
        Bestätigung mit Info über gelöschte Mappings
    
    Errors:
        404: Format existiert nicht
        500: Löschen fehlgeschlagen
    """
    try:
        logger.info(f"Lösche Format '{format_name}' (soft delete + mapping cleanup)")
        
        # 1. Soft Delete via CRUD
        erfolg, nachricht = format_crud.delete(format_name)
        
        if not erfolg:
            logger.warning(f"⚠️ Format-Löschen failed: {nachricht}")
            raise HTTPException(status_code=404, detail=nachricht)
        
        logger.info(f"💀 Format '{format_name}' gelöscht (→ .deleted)")
        
        # 2. MAPPING CLEANUP - Entferne alle Mappings die auf dieses Format zeigen!
        mapping_file = Path("/opt/syntx-config/mapping.json")
        geloeschte_mappings = []
        
        try:
            if mapping_file.exists():
                logger.debug(f"Checke mapping.json für Format '{format_name}'")
                
                # Lade mapping.json
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    mapping_daten = json.load(f)
                
                # Suche Mappings die auf dieses Format zeigen
                alle_mappings = mapping_daten.get("mappings", {})
                
                # Checke jedes Mapping ob es das gelöschte Format referenziert
                for mapping_name, mapping_config in list(alle_mappings.items()):
                    # Wenn Mapping auf gelöschtes Format zeigt → raus damit!
                    if mapping_name == format_name:
                        geloeschte_mappings.append(mapping_name)
                        del alle_mappings[mapping_name]
                        logger.info(f"🗑️  Mapping '{mapping_name}' gelöscht (Format nicht mehr da)")
                
                # Speichere updated mapping.json
                if geloeschte_mappings:
                    mapping_daten["mappings"] = alle_mappings
                    mapping_daten["updated"] = datetime.now().isoformat()
                    
                    with open(mapping_file, 'w', encoding='utf-8') as f:
                        json.dump(mapping_daten, f, indent=2, ensure_ascii=False)
                    
                    logger.info(f"✅ {len(geloeschte_mappings)} Mappings aus mapping.json entfernt!")
                else:
                    logger.debug(f"Keine Mappings für Format '{format_name}' gefunden")
            else:
                logger.debug("mapping.json existiert nicht - kein Cleanup nötig")
                
        except Exception as mapping_error:
            # Mapping-Cleanup failed? Loggen aber nicht crashen!
            # Format ist ja schon gelöscht, Mapping-Cleanup ist nur Aufräumen.
            logger.warning(f"⚠️ Mapping-Cleanup failed (Format trotzdem gelöscht): {mapping_error}")
        
        return {
            "status": "💀 FORMAT FREIGEGEBEN",
            "message": nachricht,
            "mapping_cleanup": {
                "deleted_mappings": geloeschte_mappings,
                "count": len(geloeschte_mappings)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Format-Löschen '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Format nicht löschen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 FELD CRUD ENDPOINTS - Einzelne Felder bearbeiten
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/{format_name}/fields")
async def add_field(format_name: str, field: FieldCreate):
    """
    ➕ FELD ZUM FORMAT HINZUFÜGEN
    
    Fügt neues Feld zu bestehendem Format hinzu!
    Wie neue Spalte in Excel-Tabelle einfügen.
    
    Args:
        format_name: Format zum Erweitern
        field: Neues Feld
    
    Returns:
        Bestätigung mit neuer Feldanzahl
    
    Errors:
        404: Format existiert nicht
        400: Feld existiert schon oder invalid
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Füge Feld '{field.name}' zu Format '{format_name}' hinzu")
        
        # Feld hinzufügen via CRUD
        erfolg, nachricht, resultat = format_crud.add_field(format_name, field.model_dump())
        
        if not erfolg:
            logger.warning(f"⚠️ Feld hinzufügen failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"✅ Feld '{field.name}' hinzugefügt!")
        
        return {
            "status": "➕ FELD HINZUGEFÜGT",
            "message": nachricht,
            "fields_count": len(resultat.get("fields", []))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Feld-Hinzufügen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Feld nicht hinzufügen: {str(e)}"
        )


@router.put("/{format_name}/fields/{field_name}")
async def update_field(format_name: str, field_name: str, updates: FieldUpdate):
    """
    🔄 EINZELNES FELD UPDATEN
    
    Ändert Eigenschaften von einem Feld!
    Wie Zellenformat ändern in Excel - nur diese eine Spalte.
    
    Args:
        format_name: Format das das Feld enthält
        field_name: Feld zum Updaten
        updates: Nur die Eigenschaften die geändert werden
    
    Returns:
        Bestätigung
    
    Errors:
        404: Format oder Feld existiert nicht
        400: Keine Updates oder invalid
        500: Speichern fehlgeschlagen
    """
    try:
        # Nur gesetzte Felder
        update_daten = {key: value for key, value in updates.model_dump().items() if value is not None}
        
        if not update_daten:
            raise HTTPException(
                status_code=400, 
                detail="Keine Updates übergeben!"
            )
        
        logger.info(f"Update Feld '{field_name}' in Format '{format_name}': {list(update_daten.keys())}")
        
        # Update via CRUD
        erfolg, nachricht, resultat = format_crud.update_field(format_name, field_name, update_daten)
        
        if not erfolg:
            logger.warning(f"⚠️ Feld-Update failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"✅ Feld '{field_name}' updated!")
        
        return {
            "status": "🔄 FELD AKTUALISIERT",
            "message": nachricht
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Feld-Update: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Feld nicht updaten: {str(e)}"
        )


@router.delete("/{format_name}/fields/{field_name}")
async def remove_field(format_name: str, field_name: str):
    """
    ➖ FELD AUS FORMAT ENTFERNEN
    
    Löscht ein Feld aus dem Format!
    Wie Spalte in Excel löschen - weg ist weg!
    
    Args:
        format_name: Format das das Feld enthält
        field_name: Feld zum Entfernen
    
    Returns:
        Bestätigung mit neuer Feldanzahl
    
    Errors:
        404: Format oder Feld existiert nicht
        400: Letztes Feld kann nicht gelöscht werden
        500: Speichern fehlgeschlagen
    """
    try:
        logger.info(f"Entferne Feld '{field_name}' aus Format '{format_name}'")
        
        # Entfernen via CRUD
        erfolg, nachricht, resultat = format_crud.remove_field(format_name, field_name)
        
        if not erfolg:
            logger.warning(f"⚠️ Feld-Entfernen failed: {nachricht}")
            raise HTTPException(status_code=400, detail=nachricht)
        
        logger.info(f"➖ Feld '{field_name}' entfernt!")
        
        return {
            "status": "➖ FELD ENTFERNT",
            "message": nachricht,
            "fields_count": len(resultat.get("fields", []))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Feld-Entfernen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Feld nicht entfernen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎬 ENDE - Format Router ist jetzt 100% SYNTX-Style! 💎⚡🔥
# ═══════════════════════════════════════════════════════════════════════════════
