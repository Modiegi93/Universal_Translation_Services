$(document).ready(function() {
      // AJAX request to get supported languages
  $.get("http://localhost:5002/api/v1/supported_languages", function(data) {
    // Iterate over the languages and populate the dropdown
    $.each(data, function(code, name) {
      var option = $("<option>").val(code).text(name + " - (" + code + ")");
      $("#languageSelector").append(option);
    });
  });

   $(".detect-button").click(function() {
    var button = $(this);
    
    // Disable the button and show the loading state
    button.prop("disabled", true).text("Loading...");
    
    // Get the input text
    var text = $("#input-text").val();

   // Check if input text is empty
   if (text === "") {
    	alert("Please enter some text.");
    	button.prop("disabled", false).text("Detect Language");
    	return;
  }	
    
    // Make a POST request to the detect language endpoint
    $.ajax({
      url: "http://localhost:5003/api/v1/detect",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ text: text }),
      success: function(response) {
        // Enable the button and restore the original text
        button.prop("disabled", false).text("Detect Language");
        
        // Update the output with the detected language result
        $("#output").text("Detected language: " + response.language);
      },
      error: function(xhr, status, error) {
        // Enable the button and restore the original text
        button.prop("disabled", false).text("Detect Language");
        
        // Handle the error response
        var errorMessage = xhr.responseJSON.error || "Language detection failed.";
        $("#output").text("Error: " + errorMessage);
      }
    });
  });
function translateText() {
  var inputText = $("#textToTranslate").text();
  var targetLang = $("#languageSelector").val();
  var button = $(".translate-button");

  if (!inputText && !targetLang) {
    alert("Please provide text to translate and select a target language.");
    return;

  } else if (!inputText) {
    alert("Please provide text to translate.");
    return;

  } else if (!targetLang) {
    alert("Please select a target language.");
    return;
  }

  // Disable the button and show the loading state
  button.prop("disabled", true).text("Loading...");

  // Send the translation request to the server
  $.ajax({
    url: "http://localhost:5004/api/v1/texts",
    type: "POST",
    data: JSON.stringify({
      text: inputText,
      target_lang: targetLang
    }),
    contentType: "application/json",
    success: function(response) {
      // Enable the button and restore the original text
      button.prop("disabled", false).text("Translate");

      // Update the translated output
      var translatedText = response.translated_text;
      $("#translatedOutput").text(translatedText);
    },
    error: function(jqXHR, textStatus, errorThrown) {
      // Handle the error case
      button.prop("disabled", false).text("Translate");

      // Show an error message
      alert("Translation failed. Error: " + textStatus);
    }
  });
}

function translateText() {
  var button = $(".translate-button");
  var fileInput = $("#file-input")[0];
  var targetLang = $("#languageSelector").val();

  // Check if target language is selected
  if (!targetLang) {
    alert("Please select a target language.");
    return;
  }

  // Check if a file is selected
  if (fileInput.files.length > 0) {
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append("file", file);
    formData.append("target_lang", targetLang);

    // Show the name of the loaded file
    $(".file-upload-description").text("File loaded: " + file.name);

    // Disable the button and show the loading state
    button.prop("disabled", true).addClass("loading");

    // Send the translation request to the server
    $.ajax({
      url: "http://localhost:5005/api/v1/documents",
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      success: function(response) {
        // Enable the button and restore the original text
        button.prop("disabled", false).removeClass("loading");

        // Update the translated output
        var translatedText = response.translated_text;
        $("#translatedOutput").text(translatedText);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        // Handle the error case
        button.prop("disabled", false).removeClass("loading");

        // Show an error message
        alert("Translation failed. Error: " + textStatus);
      }
    });
  } else {
    // No file selected, show an error message
    alert("Please upload a file.");
  }
}

// Add hover effect to the translate button
  $(".translate-button").hover(
    function() {
      $(this).addClass("hover");
    },
    function() {
      $(this).removeClass("hover");
    }
  );

  // Handle file selection
  $("#file-input").change(function() {
    var file = $(this).prop("files")[0];

    // Show the name of the loaded file
    $(".file-upload-description").text("File loaded: " + file.name);
  });

  // Handle translate button click
  $(".translate-button").click(function() {
    // Check if a file is uploaded
    if ($("#file-input").get(0).files.length === 0) {
      alert("Please upload an image file.");
      return;
    }

     // Check if a target language is selected
     var targetLang = $("#languageSelector").val();
     if (!targetLang) {
       alert("Please select a target language.");
       return;
    }

    // Disable the button and show the loading status
    $(this).prop("disabled", true).addClass("loading");

    // Perform translation or other logic
    var file = $("#file-input").prop("files")[0];
    var targetLang = $("#languageSelector").val();

    var formData = new FormData();
    formData.append("file", file);
    formData.append("target_lang", targetLang);

    $.ajax({
      url: "http://localhost:5006/api/v1/images",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        // Handle the response
        console.log(response);

        // Enable the button and remove the loading status
        $(".translate-button").prop("disabled", false).removeClass("loading");

        // Reset the file upload description
        $(".file-upload-description").text("Upload image (png, jpg, or jpeg)");
      },
      error: function(xhr, status, error) {
        // Handle the error
        console.error(error);

        // Enable the button and remove the loading status
        $(".translate-button").prop("disabled", false).removeClass("loading");

        // Reset the file upload description
        $(".file-upload-description").text("Upload image (png, jpg, or jpeg)");
      }
    });
  });

// Add hover effect to the button
$('.website-translation-button').hover(function() {
  $(this).css('background', 'rgb(30, 88, 120)');
}, function() {
  $(this).css('background', 'rgb(20, 68, 100)');
});

// Handle website translation button click
$('#website-form').submit(function(event) {
  event.preventDefault();
  var url = $('#website-input').val();
  var targetLang = $('#languageSelector').val(); // Get the selected target language

  if (!url) {
    alert('Please enter a website URL.');
    return;
  }

  if (!targetLang) {
    alert('Please select a target language.');
    return;
  }

  var requestData = {
    url: url,
    target_lang: targetLang
  };

  // Send the translation request to the server
  $.ajax({
    url: 'http://localhost:5007/api/v1/websites',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(requestData),
    success: function(response) {
      var websiteId = response.website_id;
      // Redirect to the website translation page with the website ID
      window.open('http://localhost:5006/translate?website_id=' + websiteId, '_blank');
    },
    error: function(xhr, status, error) {
      // Handle the error response
      console.error(xhr.responseText);
    }
  });
});
});
