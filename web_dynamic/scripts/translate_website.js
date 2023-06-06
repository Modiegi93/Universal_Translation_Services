document.getElementById('website-form').addEventListener('submit', function(event) {
  event.preventDefault();
  var websiteUrl = document.getElementById('website-input').value;
    
  fetch('/translations/website', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'website-input=' + encodeURIComponent(websiteUrl)
  })
  .then(response => response.text())
  .then(data => {
    // Update the translated content in your desired HTML element
    console.log(data);
  })
  .catch(error => console.error(error));
});
