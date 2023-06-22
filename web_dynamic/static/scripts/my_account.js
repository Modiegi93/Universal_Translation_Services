$(document).ready(function() {
  const translationTable = document.getElementById('translationHistoryTable');
  const filterInput = document.getElementById('filterInput');

  filterInput.addEventListener('input', function () {
    const filterValue = filterInput.value.toLowerCase();
    // Loop through table rows and hide those that do not match the filter value
    for (let i = 1; i < translationTable.rows.length; i++) {
      const row = translationTable.rows[i];
      const sourceText = row.cells[1].textContent.toLowerCase();
      const translatedText = row.cells[2].textContent.toLowerCase();
      if (sourceText.includes(filterValue) || translatedText.includes(filterValue)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  });

  $("#History").on("click", function() {
    // Perform AJAX request to fetch translation history data
    $.ajax({
      url: "http://0.0.0.0:5010/translations_history",
      method: "GET",
      success: function(response) {
        // Populate the translation history table with the fetched data
        $("#translationHistoryTable").html(response);
      },
      error: function(xhr, status, error) {
        // Handle error case
        console.error(error);
      }
    });
  });
  // Handle click event for subscription buttons
  $(".price_button").on("click", function(event) {
    event.preventDefault();
    var url = $(this).attr("href");

    // Redirect to the corresponding signup page
    window.location.href = url;
  });
  // Handle form submission
  $("#Settings form").submit(function(event) {
    event.preventDefault();

    // Get form data
    var targetLanguages = $("#target-languages").val();
    var defaultLanguage = $("#default-language").val();

    // Prepare data for AJAX request
    var data = {
      target_languages: targetLanguages,
      default_language: defaultLanguage
    };

    // Perform AJAX request to save settings
    $.ajax({
      url: "http://0.0.0.0:5009/settings",
      method: "POST",
      data: data,
      success: function(response) {
        // Handle success case
        alert("Settings saved successfully!");
      },
      error: function(xhr, status, error) {
        // Handle error case
        console.error(error);
      }
    });
  });
   // Handle click event for subscription buttons
  $(".price_button").on("click", function(event) {
    event.preventDefault();
    var url = $(this).attr("href");

    // Redirect to the corresponding signup page
    window.location.href = url;
  });
});
