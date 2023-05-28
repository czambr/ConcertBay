
let calcularPrecio = () => {
    let ticketsComprados = document.getElementById("ticketsComprados");                                          // Tickets Comprados por el usuario
    const precioTicket_string = document.getElementById("precioConcierto").getAttribute("data-valor-precio");    // Precio del Concierto
    const precioTicket = parseFloat(precioTicket_string.replace(',', '.'))                                       
    const ticketsDiponibles_string = document.getElementById("entradasDisponibles").getAttribute("data-valor-num-ticket");
    const ticketsDiponibles = parseInt(ticketsDiponibles_string);                                                // Numero de Tickets Disponibles     
    let totalCompra = document.getElementById("totalCompra");                                                    // Etiqueta que contiene el de la compra

    ticketsComprados.addEventListener ( 'change', () => {
        if ( ticketsComprados.value <= ticketsDiponibles ) {
            totalCompra.innerHTML = `$ ${(precioTicket * ticketsComprados.value).toFixed(2)}`
        };   
    })
};

window.addEventListener('DOMContentLoaded', () => { 
    calcularPrecio()  // Calculo de la compra 
});