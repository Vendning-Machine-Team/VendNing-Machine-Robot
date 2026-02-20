const payButton = document.getElementById('payButton');
const reportButton = document.getElementById('reportButton');
const snackCount = document.getElementById('snackCount');
const price = 10;

function calculateTotal() {
    const count = snackCount.value;
    const total = count * price;
    document.getElementById('total').innerText = `$${total}`;
}

//taking calculateTotal out of the html so that it registers properly when built.
snackCount.addEventListener("input", calculateTotal);

reportButton.addEventListener("click", () => {
    window.location.replace("./pages/reportIssue.html");
});

payButton.addEventListener("click", () => {
    window.location.replace("./pages/paymentCode.html");
});

