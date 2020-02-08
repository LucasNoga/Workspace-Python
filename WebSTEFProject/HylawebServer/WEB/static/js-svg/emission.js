var hylaweb = hylaweb || {};
$(document).ready(function () {

    $('#emission').on('click', function () {
        window.location.href = "./tx"
    })
  
    $('#reception').on('click', function () {
        window.location.href ="./rx"
    })
});