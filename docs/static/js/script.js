document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('translationForm');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const fullAppLink = document.getElementById('fullAppLink');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!inputText.value.trim()) {
            alert('Please enter text to translate');
            return;
        }

        outputText.value = "This is a static demo. Translation functionality is not available here. Please visit the full application for actual translations.";
    });

    // Set the full application link
    fullAppLink.href = "https://rosy-translator.example.com";
});
