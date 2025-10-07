// Configuration - Connected to Production Backend
// Backend deployed on Render: https://place-search-gen-ai.onrender.com
const API_BASE_URL = "https://place-search-gen-ai.onrender.com";

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

  // Create Google Maps search for the specific place
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
  searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting Suggestions...';
}

function hideLoading() {
  loading.style.display = "none";
  searchBtn.disabled = false;
  searchBtn.innerHTML = '<i class="fas fa-search"></i> Get Suggestions';
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

// Enhanced Auto-complete with expanded city and area data
const popularCities = [
  "Agra",
  "Ahmedabad",
  "Ajmer",
  "Amritsar",
  "Aurangabad",
  "Bengaluru",
  "Bhopal",
  "Bhubaneswar",
  "Chandigarh",
  "Chennai",
  "Coimbatore",
  "Cuttack",
  "Dehradun",
  "Delhi",
  "Faridabad",
  "Ghaziabad",
  "Goa",
  "Gurgaon",
  "Guwahati",
  "Hyderabad",
  "Indore",
  "Jaipur",
  "Jalandhar",
  "Jammu",
  "Jodhpur",
  "Kanpur",
  "Kochi",
  "Kolkata",
  "Lucknow",
  "Ludhiana",
  "Madurai",
  "Mangalore",
  "Mumbai",
  "Mysore",
  "Nagpur",
  "Nashik",
  "Noida",
  "Patna",
  "Pune",
  "Raipur",
  "Rajkot",
  "Ranchi",
  "Salem",
  "Surat",
  "Thiruvananthapuram",
  "Thrissur",
  "Tirupati",
  "Udaipur",
  "Vadodara",
  "Varanasi",
  "Vijayawada",
  "Visakhapatnam",
  "Warangal",
];

const popularAreas = {
  bengaluru: [
    "Koramangala",
    "Indiranagar",
    "Whitefield",
    "Electronic City",
    "Marathahalli",
    "HSR Layout",
    "BTM Layout",
    "Jayanagar",
    "Rajajinagar",
    "Malleswaram",
  ],
  mumbai: [
    "Bandra",
    "Andheri",
    "Powai",
    "Lower Parel",
    "Worli",
    "Juhu",
    "Colaba",
    "Fort",
    "Dadar",
    "Thane",
  ],
  delhi: [
    "Connaught Place",
    "Karol Bagh",
    "Lajpat Nagar",
    "Saket",
    "Dwarka",
    "Rohini",
    "Vasant Kunj",
    "Greater Kailash",
    "Nehru Place",
    "Chandni Chowk",
  ],
  chennai: [
    "T Nagar",
    "Anna Nagar",
    "Velachery",
    "Adyar",
    "Tambaram",
    "Mylapore",
    "Nungambakkam",
    "Guindy",
    "OMR",
    "ECR",
  ],
  hyderabad: [
    "Banjara Hills",
    "Jubilee Hills",
    "Gachibowli",
    "Kondapur",
    "Madhapur",
    "Hitech City",
    "Secunderabad",
    "Begumpet",
    "Ameerpet",
    "Kukatpally",
  ],
  pune: [
    "Koregaon Park",
    "Hinjewadi",
    "Baner",
    "Wakad",
    "Viman Nagar",
    "Kothrud",
    "Shivaji Nagar",
    "Camp",
    "Magarpatta",
    "Hadapsar",
  ],
  kolkata: [
    "Salt Lake",
    "Park Street",
    "Ballygunge",
    "New Town",
    "Howrah",
    "Esplanade",
    "Gariahat",
    "Dumdum",
    "Jadavpur",
    "Tollygunge",
  ],
  ahmedabad: [
    "Satellite",
    "Vastrapur",
    "Bopal",
    "Prahlad Nagar",
    "CG Road",
    "Navrangpura",
    "Maninagar",
    "Iscon",
    "SG Highway",
    "Ashram Road",
  ],
  jaipur: [
    "Malviya Nagar",
    "Vaishali Nagar",
    "Mansarovar",
    "C Scheme",
    "Tonk Road",
    "MI Road",
    "Jagatpura",
    "Sodala",
    "Civil Lines",
    "Raja Park",
  ],
  surat: [
    "Adajan",
    "Vesu",
    "Pal",
    "Athwa",
    "Magdalla",
    "Piplod",
    "Citylight",
    "Rander",
    "Katargam",
    "Udhna",
  ],
  vijayawada: [
    "Benz Circle",
    "Auto Nagar",
    "Governorpet",
    "Labbipet",
    "Patamata",
    "Tadepalli",
    "Gunadala",
    "Krishna Lanka",
    "Ring Road",
    "PVP Square",
  ],
  visakhapatnam: [
    "MVP Colony",
    "Dwaraka Nagar",
    "Gajuwaka",
    "Madhurawada",
    "Rushikonda",
    "Beach Road",
    "Siripuram",
    "PM Palem",
    "Kommadi",
    "Pendurthi",
  ],
};

// Get DOM elements for dropdowns
const cityDropdown = document.getElementById("cityDropdown");
const areaDropdown = document.getElementById("areaDropdown");

// City autocomplete functionality
cityInput.addEventListener("input", function () {
  const value = this.value.toLowerCase().trim();

  if (value.length === 0) {
    hideCityDropdown();
    return;
  }

  const filteredCities = popularCities.filter((city) =>
    city.toLowerCase().startsWith(value)
  );

  showCityDropdown(filteredCities, value);

  // Clear area suggestions when city changes
  areaInput.value = "";
  hideAreaDropdown();
});

// Area autocomplete functionality
areaInput.addEventListener("input", function () {
  const value = this.value.toLowerCase().trim();
  const selectedCity = cityInput.value.toLowerCase().trim();

  if (value.length === 0) {
    hideAreaDropdown();
    return;
  }

  const cityAreas = popularAreas[selectedCity] || [];
  const filteredAreas = cityAreas.filter((area) =>
    area.toLowerCase().startsWith(value)
  );

  showAreaDropdown(filteredAreas, value);
});

// Show city dropdown
function showCityDropdown(cities, searchValue) {
  cityDropdown.innerHTML = "";
  cityDropdown.style.display = "block";

  if (cities.length === 0) {
    const noResults = document.createElement("div");
    noResults.className = "autocomplete-item no-results";
    noResults.textContent = "No cities found";
    cityDropdown.appendChild(noResults);
    return;
  }

  cities.slice(0, 8).forEach((city) => {
    // Limit to 8 suggestions
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    item.textContent = city;

    item.addEventListener("click", function () {
      cityInput.value = city;
      hideCityDropdown();
      cityInput.focus();

      // Update area suggestions for selected city
      updateAreaSuggestions(city.toLowerCase());
    });

    cityDropdown.appendChild(item);
  });
}

// Show area dropdown
function showAreaDropdown(areas, searchValue) {
  areaDropdown.innerHTML = "";
  areaDropdown.style.display = "block";

  if (areas.length === 0) {
    const noResults = document.createElement("div");
    noResults.className = "autocomplete-item no-results";
    noResults.textContent = "No areas found for this city";
    areaDropdown.appendChild(noResults);
    return;
  }

  areas.slice(0, 8).forEach((area) => {
    // Limit to 8 suggestions
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    item.textContent = area;

    item.addEventListener("click", function () {
      areaInput.value = area;
      hideAreaDropdown();
      areaInput.focus();
    });

    areaDropdown.appendChild(item);
  });
}

// Hide dropdowns
function hideCityDropdown() {
  cityDropdown.style.display = "none";
}

function hideAreaDropdown() {
  areaDropdown.style.display = "none";
}

// Update area suggestions when city is selected
function updateAreaSuggestions(city) {
  const areas = popularAreas[city];
  if (areas) {
    // Show placeholder in area input
    areaInput.placeholder = `e.g., ${areas[0]}`;
  }
}

// Hide dropdowns when clicking outside
document.addEventListener("click", function (e) {
  if (!cityInput.contains(e.target) && !cityDropdown.contains(e.target)) {
    hideCityDropdown();
  }
  if (!areaInput.contains(e.target) && !areaDropdown.contains(e.target)) {
    hideAreaDropdown();
  }
});

// Keyboard navigation for dropdowns
cityInput.addEventListener("keydown", handleCityKeyboard);
areaInput.addEventListener("keydown", handleAreaKeyboard);

function handleCityKeyboard(e) {
  const items = cityDropdown.querySelectorAll(
    ".autocomplete-item:not(.no-results)"
  );
  const highlighted = cityDropdown.querySelector(
    ".autocomplete-item.highlighted"
  );

  if (e.key === "ArrowDown") {
    e.preventDefault();
    const next = highlighted ? highlighted.nextElementSibling : items[0];
    if (next && !next.classList.contains("no-results")) {
      if (highlighted) highlighted.classList.remove("highlighted");
      next.classList.add("highlighted");
    }
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    const prev = highlighted
      ? highlighted.previousElementSibling
      : items[items.length - 1];
    if (prev && !prev.classList.contains("no-results")) {
      if (highlighted) highlighted.classList.remove("highlighted");
      prev.classList.add("highlighted");
    }
  } else if (e.key === "Enter") {
    e.preventDefault();
    if (highlighted) {
      highlighted.click();
    }
  } else if (e.key === "Escape") {
    hideCityDropdown();
  }
}

function handleAreaKeyboard(e) {
  const items = areaDropdown.querySelectorAll(
    ".autocomplete-item:not(.no-results)"
  );
  const highlighted = areaDropdown.querySelector(
    ".autocomplete-item.highlighted"
  );

  if (e.key === "ArrowDown") {
    e.preventDefault();
    const next = highlighted ? highlighted.nextElementSibling : items[0];
    if (next && !next.classList.contains("no-results")) {
      if (highlighted) highlighted.classList.remove("highlighted");
      next.classList.add("highlighted");
    }
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    const prev = highlighted
      ? highlighted.previousElementSibling
      : items[items.length - 1];
    if (prev && !prev.classList.contains("no-results")) {
      if (highlighted) highlighted.classList.remove("highlighted");
      prev.classList.add("highlighted");
    }
  } else if (e.key === "Enter") {
    e.preventDefault();
    if (highlighted) {
      highlighted.click();
    }
  } else if (e.key === "Escape") {
    hideAreaDropdown();
  }
}

// Initialize the app
document.addEventListener("DOMContentLoaded", function () {
  console.log("Place Search App initialized");

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
