/** definit un nombre random */
function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

/**
 * Definit une couleur de maniere random
 */
function getRandomColor(){
    var colors = ["red", "orange", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown", "grey", "black"]
    return colors[getRandomInt(colors.length)]
}

/**
 * Retourne la date pour un fax
 * @param {*} date 
 */
function getDateFax(date){
    moment.locale('fr');
    return moment(date).format("llll");
}

/**
 * Retourne la date avec les seconds pour un fax
 * @param {*} date 
 */
function getDateFaxWithSecond(date){
    moment.locale('fr');
    return moment(date).format('DD/MM/YYYY') + " à "+ moment(date).format('HH:mm:ss');
}

function getSimplifyDateFax(date){
    moment.locale('fr');
    return "le " + moment(date).format('DD/MM/YYYY') + " à "+ moment(date).format('HH:mm');
}

/** Teste si un onglet a le focus
 * lien du code: 
 * https://greensock.com/forums/topic/9059-cross-browser-to-detect-tab-or-window-is-active-so-animations-stay-in-sync-using-html5-visibility-api/ 
 */
var vis = (function () {
    var stateKey,
        eventKey,
        keys = {
            hidden: "visibilitychange",
            webkitHidden: "webkitvisibilitychange",
            mozHidden: "mozvisibilitychange",
            msHidden: "msvisibilitychange"
        };
    for (stateKey in keys) {
        if (stateKey in document) {
            eventKey = keys[stateKey];
            break;
        }
    }
    return function (c) {
        if (c) document.addEventListener(eventKey, c);
        return !document[stateKey];
    }

    // check if browser window has focus		
    var notIE = (document.documentMode === undefined),
        isChromium = window.chrome;

    if (notIE && !isChromium) {

        // checks for Firefox and other  NON IE Chrome versions
        $(window).on("focusin", function () {

            // tween resume() code goes here
            setTimeout(function () {
                console.log("focus");
            }, 300);

        }).on("focusout", function () {

            // tween pause() code goes here
            console.log("blur");

        });

    } else {

        // checks for IE and Chromium versions
        if (window.addEventListener) {

            // bind focus event
            window.addEventListener("focus", function (event) {

                // tween resume() code goes here
                setTimeout(function () {
                    console.log("focus");
                }, 300);

            }, false);

            // bind blur event
            window.addEventListener("blur", function (event) {

                // tween pause() code goes here
                console.log("blur");

            }, false);

        } else {

            // bind focus event
            window.attachEvent("focus", function (event) {

                // tween resume() code goes here
                setTimeout(function () {
                    console.log("focus");
                }, 300);

            });

            // bind focus event
            window.attachEvent("blur", function (event) {

                // tween pause() code goes here
                console.log("blur");

            });
        }
    }
})();
