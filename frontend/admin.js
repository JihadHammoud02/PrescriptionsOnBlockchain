function addDoctor() {
    const doctorAddress = document.getElementById('doctorInfo').value;
    const doctorName = document.getElementById('doctorName').value;
    const doctorsp = document.getElementById('doctorSp').value;
    let bodyContent = JSON.stringify({
        "add":doctorAddress,
        "name": doctorName,
        "sp":doctorsp,
    });
    let headersList = {
        "Accept": "*/*",
        "Content-Type": "application/json"
        };
    fetch('/addDosctor', {
        method: 'POST',
        body: bodyContent,
        headers: headersList
    
    })
    .then(response => response.json())
    .then(data =>console.log(data))

    
}


