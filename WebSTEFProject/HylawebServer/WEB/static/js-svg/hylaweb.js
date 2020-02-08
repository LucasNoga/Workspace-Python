$(document).ready(function () {
    hylaweb.init();
});

hylaweb = (function () {

    self.user = {}
    var $user = null
    var $img_user = null

    self.init = function () {
        $user = $('#utilisateur');
        $img_user = $('#img-user')
        $('#aide').on('click', function () {
            hylaweb.displayHelp()
        });

        //self.NavBar.init()

        //on recupere le guid du user
        self.getInfosUser();
    }

    //Affiche l'aide
    self.displayHelp = function () {
        $('.help.ui.modal').modal({
            centered: false
        }).modal('show')
    }

    /**
    * Retourne les infos sur l'utilisateur
    */
    self.getInfosUser = function () {
        var url_user = hylaweb.api.urls['user'].replace('#guid#', hylaweb.session.guid)
        $.ajax({
            url: url_user,
            type: 'get'
        })
            .done(function (json) {
                self.user = json.items
                updateUser()

                // On creer le menu des services et des agences
                self.MenuServices.CreateMenu();

                // On creer la bar de navigation
                self.NavBar.init();
            });
    }

    // Met a jour le champ de l'utilisateur et sa photo
    var updateUser = function () {
        $user.text(self.user.prenom + " " + self.user.nom.toUpperCase())
        var initial = self.user.prenom.charAt(0) + self.user.nom.charAt(0)
        var url_get_avatar = hylaweb.api.urls['get_avatar'].replace("#initial#", initial).replace('#mail#', self.user.mail).replace('#key#', self.user.nom)
        $img_user.replaceWith('<img id="img-user" src="' + url_get_avatar + '"></div>')
    }

    // retourne l'id service courant
    self.getIdServiceCurrent = function () {
        return $('#service-default').attr('idservice')
    }

    /**
    *  rafraichit les fax et se reconnecte a rabbit si on a le focus de la window
    */
    self.focus = function () {
        vis(function () {
            if (vis()) {
                setTimeout(function () {
                    console.log("Reconnexion à Rabbit")
                    console.log("Update service: " + hylaweb.getIdServiceCurrent())

                    //On rafraichit la liste des fax
                    self.reception.FaxList.updateListFax(self.getIdServiceCurrent())

                    // On se reconnecte de la queue rabbit
                    hylaweb.Rabbit.connect(self.hostRabbit, hylaweb.session.login, self.getIdServiceCurrent())
                }, 500);
            } else {
                console.log("deconnexion de rabbit")
                hylaweb.Rabbit.disconnect()
            }
        });
    }

    self.check_hylanotify = function () {
        var url_check = hylaweb.api.urls['check_hylanotify'];
        $.ajax({
            url: url_check,
            data: {
                login_ad: hylaweb.session.login
            }
        })
            .done(function (json) {
                if (json.status == "KO") {
                    console.log("Hylanotify pas lancé")
                    hylaweb.afficherNotif('delete', "Attention!!!<br/> Hylanotify n'est pas lancé", "red", true)
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

    return self;
})();


// gestion de la barre de navigation 
hylaweb.NavBar = (function () {
    var self = {};

    self.init = function () {
        activatePopup()

    }

    var activatePopup = function () {
        console.log($('#sidebar .item'))
        $('#sidebar .item').popup({
            position: 'bottom center',
            delay: {
                show: 200,
            }
        });
    }

    return self;
})();

// Menu pour la liste des services
hylaweb.MenuServices = (function () {
    var self = {};

    // Recupere les services de l'utilisateur
    self.CreateMenu = function (json) {
        var $list_agence = $('#liste-agence')
        var url_services = hylaweb.api.urls['services'].replace('#guid#', hylaweb.user.guid_ad)
        $.ajax({
            url: url_services,
            type: 'get'
        })
            .done(function (json) {
                var default_service = json.items.service_defaut

                var $service_default = $('#service-default')
                var $agence = $('#agence')
                $service_default.text(default_service.service)
                $service_default.attr('idService', default_service.serviceid)
                $agence.text(default_service.agence)

                // On affiche les fax correspondants au service par defaut de l'utilisateur
                hylaweb.reception.FaxList.updateListFax(hylaweb.getIdServiceCurrent())

                // on se connecte a Rabbit
                hylaweb.Rabbit.connect(hylaweb.reception.hostRabbit, hylaweb.session.login, hylaweb.getIdServiceCurrent())

                // Parcourt des agences
                $.each(json.items.agences, function (i, agence) {
                    $list_agence.append($("<div id-agence=\"" + agence.id + "\"class=\"ui dropdown item\">"
                        + agence.agence
                        + "<i class=\"dropdown icon\"></i>"
                        + "<div class=\"menu\">"
                        + "</div></div>"))

                    var id_agence = agence.id

                    // Parcourt des services par agence
                    $.each(agence.services, function (i, service) {
                        $service = $("<a agence=\"" + agence.agence + "\" idservice=\"" + service.serviceid + "\" class=\"item\">" + service.service + "</a>")
                        var $list_service = $list_agence.find('[id-agence=' + id_agence + '] .menu')
                        $list_service.append($service)
                        hylaweb.Service.init($service)
                    });
                });
            });

        // Active le dropdown pour les services
        $('#dropdown-service').dropdown();
    }
    return self;
})();


hylaweb.Service = (function () {
    var self = {};
    self.$service = null
    self.init = function ($service) {
        self.$service = $service
        addEvents()
    }

    addEvents = function () {
        self.$service.on('click', function () {
            hylaweb.reception.updateService($(this).text(), $(this).attr('idservice'), $(this).attr('agence'))
        })
    }

    return self;
})();

