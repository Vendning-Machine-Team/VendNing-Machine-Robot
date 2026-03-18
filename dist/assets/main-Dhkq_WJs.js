import"./style-B4IgR0yf.js";const i=document.getElementById("payButton"),l=document.getElementById("reportButton"),p=document.getElementById("total"),s=document.getElementById("productContainer");let o=[],a={};async function c(){o=await(await fetch("/api/products")).json(),s.innerHTML="",o.forEach(e=>{a[e.id]=0;const t=document.createElement("div");t.className="flex justify-between items-center py-3 border-b",t.innerHTML=`
            <div>
            <p class="font-medium">${e.name}</p>
            <p class="text-sm text-gray-500">$${e.price}</p>
            <p class="text-xs text-gray-400">${e.inventory} available</p>
            </div>

            <input
            type="number"
            min="0"
            max="${e.inventory}"
            value="0"
            data-id="${e.id}"
            class="w-20 text-center border rounded-lg"
            >
        `,s.appendChild(t)}),u(),r()}function u(){document.querySelectorAll("input[data-id]").forEach(e=>{e.addEventListener("input",()=>{const t=e.dataset.id,d=parseInt(e.value)||0;a[t]=d,r()})})}function r(){let n=0;o.forEach(e=>{const t=a[e.id]||0;n+=t*e.price}),p.innerText=`$${n}`,i.disabled=n===0}l.addEventListener("click",()=>{window.location.replace("./pages/reportIssue.html")});i.addEventListener("click",async()=>{const n=await fetch("/api/create-test-payment",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({items:a})}),e=await n.json();if(!n.ok){alert("Inventory changed while you were ordering. Please update your selection."),c();return}const t=e.session_id;window.location.replace(`./pages/paymentCode.html?session_id=${t}`)});c();
