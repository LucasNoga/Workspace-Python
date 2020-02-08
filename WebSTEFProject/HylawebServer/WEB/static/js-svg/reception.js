var hylaweb = hylaweb || {};
$(document).ready(function () {
    // TODO faire une fonction add_agence et add_service
    // TODO mettre la methode focus dans hylaweb

    hylaweb.reception.init();

    // Verifie HylaNotify est lancé
    hylaweb.check_hylanotify()

    // verifie si on a le focus
    hylaweb.focus();

    $('#emission').on('click', function () {
        window.location.href = "./tx"
    })

    $('#reception').on('click', function () {
        window.location.href = "./rx"
    })

    // Automatically shows on init if cookie isnt set
    $('.cookie.nag').nag({
            key: 'accepts-cookies',
            value: true
        });
});
