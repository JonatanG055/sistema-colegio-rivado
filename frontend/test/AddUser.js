const url = 'http://127.0.0.1:5000/usuarios';

// Añadir un nuevo usuario
const nuevoUsuario = {
    Nombre: 'Jonatan Elias',                // Nombre del usuario
    Apellido: 'Guevara',             // Apellido del usuario
    Email: 'jonatan@email.com',  // Email del usuario
    Username: 'jonatan123',         // Nombre de usuario (Username)
    PasswordHash: 'password', // La contraseña 
    Rol: 'admin',                   // Rol del usuario
    Estado: 'activo'  
};

// Configuración de la solicitud POST para crear el usuario
const opciones = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json' 
    },
    body: JSON.stringify(nuevoUsuario) 
};

// Realizamos la solicitud POST para crear el usuario
fetch(url, opciones)
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al crear el usuario: ' + response.statusText);
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Usuario creado exitosamente:', data);
    })
    .catch(error => {
        console.error('Hubo un problema con la creación del usuario:', error);
    });
