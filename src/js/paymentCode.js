const reportButton = document.getElementById('reportButton');
const homeButton = document.getElementById('homeButton');

homeButton.addEventListener("click", () => {
    window.location.replace("/pages/index.html");
});

reportButton.addEventListener("click", () => {
    window.location.replace("/pages/reportIssue.html");
});