function translateDocument() {
	var inputFile = document.getElementById("document-input").files[0];
	var sourceLanguage = document.getElementById("source-language").value;
	var targetLanguage = document.getElementById("target-lanaguage").value;

	var formData = new FormData();
	formData.append("file", inputFile);
	formData.append("sourceLanguage", sourceLanguage);
	formData.append("targetLanguage", targetLanguage);

	//Make an API call to translate the document
	//Replace 'API_ENDPOINT' with your actual API endpoint
	fetch('API_ENDPOINT', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		// Process the translated document
		// Replace 'download-link' with the ID of the download link element in your HTML
		var downloadLink = document.getElementById("download-link");
		downloadLink.href =data.translatedDocumentUrl;
		downloadLink.style.display = "block";
	})
	.catch(error => {
		console.error('Error:', error);
	});
}
