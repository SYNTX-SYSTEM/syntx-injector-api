"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📊 SYNTX PROFILE ANALYTICS - DAS GEDÄCHTNIS                                 ║
║                                                                              ║
║  Aggregates scoring logs by profile ID.                                     ║
║  Memory of profile performance over time.                                   ║
║                                                                              ║
║  "Ein System das sich erinnert, kann lernen." 💎                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════════════════════
#  📁 LOG LOCATION
# ═══════════════════════════════════════════════════════════════════════════════

LOGS_DIR = Path("/opt/syntx-logs/scoring")


# ═══════════════════════════════════════════════════════════════════════════════
#  📊 PROFILE ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════

def get_profile_analytics(days: int = 7) -> Dict:
    """
    📊 Aggregate scoring logs by profile ID
    
    Returns stats for each profile:
    - total_usage: How many times used
    - avg_score: Average score
    - min_score, max_score: Score range
    - fields_using_it: Which fields use this profile
    
    Args:
        days: How many days back to analyze
    
    Returns:
        {
            "profile_id": {
                "profile_id": str,
                "total_usage": int,
                "avg_score": float,
                "min_score": float,
                "max_score": float,
                "fields_using_it": List[str]
            }
        }
    """
    if not LOGS_DIR.exists():
        return {}
    
    # Calculate time cutoff
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Aggregate stats by profile
    profile_stats = defaultdict(lambda: {
        "profile_id": "",
        "total_usage": 0,
        "scores": [],
        "fields": set()
    })
    
    # Read log files (last N days)
    log_files = sorted(LOGS_DIR.glob("scores_*.jsonl"))
    recent_files = log_files[-days:] if len(log_files) > days else log_files
    
    for log_file in recent_files:
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    try:
                        entry = json.loads(line)
                        
                        # Check timestamp
                        timestamp = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
                        if timestamp < cutoff:
                            continue
                        
                        # Extract data
                        profile_id = entry.get("profile")
                        field_name = entry.get("field")
                        score = entry.get("score")
                        
                        if not profile_id:
                            continue
                        
                        # Aggregate
                        stats = profile_stats[profile_id]
                        stats["profile_id"] = profile_id
                        stats["total_usage"] += 1
                        stats["scores"].append(score)
                        stats["fields"].add(field_name)
                        
                    except (json.JSONDecodeError, KeyError) as e:
                        continue
        except Exception as e:
            continue
    
    # Calculate final stats
    result = {}
    for profile_id, stats in profile_stats.items():
        scores = stats["scores"]
        
        result[profile_id] = {
            "profile_id": profile_id,
            "total_usage": stats["total_usage"],
            "avg_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
            "min_score": round(min(scores), 2) if scores else 0.0,
            "max_score": round(max(scores), 2) if scores else 0.0,
            "fields_using_it": sorted(list(stats["fields"]))
        }
    
    return result


def get_single_profile_stats(profile_id: str, days: int = 7) -> Optional[Dict]:
    """
    📈 Get stats for a single profile
    
    Returns:
        Same as get_profile_analytics but for one profile,
        or None if profile not found in logs
    """
    all_stats = get_profile_analytics(days=days)
    return all_stats.get(profile_id)


def analyze_profile_usage() -> Dict:
    """
    🔍 Summary statistics across all profiles
    
    Returns:
        {
            "total_profiles_used": int,
            "total_scores": int,
            "most_used_profile": str,
            "best_performing_profile": str,
            "avg_score_overall": float
        }
    """
    stats = get_profile_analytics(days=7)
    
    if not stats:
        return {
            "total_profiles_used": 0,
            "total_scores": 0,
            "most_used_profile": None,
            "best_performing_profile": None,
            "avg_score_overall": 0.0
        }
    
    total_scores = sum(s["total_usage"] for s in stats.values())
    all_scores = []
    
    most_used = max(stats.items(), key=lambda x: x[1]["total_usage"])
    best_perf = max(stats.items(), key=lambda x: x[1]["avg_score"])
    
    for profile_stats in stats.values():
        all_scores.extend([profile_stats["avg_score"]] * profile_stats["total_usage"])
    
    return {
        "total_profiles_used": len(stats),
        "total_scores": total_scores,
        "most_used_profile": most_used[0],
        "best_performing_profile": best_perf[0],
        "avg_score_overall": round(sum(all_scores) / len(all_scores), 2) if all_scores else 0.0
    }
