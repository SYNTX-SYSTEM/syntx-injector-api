"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔥 SYNTX FORMAT LOADER v3.1 - MIT FELD-TYPEN + VERERBUNG + DOMAINS         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

FORMATS_DIR = Path("/opt/syntx-config/formats")


def _load_format_raw(format_name: str) -> Optional[Dict]:
    """📖 Raw load ohne Cache für Vererbung"""
    spell_path = FORMATS_DIR / f"{format_name}.json"
    if not spell_path.exists():
        return None
    try:
        with open(spell_path, 'r', encoding='utf-8') as tome:
            return json.load(tome)
    except:
        return None


# @lru_cache(maxsize=16)  # DISABLED - caused stale reads
def load_format(format_name: str) -> Optional[Dict]:
    """🔮 FORMAT LADEN MIT VERERBUNG"""
    fmt = _load_format_raw(format_name)
    if not fmt:
        print(f"⚠️ Format '{format_name}' nicht gefunden")
        return None
    if "extends" in fmt:
        parent = _load_format_raw(fmt["extends"])
        if parent:
            merged = list(parent.get("fields", []))
            child_names = {f["name"] for f in fmt.get("fields", [])}
            merged = [f for f in merged if f["name"] not in child_names]
            merged.extend(fmt.get("fields", []))
            fmt["fields"] = merged
            if not fmt.get("domain"):
                fmt["domain"] = parent.get("domain")
    return fmt


def get_format_fields(format_name: str, language: str = "de") -> List[Dict]:
    """🔧 FELD-DEFINITIONEN HOLEN"""
    fmt = load_format(format_name)
    if not fmt:
        return []
    fields = []
    for field in fmt.get("fields", []):
        headers = field.get("headers", {})
        header_list = headers.get(language, headers.get("de", []))
        header = header_list[0] if header_list else field.get("name", "Unknown")
        descs = field.get("description", {})
        desc = descs.get(language, descs.get("de", ""))
        kws = field.get("keywords", {})
        kw_list = kws.get(language, kws.get("de", []))
        fields.append({"name": field.get("name"), "header": header, "description": desc, "keywords": kw_list, "weight": field.get("weight", 0), "type": field.get("type", "text")})
    return fields


def get_recommended_wrapper(format_name: str) -> Optional[str]:
    fmt = load_format(format_name)
    return fmt.get("wrapper") if fmt else None


def build_format_prompt(format_name: str, language: str = "de") -> str:
    """🔥 FORMAT-PROMPT MIT FELD-TYPEN (text/list/rating/keywords)"""
    fields = get_format_fields(format_name, language)
    if not fields:
        return ""
    hints = []
    for f in fields:
        ftype = f.get("type", "text")
        hint = f["header"]
        if ftype == "list": hint += " (Bullet Points)"
        elif ftype == "rating": hint += " (Skala 1-10)"
        elif ftype == "keywords": hint += " (Komma-separiert)"
        hints.append(f"  - {hint}")
    instruction = "ANALYSE-FORMAT - Felder:\n" + "\n".join(hints) + "\n"
    sections = []
    for f in fields:
        ftype, h, d = f.get("type", "text"), f["header"], f["description"]
        if ftype == "list": sections.append(f"### {h}:\n{d}\n(Bullet Points)")
        elif ftype == "rating": sections.append(f"### {h}:\n{d}\n(Skala 1-10)")
        elif ftype == "keywords": sections.append(f"### {h}:\n{d}\n(Komma-separiert)")
        else: sections.append(f"### {h}:\n{d}")
    fmt = load_format(format_name)
    intro = fmt.get("description", {}).get(language, "") if fmt else ""
    return instruction + ("\n" + intro + "\n" if intro else "") + "\n\n".join(sections)


def build_dynamic_prompt(user_prompt: str, format_name: str, language: str = "de") -> Tuple[str, Dict]:
    section = build_format_prompt(format_name, language)
    fields = get_format_fields(format_name, language)
    wrapper = get_recommended_wrapper(format_name)
    if not section: return user_prompt, {"error": f"Format '{format_name}' nicht gefunden"}
    return f"AUFGABE: {user_prompt}\n\n{section}", {"format": format_name, "fields_count": len(fields), "fields": [f["name"] for f in fields], "wrapper": wrapper}


def list_formats(domain: Optional[str] = None) -> List[str]:
    if not FORMATS_DIR.exists(): return []
    all_fmts = [f.stem for f in FORMATS_DIR.glob("*.json") if not f.stem.startswith('.')]
    if domain is None: return all_fmts
    return [n for n in all_fmts if (load_format(n) or {}).get("domain") == domain]


def get_all_domains() -> List[str]:
    domains = set()
    for n in list_formats():
        fmt = load_format(n)
        if fmt and fmt.get("domain"): domains.add(fmt["domain"])
    return sorted(list(domains))


def get_format_summary(format_name: str) -> Optional[Dict]:
    fmt = load_format(format_name)
    if not fmt: return None
    return {"name": format_name, "domain": fmt.get("domain"), "fields_count": len(fmt.get("fields", [])), "wrapper": fmt.get("wrapper")}


def clear_format_cache():
    load_format.cache_clear()
