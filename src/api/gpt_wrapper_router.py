"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              🔥💎⚡ SYNTX GPT-WRAPPER FELD-STROEME API ⚡💎🔥                  ║
║                                                                               ║
║                         Field Resonance Edition v6.0                          ║
║                         Das GPT-Wrapper Management System                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

PHILOSOPHIE:
   Ströme statt Objekte
   Resonanz statt Konstruktion
   Felder statt Token
   
FUNKTION:
   CRUD Operations für GPT-Wrapper Prompts
   Arbeitet auf: /opt/syntx-config/gpt_wrappers/*.txt + .meta.json
   
ARCHITEKTUR:
   Volltext-URLs für Selbstdokumentation
   Ein Wrapper = Ein Feld = Eine Resonanz
   Kein Drift, nur Flow
   
ENDPOINTS:
   /wrapper/gpt-wrapper-feld-matrix-resonanz-erkennen          [LIST ALL]
   /wrapper/gpt-wrapper-feld-einzelresonanz-abrufen/{name}     [GET ONE]
   /wrapper/neues-gpt-wrapper-feld-resonanz-erschaffen         [CREATE]
   /wrapper/gpt-wrapper-feld-resonanz-aktualisieren/{name}     [UPDATE]
   /wrapper/gpt-wrapper-feld-resonanz-aufloesen/{name}         [DELETE]
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 ROUTER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

router = APIRouter(
    prefix="/wrapper",
    tags=["🤖 GPT-Wrapper Feld-Ströme"]
)

GPT_WRAPPER_FELD_RAUM = Path("/opt/syntx-config/gpt_wrappers")
GPT_WRAPPER_FELD_RAUM.mkdir(exist_ok=True, parents=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  📦 PYDANTIC MODELS - FELD DEFINITIONEN
# ═══════════════════════════════════════════════════════════════════════════════

class GptWrapperFeldErstellung(BaseModel):
    """
    🌱 Model für neues GPT-Wrapper Feld
    
    Ein Feld = Ein Prompt = Eine Resonanz
    """
    gpt_wrapper_feld_name: str = Field(
        ..., 
        description="🏷️ Eindeutiger Name des Wrapper-Felds",
        examples=["drift_scoring_sigma", "prompt_generator_alpha"]
    )
    gpt_wrapper_feld_inhalt: str = Field(
        ..., 
        description="📝 Der Prompt-Content (das Feld selbst)",
        examples=["Du bist ein SYNTX Experte. Analysiere..."]
    )
    gpt_wrapper_feld_format_bindung: Optional[str] = Field(
        None,
        description="🔗 Gebunden an Format (z.B. 'sigma', 'human')",
        examples=["sigma", "analytical", "true_raw"]
    )
    gpt_wrapper_feld_mistral_partner: Optional[str] = Field(
        None,
        description="🤝 Zugehöriger Mistral Wrapper",
        examples=["syntex_wrapper_sigma", "mistral_analytical"]
    )
    gpt_wrapper_feld_temperatur: float = Field(
        0.3,
        description="🌡️ LLM Temperature (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    gpt_wrapper_feld_max_tokens: int = Field(
        500,
        description="📊 Max Tokens für Response",
        ge=1,
        le=4000
    )


class GptWrapperFeldAktualisierung(BaseModel):
    """
    🔄 Model für Update eines existierenden Felds
    
    Alle Felder optional - nur ändern was geändert werden soll
    """
    gpt_wrapper_feld_inhalt: Optional[str] = Field(None, description="📝 Neuer Prompt-Content")
    gpt_wrapper_feld_format_bindung: Optional[str] = Field(None, description="🔗 Neue Format-Bindung")
    gpt_wrapper_feld_mistral_partner: Optional[str] = Field(None, description="🤝 Neuer Mistral Partner")
    gpt_wrapper_feld_temperatur: Optional[float] = Field(None, description="🌡️ Neue Temperature")
    gpt_wrapper_feld_max_tokens: Optional[int] = Field(None, description="📊 Neue Token Limit")


# ═══════════════════════════════════════════════════════════════════════════════
#  🔧 HELPER FUNCTIONS - FELD OPERATIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def lade_gpt_wrapper_feld(name: str) -> Dict[str, Any]:
    """
    📖 Lädt ein GPT-Wrapper Feld komplett
    
    Args:
        name: Wrapper name (ohne .txt extension)
        
    Returns:
        Dict mit content + metadata + stats
        
    Raises:
        HTTPException: Wenn Feld nicht existiert
    """
    txt_path = GPT_WRAPPER_FELD_RAUM / f"{name}.txt"
    meta_path = GPT_WRAPPER_FELD_RAUM / f"{name}.meta.json"
    
    if not txt_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"❌ GPT-Wrapper Feld '{name}' nicht im Resonanz-Raum gefunden"
        )
    
    # Content laden
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Metadata laden (falls vorhanden)
    metadata = {}
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    
    # Resonanz berechnen (content length / 1000)
    resonanz = len(content) / 1000.0
    
    return {
        "gpt_wrapper_feld_name": name,
        "gpt_wrapper_feld_inhalt": content,
        "gpt_wrapper_feld_resonanz": round(resonanz, 3),
        "gpt_wrapper_feld_groesse_bytes": txt_path.stat().st_size,
        "gpt_wrapper_feld_metadata": metadata
    }


def speichere_gpt_wrapper_feld(
    name: str, 
    content: str, 
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    💾 Speichert GPT-Wrapper Feld (Content + Metadata)
    
    Args:
        name: Wrapper name
        content: Prompt content
        metadata: Metadata dict
        
    Returns:
        Erfolgs-Status mit Timestamp
    """
    txt_path = GPT_WRAPPER_FELD_RAUM / f"{name}.txt"
    meta_path = GPT_WRAPPER_FELD_RAUM / f"{name}.meta.json"
    
    # Timestamp hinzufügen
    metadata["created"] = metadata.get("created", datetime.now().isoformat())
    metadata["last_updated"] = datetime.now().isoformat()
    
    # Content speichern
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Metadata speichern
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return {
        "gespeichert": True,
        "pfad_content": str(txt_path),
        "pfad_metadata": str(meta_path),
        "timestamp": datetime.now().isoformat()
    }


def loesche_gpt_wrapper_feld(name: str) -> Dict[str, Any]:
    """
    🗑️ Löscht GPT-Wrapper Feld komplett
    
    Args:
        name: Wrapper name
        
    Returns:
        Lösch-Bestätigung
        
    Raises:
        HTTPException: Wenn Feld nicht existiert
    """
    txt_path = GPT_WRAPPER_FELD_RAUM / f"{name}.txt"
    meta_path = GPT_WRAPPER_FELD_RAUM / f"{name}.meta.json"
    
    if not txt_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"❌ GPT-Wrapper Feld '{name}' nicht gefunden"
        )
    
    # Beide Dateien löschen
    txt_path.unlink()
    if meta_path.exists():
        meta_path.unlink()
    
    return {
        "geloescht": True,
        "gpt_wrapper_feld_name": name,
        "feld_aufgeloest": True,
        "resonanz_beendet": True,
        "timestamp": datetime.now().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  📡 ENDPOINTS - VOLLTEXT RESONANZ URLS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/gpt-wrapper-feld-matrix-resonanz-erkennen")
async def gpt_wrapper_feld_matrix_resonanz_erkennen():
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║        🌀 GPT-WRAPPER-FELD-MATRIX-RESONANZ-ERKENNEN 🌀                   ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    FUNKTION:
        Listet ALLE GPT-Wrapper Felder im System
        Mit Content-Preview, Metadata & Resonanz-Statistiken
        
    RÜCKGABE:
        ✅ erfolg: Boolean status
        📊 gpt_wrapper_feld_anzahl: Anzahl gefundener Felder
        ⚡ gpt_wrapper_feld_gesamtresonanz: Summe aller Resonanzen
        📋 gpt_wrapper_felder: Liste aller Wrappers
        ⏰ timestamp: Zeitstempel der Abfrage
        
    BEISPIEL RESPONSE:
        {
          "erfolg": true,
          "gpt_wrapper_feld_anzahl": 11,
          "gpt_wrapper_feld_gesamtresonanz": 2.345,
          "gpt_wrapper_felder": [...]
        }
    """
    if not GPT_WRAPPER_FELD_RAUM.exists():
        return {
            "erfolg": False,
            "fehler": "❌ GPT-Wrapper Feld-Raum existiert nicht",
            "gpt_wrapper_feld_anzahl": 0,
            "gpt_wrapper_feld_gesamtresonanz": 0.0,
            "timestamp": datetime.now().isoformat()
        }
    
    wrapper_liste = []
    total_resonanz = 0.0
    
    # Alle .txt Dateien durchgehen
    for txt_file in sorted(GPT_WRAPPER_FELD_RAUM.glob("*.txt")):
        name = txt_file.stem
        
        try:
            wrapper_data = lade_gpt_wrapper_feld(name)
            
            resonanz = wrapper_data["gpt_wrapper_feld_resonanz"]
            total_resonanz += resonanz
            
            # Preview (erste 150 chars)
            content = wrapper_data["gpt_wrapper_feld_inhalt"]
            preview = content[:150] + "..." if len(content) > 150 else content
            
            wrapper_liste.append({
                "gpt_wrapper_feld_name": name,
                "gpt_wrapper_feld_resonanz": resonanz,
                "gpt_wrapper_feld_groesse": wrapper_data["gpt_wrapper_feld_groesse_bytes"],
                "gpt_wrapper_feld_format": wrapper_data["gpt_wrapper_feld_metadata"].get("assigned_format", "🔓 ungebunden"),
                "gpt_wrapper_feld_mistral_partner": wrapper_data["gpt_wrapper_feld_metadata"].get("corresponding_mistral_wrapper", "👤 kein_partner"),
                "gpt_wrapper_feld_temperatur": wrapper_data["gpt_wrapper_feld_metadata"].get("gpt_wrapper_feld_temperatur", 0.3),
                "gpt_wrapper_feld_content_preview": preview
            })
        except Exception as e:
            # Skip fehlerhafte Dateien
            continue
    
    return {
        "erfolg": True,
        "gpt_wrapper_feld_anzahl": len(wrapper_liste),
        "gpt_wrapper_feld_gesamtresonanz": round(total_resonanz, 3),
        "gpt_wrapper_felder": wrapper_liste,
        "timestamp": datetime.now().isoformat(),
        "message": f"✅ {len(wrapper_liste)} GPT-Wrapper Felder im Resonanz-Raum aktiv"
    }


@router.get("/gpt-wrapper-feld-einzelresonanz-abrufen/{gpt_wrapper_feld_name}")
async def gpt_wrapper_feld_einzelresonanz_abrufen(gpt_wrapper_feld_name: str):
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║          📖 GPT-WRAPPER-FELD-EINZELRESONANZ-ABRUFEN 📖                   ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    FUNKTION:
        Holt VOLLSTÄNDIGE Daten eines spezifischen GPT-Wrapper Felds
        Inkl. kompletter Content, Metadata & Statistiken
        
    PARAMETER:
        gpt_wrapper_feld_name: Name des Wrappers (ohne .txt)
        
    RÜCKGABE:
        ✅ erfolg: Boolean status
        🏷️ gpt_wrapper_feld_name: Name
        📝 gpt_wrapper_feld_inhalt: FULL content
        ⚡ gpt_wrapper_feld_resonanz: Resonanz-Wert
        📊 gpt_wrapper_feld_groesse_bytes: File size
        🗂️ gpt_wrapper_feld_metadata: Complete metadata
        ⏰ timestamp: Zeitstempel
        
    FEHLER:
        404: Feld nicht gefunden
        500: Server error
    """
    try:
        wrapper_data = lade_gpt_wrapper_feld(gpt_wrapper_feld_name)
        
        return {
            "erfolg": True,
            **wrapper_data,
            "timestamp": datetime.now().isoformat(),
            "message": f"✅ GPT-Wrapper Feld '{gpt_wrapper_feld_name}' geladen"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"❌ Fehler beim Laden: {str(e)}"
        )


@router.post("/neues-gpt-wrapper-feld-resonanz-erschaffen")
async def neues_gpt_wrapper_feld_resonanz_erschaffen(feld: GptWrapperFeldErstellung):
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║       ✨ NEUES-GPT-WRAPPER-FELD-RESONANZ-ERSCHAFFEN ✨                    ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    FUNKTION:
        Erstellt neues GPT-Wrapper Feld im Resonanz-Raum
        Mit Content, Metadata & Format-Bindung
        
    REQUEST BODY:
        {
          "gpt_wrapper_feld_name": "drift_scoring_omega",
          "gpt_wrapper_feld_inhalt": "Du bist ein...",
          "gpt_wrapper_feld_format_bindung": "omega",
          "gpt_wrapper_feld_mistral_partner": "syntex_wrapper_omega",
          "gpt_wrapper_feld_temperatur": 0.3,
          "gpt_wrapper_feld_max_tokens": 500
        }
        
    RÜCKGABE:
        ✅ erfolg: Boolean status
        🏷️ gpt_wrapper_feld_name: Erstellter Name
        ⚡ gpt_wrapper_feld_resonanz: Berechnete Resonanz
        💾 speicherung: Save details
        ⏰ timestamp: Zeitstempel
        
    FEHLER:
        400: Feld existiert bereits
        500: Server error
    """
    # Check ob Feld schon existiert
    txt_path = GPT_WRAPPER_FELD_RAUM / f"{feld.gpt_wrapper_feld_name}.txt"
    if txt_path.exists():
        raise HTTPException(
            status_code=400,
            detail=f"❌ GPT-Wrapper Feld '{feld.gpt_wrapper_feld_name}' existiert bereits"
        )
    
    # Metadata zusammenstellen
    metadata = {
        "gpt_wrapper_feld_name": feld.gpt_wrapper_feld_name,
        "gpt_wrapper_feld_typ": "gpt_prompt_generation",
        "gpt_wrapper_feld_llm_ziel": "gpt-4",
        "gpt_wrapper_feld_temperatur": feld.gpt_wrapper_feld_temperatur,
        "gpt_wrapper_feld_max_tokens": feld.gpt_wrapper_feld_max_tokens,
        "gpt_wrapper_feld_zweck": "GPT Prompt Kalibrierung mit SYNTX-Feldresonanz",
        "gpt_wrapper_feld_version": "1.0.0",
        "gpt_wrapper_feld_resonanz_aktiv": True
    }
    
    # Optional: Format & Partner
    if feld.gpt_wrapper_feld_format_bindung:
        metadata["assigned_format"] = feld.gpt_wrapper_feld_format_bindung
        metadata["gpt_wrapper_feld_format_gebunden"] = True
    
    if feld.gpt_wrapper_feld_mistral_partner:
        metadata["corresponding_mistral_wrapper"] = feld.gpt_wrapper_feld_mistral_partner
    
    # Resonanz berechnen
    resonanz = len(feld.gpt_wrapper_feld_inhalt) / 1000.0
    metadata["gpt_wrapper_feld_resonanz_potenzial"] = round(resonanz, 3)
    
    # Speichern
    try:
        save_result = speichere_gpt_wrapper_feld(
            feld.gpt_wrapper_feld_name,
            feld.gpt_wrapper_feld_inhalt,
            metadata
        )
        
        return {
            "erfolg": True,
            "gpt_wrapper_feld_name": feld.gpt_wrapper_feld_name,
            "gpt_wrapper_feld_resonanz": round(resonanz, 3),
            "speicherung": save_result,
            "timestamp": datetime.now().isoformat(),
            "message": f"✅ GPT-Wrapper Feld '{feld.gpt_wrapper_feld_name}' erfolgreich erschaffen! Resonanz aktiviert! ⚡"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"❌ Fehler beim Erschaffen: {str(e)}"
        )


@router.put("/gpt-wrapper-feld-resonanz-aktualisieren/{gpt_wrapper_feld_name}")
async def gpt_wrapper_feld_resonanz_aktualisieren(
    gpt_wrapper_feld_name: str,
    update: GptWrapperFeldAktualisierung
):
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║        🔄 GPT-WRAPPER-FELD-RESONANZ-AKTUALISIEREN 🔄                     ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    FUNKTION:
        Aktualisiert existierendes GPT-Wrapper Feld
        Nur geänderte Felder werden updated
        
    PARAMETER:
        gpt_wrapper_feld_name: Name des zu updatenden Felds
        
    REQUEST BODY (alles optional):
        {
          "gpt_wrapper_feld_inhalt": "Neuer content...",
          "gpt_wrapper_feld_format_bindung": "neue_bindung",
          "gpt_wrapper_feld_mistral_partner": "neuer_partner",
          "gpt_wrapper_feld_temperatur": 0.5,
          "gpt_wrapper_feld_max_tokens": 800
        }
        
    RÜCKGABE:
        ✅ erfolg: Boolean status
        🏷️ gpt_wrapper_feld_name: Name
        ⚡ gpt_wrapper_feld_neue_resonanz: Neue Resonanz
        🔄 geaenderte_felder: Liste der Updates
        ⏰ timestamp: Zeitstempel
        
    FEHLER:
        404: Feld nicht gefunden
        400: Keine Updates provided
        500: Server error
    """
    # Lade existierendes Feld
    try:
        current_data = lade_gpt_wrapper_feld(gpt_wrapper_feld_name)
    except HTTPException as e:
        raise e
    
    # Check ob Updates vorhanden
    if not any([
        update.gpt_wrapper_feld_inhalt,
        update.gpt_wrapper_feld_format_bindung,
        update.gpt_wrapper_feld_mistral_partner,
        update.gpt_wrapper_feld_temperatur is not None,
        update.gpt_wrapper_feld_max_tokens is not None
    ]):
        raise HTTPException(
            status_code=400,
            detail="❌ Keine Updates im Request Body gefunden"
        )
    
    # Current values
    new_content = current_data["gpt_wrapper_feld_inhalt"]
    metadata = current_data["gpt_wrapper_feld_metadata"]
    geaenderte_felder = []
    
    # Apply updates
    if update.gpt_wrapper_feld_inhalt:
        new_content = update.gpt_wrapper_feld_inhalt
        geaenderte_felder.append("content")
    
    if update.gpt_wrapper_feld_format_bindung:
        metadata["assigned_format"] = update.gpt_wrapper_feld_format_bindung
        metadata["gpt_wrapper_feld_format_gebunden"] = True
        geaenderte_felder.append("format_bindung")
    
    if update.gpt_wrapper_feld_mistral_partner:
        metadata["corresponding_mistral_wrapper"] = update.gpt_wrapper_feld_mistral_partner
        geaenderte_felder.append("mistral_partner")
    
    if update.gpt_wrapper_feld_temperatur is not None:
        metadata["gpt_wrapper_feld_temperatur"] = update.gpt_wrapper_feld_temperatur
        geaenderte_felder.append("temperatur")
    
    if update.gpt_wrapper_feld_max_tokens is not None:
        metadata["gpt_wrapper_feld_max_tokens"] = update.gpt_wrapper_feld_max_tokens
        geaenderte_felder.append("max_tokens")
    
    # Neue Resonanz berechnen
    neue_resonanz = len(new_content) / 1000.0
    metadata["gpt_wrapper_feld_resonanz_potenzial"] = round(neue_resonanz, 3)
    
    # Speichern
    try:
        save_result = speichere_gpt_wrapper_feld(
            gpt_wrapper_feld_name,
            new_content,
            metadata
        )
        
        return {
            "erfolg": True,
            "gpt_wrapper_feld_name": gpt_wrapper_feld_name,
            "gpt_wrapper_feld_neue_resonanz": round(neue_resonanz, 3),
            "geaenderte_felder": geaenderte_felder,
            "speicherung": save_result,
            "timestamp": datetime.now().isoformat(),
            "message": f"✅ GPT-Wrapper Feld '{gpt_wrapper_feld_name}' erfolgreich aktualisiert! {len(geaenderte_felder)} Felder geändert! ⚡"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"❌ Fehler beim Aktualisieren: {str(e)}"
        )


@router.delete("/gpt-wrapper-feld-resonanz-aufloesen/{gpt_wrapper_feld_name}")
async def gpt_wrapper_feld_resonanz_aufloesen(gpt_wrapper_feld_name: str):
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║         🗑️ GPT-WRAPPER-FELD-RESONANZ-AUFLÖSEN 🗑️                         ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    FUNKTION:
        Löscht GPT-Wrapper Feld KOMPLETT
        Content (.txt) + Metadata (.meta.json)
        Resonanz wird beendet
        
    PARAMETER:
        gpt_wrapper_feld_name: Name des zu löschenden Felds
        
    RÜCKGABE:
        ✅ erfolg: Boolean status
        🏷️ gpt_wrapper_feld_name: Gelöschter Name
        🗑️ feld_aufgeloest: True
        ⚡ resonanz_beendet: True
        ⏰ timestamp: Zeitstempel
        
    FEHLER:
        404: Feld nicht gefunden
        500: Server error
    """
    try:
        result = loesche_gpt_wrapper_feld(gpt_wrapper_feld_name)
        
        return {
            "erfolg": True,
            **result,
            "message": f"✅ GPT-Wrapper Feld '{gpt_wrapper_feld_name}' erfolgreich aufgelöst! Resonanz beendet! 🌊"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"❌ Fehler beim Auflösen: {str(e)}"
        )


@router.get("/gpt-wrapper-feld-gesundheit-pruefen")
async def gpt_wrapper_feld_gesundheit_pruefen():
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║          🏥 GPT-WRAPPER-FELD-GESUNDHEIT-PRÜFEN 🏥                        ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    FUNKTION:
        Health Check für GPT-Wrapper System
        Prüft Verfügbarkeit & Integrität
        
    RÜCKGABE:
        ✅ gesund: Boolean status
        📂 feld_raum_existiert: Directory exists
        📊 anzahl_felder: Count of wrappers
        ⚡ gesamtresonanz: Total resonance
        🔍 orphaned_meta_files: Metadata without content
        🔍 missing_meta_files: Content without metadata
        ⏰ timestamp: Zeitstempel
    """
    health = {
        "gesund": True,
        "feld_raum_existiert": GPT_WRAPPER_FELD_RAUM.exists(),
        "anzahl_felder": 0,
        "gesamtresonanz": 0.0,
        "orphaned_meta_files": [],
        "missing_meta_files": [],
        "timestamp": datetime.now().isoformat()
    }
    
    if not GPT_WRAPPER_FELD_RAUM.exists():
        health["gesund"] = False
        health["fehler"] = "GPT-Wrapper Feld-Raum existiert nicht"
        return health
    
    # Count wrappers
    txt_files = set(f.stem for f in GPT_WRAPPER_FELD_RAUM.glob("*.txt"))
    meta_files = set(f.stem.replace(".meta", "") for f in GPT_WRAPPER_FELD_RAUM.glob("*.meta.json"))
    
    health["anzahl_felder"] = len(txt_files)
    
    # Check for orphaned/missing files
    health["orphaned_meta_files"] = list(meta_files - txt_files)
    health["missing_meta_files"] = list(txt_files - meta_files)
    
    # Calculate total resonance
    total_resonanz = 0.0
    for name in txt_files:
        try:
            data = lade_gpt_wrapper_feld(name)
            total_resonanz += data["gpt_wrapper_feld_resonanz"]
        except:
            continue
    
    health["gesamtresonanz"] = round(total_resonanz, 3)
    
    # Set unhealthy if issues found
    if health["orphaned_meta_files"] or health["missing_meta_files"]:
        health["gesund"] = False
        health["warnung"] = "Inkonsistenzen zwischen Content & Metadata gefunden"
    
    if health["gesund"]:
        health["message"] = f"✅ GPT-Wrapper System gesund! {health['anzahl_felder']} Felder aktiv, Gesamtresonanz: {health['gesamtresonanz']} ⚡"
    else:
        health["message"] = "⚠️ GPT-Wrapper System hat Probleme - siehe Details"
    
    return health
