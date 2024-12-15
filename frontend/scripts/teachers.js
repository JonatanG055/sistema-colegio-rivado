document.addEventListener("DOMContentLoaded", () => {
    loadProfesores();

    const addForm = document.getElementById("addProfesorForm");
    addForm.addEventListener("submit", function (event) {
        // Previene el envío del formulario si no es válido
        if (!addForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            addProfesor();
        }

        // Marca el formulario como validado
        addForm.classList.add('was-validated');
    });
});

const token = localStorage.getItem('authToken');
const apiUrl = 'http://127.0.0.1:5000/profesores';

// Función para cargar la lista de profesores con sus cursos
function loadProfesores() {
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` 
        }
    })
    .then(response => response.json())
    .then(data => {
        const profesorList = document.getElementById("profesorList");
        profesorList.innerHTML = ''; 

        data.forEach(profesor => {
            const cursosList = profesor.Cursos.length > 0 
                ? `<ul>${profesor.Cursos.map(curso => `<li>${curso}</li>`).join('')}</ul>` 
                : "<p>Sin cursos asignados</p>";

            profesorList.innerHTML += `
                <div class="contents-row d-flex" data-id="${profesor.ProfesorID}">
                    <div class="content-cell"><p>${profesor.Nombre}</p></div>
                    <div class="content-cell"><p>${profesor.Apellido}</p></div>
                    <div class="content-cell"><p>${profesor.Especialidad}</p></div>
                    <div class="content-cell"><p>${profesor.Telefono}</p></div>
                    <div class="content-cell"><p>${profesor.Email}</p></div>
                    <div class="content-cell">${cursosList}</div>
                    <div class="content-cell">
                        <button onclick="showEditModal(${profesor.ProfesorID})" class="btn btn-warning mr-2">Editar</button>
                        <button onclick="showDeleteModal(${profesor.ProfesorID})" class="btn btn-danger">Eliminar</button>
                    </div>
                </div>`;
        });
    })
    .catch(error => console.error('Error al cargar profesores:', error));
}


// Función para agregar un nuevo profesor
function addProfesor() {
    const profesorData = {
        Nombre: document.getElementById("addProfesorName").value,
        Apellido: document.getElementById("addProfesorLastName").value,
        Especialidad: document.getElementById("addProfessorSpecialty").value,
        Telefono: document.getElementById("addProfesorPhone").value,
        Email: document.getElementById("addProfesorEmail").value
    };

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agrega el token en el encabezado
        },
        body: JSON.stringify(profesorData)
    })
    .then(response => response.json())
    .then(() => {
        $('#addModal').modal('hide');
        loadProfesores();
        clearModalFields();
    })
    .catch(error => console.error('Error al añadir profesor:', error));
}

// Función para mostrar el modal de edición con los datos del profesor
function showEditModal(profesorId) {
    fetch(`${apiUrl}/${profesorId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agrega el token en el encabezado
        }
    })
    .then(response => response.json())
    .then(profesor => {
        document.getElementById("editProfesorName").value = profesor.Nombre;
        document.getElementById("editProfesorLastName").value = profesor.Apellido;
        document.getElementById("editProfessorSpecialty").value = profesor.Especialidad;
        document.getElementById("editProfesorPhone").value = profesor.Telefono;
        document.getElementById("editProfesorEmail").value = profesor.Email;
        document.getElementById("editProfesorForm").dataset.profesorId = profesorId; 
        $('#editModal').modal('show');
    })
    .catch(error => console.error('Error al cargar datos del profesor para edición:', error));
}

// Función para editar un profesor
function editProfesor() {
    const profesorId = document.getElementById("editProfesorForm").dataset.profesorId;
    const updatedData = {
        Nombre: document.getElementById("editProfesorName").value,
        Apellido: document.getElementById("editProfesorLastName").value,
        Especialidad: document.getElementById("editProfessorSpecialty").value,
        Telefono: document.getElementById("editProfesorPhone").value,
        Email: document.getElementById("editProfesorEmail").value
    };

    fetch(`${apiUrl}/${profesorId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agrega el token en el encabezado
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(() => {
        $('#editModal').modal('hide');
        loadProfesores(); 
    })
    .catch(error => console.error('Error al editar profesor:', error));
}

// Función para mostrar el modal de eliminación
function showDeleteModal(profesorId) {
    document.getElementById("deleteModal").dataset.profesorId = profesorId;
    $('#deleteModal').modal('show');
}

// Función para eliminar un profesor
function deleteProfesor() {
    const profesorId = document.getElementById("deleteModal").dataset.profesorId;

    fetch(`${apiUrl}/${profesorId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}` // Agrega el token en el encabezado
        }
    })
    .then(response => response.json())
    .then(() => {
        $('#deleteModal').modal('hide');
        loadProfesores(); 
    })
    .catch(error => console.error('Error al eliminar profesor:', error));
}

// Función para limpiar los campos de los modales
function clearModalFields() {
    document.getElementById("addProfesorForm").reset();
}

// Limpiar el formulario cuando se cierre el modal de añadir
$('#addModal').on('hidden.bs.modal', function () {
    clearModalFields();
});
