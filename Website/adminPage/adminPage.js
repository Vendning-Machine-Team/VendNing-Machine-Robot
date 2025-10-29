const setPathButton = document.getElementById('setPathButton');
const setInventoryButton = document.getElementById('setInventoryButton');
const viewAuditButton = document.getElementById('viewAuditButton');
const logOutButton = document.getElementById('logOutButton');

setPathButton.addEventListener('click', () => {
    // TODO: Add logic for setting path
    console.log('Set Path button clicked');
});

setInventoryButton.addEventListener('click', () => {
    // TODO: Add logic for setting inventory
    console.log('Set Inventory button clicked');
});

viewAuditButton.addEventListener('click', () => {
    // TODO: Add logic for viewing audit
    console.log('View Audit button clicked');
});

logOutButton.addEventListener('click', () => {
    window.location.replace("../Startpage/Startpage.html");
    console.log('Log Out button clicked');
});
