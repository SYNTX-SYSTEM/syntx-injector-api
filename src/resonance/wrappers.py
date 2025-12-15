"""
SYNTX Field Resonance - Wrapper Management

Not "file management" - FIELD DISCOVERY.
Wrappers are dormant fields, this activates them.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
from typing import List, Dict, Optional
import re

from ..config import settings

router = APIRouter(prefix="/resonanz", tags=["resonance-wrappers"])


def get_active_wrapper() -> str:
    """Get currently active default wrapper."""
    from .config import get_active_wrapper as _get_active
    return _get_active()


@router.get("/wrappers")
async def list_wrappers(active: bool = False) -> Dict:
    """
    List all available wrapper fields.
    Query param 'active=true' filters to show only active wrapper.
    """
    wrapper_dir = Path(settings.wrapper_dir)
    wrappers = []
    
    if not wrapper_dir.exists():
        return {"wrappers": [], "active_wrapper": None}
    
    active_wrapper = get_active_wrapper()
    
    for file in wrapper_dir.glob("*.txt"):
        stat = file.stat()
        is_active = (file.stem == active_wrapper)
        
        wrapper_info = {
            "name": file.stem,
            "path": str(file),
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z',
            "is_active": is_active
        }
        
        # Filter: if active=true, only include active wrapper
        if not active or is_active:
            wrappers.append(wrapper_info)
    
    return {
        "wrappers": sorted(wrappers, key=lambda x: x["name"]),
        "active_wrapper": active_wrapper
    }


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
        active_wrapper = get_active_wrapper()
        
        return {
            "name": name,
            "content": content,
            "size_bytes": stat.st_size,
            "size_human": f"{stat.st_size / 1024:.1f} KB",
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z',
            "is_active": (name == active_wrapper)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Field activation failed: {str(e)}")


@router.post("/upload")
async def upload_wrapper(file: UploadFile = File(...)) -> Dict:
    """Upload new wrapper field (simple, no metadata)."""
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


@router.post("/upload-metadata")
async def upload_wrapper_with_metadata(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    version: Optional[str] = Form("1.0"),
    tags: Optional[str] = Form(None)
):
    """
    Upload wrapper field with metadata.
    File is uploaded, metadata added as header.
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        if len(content) > 50 * 1024:
            raise HTTPException(status_code=400, detail="Wrapper field too large (max 50KB)")
        
        # Get name from filename
        name = file.filename.replace('.txt', '')
        safe_name = name.lower().replace(' ', '_')
        safe_name = re.sub(r'[^a-z0-9_-]', '_', safe_name)
        
        # Build metadata header
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
        
        # Combine metadata + content
        full_content = "\n".join(metadata_lines) + "\n" + content_str
        
        # Write to file
        wrapper_path = settings.wrapper_dir / f"{safe_name}.txt"
        settings.wrapper_dir.mkdir(parents=True, exist_ok=True)
        
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return {
            "status": "success",
            "message": "Wrapper with metadata uploaded successfully",
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


@router.post("/wrappers/{name}/activate")
async def activate_wrapper(name: str) -> Dict:
    """
    Activate a specific wrapper as default.
    This wrapper will be used when no 'mode' is specified in chat requests.
    """
    from .config import set_active_wrapper
    
    wrapper_path = settings.wrapper_dir / f"{name}.txt"
    
    if not wrapper_path.exists():
        raise HTTPException(status_code=404, detail=f"Wrapper field '{name}' not found")
    
    set_active_wrapper(name)
    
    return {
        "status": "success",
        "message": f"Wrapper '{name}' activated as default",
        "active_wrapper": name,
        "path": str(wrapper_path)
    }
