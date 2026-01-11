"""
SYNTX Drift Scoring - Logging Strom
Charlottenburg Style - Ströme statt Pattern! 💎⚡🔥
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

LOG_DIR = Path("/opt/syntx-config/logs")
DRIFT_LOG = LOG_DIR / "drift_scoring.jsonl"


class DriftStrom:
    """
    Der Logging-Strom für Drift Scoring
    Jede Operation fließt hier durch
    """
    
    @staticmethod
    def log_strom(
        strom_typ: str,
        data: Dict[str, Any],
        erfolg: bool = True,
        fehler: str = None
    ):
        """
        Hauptstrom - Alles fließt hier durch
        """
        eintrag = {
            "timestamp": datetime.now().isoformat(),
            "strom_typ": strom_typ,
            "erfolg": erfolg,
            "data": data
        }
        
        if fehler:
            eintrag["fehler"] = fehler
        
        # Schreibe in JSONL
        with open(DRIFT_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(eintrag, ensure_ascii=False) + '\n')
    
    @staticmethod
    def template_geladen(template_id: str, erfolg: bool = True, fehler: str = None):
        """Strom: Template Loading"""
        DriftStrom.log_strom(
            strom_typ="TEMPLATE_LADEN",
            data={"template_id": template_id},
            erfolg=erfolg,
            fehler=fehler
        )
    
    @staticmethod
    def prompt_gebaut(template_id: str, fields_count: int, text_length: int):
        """Strom: Prompt Building"""
        DriftStrom.log_strom(
            strom_typ="PROMPT_BAUEN",
            data={
                "template_id": template_id,
                "fields_count": fields_count,
                "text_length": text_length
            }
        )
    
    @staticmethod
    def gpt_call(template_id: str, model: str, erfolg: bool = True, fehler: str = None):
        """Strom: GPT API Call"""
        DriftStrom.log_strom(
            strom_typ="GPT_CALL",
            data={
                "template_id": template_id,
                "model": model
            },
            erfolg=erfolg,
            fehler=fehler
        )
    
    @staticmethod
    def result_gespeichert(filename: str, result_path: str):
        """Strom: Result Saved"""
        DriftStrom.log_strom(
            strom_typ="RESULT_SPEICHERN",
            data={
                "source_file": filename,
                "result_path": result_path
            }
        )
    
    @staticmethod
    def scoring_komplett(
        filename: str,
        fields_analyzed: int,
        drift_detected: bool,
        resonance_score: float,
        duration_ms: int
    ):
        """Strom: Complete Scoring Flow"""
        DriftStrom.log_strom(
            strom_typ="SCORING_KOMPLETT",
            data={
                "filename": filename,
                "fields_analyzed": fields_analyzed,
                "drift_detected": drift_detected,
                "resonance_score": resonance_score,
                "duration_ms": duration_ms
            }
        )
    
    @staticmethod
    def api_request(endpoint: str, method: str, params: Dict = None):
        """Strom: API Request"""
        DriftStrom.log_strom(
            strom_typ="API_REQUEST",
            data={
                "endpoint": endpoint,
                "method": method,
                "params": params or {}
            }
        )
    
    @staticmethod
    def fehler_strom(kontext: str, fehler: str, details: Dict = None):
        """Strom: Error Flow"""
        DriftStrom.log_strom(
            strom_typ="FEHLER",
            data={
                "kontext": kontext,
                "details": details or {}
            },
            erfolg=False,
            fehler=fehler
        )
