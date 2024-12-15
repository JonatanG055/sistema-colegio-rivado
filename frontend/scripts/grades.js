// URLs de las APIs
const gradeApiUrl = 'http://127.0.0.1:5000/calificaciones';
const studentApiUrl = 'http://127.0.0.1:5000/api/estudiantes';
const courseApiUrl = 'http://127.0.0.1:5000/cursos';

document.addEventListener("DOMContentLoaded", () => {
    loadGrades();

    const addForm = document.getElementById("addGradeForm");
        addForm.addEventListener("submit", function(event) {
            // Previene el envío del formulario si no es válido
            if (!addForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                addGrade();
            }
    
            // Marca el formulario como validado
            addForm.classList.add('was-validated');
        });
});

// Obtener el token de localStorage
const token = localStorage.getItem("authToken");

// Cargar estudiantes en los select de los modales
function loadStudents() {
    return fetch(studentApiUrl, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        }
    })
        .then(response => response.json())
        .then(data => {
            const addSelect = document.getElementById("addGradeStudent");
            const editSelect = document.getElementById("editGradeStudent");

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
function loadCourses(estudianteId) {
    if (!estudianteId) {
        // Si no hay estudiante seleccionado, vaciar los selects
        const addSelect = document.getElementById("addGradeCourse");
        const editSelect = document.getElementById("editGradeCourse");

        addSelect.innerHTML = '<option value="">Seleccione un curso</option>';
        editSelect.innerHTML = '<option value="">Seleccione un curso</option>';
        return;
    }

    // Llamada a la API para obtener cursos inscritos por el estudiante
    return fetch(`http://127.0.0.1:5000/inscripciones/estudiantes/${estudianteId}/cursos`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        }
    })
        .then(response => response.json())
        .then(data => {
            const addSelect = document.getElementById("addGradeCourse");
            const editSelect = document.getElementById("editGradeCourse");

            addSelect.innerHTML = '<option value="">Seleccione un curso</option>';
            editSelect.innerHTML = '<option value="">Seleccione un curso</option>';

            data.forEach(course => {
                const option = `<option value="${course.CursoID}">${course.Nombre}</option>`;
                addSelect.innerHTML += option;
                editSelect.innerHTML += option;
            });
        })
        .catch(error => console.error('Error al cargar cursos:', error));
}

// Cargar lista de calificaciones
function loadGrades() {
    fetch(gradeApiUrl, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        }
    })
        .then(response => response.json())
        .then(data => {
            const gradeList = document.getElementById("gradeList");
            gradeList.innerHTML = '';
            data.forEach(grade => {
                gradeList.innerHTML += `
                    <div class="contents-row d-flex" data-id="${grade.CalificacionID}">
                        <div class="content-cell"><p>${grade.NombreEstudiante}</p></div>
                        <div class="content-cell"><p>${grade.NombreCurso}</p></div>
                        <div class="content-cell"><p>${grade.Nota}</p></div>
                        <div class="content-cell">
                            <button onclick="showEditModal(${grade.CalificacionID})" class="btn btn-warning mr-2">Editar</button>
                            <button onclick="showDeleteModal(${grade.CalificacionID})" class="btn btn-danger">Eliminar</button>
                        </div>
                    </div>`;
            });
        })
        .catch(error => console.error('Error al cargar calificaciones:', error));
}

// Llamar a la función de cargar estudiantes y cursos al abrir el modal
$('#addModal').on('show.bs.modal', function () {
    loadStudents(); // Cargar estudiantes

    // Obtener el estudiante seleccionado y cargar sus cursos
    const selectedStudentId = document.getElementById("addGradeStudent").value;
    loadCourses(selectedStudentId); // Cargar cursos para el estudiante seleccionado
});

// Modificar la función que maneja el cambio de estudiante en el select
document.getElementById("addGradeStudent").addEventListener("change", function () {
    const selectedStudentId = this.value;
    loadCourses(selectedStudentId); // Cargar los cursos del estudiante seleccionado
});

// Añadir calificación
function addGrade() {
    const gradeData = {
        EstudianteID: document.getElementById("addGradeStudent").value,
        CursoID: document.getElementById("addGradeCourse").value,
        Nota: document.getElementById("addGradeScore").value
    };

    fetch(gradeApiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        },
        body: JSON.stringify(gradeData)
    })
        .then(response => response.json())
        .then(() => {
            loadGrades();
            $('#addModal').modal('hide');
        })
        .catch(error => console.error('Error al añadir calificación:', error));
}

// Mostrar modal de edición
function showEditModal(calificacionID) {
    fetch(`${gradeApiUrl}/${calificacionID}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        }
    })
        .then(response => {
            if (!response.ok) throw new Error('Error al obtener la calificación');
            return response.json();
        })
        .then(calificacion => {
            if (!calificacion) throw new Error('No se encontró la calificación');

            // Cargar estudiantes y cursos asociados
            Promise.all([
                loadStudents(), // Cargar estudiantes
                loadCourses(calificacion.EstudianteID) // Cargar cursos del estudiante
            ]).then(() => {
                // Rellenar los campos del formulario de edición
                const editForm = document.getElementById("editGradeForm");
                editForm.dataset.calificacionId = calificacion.CalificacionID;

                document.getElementById("editGradeStudent").value = calificacion.EstudianteID;
                document.getElementById("editGradeCourse").value = calificacion.CursoID;
                document.getElementById("editGradeScore").value = calificacion.Nota;

                // Mostrar el modal después de cargar todos los datos
                $('#editModal').modal('show');
            }).catch(error => console.error('Error al cargar datos para editar:', error));
        })
        .catch(error => console.error('Error al cargar la calificación para editar:', error));
}


// Actualizar calificación
function editGrade() {
    const calificacionId = document.getElementById("editGradeForm").dataset.calificacionId;
    const gradeData = {
        CalificacionID: calificacionId,
        EstudianteID: document.getElementById("editGradeStudent").value,
        CursoID: document.getElementById("editGradeCourse").value,
        Nota: document.getElementById("editGradeScore").value
    };

    fetch(`${gradeApiUrl}/${calificacionId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        },
        body: JSON.stringify(gradeData)
    })
        .then(response => response.json())
        .then(() => {
            loadGrades();
            $('#editModal').modal('hide');
        })
        .catch(error => console.error('Error al editar la calificación:', error));
}

// Mostrar modal de eliminación
function showDeleteModal(calificacionId) {
    document.getElementById("deleteModal").dataset.calificacionId = calificacionId;
    $('#deleteModal').modal('show');
}

// Eliminar calificación
function deleteGrade() {
    const calificacionId = document.getElementById("deleteModal").dataset.calificacionId;

    fetch(`${gradeApiUrl}/${calificacionId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Agregar token a las cabeceras
        }
    })
        .then(response => response.json())
        .then(() => {
            $('#deleteModal').modal('hide');
            loadGrades();
        })
        .catch(error => console.error('Error al eliminar calificación:', error));
}
