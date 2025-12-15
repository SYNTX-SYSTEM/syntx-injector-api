"""
SYNTX Field Resonance - Wrapper Management

Not "file management" - FIELD DISCOVERY.
Wrappers are dormant fields, this activates them.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import re

from ..config import settings

router = APIRouter(prefix="/resonanz", tags=["resonance-wrappers"])


@router.get("/wrappers")
async def list_wrappers() -> Dict[str, List[Dict]]:
    """List all available wrapper fields."""
    wrapper_dir = Path(settings.wrapper_dir)
    wrappers = []
    
    if not wrapper_dir.exists():
        return {"wrappers": []}
    
    for file in wrapper_dir.glob("*.txt"):
        stat = file.stat()
        wrappers.append({
            "name": file.stem,
            "path": str(file),
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z'
        })
    
    return {"wrappers": sorted(wrappers, key=lambda x: x["name"])}


@router.get("/wrapper/{name}")
async def get_wrapper(name: str) -> Dict:
    """Get specific wrapper field content."""
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Wrapper field '{name}' not found")
    
    try:
        with open(wrapper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stat = wrapper_path.stat()
        
        return {
            "name": name,
            "content": content,
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Field activation failed: {str(e)}")


@router.post("/upload")
async def upload_wrapper(file: UploadFile = File(...)) -> Dict:
    """Upload new wrapper field."""
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt wrapper fields allowed")
    
    content = await file.read()
    
    if len(content) > 50 * 1024:
        raise HTTPException(status_code=400, detail="Wrapper field too large (max 50KB)")
    
    name = file.filename.replace('.txt', '')
    name = re.sub(r'[^a-z0-9_-]', '_', name.lower())
    
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    try:
        settings.wrapper_dir.mkdir(parents=True, exist_ok=True)
        
        with open(wrapper_path, 'wb') as f:
            f.write(content)
        
        return {
            "success": True,
            "wrapper": {
                "name": name,
                "path": str(wrapper_path),
                "size_bytes": len(content),
                "size_human": f"{len(content) / 1024:.1f} KB"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Field extension failed: {str(e)}")
