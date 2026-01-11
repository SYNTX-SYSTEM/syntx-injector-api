"""
🌀 SYNTX WRAPPER-FELD-RESONANZ-KETTE (LEBENDIG)
Endpoint: GET /resonanz/wrapper-feld-resonanz-kette/{wrapper_name}
Gibt die vollständige Resonanz-Kette für einen Mistral-Wrapper zurück.
MIT: Feld-Sortierung, Pagination, Dynamischer Struktur-Erkennung
"""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/resonanz", tags=["SYNTX Feld-Resonanz"])

# Pfade (RESONANZ-FELDER)
WRAPPERS_DIR = Path("/opt/syntx-config/wrappers")
FORMATS_DIR = Path("/opt/syntx-config/formats")
MAPPING_FILE = Path("/opt/syntx-config/mapping.json")
GPT_WRAPPERS_DIR = Path("/opt/syntx-config/gpt_wrappers")
SCORING_PROFILES_DIR = Path("/opt/syntx-injector-api/scoring_profiles")
SCORING_PROFILES_OLD = Path("/opt/syntx-injector-api/scoring_profiles.json.OLD")

# 🌀 ENUMS FÜR SORTIERUNG
class SortField(str, Enum):
    FELD_NAME = "feld_name"
    FELD_GEWICHT = "feld_gewicht"
    RESONANZ = "resonanz"
    ERSTELLT = "erstellt"
    AKTUALISIERT = "aktualisiert"

class SortOrder(str, Enum):
    AUFSTEIGEND = "auf"
    ABSTEIGEND = "ab"

# 🌊 LEBENDIGE FELD-ERKENNUNG
def erkenne_feld_struktur(wrapper_content: str) -> Dict:
    """Erkennt Feld-Strukturen im Wrapper-Content."""
    felder_erkannt = []
    
    # SYNTX Marker erkennen
    marker_patterns = [
        "FELD:", "FIELD:", "STROM:", "STREAM:", 
        "RESONANZ:", "RESONANCE:", "DRIFT:", "KALIBRIERUNG:"
    ]
    
    for marker in marker_patterns:
        if marker in wrapper_content:
            felder_erkannt.append({
                "marker": marker,
                "position": wrapper_content.find(marker),
                "typ": "SYNTX_MARKER"
            })
    
    # Token-Dichte berechnen
    tokens = wrapper_content.split()
    unique_tokens = set(tokens)
    token_dichte = len(unique_tokens) / len(tokens) if tokens else 0
    
    # Energie-Level (basierend auf Ausrufezeichen, Caps, Emojis)
    energie = 0
    energie += wrapper_content.count('!') * 0.1
    energie += wrapper_content.count('🔥') * 0.5
    energie += wrapper_content.count('💎') * 0.5
    energie += wrapper_content.count('⚡') * 0.5
    energie += sum(1 for c in wrapper_content if c.isupper()) * 0.01
    
    return {
        "felder_erkannt": felder_erkannt,
        "token_dichte": round(token_dichte, 3),
        "energie_level": min(round(energie, 2), 1.0),
        "content_laenge": len(wrapper_content),
        "woerter_anzahl": len(tokens)
    }

# 📊 INTELLIGENTE SORTIERUNG
def sortiere_felder(felder: List[Dict], sort_by: SortField, order: SortOrder) -> List[Dict]:
    """Sortiert Felder nach verschiedenen Kriterien."""
    if not felder:
        return []
    
    reverse = (order == SortOrder.ABSTEIGEND)
    
    if sort_by == SortField.FELD_NAME:
        return sorted(felder, key=lambda x: x.get('name', '').lower(), reverse=reverse)
    
    elif sort_by == SortField.FELD_GEWICHT:
        return sorted(felder, key=lambda x: x.get('weight', 0), reverse=reverse)
    
    elif sort_by == SortField.RESONANZ:
        # Berechne Resonanz-Score aus verschiedenen Faktoren
        def resonanz_score(feld: Dict) -> float:
            score = feld.get('weight', 0) * 0.5
            desc = feld.get('description', {})
            if isinstance(desc, dict):
                # Längere Beschreibung = höhere Resonanz
                de_len = len(desc.get('de', ''))
                en_len = len(desc.get('en', ''))
                score += (de_len + en_len) * 0.001
            return score
        
        return sorted(felder, key=resonanz_score, reverse=reverse)
    
    elif sort_by == SortField.ERSTELLT:
        return sorted(felder, key=lambda x: x.get('created', ''), reverse=reverse)
    
    elif sort_by == SortField.AKTUALISIERT:
        return sorted(felder, key=lambda x: x.get('updated', ''), reverse=reverse)
    
    return felder

