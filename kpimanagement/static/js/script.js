$(document).ready(function () {
  $("#actuals-table").hide();
});

$("#goal-selector").change(function () {
  $("#actuals-table").fadeIn();
});

// Flash Message Fadeout Time
$(document).ready(function () {
  setTimeout(function () {
    $(".alert").alert("close");
  }, 3000);
});

// Clear Add Actual Form After Submit
document.body.addEventListener("htmx:afterOnLoad", function (evt) {
  if (evt.detail.successful) {
    // Assuming your form has an id 'myForm'
    document.getElementById("add-form").reset();
  }
});
