// URLs de las APIs
const inscriptionApiUrl = 'http://127.0.0.1:5000/asistencias';
const studentApiUrl = 'http://127.0.0.1:5000/api/estudiantes';
const enrollmentApiUrl = 'http://127.0.0.1:5000/inscripciones/estudiantes';

// Obtener el token del localStorage
const token = localStorage.getItem('authToken');

document.addEventListener("DOMContentLoaded", () => {
    loadAsistencias();

    const addForm = document.getElementById("addAsistenciaForm");
        addForm.addEventListener("submit", function(event) {
            // Previene el envío del formulario si no es válido
            if (!addForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                addAsistencia();
            }
    
            // Marca el formulario como validado
            addForm.classList.add('was-validated');
        });
});

// Cargar estudiantes en los select de los modales
function loadStudents() {
    return fetch(studentApiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        }
    })
        .then(response => response.json())
        .then(data => {
            const addSelect = document.getElementById("addAsistenciaStudent");
            const editSelect = document.getElementById("editAsistenciaStudent");

            addSelect.innerHTML = '<option value="">Seleccione un estudiante</option>';
            editSelect.innerHTML = '<option value="">Seleccione un estudiante</option>';

            data.forEach(student => {
                const option = `<option value="${student.EstudianteID}">${student.Nombre} ${student.Apellido}</option>`;
                addSelect.innerHTML += option;
                editSelect.innerHTML += option;
            });
        })
        .catch(error => console.error('Error al cargar estudiantes:', error));
}

// Cargar cursos inscritos por un estudiante específico
function loadCourses(estudianteId, targetSelectId) {
    const select = document.getElementById(targetSelectId);

    if (!estudianteId) {
        select.innerHTML = '<option value="">Seleccione un curso</option>';
        return;
    }

    return fetch(`${enrollmentApiUrl}/${estudianteId}/cursos`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        }
    })
        .then(response => response.json())
        .then(data => {
            select.innerHTML = '<option value="">Seleccione un curso</option>';
            data.forEach(course => {
                const option = `<option value="${course.CursoID}">${course.Nombre}</option>`;
                select.innerHTML += option;
            });
        })
        .catch(error => console.error('Error al cargar cursos:', error));
}

// Cargar lista de asistencias
function loadAsistencias() {
    fetch(inscriptionApiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        }
    })
        .then(response => response.json())
        .then(data => {
            const asistenciaList = document.getElementById("asistenciaList");
            asistenciaList.innerHTML = '';
            data.forEach(asistencia => {
                asistenciaList.innerHTML += `
                    <div class="contents-row d-flex" data-id="${asistencia.AsistenciaID}">
                        <div class="content-cell"><p>${asistencia.NombreEstudiante}</p></div>
                        <div class="content-cell"><p>${asistencia.NombreCurso}</p></div>
                        <div class="content-cell"><p>${asistencia.Fecha}</p></div>
                        <div class="content-cell"><p>${asistencia.Estado}</p></div>
                        <div class="content-cell">
                            <button onclick="showEditModal(${asistencia.AsistenciaID})" class="btn btn-warning mr-2">Editar</button>
                            <button onclick="showDeleteModal(${asistencia.AsistenciaID})" class="btn btn-danger">Eliminar</button>
                        </div>
                    </div>`;
            });
        })
        .catch(error => console.error('Error al cargar asistencias:', error));
}

// Llamar a la función de cargar estudiantes y cursos al abrir el modal
$('#addModal').on('show.bs.modal', function () {
    loadStudents().then(() => {
        const selectedStudentId = document.getElementById("addAsistenciaStudent").value;
        loadCourses(selectedStudentId, 'addAsistenciaCourse');
    });
});

// Manejar el cambio de estudiante en el modal de añadir
document.getElementById("addAsistenciaStudent").addEventListener("change", function () {
    const selectedStudentId = this.value;
    loadCourses(selectedStudentId, 'addAsistenciaCourse');
});

// Añadir asistencia
function addAsistencia() {
    const asistenciaData = {
        EstudianteID: document.getElementById("addAsistenciaStudent").value,
        CursoID: document.getElementById("addAsistenciaCourse").value,
        Fecha: document.getElementById("addAsistenciaDate").value,
        Estado: document.getElementById("addAsistenciaState").value
    };

    fetch(inscriptionApiUrl, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        },
        body: JSON.stringify(asistenciaData)
    })
        .then(response => response.json())
        .then(() => {
            loadAsistencias();
            $('#addModal').modal('hide');
        })
        .catch(error => console.error('Error al añadir asistencia:', error));
}

// Mostrar modal de edición
function showEditModal(asistenciaId) {
    fetch(`${inscriptionApiUrl}/${asistenciaId}`, {
        method: 'GET',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        }
    })
        .then(response => response.json())
        .then(asistencia => {
            Promise.all([
                loadStudents(),
                loadCourses(asistencia.EstudianteID, 'editAsistenciaCourse')
            ]).then(() => {
                const editForm = document.getElementById("editAsistenciaForm");
                editForm.dataset.asistenciaId = asistencia.AsistenciaID;

                document.getElementById("editAsistenciaStudent").value = asistencia.EstudianteID;
                document.getElementById("editAsistenciaCourse").value = asistencia.CursoID;
                document.getElementById("editAsistenciaDate").value = asistencia.Fecha;
                document.getElementById("editAsistenciaState").value = asistencia.Estado;

                $('#editModal').modal('show');
            });
        })
        .catch(error => console.error('Error al cargar asistencia para edición:', error));
}

// Actualizar asistencia
function editAsistencia() {
    const asistenciaId = document.getElementById("editAsistenciaForm").dataset.asistenciaId;
    const asistenciaData = {
        AsistenciaID: asistenciaId,
        EstudianteID: document.getElementById("editAsistenciaStudent").value,
        CursoID: document.getElementById("editAsistenciaCourse").value,
        Fecha: document.getElementById("editAsistenciaDate").value,
        Estado: document.getElementById("editAsistenciaState").value
    };

    fetch(`${inscriptionApiUrl}/${asistenciaId}`, {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        },
        body: JSON.stringify(asistenciaData)
    })
        .then(response => response.json())
        .then(() => {
            loadAsistencias();
            $('#editModal').modal('hide');
        })
        .catch(error => console.error('Error al editar asistencia:', error));
}

// Mostrar modal de eliminación
function showDeleteModal(asistenciaId) {
    document.getElementById("deleteModal").dataset.asistenciaId = asistenciaId;
    $('#deleteModal').modal('show');
}

// Eliminar asistencia
function deleteAsistencia() {
    const asistenciaId = document.getElementById("deleteModal").dataset.asistenciaId;

    fetch(`${inscriptionApiUrl}/${asistenciaId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`  // Incluir el token en el encabezado
        }
    })
        .then(() => {
            loadAsistencias();
            $('#deleteModal').modal('hide');
        })
        .catch(error => console.error('Error al eliminar asistencia:', error));
}
