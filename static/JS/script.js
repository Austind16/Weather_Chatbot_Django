document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("chat-form");
    const chatBody = document.getElementById("chat-body");

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

            if (button) {
                button.disabled = false;
                button.textContent = "Send";
            }

            input.focus();
        }
    });


    function addMessage(message, className) {

        const messageElement = document.createElement("div");

        messageElement.classList.add(className);

        messageElement.textContent = message;

        chatBody.appendChild(messageElement);

        chatBody.scrollTop = chatBody.scrollHeight;
    }

});