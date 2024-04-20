function addPrescription() {
    const patientAddress = document.getElementById('patientAddress').value;
    const normalMedication = document.getElementById('normalMedication').value;
    const normalDosage = document.getElementById('normalDosage').value;
    const brandedMedication = document.getElementById('brandedMedication').value;
    const brandedDosage = document.getElementById('brandedDosage').value;

    // Assume API endpoint and method in your backend to handle this
    const postData = {
        patientAddress,
        normalMedication,
        normalDosage,
        brandedMedication,
        brandedDosage
    };

    fetch('/api/addPrescription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(data => alert('Prescription added successfully'))
    .catch(error => alert('Error adding prescription: ' + error));
}
