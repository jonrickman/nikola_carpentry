const stars = document.querySelectorAll('.star');
const ratingDisplay = document.getElementById('rating');

stars.forEach(star => {
    star.addEventListener('click', () => {
        const rating = star.getAttribute('data-value');
        ratingDisplay.value = rating;
        resetStars()
        document.querySelector('.stars').setAttribute('data-rating', rating);
    });
});

function resetStars() {
    const stars = document.querySelectorAll('.star');
    const ratingDisplay = document.getElementById('rating').value;

    stars.forEach(star => {
        star.classList.remove('active');

        if (star.getAttribute('data-value') <= ratingDisplay) {
            star.classList.add('active');
        }
    });
}