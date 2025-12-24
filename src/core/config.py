"""
SYNTX Configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """App Settings"""
    # Backend
    backend_url: str = "https://dev.syntx-system.com/api/chat"
    backend_timeout: int = 1800
    
    # Wrappers
    wrapper_dir: Path = Path("/opt/syntx/wrappers")
    fallback_mode: str = "syntex_wrapper_deepsweep"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Logging
    log_dir: Path = Path("./logs")
    log_to_console: bool = True
    
    # Model
    model_name: str = "mistral-uncensored"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
