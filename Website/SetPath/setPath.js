const homeButton = document.getElementById('homeButton');
homeButton.addEventListener('click', () => {
    window.location.replace("../adminPage/adminPage.html");
    console.log('Home button clicked');
});