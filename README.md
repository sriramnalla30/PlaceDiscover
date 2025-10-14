# 🗺️ PlaceDiscover - Real-time Business Discovery# AI-Powered Place Search with Generative AI

**Discover businesses with accurate, real-time data**An intelligent place search application that uses Generative AI to find cafes, restaurants, hospitals, and other places based on city, area, and type inputs.

A modern web application for searching and discovering local businesses using real-time Google data.## Features

---- 🔍 **Smart Place Discovery**: Find places by city, area, and type

- 🤖 **Gen AI Powered**: Uses Gemini API for accurate and detailed results

## ✨ Features- 📱 **Interactive UI**: Clean interface with maps and dialer integration

- 🚀 **Fast Deployment**: Optimized for free hosting platforms

- 🔍 **Real-time Search**: Get up-to-date business information

- 📍 **Location-based**: Search by city and specific area## Tech Stack

- 🏢 **Multiple Categories**: Restaurants, gyms, hospitals, hotels, banks, and more

- ⭐ **Ratings & Reviews**: See business ratings and review counts- **Frontend**: Vanilla HTML/CSS/JavaScript

- 📞 **Contact Information**: Direct phone numbers with click-to-call- **Backend**: Python FastAPI

- 🗺️ **Google Maps Integration**: One-click directions- **AI**: Google Gemini API

- 🎨 **Modern UI**: Dark theme with smooth animations- **Deployment**: Netlify (frontend) + Railway/Render (backend)

- 📱 **Responsive Design**: Works on all devices

## Project Structure

---

````

## 🚀 Quick StartPlace_Search-Gen_AI/

├── frontend/           # Frontend application

### Prerequisites│   ├── index.html     # Main HTML file

- Python 3.8+│   ├── styles.css     # Styling

- SerpStack API Key (free tier: 100 requests/month)│   ├── script.js      # JavaScript logic

│   └── assets/        # Static assets

### Installation├── backend/           # FastAPI backend

│   ├── main.py        # FastAPI application

1. **Clone the repository**│   ├── services/      # Business logic

```bash│   └── models/        # Data models

git clone https://github.com/sriramnalla30/Place_Search-Gen_AI.git├── requirements.txt   # Python dependencies

cd Place_Search-Gen_AI├── .env.example      # Environment variables template

```├── netlify.toml      # Netlify deployment config

├── railway.json      # Railway deployment config

2. **Install dependencies**└── README.md         # Documentation

```bash```

cd backend

pip install fastapi uvicorn requests python-dotenv## Getting Started

````

### Backend Setup

3. **Configure API Key**

Edit `backend/services/serpstack_service.py`:1. Install dependencies:

````python

self.api_key = "YOUR_SERPSTACK_API_KEY"```bash

```pip install -r requirements.txt

````

4. **Start the server**

```````bash2. Set up environment variables:

python -m uvicorn main:app --port 8003 --reload

``````bash

cp .env.example .env

5. **Open frontend**# Add your Gemini API key to .env

Open `frontend/index.html` in your browser```



---3. Run the backend:



## 📖 Usage```bash

uvicorn backend.main:app --reload

1. Enter city name (e.g., "Vijayawada", "Bengaluru")```

2. Enter area/locality (e.g., "Benz Circle", "Koramangala")

3. Select business type (Gym, Restaurant, Hospital, etc.)### Frontend Setup

4. Click "Search Places"

5. View results with ratings, addresses, and phone numbers1. Open `frontend/index.html` in your browser

6. Click phone to call or "Open in Maps" for directions2. Or serve with a simple HTTP server:



---```bash

python -m http.server 8000 -d frontend

## 🏗️ Project Structure```



```## Deployment

Place_Search-Gen_AI/

├── frontend/### Backend (Railway/Render)

│   ├── index.html          # Main HTML

│   ├── styles.css          # Styling- Connect your GitHub repository

│   └── script.js           # Frontend logic- Set environment variables (GEMINI_API_KEY)

├── backend/- Deploy automatically

│   ├── main.py            # FastAPI app

│   ├── services/### Frontend (Netlify)

│   │   └── serpstack_service.py  # API integration

│   └── requirements.txt- Connect your GitHub repository

└── docs/- Set publish directory to `frontend`

    └── SERPSTACK_API_GUIDE.md- Deploy automatically

```````

## Environment Variables

---

- `GEMINI_API_KEY`: Your Google Gemini API key

## 🎨 Technology Stack

## API Endpoints

**Frontend**: HTML5, CSS3, Vanilla JavaScript

**Backend**: FastAPI, Python 3.8+ - `POST /search` - Search for places

**API**: SerpStack (Real-time Google data) - `GET /health` - Health check

**Server**: Uvicorn ASGI

## Usage

---

Input format: `city: bengaluru | area: koramangala | type: cafe`

## 📱 Features

The application will return formatted results with:

### Smart Search

- City and area autocomplete- Place names

- 13+ business categories- Addresses

- Real-time validation- Phone numbers

- Google Maps integration

### Business Display- Direct dialer links

- Name and category
- Star ratings with review counts
- Full address
- Clickable phone numbers
- Action buttons (Maps, Call)

### UI/UX

- Dark theme with gradients
- Glass morphism effects
- Smooth animations
- Responsive design

---

## 🐛 Troubleshooting

**Backend won't start?**

```bash
cd backend
python -m uvicorn main:app --port 8003 --reload
```

**No results?**

- Check API key
- Verify backend is running (http://localhost:8003/docs)
- Check API quota (100/month free tier)

---

## 📄 License

MIT License - Open source

---

## 👨‍💻 Developer

**Sri Ram Nalla**

- 📧 [LinkedIn](https://www.linkedin.com/in/sri-ram-nalla-6a2a3324b/)
- 📱 +91 9391060967

---

**Made with ❤️ by Sri Ram Nalla**
