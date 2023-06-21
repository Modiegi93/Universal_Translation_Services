$(document).ready(function() {
    // Handle newsletter subscription form submission
    $(".newsletter-submit").click(function(event) {
      event.preventDefault();

      // Get the email address from the input field
      var email = $(".newsletter-input").val();

      // Check if the checkbox for daily newsletter is checked
      var isDailyNewsletter = $("#daily-newsletter").is(":checked");

      // Prepare data for AJAX request
      var data = {
        email: email,
        isDailyNewsletter: isDailyNewsletter
      };

      // Perform AJAX request to subscribe to the newsletter
      $.ajax({
        url: "http://0.0.0.0:5011/subscribe",
        method: "POST",
        data: data,
        success: function(response) {
          // Handle success case
          alert("Successfully subscribed to the newsletter!");
        },
        error: function(xhr, status, error) {
          // Handle error case
          console.error(error);
        }
      });
    });
  });
