// Base URLs
const API_URL_DOCTORS = '/api/doctors/';

document.addEventListener('DOMContentLoaded', () => {
    // Basic Routing / Tab Switching Logic
    const navItems = document.querySelectorAll('.nav-item');
    const viewSections = document.querySelectorAll('.view-section');

    function switchView(targetId) {
        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.target === targetId) {
                item.classList.add('active');
            }
        });

        viewSections.forEach(section => {
            section.classList.remove('active');
            if (section.id === targetId) {
                section.classList.add('active');
            }
        });

        // Trigger loading data depending on view
        if (targetId === 'doctors') {
            fetchDoctors();
        } else if (targetId === 'map') {
            initMap(); // defined in inline script because of API key
        }
    }

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const target = e.currentTarget.dataset.target;
            switchView(target);
        });
    });

    // Default Load View
    switchView('doctors');

    /* =======================================
       DOCTOR CRUD OPERATIONS
       ======================================= */
    const doctorGrid = document.getElementById('doctorGrid');
    const addDoctorBtn = document.getElementById('addDoctorBtn');
    const doctorModal = document.getElementById('doctorModal');
    const doctorForm = document.getElementById('doctorForm');
    const cancelModal = document.getElementById('cancelModal');
    const modalTitle = document.getElementById('modalTitle');
    
    // Form fields
    const formId = document.getElementById('doc_id');
    const formName = document.getElementById('doc_name');
    const formSpecialty = document.getElementById('doc_specialty');
    const formLat = document.getElementById('doc_lat');
    const formLng = document.getElementById('doc_lng');

    // Fetch CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    async function fetchDoctors() {
        try {
            const res = await fetch(API_URL_DOCTORS);
            const data = await res.json();
            // Data could be paginated. Use data.results if paginated, else data.
            const results = data.results ? data.results : data;
            
            doctorGrid.innerHTML = '';
            
            results.forEach(doc => {
                const card = document.createElement('div');
                card.className = 'card doctor-card';
                card.innerHTML = `
                    <h3>${doc.name}</h3>
                    <p><strong>Specialty:</strong> ${doc.specialty}</p>
                    <p><strong>Lat/Lng:</strong> ${doc.latitude || 'N/A'}, ${doc.longitude || 'N/A'}</p>
                    <div class="card-actions">
                        <button class="btn btn-small edit-btn" data-id="${doc.id}">Edit</button>
                        <button class="btn btn-danger btn-small del-btn" data-id="${doc.id}">Delete</button>
                    </div>
                `;
                doctorGrid.appendChild(card);
            });

            // Attach event listeners for dynamic buttons
            document.querySelectorAll('.edit-btn').forEach(btn => btn.addEventListener('click', handleEditClick));
            document.querySelectorAll('.del-btn').forEach(btn => btn.addEventListener('click', handleDeleteClick));
            
        } catch (err) {
            console.error('Failed to fetch doctors', err);
        }
    }

    // Modal UI Handlers
    function openModal() {
        doctorModal.classList.add('active');
    }

    function closeModal() {
        doctorModal.classList.remove('active');
        doctorForm.reset();
        formId.value = '';
        modalTitle.innerText = "Add Doctor";
    }

    addDoctorBtn.addEventListener('click', () => {
        modelTitle = "Add Doctor";
        openModal();
    });
    cancelModal.addEventListener('click', closeModal);

    // Form Submit (Create / Update)
    doctorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            name: formName.value,
            specialty: formSpecialty.value,
            latitude: formLat.value ? parseFloat(formLat.value) : null,
            longitude: formLng.value ? parseFloat(formLng.value) : null
        };

        const docId = formId.value;
        const method = docId ? 'PUT' : 'POST';
        const url = docId ? `${API_URL_DOCTORS}${docId}/` : API_URL_DOCTORS;

        try {
            const res = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(payload)
            });

            if(res.ok) {
                closeModal();
                fetchDoctors();
            } else {
                const errorData = await res.json();
                alert(`Error: ${JSON.stringify(errorData)}`);
            }
        } catch (err) {
            console.error('Error saving doctor', err);
        }
    });

    async function handleEditClick(e) {
        const id = e.target.dataset.id;
        try {
            const res = await fetch(`${API_URL_DOCTORS}${id}/`);
            if (res.ok) {
                const doc = await res.json();
                formId.value = doc.id;
                formName.value = doc.name;
                formSpecialty.value = doc.specialty;
                formLat.value = doc.latitude;
                formLng.value = doc.longitude;
                modalTitle.innerText = "Edit Doctor";
                openModal();
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    }

    async function handleDeleteClick(e) {
        const id = e.target.dataset.id;
        if(confirm("Are you sure you want to delete this doctor?")) {
            try {
                const res = await fetch(`${API_URL_DOCTORS}${id}/`, {
                    method: 'DELETE',
                    headers: {'X-CSRFToken': csrftoken}
                });
                if(res.ok) fetchDoctors();
            } catch (err) {
                console.error('Error deleting', err);
            }
        }
    }

    /* =======================================
       INTEGRATIONS LOGIC
       ======================================= */
    
    // Weather
    const weatherBtn = document.getElementById('weatherBtn');
    const weatherCity = document.getElementById('weatherCity');
    const weatherResult = document.getElementById('weatherResult');
    
    weatherBtn.addEventListener('click', async () => {
        const city = weatherCity.value || 'New York';
        try {
            const r = await fetch(`/api/weather/?city=${city}`);
            const data = await r.json();
            weatherResult.innerText = JSON.stringify(data, null, 2);
        } catch (err) {
            weatherResult.innerText = `Error: ${err}`;
        }
    });

    // GitHub
    const githubBtn = document.getElementById('githubBtn');
    const githubUser = document.getElementById('githubUser');
    const githubResult = document.getElementById('githubResult');

    githubBtn.addEventListener('click', async () => {
        const user = githubUser.value || 'octocat';
        try {
            const r = await fetch(`/api/github/?username=${user}`);
            const data = await r.json();
            githubResult.innerText = JSON.stringify(data.slice(0, 3), null, 2); // Show first 3
        } catch (err) {
            githubResult.innerText = `Error: ${err}`;
        }
    });

    // RestCountries
    const countryBtn = document.getElementById('countryBtn');
    const countryName = document.getElementById('countryName');
    const countryResult = document.getElementById('countryResult');

    countryBtn.addEventListener('click', async () => {
        const name = countryName.value || 'India';
        try {
            const r = await fetch(`/api/country/?name=${name}`);
            const data = await r.json();
            countryResult.innerText = JSON.stringify(data, null, 2);
        } catch (err) {
            countryResult.innerText = `Error: ${err}`;
        }
    });

});
