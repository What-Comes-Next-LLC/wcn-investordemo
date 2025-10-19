# Cloudflare Tunnel Setup Guide - Catalyst Demo Status Endpoint

**Goal**: Expose `http://wcn-oglaptop:8000/status` as `https://api.evolutions.whatcomesnextllc.ai/status`

**What you're doing**: Creating a secure tunnel from Cloudflare's edge to your apartment so the React widget can poll your infrastructure status without exposing your home IP.

---

## Prerequisites

- [ ] Domain registered with Cloudflare (you have whatcomesnextllc.ai)
- [ ] FastAPI running on wcn-oglaptop port 8000
- [ ] SSH access to wcn-oglaptop

---

## Step 1: Install cloudflared on wcn-oglaptop

**SSH into wcn-oglaptop:**
```bash
ssh jasonrashaad@wcn-oglaptop
```

**Install cloudflared (Debian):**
```bash
# Download the package
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Install it
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify installation
cloudflared --version
```

---

## Step 2: Authenticate with Cloudflare

**Run the login command:**
```bash
cloudflared tunnel login
```

This will:
1. Open a browser window (or give you a URL to paste)
2. Ask you to select your domain (whatcomesnextllc.ai)
3. Download a cert to `~/.cloudflared/cert.pem`

**Verify the cert exists:**
```bash
ls -la ~/.cloudflared/cert.pem
```

You should see a file created. This proves you're authenticated.

---

## Step 3: Create the Tunnel

**Create a named tunnel:**
```bash
cloudflared tunnel create catalyst-api
```

**Output will look like:**
```
Tunnel credentials written to /home/jasonrashaad/.cloudflared/<TUNNEL-ID>.json
Created tunnel catalyst-api with id <TUNNEL-ID>
```

**Save that TUNNEL-ID** - you'll need it in a moment.

**List your tunnels to verify:**
```bash
cloudflared tunnel list
```

You should see `catalyst-api` listed.

---

## Step 4: Configure DNS

**Point your subdomain to the tunnel:**
```bash
cloudflared tunnel route dns catalyst-api api.evolutions.whatcomesnextllc.ai
```

This creates a CNAME record in Cloudflare DNS:
- `api.evolutions.whatcomesnextllc.ai` → `<TUNNEL-ID>.cfargotunnel.com`

**Verify in Cloudflare Dashboard:**
1. Go to cloudflare.com → Domains → whatcomesnextllc.ai
2. Click "DNS" in the sidebar
3. You should see a new CNAME record for `api.evolutions`

---

## Step 5: Create Tunnel Configuration File

**Create the config file:**
```bash
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

**Paste this config:**
```yaml
tunnel: <TUNNEL-ID>
credentials-file: /home/jasonrashaad/.cloudflared/<TUNNEL-ID>.json

ingress:
  # Route all requests to api.evolutions.whatcomesnextllc.ai to your FastAPI
  - hostname: api.evolutions.whatcomesnextllc.ai
    service: http://localhost:8000
  
  # Catch-all rule (required by cloudflared)
  - service: http_status:404
