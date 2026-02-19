document.addEventListener("DOMContentLoaded", () => {
    const submitButton = document.getElementById("submitButton");
    const issueTextArea = document.getElementById("issue");
    const homeButton = document.getElementById("homebutton");

    submitButton.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent page reload
        const issueText = issueTextArea.value.trim();

        if (issueText === "") {
            alert("Please enter an issue before submitting.");
        } else {
            // TODO: Send to backend or store issue
            console.log("Issue submitted:", issueText);
            alert("Thank you for reporting the issue!");
            issueTextArea.value = ""; // Clear textarea
        }
    });

    // Handle home button click
    homeButton.addEventListener("click", () => {
        //TODO: allow for going to the home page
        //window.location.href = "home.html"; // Change to your actual home page
        window.location.replace("../Startpage/Startpage.html");
    });
});
