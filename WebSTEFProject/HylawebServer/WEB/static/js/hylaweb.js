var hylaweb = hylaweb || {};

$(document).ready(function () {
    hylaweb.init();
});

hylaweb = (function () {
    self.user = {}

    self.hostRabbit = null

    self.queueSys = null

    self.init = function () {

        // On creer la bar de navigation
        hylaweb.NavBar.init();

        //Recuperation des donnees du user
        getInfosUser();

        // Verifie si HylaNotify est lancé
        checkHylaNotify()

        //Envoi du message rabbit pour le chamgement de service par defaut
        $('#check-default-service').on('click', function () {
            if (!$('#check-default-service').hasClass('disabled'))
                self.changeService()
        })
    }

    // Verifie si le user est connecté a rabbit
    self.isConnected = function () {
        return self.queueSys != null && self.hostRabbit != null
    }

    //Envoi du message rabbit pour le chamgement de service par defaut
    self.changeService = function () {
        var url_services = api.urls['services'].replace('#guid#', hylaweb.session.guid)
        $.ajax({
            url: url_services,
            async: false,
            type: 'post',
            data: {
                service_defaut: $('#service-current').attr('idservice'),
                hostRabbit: hylaweb.hostRabbit,
                queueSys: decodeURI(hylaweb.queueSys),
            }
        })
            .done(function (json) {
                if (json.status = "OK") {
                    console.log('mis a jour du service')
                    $('#check-default-service i').addClass('green')
                    $('#check-default-service').addClass('disabled')
                    $('#check-default-service').attr('id-service', json.items.idService)
                }
                else {
                    console.log(json)
                    Logger.error('Impossible de changer votre service par defaut')
                }
            })
            .fail(function () {
                Logger.error("Erreur requete")
            });
    }

    //Affiche l'aide
    self.displayHelp = function () {
        $('.help.ui.modal').modal({
            centered: false,
            onShow: function () {
                $(this).find('iframe').attr('src', '../static/pdfjs/web/viewer.html?file=../../Notice_Utilisateur_Hylafax_WEB.pdf');
            },
            onHidden: function () {
                $(this).find('iframe').attr('src', '');
            }
        }).modal('show')
    }

    self.getUserId = function(){
        return self.user.id
    }

    // reotourne true si le user est un utilisateur generique
    self.userIsGeneric = function(){
        return self.user.util_gen
    }

    /**
    * Retourne les infos sur l'utilisateur, Appel synchrone pour effectuer correctement les traitements par la suite
    */
    var getInfosUser = function () {
        var url_user = api.urls['user'].replace('#guid#', hylaweb.session.guid)
        $.ajax({
            url: url_user,
            async: false,
            type: 'get'
        })
            .done(function (json) {
                self.user = json.items
                updateUser()
            });
    }

    // Met a jour le champ de l'utilisateur et sa photo
    var updateUser = function () {
        $('#utilisateur').text(self.user.prenom + " " + self.user.nom.toUpperCase())
        var initial = self.user.prenom.charAt(0) + self.user.nom.charAt(0)
        var url_get_avatar = api.urls['get_avatar'].replace("#initial#", initial).replace('#mail#', self.user.mail).replace('#key#', self.user.nom)
        $('#img-user').replaceWith('<img id="img-user" src="' + url_get_avatar + '">')
    }

    // retourne l'id service courant
    self.getIdServiceCurrent = function () {
        return $('#service-current').attr('idservice')
    }

    // Recupere le tableau des services de l'agence du user
    self.getServicesDefault = function () {
        var agence_name = $('#agence').text()
        var agence = $('#liste-agence .item:contains(' + agence_name + ')').find('a').clone()
        var services = []
        $.each(agence, function (i, service) {
            services[i] = { 'name': $(service).text(), 'value': $(service).attr('idservice') }
        });
        return services
    }

    /**
    *  Rafraichit les fax et se reconnecte a rabbit si on a le focus de la window
    */
    self.focusReception = function () {
        vis(function () {
            if (vis()) {
                setTimeout(function () {
                    Logger.debug("Reconnexion à Rabbit")
                    Logger.debug("Update service: " + hylaweb.getIdServiceCurrent())

                    $(document).attr('title', ":: Hylafax ::")
                    $("#favicon").attr("href", "/static/icon/icon.png");

                    //On rafraichit la liste des fax
                    self.reception.FaxList.updateListFax(self.getIdServiceCurrent())

                    // On se reconnecte de la queue rabbit
                    hylaweb.Rabbit.connect(self.hostRabbit, hylaweb.session.login, self.getIdServiceCurrent())
                }, 500);
            } else {
                try {
                    Logger.debug("Déconnexion de rabbit")
                    hylaweb.Rabbit.disconnect()
                } catch (error) {
                    Logger.error(error)
                }
            }
        });
    }
    /*
   *  Reconnexion a rabbit si on a le focus de la window
   */
    self.focusEmission = function () {
        vis(function () {
            if (vis()) {
                setTimeout(function () {
                    // On se reconnecte de la queue rabbit
                    Logger.debug("Reconnexion à Rabbit")
                    hylaweb.Rabbit.connect(self.hostRabbit, hylaweb.session.login, self.emission.getIdDefaultService())

                    //On rafraichit la liste des fax en emision
                    Logger.debug("refresh de la liste")
                    self.emission.FaxList.updateListFax(self.emission.getIdDefaultService())

                }, 500);
            } else {
                try {
                    Logger.debug("Déconnexion de rabbit")
                    hylaweb.Rabbit.disconnect()
                } catch (error) {
                    Logger.error(error)
                }
            }
        });
    }

    /**
     * Verifie que HylaNotify est lancé sur le post de l'utilisateur et 
     * retourne l'host rabbit sur lequel la queue WEB doit se connecter
     * Appel Synchrone
     */
    checkHylaNotify = function () {
        var url_check = api.urls['check_hylanotify'];
        // reinitialisation des données
        self.hostRabbit = null
        self.queueSys = null
        $.ajax({
            url: url_check,
            async: false,
            data: {
                login_ad: hylaweb.session.login,
            }
        })
            .done(function (json) {
                if (json.status == "KO") {
                    console.log("Hylanotify pas lancé")
                    hylaweb.afficherNotif('delete', "Attention, HylaNotify n'est pas demarré sur votre PC !<br/>Pour disposer de l'ensemble des fonctionnalités, veuillez démarrer HylaNotify.", "red", true)
                    self.hostRabbit = null
                    self.queueSys = null
                }
                else if (json.status == "OK") {
                    Logger.debug("Hylanotify lancé")
                    self.hostRabbit = json.items.HostRabbit
                    self.queueSys = decodeURI(json.items.QueueSystem)
                    Logger.debug('Queue rabbit', self.queueSys)
                }
            })
            .fail(function () {
                Logger.error("API non disponible, Hylanotify pas lancé")
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
        addEvents()
    }

    var activatePopup = function () {
        $('#sidebar .item').popup({
            position: 'right center',
            delay: {
                show: 200,
            }
        });
    }

    var addEvents = function () {
        $('#tx').on('click', function () {
            window.location.href = "./tx"
        })

        $('#rx').on('click', function () {
            window.location.href = "./rx"
        })

        $('#arc').on('click', function () {
            window.location.href = "./archive"
        })

        $('#newFax').on('click', function () {
            window.open("./send/new", 'newFax')
        })
        
        
        /* $('#carnet').on('click', function () {
            window.location.href = "./book"
        }) */

        $('#aide').on('click', function () {
            hylaweb.displayHelp()
        });

    }
    return self;
})();

// Menu pour la liste des services
hylaweb.MenuServices = (function () {
    var self = {};

    // TODO faire une fonction add_agence et add_service lors de l'ajout dans le dropdown
    // Recupere les services de l'utilisateur
    self.CreateMenu = function (json) {
        var $list_agence = $('#liste-agence')
        var url_services = api.urls['services'].replace('#guid#', hylaweb.user.guid_ad)
        $.ajax({
            url: url_services,
            async: false,
            type: 'get'

        })
            .done(function (json) {
                var default_service = json.items.service_defaut

                //on conserve le service par défaut dans le check
                $('#check-default-service').attr('id-service', default_service.serviceid)

                var $service_current = $('#service-current')
                var $agence = $('#agence')
                $service_current.text(default_service.service)
                $service_current.attr('idService', default_service.serviceid)
                $agence.text(default_service.agence)
                $agence.attr('code-agence', default_service.code)

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
                        $service = $("<a code-agence=\"" + service["code-agence"] + "\" agence=\"" + agence.agence + "\" idservice=\"" + service.serviceid + "\" class=\"item\">" + service.service + "</a>")
                        var $list_service = $list_agence.find('[id-agence=' + id_agence + '] .menu')
                        $list_service.append($service)
                        hylaweb.Service.init($service)
                    });
                });

                // Active le dropdown pour les services 
                $('#dropdown-service').dropdown();
            })
    }
    return self;
})();


