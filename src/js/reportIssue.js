document.addEventListener("DOMContentLoaded", () => {
    const submitButton = document.getElementById("submitButton");
    const issueTextArea = document.getElementById("issue");
    const responseMessage = document.getElementById("response"); // optional display area

    submitButton.addEventListener("click", async (event) => {
        event.preventDefault(); // Prevent page reload

        const issueText = issueTextArea.value.trim();

        if (!issueText) {
            alert("Please enter an issue before submitting.");
            return;
        }

        try {
            const res = await fetch("/api/message", {
                method: "POST",
                credentials: "include", // important if using sessions
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: issueText
                })
            });

            if (!res.ok) {
                throw new Error("Server error");
            }

            const data = await res.json();

            // Show backend response
            if (responseMessage) {
                responseMessage.innerText = data.reply;
            } else {
                alert("Server says: " + data.reply);
            }

            issueTextArea.value = ""; // Clear textarea

        } catch (error) {
            console.error("Error submitting issue:", error);
            alert("Something went wrong while submitting the issue.");
        }
    });
});