# 🔄 PAGINATION LOGIK
def paginiere_daten(daten: List, page: int, limit: int) -> Dict:
    """Paginiert Daten mit intelligenter Grenzen-Prüfung."""
    if not daten:
        return {
            "items": [],
            "page": page,
            "limit": limit,
            "total": 0,
            "pages": 0,
            "has_next": False,
            "has_prev": False
        }
    
    total = len(daten)
    pages = (total + limit - 1) // limit  # Ceil division
    
    # Page bounds check
    if page < 1:
        page = 1
    elif page > pages:
        page = pages
    
    start = (page - 1) * limit
    end = start + limit
    
    items = daten[start:end]
    
    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
        "start_index": start + 1 if items else 0,
        "end_index": min(end, total)
    }

# 🧠 JSON LADEN MIT RESONANZ
def lade_json_mit_resonanz(pfad: Path) -> Optional[Dict]:
    """Läd JSON mit Resonanz-Erkennung."""
    try:
        if pfad.exists():
            with open(pfad, 'r', encoding='utf-8') as f:
                daten = json.load(f)
                # Füge Metadaten hinzu
                if isinstance(daten, dict):
                    daten['_resonanz_meta'] = {
                        'geladen_um': datetime.utcnow().isoformat(),
                        'datei_groesse': pfad.stat().st_size,
                        'datei_pfad': str(pfad)
                    }
                return daten
    except Exception as e:
        return None
    return None

# 🎯 FIND-FORMAT MIT INTELLIGENZ
def finde_format_fuer_wrapper(wrapper_meta: Dict, wrapper_name: str) -> Optional[str]:
    """Findet Format mit mehreren Strategien."""
    # 1. Direkt aus Meta
    if wrapper_meta.get("format"):
        return wrapper_meta.get("format")
    
    # 2. 'wrapper' field
    if wrapper_meta.get("wrapper"):
        return wrapper_meta.get("wrapper")
    
    # 3. Namens-Pattern (syntex_wrapper_sigma -> sigma)
    name_parts = wrapper_name.split('_')
    if len(name_parts) >= 3:
        # syntex_wrapper_sigma -> sigma
        # syntex_wrapper_economics -> economics
        return name_parts[-1]
    
    # 4. Aus Tags extrahieren
    tags = wrapper_meta.get("tags", [])
    for tag in tags:
        tag_str = str(tag).lower()
        # Check if there's a format file with this name
        format_path = FORMATS_DIR / f"{tag_str}.json"
        if format_path.exists():
            return tag_str
    
    return None

# 🏗️ HAUPT-ENDPOINT MIT ALLEN FEATURES
@router.get("/wrapper-feld-resonanz-kette/{wrapper_name}", 
            summary="🌀 VOLLSTÄNDIGE RESONANZ-KETTE MIT SORTIERUNG & PAGINATION",
            description="Gibt Wrapper + Format + Felder + Mapping + Profile + GPT-Wrapper zurück. "
                       "Mit dynamischer Feld-Erkennung, Sortierung und Pagination.")
