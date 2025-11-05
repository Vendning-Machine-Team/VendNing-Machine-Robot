const setPathButton = document.getElementById('setPathButton');
const setInventoryButton = document.getElementById('setInventoryButton');
const viewAuditButton = document.getElementById('viewAuditButton');
const logOutButton = document.getElementById('logOutButton');

setPathButton.addEventListener('click', () => {
    window.location.replace("../setPath/setPath.html");
    console.log('Set Path button clicked');
});

setInventoryButton.addEventListener('click', () => {
    window.location.replace("../inventory/Inventory.html");
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
