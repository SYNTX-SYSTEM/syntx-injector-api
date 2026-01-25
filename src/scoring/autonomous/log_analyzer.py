"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔍 LOG ANALYZER - Der Scanner (v2 - Fixed for actual log structure)        ║
║                                                                              ║
║  Architecture validated by GPT-4 on 2026-01-05                              ║
║  Fixed for actual log format: field, profile, text_preview                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict


LOG_DIR = Path("/opt/syntx-config/logs/scoring")


def analyze_low_scores(
    days: int = 7,
    score_threshold: float = 0.3,
    min_occurrences: int = 3
) -> Dict:
    """
    🔍 Find fields with consistently low scores
    
    Actual log structure:
    {
      "timestamp": "2026-01-05T16:04:10.903888Z",
      "field": "driftkorper",
      "score": 0.45,
      "text_preview": "Das System driftet...",
      "profile": "dynamic_language_v1",
      "components": {...}
    }
    """
    from datetime import timezone; cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Collect data per field
    field_data = defaultdict(lambda: {
        "scores": [],
        "profiles": Counter(),
        "texts": []
    })
    
    # Scan log files
    if not LOG_DIR.exists():
        return {"error": "Log directory not found", "path": str(LOG_DIR)}
    
    log_files = list(LOG_DIR.glob("scores_*.jsonl"))
    if not log_files:
        return {
            "error": "No log files found",
            "path": str(LOG_DIR),
            "pattern": "scores_*.jsonl"
        }
    
    for log_file in sorted(log_files):
        try:
            with open(log_file) as f:
                for line in f:
                    entry = json.loads(line)
                    
                    # Check date
                    log_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                    if log_time < cutoff_date:
                        continue
                    
                    # Get field (support both old and new format)
                    field = entry.get("field", entry.get("field_name", "unknown"))
                    score = entry.get("score", 0)
                    
                    # Filter by threshold
                    if score <= score_threshold:
                        field_data[field]["scores"].append(score)
                        
                        # Get profile (support both formats)
                        profile = entry.get("profile", entry.get("profile_used", "unknown"))
                        field_data[field]["profiles"][profile] += 1
                        
                        # Get text (support both formats)
                        text = entry.get("text_preview", entry.get("text", ""))
                        if text and len(field_data[field]["texts"]) < 10:
                            field_data[field]["texts"].append(text)
        except Exception as e:
            print(f"⚠️  Error reading {log_file}: {e}")
            continue
    
    # Process results
    problematic_fields = {}
    
    for field, data in field_data.items():
        if len(data["scores"]) >= min_occurrences:
            avg_score = sum(data["scores"]) / len(data["scores"])
            most_common_profile = data["profiles"].most_common(1)[0][0] if data["profiles"] else "unknown"
            
            problematic_fields[field] = {
                "avg_score": round(avg_score, 3),
                "count": len(data["scores"]),
                "profile_used": most_common_profile,
                "sample_texts": data["texts"][:5],  # Top 5 for display
                "all_samples": data["texts"]  # All for pattern extraction
            }
    
    return {
        "analysis_period_days": days,
        "score_threshold": score_threshold,
        "min_occurrences": min_occurrences,
        "problematic_fields": problematic_fields,
        "total_fields_analyzed": len(field_data),
        "problematic_count": len(problematic_fields),
        "log_files_scanned": len(log_files),
        "timestamp": datetime.now().isoformat()
    }


def get_field_trends(field_name: str, days: int = 30) -> Dict:
    """📈 Track score trends for a specific field over time"""
    from datetime import timezone; cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    daily_scores = defaultdict(list)
    
    for log_file in sorted(LOG_DIR.glob("scores_*.jsonl")):
        try:
            with open(log_file) as f:
                for line in f:
                    entry = json.loads(line)
                    
                    field = entry.get("field", entry.get("field_name"))
                    if field != field_name:
                        continue
                    
                    log_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                    if log_time < cutoff_date:
                        continue
                    
                    day = log_time.date().isoformat()
                    daily_scores[day].append(entry["score"])
        except Exception as e:
            continue
    
    # Calculate daily statistics
    trends = {}
    for day, scores in sorted(daily_scores.items()):
        trends[day] = {
            "avg": round(sum(scores) / len(scores), 3),
            "count": len(scores),
            "min": round(min(scores), 3),
            "max": round(max(scores), 3),
            "stddev": round(_stddev(scores), 3) if len(scores) > 1 else 0.0
        }
    
    return {
        "field_name": field_name,
        "period_days": days,
        "daily_trends": trends,
        "total_days_with_data": len(trends)
    }


def _stddev(values: List[float]) -> float:
    """Calculate standard deviation"""
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    return variance ** 0.5
