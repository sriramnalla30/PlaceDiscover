# Deploy to Railway (Backend)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR_TEMPLATE_ID)

## Quick Deploy Steps:

### 1. Backend Deployment (Railway)

1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. **Set Environment Variable:**
   - Variable: `GEMINI_API_KEY`
   - Value: `AIzaSyBXM1LyJjszoTvPVZlUliQ-5UyCZHwT3kY`
6. Railway will auto-deploy!

### 2. Frontend Deployment (Netlify)

1. Go to [Netlify.com](https://netlify.com)
2. Sign in with GitHub
3. Click "New site from Git"
4. Select this repository
5. **Build settings:**
   - Build command: (leave empty)
   - Publish directory: `frontend`
6. **After deployment, update backend URL:**
   - Get your Railway backend URL (like `https://your-app.railway.app`)
   - Update `frontend/script.js` line 2:
   ```javascript
   const API_BASE_URL = "https://your-railway-app.railway.app";
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