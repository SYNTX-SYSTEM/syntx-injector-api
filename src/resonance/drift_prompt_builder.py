"""
SYNTX Drift Scoring - Prompt Builder
Builds dynamic GPT prompts from templates
"""
import json
from pathlib import Path
from typing import Dict, List, Any

PROMPTS_DIR = Path("/opt/syntx-config/prompts")


def load_template(template_id: str) -> Dict[str, Any]:
    """Load prompt template from file"""
    template_path = PROMPTS_DIR / f"{template_id}.json"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{template_id}' not found at {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_templates() -> List[Dict[str, Any]]:
    """List all available templates"""
    templates = []
    
    for template_file in PROMPTS_DIR.glob("*.json"):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
                templates.append({
                    "id": template.get("id"),
                    "name": template.get("name"),
                    "version": template.get("version"),
                    "description": template.get("description")
                })
        except Exception as e:
            print(f"Error loading template {template_file}: {e}")
    
    return templates


def build_response_format(fields: List[str], field_schema: Dict, summary_schema: Dict) -> str:
    """Build JSON response format string with all fields"""
    field_entries = []
    
    for field in fields:
        field_entry = f'''  "{field}": {{
    "score": 0.0,
    "drift_type": "...",
    "masking": false,
    "reason": "...",
    "dominant_phrases": ["...", "..."]
  }}'''
        field_entries.append(field_entry)
    
    summary_entry = '''  "summary": {
    "drift_detected": true,
    "dominant_drift_types": ["..."],
    "high_resonance_fields": ["..."],
    "resonance_score": 0.0
  }'''
    
    all_entries = ",\n".join(field_entries) + ",\n" + summary_entry
    
    return "{\n" + all_entries + "\n}"


def build_prompt(
    template_id: str,
    fields: List[str],
    response_text: str
) -> Dict[str, Any]:
    """
    Build complete GPT prompt from template
    
    Args:
        template_id: Template to use
        fields: List of field names to analyze
        response_text: Full Mistral response text
    
    Returns:
        Complete GPT API payload
    """
    template = load_template(template_id)
    
    # Build fields list string
    fields_list = "**, **".join(fields)
    fields_list = f"**{fields_list}**"
    
    # Build response format JSON
    response_format = build_response_format(
        fields,
        template["field_schema"],
        template["summary_schema"]
    )
    
    # Replace placeholders in user prompt
    user_prompt = template["user_prompt_template"]
    user_prompt = user_prompt.replace("{FIELDS_LIST}", fields_list)
    user_prompt = user_prompt.replace("{RESPONSE_TEXT}", response_text)
    user_prompt = user_prompt.replace("{RESPONSE_FORMAT}", response_format)
    
    # Build complete API payload
    payload = {
        "model": template["model_config"]["model"],
        "temperature": template["model_config"]["temperature"],
        "max_tokens": template["model_config"].get("max_tokens", 2000),
        "messages": [
            {
                "role": "system",
                "content": template["system_prompt"]
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }
    
    return payload


def save_template(template_data: Dict[str, Any]) -> bool:
    """Save a new or updated template"""
    template_id = template_data.get("id")
    if not template_id:
        raise ValueError("Template must have an 'id' field")
    
    template_path = PROMPTS_DIR / f"{template_id}.json"
    
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, indent=2, ensure_ascii=False)
    
    return True


def delete_template(template_id: str) -> bool:
    """Delete a template"""
    if template_id == "drift_scoring_default":
        raise ValueError("Cannot delete default template")
    
    template_path = PROMPTS_DIR / f"{template_id}.json"
    
    if template_path.exists():
        template_path.unlink()
        return True
    
    return False


# ═══════════════════════════════════════════════════════════════════════════════
#  🔥 GPT AUTO-TRIGGER EXTENSION - LIVE DATA MODE
# ═══════════════════════════════════════════════════════════════════════════════

def build_prompt_from_data(
    template_id: str,
    format_name: str,
    fields: List[str],
    response_text: str
) -> Dict:
    """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║          🔥 BUILD GPT PROMPT FROM LIVE DATA (AUTO-TRIGGER) 🔥            ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    
    ZWECK:
        Baut GPT-4 Scoring Prompt DIREKT aus Live-Daten
        Kein File-Loading - Pure Field Resonanz
        
    VERWENDUNG:
        Nach Mistral Response für Auto-Trigger
        
    PARAMETER:
        template_id: Entity Config ID (z.B. "gpt4_semantic_entity")
        format_name: Format Name (z.B. "sigma")
        fields: Liste der Field Names aus format.json
        response_text: Mistral's generierter Response Text
        
    RÜCKGABE:
        OpenAI API Payload (Dict mit model, temperature, messages)
        
    FELD-KALIBRIERUNG:
        - System Prompt aus Entity Config
        - User Prompt Template mit Platzhaltern
        - Field Definitions dynamisch generiert
        - Response Text eingebettet
        
    STROM-FLUSS:
        Entity Config → Template Extraction → Field Injection → API Payload
    """
    # Load Entity Configuration
    entity_path = Path(f"/opt/syntx-config/scoring_entities/{template_id}.json")
    
    if not entity_path.exists():
        raise FileNotFoundError(f"❌ Entity config nicht gefunden: {template_id}")
    
    with open(entity_path, 'r', encoding='utf-8') as f:
        entity = json.load(f)
    
    # Extract Prompt Templates
    system_prompt = entity["prompt_templates"]["system_prompt"]
    user_template = entity["prompt_templates"]["user_prompt_template"]
    
    # Build Field Definitions String
    field_definitions = "\n".join([f"- {field}" for field in fields])
    
    # Replace Placeholders in User Prompt
    user_prompt = user_template.replace("{FORMAT_NAME}", format_name)
    user_prompt = user_prompt.replace("{FIELD_DEFINITIONS}", field_definitions)
    user_prompt = user_prompt.replace("{RESPONSE_TEXT}", response_text)
    
    # Build OpenAI API Payload
    payload = {
        "model": entity["llm_configuration"]["model"],
        "temperature": entity["llm_configuration"]["temperature"],
        "max_tokens": entity["llm_configuration"]["max_tokens"],
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }
    
    return payload
