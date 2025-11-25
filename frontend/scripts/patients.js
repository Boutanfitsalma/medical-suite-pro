const apiUrl = 'http://localhost:5000/api/patients';

function fetchPatients() {
    fetch('http://localhost:5000/patients')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("patient-list");
            tableBody.innerHTML = '';
            data.forEach(p => {
                const row = `
                    <tr>
                        <td>${p.nom || ''}</td>
                        <td>${p.age || ''}</td>
                        <td>${p.sexe || ''}</td>
                        <td>${p.telephone || ''}</td>
                        <td>${p.couverture || ''}</td>
                        <td>
                            <button class="btn btn-info btn-sm" onclick='editPatient("${p._id}", 
                                "${encodeURIComponent(p.nom)}", 
                                ${p.age}, 
                                "${encodeURIComponent(p.sexe)}", 
                                "${encodeURIComponent(p.telephone)}", 
                                "${encodeURIComponent(p.couverture)}")'>Modifier</button>
                            <button class="btn btn-danger btn-sm" onclick='deletePatient("${p._id}")'>Supprimer</button>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => console.error('Erreur :', error));
}

function addOrUpdatePatient() {
    const id = document.getElementById('patient-id').value;
    const patient = {
        nom: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        sexe: document.getElementById('gender').value,
        telephone: document.getElementById('phone').value,
        couverture: document.getElementById('coverage').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${apiUrl}/${id}` : apiUrl;

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patient)
    }).then(() => {
        fetchPatients();
        document.getElementById('patient-form').reset();
        document.getElementById('patient-id').value = '';
    });
}

function editPatient(id, nom, age, sexe, telephone, couverture) {
    document.getElementById('patient-id').value = id;
    document.getElementById('name').value = decodeURIComponent(nom);
    document.getElementById('age').value = age;
    document.getElementById('gender').value = decodeURIComponent(sexe);
    document.getElementById('phone').value = decodeURIComponent(telephone);
    document.getElementById('coverage').value = decodeURIComponent(couverture);
}

function deletePatient(id) {
    fetch(`${apiUrl}/${id}`, { method: 'DELETE' }).then(fetchPatients);
}

document.getElementById('patient-form').addEventListener('submit', (e) => {
    e.preventDefault();
    addOrUpdatePatient();
});

window.onload = fetchPatients;
