// Obtener la información del usuario desde localStorage
const usuario = JSON.parse(localStorage.getItem('usuario'));


if (usuario) {
    // Mostrar los datos del usuario en la interfaz
    document.getElementById('account-info-name').innerText = usuario.nombre + ' ' + usuario.apellido;
    
} else {
    console.log('No hay datos.');
    window.location.href = '../pages/404.html';
}