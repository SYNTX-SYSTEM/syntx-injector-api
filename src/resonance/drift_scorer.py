"""
SYNTX Drift Scoring - Core Logic
GPT-4 based semantic drift analysis
💎 MIT LOGGING STROM 💎
"""
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from .drift_prompt_builder import build_prompt
from .drift_logger import DriftStrom

PROCESSED_DIR = Path("/opt/syntx-config/processed")
RESULTS_DIR = Path("/opt/syntx-config/drift_results")


def load_processed_file(filename: str) -> tuple[Dict, str]:
    """Load processed JSON and response text"""
    try:
        json_path = PROCESSED_DIR / f"{filename}.json"
        if not json_path.exists():
            DriftStrom.fehler_strom("load_processed_file", f"File not found: {json_path}")
            raise FileNotFoundError(f"Processed file not found: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        txt_path = PROCESSED_DIR / f"{filename}_response.txt"
        if not txt_path.exists():
            DriftStrom.fehler_strom("load_processed_file", f"Response file not found: {txt_path}")
            raise FileNotFoundError(f"Response file not found: {txt_path}")
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            response_text = f.read()
        
        return metadata, response_text
        
    except Exception as e:
        DriftStrom.fehler_strom("load_processed_file", str(e), {"filename": filename})
        raise


def extract_fields(metadata: Dict) -> List[str]:
    """Extract field names from metadata"""
    try:
        fields = list(metadata["syntex_result"]["quality_score"]["detail_breakdown"].keys())
        return fields
    except KeyError as e:
        DriftStrom.fehler_strom("extract_fields", f"KeyError: {e}")
        raise ValueError("Could not extract fields from metadata")


def call_gpt(prompt_payload: Dict, api_key: str) -> Dict:
    """Call OpenAI GPT-4 API"""
    model = prompt_payload.get("model", "gpt-4")
    
    try:
        DriftStrom.gpt_call(template_id="unknown", model=model, erfolg=True)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=prompt_payload,
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        DriftStrom.fehler_strom("call_gpt", str(e), {"model": model})
        raise


def parse_gpt_response(gpt_response: Dict) -> Dict:
    """Parse GPT response and extract drift analysis JSON"""
    try:
        content = gpt_response["choices"][0]["message"]["content"]
        
        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            json_start = content.find("```json") + 7
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()
        elif "```" in content:
            json_start = content.find("```") + 3
            json_end = content.find("```", json_start)
            content = content[json_start:json_end].strip()
        
        # Parse JSON
        analysis = json.loads(content)
        return analysis
        
    except Exception as e:
        DriftStrom.fehler_strom("parse_gpt_response", str(e))
        raise ValueError(f"Failed to parse GPT response: {e}")


def save_result(filename: str, analysis: Dict, metadata: Dict) -> str:
    """Save drift scoring result"""
    timestamp = int(datetime.now().timestamp())
    result_filename = f"{filename}_drift_{timestamp}.json"
    result_path = RESULTS_DIR / result_filename
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "source_file": filename,
        "format": metadata.get("syntex_result", {}).get("quality_score", {}).get("format"),
        "topic": metadata.get("topic"),
        "style": metadata.get("style"),
        "drift_analysis": analysis
    }
    
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    DriftStrom.result_gespeichert(filename, str(result_path))
    
    return str(result_path)


def score_file(
    filename: str,
    template_id: str,
    api_key: str
) -> Dict[str, Any]:
    """
    Complete drift scoring workflow
    💎 STROM ORCHESTRATOR 💎
    """
    start_time = time.time()
    
    try:
        # 1. Load files
        metadata, response_text = load_processed_file(filename)
        
        # 2. Extract fields
        fields = extract_fields(metadata)
        
        # 3. Build prompt
        prompt_payload = build_prompt(template_id, fields, response_text)
        DriftStrom.prompt_gebaut(template_id, len(fields), len(response_text))
        
        # 4. Call GPT
        gpt_response = call_gpt(prompt_payload, api_key)
        
        # 5. Parse response
        analysis = parse_gpt_response(gpt_response)
        
        # 6. Save result
        result_path = save_result(filename, analysis, metadata)
        
        # 7. Complete
        duration_ms = int((time.time() - start_time) * 1000)
        
        drift_detected = analysis.get("summary", {}).get("drift_detected", False)
        resonance_score = analysis.get("summary", {}).get("resonance_score", 0.0)
        
        DriftStrom.scoring_komplett(
            filename=filename,
            fields_analyzed=len(fields),
            drift_detected=drift_detected,
            resonance_score=resonance_score,
            duration_ms=duration_ms
        )
        
        return {
            "status": "success",
            "filename": filename,
            "result_path": result_path,
            "fields_analyzed": len(fields),
            "drift_detected": drift_detected,
            "resonance_score": resonance_score,
            "duration_ms": duration_ms,
            "analysis": analysis
        }
        
    except Exception as e:
        DriftStrom.fehler_strom("score_file", str(e), {"filename": filename})
        raise
