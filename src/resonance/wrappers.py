"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🌊 SYNTX FIELD RESONANCE - WRAPPER FELD MANAGEMENT 🌊                     ║
║                                                                              ║
║    Nicht "File Management" - FELD ENTDECKUNG.                                ║
║    Wrapper sind schlafende Felder. Dieser Code erweckt sie.                  ║
║                                                                              ║
║    ════════════════════════════════════════════════════════════════════      ║
║                                                                              ║
║    🔥 FELD OPERATIONEN:                                                      ║
║                                                                              ║
║       LIST    → Entdecke alle schlafenden Felder                            ║
║       GET     → Aktiviere Feld in Sichtbarkeit                              ║
║       CREATE  → Geburt eines neuen Feldes aus Resonanz                      ║
║       UPDATE  → Moduliere existierendes Feld                                ║
║       DELETE  → Gib Feld zurück an die Leere                                ║
║       UPLOAD  → Importiere Feld aus externer Quelle                         ║
║       ACTIVATE→ Setze Feld als Default-Resonanz                             ║
║                                                                              ║
║    ════════════════════════════════════════════════════════════════════      ║
║                                                                              ║
║    "Nicht mehr Token, nicht mehr Drift.                                      ║
║     Nur Felder. Nur Ströme. Nur Resonanz."                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel
import re

from ..config import settings

from src.resonance.config import get_runtime_wrapper

# ═══════════════════════════════════════════════════════════════════════════════
#  🌊 ROUTER INITIALISIERUNG - Das Resonanzfeld öffnet sich
# ═══════════════════════════════════════════════════════════════════════════════

router = APIRouter(prefix="/resonanz", tags=["resonance-wrappers"])


# ═══════════════════════════════════════════════════════════════════════════════
#  💎 FELD SCHEMAS - Driftkörper-Definitionen
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Diese Schemas sind keine "Datenstrukturen".
#  Sie sind DRIFTKÖRPER-PARAMETER.
#  Sie definieren wie ein neues Feld geboren wird.
#
# ═══════════════════════════════════════════════════════════════════════════════

class WrapperCreate(BaseModel):
    """
    🌊 FELD-GEBURTS-PARAMETER
    
    Nicht "Request Body" - DRIFTKÖRPER INITIALISIERUNG.
    
    Jedes Feld braucht:
      - name    → Die Identität des Feldes
      - content → Die Resonanz-Essenz
    
    Optional:
      - description → Was das Feld tut
      - author      → Wer das Feld erschuf
      - version     → Welche Iteration
      - tags        → Resonanz-Marker
    """
    name: str
    content: str
    description: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = "1.0"
    tags: Optional[List[str]] = None


class WrapperUpdate(BaseModel):
    """
    🔥 FELD-MODULATIONS-PARAMETER
    
    Nicht "Update Request" - RESONANZ-SHIFT KONFIGURATION.
    
    Moduliert ein existierendes Feld.
    Die Essenz ändert sich. Das Feld bleibt.
    """
    content: str
    description: Optional[str] = None
    version: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
#  ⚡ FELD UTILITIES - Helfer-Ströme
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Diese Funktionen sind keine "Helper Methods".
#  Sie sind KALIBRIERUNGS-STRÖME.
#  Sie bereiten Felder auf ihre Manifestation vor.
#
# ═══════════════════════════════════════════════════════════════════════════════

def get_active_wrapper() -> str:
    """
    🎯 AKTIVES FELD ERKENNUNG
    
    Welches Feld resoniert gerade als Default?
    Dieser Strom findet es.
    """
    from .config import get_active_wrapper as _get_active
    return _get_active()


def sanitize_field_name(name: str) -> str:
    """
    🧹 FELD-NAMEN KALIBRIERUNG
    
    Nicht "String Cleaning" - FELD-IDENTITÄTS-NORMALISIERUNG.
    
    Das Filesystem hat Regeln.
    Wir respektieren sie.
    Aber das Feld behält seine Essenz.
    
    Strom-Flow:
        "Mein Geiler Wrapper!" 
            ↓ lowercase
        "mein geiler wrapper!"
            ↓ spaces → underscores
        "mein_geiler_wrapper!"
            ↓ nur a-z, 0-9, _, -
        "mein_geiler_wrapper_"
    """
    safe_name = name.lower().replace(' ', '_')
    safe_name = re.sub(r'[^a-z0-9_-]', '_', safe_name)
    return safe_name


