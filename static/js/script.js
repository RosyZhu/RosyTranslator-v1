document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('translationForm');
    const sourceLanguage = document.getElementById('sourceLanguage');
    const targetLanguage = document.getElementById('targetLanguage');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!inputText.value.trim()) {
            alert('Please enter text to translate');
            return;
        }

        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'text': inputText.value,
                'source_language': sourceLanguage.value,
                'target_language': targetLanguage.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            outputText.value = data.translation;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during translation. Please try again.');
        });
    });
});
