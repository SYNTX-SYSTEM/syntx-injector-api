#!/usr/bin/env python3
"""
Test SYNTX Scoring System
"""
import sys
sys.path.insert(0, 'src')

from scoring.router import score_response, get_available_scorers

# Test Format
test_format = {
    "name": "syntx_true_raw",
    "fields": [
        {"name": "driftkorper", "weight": 1.0},
        {"name": "kalibrierung", "weight": 1.0},
        {"name": "stromung", "weight": 0.7}
    ]
}

# Test Text (German, SYNTX-style)
test_text = """
Das System driftet stark nach links. Die Bewegung ist instabil und kippt.
Wir brauchen dringend Kalibrierung und Anpassung der Parameter.
Der Fluss der Energie ist gestört, der Transfer zwischen den Komponenten funktioniert nicht richtig.
"""

print("=" * 80)
print("🎯 SYNTX SCORING SYSTEM TEST")
print("=" * 80)
print("")

# Test 1: Get Available Scorers
print("TEST 1: Available Scorers")
print("-" * 80)
scorers = get_available_scorers()
print(f"Specific Scorers: {scorers['specific']}")
print(f"Fallback: {scorers['fallback']}")
print("")

# Test 2: Score Response
print("TEST 2: Score Response")
print("-" * 80)
print(f"Format: {test_format['name']}")
print(f"Fields: {len(test_format['fields'])}")
print(f"Text length: {len(test_text)} chars")
print("")

result = score_response(test_format, test_text)

print("RESULTS:")
print("-" * 80)
for field in result['scored_fields']:
    print(f"  {field['name']:20s} | Score: {field['score']:.2f} | Weight: {field['weight']:.1f} | Weighted: {field['weighted_score']:.2f} | Method: {field['scoring_method']}")

print("-" * 80)
print(f"  {'TOTAL SCORE':20s} | {result['total_score']:.2f}")
print("-" * 80)
print("")

# Test 3: Test with empty text
print("TEST 3: Empty Text Test")
print("-" * 80)
result_empty = score_response(test_format, "")
print(f"Total Score (empty): {result_empty['total_score']:.2f}")
print("")

print("=" * 80)
print("✅ ALL TESTS COMPLETED!")
print("=" * 80)
