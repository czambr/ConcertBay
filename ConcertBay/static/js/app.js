
const card = document.querySelectorAll('.card')

card.forEach( (card) => {
    const cardSection = card.querySelector('.card-body')

    cardSection.addEventListener('mouseover', ()=>{
        cardDetail = cardSection.querySelector('.card-detail')
        cardDetail.classList.remove('d-none')
    });
    
    cardSection.addEventListener('mouseout', ()=>{
        cardDetail = cardSection.querySelector('.card-detail')
        cardDetail.classList.add('d-none')
    });
})

