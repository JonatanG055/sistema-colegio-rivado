document.addEventListener("DOMContentLoaded", () => {
    loadStudents();

    const addForm = document.getElementById("addStudentForm");
        addForm.addEventListener("submit", function(event) {
            // Previene el envío del formulario si no es válido
            if (!addForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                addStudent();
            }
    
            // Marca el formulario como validado
            addForm.classList.add('was-validated');
        });
});

const token = localStorage.getItem('authToken');
const apiUrl = 'http://127.0.0.1:5000/api/estudiantes'; 

// Función para cargar la lista de estudiantes
function loadStudents() {
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Agrega el token en el encabezado
        }
    })
    .then(response => response.json())
    .then(data => {
        const studentList = document.getElementById("studentList");
        studentList.innerHTML = '';
        data.forEach(student => {
            studentList.innerHTML += `
                <div class="contents-row d-flex" data-id="${student.EstudianteID}">
                    <div class="content-cell"><p>${student.Nombre}</p></div>
                    <div class="content-cell"><p>${student.Apellido}</p></div>
                    <div class="content-cell"><p>${student.FechaNacimiento}</p></div>
                    <div class="content-cell"><p>${student.Direccion}</p></div>
                    <div class="content-cell"><p>${student.Telefono}</p></div>
                    <div class="content-cell"><p>${student.Email}</p></div>
                    <div class="content-cell">
                        <button onclick="showEditModal(${student.EstudianteID})" class="btn btn-warning mr-2">Editar</button>
                        <button onclick="showDeleteModal(${student.EstudianteID})" class="btn btn-danger">Eliminar</button>
                    </div>
                </div>`;
        });
    })
    .catch(error => console.error('Error al cargar estudiantes:', error));
}


// Función para agregar un nuevo estudiante
function addStudent() {
    const studentData = {
        nombre: document.getElementById("addStudentName").value, 
        apellido: document.getElementById("addStudentLastName").value, 
        fecha_nacimiento: document.getElementById("addStudentBirthDate").value, 
        direccion: document.getElementById("addStudentAddress").value, 
        telefono: document.getElementById("addStudentPhone").value, 
        email: document.getElementById("addStudentEmail").value 
    };

    fetch(apiUrl, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(studentData)
    })
    .then(response => response.json())
    .then(() => {
        $('#addModal').modal('hide');
        loadStudents();
        clearModalFields();
    })
    .catch(error => console.error('Error al añadir estudiante:', error));
}


// Función para mostrar el modal de edición con los datos del estudiante
function showEditModal(studentId) {
    fetch(`${apiUrl}/${studentId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Agrega el token en el encabezado
        }
    })
    .then(response => response.json())
    .then(student => {
        document.getElementById("editStudentName").value = student.Nombre;
        document.getElementById("editStudentLastName").value = student.Apellido;
        document.getElementById("editStudentBirthDate").value = student.FechaNacimiento;
        document.getElementById("editStudentAddress").value = student.Direccion;
        document.getElementById("editStudentPhone").value = student.Telefono;
        document.getElementById("editStudentEmail").value = student.Email;
        document.getElementById("editStudentForm").dataset.studentId = studentId; 
        $('#editModal').modal('show');
    })
    .catch(error => console.error('Error al cargar datos del estudiante para edición:', error));
}


// Función para editar un estudiante
function editStudent() {
    const studentId = document.getElementById("editStudentForm").dataset.studentId;
    const updatedData = {
        nombre: document.getElementById("editStudentName").value,
        apellido: document.getElementById("editStudentLastName").value,
        fecha_nacimiento: document.getElementById("editStudentBirthDate").value,
        direccion: document.getElementById("editStudentAddress").value,
        telefono: document.getElementById("editStudentPhone").value,
        email: document.getElementById("editStudentEmail").value
    };

    fetch(`${apiUrl}/${studentId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Agrega el token en el encabezado
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(() => {
        $('#editModal').modal('hide');
        loadStudents(); 
    })
    .catch(error => console.error('Error al editar estudiante:', error));
}


// Función para mostrar el modal de eliminación
function showDeleteModal(studentId) {
    document.getElementById("deleteModal").dataset.studentId = studentId;
    $('#deleteModal').modal('show');
}


// Función para eliminar un estudiante
function deleteStudent() {
    const studentId = document.getElementById("deleteModal").dataset.studentId;

    fetch(`${apiUrl}/${studentId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`  // Agrega el token en el encabezado
        }
    })
    .then(response => response.json())
    .then(() => {
        $('#deleteModal').modal('hide');
        loadStudents(); 
    })
    .catch(error => console.error('Error al eliminar estudiante:', error));
}


// Función para limpiar los campos del formulario
function clearModalFields() {
    document.getElementById("addStudentForm").reset();
}


// Limpiar el formulario cuando se cierre el modal de añadir
$('#addModal').on('hidden.bs.modal', function () {
    clearModalFields();
});
