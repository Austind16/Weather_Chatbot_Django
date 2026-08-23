document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("chat-form");
    const chatBody = document.getElementById("chat-body");
    const clearChatButton = document.getElementById("clear-chat-btn");

    if (clearChatButton) {

    clearChatButton.addEventListener("click", async function () {

        const confirmed = confirm(
            "Are you sure you want to clear your entire chat history?"
        );

        if (!confirmed) {
            return;
        }

        try {

            const csrfInput = form.querySelector(
                'input[name="csrfmiddlewaretoken"]'
            );

            const formData = new FormData();

            formData.append(
                "csrfmiddlewaretoken",
                csrfInput.value
            );

            const response = await fetch("/clear-chat/", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.message || "Failed to clear chat."
                );
            }

            // Remove all current messages
            chatBody.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">🌦️</div>
                    <h3>Welcome to WeatherChat</h3>
                    <p>
                        Ask me about the weather in any city.
                    </p>
                </div>
            `;

        // Reset weather card
        const weatherContent = document.getElementById("weather-content");

        if (weatherContent) {
            weatherContent.innerHTML = `
                <div class="weather-empty">
                    <div class="weather-empty-icon">🌤️</div>

                    <h3>No weather searched yet</h3>

                    <p>
                        Ask me about a city and its weather
                        will appear here.
                    </p>
                </div>
            `;
        }

        const input = form.elements["message"];

        if (input) {
            input.value = "";
        }

        } catch (error) {

            console.error("Clear chat error:", error);

            alert("Unable to clear the chat.");

        }

    });

}

function showTypingIndicator() {
    const row = document.createElement("div");
    row.classList.add("message-row", "bot-row");
    row.id = "typing-indicator";

    const avatar = document.createElement("div");
    avatar.classList.add("bot-avatar");
    avatar.textContent = "🌦️";

    const message = document.createElement("div");
    message.classList.add("bot-message");
    message.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    row.appendChild(avatar);
    row.appendChild(message);

    chatBody.appendChild(row);

    chatBody.scrollTop = chatBody.scrollHeight;
}


function removeTypingIndicator() {
    const indicator = document.getElementById("typing-indicator");

    if (indicator) {
        indicator.remove();
    }
}

    if (!form) {
        console.error("Chat form was not found.");
        return;
    }

    if (!chatBody) {
        console.error("Chat body was not found.");
        return;
    }

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const input = form.elements["message"];

        if (!input) {
            console.error("Message input was not found.");
            return;
        }

        const message = input.value.trim();

        if (!message) {
            return;
        }

        // Get CSRF token
        const csrfInput = form.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        );

        if (!csrfInput) {
            console.error("CSRF token was not found.");
            return;
        }

        /*
         * IMPORTANT:
         * Create FormData BEFORE clearing the input.
         */
        const formData = new FormData();

        formData.append(
            "csrfmiddlewaretoken",
            csrfInput.value
        );

        formData.append(
            "message",
            message
        );

        // Show user's message
        addMessage(message, "user-message");

        // NOW it is safe to clear the input
        input.value = "";

        // Disable button
        const button = form.querySelector("button");

        if (button) {
            button.disabled = true;
            button.textContent = "Sending...";
        }

        showTypingIndicator();

        try {

            const response = await fetch("/chat/", {
                method: "POST",

                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },

                body: formData
            });

            const data = await response.json();

            console.log("Chatbot response:", data);

            if (!response.ok) {
                throw new Error(
                    data.message || `Server returned ${response.status}`
                );
            }

            if (data.success === false) {

                addMessage(
                    data.reply || data.message || "Something went wrong.",
                    "bot-message"
                );

                return;
            }

            if (data.weather) {
                updateWeatherCard(data.weather);
            }

            addMessage(
                data.reply || "I couldn't generate a response.",
                "bot-message"
            );

        } catch (error) {

            console.error("Chat error:", error);

            addMessage(
                "Sorry, something went wrong while contacting the chatbot.",
                "bot-message"
            );

        } finally {

            removeTypingIndicator();
            if (button) {
                button.disabled = false;
                button.textContent = "Send";
            }

            input.focus();
        }
    });


    function addMessage(message, className, timestamp = null) {

        const row = document.createElement("div");
        row.classList.add("message-row");

        const messageElement = document.createElement("div");
        messageElement.classList.add(className);

        const textElement = document.createElement("div");
        textElement.classList.add("message-text");
        textElement.textContent = message;

        const timeElement = document.createElement("span");
        timeElement.classList.add("message-time");

        timeElement.textContent = timestamp || formatCurrentTime();

        messageElement.appendChild(textElement);
        messageElement.appendChild(timeElement);

        // Bot gets an avatar and left alignment
        if (className === "bot-message") {

            row.classList.add("bot-row");

            const avatar = document.createElement("div");
            avatar.classList.add("bot-avatar");
            avatar.textContent = "🌦️";

            row.appendChild(avatar);
            row.appendChild(messageElement);

        } else {

            // User goes to the right
            row.classList.add("user-row");
            row.appendChild(messageElement);

        }

        chatBody.appendChild(row);

        setTimeout(() => {
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 0);
    }
    function formatCurrentTime() {

    const now = new Date();

    return now.toLocaleString("en-IN", {
        month: "short",
        day: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true
    });
}

   
    function updateWeatherCard(weather) {

    if (!weather) {
        return;
    }

    const weatherContent = document.getElementById("weather-content");

    if (!weatherContent) {
        return;
    }

    // Create the weather card if it is currently showing
    // the "No weather searched yet" state.
    if (!document.getElementById("weather-city")) {

        weatherContent.innerHTML = `
            <div class="weather-main">

                <div class="weather-icon">
                    <img
                        id="weather-icon"
                        src="https://openweathermap.org/img/wn/${weather.icon}@2x.png"
                        alt="${weather.description}"
                    >
                </div>

                <div>
                    <h2 id="weather-city"></h2>

                    <div class="temperature">
                        <span id="weather-temperature"></span>°C
                    </div>

                    <p id="weather-description"></p>
                </div>

            </div>

            <div class="weather-stats">

                <div class="weather-stat">
                    <span class="stat-icon">🌡️</span>

                    <div>
                        <small>Feels like</small>
                        <strong id="weather-feels-like"></strong>
                    </div>
                </div>

                <div class="weather-stat">
                    <span class="stat-icon">💧</span>

                    <div>
                        <small>Humidity</small>
                        <strong id="weather-humidity"></strong>
                    </div>
                </div>

                <div class="weather-stat">
                    <span class="stat-icon">💨</span>

                    <div>
                        <small>Wind</small>
                        <strong id="weather-wind"></strong>
                    </div>
                </div>

                <div class="weather-stat">
                    <span class="stat-icon">🧭</span>

                    <div>
                        <small>Pressure</small>
                        <strong id="weather-pressure"></strong>
                    </div>
                </div>

                <div class="weather-stat">
                    <span class="stat-icon">👁️</span>

                    <div>
                        <small>Visibility</small>
                        <strong id="weather-visibility"></strong>
                    </div>
                </div>

            </div>
        `;
    }

    // Main weather information
    document.getElementById("weather-city").textContent =
        `${weather.city}, ${weather.country}`;

    document.getElementById("weather-temperature").textContent =
        weather.temperature;

    document.getElementById("weather-description").textContent =
        capitalize(weather.description);

    // Weather statistics
    document.getElementById("weather-feels-like").textContent =
        `${weather.feels_like}°C`;

    document.getElementById("weather-humidity").textContent =
        `${weather.humidity}%`;

    document.getElementById("weather-wind").textContent =
        `${weather.wind_speed} m/s`;

    document.getElementById("weather-pressure").textContent =
        `${weather.pressure} hPa`;

    document.getElementById("weather-visibility").textContent =
        formatVisibility(weather.visibility);

    // Weather icon
    const icon = document.getElementById("weather-icon");

    if (icon) {

        icon.src =
            `https://openweathermap.org/img/wn/${weather.icon}@2x.png`;

        icon.alt = weather.description;
    }
}

    function formatVisibility(meters) {

    if (!meters) {
        return "N/A";
    }

    return `${(meters / 1000).toFixed(1)} km`;
    }

    function capitalize(text) {

        if (!text) {
            return "";
        }

        return text.charAt(0).toUpperCase() + text.slice(1);
    }

    setTimeout(() => {
        chatBody.scrollTop = chatBody.scrollHeight;
        }, 0);

});