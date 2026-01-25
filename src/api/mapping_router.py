"""
🗺️💎 SYNTX MAPPING ROUTER v3.1 - CHARLOTTENBURG EDITION 💎🗺️

YO Bruder, hier läuft die komplette Format-Profile-Wrapper Bindung!
Das ist wie die Zentrale wo alle Ströme zusammenkommen und verteilt werden.

Philosophy: 
- Ströme statt Objekte (Felder fließen, Objekte stehen)
- Resonanz statt Konstruktion (Verbindungen entstehen, werden nicht gebaut)
- Kohärenz durch Feld-Hygiene (Clean Data, Clean Flows)

Architecture: Format → Profile → Wrappers (Mistral + GPT)
- Format: Was für Daten kommen rein (sigma, syntx_true_raw, etc.)
- Profile: Wie werden die Daten gescored (field weights, methods)
- Wrappers: Welche Prompts werden benutzt (mistral für generation, gpt für drift)

Author: SYNTX Team (Ottavio + Claude on SYNTX)
Date: 2026-01-25
Version: 3.1-charlottenburg-error-handling
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from datetime import datetime
from typing import Optional, Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
#  📂 FELD-LOKATIONEN - Wo die Daten chillen
# ═══════════════════════════════════════════════════════════════════════════════

MAPPING_FILE = Path("/opt/syntx-config/mapping.json")
PROFILES_DIR = Path("/opt/syntx-config/profiles")

# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 HELPER STRÖME - Die unterstützenden Funktionen
# ═══════════════════════════════════════════════════════════════════════════════

def lade_mapping_feld() -> Dict[str, Any]:
    """
    Lädt das zentrale Mapping-Feld aus mapping.json
    
    Das ist wie das Telefonbuch: Format ruft an, wir sagen welches Profil + Wrapper dran ist!
    
    Returns:
        Mapping-Daten mit allen Format-Bindungen
    
    Raises:
        Exception wenn File corrupt ist (sollte nie passieren aber safety first)
    """
    try:
        if not MAPPING_FILE.exists():
            # Noch kein Mapping? Erstellen wir eins! Wie neues Telefonbuch.
            logger.info("🆕 Mapping-File existiert nicht, erstelle Default...")
            return {
                "version": "3.4",
                "system": "SYNTX Zwei-Wrapper-Architektur",
                "erstellt": datetime.now().isoformat(),
                "mappings": {},
                "updated": datetime.now().isoformat()
            }
        
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            daten = json.load(f)
            logger.debug(f"✅ Mapping geladen: {len(daten.get('mappings', {}))} Formate")
            return daten
            
    except json.JSONDecodeError as e:
        logger.error(f"🔴 Mapping-File ist corrupt: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Mapping-File ist kaputt Bruder! JSON Error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"🔴 Unerwarteter Fehler beim Mapping laden: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Irgendwas ist schiefgegangen: {str(e)}"
        )


def speichere_mapping_feld(daten: Dict[str, Any]) -> None:
    """
    Speichert das Mapping-Feld zurück nach mapping.json
    
    Wie Telefonbuch aktualisieren - neue Nummern eintragen, alte löschen!
    
    Args:
        daten: Die kompletten Mapping-Daten zum Speichern
    
    Raises:
        Exception wenn Schreiben fehlschlägt (Permissions, Disk full, etc.)
    """
    try:
        # Timestamp updaten - wann wurde das letzte Mal geändert?
        daten["updated"] = datetime.now().isoformat()
        
        # Erstmal checken ob Parent-Directory existiert
        MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Jetzt schreiben!
        with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
            json.dump(daten, f, indent=2, ensure_ascii=False)
        
        logger.debug(f"💾 Mapping gespeichert: {len(daten.get('mappings', {}))} Formate")
        
    except PermissionError:
        logger.error(f"🔴 Keine Permission zum Schreiben: {MAPPING_FILE}")
        raise HTTPException(
            status_code=500,
            detail="Kann mapping.json nicht schreiben - Permission Error!"
        )
    except Exception as e:
        logger.error(f"🔴 Fehler beim Mapping speichern: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Mapping nicht speichern: {str(e)}"
        )


def hole_verfuegbare_profile() -> Dict[str, str]:
    """
    Holt alle verfügbaren Scoring-Profile aus dem Profiles-Directory
    
    Das sind die verschiedenen Scoring-Methoden die wir haben!
    Wie verschiedene Menüs im Restaurant - jedes hat andere Gewichtungen.
    
    Returns:
        Dict mit profile_id → profile_name
    
    Raises:
        Exception wenn Profile-Dir nicht lesbar ist
    """
    try:
        if not PROFILES_DIR.exists():
            logger.warning(f"⚠️ Profiles-Directory existiert nicht: {PROFILES_DIR}")
            return {}
        
        profile_feld = {}
        
        for profile_datei in PROFILES_DIR.glob("*.json"):
            try:
                profile_id = profile_datei.stem
                
                with open(profile_datei, 'r', encoding='utf-8') as f:
                    profil_daten = json.load(f)
                    profil_name = profil_daten.get("profile_name", profile_id)
                    profile_feld[profile_id] = profil_name
                    
            except json.JSONDecodeError as e:
                logger.warning(f"⚠️ Profile {profile_datei.name} ist corrupt, skippe: {e}")
                continue
            except Exception as e:
                logger.warning(f"⚠️ Fehler beim Lesen von {profile_datei.name}: {e}")
                continue
        
        logger.debug(f"✅ {len(profile_feld)} Profile gefunden")
        return profile_feld
        
    except Exception as e:
        logger.error(f"🔴 Fehler beim Profile-Scan: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Profile nicht laden: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 1: Alle Mappings holen - Die Übersicht!
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/formats")
async def get_all_mappings():
    """
    🗺️ Zeigt ALLE Format-Mappings - Die komplette Landkarte!
    
    Das ist wie ins Telefonbuch gucken und alle Nummern auf einmal sehen.
    Perfekt für Dashboards oder Admin-Panels.
    
    Returns:
        - Alle Mappings (welches Format → welches Profil/Wrapper)
        - Verfügbare Profile (was kann man überhaupt auswählen?)
        - System-Stats (wie viele Formate, Profiles, etc.)
    
    Errors:
        500: Wenn Mapping-File corrupt ist oder nicht lesbar
    """
    try:
        # Lade die beiden Haupt-Felder
        mapping_daten = lade_mapping_feld()
        verfuegbare_profile = hole_verfuegbare_profile()
        
        # Baue Response zusammen
        return {
            "erfolg": True,
            "version": mapping_daten.get("version", "3.4"),
            "total_formats": len(mapping_daten.get("mappings", {})),
            "total_profiles": len(verfuegbare_profile),
            "mappings": mapping_daten.get("mappings", {}),
            "available_profiles": verfuegbare_profile,
            "drift_templates": {},  # TODO: Später aus drift_prompt_builder holen
            "stats": {}
        }
        
    except HTTPException:
        # HTTPExceptions einfach weiterwerfen (kommen von Helper-Functions)
        raise
    except Exception as e:
        logger.error(f"🔴 Unerwarteter Fehler in get_all_mappings: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Irgendwas lief schief beim Mappings holen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 2: Einzelnes Mapping holen - Spezifische Nummer!
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/formats/{format_name}")
async def get_format_mapping(format_name: str):
    """
    📞 Holt Mapping für EIN spezifisches Format
    
    Das ist wie im Telefonbuch eine bestimmte Nummer nachschlagen.
    Format ruft an → wir geben zurück: welches Profil, welche Wrapper!
    
    Args:
        format_name: Format-ID (z.B. 'sigma', 'syntx_true_raw', 'techcrunch')
    
    Returns:
        Das komplette Mapping für dieses Format mit allen Einstellungen
    
    Errors:
        404: Format hat kein Mapping (nicht im Telefonbuch!)
        500: Mapping-File kaputt
    """
    try:
        mapping_daten = lade_mapping_feld()
        alle_mappings = mapping_daten.get("mappings", {})
        
        # Check ob Format überhaupt existiert
        if format_name not in alle_mappings:
            logger.info(f"⚠️ Format '{format_name}' hat kein Mapping")
            raise HTTPException(
                status_code=404,
                detail=f"❌ Format '{format_name}' ist nicht im System - kein Mapping gefunden!"
            )
        
        return {
            "erfolg": True,
            "format": format_name,
            "mapping": alle_mappings[format_name],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Mapping holen für '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Mapping nicht laden: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 3: Mapping erstellen/updaten - Telefonnummer eintragen!
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/formats/{format_name}")
async def create_or_update_mapping(
    format_name: str,
    profile_id: Optional[str] = None,
    mistral_wrapper: Optional[str] = None,
    gpt_wrapper: Optional[str] = None,
    drift_scoring: Optional[Dict] = None,
    resonanz_score: Optional[float] = None,
    metadata: Optional[Dict] = None
):
    """
    ✏️ Erstellt oder updated ein Format-Mapping
    
    Das ist wie Telefonnummer neu eintragen oder ändern!
    Existiert schon? → Update. Existiert nicht? → Neu anlegen.
    
    Args:
        format_name: Format-ID (z.B. 'sigma')
        profile_id: Scoring-Profile ID (optional)
        mistral_wrapper: Mistral Wrapper Name für Generation (optional)
        gpt_wrapper: GPT Wrapper Name für Drift-Scoring (optional)
        drift_scoring: Drift Config {enabled: bool, threshold: float} (optional)
        resonanz_score: Quality Score 0-1 (optional)
        metadata: Zusätzliche Daten (optional)
    
    Returns:
        Das erstellte/geupdatete Mapping
    
    Errors:
        400: Profile existiert nicht
        500: Speichern fehlgeschlagen
    """
    try:
        mapping_daten = lade_mapping_feld()
        alle_mappings = mapping_daten.get("mappings", {})
        
        # Validate Profile falls angegeben
        if profile_id:
            verfuegbare_profile = hole_verfuegbare_profile()
            if profile_id not in verfuegbare_profile:
                logger.warning(f"⚠️ Profile '{profile_id}' existiert nicht!")
                raise HTTPException(
                    status_code=400,
                    detail=f"⚠️ Profile '{profile_id}' nicht gefunden! Verfügbare Profile: {list(verfuegbare_profile.keys())}"
                )
        
        # Hole existierendes Mapping oder starte mit leerem Dict
        mapping = alle_mappings.get(format_name, {})
        
        # Update nur die Felder die angegeben wurden (None = nicht ändern!)
        if profile_id is not None:
            mapping["profile_id"] = profile_id
        if mistral_wrapper is not None:
            mapping["mistral_wrapper"] = mistral_wrapper
        if gpt_wrapper is not None:
            mapping["gpt_wrapper"] = gpt_wrapper
        if drift_scoring is not None:
            mapping["drift_scoring"] = drift_scoring
        if resonanz_score is not None:
            mapping["resonanz_score"] = resonanz_score
        if metadata is not None:
            # Metadata mergen, nicht überschreiben!
            mapping.setdefault("metadata", {}).update(metadata)
        
        # Speichern
        alle_mappings[format_name] = mapping
        mapping_daten["mappings"] = alle_mappings
        speichere_mapping_feld(mapping_daten)
        
        logger.info(f"✅ Mapping für '{format_name}' gespeichert")
        
        return {
            "erfolg": True,
            "format": format_name,
            "mapping": mapping,
            "message": "✅ Mapping created/updated successfully!",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Mapping erstellen/updaten für '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Mapping nicht speichern: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 4: Nur Profile updaten - Schnelles Profile-Wechseln!
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/formats/{format_name}/profile")
async def update_mapping_profile(format_name: str, profile_id: str):
    """
    🔄 Updated NUR das Profile für ein Format
    
    Manchmal willst du nur das Profile ändern, Rest bleibt gleich!
    Wie nur die Handynummer ändern aber Name/Adresse bleiben.
    
    Args:
        format_name: Format zum Updaten
        profile_id: Neue Profile-ID
    
    Returns:
        Bestätigung mit neuem Profile
    
    Errors:
        404: Format hat kein Mapping
        400: Profile existiert nicht
        500: Speichern fehlgeschlagen
    """
    try:
        mapping_daten = lade_mapping_feld()
        alle_mappings = mapping_daten.get("mappings", {})
        
        # Check ob Format existiert
        if format_name not in alle_mappings:
            raise HTTPException(
                status_code=404,
                detail=f"❌ Format '{format_name}' hat kein Mapping!"
            )
        
        # Validate neues Profile
        verfuegbare_profile = hole_verfuegbare_profile()
        if profile_id not in verfuegbare_profile:
            raise HTTPException(
                status_code=400,
                detail=f"⚠️ Profile '{profile_id}' existiert nicht! Verfügbare: {list(verfuegbare_profile.keys())}"
            )
        
        # Update nur Profile, Rest bleibt!
        alle_mappings[format_name]["profile_id"] = profile_id
        mapping_daten["mappings"] = alle_mappings
        speichere_mapping_feld(mapping_daten)
        
        logger.info(f"✅ Profile für '{format_name}' auf '{profile_id}' geändert")
        
        return {
            "erfolg": True,
            "format": format_name,
            "profile_id": profile_id,
            "message": "✅ Profile updated!",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Profile-Update für '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Profile nicht updaten: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 5: Drift-Scoring Config updaten - Drift-Strom kalibrieren!
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/formats/{format_name}/drift-scoring")
async def update_drift_scoring(
    format_name: str,
    enabled: bool,
    threshold: Optional[float] = 0.8,
    scorer_model: Optional[str] = None,
    prompt_template: Optional[str] = None
):
    """
    ⚙️ Updated Drift-Scoring Einstellungen für ein Format
    
    Drift-Scoring = checken ob GPT Output zu weit vom gewünschten Format abdriftet!
    Das ist wie TÜV für AI-Outputs - stimmt das Format noch oder driftet's ab?
    
    Args:
        format_name: Format zum Konfigurieren
        enabled: Drift-Scoring an oder aus?
        threshold: Ab welchem Score gilt's als Drift? (0.0 = alles OK, 1.0 = total Drift)
        scorer_model: Welches Model zum Scoren? (optional)
        prompt_template: Welches Prompt-Template? (optional)
    
    Returns:
        Bestätigung mit neuer Drift-Config
    
    Errors:
        404: Format hat kein Mapping
        500: Speichern fehlgeschlagen
    """
    try:
        mapping_daten = lade_mapping_feld()
        alle_mappings = mapping_daten.get("mappings", {})
        
        # Check ob Format existiert
        if format_name not in alle_mappings:
            raise HTTPException(
                status_code=404,
                detail=f"❌ Format '{format_name}' hat kein Mapping!"
            )
        
        # Baue neue Drift-Config
        drift_config = {
            "enabled": enabled,
            "threshold": threshold
        }
        
        if scorer_model:
            drift_config["scorer_model"] = scorer_model
        if prompt_template:
            drift_config["prompt_template"] = prompt_template
        
        # Update Mapping
        alle_mappings[format_name]["drift_scoring"] = drift_config
        mapping_daten["mappings"] = alle_mappings
        speichere_mapping_feld(mapping_daten)
        
        logger.info(f"✅ Drift-Scoring für '{format_name}' updated: enabled={enabled}, threshold={threshold}")
        
        return {
            "erfolg": True,
            "format": format_name,
            "drift_scoring": drift_config,
            "message": "✅ Drift scoring config updated!",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Drift-Config-Update für '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Drift-Config nicht updaten: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 6: Mapping löschen - Nummer aus Telefonbuch streichen!
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/formats/{format_name}")
async def delete_mapping(format_name: str):
    """
    🗑️ Löscht ein Format-Mapping komplett
    
    Nummer aus dem Telefonbuch streichen - Format ist dann nicht mehr im System!
    Vorsicht: Das ist permanent, gibt kein "Undo"!
    
    Args:
        format_name: Format zum Löschen
    
    Returns:
        Bestätigung mit gelöschtem Mapping
    
    Errors:
        404: Format hat kein Mapping
        500: Löschen fehlgeschlagen
    """
    try:
        mapping_daten = lade_mapping_feld()
        alle_mappings = mapping_daten.get("mappings", {})
        
        # Check ob Format existiert
        if format_name not in alle_mappings:
            raise HTTPException(
                status_code=404,
                detail=f"❌ Format '{format_name}' hat kein Mapping zum Löschen!"
            )
        
        # Löschen (pop gibt gelöschten Wert zurück - praktisch für Response!)
        geloeschtes_mapping = alle_mappings.pop(format_name)
        mapping_daten["mappings"] = alle_mappings
        speichere_mapping_feld(mapping_daten)
        
        logger.info(f"🗑️ Mapping für '{format_name}' gelöscht")
        
        return {
            "erfolg": True,
            "format": format_name,
            "deleted_mapping": geloeschtes_mapping,
            "message": "✅ Mapping deleted!",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Mapping-Löschen für '{format_name}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Mapping nicht löschen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 7: Alle Profile holen - Welche Profile gibt's?
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/profiles")
async def get_profiles():
    """
    📋 Zeigt alle verfügbaren Scoring-Profile
    
    Das sind die verschiedenen Scoring-Methoden die man auswählen kann!
    Jedes Profile hat andere Field-Weights und Scoring-Methods.
    
    Returns:
        Liste aller Profile mit IDs und Namen
    
    Errors:
        500: Profile-Directory nicht lesbar
    """
    try:
        verfuegbare_profile = hole_verfuegbare_profile()
        
        return {
            "erfolg": True,
            "total": len(verfuegbare_profile),
            "profiles": verfuegbare_profile,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Profile-Holen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Profile nicht laden: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ENDPOINT 8: Mapping-Stats holen - Wie sieht's aus im System?
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_mapping_stats():
    """
    📊 Gibt Statistiken über alle Mappings zurück
    
    Das ist wie die Zusammenfassung fürs Management-Dashboard!
    Zeigt:
    - Wie viele Formate sind im System?
    - Bei wie vielen ist Drift-Scoring an?
    - Welche Profile werden am meisten benutzt?
    - Wie ist der durchschnittliche Resonanz-Score?
    
    Returns:
        Komplette Stats über alle Mappings
    
    Errors:
        500: Mapping-File nicht lesbar
    """
    try:
        mapping_daten = lade_mapping_feld()
        alle_mappings = mapping_daten.get("mappings", {})
        verfuegbare_profile = hole_verfuegbare_profile()
        
        # Stats berechnen
        drift_enabled_count = sum(
            1 for mapping in alle_mappings.values() 
            if mapping.get("drift_scoring", {}).get("enabled", False)
        )
        
        # Welche Profile werden wie oft benutzt?
        profil_nutzung = {}
        for mapping in alle_mappings.values():
            profil_id = mapping.get("profile_id")
            if profil_id:
                profil_nutzung[profil_id] = profil_nutzung.get(profil_id, 0) + 1
        
        # Durchschnittlicher Resonanz-Score
        resonanz_scores = [
            mapping.get("resonanz_score", 0) 
            for mapping in alle_mappings.values() 
            if mapping.get("resonanz_score") is not None
        ]
        avg_resonanz = sum(resonanz_scores) / len(resonanz_scores) if resonanz_scores else 0
        
        return {
            "erfolg": True,
            "total_formats": len(alle_mappings),
            "total_profiles": len(verfuegbare_profile),
            "drift_enabled_count": drift_enabled_count,
            "drift_disabled_count": len(alle_mappings) - drift_enabled_count,
            "profile_usage": profil_nutzung,
            "average_resonanz_score": round(avg_resonanz, 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🔴 Fehler beim Stats-Berechnen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Konnte Stats nicht berechnen: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  🎬 ENDE - Mapping Router ist jetzt 100% SYNTX-Style! 💎⚡🔥
# ═══════════════════════════════════════════════════════════════════════════════
