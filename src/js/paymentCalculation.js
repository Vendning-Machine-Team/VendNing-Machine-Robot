const payButton = document.getElementById('payButton');
const reportButton = document.getElementById('reportButton');
const totalText = document.getElementById("total");
const productContainer = document.getElementById("productContainer");

//these variables allow us to have multiple different products
let products = [];
//this cart keeps track of the quantity of reach product
let cart = {};

// Load products from database
async function loadProducts() {

    const response = await fetch("/api/products");
    products = await response.json();

    productContainer.innerHTML = "";
    //this builds the html based on the products in the database.
    products.forEach(product => {

        cart[product.id] = 0;

        const row = document.createElement("div");
        row.className = "flex justify-between items-center py-3 border-b";

        row.innerHTML = `
            <div>
            <p class="font-medium">${product.name}</p>
            <p class="text-sm text-gray-500">$${product.price}</p>
            <p class="text-xs text-gray-400">${product.inventory} available</p>
            </div>

            <input
            type="number"
            min="0"
            max="${product.inventory}"
            value="0"
            data-id="${product.id}"
            class="w-20 text-center border rounded-lg"
            >
        `;

        productContainer.appendChild(row);
    });

    addInputListeners();
    calculateTotal();
}

// Listen for quantity changes
function addInputListeners() {

    const inputs = document.querySelectorAll("input[data-id]");

    inputs.forEach(input => {

        input.addEventListener("input", () => {

            const id = input.dataset.id;
            const qty = parseInt(input.value) || 0;

            cart[id] = qty;

            calculateTotal();
        });

    });
}

// Calculate total price
function calculateTotal() {
    let total = 0;
    products.forEach(product => {

        const qty = cart[product.id] || 0;
        total += qty * product.price;

    });
    
    totalText.innerText = `$${total}`;
    //prevents them from buying nothings
    payButton.disabled = total === 0;
}


reportButton.addEventListener("click", () => {
    window.location.replace("./pages/reportIssue.html");
});


//this currently points to a fake "stripe" session id this may need some slight changing in the future
payButton.addEventListener("click", async () => {

    const response = await fetch("/api/create-test-payment", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        items: cart
    })
});

    const data = await response.json();

    //checks to make sure that inventory was okay while ordering if not then it tells them
    if (!response.ok) {
        alert("Inventory changed while you were ordering. Please update your selection.");
        loadProducts(); // refresh inventory from server
        return;
    }
    const sessionId = data.session_id;

    window.location.replace(`./pages/paymentCode.html?session_id=${sessionId}`);
});

loadProducts();