const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

function addMessage(content, className) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", className);
    messageElement.innerHTML = content;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageElement;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(`<p>${text}</p>`, "user-message");
    userInput.value = "";
    sendButton.disabled = true;

    const botBubble = addMessage(`<p>...</p>`, "bot-message");
    let botMessage = "";

    try {
        const response = await fetch("/chat/rag/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: text }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Network error: ${response.status} ${errorText}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        botBubble.innerHTML = `<p></p>`;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            
            if (chunk.includes("[DONE]")) {
                break;
            }

            botMessage += chunk;
            botBubble.innerHTML = `<p>${botMessage}</p>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

    } catch (err) {
        botBubble.innerHTML = `<p class="error">⚠️ Error: Could not get a response from the server. Please try again later.</p>`;
        console.error(err);
    } finally {
        sendButton.disabled = false;
        userInput.focus();
    }
}

sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault(); 
        sendMessage();
    }
});