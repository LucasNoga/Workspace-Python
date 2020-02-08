
// Partie Emission
hylaweb = hylaweb || {}

hylaweb.emission = (function () {
    var self = {};

    self.user = {}

    self.hostRabbit = null

    var $list_agence = null
    var $user = null
    var $service_default = null
    var $agence = null

    self.init = function () {
        $list_agence = $('#liste-agence');
        $user = $('#utilisateur');
        $service_default = $('#service-default')
        $agence = $('#agence')
        self.FaxList.init();
        self.getInfosUser();
    }

    self.check_hylanotify = function () {
        var url_check = hylaweb.api.urls['check_hylanotify'];
        console.log(url_check)
        $.ajax({
            url: url_check,
            data: {
                login_ad: login
            }
        })
            .done(function (json) {
                console.log(json)
                if (json.status == "KO") {
                    console.log("Hylanotify pas lancé")
                    self.afficherNotif('delete', "Attention!!!<br/> Hylanotify n'est pas lancé", "red", true)
                }
                else if (json.status == "OK") {
                    console.log("Hylanotify lancé")

                    //TODO a mettre dans le stomp Recuperation de l'ip du server rabbit
                    self.hostRabbit = json.items.ipRabbit
                }
            })
            .fail(function () {
                console.log("API non disponible, Hylanotify pas lancé")
                self.afficherNotif('delete', "Attention!!!<br/> Hylanotify n'est pas lancé", "red", true)
            });
    }

    /**
     * Notification des actoins faites par l'utilisateur
     * @param {Icone} icon 
     * @param {Message de la notif} msg  
     * @param {couleur de l'icone} color 
     * @param {true=closable, false=unclosable} type
     */
    self.afficherNotif = function (icone, msg, color, type) {
        var $notif = $('#notif')
        var $text = $notif.find('span')
        var $icon = $notif.find('i')
        $text.html(msg)
        $icon.removeClass($icon.attr('class'))
        $icon.addClass(icone + " " + color + " " + "icon")
        $notif.modal({
            closable: type
        }).modal('show');
    }

    // retourne l'id service courant
    self.getIdServiceCurrent = function () {
        return $('#service-default').attr('idservice')
    }

    /**
     * Retourne les infos sur l'utilisateur
     */
    self.getInfosUser = function () {
        var url_user = hylaweb.api.urls['user']
        $.ajax({
            url: url_user,
            type: 'get'
        })
            .done(function (json) {
                self.user = json.items
                updateUser()
            });
    }

   

    /**
     *  rafraichit les fax et se reconnecte a rabbit si on a le focus de la window
     */
    self.focus = function () {
        vis(function () {
            if (vis()) {
                setTimeout(function () {
                    console.log("refresh liste service: " + self.getIdServiceCurrent())

                    //On rafraichit la liste des fax
                    //TODO a remettre self.FaxList.updateListFax(self.getIdServiceCurrent())

                    // On se reconnecte de la queue rabbit
                    //hylaweb.Rabbit.connect(self.hostRabbit, login, self.getIdServiceCurrent())
                }, 500);
            } else {
                //TODO a mettre hylaweb.Rabbit.disconnect()
            }
        });
    }
    return self;
})();

