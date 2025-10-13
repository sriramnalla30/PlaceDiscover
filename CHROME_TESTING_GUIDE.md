# 🌐 How to Test in Chrome Browser

## 🚀 Quick Start (Easiest Way)

### Option 1: Double-Click Batch File

1. **Double-click** `START_APP.bat` in the project root
2. Backend starts automatically
3. Chrome opens automatically
4. Start searching! 🎉

---

## 📋 Manual Setup (Step-by-Step)

### Step 1: Start Backend Server

**Option A: Using PowerShell**

```powershell
cd backend
python -m uvicorn main:app --port 8003 --reload
```

**Option B: Using Command Prompt**

```cmd
cd backend
python -m uvicorn main:app --port 8003 --reload
```

**You should see:**

```
INFO:     Uvicorn running on http://127.0.0.1:8003
INFO:     Application startup complete.
```

✅ **Backend is ready!**

---

### Step 2: Open Frontend in Chrome

**Option A: File Explorer**

1. Navigate to: `d:\gitcode\Projects\Place_Search\Place_Search-Gen_AI\frontend`
2. **Right-click** on `index.html`
3. Select **"Open with"** → **"Google Chrome"**

**Option B: Chrome Address Bar**

1. Open Chrome
2. Press `Ctrl + L` (focus address bar)
3. Paste: `file:///d:/gitcode/Projects/Place_Search/Place_Search-Gen_AI/frontend/index.html`
4. Press Enter

**Option C: Drag and Drop**

1. Open Chrome
2. Open File Explorer to frontend folder
3. **Drag** `index.html` into Chrome window

---

## 🧪 Test the Application

### 1. Fill in the Search Form:

- **City**: `Vijayawada`
- **Area**: `Benz Circle`
- **Type**: Select `Gym`

### 2. Click "Get Suggestions"

### 3. Expected Results:

You should see **real gyms** with:

- ✅ **Real Business Names** (MultiFit, Golden Fitness, Gold's Gym)
- ⭐ **Google Ratings** (4.8 stars, 4.7 stars, etc.)
- 📊 **Review Counts** (407 reviews, 532 reviews, etc.)
- 📍 **Real Addresses** in Benz Circle
- 🔖 **Source Tag**: "SerpStack (Google Local)"

---

## 🎯 What You Should See

### Search Interface:

```
╔════════════════════════════════════════════╗
║  🔍 Place Search                          ║
║  Find cafes, restaurants, and more        ║
╠════════════════════════════════════════════╣
║  City:  [Vijayawada          ]            ║
║  Area:  [Benz Circle         ]            ║
║  Type:  [Gym ▼               ]            ║
║         [🔍 Get Suggestions  ]            ║
╚════════════════════════════════════════════╝
```

### Results Display:

```
╔════════════════════════════════════════════╗
║  MultiFit - Best Functional Classes       ║
║  Gym                        ⭐ 4.8 (407)   ║
║  📍 2nd Floor, Vajra Commercial Complex   ║
║  ✅ SerpStack (Google Local)              ║
║  [🗺️ Get Directions] [📞 Call Now]       ║
╠════════════════════════════════════════════╣
║  Golden Fitness Gym                       ║
║  Gym                        ⭐ 4.7 (532)   ║
║  📍 40-27-7, Polyclinic Rd               ║
║  ✅ SerpStack (Google Local)              ║
║  [🗺️ Get Directions] [📞 Call Now]       ║
╚════════════════════════════════════════════╝
```

---

## 🔧 Troubleshooting

### Issue 1: "Failed to search places"

**Problem**: Backend not running or wrong port

**Solution**:

1. Check if backend is running: Open `http://localhost:8003/docs` in browser
2. If not working, restart backend:
   ```powershell
   cd backend
   python -m uvicorn main:app --port 8003 --reload
   ```

### Issue 2: No results shown

**Problem**: SerpStack API timeout or quota exceeded

**Solution**:

1. Check terminal output for errors
2. Verify `.env` file exists in `backend/` folder with:
   ```
   SERPSTACK_API_KEY=088f24b4864557232354176ec84fceb7
   ```
3. Check SerpStack quota: https://serpstack.com/dashboard

### Issue 3: CORS Error in Browser Console

**Problem**: Frontend can't connect to backend

**Solution**:

1. Backend automatically allows CORS for all origins
2. If still having issues, check if backend is on correct port (8003)
3. Check browser console (F12) for exact error

### Issue 4: Chrome shows blank page

**Problem**: File path issue

**Solution**:

1. Make sure all files are in correct locations:
   ```
   frontend/
   ├── index.html
   ├── script.js
   └── styles.css
   ```
2. Check browser console (F12) for JavaScript errors

---

## 🌐 Alternative: Use Live Server (Optional)

If you want a proper local server instead of `file://`:

### Install Live Server Extension (VS Code)

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for "Live Server"
4. Install by Ritwick Dey
5. Right-click `index.html` → "Open with Live Server"
6. Opens at `http://127.0.0.1:5500/frontend/index.html`

---

## 📊 Test Different Searches

### Test Case 1: Cafes

- City: `Bangalore`
- Area: `Koramangala`
- Type: `Cafe`

### Test Case 2: Restaurants

- City: `Delhi`
- Area: `Connaught Place`
- Type: `Restaurant`

### Test Case 3: Hospitals

- City: `Mumbai`
- Area: `Bandra`
- Type: `Hospital`

---

## ✅ Success Checklist

- [ ] Backend running on `http://localhost:8003`
- [ ] Frontend opens in Chrome
- [ ] Can fill in City, Area, Type
- [ ] Click "Get Suggestions" shows loading spinner
- [ ] Results appear with real business names
- [ ] Ratings and reviews visible (⭐ 4.8 stars)
- [ ] Source tag shows "SerpStack (Google Local)"
- [ ] "Get Directions" opens Google Maps
- [ ] "Call Now" opens phone dialer (mobile)

---

## 🎉 You're All Set!

Your Place Search app is now running with:

- ✅ **100% Real Google Data** from SerpStack
- ✅ **Zero AI Hallucinations**
- ✅ **Verified Ratings & Reviews**
- ✅ **Fast 1-2 second responses**

**Enjoy searching for real places!** 🚀

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8003/docs
- **Backend Logs**: Check terminal where uvicorn is running
- **Frontend Console**: Press F12 in Chrome → Console tab
- **Network Tab**: F12 → Network → See API requests/responses

---

**Need Help?**

- Check backend terminal for error messages
- Check Chrome console (F12) for JavaScript errors
- Verify `.env` file has correct SerpStack API key
- Ensure port 8003 is not blocked by firewall
