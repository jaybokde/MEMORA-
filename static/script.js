async function saveThought() {

    const input = document.getElementById("thought");
    const status = document.getElementById("status");

    const text = input.value.trim();

    if (!text) {
        status.textContent = "Please enter something.";
        return;
    }

    status.textContent = "MEMORA is thinking...";

    try {

        const response = await fetch("/api/capture", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        status.textContent = data.message;
        input.value = "";

    } catch (error) {

        console.error(error);status.textContent = data.message;

        status.textContent =
            "Error: " + error.message;
    }
}


async function loadMemory() {

    try {

        const response = await fetch("/api/memory");

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        displayItems("tasks", data.tasks);
        displayItems("events", data.events);
        displayItems("memories", data.memories);

    } catch (error) {

        console.error(error);

    }
}


function displayItems(elementId, items) {

    const container = document.getElementById(elementId);

    if (!container) {
        return;
    }

    if (items.length === 0) {

        container.innerHTML =
            "<p>Nothing here yet.</p>";

        return;
    }

    container.innerHTML = "";

    items.forEach(item => {

        const div = document.createElement("div");

        div.className = "memory-item";

        div.textContent =
            item.title ||
            item.content ||
            "No information";

        container.appendChild(div);

    });
}


if (window.location.pathname === "/memory") {

    loadMemory();

}