document.addEventListener("DOMContentLoaded", () => {
    loadCourses();  
    loadProfessors(); 
    loadAvailableCourses(); 

    const addForm = document.getElementById("addCourseForm");
    addForm.addEventListener("submit", function (event) { 
        if (!addForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            addCourse();
        }
        addForm.classList.add('was-validated');
    });
});

const token = localStorage.getItem('authToken');
const apiUrlProfessors = 'http://127.0.0.1:5000/profesores';
const apiUrlAssignedCourses = 'http://127.0.0.1:5000/profesores/cursos'; 

// Función para cargar los cursos ya asignados a los profesores
function loadCourses() {
    fetch(apiUrlAssignedCourses, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const courseList = document.getElementById("courseList");
        courseList.innerHTML = ''; 
        if (data.length > 0) {
            data.forEach(course => {
                courseList.innerHTML += `
                    <div class="contents-row d-flex" data-id="${course.CursoID}">
                        <div class="content-cell"><p>${course.ProfesorNombre}</p></div>
                        <div class="content-cell"><p>${course.CursoNombre}</p></div>
                        <div class="content-cell">
                            <button onclick="showDeleteModal(${course.ProfesorID}, ${course.CursoID})" class="btn btn-danger">Desasignar</button>
                        </div>
                    </div>`;
            });
        } else {
            courseList.innerHTML = '<p>No hay cursos asignados.</p>';
        }
    })
    .catch(error => console.error('Error al cargar los cursos asignados:', error));
}

// Función para cargar la lista de profesores en el select
function loadProfessors() {
    fetch(apiUrlProfessors, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const professorSelect = document.getElementById("addCourseProfessor");
        data.forEach(professor => {
            professorSelect.innerHTML += `
                <option value="${professor.ProfesorID}">${professor.Nombre} ${professor.Apellido}</option>
            `;
        });
    })
    .catch(error => console.error('Error al cargar los profesores:', error));
}

// Función para cargar los cursos disponibles en el select
function loadAvailableCourses() {
    fetch('http://127.0.0.1:5000/cursos', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const courseSelect = document.getElementById("addCourse");
        data.forEach(course => {
            courseSelect.innerHTML += `
                <option value="${course.CursoID}">${course.Nombre}</option>
            `;
        });
    })
    .catch(error => console.error('Error al cargar cursos disponibles:', error));
}

// Función para asignar un curso a un profesor
function addCourse() {
    const professorId = document.getElementById("addCourseProfessor").value;
    const courseId = document.getElementById("addCourse").value;

    const courseData = {
        CursoID: courseId
    };

    fetch(`http://127.0.0.1:5000/profesores/${professorId}/cursos`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(courseData)
    })
    .then(response => response.json())
    .then(() => {
        $('#addModal').modal('hide'); 
        loadCourses(); 
        clearModalFields(); 
    })
    .catch(error => console.error('Error al asignar curso:', error));
}

// Función para eliminar un curso asignado de un profesor
function deleteCourse(professorId, courseId) {
    fetch(`http://127.0.0.1:5000/profesores/${professorId}/cursos/${courseId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(() => {
        $('#deleteModal').modal('hide'); 
        loadCourses(); 
    })
    .catch(error => console.error('Error al desasignar curso:', error));
}

// Muestra el modal de eliminación
function showDeleteModal(professorId, courseId) {
    const deleteModal = document.getElementById("deleteModal");
    deleteModal.dataset.professorId = professorId;
    deleteModal.dataset.courseId = courseId;
    $('#deleteModal').modal('show');
}

// Función para limpiar los campos del formulario
function clearModalFields() {
    const addForm = document.getElementById("addCourseForm");
    addForm.reset();
    addForm.classList.remove('was-validated');
}

// Limpia el formulario al cerrar el modal de añadir curso
$('#addModal').on('hidden.bs.modal', function () {
    clearModalFields();
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
});