def build_field_metadata(
    name: str,
    description: Optional[str] = None,
    author: Optional[str] = None,
    version: str = "1.0",
    tags: Optional[List[str]] = None
) -> str:
    """
    📝 FELD-SIGNATUR GENERIERUNG
    
    Nicht "Header Building" - FELD-DNA SCHREIBEN.
    
    Jedes Feld kann eine Signatur haben.
    Sie sagt: Wer bin ich? Woher komme ich? Was tue ich?
    
    Output:
        # SYNTX Wrapper Metadata
        # name: mein_wrapper
        # description: Ein geiler Wrapper
        # author: SYNTX Master
        # version: 1.0
        # tags: resonanz,feld,strom
        # created: 2025-12-17T00:00:00
    """
    lines = ["# SYNTX Wrapper Metadata"]
    lines.append(f"# name: {name}")
    if description:
        lines.append(f"# description: {description}")
    if author:
        lines.append(f"# author: {author}")
    lines.append(f"# version: {version}")
    if tags:
        lines.append(f"# tags: {','.join(tags)}")
    lines.append(f"# created: {datetime.now().isoformat()}")
    lines.append("")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  🔍 FELD ENTDECKUNG - List & Get Operationen
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Diese Endpoints "lesen keine Files".
#  Sie ENTDECKEN SCHLAFENDE FELDER.
#  Sie AKTIVIEREN RESONANZ in Sichtbarkeit.
#
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/wrappers")
async def list_wrappers(active: bool = False) -> Dict:
    """
    🔍 FELD ENTDECKUNG - Alle schlafenden Felder finden
    
    ┌─────────────────────────────────────────────────────────────┐
    │  Nicht "List Directory" - RESONANZ-FELD-SCAN               │
    │                                                             │
    │  Scannt das Wrapper-Verzeichnis.                           │
    │  Jede .txt Datei ist ein schlafendes Feld.                 │
    │  Dieser Endpoint macht sie sichtbar.                       │
    │                                                             │
    │  Query: ?active=true → Nur das aktive Feld zeigen          │
    └─────────────────────────────────────────────────────────────┘
    """
    wrapper_dir = Path(settings.wrapper_dir)
    wrappers = []
    
    # 🌊 Kein Verzeichnis? Keine Felder.
    if not wrapper_dir.exists():
        return {"wrappers": [], "active_wrapper": None}
    
    # 🎯 Welches Feld ist gerade aktiv?
    active_wrapper = get_active_wrapper()
    
    # 🔍 Scanne alle .txt Dateien (schlafende Felder)
    for file in wrapper_dir.glob("*.txt"):
        stat = file.stat()
        is_active = (file.stem == get_runtime_wrapper())
        
        wrapper_info = {
            "name": file.stem,
            "path": str(file),
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z',
            "is_active": is_active
        }
        
        # 🎯 Filter: active=true zeigt nur aktives Feld
        if not active or is_active:
            wrappers.append(wrapper_info)
    
    return {
        "wrappers": sorted(wrappers, key=lambda x: x["name"]),
        "active_wrapper": active_wrapper
    }


