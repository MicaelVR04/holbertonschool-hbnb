const API_BASE_URL = "http://127.0.0.1:5000/api/v1";
let allPlaces = [];

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const priceFilter = document.getElementById("price-filter");

    if (loginForm) {
        loginForm.addEventListener("submit", handleLoginSubmit);
    }

    if (priceFilter) {
        checkAuthentication();
        fetchPlaces();
        priceFilter.addEventListener("change", handlePriceFilter);
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
        return;
    }

    if (token) {
        loginLink.style.display = "none";
    } else {
        loginLink.style.display = "inline-flex";
    }
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
