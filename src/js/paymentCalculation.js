const payButton = document.getElementById('payButton');
const reportButton = document.getElementById('reportButton');

const price = 10;

function calculateTotal() {
    const count = document.getElementById('snackCount').value;
    const total = count * price;
    document.getElementById('total').innerText = `$${total}`;
}

reportButton.addEventListener("click", () => {
    window.location.replace("/public/pages/reportIssue.html");
});

payButton.addEventListener("click", () => {
    window.location.replace("/public/pages/paymentCode.html");
});

