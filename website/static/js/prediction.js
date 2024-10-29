// csrf token for predict
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// Predict Churn button
document.getElementById('predict-btn').addEventListener('click', function(event) {
    event.preventDefault();

    
    const customerId = this.getAttribute('customer-id');

    fetch(`/predict/${customerId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            
            document.getElementById('prediction-result').innerHTML = 
                `Prediction: ${data.prediction}<br>Probability of Churn: ${data.probability}%`;
            
            const progressBar = document.getElementById('progress-bar');
            progressBar.style.width = `${data.probability}%`; 
            progressBar.setAttribute('aria-valuenow', data.probability);
        } else {
            
            document.getElementById('prediction-result').innerText = `Error: ${data.message}`;
        }
    })
    .catch(error => {
        document.getElementById('prediction-result').innerText = `Error: ${error.message}`;
    });
});
