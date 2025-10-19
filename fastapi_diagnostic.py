#!/usr/bin/env python3
"""
FastAPI Diagnostic - See what the endpoint actually returns
"""

import requests
import json

OLLAMA_ENDPOINT = "http://wcn-oglaptop:8000/api/review"

# Simple test transcript
test_transcript = "This is a test of the Catalyst system. We are building a privacy-first coaching platform using local LLM inference."

print("=" * 70)
print("FASTAPI DIAGNOSTIC")
print("=" * 70)
print(f"Endpoint: {OLLAMA_ENDPOINT}")
print()

# Test prompt (simplified version)
prompt = f"""Analyze this voice note and respond with JSON:

TRANSCRIPT: {test_transcript}

Respond ONLY with valid JSON in this format:
{{
    "category": ["product-strategy"],
    "insight_type": "reflection",
    "energy": "medium",
    "actionable": false,
    "summary": "Testing the system"
}}"""

print("Sending request...")
print()

try:
    response = requests.post(
        OLLAMA_ENDPOINT,
        json={
            "text": prompt,
            "model": "mistral"
        },
        timeout=60
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    print("Raw Response:")
    print("-" * 70)
    print(response.text)
    print("-" * 70)
    print()
    
    print("Response Headers:")
    print(response.headers)
    print()
    
    if response.status_code == 200:
        print("Attempting to parse as JSON...")
        try:
            data = response.json()
            print("✓ Valid JSON response")
            print()
            print("JSON Structure:")
            print(json.dumps(data, indent=2))
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
    
except Exception as e:
    print(f"❌ Request failed: {e}")

print()
print("=" * 70)
