$(document).ready(function() {
    // Handle payment form submission
    $("#payment-form").submit(function(event) {
      event.preventDefault();

      // Get form data
      var cardNumber = $("#card-number").val();
      var expirationDate = $("#expiration-date").val();
      var cvv = $("#cvv").val();

      // Prepare data for AJAX request
      var data = {
        cardNumber: cardNumber,
        expirationDate: expirationDate,
        cvv: cvv
      };

      // Perform AJAX request to process payment
      $.ajax({
        url: "http://0.0.0.0:5000/process_payment",
        method: "POST",
        data: data,
        success: function(response) {
          // Handle success case
          alert("Payment successful!");
        },
        error: function(xhr, status, error) {
          // Handle error case
          console.error(error);
        }
      });
    });
