function logout() {
    // Eliminar el token de acceso (si está almacenado en localStorage)
    localStorage.removeItem('authToken');

    // Eliminar la información del usuario (si estaba almacenada en localStorage)
    localStorage.removeItem('usuario');


    // Redirigir al usuario a la página de inicio de sesión
    window.location.href = '../pages/login.html'; 
}
