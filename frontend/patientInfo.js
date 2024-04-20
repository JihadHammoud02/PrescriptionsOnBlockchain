// patientInfo.js

function getPatientInfo() {
    const patientAddress = document.getElementById('patientAddress').value;

    fetch(`/api/getPatientInfo/${patientAddress}`)
        .then(response => response.json())
        .then(data => {
            const patientInfoDisplay = document.getElementById('patientInfoDisplay');

            // Clear previous data
            patientInfoDisplay.innerHTML = '';

            if (data.length > 0) {
                const ul = document.createElement('ul');

                data.forEach(info => {
                    const li = document.createElement('li');
                    li.textContent = `${info.key}: ${info.value}`;
                    ul.appendChild(li);
                });

                patientInfoDisplay.appendChild(ul);
            } else {
                patientInfoDisplay.textContent = 'No information found for this patient.';
            }
        })
        .catch(error => {
            console.error('Error fetching patient information:', error);
            const patientInfoDisplay = document.getElementById('patientInfoDisplay');
            patientInfoDisplay.textContent = 'An error the adress provided may be wrong.';
        });
}
