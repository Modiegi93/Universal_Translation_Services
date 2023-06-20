function translateText() {
	// Retrieve the text to translate
	var textToTranslate = $('#textToTranslate').text().trim();

	// Check if there is text to translate
	if (textToTranslate.length === 0) {
	  $('#translatedOutput').text('No text provided');
	  return;
	}

	 // Retrieve the selected target language
	 var targetLanguage = $('#languageSelector').val();

	// Check if a target language is selected
	if (!targetLanguage) {
	  $('#translatedOutput').text('Select a target language');
	  return;
	}

	// Detect the source language using googletrans
	var sourceLanguage = googletrans.detect(textToTranslate).then(function(result) {
	  return result[0].lang;
	}).catch(function(error) {
	  console.log('Language detection error:', error);
	  return null;
	});
	
	// Translate the text to the target language using googletrans
	var translatedText = googletrans.translate(textToTranslate, { dest: targetLanguage }).then(function(result) {
	  return result.text;
	}).catch(function(error) {
	  console.log('Translation error:', error);
	  return null;
	});
	
	//Update the translated text in the output element
	$.when(sourceLanguage, translatedText).done(function(sourceLang, translatedText) {
	  if (sourceLang && translatedText) {
	    $('#translatedOutput').text(translatedText)
	  } else {
            $('#translatedOutput').text('Translation error');
          }
	});
      }
      
      function selectLanguage() {
	 // Clear the translated output when the language is changed
	 $('#translatedOutput').text('');
	}
