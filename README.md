# 🗺️ PlaceDiscover - Real-time Business Discovery 
## URL: https://placediscover.netlify.app/ ##

Discover local businesses with accurate, real-time Google data. PlaceDiscover is a modern web application for searching and discovering local businesses (restaurants, gyms, hospitals, hotels, banks, etc.) with ratings, contact info, and map directions.

---

## ✨ Features

- 🔍 Real-time Search: Up-to-date business information via SerpStack
- 📍 Location-based: Search by city and area/locality
- 🏷️ Multiple Categories: Restaurants, gyms, hospitals, hotels, banks, cafes, and more (13+ categories)
- ⭐ Ratings & Reviews: Star ratings with review counts
- 📞 Contact Information: Click-to-call phone numbers
- 🗺️ Google Maps Integration: One-click directions / Open in Maps
- 🎨 Modern UI: Dark theme, smooth animations, glassmorphism effects
- 📱 Responsive Design: Works across devices

---

## 🎨 Technology Stack

- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: FastAPI (Python 3.8+)
- API: SerpStack (for real-time Google data)
- Server: Uvicorn ASGI

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- SerpStack API Key (free tier: 100 requests/month)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sriramnalla30/PlaceDiscover.git
   cd PlaceDiscover
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install fastapi uvicorn requests python-dotenv
   ```

3. Configure API key:
   - Edit `backend/services/serpstack_service.py` and set:
     ```python
     self.api_key = "YOUR_SERPSTACK_API_KEY"
     ```
   - Or use environment variables (recommended). Copy `.env.example` to `.env` and set your API key there.

4. Start the backend server:
   ```bash
   cd backend
   python -m uvicorn main:app --port 8003 --reload
   ```

5. Open the frontend:
   - Open `frontend/index.html` in your browser
   - Or serve the frontend with a simple HTTP server:
     ```bash
     python -m http.server 8000 -d frontend
     ```

---

## 📖 Usage

Input format for the backend /search endpoint:
- Example: `city: bengaluru | area: koramangala | type: cafe`

Typical flow:
1. Enter city name (e.g., "Vijayawada", "Bengaluru")
2. Enter area/locality (e.g., "Benz Circle", "Koramangala")
3. Select business type (Gym, Restaurant, Hospital, etc.)
4. Click "Search Places"
5. View results with ratings, addresses, phone numbers; click phone to call or "Open in Maps" for directions

### API Endpoints
- POST /search — Search for places
- GET /health — Health check

---

## 🏗️ Project Structure

PlaceDiscover/
- frontend/
  - index.html          # Main HTML
  - styles.css          # Styling
  - script.js           # Frontend logic
- backend/
  - main.py             # FastAPI app
  - services/
    - serpstack_service.py  # API integration
  - requirements.txt
- docs/
  - SERPSTACK_API_GUIDE.md

---

## 🐛 Troubleshooting

- Backend won't start?
  ```bash
  cd backend
  python -m uvicorn main:app --port 8003 --reload
  ```
- No results?
  - Check your SerpStack API key in `backend/services/serpstack_service.py` or .env
  - Verify backend is running: http://localhost:8003/docs
  - Check API quota (SerpStack free tier: 100 requests/month)

---

## Deployment

- Backend: Host on Render, or other similar platforms — connect your GitHub repo and deploy backend code.
- Frontend: Host on Netlify, Vercel, GitHub Pages, or serve through a static host with publish directory set to `frontend`.


---

## 👨‍💻 Developer

**Sri Ram Nalla**

- GitHub: https://github.com/sriramnalla30
- LinkedIn: https://www.linkedin.com/in/sri-ram-nalla-6a2a3324b/
- Phone: +91 9391060967

---

Made with ❤️ by Sri Ram Nalla
