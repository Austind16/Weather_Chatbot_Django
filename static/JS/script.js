document.addEventListener("DOMContentLoaded", function () {

    /* =========================================
       CHAT ELEMENTS
    ========================================= */

    const form = document.getElementById("chat-form");
    const chatBody = document.getElementById("chat-body");
    const clearChatButton = document.getElementById("clear-chat-btn");


    /*
     * script.js is loaded globally through base.html.
     *
     * Login/Register pages don't have the chatbot.
     * Therefore, simply stop here if we're not on
     * the chatbot page.
     */
    if (!form || !chatBody) {
        return;
    }


    /* =========================================
       CLEAR CHAT
    ========================================= */

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

                if (!csrfInput) {
                    console.error("CSRF token was not found.");
                    return;
                }


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


                /* ---------------------------------
                   Reset chat messages
                --------------------------------- */

                chatBody.innerHTML = `
                    <div class="welcome-message">

                        <div class="welcome-icon">
                            🌦️
                        </div>

                        <h3>
                            Welcome to WeatherChat
                        </h3>

                        <p>
                            Ask me about the weather in any city.
                        </p>

                    </div>
                `;


                /* ---------------------------------
                   Reset weather card
                --------------------------------- */

                const weatherContent =
                    document.getElementById("weather-content");


                if (weatherContent) {

                    weatherContent.innerHTML = `
                        <div class="weather-empty">

                            <div class="weather-empty-icon">
                                🌤️
                            </div>

                            <h3>
                                No weather searched yet
                            </h3>

                            <p>
                                Ask me about a city and its weather
                                will appear here.
                            </p>

                        </div>
                    `;
                }


                /* ---------------------------------
                   Clear input
                --------------------------------- */

                const input = form.elements["message"];

                if (input) {
                    input.value = "";
                    input.focus();
                }


            } catch (error) {

                console.error(
                    "Clear chat error:",
                    error
                );

                alert("Unable to clear the chat.");
            }

        });

    }


    /* =========================================
       TYPING INDICATOR
    ========================================= */

    function showTypingIndicator() {

        const row = document.createElement("div");

        row.classList.add(
            "message-row",
            "bot-row"
        );

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


        scrollToBottom();
    }


    function removeTypingIndicator() {

        const indicator =
            document.getElementById("typing-indicator");


        if (indicator) {
            indicator.remove();
        }
    }


    /* =========================================
       CHAT FORM
    ========================================= */

    form.addEventListener("submit", async function (e) {

        e.preventDefault();


        const input = form.elements["message"];


        if (!input) {

            console.error(
                "Message input was not found."
            );

            return;
        }


        const message = input.value.trim();


        if (!message) {
            return;
        }


        /* ---------------------------------
           CSRF
        --------------------------------- */

        const csrfInput = form.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        );


        if (!csrfInput) {

            console.error(
                "CSRF token was not found."
            );

            return;
        }


        /* ---------------------------------
           Create FormData BEFORE clearing
           the input
        --------------------------------- */

        const formData = new FormData();


        formData.append(
            "csrfmiddlewaretoken",
            csrfInput.value
        );


        formData.append(
            "message",
            message
        );


        /* ---------------------------------
           Show user message immediately
        --------------------------------- */

        addMessage(
            message,
            "user-message"
        );


        input.value = "";


        /* ---------------------------------
           Disable send button
        --------------------------------- */

        const button =
            form.querySelector("button");


        if (button) {

            button.disabled = true;

            button.textContent = "Sending...";
        }


        /* ---------------------------------
           Show typing indicator
        --------------------------------- */

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


            console.log(
                "Chatbot response:",
                data
            );


            if (!response.ok) {

                throw new Error(
                    data.message ||
                    `Server returned ${response.status}`
                );
            }


            /* ---------------------------------
               Server reported failure
            --------------------------------- */

            if (data.success === false) {

                addMessage(
                    data.reply ||
                    data.message ||
                    "Something went wrong.",

                    "bot-message"
                );

                return;
            }


            /* ---------------------------------
               Update weather card
            --------------------------------- */

            if (data.weather) {

                updateWeatherCard(
                    data.weather
                );
            }


            /* ---------------------------------
               Add bot response
            --------------------------------- */

            addMessage(
                data.reply ||
                "I couldn't generate a response.",

                "bot-message"
            );


        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


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


    /* =========================================
       ADD MESSAGE
    ========================================= */

    function addMessage(
        message,
        className,
        timestamp = null
    ) {

        const row =
            document.createElement("div");


        row.classList.add(
            "message-row"
        );


        const messageElement =
            document.createElement("div");


        messageElement.classList.add(
            className
        );


        const textElement =
            document.createElement("div");


        textElement.classList.add(
            "message-text"
        );


        textElement.textContent =
            message;


        const timeElement =
            document.createElement("span");


        timeElement.classList.add(
            "message-time"
        );


        timeElement.textContent =
            timestamp ||
            formatCurrentTime();


        messageElement.appendChild(
            textElement
        );


        messageElement.appendChild(
            timeElement
        );


        /* ---------------------------------
           Bot message
        --------------------------------- */

        if (className === "bot-message") {

            row.classList.add(
                "bot-row"
            );


            const avatar =
                document.createElement("div");


            avatar.classList.add(
                "bot-avatar"
            );


            avatar.textContent = "🌦️";


            row.appendChild(avatar);

            row.appendChild(
                messageElement
            );

        }


        /* ---------------------------------
           User message
        --------------------------------- */

        else {

            row.classList.add(
                "user-row"
            );


            row.appendChild(
                messageElement
            );
        }


        chatBody.appendChild(
            row
        );


        scrollToBottom();
    }


    /* =========================================
       CURRENT TIMESTAMP
    ========================================= */

    function formatCurrentTime() {

        const now = new Date();


        return now.toLocaleString(
            "en-IN",
            {
                month: "short",
                day: "2-digit",
                year: "numeric",

                hour: "2-digit",
                minute: "2-digit",

                hour12: true
            }
        );
    }


    /* =========================================
       AUTO SCROLL
    ========================================= */

    function scrollToBottom() {

        setTimeout(function () {

            chatBody.scrollTop =
                chatBody.scrollHeight;

        }, 0);
    }


    /* =========================================
       WEATHER CARD
    ========================================= */

    function updateWeatherCard(weather) {

        if (!weather) {
            return;
        }


        const weatherContent =
            document.getElementById(
                "weather-content"
            );


        if (!weatherContent) {
            return;
        }


        /* ---------------------------------
           Create weather card if necessary
        --------------------------------- */

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

                            <span
                                id="weather-temperature"
                            ></span>°C

                        </div>


                        <p id="weather-description"></p>

                    </div>

                </div>


                <div class="weather-stats">


                    <div class="weather-stat">

                        <span class="stat-icon">
                            🌡️
                        </span>

                        <div>

                            <small>
                                Feels like
                            </small>

                            <strong
                                id="weather-feels-like"
                            ></strong>

                        </div>

                    </div>


                    <div class="weather-stat">

                        <span class="stat-icon">
                            💧
                        </span>

                        <div>

                            <small>
                                Humidity
                            </small>

                            <strong
                                id="weather-humidity"
                            ></strong>

                        </div>

                    </div>


                    <div class="weather-stat">

                        <span class="stat-icon">
                            💨
                        </span>

                        <div>

                            <small>
                                Wind
                            </small>

                            <strong
                                id="weather-wind"
                            ></strong>

                        </div>

                    </div>


                    <div class="weather-stat">

                        <span class="stat-icon">
                            🧭
                        </span>

                        <div>

                            <small>
                                Pressure
                            </small>

                            <strong
                                id="weather-pressure"
                            ></strong>

                        </div>

                    </div>


                    <div class="weather-stat">

                        <span class="stat-icon">
                            👁️
                        </span>

                        <div>

                            <small>
                                Visibility
                            </small>

                            <strong
                                id="weather-visibility"
                            ></strong>

                        </div>

                    </div>


                </div>
            `;
        }


        /* ---------------------------------
           Main weather information
        --------------------------------- */

        const city =
            document.getElementById(
                "weather-city"
            );


        if (city) {

            city.textContent =
                `${weather.city}, ${weather.country}`;
        }


        const temperature =
            document.getElementById(
                "weather-temperature"
            );


        if (temperature) {

            temperature.textContent =
                weather.temperature;
        }


        const description =
            document.getElementById(
                "weather-description"
            );


        if (description) {

            description.textContent =
                capitalize(
                    weather.description
                );
        }


        /* ---------------------------------
           Weather statistics
        --------------------------------- */

        const feelsLike =
            document.getElementById(
                "weather-feels-like"
            );


        if (feelsLike) {

            feelsLike.textContent =
                `${weather.feels_like}°C`;
        }


        const humidity =
            document.getElementById(
                "weather-humidity"
            );


        if (humidity) {

            humidity.textContent =
                `${weather.humidity}%`;
        }


        const wind =
            document.getElementById(
                "weather-wind"
            );


        if (wind) {

            wind.textContent =
                `${weather.wind_speed} m/s`;
        }


        const pressure =
            document.getElementById(
                "weather-pressure"
            );


        if (pressure) {

            pressure.textContent =
                `${weather.pressure} hPa`;
        }


        const visibility =
            document.getElementById(
                "weather-visibility"
            );


        if (visibility) {

            visibility.textContent =
                formatVisibility(
                    weather.visibility
                );
        }


        /* ---------------------------------
           Weather icon
        --------------------------------- */

        const icon =
            document.getElementById(
                "weather-icon"
            );


        if (icon) {

            icon.src =
                `https://openweathermap.org/img/wn/${weather.icon}@2x.png`;

            icon.alt =
                weather.description;
        }

    }


    /* =========================================
       VISIBILITY
    ========================================= */

    function formatVisibility(meters) {

        if (!meters) {
            return "N/A";
        }


        return `${(meters / 1000).toFixed(1)} km`;
    }


    /* =========================================
       CAPITALIZE
    ========================================= */

    function capitalize(text) {

        if (!text) {
            return "";
        }


        return (
            text.charAt(0).toUpperCase() +
            text.slice(1)
        );
    }


    /* =========================================
       INITIAL SCROLL
    ========================================= */

    scrollToBottom();

});