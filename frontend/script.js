// Configuration
const API_BASE_URL = "http://localhost:8000"; // Change this to your deployed backend URL

// DOM Elements
const cityInput = document.getElementById("city");
const areaInput = document.getElementById("area");
const typeSelect = document.getElementById("type");
const searchBtn = document.getElementById("searchBtn");
const loading = document.getElementById("loading");
const results = document.getElementById("results");
const resultsContainer = document.getElementById("resultsContainer");
const error = document.getElementById("error");
const errorText = document.getElementById("errorText");

// Event Listeners
searchBtn.addEventListener("click", handleSearch);

// Allow Enter key to trigger search
[cityInput, areaInput, typeSelect].forEach((element) => {
  element.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  });
});

// Main search function
async function handleSearch() {
  const city = cityInput.value.trim();
  const area = areaInput.value.trim();
  const type = typeSelect.value;

  // Validation
  if (!city || !area || !type) {
    showError("Please fill in all fields");
    return;
  }

  // Show loading state
  showLoading();
  hideError();
  hideResults();

  try {
    const response = await fetch(`${API_BASE_URL}/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        city: city,
        area: area,
        type: type,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    hideLoading();

    if (data.places && data.places.length > 0) {
      displayResults(data.places);
    } else {
      showError("No places found for your search criteria");
    }
  } catch (err) {
    hideLoading();
    console.error("Search error:", err);
    showError("Failed to search places. Please try again.");
  }
}

// Display search results
function displayResults(places) {
  resultsContainer.innerHTML = "";

  places.forEach((place) => {
    const placeCard = createPlaceCard(place);
    resultsContainer.appendChild(placeCard);
  });

  results.style.display = "block";
}

// Create individual place card
function createPlaceCard(place) {
  const card = document.createElement("div");
  card.className = "place-card";

  const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
    place.name + " " + place.address
  )}`;
  const phoneUrl = place.phone ? `tel:${place.phone}` : null;

  card.innerHTML = `
        <div class="place-header">
            <div>
                <div class="place-name">${place.name}</div>
                <div class="place-type">${place.type || typeSelect.value}</div>
            </div>
        </div>
        <div class="place-address">
            <i class="fas fa-map-marker-alt"></i> ${place.address}
        </div>
        ${
          place.phone
            ? `
            <div class="place-phone">
                <i class="fas fa-phone"></i> ${place.phone}
            </div>
        `
            : ""
        }
        <div class="place-actions">
            <a href="${mapsUrl}" target="_blank" class="action-btn maps-btn">
                <i class="fas fa-map"></i> View on Maps
            </a>
            ${
              phoneUrl
                ? `
                <a href="${phoneUrl}" class="action-btn phone-btn">
                    <i class="fas fa-phone"></i> Call Now
                </a>
            `
                : ""
            }
        </div>
    `;

  return card;
}

// UI Helper Functions
function showLoading() {
  loading.style.display = "block";
  searchBtn.disabled = true;
  searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
}

function hideLoading() {
  loading.style.display = "none";
  searchBtn.disabled = false;
  searchBtn.innerHTML = '<i class="fas fa-search"></i> Search Places';
}

function showError(message) {
  errorText.textContent = message;
  error.style.display = "block";
}

function hideError() {
  error.style.display = "none";
}

function hideResults() {
  results.style.display = "none";
}

// Auto-complete suggestions (basic implementation)
const popularCities = [
  "Bengaluru",
  "Mumbai",
  "Delhi",
  "Chennai",
  "Hyderabad",
  "Pune",
  "Kolkata",
  "Ahmedabad",
  "Jaipur",
  "Surat",
];

const popularAreas = {
  bengaluru: [
    "Koramangala",
    "Indiranagar",
    "Whitefield",
    "Electronic City",
    "Marathahalli",
  ],
  mumbai: ["Bandra", "Andheri", "Powai", "Lower Parel", "Worli"],
  delhi: ["Connaught Place", "Karol Bagh", "Lajpat Nagar", "Saket", "Dwarka"],
  chennai: ["T Nagar", "Anna Nagar", "Velachery", "Adyar", "Tambaram"],
  hyderabad: [
    "Banjara Hills",
    "Jubilee Hills",
    "Gachibowli",
    "Kondapur",
    "Madhapur",
  ],
};

// Simple autocomplete for city
cityInput.addEventListener("input", function () {
  const value = this.value.toLowerCase();
  // You can implement a dropdown with suggestions here
  console.log("City suggestions for:", value);
});

// Update area suggestions based on city
cityInput.addEventListener("blur", function () {
  const city = this.value.toLowerCase();
  if (popularAreas[city]) {
    // You can update area suggestions here
    console.log("Area suggestions for", city, ":", popularAreas[city]);
  }
});

// Initialize the app
document.addEventListener("DOMContentLoaded", function () {
  console.log("AI Place Search App initialized");

  // Focus on city input
  cityInput.focus();

  // Test backend connection
  testBackendConnection();
});

// Test backend connection
async function testBackendConnection() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (response.ok) {
      console.log("Backend connection successful");
    } else {
      console.warn("Backend connection failed");
    }
  } catch (error) {
    console.warn("Backend not available:", error.message);
  }
}
