
// Function to connect to wallet using Json RPC
async function connectWallet(){
    console.log(window.ethereum)
    if(window.ethereum !== "undefined"){
        await ethereum.request({ method: 'eth_requestAccounts' });
        address= await ethereum.request({ method: 'eth_accounts' })
        displayWalletAddress(address)
    }
}

// Adding a textContent to the div 
function displayWalletAddress(address){
    walletAddressBlock=document.querySelector("#walletAddress");
    walletAddressBlock.textContent+=address;
}





/* On document loading */
function setup(){
    connectWallet();
}
window.addEventListener('load',setup,false)