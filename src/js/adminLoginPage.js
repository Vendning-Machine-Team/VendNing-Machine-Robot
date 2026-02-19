// Fixed credentials (temporary)
const ADMIN_USERNAME = "username";
const ADMIN_PASSWORD = "password1234";

// Grab elements
const form = document.querySelector("form");
const usernameInput = document.querySelector('input[type="text"]');
const passwordInput = document.querySelector('input[type="password"]');

// Optional error message (we’ll inject it)
const errorMessage = document.createElement("p");
errorMessage.textContent = "Invalid username or password";
errorMessage.className = "mt-4 text-center text-red-500 text-sm hidden";
form.appendChild(errorMessage);

// Handle form submission
form.addEventListener("submit", (event) => {
  event.preventDefault(); //stops page reload

  const enteredUsername = usernameInput.value.trim();
  const enteredPassword = passwordInput.value;

  if (
    enteredUsername === ADMIN_USERNAME &&
    enteredPassword === ADMIN_PASSWORD
  ) {
    // Successful logi
    window.location.href = "pages/adminDashboard.html";
  } else {
    // Show error
    errorMessage.classList.remove("hidden");
  }
});

// Hide error when typing again
usernameInput.addEventListener("input", () => {
  errorMessage.classList.add("hidden");
});
passwordInput.addEventListener("input", () => {
  errorMessage.classList.add("hidden");
});