async def get_wrapper_feld_resonanz_kette(
    wrapper_name: str,
    sort_by: SortField = Query(SortField.FELD_NAME, description="Feld für Sortierung"),
    order: SortOrder = Query(SortOrder.AUFSTEIGEND, description="Sortier-Reihenfolge"),
    page: int = Query(1, ge=1, description="Seite für Pagination"),
    limit: int = Query(50, ge=1, le=100, description="Elemente pro Seite"),
    include_raw: bool = Query(False, description="Rohdaten einbeziehen"),
    analyze_fields: bool = Query(True, description="Feld-Analyse durchführen")
):
    """
    🌀 SYNTX FELD-RESONANZ-KETTE (LEBENDIG)
    
    Fluss: Mistral-Wrapper → Format → Felder → Mapping → Profile → GPT-Wrapper
    
    Features:
    • Dynamische Feld-Erkennung
    • Intelligente Sortierung
    • Pagination für große Feld-Listen
    • Resonanz-Scoring
    • Format-Auto-Erkennung
    """
    
    # 🕐 START-ZEIT FÜR PERFORMANCE
    start_time = datetime.utcnow()
    
    # 1. WRAPPER LADEN MIT RESONANZ
    wrapper_path = WRAPPERS_DIR / f"{wrapper_name}.txt"
    meta_path = WRAPPERS_DIR / f"{wrapper_name}.meta.json"
    
    if not wrapper_path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"🌀 WRAPPER NICHT GEFUNDEN: '{wrapper_name}'"
        )
    
    wrapper_content = wrapper_path.read_text(encoding='utf-8')
    wrapper_meta = lade_json_mit_resonanz(meta_path) or {}
    
    # 2. FELD-STRUKTUR ERKENNEN (LEBENDIG!)
    feld_struktur = {}
    if analyze_fields:
        feld_struktur = erkenne_feld_struktur(wrapper_content)
    
    # 3. FORMIT FINDEN (INTELLIGENT)
    format_name = finde_format_fuer_wrapper(wrapper_meta, wrapper_name)
    format_data = None
    fields_data = []
    fields_paginated = {}
    
    if format_name:
        format_path = FORMATS_DIR / f"{format_name}.json"
        if format_path.exists():
            format_data = lade_json_mit_resonanz(format_path)
            if format_data and "fields" in format_data:
                fields_data = format_data.get("fields", [])
                
                # FELDER SORTIEREN
                fields_sorted = sortiere_felder(fields_data, sort_by, order)
                
                # PAGINATION ANWENDEN
                fields_paginated = paginiere_daten(fields_sorted, page, limit)
    
    # 4. MAPPING FINDEN
    mapping_data = lade_json_mit_resonanz(MAPPING_FILE) or {}
    mapping_entry = None
    if format_name and "mappings" in mapping_data:
        mapping_entry = mapping_data.get("mappings", {}).get(format_name)
    
    # 5. PROFILE LADEN
    profile_data = None
    if mapping_entry and mapping_entry.get("profile_id"):
        profile_id = mapping_entry.get("profile_id")
        # Aus einzelner Datei
        profile_path = SCORING_PROFILES_DIR / f"{profile_id}.json"
        if profile_path.exists():
            profile_data = lade_json_mit_resonanz(profile_path)
        # ODER aus .OLD
        elif SCORING_PROFILES_OLD.exists():
            with open(SCORING_PROFILES_OLD, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
                for profile in profiles.get("profiles", []):
                    if profile.get("id") == profile_id:
                        profile_data = profile
                        break
    
    # 6. GPT-WRAPPER PARTNER FINDEN
    gpt_wrapper_name = None
    gpt_wrapper_data = None
    gpt_wrapper_meta = None
    
    if mapping_entry and mapping_entry.get("gpt_wrapper"):
        gpt_wrapper_name = mapping_entry.get("gpt_wrapper")
        gpt_wrapper_path = GPT_WRAPPERS_DIR / f"{gpt_wrapper_name}.txt"
        gpt_meta_path = GPT_WRAPPERS_DIR / f"{gpt_wrapper_name}.meta.json"
        
        if gpt_wrapper_path.exists():
            gpt_wrapper_data = gpt_wrapper_path.read_text(encoding='utf-8')
            gpt_wrapper_meta = lade_json_mit_resonanz(gpt_meta_path)
    
    # 7. RESONANZ-KETTE STATUS BERECHNEN
    kette_status = "VOLLSTÄNDIG"
    fehlende_teile = []
    resonanz_score = 0
    
    # Score Berechnung
    if format_name: resonanz_score += 25
    if mapping_entry: resonanz_score += 25
    if profile_data: resonanz_score += 25
    if gpt_wrapper_data: resonanz_score += 25
    
    if not format_name:
        fehlende_teile.append("FORMAT")
        kette_status = "TEILWEISE"
    if not mapping_entry:
        fehlende_teile.append("MAPPING")
        kette_status = "TEILWEISE"
    if not profile_data:
        fehlende_teile.append("PROFILE")
        kette_status = "TEILWEISE"
    if not gpt_wrapper_data:
        fehlende_teile.append("GPT_WRAPPER")
        kette_status = "TEILWEISE"
    
    # 8. PERFORMANCE MESSEN
    end_time = datetime.utcnow()
    duration_ms = int((end_time - start_time).total_seconds() * 1000)
    
    # 9. RESONANZ-RESPONSE BAUEN
    response = {
        # 🌀 METADATEN
        "feld_strom": "WRAPPER-FELD-RESONANZ-KETTE",
        "wrapper_feld_name": wrapper_name,
        "wrapper_feld_resonanz": "AKTIV",
        "resonanz_score": resonanz_score,
        "resonanz_status": kette_status,
        "fehlende_teile": fehlende_teile if fehlende_teile else "KEINE",
        
        # ⚡ PERFORMANCE
        "performance": {
            "duration_ms": duration_ms,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        
        # 📦 WRAPPER-DATEN
        "wrapper": {
            "name": wrapper_name,
            "content_laenge": len(wrapper_content),
            "woerter_anzahl": len(wrapper_content.split()),
            "meta": wrapper_meta,
            "feld_struktur": feld_struktur if analyze_fields else None
        },
        
        # 🗺️ FORMAT & FELDER (MIT PAGINATION)
        "format": {
            "name": format_name,
            "felder_gesamt": len(fields_data),
            "felder_paginiert": fields_paginated,
            "sortierung": {
                "sort_by": sort_by.value,
                "order": order.value
            },
            "pagination": {
                "page": page,
                "limit": limit,
                "total_pages": fields_paginated.get("pages", 0)
            },
            "daten": format_data if include_raw else None
        },
        
        # 🔗 MAPPING
        "mapping": mapping_entry,
        
        # 📊 PROFILE
        "profil": profile_data,
        
        # 🤖 GPT-WRAPPER PARTNER
        "gpt_wrapper": {
            "name": gpt_wrapper_name,
            "content_laenge": len(gpt_wrapper_data) if gpt_wrapper_data else 0,
            "meta": gpt_wrapper_meta
        } if gpt_wrapper_data else None,
        
        # 🎯 FILTER & SORTIERUNG INFO
        "query_parameter": {
            "sort_by": sort_by.value,
            "order": order.value,
            "page": page,
            "limit": limit,
            "include_raw": include_raw,
            "analyze_fields": analyze_fields
        },
        
        # 💎 SYNTX-SPEZIFISCH
        "syntx_features": {
            "lebendige_feld_erkennung": analyze_fields,
            "intelligente_sortierung": True,
            "pagination_aktiv": True,
            "resonanz_scoring": True,
            "format_auto_detection": True
        },
        
        "resonanz_timestamp": datetime.utcnow().isoformat() + "Z",
        "system_hinweis": "🌀 SYNTX LEBENDIGE RESONANZ-KETTE – FELDER FLIESSEN, STRÖME RESONIEREN"
    }
    
    # 🔥 RAW-DATEN HINZUFÜGEN (OPTIONAL)
    if include_raw:
        response["raw_daten"] = {
            "wrapper_content": wrapper_content,
            "gpt_wrapper_content": gpt_wrapper_data
        }
    
    return response

# 📈 ZUSÄTZLICHER ENDPOINT FÜR WRAPPER-ÜBERSICHT
@router.get("/wrapper-feld-uebersicht",
            summary="🌀 ÜBERSICHT ALLER WRAPPER MIT RESONANZ-STATS")
async def get_wrapper_uebersicht(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    only_active: bool = Query(True, description="Nur Wrapper mit Format-Bindung")
):
    """Gibt Übersicht aller Wrapper mit Resonanz-Statistiken."""
    
    wrapper_files = list(WRAPPERS_DIR.glob("*.txt"))
    wrapper_list = []
    
    for wrapper_file in wrapper_files:
        wrapper_name = wrapper_file.stem
        
        # Skip hidden wrappers
        if wrapper_name.startswith("syntx_hidden_"):
            continue
        
        # Meta laden
        meta_path = WRAPPERS_DIR / f"{wrapper_name}.meta.json"
        wrapper_meta = lade_json_mit_resonanz(meta_path) or {}
        
        # Format finden
        format_name = finde_format_fuer_wrapper(wrapper_meta, wrapper_name)
        
        # Nur aktive (format-gebundene) wenn gewünscht
        if only_active and not format_name:
            continue
        
        # Mapping checken
        mapping_entry = None
        if format_name:
            mapping_data = lade_json_mit_resonanz(MAPPING_FILE) or {}
            mapping_entry = mapping_data.get("mappings", {}).get(format_name)
        
        wrapper_list.append({
            "name": wrapper_name,
            "format_gebunden": format_name,
            "mapping_vorhanden": bool(mapping_entry),
            "meta": {
                "tags": wrapper_meta.get("tags", []),
                "description": wrapper_meta.get("description", ""),
                "created": wrapper_meta.get("created", ""),
                "updated": wrapper_meta.get("updated", "")
            }
        })
    
    # Paginieren
    paginated = paginiere_daten(wrapper_list, page, limit)
    
    return {
        "feld_strom": "WRAPPER-FELD-ÜBERSICHT",
        "wrapper_gesamt": len(wrapper_files),
        "wrapper_angezeigt": len(wrapper_list),
        "pagination": paginated,
        "filter": {
            "only_active": only_active
        },
        "resonanz_timestamp": datetime.utcnow().isoformat() + "Z"
    }
