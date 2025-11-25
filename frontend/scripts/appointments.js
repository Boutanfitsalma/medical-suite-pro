const apiUrl = 'http://localhost:5000/api/appointments';

// Remplacer la fonction fetchAppointments par :
async function fetchAppointments() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        const data = await response.json();
        renderAppointments(data);
    } catch (error) {
        console.error('Erreur:', error);
        showErrorToast('Impossible de charger les rendez-vous');
    }
}

// Ajouter cette fonction d'affichage d'erreur
function showErrorToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast bg-danger text-white';
    toast.innerHTML = `
        <div class="toast-body">
            ${message}
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function getStatusBadge(status) {
    const statusStyles = {
        'planned': 'bg-primary',
        'completed': 'bg-success',
        'cancelled': 'bg-danger'
    };
    return statusStyles[status] || 'bg-secondary';
}

function addOrUpdateAppointment() {
    const id = document.getElementById('appointment-id').value;
    const appointment = {
        patient_name: document.getElementById('patient-name').value,
        date: new Date(document.getElementById('date').value).toISOString(),
        reason: document.getElementById('reason').value,
        status: document.getElementById('status').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${apiUrl}/${id}` : apiUrl;

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(appointment)
    }).then(() => {
        fetchAppointments();
        document.getElementById('appointment-form').reset();
        document.getElementById('appointment-id').value = '';
    });
}

function editAppointment(id, patientName, date, reason, status) {
    document.getElementById('appointment-id').value = id;
    document.getElementById('patient-name').value = decodeURIComponent(patientName);
    document.getElementById('date').value = new Date(date).toISOString().slice(0, 16);
    document.getElementById('reason').value = decodeURIComponent(reason);
    document.getElementById('status').value = status;
}

function renderAppointments(data) {
    const tableBody = document.getElementById("appointments-list");
    tableBody.innerHTML = `
        <tr>
            <th>Patient</th>
            <th>Date</th>
            <th>Motif</th>
            <th>Statut</th>
            <th>Créé le</th>
            <th>Actions</th>
        </tr>
    `;

    data.forEach(a => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${a.patient_name}</td>
            <td>${new Date(a.date).toLocaleString('fr-FR')}</td>
            <td>${a.reason}</td>
            <td><span class="badge ${getStatusBadge(a.status)}">${a.status}</span></td>
            <td>${new Date(a.created_at).toLocaleDateString('fr-FR')}</td>
            <td>
                <button class="btn btn-info btn-sm" 
                    onclick='editAppointment("${a._id}", "${a.patient_name}", "${a.date}", "${a.reason}", "${a.status}")'>
                    Modifier
                </button>
                <button class="btn btn-danger btn-sm" 
                    onclick='deleteAppointment("${a._id}")'>
                    Supprimer
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
} 

function deleteAppointment(id) {
    if(confirm('Confirmer la suppression ?')) {
        fetch(`${apiUrl}/${id}`, { method: 'DELETE' }).then(fetchAppointments);
    }
}

document.getElementById('appointment-form').addEventListener('submit', (e) => {
    e.preventDefault();
    addOrUpdateAppointment();
});

window.onload = fetchAppointments;