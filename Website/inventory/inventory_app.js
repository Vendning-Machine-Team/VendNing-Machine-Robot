

function calculateTotal() {
    const count = document.getElementById('inventory_count').value;
    const price = document.getElementById('product_price').value;
    const total = count * price;
    document.getElementById('total').innerText = `$${total}`;
}

function updateInventory() {
    const count = document.getElementById('inventory_count').value;
    const price = document.getElementById('product_price').value;
    document.getElementById('current_Inventory').innerText = count;
    document.getElementById('current_Price').innerText = price;
    calculateTotal();
}