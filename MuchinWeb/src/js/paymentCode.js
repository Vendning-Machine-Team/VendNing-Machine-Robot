const reportButton = document.getElementById('reportButton');
const homeButton = document.getElementById('homeButton');

homeButton.addEventListener("click", () => {
    window.location.replace("/public/pages/index.html");
});

reportButton.addEventListener("click", () => {
    window.location.replace("/public/pages/reportIssue.html");
});