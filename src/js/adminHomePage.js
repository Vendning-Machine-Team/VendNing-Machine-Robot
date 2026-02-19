const setPathButton = document.getElementById('setPathButton');
const setInventoryButton = document.getElementById('setInventoryButton');
const logOutButton = document.getElementById('logOutButton');

setPathButton.addEventListener('click', () => {
    window.location.replace("/pages/setPath.html");
    console.log('Set Path button clicked');
});

setInventoryButton.addEventListener('click', () => {
    window.location.replace("pages/setInventory.html");
    console.log('Set Inventory button clicked');
});

logOutButton.addEventListener('click', () => {
    window.location.replace("pages/adminLogin.html");
    console.log('Log Out button clicked');
});
