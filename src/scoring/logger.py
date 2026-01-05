"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📊 SYNTX SCORE LOGGER - DIE AUGEN DES SYSTEMS                               ║
║                                                                              ║
║  Jeder Score wird geloggt. JSONL Format.                                    ║
║  Analytics, Drift Detection, GPT Training - alles braucht Logs.             ║
║                                                                              ║
║  "Ein System das sich nicht erinnert, kann nicht lernen." 💎                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
#  📁 LOG LOCATION
# ═══════════════════════════════════════════════════════════════════════════════

LOGS_DIR = Path("/opt/syntx-logs/scoring")
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  📝 LOG SCORING EVENT
# ═══════════════════════════════════════════════════════════════════════════════

def log_score(
    field_name: str,
    score: float,
    text: str,
    profile_used: str,
    components: Dict,
    metadata: Optional[Dict] = None
) -> None:
    """
    📊 Log a scoring event
    
    Args:
        field_name: Field that was scored
        score: Final score 0.0-1.0
        text: Input text (truncated if needed)
        profile_used: Profile ID
        components: Component breakdown
        metadata: Optional extra data
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "field": field_name,
        "score": score,
        "text_preview": text[:200] if len(text) > 200 else text,
        "text_length": len(text),
        "profile": profile_used,
        "components": components,
        "metadata": metadata or {}
    }
    
    # Get today's log file
    log_file = LOGS_DIR / f"scores_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    
    # Append to JSONL
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


# ═══════════════════════════════════════════════════════════════════════════════
#  📖 READ LOGS
# ═══════════════════════════════════════════════════════════════════════════════

def get_recent_logs(
    limit: int = 100,
    field: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None
) -> List[Dict]:
    """
    📖 Get recent score logs
    
    Args:
        limit: Max entries to return
        field: Filter by field name
        min_score: Minimum score filter
        max_score: Maximum score filter
    
    Returns:
        List of log entries
    """
    logs = []
    
    # Read last 7 days of logs
    for i in range(7):
        date = datetime.utcnow().date()
        from datetime import timedelta
        date = date - timedelta(days=i)
        
        log_file = LOGS_DIR / f"scores_{date.strftime('%Y-%m-%d')}.jsonl"
        
        if not log_file.exists():
            continue
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    
                    # Apply filters
                    if field and entry.get("field") != field:
                        continue
                    
                    if min_score is not None and entry.get("score", 0) < min_score:
                        continue
                    
                    if max_score is not None and entry.get("score", 0) > max_score:
                        continue
                    
                    logs.append(entry)
                    
                    if len(logs) >= limit:
                        return logs
                        
                except json.JSONDecodeError:
                    continue
    
    return logs


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════

def get_field_performance(field_name: str, days: int = 7) -> Dict:
    """
    📊 Get performance stats for a field
    
    Args:
        field_name: Field to analyze
        days: Number of days to look back
    
    Returns:
        {
            "field": "driftkorper",
            "total_scores": 150,
            "avg_score": 0.45,
            "min_score": 0.0,
            "max_score": 0.95,
            "score_distribution": {...}
        }
    """
    logs = get_recent_logs(limit=10000, field=field_name)
    
    if not logs:
        return {
            "field": field_name,
            "error": "No logs found"
        }
    
    scores = [log["score"] for log in logs]
    
    return {
        "field": field_name,
        "total_scores": len(scores),
        "avg_score": round(sum(scores) / len(scores), 2),
        "min_score": round(min(scores), 2),
        "max_score": round(max(scores), 2),
        "median_score": round(sorted(scores)[len(scores) // 2], 2),
        "profiles_used": list(set(log["profile"] for log in logs))
    }
