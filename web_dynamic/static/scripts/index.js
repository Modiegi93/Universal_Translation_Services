$(document).ready(function() {
    // Open sign-up modal when the "Sign Up" button is clicked
    $("#signupBtn").click(function() {
      $("#signupModal").css("display", "block");
    });

    // Close sign-up modal when the close button or outside the modal is clicked
    $(".close").click(function() {
      $("#signupModal").css("display", "none");
    });
    $(window).click(function(event) {
      if (event.target == $("#signupModal")[0]) {
        $("#signupModal").css("display", "none");
      }
    });

    // Handle sign-up form submission
    $("#signupForm").submit(function(event) {
      event.preventDefault();

      // Get the form data
      var fullName = $("#fullname").val();
      var email = $("#email").val();
      var password = $("#password").val();
      var repeatPassword = $("#repeatPassword").val();

      // Validate the form data
      if (fullName === "" || email === "" || password === "" || repeatPassword === "") {
        alert("Please fill in all fields");
        return;
      }

      if (password !== repeatPassword) {
        alert("Passwords do not match");
        return;
      }

      // Prepare data for AJAX request
      var data = {
        full_name: fullName,
        email: email,
        password: password,
        repeatPassword: repeatPassword
      };

      // Perform AJAX request to create a new user
      $.ajax({
        url: "http://0.0.0.0:5014/create_user",
        method: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(response) {
          // Handle success case
          console.log("User created successfully");
          // Redirect to the translations page
          window.location.href = "/translations";
        },
        error: function(xhr, status, error) {
          // Handle error case
          console.error(error);
        }
      });
    });
   // Open login modal when the "Login" button is clicked
    $("#loginBtn").click(function() {
      $("#loginModal").css("display", "block");
    });

    // Close login modal when the close button or outside the modal is clicked
    $(".close").click(function() {
      $("#loginModal").css("display", "none");
    });
    $(window).click(function(event) {
      if (event.target == $("#loginModal")[0]) {
        $("#loginModal").css("display", "none");
      }
    });

    // Handle login form submission
    $("#loginForm").submit(function(event) {
      event.preventDefault();

      // Get the form data
      var email = $("#email").val();
      var password = $("#password").val();

      // Validate the form data
      if (email === "" || password === "") {
        alert("Please fill in all fields");
        return;
      }

      // Prepare data for AJAX request
      var data = {
        email: email,
        password: password
      };

      // Perform AJAX request to authenticate the user
      $.ajax({
        url: "http://0.0.0.0:5013/login",
        method: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(response) {
          // Handle success case
          console.log("User logged in successfully");

          // Retrieve the user data
          $.ajax({
            url: "http://0.0.0.0:5012/api/v1/users",
            method: "GET",
            success: function(response) {
              // Handle user retrieval success
              console.log("User data retrieved successfully");
              console.log(response);
            },
            error: function(xhr, status, error) {
              // Handle user retrieval error
              console.error(error);
            }
          });

          // Redirect to the desired page
          window.location.href = "/dashboard";
        },
        error: function(xhr, status, error) {
          // Handle error case
          console.error(error);
        }
      });
    });
     $.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
	console.log(data);
	if (data.status === 'OK') {
		$('DIV#api_status').addClass('available');
	} else {
		$('DIV#api_status').removeClass('available');
	}
});

  });
