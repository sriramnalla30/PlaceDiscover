# 🗺️ PlaceDiscover - Real-time Business Discovery# 🗺️ PlaceDiscover - Real-time Business Discovery# 🗺️ PlaceDiscover - Real-time Business Discovery

**Discover businesses with accurate, real-time data\*\***Discover businesses with accurate, real-time data\*\*\*\*Discover businesses with accurate, real-time data\*\*

A modern web application for searching and discovering local businesses using real-time Google data.A modern web application for searching and discovering local businesses using real-time Google data.A modern web application for searching and discovering local businesses using real-time Google data.

---

## ✨ Features## ✨ Features## ✨ Features

- 🔍 **Real-time Search**: Get up-to-date business information- 🔍 **Real-time Search**: Get up-to-date business information- **Real-time Search**: Get up-to-date business information

- 📍 **Location-based**: Search by city and specific area

- 🏢 **Multiple Categories**: Restaurants, gyms, hospitals, hotels, banks, and more- 📍 **Location-based**: Search by city and specific area- 📍 **Location-based**: Search by city and specific area

- ⭐ **Ratings & Reviews**: See business ratings and review counts

- 📞 **Contact Information**: Direct phone numbers with click-to-call- 🏢 **Multiple Categories**: Restaurants, gyms, hospitals, hotels, banks, and more- 🏢 **Multiple Categories**: Restaurants, gyms, hospitals, hotels, banks, and more

- 🗺️ **Google Maps Integration**: One-click directions

- 🎨 **Modern UI**: Dark theme with smooth animations- ⭐ **Ratings & Reviews**: See business ratings and review counts- ⭐ **Ratings & Reviews**: See business ratings and review counts

- 📱 **Responsive Design**: Works on all devices

- 📞 **Contact Information**: Direct phone numbers with click-to-call- 📞 **Contact Information**: Direct phone numbers with click-to-call

---

- 🗺️ **Google Maps Integration**: One-click directions- 🗺️ **Google Maps Integration**: One-click directions

## 🎨 Technology Stack

- 🎨 **Modern UI**: Dark theme with smooth animations- 🎨 **Modern UI**: Dark theme with smooth animations

**Frontend**: HTML5, CSS3, Vanilla JavaScript

**Backend**: FastAPI, Python 3.8+ - 📱 **Responsive Design**: Works on all devices- 📱 **Responsive Design**: Works on all devices

**API**: SerpStack (Real-time Google data)

**Server**: Uvicorn ASGI---

---## 🎨 Technology Stack## 🎨 Technology Stack

## 🚀 Quick Start**Frontend**: HTML5, CSS3, Vanilla JavaScript **Frontend**: HTML5, CSS3, Vanilla JavaScript

### Prerequisites**Backend**: FastAPI, Python 3.8+ **Backend**: FastAPI, Python 3.8+

- Python 3.8+

- SerpStack API Key (free tier: 100 requests/month)**API**: SerpStack (Real-time Google data) **API**: SerpStack (Real-time Google data)

### Installation**Server**: Uvicorn ASGI**Server**: Uvicorn ASGI

1. **Clone the repository**---

````bash

git clone https://github.com/sriramnalla30/PlaceDiscover.git## 🚀 Quick Start## 🚀 Quick Start

cd PlaceDiscover

```### Prerequisites### Prerequisites



2. **Install dependencies**- Python 3.8+- Python 3.8+

```bash

cd backend- SerpStack API Key (free tier: 100 requests/month)- SerpStack API Key (free tier: 100 requests/month)

pip install fastapi uvicorn requests python-dotenv

```### Installation### Installation



3. **Configure API Key**1. **Clone the repository**1. **Clone the repository**



Edit `backend/services/serpstack_service.py`:`bash`bash

```python

self.api_key = "YOUR_SERPSTACK_API_KEY"git clone https://github.com/sriramnalla30/PlaceDiscover.gitgit clone https://github.com/sriramnalla30/PlaceDiscover.git

````

cd PlaceDiscovercd PlaceDiscover

4. **Start the server**

```bash````

cd backend

python -m uvicorn main:app --port 8003 --reload

````

2. **Install dependencies**2. **Install dependencies**

5. **Open frontend**

```bash```bash

Open `frontend/index.html` in your browser

cd backendcd backend

---

pip install fastapi uvicorn requests python-dotenvpip install fastapi uvicorn requests python-dotenv

## 📖 Usage

````

1. Enter city name (e.g., "Vijayawada", "Bengaluru")

2. Enter area/locality (e.g., "Benz Circle", "Koramangala")3. **Configure API Key**### Backend Setup

3. Select business type (Gym, Restaurant, Hospital, etc.)

4. Click "Search Places"Edit `backend/services/serpstack_service.py`:3. **Configure API Key**

5. View results with ratings, addresses, and phone numbers

6. Click phone to call or "Open in Maps" for directions```python

---self.api_key = "YOUR_SERPSTACK_API_KEY"Edit `backend/services/serpstack_service.py`:1. Install dependencies:

## 🏗️ Project Structure```

