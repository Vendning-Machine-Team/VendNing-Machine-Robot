// Fixed credentials (temporary)
//const ADMIN_USERNAME = "username";
//const ADMIN_PASSWORD = "password1234";

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
// Handle form submission
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const enteredUsername = usernameInput.value.trim();
  const enteredPassword = passwordInput.value;

  try {
    const response = await fetch("/api/admin-login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: enteredUsername,
        password: enteredPassword,
      }),
    });

    const result = await response.json();

    if (result.success) {
      // login successful
      localStorage.setItem("adminUsername", result.username);
      window.location.href = "./adminDashboard.html";
    } else {
      // login failed
      errorMessage.classList.remove("hidden");
    }

  } catch (error) {
    console.error("Login error:", error);
    errorMessage.textContent = "Server error";
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
