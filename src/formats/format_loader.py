"""
SYNTX FORMAT LOADER v3.0 - MIT VERERBUNG + DOMAINS
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

FORMATS_DIR = Path("/opt/syntx-config/formats")


def _load_format_raw(format_name: str) -> Optional[Dict]:
    """Raw load ohne Cache für Vererbung"""
    format_path = FORMATS_DIR / f"{format_name}.json"
    if not format_path.exists():
        return None
    try:
        with open(format_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None


@lru_cache(maxsize=16)
def load_format(format_name: str) -> Optional[Dict]:
    """FORMAT LADEN MIT VERERBUNG - extends Key wird gemerged"""
    fmt = _load_format_raw(format_name)
    if not fmt:
        print(f"⚠️ Format nicht gefunden: {format_name}")
        return None
    
    if "extends" in fmt:
        parent = _load_format_raw(fmt["extends"])
        if parent:
            merged_fields = list(parent.get("fields", []))
            child_names = {f["name"] for f in fmt.get("fields", [])}
            merged_fields = [f for f in merged_fields if f["name"] not in child_names]
            merged_fields.extend(fmt.get("fields", []))
            fmt["fields"] = merged_fields
            if not fmt.get("domain"):
                fmt["domain"] = parent.get("domain")
    return fmt


def get_format_fields(format_name: str, language: str = "de") -> List[Dict]:
    """FELD-DEFINITIONEN HOLEN"""
    format_data = load_format(format_name)
    if not format_data:
        return []
    fields = []
    for field in format_data.get("fields", []):
        headers = field.get("headers", {})
        header_list = headers.get(language, headers.get("de", []))
        header = header_list[0] if header_list else field.get("name", "Unknown")
        descriptions = field.get("description", {})
        description = descriptions.get(language, descriptions.get("de", ""))
        keywords = field.get("keywords", {})
        keyword_list = keywords.get(language, keywords.get("de", []))
        fields.append({
            "name": field.get("name"),
            "header": header,
            "description": description,
            "keywords": keyword_list,
            "weight": field.get("weight", 0)
        })
    return fields


def get_recommended_wrapper(format_name: str) -> Optional[str]:
    """EMPFOHLENEN WRAPPER HOLEN"""
    fmt = load_format(format_name)
    return fmt.get("wrapper") if fmt else None


def build_format_prompt(format_name: str, language: str = "de") -> str:
    """FORMAT-PROMPT BAUEN"""
    fields = get_format_fields(format_name, language)
    if not fields:
        return ""
    field_names = [f["header"] for f in fields]
    field_list = "\n".join([f"  - {name}" for name in field_names])
    instruction = f"ANALYSE-FORMAT - Bitte fülle folgende Felder aus:\n{field_list}\nStrukturiere mit ### FELDNAME: als Header.\n"
    sections = [f"### {f['header']}:\n{f['description']}" for f in fields]
    fmt = load_format(format_name)
    intro = ""
    if fmt:
        desc = fmt.get("description", {})
        intro = desc.get(language, desc.get("de", "")) if isinstance(desc, dict) else ""
    return instruction + ("\n" + intro + "\n" if intro else "") + "\n\n".join(sections)


def build_dynamic_prompt(user_prompt: str, format_name: str, language: str = "de") -> Tuple[str, Dict]:
    """DYNAMISCHER PROMPT BUILDER"""
    format_section = build_format_prompt(format_name, language)
    fields = get_format_fields(format_name, language)
    wrapper = get_recommended_wrapper(format_name)
    if not format_section:
        return user_prompt, {"error": f"Format '{format_name}' nicht gefunden"}
    combined = f"AUFGABE: {user_prompt}\n\n{format_section}"
    return combined, {"format": format_name, "language": language, "fields_count": len(fields), "fields": [f["name"] for f in fields], "recommended_wrapper": wrapper}


def list_formats(domain: Optional[str] = None) -> List[str]:
    """ALLE FORMATE LISTEN - optional gefiltert nach domain"""
    if not FORMATS_DIR.exists():
        return []
    all_fmts = [f.stem for f in FORMATS_DIR.glob("*.json") if not f.stem.startswith('.')]
    if domain is None:
        return all_fmts
    return [n for n in all_fmts if (load_format(n) or {}).get("domain") == domain]


def get_all_domains() -> List[str]:
    """ALLE DOMAINS LISTEN"""
    domains = set()
    for n in list_formats():
        fmt = load_format(n)
        if fmt and fmt.get("domain"):
            domains.add(fmt["domain"])
    return sorted(list(domains))


def get_format_summary(format_name: str) -> Optional[Dict]:
    """FORMAT SUMMARY"""
    fmt = load_format(format_name)
    if not fmt:
        return None
    return {"name": format_name, "domain": fmt.get("domain"), "fields_count": len(fmt.get("fields", [])), "wrapper": fmt.get("wrapper"), "languages": fmt.get("languages", ["de"])}


def clear_format_cache():
    """CACHE LEEREN"""
    load_format.cache_clear()
