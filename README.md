# AI-Powered Place Search with Generative AI

An intelligent place search application that uses Generative AI to find cafes, restaurants, hospitals, and other places based on city, area, and type inputs.

## Features

- 🔍 **Smart Place Discovery**: Find places by city, area, and type
- 🤖 **Gen AI Powered**: Uses Gemini API for accurate and detailed results
- 📱 **Interactive UI**: Clean interface with maps and dialer integration
- 🚀 **Fast Deployment**: Optimized for free hosting platforms

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Backend**: Python FastAPI
- **AI**: Google Gemini API
- **Deployment**: Netlify (frontend) + Railway/Render (backend)

## Project Structure

```
Place_Search-Gen_AI/
├── frontend/           # Frontend application
│   ├── index.html     # Main HTML file
│   ├── styles.css     # Styling
│   ├── script.js      # JavaScript logic
│   └── assets/        # Static assets
├── backend/           # FastAPI backend
│   ├── main.py        # FastAPI application
│   ├── services/      # Business logic
│   └── models/        # Data models
├── requirements.txt   # Python dependencies
├── .env.example      # Environment variables template
├── netlify.toml      # Netlify deployment config
├── railway.json      # Railway deployment config
└── README.md         # Documentation
```

## Getting Started

### Backend Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
cp .env.example .env
# Add your Gemini API key to .env
```

3. Run the backend:

```bash
uvicorn backend.main:app --reload
```

### Frontend Setup

1. Open `frontend/index.html` in your browser
2. Or serve with a simple HTTP server:

```bash
python -m http.server 8000 -d frontend
```

## Deployment

### Backend (Railway/Render)

- Connect your GitHub repository
- Set environment variables (GEMINI_API_KEY)
- Deploy automatically

### Frontend (Netlify)

- Connect your GitHub repository
- Set publish directory to `frontend`
- Deploy automatically

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key

## API Endpoints

- `POST /search` - Search for places
- `GET /health` - Health check

## Usage

Input format: `city: bengaluru | area: koramangala | type: cafe`

The application will return formatted results with:

- Place names
- Addresses
- Phone numbers
- Google Maps integration
- Direct dialer links

## License

MIT License
