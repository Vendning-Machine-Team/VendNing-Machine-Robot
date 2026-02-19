const setPathButton = document.getElementById('setPathButton');
const setInventoryButton = document.getElementById('setInventoryButton');
const logOutButton = document.getElementById('logOutButton');

setPathButton.addEventListener('click', () => {
    window.location.replace("./setPath.html");
    console.log('Set Path button clicked');
});

setInventoryButton.addEventListener('click', () => {
    window.location.replace("./setInventory.html");
    console.log('Set Inventory button clicked');
});

logOutButton.addEventListener('click', () => {
    window.location.replace("./adminLogin.html");
    console.log('Log Out button clicked');
});
