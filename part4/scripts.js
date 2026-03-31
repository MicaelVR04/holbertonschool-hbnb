const API_BASE_URL = "http://127.0.0.1:5000/api/v1";
let allPlaces = [];

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const priceFilter = document.getElementById("price-filter");
    const placeDetailsSection = document.getElementById("place-details");

    if (loginForm) {
        loginForm.addEventListener("submit", handleLoginSubmit);
    }

    if (priceFilter) {
        checkAuthentication();
        fetchPlaces();
        priceFilter.addEventListener("change", handlePriceFilter);
    }

    if (placeDetailsSection) {
        loadPlacePage();
    }
});

async function handleLoginSubmit(event) {
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            const message = data.error || data.message || "Login failed";
            alert(message);
            return;
        }

        setCookie("token", data.access_token, 1);
        window.location.href = "index.html";
    } catch (error) {
        console.error("Login error:", error);
        alert("Unable to connect to the server. Please try again.");
    }
}

function checkAuthentication() {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");

    if (!loginLink) {
        return token;
    }

    if (token) {
        loginLink.style.display = "none";
    } else {
        loginLink.style.display = "inline-flex";
    }

    return token;
}

async function fetchPlaces() {
    const token = getCookie("token");
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: "GET",
            headers
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch places: ${response.status}`);
        }

        const places = await response.json();
        allPlaces = places;
        displayPlaces(allPlaces);
    } catch (error) {
        console.error("Fetch places error:", error);
        displayPlaces([]);
        alert("Unable to load places right now.");
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById("places-list");
    if (!placesList) {
        return;
    }

    placesList.innerHTML = "";

    if (!places.length) {
        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "No places available.";
        placesList.appendChild(emptyMessage);
        return;
    }

    places.forEach((place) => {
        const placeCard = document.createElement("article");
        placeCard.className = "place-card";
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p class="place-price">$${Number(place.price).toFixed(2)} / night</p>
            <p class="place-location">${place.description || "No description available"}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

function handlePriceFilter(event) {
    const selectedValue = event.target.value;

    if (!selectedValue) {
        displayPlaces(allPlaces);
        return;
    }

    const maxPrice = Number(selectedValue);
    const filteredPlaces = allPlaces.filter((place) => Number(place.price) <= maxPrice);
    displayPlaces(filteredPlaces);
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function loadPlacePage() {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById("add-review");

    if (!placeId) {
        displayPlaceError("No place ID was provided in the URL.");
        return;
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? "flex" : "none";
        const reviewLink = addReviewSection.querySelector("a");
        if (reviewLink) {
            reviewLink.href = `add_review.html?id=${placeId}`;
        }
    }

    await fetchPlaceDetails(placeId, token);
}

async function fetchPlaceDetails(placeId, token) {
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: "GET",
            headers
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch place details: ${response.status}`);
        }

        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error("Fetch place details error:", error);
        displayPlaceError("Unable to load place details right now.");
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById("place-details");
    const reviewsSection = document.getElementById("reviews");

    if (!placeDetailsSection || !reviewsSection) {
        return;
    }

    const amenities = Array.isArray(place.amenities) ? place.amenities : [];
    const reviews = Array.isArray(place.reviews) ? place.reviews : [];

    placeDetailsSection.innerHTML = `
        <div class="place-heading">
            <h1>${place.title}</h1>
            <p class="place-price">$${Number(place.price).toFixed(2)} / night</p>
        </div>

        <div class="place-info-grid">
            <div class="place-info">
                <h2>Host</h2>
                <p>${place.owner_id || "Host information unavailable"}</p>
            </div>

            <div class="place-info">
                <h2>Description</h2>
                <p>${place.description || "No description available."}</p>
            </div>

            <div class="place-info">
                <h2>Location</h2>
                <p>Latitude: ${place.latitude} | Longitude: ${place.longitude}</p>
            </div>

            <div class="place-info">
                <h2>Amenities</h2>
                <ul class="amenities-list">
                    ${
                        amenities.length
                            ? amenities.map((amenity) => `<li>${typeof amenity === "string" ? amenity : amenity.name}</li>`).join("")
                            : "<li>No amenities listed.</li>"
                    }
                </ul>
            </div>
        </div>
    `;

    reviewsSection.innerHTML = "<h2>Reviews</h2>";

    if (!reviews.length) {
        reviewsSection.innerHTML += "<p>No reviews yet.</p>";
        return;
    }

    reviews.forEach((review) => {
        const reviewCard = document.createElement("article");
        reviewCard.className = "review-card";
        reviewCard.innerHTML = `
            <h3>${review.user_id || "Guest"}</h3>
            <p class="review-rating">Rating: ${review.rating}/5</p>
            <p>${review.text}</p>
        `;
        reviewsSection.appendChild(reviewCard);
    });
}

function displayPlaceError(message) {
    const placeDetailsSection = document.getElementById("place-details");
    const reviewsSection = document.getElementById("reviews");

    if (placeDetailsSection) {
        placeDetailsSection.innerHTML = `<p>${message}</p>`;
    }

    if (reviewsSection) {
        reviewsSection.innerHTML = "";
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim();
        if (trimmedCookie.startsWith(`${name}=`)) {
            return trimmedCookie.substring(name.length + 1);
        }
    }

    return null;
}

function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}
