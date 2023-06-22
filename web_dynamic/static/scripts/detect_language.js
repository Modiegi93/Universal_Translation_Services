function detectLanguage() {
  // Get the text to detect language from the input field
  var textToDetect = document.getElementById("textToTranslate").value;

  // Make a POST request to the API endpoint
  fetch('/translations/detect_language', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          text: textToDetect
      })
  })
  .then(response => response.json())
  .then(data => {
      // Display the detected language
      var detectedLanguage = data.detected_language;
      var outputElement = document.getElementById("output");
      outputElement.innerText = "Detected Language: " + detectedLanguage;
  })
  .catch(error => {
      console.log(error);
  });
}
