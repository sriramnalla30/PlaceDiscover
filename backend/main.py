from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from backend.services.gemini_service import GeminiService
from backend.models.place import Place, SearchRequest

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Place Search API",
    description="Search for places using Generative AI",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini service
gemini_service = GeminiService()

@app.get("/")
async def root():
    return {"message": "AI Place Search API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Place Search API"}

@app.post("/search", response_model=dict)
async def search_places(request: SearchRequest):
    """
    Search for places using Gemini AI
    """
    try:
        # Validate input
        if not request.city or not request.area or not request.type:
            raise HTTPException(status_code=400, detail="City, area, and type are required")
        
        # Search using Gemini AI
        places = await gemini_service.search_places(
            city=request.city,
            area=request.area,
            place_type=request.type
        )
        
        return {
            "success": True,
            "query": f"{request.type} in {request.area}, {request.city}",
            "places": places,
            "count": len(places)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/types")
async def get_place_types():
    """
    Get available place types
    """
    return {
        "types": [
            "cafe", "restaurant", "hospital", "hotel", "hostel",
            "mens_pg", "womens_pg", "paying_guest",
            "gym", "pharmacy", "bank", "atm", "gas_station"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)