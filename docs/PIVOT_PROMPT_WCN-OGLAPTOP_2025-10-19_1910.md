# Claude Code Prompt for wcn-oglaptop
**Created**: 2025-10-19 19:10
**Machine**: wcn-oglaptop
**Context**: Catalyst Demo API - CORS Configuration & Security Hardening

---

## Current Situation

You are working on wcn-oglaptop, which is running a FastAPI instance (`ollama_api.py`) that serves as the backend for The Catalyst demo infrastructure. This API is exposed via Cloudflare Tunnel at `https://catalyst-api.whatcomesnextllc.ai`.

### What Just Happened

1. **CORS was configured to allow all origins** (`allow_origins=["*"]`) to enable testing from wcn-workbench
2. **Test harness confirmed working** - Browser can now successfully fetch from `/status` endpoint
3. **Current API endpoints**:
   - `GET /status` - Public status widget data (WORKING, CORS enabled)
   - `POST /api/review` - Content flagging via Ollama (NEEDS SECURING)
   - `POST /api/analyze` - Generic LLM analysis via Ollama (NEEDS SECURING)
   - `GET /health` - Simple health check

### Security Concern

The `/api/review` and `/api/analyze` endpoints currently invoke Ollama and consume compute resources. With `allow_origins=["*"]`, anyone can call these endpoints from a browser. This is not acceptable for production.

---

## Your Task

**Implement Option B: Keep `/status` public, secure Ollama endpoints**

### Objectives

1. **Verify current state**:
   - Confirm `ollama_api.py` is running with CORS enabled
   - Test that `/status` endpoint responds correctly
   - Document current CORS configuration

2. **Secure the Ollama endpoints**:
   - `/status` remains public (`allow_origins=["*"]` is fine - it's read-only metadata)
   - `/api/review` and `/api/analyze` should be **disabled or heavily restricted**

3. **Implementation approach** (choose one):

   **Option A: Simple comment-out (Recommended for now)**
   ```python
   # Temporarily disable Ollama endpoints until auth is implemented
   # @app.post("/api/review")
   # async def review_segment(payload: dict):
   #     ...

   # @app.post("/api/analyze")
   # async def analyze_text(payload: dict):
   #     ...
   ```

   **Option B: IP whitelist (if you need them for local testing)**
   ```python
   from fastapi import Request, HTTPException

   ALLOWED_IPS = ["127.0.0.1", "192.168.1.0/24"]  # Local network only

   @app.post("/api/review")
   async def review_segment(request: Request, payload: dict):
       if request.client.host not in ALLOWED_IPS:
           raise HTTPException(status_code=403, detail="Access denied")
       # ... rest of function
   ```

   **Option C: Add simple API key (temporary until proper auth)**
   ```python
   from fastapi import Header, HTTPException

   API_KEY = "your-secret-key-here"  # Store in env var in production

   @app.post("/api/review")
   async def review_segment(payload: dict, x_api_key: str = Header(None)):
       if x_api_key != API_KEY:
           raise HTTPException(status_code=401, detail="Invalid API key")
       # ... rest of function
   ```

4. **Update CORS configuration**:
   Add a comment documenting the decision:
   ```python
   # CORS Configuration:
   # /status endpoint is intentionally public (demo widget needs this)
   # /api/review and /api/analyze are disabled/secured separately
   # Future: These endpoints will be gated by investor RBAC auth
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Public /status only, Ollama endpoints secured
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   ```

5. **Test the changes**:
   ```bash
   # Verify /status still works publicly
   curl https://catalyst-api.whatcomesnextllc.ai/status

   # Verify Ollama endpoints are secured
   curl -X POST https://catalyst-api.whatcomesnextllc.ai/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"prompt": "test", "model": "mistral"}'
   # Should return 403/401 or method not found
   ```

6. **Restart the service**:
   ```bash
   pkill -f uvicorn
   uvicorn ollama_api:app --host 0.0.0.0 --port 8000 &
   # Or: sudo systemctl restart ollama_api
   ```

---

## Verification Checklist

- [ ] Current `ollama_api.py` backed up: `cp ~/ollama_api.py ~/ollama_api.py.backup-$(date +%Y%m%d)`
- [ ] CORS configuration confirmed in code
- [ ] `/status` endpoint responds with 200 and valid JSON
- [ ] `/api/review` endpoint is secured (403/401 or disabled)
- [ ] `/api/analyze` endpoint is secured (403/401 or disabled)
- [ ] Service restarted successfully
- [ ] Cloudflare tunnel still routing correctly

---

## Recommendation

**Go with Option A (comment out)** for now because:
- Simplest and safest
- You're not using these endpoints in the demo anyway
- When investor RBAC is ready, you'll uncomment and add proper auth
- `/status` remains publicly accessible for the demo widget

---

## Context for Future

- The demo page will only call `GET /status` (every 30 seconds)
- The "live upload" feature (which would use `/api/analyze`) will be built later with proper auth
- This API will eventually integrate with Supabase auth for investor-gated access
- For now, we just want the green light visible, not Ollama accessible

---

## Files to Modify

- `~/ollama_api.py` - Main FastAPI application
- (Optional) `~/.bashrc` or systemd service file - If you want to set environment variables

---

## Questions to Resolve

1. Is `ollama_api.py` running as a systemd service or manually via screen/tmux?
2. Do you want to keep `/api/review` and `/api/analyze` available for local testing, or fully disable?
3. Should we add rate limiting to `/status` as well (e.g., 60 requests/minute per IP)?

---

**After completing this, the wcn-oglaptop side will be secure and ready for Phase 2 integration on wcn-workbench/wcn-spark.**
