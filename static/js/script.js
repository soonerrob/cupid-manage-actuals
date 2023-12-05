$(document).ready(function () {
  $("#actuals-table").hide();
});

$("#goal-selector").change(function () {
  $("#actuals-table").fadeIn();
});

$(document).ready(function () {
  setTimeout(function () {
    $(".alert").alert("close");
  }, 3000);
});
