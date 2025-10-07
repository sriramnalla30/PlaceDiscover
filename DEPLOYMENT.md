# Deploy to Render (Backend) & Netlify (Frontend)

## Quick Deploy Steps:

### 1. Backend Deployment (Render - Completely Free)

1. Go to [Render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect to this repository
5. **Configuration:**
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. **Set Environment Variable:**
   - Variable: `GEMINI_API_KEY`
   - Value: `AIzaSyBXM1LyJjszoTvPVZlUliQ-5UyCZHwT3kY`
7. Click "Create Web Service"

### 2. Frontend Deployment (Netlify)

1. Go to [Netlify.com](https://netlify.com)
2. Sign in with GitHub
3. Click "New site from Git"
4. Select this repository
5. **Build settings:**
   - Build command: (leave empty)
   - Publish directory: `frontend`
6. **After deployment, update backend URL:**
   - Get your Render backend URL (like `https://your-app.onrender.com`)
   - Update `frontend/script.js` line 4:
   ```javascript
   const API_BASE_URL = "https://your-app.onrender.com";
   ```
   - Push changes to auto-redeploy

## Update Process (After Deployment)

```bash
# Make changes locally
git add .
git commit -m "Your update message"
git push origin main
# Both frontend and backend auto-deploy!
```

## Environment Variables

**Railway Backend:**

- `GEMINI_API_KEY`: Your Google Gemini API key
- `PORT`: Auto-set by Railway

**Netlify Frontend:**

- No environment variables needed
- Just update the API_BASE_URL in script.js

## Features

- ✅ Real-time place search with AI
- ✅ Support for cafes, restaurants, PGs, hotels, etc.
- ✅ Google Maps integration
- ✅ Phone dialer integration
- ✅ Mobile responsive design
- ✅ Free hosting with auto-updates
