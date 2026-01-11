"""
SYNTX Drift Scoring - FastAPI Endpoints
Complete CRUD for prompt templates + drift scoring
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from pathlib import Path

from .drift_prompt_builder import (
    load_template,
    list_templates,
    build_prompt,
    save_template,
    delete_template
)
from .drift_scorer import (
    score_file,
    load_processed_file,
    extract_fields
)
from ..config import settings

router = APIRouter(prefix="/drift", tags=["drift_scoring"])

RESULTS_DIR = Path("/opt/syntx-config/drift_results")


# ═══════════════════════════════════════════════════════════════════════════════
# 📦 MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class PromptTemplateResponse(BaseModel):
    id: str
    name: str
    version: str
    description: Optional[str] = None


class PromptBuildRequest(BaseModel):
    template_id: str = Field(..., description="Template ID to use")
    fields: List[str] = Field(..., description="Fields to analyze")
    response_text: str = Field(..., description="Full response text")


class DriftScoreRequest(BaseModel):
    template_id: str = Field(default="drift_scoring_default", description="Template to use")


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 PROMPT TEMPLATE CRUD ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/prompts")
async def get_prompt_templates():
    """
    📋 List all prompt templates
    
    Returns list of available templates with metadata
    """
    try:
        templates = list_templates()
        return {
            "status": "success",
            "count": len(templates),
            "templates": templates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")


@router.get("/prompts/{template_id}")
async def get_prompt_template(template_id: str):
    """
    🔍 Get specific prompt template
    
    Returns complete template configuration
    """
    try:
        template = load_template(template_id)
        return {
            "status": "success",
            "template": template
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load template: {str(e)}")


@router.post("/prompts")
async def create_prompt_template(template: Dict[str, Any]):
    """
    🌱 Create new prompt template
    
    Request body should contain complete template configuration
    """
    try:
        # Validate required fields
        required = ["id", "name", "version", "model_config", "system_prompt", "user_prompt_template"]
        for field in required:
            if field not in template:
                raise ValueError(f"Missing required field: {field}")
        
        success = save_template(template)
        
        return {
            "status": "success",
            "template_id": template["id"],
            "message": f"Template '{template['id']}' created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create template: {str(e)}")


@router.put("/prompts/{template_id}")
async def update_prompt_template(template_id: str, template: Dict[str, Any]):
    """
    ✏️ Update existing prompt template
    
    Template ID in path must match ID in body
    """
    try:
        if template.get("id") != template_id:
            raise ValueError("Template ID mismatch")
        
        success = save_template(template)
        
        return {
            "status": "success",
            "template_id": template_id,
            "message": f"Template '{template_id}' updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update template: {str(e)}")


@router.delete("/prompts/{template_id}")
async def delete_prompt_template(template_id: str):
    """
    🗑️ Delete prompt template
    
    Cannot delete 'drift_scoring_default'
    """
    try:
        success = delete_template(template_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
        
        return {
            "status": "success",
            "template_id": template_id,
            "message": f"Template '{template_id}' deleted successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete template: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔨 PROMPT BUILDING ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/prompts/build")
async def build_prompt_from_template(request: PromptBuildRequest):
    """
    🔨 Build GPT prompt from template
    
    Dynamically builds a complete GPT API payload from template + data
    
    Returns ready-to-use GPT API request payload
    """
    try:
        payload = build_prompt(
            request.template_id,
            request.fields,
            request.response_text
        )
        
        return {
            "status": "success",
            "template_id": request.template_id,
            "fields_count": len(request.fields),
            "payload": payload
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template '{request.template_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build prompt: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 DRIFT SCORING ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/score/{filename}")
async def score_drift(
    filename: str,
    template_id: str = Query(default="drift_scoring_default", description="Template to use")
):
    """
    🎯 Score a processed file for semantic drift
    
    Complete workflow:
    1. Load processed JSON + response text
    2. Extract fields from format
    3. Build GPT prompt from template
    4. Call GPT-4 for drift analysis
    5. Parse and save results
    
    Args:
        filename: Base filename (without .json extension)
        template_id: Prompt template to use
    
    Returns:
        Drift analysis results
    """
    try:
        result = score_file(
            filename,
            template_id,
            settings.openai_api_key
        )
        
        return result
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drift scoring failed: {str(e)}")


@router.get("/results")
async def get_drift_results(
    limit: int = Query(default=50, le=200, description="Max results to return")
):
    """
    📊 List drift scoring results
    
    Returns recent drift analysis results
    """
    try:
        results = []
        
        for result_file in sorted(RESULTS_DIR.glob("*.json"), reverse=True)[:limit]:
            import json
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                results.append({
                    "filename": result_file.name,
                    "timestamp": data.get("timestamp"),
                    "source_file": data.get("source_file"),
                    "format": data.get("format"),
                    "drift_detected": data.get("drift_analysis", {}).get("summary", {}).get("drift_detected"),
                    "resonance_score": data.get("drift_analysis", {}).get("summary", {}).get("resonance_score")
                })
        
        return {
            "status": "success",
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list results: {str(e)}")


@router.get("/results/{filename}")
async def get_drift_result(filename: str):
    """
    🔍 Get specific drift scoring result
    
    Returns complete drift analysis for a file
    """
    try:
        import json
        
        result_path = RESULTS_DIR / filename
        if not result_path.exists():
            raise HTTPException(status_code=404, detail=f"Result '{filename}' not found")
        
        with open(result_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "status": "success",
            "result": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load result: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🏥 HEALTH & INFO
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def drift_scoring_health():
    """
    🏥 Drift scoring system health check
    """
    try:
        templates = list_templates()
        results_count = len(list(RESULTS_DIR.glob("*.json")))
        
        return {
            "status": "🟢 DRIFT SCORING ACTIVE",
            "version": "1.0.0",
            "templates_available": len(templates),
            "results_stored": results_count,
            "openai_configured": bool(settings.openai_api_key),
            "features": [
                "Prompt template CRUD",
                "Dynamic prompt building",
                "GPT-4 drift analysis",
                "Per-field scoring",
                "Result storage"
            ]
        }
    except Exception as e:
        return {
            "status": "🔴 ERROR",
            "error": str(e)
        }