```

**Replace `<TUNNEL-ID>` with your actual tunnel ID from Step 3.**

**Save and exit** (Ctrl+X, then Y, then Enter in nano)

**Verify the config:**
```bash
cat ~/.cloudflared/config.yml
```

---

## Step 6: Test the Tunnel (Dry Run)

**Start the tunnel in foreground to test:**
```bash
cloudflared tunnel run catalyst-api
```

**You should see:**
```
2025-10-18T... INF Connection registered connIndex=0
2025-10-18T... INF Connection registered connIndex=1
...
```

**In another terminal (or from your workbench), test the endpoint:**
```bash
curl https://api.evolutions.whatcomesnextllc.ai/health
```

**Expected response:**
```json
{"status": "ok"}
```

**If that works, CONGRATULATIONS! The tunnel is live.**

**Stop the tunnel** (Ctrl+C in the cloudflared terminal)

---

## Step 7: Run Tunnel as a Service (Persistent)

**Install the tunnel as a systemd service:**
```bash
sudo cloudflared service install
```

**Start the service:**
```bash
sudo systemctl start cloudflared
```

**Enable it to start on boot:**
```bash
sudo systemctl enable cloudflared
```

**Check status:**
```bash
sudo systemctl status cloudflared
```

You should see `active (running)`.

---

## Step 8: Verify Everything Works

**Test the status endpoint:**
```bash
curl https://api.evolutions.whatcomesnextllc.ai/status
```

**Expected response:**
```json
{
  "status": "online",
  "last_processed": null,
  "queue_depth": 0,
  "hardware": "GTX 1060 6GB",
  "location": "Michigan",
  "avg_processing_time": "58 seconds",
  "jobs_last_hour": 0
}
```

**Test from your React app** (or just open in browser):
```
https://api.evolutions.whatcomesnextllc.ai/status
```

If you see JSON, **YOU'RE DONE!**

---

## Step 9: Update Your React App

**In your React code, the status widget is already configured to use:**
```javascript
fetch('https://api.evolutions.whatcomesnextllc.ai/status')
```

**Deploy your React app** and the status widget should start polling your apartment.

---

## Troubleshooting

### "Connection refused" when testing

**Check FastAPI is running:**
```bash
# On wcn-oglaptop
ps aux | grep uvicorn
```

If not running:
```bash
cd ~
uvicorn ollama_api:app --host 0.0.0.0 --port 8000
```

### "Tunnel not found"

**List tunnels to verify it exists:**
```bash
cloudflared tunnel list
```

If missing, recreate from Step 3.

### "DNS resolution failed"

**Check DNS propagation:**
```bash
dig api.evolutions.whatcomesnextllc.ai
```

Should return a CNAME to cfargotunnel.com. May take a few minutes to propagate.

### "404 Not Found" from tunnel

**Check your config.yml:**
- Hostname matches exactly: `api.evolutions.whatcomesnextllc.ai`
- Service points to correct port: `http://localhost:8000`
- Tunnel ID is correct

Restart the service after config changes:
```bash
sudo systemctl restart cloudflared
```

### Tunnel service won't start

**Check logs:**
```bash
sudo journalctl -u cloudflared -f
```

Look for errors about missing credentials or config files.

---

## Security Notes

### What's Exposed
- **Only `/status` and `/health` endpoints** are publicly accessible
- **No authentication required** (by design - public status widget)
- **No sensitive data** exposed (hardware info only)

### What's Protected
- Your home IP (hidden behind Cloudflare)
- Direct access to wcn-oglaptop (tunnel is one-way outbound)
- All other services on your network (only port 8000 is tunneled)

### Rate Limiting (Optional but Recommended)

Add this to your FastAPI:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/status")
@limiter.limit("60/minute")  # 60 requests per minute max
async def public_status(request: Request):
    ...
```

---

## Management Commands Reference

```bash
# Check tunnel status
sudo systemctl status cloudflared

# View logs
sudo journalctl -u cloudflared -f

# Stop tunnel
sudo systemctl stop cloudflared

# Start tunnel
sudo systemctl start cloudflared

# Restart tunnel (after config changes)
sudo systemctl restart cloudflared

# List all your tunnels
cloudflared tunnel list

# Delete a tunnel (if you need to start over)
cloudflared tunnel delete catalyst-api
```

---

## What You Just Built

```
User Browser (anywhere in world)
    ↓
https://api.evolutions.whatcomesnextllc.ai/status
    ↓
Cloudflare Edge (DDoS protection, caching)
    ↓
Cloudflare Tunnel (encrypted connection)
    ↓
wcn-oglaptop:8000 (your apartment)
    ↓
FastAPI /status endpoint
    ↓
Returns JSON status
```

**Key Benefits:**
- No port forwarding on your router
- No exposing your home IP
- Free DDoS protection from Cloudflare
- Automatic HTTPS (Cloudflare handles SSL)
- Can turn it off anytime (just stop the service)

---

## Next Steps

1. **Test the React widget** - deploy your app and watch the status update
2. **Monitor the logs** - keep an eye on requests for the first few days
3. **Set up monitoring** - use Uptime Robot to ping the status endpoint
4. **Add rate limiting** - protect against abuse (see Security Notes above)

---

**You got this. This is the exact same tunnel setup you used for dontnobodygiveashitjason.org, just pointing to a different service.**
