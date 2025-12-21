"""
╔══════════════════════════════════════════════════════════════════════════════╗
║    🔮 SYNTX CRUD ALCHEMY - CREATE, READ, UPDATE, DELETE                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from .base import SyntxCrudBase
from .file_ops import FileAlchemist
from .validators import FieldValidator, FormatValidator, StyleValidator
from .format_crud import FormatCrud
from .style_crud import StyleCrud

format_crud = FormatCrud()
style_crud = StyleCrud()
