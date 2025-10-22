        const price = 10;

        function calculateTotal() {
            const count = document.getElementById('snackCount').value;
            const total = count * price;
            document.getElementById('total').innerText = `$${total}`;
        }

