"""
SYNTX Wrapper Service - Configuration Module
All settings come from .env - no hardcoded defaults!
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """Application Settings - ALL from .env"""
    
    # Backend
    backend_url: str
    backend_timeout: int
    backend_bearer_token: Optional[str] = None
    model_name: str  # NEW: For Ollama model selection
    
    # Wrapper
    wrapper_dir: Path
    fallback_mode: str
    
    # Server
    host: str
    port: int
    
    # Logging
    log_dir: Path
    log_to_console: bool
    profiles_dir: str = "/opt/syntx-config/profiles"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
