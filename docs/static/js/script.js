document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('translationForm');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!inputText.value.trim()) {
            alert('Please enter text to translate');
            return;
        }

        // Simulate translation (for demo purposes only)
        const simulateTranslation = (text) => {
            // This is a very simple simulation and doesn't actually translate
            return text.split('').reverse().join('') + ' (模拟翻译)';
        };

        try {
            const translatedText = simulateTranslation(inputText.value);
            outputText.value = translatedText;
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during translation simulation. Please try again.');
        }
    });
});
