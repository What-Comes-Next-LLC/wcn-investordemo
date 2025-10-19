# Catalyst Demo Page - Implementation Package

**Created**: October 18, 2025  
**For**: evolutions.whatcomesnextllc.ai/catalyst-demo  
**Purpose**: Live infrastructure demo with status widget

---

## 🎯 What You're Building

A React page that shows:
1. **Video walkthrough** of The Catalyst processing Sparks (you'll create this)
2. **Live status widget** polling your actual infrastructure in Michigan
3. **Architecture explanation** showing how it works
4. **Product ecosystem** showing how Catalyst fits into the bigger picture

**The Hook**: "This isn't a mock demo. It's running right now."

---

## 📦 Deliverables in This Package

### React Components

1. **CatalystDemo.jsx** - Main page component
   - Hero section with video placeholder
   - Status widget integration
   - Architecture explanation
   - Product ecosystem grid
   - Footer with branding

2. **CatalystStatusWidget.jsx** - Live status polling component
   - Fetches status from Cloudflare tunnel every 30 seconds
   - Shows: last processed, hardware, location, queue depth
   - Handles offline states gracefully
   - Real-time updates

### Styling

3. **CatalystDemo.css** - Main page styles
   - Mobile-responsive (tablet/portrait optimized)
   - Brand Kit colors (teal #216869, coral #e76f51)
   - Raleway typography
   - Smooth transitions and hover effects

4. **CatalystStatusWidget.css** - Status widget styles
   - Online/offline visual states
   - Pulsing status indicator
   - Metric cards with hover effects
   - Accessibility features

### Backend

5. **ollama_api_updated.py** - Updated FastAPI code
   - New `/status` endpoint (public, no auth)
   - CORS enabled for your React app
   - Job history tracking
   - Existing `/api/review` and `/api/analyze` preserved

### Infrastructure

6. **cloudflare_tunnel_setup.md** - Complete setup guide
   - Step-by-step tunnel creation
   - DNS configuration
   - Service installation
   - Troubleshooting
   - Security notes

---

## 🚀 Implementation Steps

### 1. Update FastAPI on wcn-oglaptop

**Current location**: `~/ollama_api.py` on wcn-oglaptop

**Action**: Add the `/status` endpoint from `ollama_api_updated.py`

```bash
# SSH to wcn-oglaptop
ssh jasonrashaad@wcn-oglaptop

# Back up current file
cp ~/ollama_api.py ~/ollama_api.py.backup

# Edit the file and add the new endpoint + CORS
nano ~/ollama_api.py
```

**What to add**:
- CORS middleware (lines 9-22 in ollama_api_updated.py)
- `/status` endpoint (lines 99-125)
- Optional: job history tracking

**Restart the service**:
```bash
# If running manually
pkill -f uvicorn
uvicorn ollama_api:app --host 0.0.0.0 --port 8000

# OR if running as service
sudo systemctl restart ollama_api  # (if you have it as a service)
```

**Test it works**:
```bash
curl http://localhost:8000/status
```

Should return JSON with hardware, location, etc.

---

### 2. Set Up Cloudflare Tunnel

**Follow**: `cloudflare_tunnel_setup.md` (complete step-by-step guide)

**Summary**:
1. Install cloudflared on wcn-oglaptop
2. Authenticate with Cloudflare
3. Create tunnel `catalyst-api`
4. Route DNS: `api.evolutions.whatcomesnextllc.ai`
5. Configure tunnel to point to `localhost:8000`
6. Install as systemd service
7. Test: `https://api.evolutions.whatcomesnextllc.ai/status`

**Expected result**: Status endpoint accessible from anywhere via HTTPS

---

### 3. Create Your Video

**Specs**:
- **Dimensions**: 1080 x 1920 (9:16 portrait)
- **Duration**: 60-90 seconds
- **Format**: MP4 (H.264), 30fps
- **Content suggestions**:
  - Terminal showing `catalyst_demo.py` running
  - Transcription happening (faster-whisper output)
  - Mistral analysis processing
  - Results appearing in markdown
  - Obsidian index.md with Dataview
  - End screen: "Running in Michigan, not AWS"

**Tools**:
- OBS Studio (free screen recorder)
- Add captions or voiceover (optional but recommended)
- Export as MP4

**Where to put it**:
- Host on your server or Cloudflare R2
- Update `CatalystDemo.jsx` line 47 with video URL

---

### 4. Integrate React Components

**In your existing React app** (evolutions.whatcomesnextllc.ai):

**Copy files to your project**:
```bash
# Assuming your React app structure
cp CatalystDemo.jsx src/components/
cp CatalystStatusWidget.jsx src/components/
cp CatalystDemo.css src/components/
cp CatalystStatusWidget.css src/components/
```

**Copy logo assets**:
```bash
# Create assets directory if needed
mkdir -p src/components/assets/

# Copy the logos you uploaded
cp The_Spark.png src/components/assets/
cp Coach_s_Clipboard.png src/components/assets/
cp What_Comes_Next.png src/components/assets/
```

**Add route in your app** (e.g., in App.jsx or Routes.jsx):
```javascript
import CatalystDemo from './components/CatalystDemo';

// In your Routes:
<Route path="/catalyst-demo" element={<CatalystDemo />} />
```

**Update video placeholder** in `CatalystDemo.jsx`:
```javascript
// Replace lines 45-59 with:
<video 
  className="demo-video"
  controls
  poster="./path-to-poster.jpg"  // Optional thumbnail
>
  <source src="./path-to-your-video.mp4" type="video/mp4" />
  Your browser doesn't support video.
</video>
```

---

### 5. Deploy and Test

**Build your React app**:
```bash
npm run build
# or
yarn build
```

**Deploy to your hosting** (Cloudflare Pages, Vercel, etc.)

**Test the page**:
1. Visit `https://evolutions.whatcomesnextllc.ai/catalyst-demo`
2. Status widget should show "🟢 Online"
3. Metrics should populate (hardware, location, etc.)
4. "Last Processed" should update when you run a demo

**Test the status polling**:
```bash
# Run a Spark through catalyst_demo.py
python catalyst_demo.py

# Watch the status widget - "Last Processed" should update within 30 seconds
```

---

## 🎨 Customization Options

### Colors (Brand Kit Aligned)

Already using:
- Teal: `#216869` (primary)
- Coral: `#e76f51` (accent)
- Sage: `#49a078` (growth/evolution)
- Charcoal: `#2d3436` (text)
- Off-white: `#f4f4f4` (background)

**To change**:
- Edit color values in CSS files
- Update gradient backgrounds in `.hero-section`, `.cta-whitepaper`, etc.

### Layout Adjustments

**Tablet-oriented** (already optimized for portrait):
- Video is 9:16 aspect ratio
- Max-width 700px for content sections
- Mobile-responsive breakpoints at 768px

**To make more desktop-focused**:
- Increase max-widths in `.video-container`, `.status-widget`
- Adjust `.video-wrapper.portrait` to landscape aspect ratio

### Status Widget Polling Interval

**Current**: 30 seconds

**To change**:
```javascript
// In CatalystStatusWidget.jsx, line 32:
const interval = setInterval(fetchStatus, 30000);  // 30000ms = 30 seconds

// Change to 60 seconds:
const interval = setInterval(fetchStatus, 60000);
```

---

## 🔒 Security Considerations

### Public Endpoints (No Auth)

**What's exposed**:
- `/status` - Hardware info, last processed timestamp
- `/health` - Simple OK check

**What's NOT exposed**:
- Actual Spark content
- Transcripts
- Analysis results
- Your home IP (hidden behind Cloudflare)

### CORS Configuration

**Currently allows**:
- `https://evolutions.whatcomesnextllc.ai`
- `https://whatcomesnextllc.ai`
- `http://localhost:3000` (for dev)

**To add more origins**, edit `ollama_api.py`:
```python
allow_origins=[
    "https://evolutions.whatcomesnextllc.ai",
    "https://another-domain.com",  # Add here
    ...
]
```

### Rate Limiting (Recommended)

**Not currently implemented**, but you should add:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/status")
@limiter.limit("60/minute")  # Max 60 requests per minute
async def public_status():
    ...
```

Install slowapi:
```bash
pip install slowapi --break-system-packages
```

---

## 📊 Monitoring & Maintenance

### Check Tunnel Status

```bash
# On wcn-oglaptop
sudo systemctl status cloudflared

# View logs
sudo journalctl -u cloudflared -f
```

### Check FastAPI Status

```bash
# On wcn-oglaptop
ps aux | grep uvicorn

# Test locally
curl http://localhost:8000/status

# Test via tunnel
curl https://api.evolutions.whatcomesnextllc.ai/status
```

### Monitor Uptime (Optional)

**Use Uptime Robot** (free tier):
1. Sign up at uptimerobot.com
2. Add monitor for: `https://api.evolutions.whatcomesnextllc.ai/status`
3. Get alerts if tunnel goes down

---

## 🐛 Troubleshooting

### Status Widget Shows "Offline"

**Check**:
1. Is cloudflared running? `sudo systemctl status cloudflared`
2. Is FastAPI running? `ps aux | grep uvicorn`
3. Can you curl the tunnel? `curl https://api.evolutions.whatcomesnextllc.ai/status`
4. Check browser console for CORS errors

### "CORS Error" in Browser Console

**Fix**: Add your domain to `allow_origins` in `ollama_api.py`

### Status Widget Shows "Loading..." Forever

**Check**:
1. Endpoint URL is correct in `CatalystStatusWidget.jsx` line 18
2. Network tab in browser - is request failing?
3. CORS is configured correctly
4. Tunnel DNS has propagated: `dig api.evolutions.whatcomesnextllc.ai`

### Video Not Playing

**Check**:
1. Video file path is correct
2. Video is in supported format (MP4/H.264)
3. File is accessible from your hosting
4. Browser supports video codec

---

## 📝 Next Steps After Implementation

### Content Creation

1. **Record the video** (see specs above)
2. **Write blog post** announcing the demo
3. **LinkedIn teaser** with link to live demo
4. **Investor email** with demo link

### Feature Additions (Future)

1. **Investor RBAC** - Gate live upload feature
2. **Live upload interface** - Let people test with their own Sparks
3. **Queue visualization** - Show processing in real-time
4. **Demo scheduling** - "Live demos Tuesday/Thursday 2-4pm"

### Analytics (Optional)

Track:
- Page views on demo page
- Status widget poll frequency
- Video play rate
- Time spent on page

Use Cloudflare Analytics (free) or Google Analytics.

---

## 🎬 Launch Checklist

Before going live:

- [ ] FastAPI `/status` endpoint working locally
- [ ] Cloudflare Tunnel configured and running as service
- [ ] DNS propagated (`dig api.evolutions.whatcomesnextllc.ai`)
- [ ] CORS configured for your React app domain
- [ ] Video recorded and hosted
- [ ] React components integrated into your app
- [ ] Logos copied to assets directory
- [ ] Page deployed and accessible
- [ ] Status widget polling successfully
- [ ] Tested on mobile (portrait orientation)
- [ ] Tested on desktop
- [ ] All links working (whitepaper, contact, etc.)

---

## 💡 Pro Tips

### The Investor Demo Pitch

**When showing this to investors**:

1. Open the page live
2. Point to the status widget: "This is polling my apartment right now"
3. SSH to wcn-oglaptop while on call
4. Run `catalyst_demo.py` with 1 Spark
5. Watch "Last Processed" timestamp update in real-time on the page
6. **Boom. They just saw it work.**

### The LinkedIn Post

**Template**:
> "We built our AI in a laundry room. Not on AWS. Not on GCP. In an apartment in Michigan.
>
> Here's the live demo: [link]
>
> The status widget on that page? It's polling actual hardware right now. GTX 1060. ZFS SAN. Local inference.
>
> Privacy by architecture, not policy.
>
> Full technical whitepaper: [link]"

### The Blog Post

**Angle**: "Why We Built Our AI in a Laundry Room (And How You Can Too)"

Structure:
1. Problem: Everyone uses cloud APIs
2. Decision: We chose local inference
3. Implementation: Here's the architecture
4. Proof: Here's the live demo
5. Invitation: Here's how to build your own

---

## 🤝 Support

**If something doesn't work**:

1. Check the troubleshooting section above
2. Review Cloudflare tunnel logs: `sudo journalctl -u cloudflared -f`
3. Check FastAPI logs (wherever you're logging uvicorn output)
4. Test each piece individually (tunnel, FastAPI, React app)

**For Cloudflare Tunnel issues**:
- Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- You've done this before with dontnobodygiveashitjason.org - same process

---

## 🎯 Success Metrics

**You'll know it's working when**:

1. ✅ Page loads at evolutions.whatcomesnextllc.ai/catalyst-demo
2. ✅ Video plays smoothly
3. ✅ Status widget shows "🟢 Online"
4. ✅ Metrics populate (hardware, location, last processed)
5. ✅ When you run catalyst_demo.py, "Last Processed" updates within 30 seconds
6. ✅ Works on mobile (portrait mode)
7. ✅ Investor looks at it and says "holy shit this is real"

---

**You got this. The pipeline works. The code is solid. Just wire it up and ship it.**

**Remember**: This isn't about perfection. It's about proving the infrastructure is real. The demo works. The privacy-first architecture exists. Everything else is polish.

---

**Files Included**:
- `CatalystDemo.jsx` - Main page component
- `CatalystStatusWidget.jsx` - Status widget component
- `CatalystDemo.css` - Main page styles
- `CatalystStatusWidget.css` - Widget styles
- `ollama_api_updated.py` - FastAPI code with /status endpoint
- `cloudflare_tunnel_setup.md` - Complete tunnel setup guide
- `README.md` - This file

**Next**: Follow implementation steps above. Start with Cloudflare Tunnel, then integrate React components.
