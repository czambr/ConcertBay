
const card = document.querySelectorAll('.card')
let ids_card = [];
card.forEach(cardItem => ids_card.push(cardItem.id));
ids_card.forEach( id_concert => {
    const cardElement = document.getElementById(id_concert);
    cardElement.addEventListener('mouseover', ()=>{
        cardDetail = cardElement.querySelector('.card-detail')
        cardDetail.classList.remove('d-none')
        cardElement.classList.remove('border-0')
        cardElement.classList.add('border-2')
        cardElement.classList.add('shadow-lg')
    })
    cardElement.addEventListener('mouseout', ()=>{
        cardDetail = cardElement.querySelector('.card-detail')
        cardElement.classList.remove('border-2')
        cardElement.classList.remove('shadow-lg')
        cardDetail.classList.add('d-none')
        cardElement.classList.add('border-0')
    })
})

