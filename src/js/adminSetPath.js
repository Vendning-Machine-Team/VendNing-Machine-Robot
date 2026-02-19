const homeButton = document.getElementById('homeButton');
const confirmButton = document.getElementById('confirmButton');
homeButton.addEventListener('click', () => {
    window.location.replace("pages/adminDashboard.html");
    console.log('Home button clicked');
});

confirmButton.addEventListener('click', () => {
    alert("Successfully updated path bounds")
    console.log('Confirm button clicked');
});