function addPrescription() {
    const patientAddress = document.getElementById('patientAddress').value;
    const normalMedication = document.getElementById('normalMedication').value;
    const normalDosage = document.getElementById('normalDosage').value;
    const brandedMedication = document.getElementById('brandedMedication').value;
    const brandedDosage = document.getElementById('brandedDosage').value;

    if (window.ethereum) {
        const data = {
            patientAddress,
            medications,
            dosages
        };

        fetch('/addPrescription', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Prescription added:', data);
            alert('Prescription successfully added');
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please connect to MetaMask to add prescriptions.');
    }
}

function displayPrescriptions() {
    const patientAddress = document.getElementById('patientAddress').value;

    fetch(`/getPrescriptions/${patientAddress}`)
        .then(response => response.json())
        .then(data => {
            const prescriptionsList = document.getElementById('prescriptionList');
            prescriptionsList.innerHTML = ''; // Clear previous entries
            data.prescriptions.forEach(prescription => {
                const item = document.createElement('div');
                item.textContent = `Medication: ${prescription.medications.join(', ')} - Dosages: ${prescription.dosages.join(', ')} - Date: ${new Date(prescription.timestamp * 1000).toLocaleString()}`;
                prescriptionsList.appendChild(item);
            });
        })
        .catch(error => console.error('Error retrieving prescriptions:', error));
}
