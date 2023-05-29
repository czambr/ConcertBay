
window.addEventListener('DOMContentLoaded', ()=> {
    const myToast = document.querySelector('.toast')
    console.log(myToast)
    if (myToast != null ) {
        console.log('dentro');
        const eventoToast = new bootstrap.Toast(myToast);
        eventoToast.show()
    }
})
