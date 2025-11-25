const apiUrl = 'http://localhost:5000/api/medical-records';
let currentPatientId = new URLSearchParams(window.location.search).get('patientId');

document.addEventListener('DOMContentLoaded', () => {
    if(currentPatientId) {
        loadPatientDetails();
        loadMedicalRecords();
    }
});

async function loadPatientDetails() {
    try {
        const response = await fetch(`http://localhost:5000/api/patients/${currentPatientId}`);
        const patient = await response.json();
        document.getElementById('patient-name').textContent = patient.nom; // Affiche le nom
        document.title = `Dossier Médical - ${patient.nom}`; // Met à jour le titre
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('patient-name').textContent = "Patient inconnu";
    }
}

async function loadMedicalRecords() {
    try {
        const response = await fetch(`${apiUrl}?patientId=${currentPatientId}`);
        const records = await response.json();
        renderRecords(records);
    } catch (error) {
        console.error('Erreur:', error);
    }
}

function renderRecords(records) {
    const container = document.getElementById('medical-records');
    container.innerHTML = '';
    
    if(records.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info">
                    Aucun dossier médical trouvé pour ce patient
                </div>
            </div>
        `;
        return;
    }
    
    records.forEach(record => {
        const card = `
            <div class="col-md-6">
                <div class="document-card card mb-3">
                    <div class="card-header">
                        ${new Date(record.date).toLocaleDateString('fr-FR')}
                        <button class="btn btn-sm btn-danger float-end" 
                                onclick="deleteRecord('${record._id}')">Supprimer</button>
                    </div>
                    <div class="card-body">
                        <h5>Diagnostic:</h5>
                        <p>${record.diagnosis}</p>
                        ${record.prescription ? `<h5>Ordonnance:</h5><pre>${record.prescription}</pre>` : ''}
                        ${record.test_results ? `<h5>Examens:</h5><pre>${record.test_results}</pre>` : ''}
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

// Gestion du formulaire
document.getElementById('record-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const recordData = {
        patient_id: currentPatientId,
        date: document.getElementById('record-date').value,
        diagnosis: document.getElementById('diagnosis').value,
        prescription: document.getElementById('prescription').value,
        test_results: document.getElementById('test-results').value
    };

    try {
        await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(recordData)
        });
        loadMedicalRecords();
        e.target.reset();
    } catch (error) {
        console.error('Erreur:', error);
    }
});

async function deleteRecord(recordId) {
    if(confirm('Confirmer la suppression ?')) {
        await fetch(`${apiUrl}/${recordId}`, { method: 'DELETE' });
        loadMedicalRecords();
    }
}