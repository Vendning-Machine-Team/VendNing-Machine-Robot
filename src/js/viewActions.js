const actionsTextArea = document.getElementById('actions');
const homebutton = document.getElementById('homeButton');

homebutton.addEventListener('click', () => {
    window.location.replace("./adminDashboard.html");
});

async function fetchActions() {
    try {
        const response = await fetch('/api/get-actions');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const header = 'Action Time | Username | Action Type';
        const formatted = data.map(a =>
            `${a.action_time} | ${a.username} | ${a.type_name}`
        );

        actionsTextArea.value = header + '\n\n' + formatted.join('\n\n');
    } catch (error) {
        console.error('Error fetching actions:', error);
        actionsTextArea.value = 'Failed to load actions.';
    }
}

fetchActions();