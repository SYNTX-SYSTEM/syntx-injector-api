"""
🔄💎 SYNTX PAGINATION & FILTER SYSTEM 💎🔄

Generisches Pagination/Filter/Sort System für ALLE Endpoints!

Philosophy:
- DRY: Don't Repeat Yourself (1x schreiben, überall nutzen)
- Consistent: Alle Endpoints geben gleiche Response-Struktur
- SYNTX-Style: Deutsche Variablen, Charlottenburg-Kommentare

Usage:
    from core.pagination import PaginationParams, paginate_list
    
    @router.get("/items")
    async def list_items(pagination: PaginationParams = Depends()):
        items = get_all_items()
        return paginate_list(items, pagination)

Author: SYNTX Team
Date: 2026-01-25
Version: 1.0-charlottenburg
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, TypeVar, Generic
from fastapi import Query
from math import ceil

# ═══════════════════════════════════════════════════════════════════════════
#  📋 PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class PaginationParams(BaseModel):
    """
    Pagination Parameter
    
    Das ist wie Buchseiten durchblättern!
    limit = wie viele Items pro Seite
    page = welche Seite willst du sehen?
    """
    limit: int = Field(default=50, ge=1, le=1000, description="Items pro Seite (1-1000)")
    page: int = Field(default=1, ge=1, description="Seitennummer (ab 1)")
    sort_by: Optional[str] = Field(default=None, description="Nach welchem Feld sortieren?")
    sort_order: str = Field(default="asc", description="Sortier-Reihenfolge: 'asc' oder 'desc'")
    
    @validator('sort_order')
    def validate_sort_order(cls, v):
        if v not in ['asc', 'desc']:
            raise ValueError("sort_order muss 'asc' oder 'desc' sein!")
        return v
    
    @property
    def offset(self) -> int:
        """Berechne Offset aus Page + Limit"""
        return (self.page - 1) * self.limit


class FilterParams(BaseModel):
    """
    Generic Filter Parameters
    
    Das ist wie Suchfilter bei Amazon!
    Key-Value Pairs für beliebige Felder.
    """
    filters: Dict[str, Any] = Field(default_factory=dict, description="Field → Value zum Filtern")


class SearchParams(BaseModel):
    """
    Text Search Parameters
    
    Das ist wie Google-Suche!
    q = query string, fields = wo soll gesucht werden
    """
    q: Optional[str] = Field(default=None, min_length=1, description="Suchbegriff")
    search_fields: List[str] = Field(default_factory=list, description="In welchen Feldern suchen?")


# Generic Type für Items
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard Pagination Response
    
    Das ist das Format das JEDER Endpoint zurückgibt!
    Consistent = Frontend weiß immer was kommt.
    """
    items: List[T] = Field(..., description="Die Items auf dieser Seite")
    total: int = Field(..., description="Gesamt-Anzahl Items (alle Seiten)")
    page: int = Field(..., description="Aktuelle Seite")
    pages: int = Field(..., description="Gesamt-Anzahl Seiten")
    limit: int = Field(..., description="Items pro Seite")
    has_next: bool = Field(..., description="Gibt's noch eine nächste Seite?")
    has_prev: bool = Field(..., description="Gibt's eine vorherige Seite?")


# ═══════════════════════════════════════════════════════════════════════════
#  🔧 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def paginate_list(
    items: List[Any],
    pagination: PaginationParams,
    total_before_pagination: Optional[int] = None
) -> Dict[str, Any]:
    """
    🔄 PAGINATION HELPER
    
    Nimmt eine Liste und gibt paginierte Response zurück!
    Das ist wie Buchseiten schneiden - automatisch die richtige Seite raus.
    
    Args:
        items: Die komplette Liste (kann schon gefiltert sein!)
        pagination: Pagination Parameter (limit, page, sort)
        total_before_pagination: Total vor Pagination (falls schon gefiltert)
    
    Returns:
        Dict mit items, total, page, pages, etc.
    
    Example:
        >>> items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> params = PaginationParams(limit=3, page=2)
        >>> paginate_list(items, params)
        {
            'items': [4, 5, 6],
            'total': 10,
            'page': 2,
            'pages': 4,
            'limit': 3,
            'has_next': True,
            'has_prev': True
        }
    """
    # Total items (vor oder nach Filtering)
    total = total_before_pagination if total_before_pagination is not None else len(items)
    
    # Sortieren wenn gewünscht
    if pagination.sort_by:
        items = sort_items(items, pagination.sort_by, pagination.sort_order)
    
    # Berechne Pagination
    offset = pagination.offset
    limit = pagination.limit
    
    # Slice die Liste
    paginated_items = items[offset:offset + limit]
    
    # Berechne Pages
    total_pages = ceil(total / limit) if limit > 0 else 0
    
    return {
        "items": paginated_items,
        "total": total,
        "page": pagination.page,
        "pages": total_pages,
        "limit": limit,
        "has_next": pagination.page < total_pages,
        "has_prev": pagination.page > 1
    }


