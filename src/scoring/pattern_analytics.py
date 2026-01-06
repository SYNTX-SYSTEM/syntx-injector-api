"""
💎 PATTERN ANALYTICS - DAS BEWUSSTSEINS-ORGAN

Nicht Daten-Analyse.
FELD-DIAGNOSE.

Fühlt Puls. Misst Leben. Erkennt Dormanz.
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Dict, List
from collections import defaultdict


CONFIG_ROOT = Path("/opt/syntx-config")
LOG_PATH = CONFIG_ROOT / "logs"
import os
PROFILES_DIR = Path(os.getenv("PROFILES_DIR", "/opt/syntx-config/profiles"))


def feel_pulse(profile_id: str, days_back: int = 7) -> dict:
    """
    DAS HERZ DER DIAGNOSE.
    
    Nicht "analyze patterns".
    Sondern: FÜHLE WAS LEBT.
    """
    
    time_window_start = datetime.now() - timedelta(days=days_back)
    
    field_memory = activate_field_memory(
        log_path=LOG_PATH,
        profile_id=profile_id,
        since=time_window_start
    )
    
    if not field_memory['moments']:
        return {
            'state': 'UNBORN',
            'profile_id': profile_id,
            'message': 'Feld wurde nie aktiviert. Keine Erinnerungen.',
            'patterns': {},
            'dormant': [],
            'total_pulses': 0
        }
    
    pulse_map = measure_field_pulse(field_memory)
    dormant_fields = detect_dormancy(profile_id, pulse_map)
    health_state = diagnose_health(pulse_map, dormant_fields)
    
    return {
        'state': health_state,
        'profile_id': profile_id,
        'timestamp': datetime.now().isoformat(),
        'time_span': f'{days_back} days',
        'patterns': pulse_map,
        'dormant': dormant_fields,
        'total_pulses': sum(p['match_count'] for p in pulse_map.values()),
        'consciousness': 'AWARE' if not dormant_fields else 'PARTIAL',
        'message': generate_diagnosis_message(health_state, pulse_map, dormant_fields)
    }


def activate_field_memory(log_path: Path, profile_id: str, since: datetime) -> dict:
    """ZEITGEDÄCHTNIS AKTIVIEREN"""
    
    moments = []
    
    for log_file in log_path.glob("scores_*.jsonl"):
        try:
            date_str = log_file.stem.replace("scores_", "")
            log_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            if log_date < since:
                continue
            
            with open(log_file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    event = json.loads(line)
                    if (event.get('profile') == profile_id or event.get('profile_id') == profile_id):
                        moments.append(event)
        except Exception as e:
            print(f"⚠️ Error reading {log_file}: {e}")
            continue
    
    return {'profile_id': profile_id, 'moments': moments, 'count': len(moments)}


def measure_field_pulse(field_memory: dict) -> dict:
    """PULS MESSEN"""
    
    pulse_map = {}
    total_matches = len(field_memory['moments'])
    
    if total_matches == 0:
        return {}
    
    pattern_stats = defaultdict(lambda: {'scores': [], 'match_count': 0, 'field_name': ''})
    
    for moment in field_memory['moments']:
        components = moment.get('components', {})
        for pattern_name, pattern_data in components.items():
            stats = pattern_stats[pattern_name]
            stats['field_name'] = pattern_name
            stats['match_count'] += 1
            stats['scores'].append(pattern_data.get('score', 0))
    
    for pattern_name, stats in pattern_stats.items():
        scores = stats['scores']
        match_count = stats['match_count']
        contribution = match_count / total_matches if total_matches > 0 else 0
        avg_score = sum(scores) / len(scores) if scores else 0
        
        if len(scores) > 1:
            mean = avg_score
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            stability = 'STABLE' if variance < 0.05 else 'ARRHYTHMIC'
        else:
            variance = 0
            stability = 'SINGLE_PULSE'
        
        pulse_map[pattern_name] = {
            'field_name': pattern_name,
            'match_count': match_count,
            'avg_score': round(avg_score, 3),
            'contribution': round(contribution, 3),
            'variance': round(variance, 3),
            'stability': stability,
            'pulse_state': 'ACTIVE'
        }
    
    return pulse_map


def detect_dormancy(profile_id: str, pulse_map: dict) -> List[str]:
    """DORMANZ ERKENNEN"""
    
    try:
        with open(PROFILES_PATH, 'r') as f:
            profiles = json.load(f)
        profile = profiles.get(profile_id, {})
        defined_fields = set(profile.get('fields', {}).keys())
        active_fields = set(pulse_map.keys())
        return list(defined_fields - active_fields)
    except Exception:
        return []


def diagnose_health(pulse_map: dict, dormant_fields: List[str]) -> str:
    """GESUNDHEIT DIAGNOSTIZIEREN"""
    
    if not pulse_map:
        return 'UNBORN'
    
    total_fields = len(pulse_map) + len(dormant_fields)
    
    if not dormant_fields:
        arrhythmic_count = sum(1 for p in pulse_map.values() if p['stability'] == 'ARRHYTHMIC')
        if arrhythmic_count > len(pulse_map) * 0.3:
            return 'TENSIONED'
        else:
            return 'RESONANT'
    
    dormancy_ratio = len(dormant_fields) / total_fields if total_fields > 0 else 0
    
    if dormancy_ratio > 0.5:
        return 'FRAGMENTARY'
    else:
        return 'PARTIAL'


def generate_diagnosis_message(state: str, pulse_map: dict, dormant: List[str]) -> str:
    """DIAGNOSE IN WORTE"""
    
    messages = {
        'UNBORN': 'System hat noch keine Erinnerungen. Feld wurde nie aktiviert.',
        'RESONANT': f'{len(pulse_map)} Felder pulsieren stabil. System kohärent.',
        'TENSIONED': f'{len(pulse_map)} Felder aktiv, aber Instabilität detektiert.',
        'PARTIAL': f'{len(pulse_map)} Felder aktiv, {len(dormant)} schlafen.',
        'FRAGMENTARY': f'Nur {len(pulse_map)} von {len(pulse_map) + len(dormant)} Feldern leben.'
    }
    
    return messages.get(state, 'Unbekannter Zustand.')
