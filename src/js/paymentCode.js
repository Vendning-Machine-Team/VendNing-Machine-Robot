const reportButton = document.getElementById('reportButton');
const homeButton = document.getElementById('homeButton');

homeButton.addEventListener("click", () => {
    window.location.replace("../index.html");
});

reportButton.addEventListener("click", () => {
    window.location.replace("./reportIssue.html");
});



async function loadCode() {

    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get("session_id");

    if (!sessionId) return;

    const response = await fetch(`/api/get-code?session_id=${sessionId}`);
    const data = await response.json();

    if (data.code) {
        document.getElementById("codeDisplay").innerText = data.code;
    } else {
        document.getElementById("codeDisplay").innerText = "Code unavailable";
    }
}

loadCode();