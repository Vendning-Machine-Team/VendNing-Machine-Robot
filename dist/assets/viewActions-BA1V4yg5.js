import"./style-B4IgR0yf.js";const o=document.getElementById("actions"),r=document.getElementById("homeButton");r.addEventListener("click",()=>{window.location.replace("./adminDashboard.html")});async function i(){try{const t=await fetch("/api/get-actions");if(!t.ok)throw new Error("Network response was not ok");const n=await t.json(),a="Action Time | Username | Action Type",c=n.map(e=>`${e.action_time} | ${e.username} | ${e.type_name}`);o.value=a+`

`+c.join(`

`)}catch(t){console.error("Error fetching actions:",t),o.value="Failed to load actions."}}i();
