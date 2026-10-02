async function sendChatMessage() {

    const input = document.getElementById("chat-input");
    const message = input.value.trim();

    if (message === "") {
        return;
    }

    const chatBox = document.getElementById("chat-box");

    const userDiv = document.createElement("div");
    userDiv.className = "chat-message user-message";
    userDiv.textContent = message;
    chatBox.appendChild(userDiv);

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingDiv = document.createElement("div");
    loadingDiv.className = "chat-message bot-message";
    loadingDiv.textContent = "লিখছে...";
    chatBox.appendChild(loadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/ai_chat_api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (data.status === "success") {
            loadingDiv.textContent = data.reply;
        } else {
            loadingDiv.textContent = data.message || "একটা সমস্যা হয়েছে।";
        }

    } catch (error) {
        loadingDiv.textContent = "সার্ভারের সাথে সংযোগ করা যাচ্ছে না।";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("chat-input");
    input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendChatMessage();
        }
    });
});
