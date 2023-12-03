$(document).ready(function () {
  $("#actuals-table").hide();
});

$("#goal-selector").change(function () {
  $("#actuals-table").fadeIn();
});
