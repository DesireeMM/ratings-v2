const updateButtons = document.querySelectorAll('.edit-movie-rating');

for (const button of updateButtons) {
    button.addEventListener('click', () => {

        const newScore = prompt("What is your new rating?");
        const ratingID = button.id;
        const formInputs = {
            "rating_id": ratingID,
            "new_score": newScore
        }
        
        fetch('/update-ratings', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.text())
        .then(responseText => {
            const scoreHTML = document.querySelector(`#score_${ratingID}`);
            scoreHTML.innerHTML = newScore;
        })
    })
}