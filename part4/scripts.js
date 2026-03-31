const API_BASE_URL = "http://127.0.0.1:5000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", handleLoginSubmit);
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

function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}
