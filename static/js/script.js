document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('translationForm');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!inputText.value.trim()) {
            alert('Please enter English words to translate');
            return;
        }

        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'text': inputText.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            outputText.innerHTML = `
                <p><strong>Chinese Translation:</strong> ${data.translation}</p>
                <p><strong>Example Sentence:</strong> ${data.example_sentence}</p>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during translation. Please try again.');
        });
    });
});
