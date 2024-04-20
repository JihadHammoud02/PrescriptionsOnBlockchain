// Login functionality using MetaMask
function connectWallet() {
    var pk = document.getElementById("walletAddress").value;
    var privKey = document.getElementById("privateKey").value;
    let bodyContent = JSON.stringify({
                "pk":pk,
                "privKey": privKey
            });
            let headersList = {
                "Accept": "*/*",
                "Content-Type": "application/json"
                }
    fetch('http://127.0.0.1:8000/connect', {
        method: 'POST',
        body: bodyContent,
        headers: headersList
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.authentication == "Admin"){
            window.location.href='http://127.0.0.1:5500/frontend/admin.html';
        }
        else{
            if(data.authentication == "Doc"){
                window.location.href='http://127.0.0.1:5500/frontend/dashboard.html';
            }
        }
    })
}
