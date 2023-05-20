$(document).ready(function() {
  $('#myForm').submit(function(e) {
    e.preventDefault(); // prevent the form from submitting normally

    // display the "kk.html" page for 5 seconds
    window.open('kk.html', '_blank');
    setTimeout(function() {
      // after 5 seconds, redirect to the "index.html" page
      window.location.href = '{{ url_for("index") }}';
    }, 5000);
  });
});