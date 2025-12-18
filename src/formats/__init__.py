"""
SYNTX Format Loader for Rapper Service

Lädt Format-Definitionen aus /opt/syntx-config/formats/
und baut daraus Prompt-Strukturen.
"""
from .format_loader import load_format, build_format_prompt, get_format_fields, list_formats
