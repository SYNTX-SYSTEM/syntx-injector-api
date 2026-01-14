"""
🔥 SYNTX MISTRAL PROMPT BUILDER 🔥

Baut Mistral-Prompts dynamisch aus:
- Wrapper TXT (Kalibrierung)
- Format JSON (Feld-Definitionen)
- User Input (Thema)

Speichert mit vollständiger Referenz.
"""
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import json

PROMPTS_GENERATED_DIR = Path("/opt/syntx-config/prompts_generated")


def build_mistral_prompt(
    wrapper_text: str,
    user_input: str,
    wrapper_name: str = "unknown",
    format_name: Optional[str] = None,
    format_data: Optional[Dict] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    🔥 MISTRAL PROMPT BUILDER - Das Herzstück
    
    Args:
        wrapper_text: Wrapper Content (aus syntex_wrapper_sigma.txt)
        user_input: User Prompt ("Analysiere Gesellschaft")
        wrapper_name: Name des Wrappers (für Meta)
        format_name: Name des Formats (für Meta)
        format_data: Format JSON (mit fields[])
    
    Returns:
        (final_prompt, metadata)
    """
    parts = []
    
    # TEIL 1: WRAPPER
    if wrapper_text:
        parts.append(wrapper_text)
    
    # TEIL 2: FORMAT SECTION (dynamisch gebaut!)
    format_section = ""
    if format_data and "fields" in format_data:
        format_lines = []
        
        for field in format_data["fields"]:
            field_name = field.get("name", "")
            field_desc = field.get("description", {})
            
            # Deutsche Beschreibung bevorzugen
            desc_text = field_desc.get("de", field_desc.get("en", ""))
            
            if field_name and desc_text:
                format_lines.append(f"### {field_name}:")
                format_lines.append(desc_text)
                format_lines.append("")  # Leerzeile
        
        format_section = "\n".join(format_lines)
    
    # TEIL 3: FORMAT INJECTION (wenn vorhanden)
    if format_section:
        parts.append("\n" + "═" * 80)
        parts.append("📋 ANALYSE-FORMAT - Bitte fülle folgende Felder aus:")
        parts.append("═" * 80 + "\n")
        parts.append(format_section)
        parts.append("═" * 80)
        parts.append(f"🎯 THEMA ZUR ANALYSE: {user_input}")
        parts.append("═" * 80 + "\n")
        parts.append("Bitte analysiere das obige Thema und fülle ALLE Felder vollständig aus.")
    else:
        # Kein Format = einfach User Input anhängen
        parts.append(user_input)
    
    # KOMBINIERE
    final_prompt = "\n\n".join(parts)
    
    # METADATA
    metadata = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "wrapper_name": wrapper_name,
        "format_name": format_name,
        "user_input": user_input,
        "prompt_length": len(final_prompt),
        "has_format": format_section != "",
        "field_count": len(format_data.get("fields", [])) if format_data else 0
    }
    
    return final_prompt, metadata


def save_mistral_prompt(
    prompt: str,
    metadata: Dict[str, Any],
    wrapper_name: str = "unknown",
    format_name: Optional[str] = None
) -> Dict[str, str]:
    """
    💾 SPEICHERE MISTRAL PROMPT MIT REFERENZ
    
    Returns:
        Paths dict with prompt_file and meta_file
    """
    # CREATE DIRECTORY
    PROMPTS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    
    # FILENAME
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    format_part = f"_format_{format_name}" if format_name else ""
    filename_base = f"{timestamp}_wrapper_{wrapper_name}{format_part}"
    
    prompt_file = PROMPTS_GENERATED_DIR / f"{filename_base}.txt"
    meta_file = PROMPTS_GENERATED_DIR / f"{filename_base}.meta.json"
    
    # SAVE PROMPT
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    # ERWEITERE METADATA
    metadata["files"] = {
        "prompt": str(prompt_file),
        "meta": str(meta_file),
        "wrapper_source": f"/opt/syntx-config/wrappers/{wrapper_name}.txt",
        "format_source": f"/opt/syntx-config/formats/{format_name}.json" if format_name else None
    }
    metadata["saved_at"] = datetime.utcnow().isoformat() + "Z"
    
    # SAVE META
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Mistral Prompt gespeichert: {filename_base}")
    
    return {
        "prompt_file": str(prompt_file),
        "meta_file": str(meta_file),
        "filename_base": filename_base
    }


def save_mistral_response(
    response_text: str,
    prompt_filename_base: str
) -> str:
    """
    💎 SPEICHERE MISTRAL RESPONSE
    
    Args:
        response_text: Die Mistral Response
        prompt_filename_base: Base filename (ohne Extension) vom Prompt
    
    Returns:
        Path zur gespeicherten Response
    """
    response_file = PROMPTS_GENERATED_DIR / f"{prompt_filename_base}.response.txt"
    
    try:
        with open(response_file, 'w', encoding='utf-8') as f:
            f.write(response_text)
        
        print(f"💎 Response gespeichert: {prompt_filename_base}.response.txt")
        
        return str(response_file)
    except Exception as e:
        print(f"❌ Response Save Error: {e}")
        return None
