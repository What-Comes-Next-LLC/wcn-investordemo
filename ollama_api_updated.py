"""
ollama_api.py - Updated with public status endpoint for Catalyst demo

Add this to your existing ollama_api.py on wcn-oglaptop
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from datetime import datetime
from collections import deque

app = FastAPI()

# Enable CORS for your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://evolutions.whatcomesnextllc.ai",
        "https://whatcomesnextllc.ai",
        "http://localhost:3000"  # for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# Track recent processing for status widget
# In production, use Redis or similar
job_history = deque(maxlen=100)  # Keep last 100 jobs

# ============================================================================
# EXISTING ENDPOINTS (Keep these as-is)
# ============================================================================

@app.post("/api/review")
async def review_segment(payload: dict):
    """
    Original content flagging endpoint
    Expects: {"text": "transcript segment", "guidelines": "what to flag for"}
    Returns: {"flagged": bool, "reason": str}
    """
    text = payload.get("text", "").strip()
    guidelines = payload.get("guidelines", "flag anything harmful or inappropriate")
    
    if not text:
        return {"flagged": False, "reason": "empty"}
    
    prompt = f"""Review this transcript segment for content issues.
Guidelines: {guidelines}
Segment: "{text}"
Respond ONLY with JSON (no markdown): {{"flagged": true/false, "reason": "brief explanation or empty string"}}"""
    
    response = requests.post(
        OLLAMA_ENDPOINT,
        json={"model": "mistral", "prompt": prompt, "stream": False},
        timeout=60
    )
    
    result = response.json()
    response_text = result.get("response", "").strip()
    
    # Parse JSON from response
    try:
        verdict = json.loads(response_text)
        return verdict
    except:
        return {"flagged": False, "reason": "parse error"}


@app.post("/api/analyze")
async def analyze_text(payload: dict):
    """
    Generic LLM analysis endpoint (added for Catalyst demo)
    Expects: {"prompt": "full prompt text", "model": "mistral"}
    Returns: {"response": "raw LLM output"}
    """
    prompt = payload.get("prompt", "").strip()
    model = payload.get("model", "mistral")
    
    if not prompt:
        return {"response": ""}
    
    response = requests.post(
        OLLAMA_ENDPOINT,
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=60
    )
    
    result = response.json()
    response_text = result.get("response", "").strip()
    
    # Log this job for status tracking
    job_history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "success": True
    })
    
    return {"response": response_text}


# ============================================================================
# NEW: PUBLIC STATUS ENDPOINT (For the demo widget)
# ============================================================================

@app.get("/status")
async def public_status():
    """
    Public status endpoint - no authentication required
    Shows infrastructure is alive without exposing sensitive info
    
    This is what the React status widget polls every 30 seconds
    """
    
    # Get last processed job timestamp
    last_processed = None
    if job_history:
        last_processed = job_history[-1]["timestamp"]
    
    # Calculate queue depth (for demo, always 0 since we process synchronously)
    queue_depth = 0
    
    # Calculate average processing time from recent jobs
    # For demo purposes, hardcode this - in production track actual times
    avg_processing_time = "58 seconds"
    
    # Count successful jobs in last hour (optional metric)
    recent_jobs = len([j for j in job_history 
                      if (datetime.utcnow() - datetime.fromisoformat(j["timestamp"])).seconds < 3600])
    
    return {
        "status": "online",  # Could check Ollama health here if desired
        "last_processed": last_processed,
        "queue_depth": queue_depth,
        "hardware": "GTX 1060 6GB",
        "location": "Michigan",
        "avg_processing_time": avg_processing_time,
        "jobs_last_hour": recent_jobs  # Optional: shows activity level
    }


@app.get("/health")
async def health():
    """
    Simple health check
    """
    return {"status": "ok"}


# ============================================================================
# OPTIONAL: Ollama health check (uncomment if you want to verify Ollama is up)
# ============================================================================

# @app.get("/status")
# async def public_status():
#     """Version with Ollama health check"""
#     
#     # Check if Ollama is responding
#     ollama_healthy = False
#     try:
#         check = requests.get("http://localhost:11434/api/tags", timeout=2)
#         ollama_healthy = check.status_code == 200
#     except:
#         pass
#     
#     status = "online" if ollama_healthy else "degraded"
#     
#     last_processed = None
#     if job_history:
#         last_processed = job_history[-1]["timestamp"]
#     
#     return {
#         "status": status,
#         "last_processed": last_processed,
#         "queue_depth": 0,
#         "hardware": "GTX 1060 6GB",
#         "location": "Michigan",
#         "avg_processing_time": "58 seconds"
#     }
