// Open feedback form
function openForm() {
  document.getElementById("myForm").style.display = "block";
}

// Close feedback form
function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

// Submit feedback form
function submitFeedback() {
  const feedback = document.getElementById("feedbackInput").value;

  // Send feedback to the server using an API request
  fetch('/feedback', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ feedback: feedback }),
  })
    .then(response => response.json())
    .then(data => {
      // Display success message or perform any desired actions
      console.log(data.message);
      // Clear the input field
      document.getElementById("feedbackInput").value = "";
      // Close the feedback form
      closeForm();
    })
    .catch(error => {
      // Handle error
      console.error('Error:', error);
    });
}
