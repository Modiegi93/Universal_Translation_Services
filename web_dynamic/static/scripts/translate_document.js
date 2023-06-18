function translateDocument() {
  var fileInput = document.getElementById('document-input');
  var file = fileInput.files[0];
  
  var formData = new FormData();
  formData.append('document-input', file);
  
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/translations/document', true);
  
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var translatedOutput = document.getElementById('translatedOutput');
      translatedOutput.textContent = xhr.responseText;
    }
  };
  
  xhr.send(formData);
}
