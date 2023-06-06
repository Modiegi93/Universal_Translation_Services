document.getElementById('image-form').addEventListener('submit', function(event {
   event.preventDefault();
   var formData = new FormData(this);

  fetch('/translations/image', {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(data => {
    document.getElementById('translatedOutput').textContent = data;
  })
  .catch(error => console.error(error));
});
