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

payButton.addEventListener("click", async () => {

    const response = await fetch("/api/create-test-payment", {
        method: "POST"
    });

    const data = await response.json();

    const sessionId = data.session_id;

    window.location.replace(`./pages/paymentCode.html?session_id=${sessionId}`);
});

