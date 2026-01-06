"""
💎 PROFILE USAGE ANALYTICS

Misst wie oft und wie gut Profile genutzt werden.
Nicht Mock. Reality.
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Dict, Optional


CONFIG_ROOT = Path("/opt/syntx-config")
LOG_PATH = CONFIG_ROOT / "logs"


def measure_profile_usage(profile_id: str, days_back: int = 30) -> dict:
    """
    MISST PROFIL-NUTZUNG ÜBER ZEIT.
    
    Nicht "count uses".
    Sondern: FÜHLE WIE OFT PROFIL LEBT.
    """
    
    time_window_start = datetime.now() - timedelta(days=days_back)
    
    usage_events = []
    
    # Durchsuche Logs
    for log_file in LOG_PATH.glob("scores_*.jsonl"):
        try:
            date_str = log_file.stem.replace("scores_", "")
            log_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            if log_date < time_window_start:
                continue
            
            with open(log_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    event = json.loads(line)
                    
                    if event.get('profile') or event.get('profile_id') == profile_id:
                        usage_events.append({
                            'timestamp': event.get('timestamp'),
                            'score': event.get('total_score', 0)
                        })
        
        except Exception:
            continue
    
    if not usage_events:
        return {
            'profile_id': profile_id,
            'total_uses': 0,
            'avg_score': 0.0,
            'last_used': None,
            'usage_trend': 'UNUSED',
            'status': 'DORMANT'
        }
    
    # Berechne Metriken
    total_uses = len(usage_events)
    avg_score = sum(e['score'] for e in usage_events) / total_uses if total_uses > 0 else 0
    last_used = max(e['timestamp'] for e in usage_events if e['timestamp'])
    
    # Trend berechnen (erste vs zweite Hälfte)
    if total_uses > 10:
        mid_point = total_uses // 2
        first_half_avg = sum(e['score'] for e in usage_events[:mid_point]) / mid_point
        second_half_avg = sum(e['score'] for e in usage_events[mid_point:]) / (total_uses - mid_point)
        
        if second_half_avg > first_half_avg * 1.1:
            usage_trend = 'INCREASING'
        elif second_half_avg < first_half_avg * 0.9:
            usage_trend = 'DECREASING'
        else:
            usage_trend = 'STABLE'
    else:
        usage_trend = 'INSUFFICIENT_DATA'
    
    return {
        'profile_id': profile_id,
        'total_uses': total_uses,
        'avg_score': round(avg_score, 4),
        'last_used': last_used,
        'usage_trend': usage_trend,
        'status': 'ACTIVE'
    }
