$(document).ready(function() {
    // About Us link
    $("a[href='http://0.0.0.0:5015/about_us']").click(function(event) {
      event.preventDefault();
      window.location.href = "http://0.0.0.0:5015/about_us";
    });

    // Translations link
    $("a[href='http://0.0.0.0:5016/translations']").click(function(event) {
      event.preventDefault();
      window.location.href = "http://0.0.0.0:5016/translations";
    });

    // Privacy&Terms link
    $("a[href='http://0.0.0.0:5017/privacy_terms']").click(function(event) {
      event.preventDefault();
      window.location.href = "http://0.0.0.0:5017/privacy_terms";
    });
    // My Account link
    $("a[href='http://0.0.0.0:5018/my_account']").click(function(event) {
      event.preventDefault();
      window.location.href = "http://0.0.0.0:5018/my_account";
    });

    // Logout link
    $("a[href='http://0.0.0.0:5019/logout']").click(function(event) {
      event.preventDefault();
      window.location.href = "http://0.0.0.0:5019/logout";
    });
  });