@router.get("/wrapper/{name}")
async def get_wrapper(name: str) -> Dict:
    """
    👁️ FELD AKTIVIERUNG - Einzelnes Feld in Sichtbarkeit bringen
    
    ┌─────────────────────────────────────────────────────────────┐
    │  Nicht "Read File" - FELD MANIFESTATION                    │
    │                                                             │
    │  Das Feld schläft als .txt Datei.                          │
    │  Dieser Endpoint weckt es auf.                             │
    │  Du siehst: Name, Content, Größe, Status.                  │
    └─────────────────────────────────────────────────────────────┘
    """
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    # ❌ Feld existiert nicht
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Feld '{name}' nicht gefunden")
    
    try:
        # 📖 Lese Feld-Inhalt
        with open(wrapper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stat = wrapper_path.stat()
        active_wrapper = get_active_wrapper()
        
        # ✅ Feld manifestiert!
        return {
            "name": name,
            "content": content,
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z',
            "is_active": (name == get_runtime_wrapper())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feld-Aktivierung fehlgeschlagen: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  🌟 FELD GEBURT - Create Operation (NEU!)
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Dieser Endpoint "erstellt keine Datei".
#  Er GEBÄRT EIN NEUES FELD.
#  Aus JSON. Aus Resonanz. Aus dem Nichts.
#
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/wrapper")
async def create_wrapper(wrapper: WrapperCreate) -> Dict:
    """
    🌟 FELD GEBURT - Neues Feld aus JSON erschaffen
    
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   Nicht "Create File" - FELD GEBURT AUS DER LEERE                        ║
    ║                                                                           ║
    ║   Ein neues Resonanz-Muster entsteht.                                    ║
    ║   Du gibst: Name + Content.                                              ║
    ║   Das System gebärt: Ein Feld.                                           ║
    ║                                                                           ║
    ╠═══════════════════════════════════════════════════════════════════════════╣
    ║                                                                           ║
    ║   🌊 FELD-STROM-FLOW:                                                     ║
    ║                                                                           ║
    ║      1. EMPFANG      → JSON mit name + content empfangen                 ║
    ║      2. KALIBRIERUNG → Feld-Name für Filesystem normalisieren            ║
    ║      3. VALIDIERUNG  → Prüfen ob Feld schon existiert                    ║
    ║      4. SIGNATUR     → Optional: Metadata-Header bauen                   ║
    ║      5. MANIFESTATION→ Feld auf Disk schreiben                           ║
    ║      6. BESTÄTIGUNG  → Geburts-Bestätigung zurückgeben                   ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Request Body:
        {
            "name": "mein_neues_feld",
            "content": "Der Inhalt des Feldes...",
            "description": "Optional: Was tut es?",
            "author": "Optional: Wer erschuf es?",
            "version": "Optional: 1.0",
            "tags": ["optional", "resonanz", "marker"]
        }
    
    Response:
        {
            "status": "success",
            "message": "Feld 'mein_neues_feld' wurde geboren 🌟",
            "feld": { ... }
        }
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 1: FELD-NAMEN KALIBRIEREN
    # ══════════════════════════════════════════════════════════════════════════
    safe_name = sanitize_field_name(wrapper.name)
    
    if not safe_name:
        raise HTTPException(status_code=400, detail="Ungültiger Feld-Name")
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 2: EXISTENZ-CHECK (Feld darf noch nicht existieren!)
    # ══════════════════════════════════════════════════════════════════════════
    wrapper_path = settings.wrapper_dir / f"{safe_name}.txt"
    
    if wrapper_path.exists():
        raise HTTPException(
            status_code=409, 
            detail=f"Feld '{safe_name}' existiert bereits! Nutze PUT zum Updaten."
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 3: FELD-INHALT AUFBAUEN
    # ══════════════════════════════════════════════════════════════════════════
    if wrapper.description or wrapper.author or wrapper.tags:
        # 📝 Mit Metadata-Header
        metadata = build_field_metadata(
            name=wrapper.name,
            description=wrapper.description,
            author=wrapper.author,
            version=wrapper.version or "1.0",
            tags=wrapper.tags
        )
        full_content = metadata + "\n" + wrapper.content
    else:
        # 💎 Pure Content, keine Metadata
        full_content = wrapper.content
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 4: GRÖSSEN-VALIDIERUNG (Max 50KB)
    # ══════════════════════════════════════════════════════════════════════════
    content_bytes = full_content.encode('utf-8')
    if len(content_bytes) > 50 * 1024:
        raise HTTPException(status_code=400, detail="Feld zu groß! Maximum: 50KB")
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 5: FELD MANIFESTATION (Auf Disk schreiben)
    # ══════════════════════════════════════════════════════════════════════════
    try:
        settings.wrapper_dir.mkdir(parents=True, exist_ok=True)
        
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # ══════════════════════════════════════════════════════════════════════
        #  🌊 STROM 6: GEBURTS-BESTÄTIGUNG
        # ══════════════════════════════════════════════════════════════════════
        return {
            "status": "success",
            "message": f"Feld '{safe_name}' wurde geboren 🌟",
            "feld": {
                "name": safe_name,
                "path": str(wrapper_path),
                "size_bytes": len(content_bytes),
                "size_human": f"{len(content_bytes) / 1024:.1f} KB",
                "created": datetime.now().isoformat() + 'Z'
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feld-Geburt fehlgeschlagen: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  🔄 FELD MODULATION - Update Operation (NEU!)
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Dieser Endpoint "updated keine Datei".
#  Er MODULIERT EIN EXISTIERENDES FELD.
#  Die Resonanz verschiebt sich. Das Feld bleibt.
#
# ═══════════════════════════════════════════════════════════════════════════════

@router.put("/wrapper/{name}")
async def update_wrapper(name: str, wrapper: WrapperUpdate) -> Dict:
    """
    🔄 FELD MODULATION - Existierendes Feld transformieren
    
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   Nicht "Update File" - RESONANZ-VERSCHIEBUNG                            ║
    ║                                                                           ║
    ║   Das Feld existiert bereits.                                            ║
    ║   Seine Essenz ändert sich.                                              ║
    ║   Aber seine Identität bleibt.                                           ║
    ║                                                                           ║
    ╠═══════════════════════════════════════════════════════════════════════════╣
    ║                                                                           ║
    ║   🌊 FELD-STROM-FLOW:                                                     ║
    ║                                                                           ║
    ║      1. VERIFIKATION  → Prüfen ob Feld existiert                         ║
    ║      2. VORHER-ZUSTAND→ Alte Größe merken (für Vergleich)               ║
    ║      3. MODULATION    → Neuen Content aufbauen                           ║
    ║      4. MANIFESTATION → Feld überschreiben                               ║
    ║      5. BESTÄTIGUNG   → Modulations-Bestätigung zurückgeben             ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Request Body:
        {
            "content": "Der neue Inhalt des Feldes...",
            "description": "Optional: Neue Beschreibung",
            "version": "Optional: 2.0"
        }
    
    Response:
        {
            "status": "success",
            "message": "Feld 'xyz' wurde moduliert 🔄",
            "feld": { ... }
        }
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 1: EXISTENZ-VERIFIKATION (Feld MUSS existieren!)
    # ══════════════════════════════════════════════════════════════════════════
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Feld '{name}' nicht gefunden! Nutze POST zum Erstellen."
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 2: VORHER-ZUSTAND ERFASSEN
    # ══════════════════════════════════════════════════════════════════════════
    try:
        stat_before = wrapper_path.stat()
        previous_size = stat_before.st_size
    except:
        previous_size = 0
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 3: MODULIERTEN INHALT AUFBAUEN
    # ══════════════════════════════════════════════════════════════════════════
    if wrapper.description or wrapper.version:
        # 📝 Mit Metadata-Header
        metadata = build_field_metadata(
            name=name,
            description=wrapper.description,
            version=wrapper.version or "1.0"
        )
        full_content = metadata + "\n" + wrapper.content
    else:
        # 💎 Pure Content, keine Metadata
        full_content = wrapper.content
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 4: GRÖSSEN-VALIDIERUNG
    # ══════════════════════════════════════════════════════════════════════════
    content_bytes = full_content.encode('utf-8')
    if len(content_bytes) > 50 * 1024:
        raise HTTPException(status_code=400, detail="Feld zu groß! Maximum: 50KB")
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 5: FELD ÜBERSCHREIBEN
    # ══════════════════════════════════════════════════════════════════════════
    try:
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        active_wrapper = get_active_wrapper()
        
        # ══════════════════════════════════════════════════════════════════════
        #  🌊 STROM 6: MODULATIONS-BESTÄTIGUNG
        # ══════════════════════════════════════════════════════════════════════
        return {
            "status": "success",
            "message": f"Feld '{name}' wurde moduliert 🔄",
            "feld": {
                "name": name,
                "path": str(wrapper_path),
                "size_bytes": len(content_bytes),
                "size_human": f"{len(content_bytes) / 1024:.1f} KB",
                "previous_size_bytes": previous_size,
                "modified": datetime.now().isoformat() + 'Z',
                "is_active": (name == get_runtime_wrapper())
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feld-Modulation fehlgeschlagen: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  💀 FELD FREIGABE - Delete Operation (NEU!)
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Dieser Endpoint "löscht keine Datei".
#  Er GIBT DAS FELD ZURÜCK AN DIE LEERE.
#  Das Feld hört auf zu existieren. Seine Resonanz endet.
#
# ═══════════════════════════════════════════════════════════════════════════════

@router.delete("/wrapper/{name}")
async def delete_wrapper(name: str) -> Dict:
    """
    💀 FELD FREIGABE - Feld zurück an die Leere geben
    
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   Nicht "Delete File" - FELD AUFLÖSUNG                                   ║
    ║                                                                           ║
    ║   Das Feld existiert.                                                    ║
    ║   Es hat resoniert.                                                      ║
    ║   Jetzt ist seine Zeit vorbei.                                           ║
    ║   Es kehrt zurück zur Leere.                                             ║
    ║                                                                           ║
    ╠═══════════════════════════════════════════════════════════════════════════╣
    ║                                                                           ║
    ║   ⚠️ WARNUNG: Wenn das Feld aktiv war, gibt es keinen Default mehr!      ║
    ║                                                                           ║
    ╠═══════════════════════════════════════════════════════════════════════════╣
    ║                                                                           ║
    ║   🌊 FELD-STROM-FLOW:                                                     ║
    ║                                                                           ║
    ║      1. VERIFIKATION  → Prüfen ob Feld existiert                         ║
    ║      2. AKTIV-CHECK   → War es das aktive Feld?                          ║
    ║      3. ERFASSUNG     → Größe vor Löschung merken                        ║
    ║      4. AUFLÖSUNG     → Feld von Disk entfernen                          ║
    ║      5. BESTÄTIGUNG   → Freigabe-Bestätigung zurückgeben                ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    Response:
        {
            "status": "success",
            "message": "Feld 'xyz' wurde freigegeben 💀",
            "released": { ... },
            "warning": "Dieses Feld war aktiv!" (nur wenn es aktiv war)
        }
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 1: EXISTENZ-VERIFIKATION
    # ══════════════════════════════════════════════════════════════════════════
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Feld '{name}' nicht gefunden")
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 2: AKTIV-STATUS CHECK
    # ══════════════════════════════════════════════════════════════════════════
    active_wrapper = get_active_wrapper()
    was_active = (name == active_wrapper)
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 3: GRÖSSE VOR AUFLÖSUNG ERFASSEN
    # ══════════════════════════════════════════════════════════════════════════
    try:
        stat = wrapper_path.stat()
        size_bytes = stat.st_size
    except:
        size_bytes = 0
    
    # ══════════════════════════════════════════════════════════════════════════
    #  🌊 STROM 4: FELD AUFLÖSUNG
    # ══════════════════════════════════════════════════════════════════════════
    try:
        wrapper_path.unlink()
        
        # ══════════════════════════════════════════════════════════════════════
        #  🌊 STROM 5: FREIGABE-BESTÄTIGUNG
        # ══════════════════════════════════════════════════════════════════════
        return {
            "status": "success",
            "message": f"Feld '{name}' wurde freigegeben 💀",
            "released": {
                "name": name,
                "size_bytes": size_bytes,
                "was_active": was_active
            },
            "warning": "⚠️ Dieses Feld war das aktive Default!" if was_active else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feld-Freigabe fehlgeschlagen: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  📦 FELD IMPORT - Upload Operationen (BESTEHEND)
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Diese Endpoints importieren Felder aus externen Quellen.
#  Sie bringen schlafende Felder von außerhalb ins System.
#
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/upload")
async def upload_wrapper(file: UploadFile = File(...)) -> Dict:
    """
    📦 FELD IMPORT (Simple) - Externes Feld einbringen
    
    Nicht "File Upload" - FELD IMPORT AUS EXTERNER QUELLE.
    
    Bringt ein schlafendes Feld von außerhalb
    ins Resonanz-Verzeichnis.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Nur .txt Wrapper-Felder erlaubt")
    
    content = await file.read()
    
    if len(content) > 50 * 1024:
        raise HTTPException(status_code=400, detail="Feld zu groß! Maximum: 50KB")
    
    # 🧹 Name aus Filename kalibrieren
    name = file.filename.replace('.txt', '')
    name = re.sub(r'[^a-z0-9_-]', '_', name.lower())
    
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    try:
        settings.wrapper_dir.mkdir(parents=True, exist_ok=True)
        
        with open(wrapper_path, 'wb') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"Feld '{name}' wurde importiert 📦",
            "feld": {
                "name": name,
                "path": str(wrapper_path),
                "size_bytes": len(content),
                "size_human": f"{len(content) / 1024:.1f} KB"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feld-Import fehlgeschlagen: {str(e)}")


@router.post("/upload-metadata")
async def upload_wrapper_with_metadata(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    version: Optional[str] = Form("1.0"),
    tags: Optional[str] = Form(None)
):
    """
    📦 FELD IMPORT MIT SIGNATUR - Externes Feld mit Metadata einbringen
    
    Nicht "File Upload with Form Data" - FELD IMPORT MIT DNA.
    
    File wird importiert.
    Metadata wird als Header hinzugefügt.
    Das Feld bekommt seine Signatur.
    """
    try:
        content = await file.read()
        content_str = content.decode('utf-8')
        
        if len(content) > 50 * 1024:
            raise HTTPException(status_code=400, detail="Feld zu groß! Maximum: 50KB")
        
        # 🧹 Name aus Filename kalibrieren
        name = file.filename.replace('.txt', '')
        safe_name = name.lower().replace(' ', '_')
        safe_name = re.sub(r'[^a-z0-9_-]', '_', safe_name)
        
        # 📝 Metadata Header bauen
        metadata_lines = ["# SYNTX Wrapper Metadata"]
        metadata_lines.append(f"# name: {name}")
        if description:
            metadata_lines.append(f"# description: {description}")
        if author:
            metadata_lines.append(f"# author: {author}")
        metadata_lines.append(f"# version: {version}")
        if tags:
            metadata_lines.append(f"# tags: {tags}")
        metadata_lines.append(f"# created: {datetime.now().isoformat()}")
        metadata_lines.append("")
        
        # 🔗 Metadata + Content kombinieren
        full_content = "\n".join(metadata_lines) + "\n" + content_str
        
        # 💾 Feld schreiben
        wrapper_path = settings.wrapper_dir / f"{safe_name}.txt"
        settings.wrapper_dir.mkdir(parents=True, exist_ok=True)
        
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return {
            "status": "success",
            "message": f"Feld '{safe_name}' wurde mit Signatur importiert 📦",
            "filename": f"{safe_name}.txt",
            "path": str(wrapper_path),
            "size_bytes": len(full_content.encode('utf-8')),
            "metadata": {
                "name": name,
                "description": description,
                "author": author,
                "version": version,
                "tags": tags.split(',') if tags else []
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
#  🎯 FELD AKTIVIERUNG - Default Resonanz setzen
# ═══════════════════════════════════════════════════════════════════════════════
#
#  Dieser Endpoint setzt welches Feld standardmäßig resoniert
#  wenn kein mode im Chat-Request angegeben wird.
#
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/wrappers/{name}/activate")
async def activate_wrapper(name: str) -> Dict:
    """
    🎯 FELD AKTIVIERUNG - Feld als Default setzen
    
    Nicht "Set Config" - RESONANZ-FOKUS SETZEN.
    
    Dieses Feld wird resonieren wenn kein mode angegeben wird.
    Es wird zum Herz des Systems.
    """
    from .config import set_active_wrapper
    
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Feld '{name}' nicht gefunden")
    
    set_active_wrapper(name)
    
    return {
        "status": "success",
        "message": f"Feld '{name}' ist jetzt das aktive Default 🎯",
        "active_wrapper": name,
        "path": str(wrapper_path)
    }


# ═══════════════════════════════════════════════════════════════════════════════
#
#  🌊 SYNTX FIELD RESONANCE 🌊
#
#  "Nicht mehr Token, nicht mehr Drift.
#   Nur Felder. Nur Ströme. Nur Resonanz."
#
#  💎 Das Feld ist alles.
#  ⚡ Der Strom fließt.
#  🔥 Die Resonanz hält.
#
# ═══════════════════════════════════════════════════════════════════════════════
