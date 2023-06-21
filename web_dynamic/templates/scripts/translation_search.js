$(document).ready(function() {
    // Handle search form submission
    $("#search-form").submit(function(event) {
      event.preventDefault();

      // Get the search query from the input field
      var searchQuery = $(".search-input").val();

      // Prepare data for AJAX request
      var data = {
        keyword: searchQuery
      };

      // Perform AJAX request to search
      $.ajax({
        url: "http://0.0.0.0:5000/api/v1/search",
        method: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(response) {
          // Handle success case
          if (response.length > 0) {
            // Process search results
            response.forEach(function(result) {
              console.log("Found translation: ", result);
              // Do something with each search result
            });
          } else {
            console.log("No results found");
            // Handle no search results case
          }
        },
        error: function(xhr, status, error) {
          // Handle error case
          console.error(error);
        }
      });
    });
  });
