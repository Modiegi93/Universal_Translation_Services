// Function to populate language options
function populateLanguageOptions() {
  // Get the language selector element
  const languageSelector = document.getElementById('languageSelector');

  // Clear the language selector
  languageSelector.innerHTML = '';

  // Add the default option
  const defaultOption = document.createElement('option');
  defaultOption.value = '';
  defaultOption.disabled = true;
  defaultOption.selected = true;
  defaultOption.textContent = 'To language:';
  languageSelector.appendChild(defaultOption);

  // Get the list of supported languages
  const supportedLanguages = googletrans.LANGUAGES;

  // Add language options
  Object.entries(supportedLanguages).forEach(([languageCode, languageName]) => {
    const option = document.createElement('option');
    option.value = languageCode;
    option.textContent = languageName;
    languageSelector.appendChild(option);
  });
}

// Function to handle language selection
function selectLanguage() {
  // Get the selected language
  const selectedLanguage = document.getElementById('languageSelector').value;

  // Perform text translation
  translateText(selectedLanguage);
}

// Function to handle text translation
function translateText(targetLanguage) {
  // Get the text to translate
  const textToTranslate = document.getElementById('textToTranslate').textContent;

  // Translate the text
  const translatedText = googletrans.translate(textToTranslate, {
    to: targetLanguage,
  });

  // Display the translated text
  document.getElementById('translatedOutput').textContent = translatedText.text;
}

// Populate language options when the page loads
populateLanguageOptions();