hylaweb.Service = (function () {
    var self = {};
    self.$service = null
    self.init = function ($service) {
        self.$service = $service

        self.$service.on('click', function () {
            hylaweb.reception.updateService($(this).text(), $(this).attr('idservice'), $(this).attr('agence'), $(this).attr('code-agence'))

            hylaweb.reception.FaxList.getItems().removeClass('selected')

            //Popup pour le changement de service par defaut
            $('#check-default-service').popup({
                html: "Choisir <b> " + $('#agence').text() + "</b> : <b>" + $('#service-current').text() + " </b>comme service par défaut",
                position: 'right center',
                inline: true,
                variation: 'small',
                delay: {
                    show: 200,
                },
                onShow: function () {
                    // Affiche uniquement la popup si le bouton est disponible
                    return (!$('#check-default-service').hasClass('disabled'))
                }
            })

            // si c'est le service par defaut on bloque la checkbox
            if (serviceIsDefault($(this).attr('idservice'))) {
                Logger.debug('service par defaut selectionné')
                $('#check-default-service i').addClass('green')
                $('#check-default-service').addClass('disabled')
            }

            //sinon on supprime la classe verte et on rend la checkbox accessible
            else {
                Logger.debug('autre service selectionné')
                $('#check-default-service i').removeClass('green')
                $('#check-default-service').removeClass('disabled')
            }
        })
    }

    // Verifie si le service selectionné est le service par defaut
    var serviceIsDefault = function (id_current) {
        var id_default = $('#check-default-service').attr('id-service')
        return id_default == id_current;
    }

    return self;
})();