`````````python

PlaceDiscover/

├── frontend/4. **Start the server**

│   ├── index.html          # Main HTML

│   ├── styles.css          # Styling```bashself.api_key = "YOUR_SERPSTACK_API_KEY"```bash

│   └── script.js           # Frontend logic

├── backend/cd backend

│   ├── main.py            # FastAPI app

│   ├── services/python -m uvicorn main:app --port 8003 --reload```pip install -r requirements.txt

│   │   └── serpstack_service.py  # API integration

│   └── requirements.txt```

└── docs/

    └── SERPSTACK_API_GUIDE.md````

```

5. **Open frontend**

---

6. **Start the server**

## 📱 Features Details

Open `frontend/index.html` in your browser

### Smart Search

- City and area autocomplete````````bash2. Set up environment variables:

- 13+ business categories

- Real-time validation---



### Business Displaypython -m uvicorn main:app --port 8003 --reload

- Name and category

- Star ratings with review counts## 📖 Usage

- Full address

- Clickable phone numbers``````bash

- Action buttons (Maps, Call)

1. Enter city name (e.g., "Vijayawada", "Bengaluru")

### UI/UX

- Dark theme with gradients2. Enter area/locality (e.g., "Benz Circle", "Koramangala")cp .env.example .env

- Glass morphism effects

- Smooth animations3. Select business type (Gym, Restaurant, Hospital, etc.)

- Responsive design

4. Click "Search Places"5. **Open frontend**# Add your Gemini API key to .env

---

5. View results with ratings, addresses, and phone numbers

## 🐛 Troubleshooting

6. Click phone to call or "Open in Maps" for directionsOpen `frontend/index.html` in your browser```

**Backend won't start?**

```bash

cd backend

python -m uvicorn main:app --port 8003 --reload---

```



**No results?**

- Check API key in `backend/services/serpstack_service.py`## 🏗️ Project Structure---3. Run the backend:

- Verify backend is running (http://localhost:8003/docs)

- Check API quota (100/month free tier)



---```



## 📄 LicensePlaceDiscover/



MIT License - Open source├── frontend/## 📖 Usage```bash



---│   ├── index.html          # Main HTML



## 👨‍💻 Developer│   ├── styles.css          # Stylinguvicorn backend.main:app --reload



**Sri Ram Nalla**│   └── script.js           # Frontend logic



- 🔗 [GitHub](https://github.com/sriramnalla30)├── backend/1. Enter city name (e.g., "Vijayawada", "Bengaluru")```

- 💼 [LinkedIn](https://www.linkedin.com/in/sri-ram-nalla-6a2a3324b/)

- 📱 +91 9391060967│   ├── main.py            # FastAPI app



---│   ├── services/2. Enter area/locality (e.g., "Benz Circle", "Koramangala")



**Made with ❤️ by Sri Ram Nalla**│   │   └── serpstack_service.py  # API integration


│   └── requirements.txt3. Select business type (Gym, Restaurant, Hospital, etc.)### Frontend Setup

└── docs/

    └── SERPSTACK_API_GUIDE.md4. Click "Search Places"

```

5. View results with ratings, addresses, and phone numbers1. Open `frontend/index.html` in your browser

---

6. Click phone to call or "Open in Maps" for directions2. Or serve with a simple HTTP server:

## 📱 Features Details



### Smart Search

- City and area autocomplete---```bash

- 13+ business categories

- Real-time validationpython -m http.server 8000 -d frontend



### Business Display## 🏗️ Project Structure```

- Name and category

- Star ratings with review counts

- Full address

- Clickable phone numbers```## Deployment

- Action buttons (Maps, Call)

Place_Search-Gen_AI/

### UI/UX

- Dark theme with gradients├── frontend/### Backend (Railway/Render)

- Glass morphism effects

- Smooth animations│   ├── index.html          # Main HTML

- Responsive design

│   ├── styles.css          # Styling- Connect your GitHub repository

---

│   └── script.js           # Frontend logic- Set environment variables (GEMINI_API_KEY)

## 🐛 Troubleshooting

├── backend/- Deploy automatically

**Backend won't start?**

```bash│   ├── main.py            # FastAPI app

cd backend

python -m uvicorn main:app --port 8003 --reload│   ├── services/### Frontend (Netlify)

```

│   │   └── serpstack_service.py  # API integration

**No results?**

- Check API key in `backend/services/serpstack_service.py`│   └── requirements.txt- Connect your GitHub repository

- Verify backend is running (http://localhost:8003/docs)

- Check API quota (100/month free tier)└── docs/- Set publish directory to `frontend`



---    └── SERPSTACK_API_GUIDE.md- Deploy automatically



## 📄 License```````



MIT License - Open source## Environment Variables



------



## 👨‍💻 Developer- `GEMINI_API_KEY`: Your Google Gemini API key



**Sri Ram Nalla**## 🎨 Technology Stack



- 🔗 [GitHub](https://github.com/sriramnalla30)## API Endpoints

- 💼 [LinkedIn](https://www.linkedin.com/in/sri-ram-nalla-6a2a3324b/)

- 📱 +91 9391060967**Frontend**: HTML5, CSS3, Vanilla JavaScript



---**Backend**: FastAPI, Python 3.8+ - `POST /search` - Search for places



**Made with ❤️ by Sri Ram Nalla****API**: SerpStack (Real-time Google data) - `GET /health` - Health check


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
`````````
