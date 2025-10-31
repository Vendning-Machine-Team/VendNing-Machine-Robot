// Basic guard: check session on page load and redirect to login if not authenticated
async function checkAuth() {
    try {
        const res = await fetch('/api/admin/me', { credentials: 'include' });
        if (!res.ok) {
            window.location.href = '/Login/Adminlogin.html';
            return false;
        }
        return true;
    } catch (err) {
        console.error('Auth check failed', err);
        window.location.href = '/Login/Adminlogin.html';
        return false;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const authed = await checkAuth();
    if (!authed) return; // redirected

    const setPathButton = document.getElementById('setPathButton');
    const setInventoryButton = document.getElementById('setInventoryButton');
    const viewAuditButton = document.getElementById('viewAuditButton');
    const logOutButton = document.getElementById('logOutButton');

    if (setPathButton) {
        setPathButton.addEventListener('click', () => {
            // TODO: Add logic for setting path
            console.log('Set Path button clicked');
        });
    }

    if (setInventoryButton) {
        setInventoryButton.addEventListener('click', () => {
            // TODO: Add logic for setting inventory
            console.log('Set Inventory button clicked');
        });
    }

    if (viewAuditButton) {
        viewAuditButton.addEventListener('click', () => {
            // TODO: Add logic for viewing audit
            console.log('View Audit button clicked');
        });
    }

    if (logOutButton) {
        logOutButton.addEventListener('click', async () => {
            console.log('Log Out button clicked');
            try {
                await fetch('/api/admin/logout', { method: 'POST', credentials: 'include' });
            } catch (err) {
                console.error('Logout failed', err);
            } finally {
                window.location.href = '/Login/Adminlogin.html';
            }
        });
    }
});
