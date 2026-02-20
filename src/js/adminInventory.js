const confirmButton = document.getElementById('confirmButton');
const homeButton = document.getElementById('homeButton');
const inventoryCount = document.getElementById('inventory_count');
const productPrice = document.getElementById('product_price');

function calculateTotal() {
    const count = inventoryCount.value;
    const price = productPrice.value;
    const total = count * price;
    document.getElementById('total').innerText = `$${total}`;
}

//this function will need to be done later to update to the database. i dont think it was actually doing anything
// function updateInventory() {

// }
inventoryCount.addEventListener("input", calculateTotal);
productPrice.addEventListener("input", calculateTotal);

confirmButton.addEventListener('click', () => {
    alert("Successfully changed inventory")
   // updateInventory();
    console.log('Confirm button clicked');
});

homeButton.addEventListener('click', () => {
    window.location.replace("./adminDashboard.html");
    console.log('Home button clicked');
});