def filter_items(
    items: List[Dict[str, Any]],
    filters: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    🔍 FILTER HELPER
    
    Filtert Items nach Key-Value Pairs!
    Das ist wie Excel-Filter - nur Items die matchen.
    
    Args:
        items: Liste von Dicts zum Filtern
        filters: Field → Value zum Matchen
    
    Returns:
        Gefilterte Liste
    
    Example:
        >>> items = [
        ...     {"name": "Alice", "age": 25},
        ...     {"name": "Bob", "age": 30},
        ...     {"name": "Charlie", "age": 25}
        ... ]
        >>> filter_items(items, {"age": 25})
        [{"name": "Alice", "age": 25}, {"name": "Charlie", "age": 25}]
    """
    if not filters:
        return items
    
    filtered = []
    for item in items:
        # Check ob ALLE Filter-Kriterien matchen
        matches = True
        for key, value in filters.items():
            # Nested key support (z.B. "meta.version")
            item_value = get_nested_value(item, key)
            
            if item_value != value:
                matches = False
                break
        
        if matches:
            filtered.append(item)
    
    return filtered


def sort_items(
    items: List[Dict[str, Any]],
    sort_by: str,
    sort_order: str = "asc"
) -> List[Dict[str, Any]]:
    """
    ⬆️⬇️ SORT HELPER
    
    Sortiert Items nach einem Feld!
    Das ist wie Excel-Sortierung - aufsteigend oder absteigend.
    
    Args:
        items: Liste von Dicts zum Sortieren
        sort_by: Field-Name zum Sortieren
        sort_order: 'asc' oder 'desc'
    
    Returns:
        Sortierte Liste
    
    Example:
        >>> items = [
        ...     {"name": "Charlie", "age": 25},
        ...     {"name": "Alice", "age": 30},
        ...     {"name": "Bob", "age": 20}
        ... ]
        >>> sort_items(items, "age", "asc")
        [{"name": "Bob", "age": 20}, {"name": "Charlie", "age": 25}, ...]
    """
    reverse = (sort_order == "desc")
    
    try:
        return sorted(
            items,
            key=lambda x: get_nested_value(x, sort_by),
            reverse=reverse
        )
    except (KeyError, TypeError):
        # Feld existiert nicht oder nicht vergleichbar? Original-Reihenfolge
        return items


def search_items(
    items: List[Dict[str, Any]],
    search_params: SearchParams
) -> List[Dict[str, Any]]:
    """
    🔎 SEARCH HELPER
    
    Volltextsuche in Items!
    Das ist wie Ctrl+F - findet Text in angegebenen Feldern.
    
    Args:
        items: Liste von Dicts zum Durchsuchen
        search_params: Suchbegriff + Felder
    
    Returns:
        Items die den Suchbegriff enthalten
    
    Example:
        >>> items = [
        ...     {"name": "Alice", "bio": "Software Engineer"},
        ...     {"name": "Bob", "bio": "Data Scientist"}
        ... ]
        >>> params = SearchParams(q="engineer", search_fields=["name", "bio"])
        >>> search_items(items, params)
        [{"name": "Alice", "bio": "Software Engineer"}]
    """
    if not search_params.q:
        return items
    
    query = search_params.q.lower()
    fields = search_params.search_fields
    
    results = []
    for item in items:
        # Wenn keine Felder angegeben, alle durchsuchen
        search_in = fields if fields else item.keys()
        
        for field in search_in:
            value = get_nested_value(item, field)
            if value and query in str(value).lower():
                results.append(item)
                break  # Item gefunden, nächstes Item
    
    return results


def get_nested_value(item: Dict[str, Any], key: str) -> Any:
    """
    Holt Wert aus nested Dict mit dot-notation
    
    Example:
        >>> item = {"meta": {"version": "1.0"}}
        >>> get_nested_value(item, "meta.version")
        "1.0"
    """
    keys = key.split('.')
    value = item
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return None
    
    return value


# ═══════════════════════════════════════════════════════════════════════════
#  🎬 ENDE - Pagination System ist jetzt verfügbar! 💎⚡🔥
# ═══════════════════════════════════════════════════════════════════════════
