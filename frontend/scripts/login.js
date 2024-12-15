const loginForm = document.getElementById('loginForm');

// Maneja el evento de envío del formulario
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault(); 

    // Captura los datos del formulario
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('login-message');
    
    try {
        // Realiza la petición al backend para iniciar sesión
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        // Maneja la respuesta del servidor
        if (response.ok) {
            // Si la respuesta es exitosa, almacena el token en localStorage
            localStorage.setItem('authToken', result.access_token); 
            
            // Almacena también la información del usuario (como nombre y rol)
            localStorage.setItem('usuario', JSON.stringify(result.usuario));
            
            window.location.href = '../pages/index.html'; 
        } else {
            // Si el login falla, muestra el error
            console.error( result.error );
            alert(result.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        console.error('Error al conectar con el servidor. Intenta nuevamente.');
    }
});
