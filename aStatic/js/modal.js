// Mostrar el modal al cargar la página
$(document).ready(function() {
    $('#miModal').modal('show');
    
    // Cerrar el modal después de 5 segundos
    setTimeout(function() {
        $('#miModal').modal('hide');
    }, 1000);
});