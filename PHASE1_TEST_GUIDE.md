# Phase 1 Test Guide - Catalyst Demo Standalone Test

**Machine**: wcn-workbench
**Date**: October 19, 2025
**API Endpoint**: `https://catalyst-api.whatcomesnextllc.ai/status`

---

## ✅ Phase 1 Completion Status

### Completed Tasks
1. ✅ **API Endpoint Updated** - Changed from `api.evolutions` to `catalyst-api` in CatalystStatusWidget.jsx:15
2. ✅ **Fresh SVG Logos Copied** - All product logos copied from wcn-spark to `./assets/`
3. ✅ **Standalone Test Harness Created** - `test-harness.html` ready for testing
4. ✅ **API Connectivity Verified** - Endpoint responding with HTTP 200 (0.51s response time)

---

## 🧪 How to Test

### Method 1: Direct File Opening (Quickest)
1. Navigate to: `/mnt/c/Users/Jason Rashaad/dev/wcn-investordemo/`
2. Open `test-harness.html` in a web browser:
   ```bash
   # From WSL
   explorer.exe test-harness.html

   # Or from Windows
   # Navigate to C:\Users\Jason Rashaad\dev\wcn-investordemo\test-harness.html
   # Double-click to open in default browser
   ```

### Method 2: Local HTTP Server (Recommended for CORS testing)
```bash
# From wcn-investordemo directory
cd "/mnt/c/Users/Jason Rashaad/dev/wcn-investordemo"

# Option A: Python
python3 -m http.server 8080

# Option B: Node.js (if you have http-server installed)
npx http-server -p 8080

# Then open: http://localhost:8080/test-harness.html
```

---

## 🔍 What to Verify

### 1. Initial Load
- [ ] Page loads without errors
- [ ] Test header shows "Phase 1 Standalone Test Environment"
- [ ] WCN logo displays correctly
- [ ] Status widget appears and shows "Checking infrastructure status..."

### 2. API Connection
- [ ] Status widget transitions from "loading" to "online" state
- [ ] Green dot (🟢) appears with "Infrastructure Online" label
- [ ] Bottom-right corner shows: `✓ API Connected | Last fetch: [time]`
- [ ] No CORS errors in browser console (F12 → Console tab)

### 3. Live Data Display
Check that the following metrics populate:
- [ ] **Last Processed**: Shows "Unknown" (since no jobs run yet) or timestamp
- [ ] **Hardware**: "GTX 1060 6GB"
- [ ] **Location**: "Michigan"
- [ ] **Avg Processing Time**: "58 seconds"
- [ ] **Current Queue**: "0 jobs"

### 4. Polling Behavior
- [ ] "Last checked" timestamp updates every 30 seconds
- [ ] Bottom-right status indicator updates with new fetch times
- [ ] No console errors during polling cycles

### 5. Product Ecosystem Section
- [ ] All three product logos display:
  - [ ] The Spark.svg
  - [ ] What Comes Next.svg (as The Catalyst)
  - [ ] Coach's Clipboard.svg
- [ ] Logos render cleanly (no broken image icons)

### 6. Error State Testing (Optional)
To test offline state:
1. Temporarily disable internet connection
2. Refresh page
3. Should show: 🔴 "Offline" with error message
4. Re-enable connection
5. Should auto-recover on next poll (within 30s)

---

## 📊 Expected API Response

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

---

## 🐛 Troubleshooting

### Issue: CORS Error
**Symptom**: Console shows `blocked by CORS policy`
**Solution**: Use Method 2 (local HTTP server) instead of opening file directly

### Issue: Logo Not Displaying
**Symptom**: Broken image icons
**Check**:
1. Verify `./assets/` directory exists
2. Confirm SVG files are present: `ls -la assets/`
3. Check browser console for 404 errors on image paths

### Issue: Status Widget Stuck on "Loading"
**Symptom**: Widget never transitions to online/offline
**Check**:
1. Browser console for fetch errors
2. API is reachable: `curl https://catalyst-api.whatcomesnextllc.ai/status`
3. No network firewall blocking the request

### Issue: Styles Not Applied
**Symptom**: Unstyled content
**Check**:
1. Verify CSS files exist in same directory as test-harness.html
2. Check browser console for CSS load errors
3. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

---

## 📁 File Structure After Phase 1

```
wcn-investordemo/
├── assets/
│   ├── The Spark.svg ✓
│   ├── Coach's Clipboard.svg ✓
│   └── What Comes Next.svg ✓
├── CatalystDemo.jsx ✓
├── CatalystDemo.css ✓
├── CatalystStatusWidget.jsx ✓ (API endpoint updated)
├── CatalystStatusWidget.css ✓
├── test-harness.html ✓ (NEW)
├── PHASE1_TEST_GUIDE.md ✓ (NEW - this file)
└── [other files...]
```

---

## ✅ Success Criteria

Phase 1 is complete when:
1. ✅ Test harness opens without errors
2. ✅ API connectivity confirmed (green status, live metrics)
3. ✅ All logos display correctly
4. ✅ Polling works (30s intervals, no errors)
5. ✅ Tested from wcn-workbench machine

---

## 🚀 Next Steps (Phase 2)

After Phase 1 verification:
1. Convert components to TypeScript (.jsx → .tsx)
2. Integrate into wcn-spark routing (App.tsx)
3. Convert CSS to Tailwind classes
4. Add route navigation from Evolutions page
5. Build and deploy to production

---

**Test completed by**: [Your name]
**Test date**: [Date]
**Browser tested**: [Chrome/Firefox/Safari/Edge]
**Result**: [PASS/FAIL]
**Notes**: [Any observations]
