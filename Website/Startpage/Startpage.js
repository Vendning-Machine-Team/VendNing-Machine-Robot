const adminLoginButton = document.querySelector("#admin-login");
const payButton = document.querySelector("#pay-service");

adminLoginButton.addEventListener("click", () => {
    window.location.replace("../AdminLogin/AdminLogin.html");
})

payButton.addEventListener("click", () => {
    window.location.replace("../Price/Payment_calculation.html");
})

// Button functionallity for Snack page added here