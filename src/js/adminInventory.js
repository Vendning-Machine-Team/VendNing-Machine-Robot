const confirmButton = document.getElementById('confirmButton');
const homeButton = document.getElementById('homeButton');
const inventoryCount = document.getElementById('inventory_count');
const productPrice = document.getElementById('product_price');
const currentInventoryText = document.getElementById('currentInventory');
const currentPriceText = document.getElementById('currentPrice');
const productSelect = document.getElementById("productSelect");

const username = localStorage.getItem('adminUsername');

function calculateTotal() {
    const count = inventoryCount.value;
    const price = productPrice.value;
    const total = count * price;
    document.getElementById('total').innerText = `$${total}`;
    //loadData();
}

//this function will need to be done later to update to the database. i dont think it was actually doing anything
function updateInventory() {

    const count = inventoryCount.value;
    const price = productPrice.value;
    const productId = productSelect.value;

    fetch("/api/update-inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_id: productId,
            inventory: count,
            price: price,
            username:username
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        loadData();
    });
}

function loadData(){
    //get the current inventory and price for hte selected product
    const productId = productSelect.value;

    fetch(`/api/get-inventory/${productId}`)
        .then(response => response.json())
        .then(data => {
            currentInventoryText.innerText = `Current Inventory: ${data.inventory}`;
            currentPriceText.innerText = `Current Price: $${data.price}`;

            inventoryCount.value = data.inventory;
            productPrice.value = data.price;
        });
}

function loadProducts() {
    fetch("/api/get-products")
        .then(res => res.json())
        .then(products => {

            productSelect.innerHTML = "";

            products.forEach(product => {
                const option = document.createElement("option");
                option.value = product.id;
                option.textContent = product.name;
                productSelect.appendChild(option);
            });

            loadData(); // load first product automatically
        });
}


inventoryCount.addEventListener("input", calculateTotal);
productPrice.addEventListener("input", calculateTotal);

confirmButton.addEventListener('click', () => {
    alert("Successfully changed inventory")
    updateInventory();
    console.log('Confirm button clicked');
});

homeButton.addEventListener('click', () => {
    window.location.replace("./adminDashboard.html");
    console.log('Home button clicked');
});

productSelect.addEventListener("change", () => {
    loadData();
});

loadProducts();
calculateTotal();