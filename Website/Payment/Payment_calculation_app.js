        const payButton = document.querySelector("#pay");
        const reportButton = document.querySelector("#report");
        
        const price = 10;

        function calculateTotal() {
            const count = document.getElementById('snackCount').value;
            const total = count * price;
            document.getElementById('total').innerText = `$${total}`;
        }

        reportButton.addEventListener("click", () => {
            window.location.replace("../reportIssue/reportIssue.html");
        });

