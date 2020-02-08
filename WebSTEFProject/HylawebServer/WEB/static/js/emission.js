

var hylaweb = hylaweb || {}
// TODO faire la visualisation des infos en base emission et xferfaxlog
$(document).ready(function () {
    hylaweb.emission.init();

    hylaweb.focusEmission()

    // on recupere tous les fax
    hylaweb.lazy.init($('.column.left'), 'tx');
})

// Partie Emission
hylaweb.emission = (function () {
    var self = {};

    var id_service = null

    self.init = function () {
        // Recupere les infos sur le service par defaut du user
        self.getDefaultService();

        self.FaxList.init()

        // Connexion a rabbit
        hylaweb.Rabbit.connect(hylaweb.hostRabbit, hylaweb.session.login, self.getIdDefaultService())

        // Met a jour les fax avec l'id du service par defaut du user
        self.FaxList.updateListFax(self.getIdDefaultService())
    }

    /* Id de service par defaut du user */
    self.getIdDefaultService = function () {
        return $('#default-service').attr('idservice')
    }

    /**
     * recupere le service par defaut du user dans la BD
     */
    self.getDefaultService = function () {
        url_services = api.urls['services'].replace('#guid#', hylaweb.user.guid_ad)
        $.ajax({
            url: url_services,
            async: false,
            type: 'get'
        })
            .done(function (json) {
                var default_service = json.items.service_defaut
                //on conserve le service par défaut dans le check
                var content = default_service.agence + "  ---  " + default_service.service
                $('#default-service').text(content)
                $('#default-service').attr('idservice', default_service.serviceid).attr('idagence', default_service.id)
            })
    }

    /** Gestion des messages stomp pour les fax */
    self.traitementMessageWebSocket = function (message) {
        if (message.type == "TX-NEW") {
            // TODO si l'id existe deja on fait un update
            var fax = self.Fax.getFax(message.id)
            self.FaxList.AddPrependFax(fax)
        }

        else if (message.type == "TX-UPD") {
            var fax = self.Fax.getFax(message.id)
            self.Fax.updateFax(fax, true)
        }
    }
    return self;
})();

/**
 * Représente la liste des fax
 */
hylaweb.emission.FaxList = (function () {
    var self = {};
    var liste_fax

    self.init = function () {
        liste_fax = $('#liste-fax')
    }

    // retourne la liste de fax
    self.getItems = function () {
        return liste_fax.find('.fax.item')
    }

    // retourne le fax selectionné
    self.getFaxSelected = function () {
        return liste_fax.find('.fax.item.selected')
    }

    // Met a jour la liste
    self.updateListFax = function (id_service) {

        var url_tx_fax = api.urls['tx_fax'].replace("#id_serv#", id_service) + "/" + conf.LIMIT_TX_FAX
        $.ajax({
            url: url_tx_fax,
            type: 'get',
        })
            .done(function (json) {
                // on recupere l' id du fax selectionné
                id_fax_selected = self.getFaxSelected().attr('id-fax')
                // remise a zero de la liste des fax
                reset()
                $.each(json.items, function (i, fax) {
                    self.AddAppendFax(fax)
                });

                // transition sur l'icone si en cours d'envoi
                $('.final-status[data-status=TR]')
                    .transition('set looping')
                    .transition('pulse', "1000ms");

                // transition sur l'icone si elle est en cours d'envoi
                $('.process div.green[data-status=TR]')
                    .transition('set looping')
                    .transition('pulse', "1200ms");

                var div_error = $('div.warning')
                if (isEmpty()) {
                    div_error.removeClass('hidden')
                }
                else {
                    div_error.addClass('hidden')
                }
            });
    }

    /**
     * Ajoute un fax en début de liste
     */
    self.AddPrependFax = function (fax) {
        $fax = CreateFax(fax)
        liste_fax.prepend($fax)
        // On initialise l'objet fax
        hylaweb.emission.Fax.init($fax)
    }

    /**
     * Ajoute un fax en fin de liste
     */
    self.AddAppendFax = function (fax) {
        $fax = CreateFax(fax)
        liste_fax.append($fax)
        // On initialise l'objet fax
        hylaweb.emission.Fax.init($fax)
    }

    // Construit le fax pour l'affichage
    var CreateFax = function (fax) {
        return $(hylaweb.emission.Fax.createItem(fax))
    }

    /**
     * Retourne un booleen pour savoir si un fax existe dans la liste
     */
    var isEmpty = function () {
        return (self.getItems().length == 0)
    }

    /**
     * Vide la liste des fax
     */
    var reset = function () {
        $('#liste-fax').empty()
    }

    // Recupere l'id du fax par rapport a l'item
    self.getIdFax = function ($item) {
        return liste_fax.find($item).attr('id-fax')
    }

    return self;
})();


/**
 * Un fax
 */
hylaweb.emission.Fax = (function () {
    var self = {};

    self.init = function ($item) {
        var objfax = {}
        objfax.item = $item

        objfax.id = objfax.item.attr('id-fax')
        objfax.finalStatus = objfax.item.find('.final-status');
        objfax.sender = objfax.item.find('.nom-sender');
        objfax.dest = objfax.item.find('.nom-dest');

        objfax.filefax = objfax.item.find('.filefax');
        objfax.covernotes = objfax.filefax.find('.file.icon');
        objfax.coverobject = objfax.filefax.find(".coverobject")

        objfax.statusProcess = objfax.item.find('.process');
        objfax.undefined = objfax.statusProcess.find('.undefined')

        // icones d'actions
        objfax.actions = objfax.item.find('.actions-button')
        objfax.icons = objfax.actions.find('i');
        objfax.cancelSendingButton = objfax.actions.find('.cancel-sending');
        objfax.emitReportButton = objfax.actions.find('.emit-report');
        objfax.emitFaxButton = objfax.actions.find('.emit-fax');
        objfax.cancelSendingButton = objfax.actions.find('.cancel-sending');
        objfax.sendBackButton = objfax.actions.find('.send-back');
        objfax.showData = objfax.actions.find('.show-data');

        objfax.infos = objfax.item.find('.data-infos');
        addListener(objfax)
        addPopup(objfax);
    }

    /* ajoute les differentes popup au fax */
    var addPopup = function (objfax) {
        objfax.finalStatus.popup({
            position: "left center",
            setFluidWidth: false
        })

        // si le sujet de la page de garde est trop long
        if (isTooLong(objfax.coverobject)) {
            objfax.coverobject.popup({
                position: "bottom center",
                lastResort: true,
            })
        }

        objfax.covernotes.popup({
            position: "top center",
            lastResort: true
        })

        objfax.statusProcess.find('.active').popup({
            position: "top center",
        })
    }

    /**
     * fonction pour gerer le click sur un icon
     */
    var addListener = function (objfax) {
        // empeche le click sur le fax si on click sur les icones
        objfax.actions.on('click', function () {
            event.stopPropagation();
        });

        objfax.covernotes.on('click', function () {
            event.stopPropagation();
            console.log("redirection vers le fax")
        });

        // si le rapport d'emission existe
        if (emitReportExist(objfax)) {
            objfax.emitReportButton.on('click', function () {
                event.stopPropagation();
                displayEmitReport(objfax)
            })
        }
        else {
            objfax.emitReportButton.addClass('locked')
        }

        // si l'archive existe existe
        if (archiveExist(objfax)) {
            objfax.emitFaxButton.on('click', function () {
                event.stopPropagation();
                displayFax(objfax)
            })
        }
        else {
            objfax.emitFaxButton.addClass('locked')
        }

        // si on peut annuler le fax
        if (canCancelFax(objfax)) {
            objfax.cancelSendingButton.on('click', function () {
                $('#demande-annulation').modal({
                    onApprove: function ($element) {
                        cancelFax(objfax.id)
                    },

                    // creation du message
                    onShow: function () {
                        $(this).find('.contenu').text("Êtes-vous sûr de vouloir annuler le fax destiné à " + objfax.dest.text()
                            + " (jobid = " + getInfosFax(objfax).jobid + ") ?")
                    }
                }).modal('show');
            })
        }
        else {
            objfax.cancelSendingButton.addClass('locked')
        }

        // si on peut renvoyer
        if (canSendBack(objfax)) {
            objfax.sendBackButton.on('click', function () {

                $('#demande-renvoi').modal({
                    onApprove: function ($element) {
                        sendBackFax(objfax.id)
                    },

                    // creation du message
                    onShow: function () {
                        $(this).find('.contenu').html("Êtes-vous sûr de vouloir renvoyer le fax <br/> à " + objfax.dest.text() + " au " + objfax.dest.attr('num-dest') + " ?")
                    }
                }).modal('show');
            })
        }
        else {
            objfax.sendBackButton.addClass('locked')
        }

        // affichage des donnees techniques
        objfax.showData.on('click', function () {
            displayTechnicalData(objfax)
        });

        objfax.item.hover(
            function () {
                objfax.undefined.css('background-color', '#eaeaea')
                objfax.icons.css('color', 'black');
            }, function () {
                objfax.undefined.css('background-color', 'white')
                objfax.icons.removeAttr('style')
            }
        );
    }

    // affiche les donnees technique du fax
    var displayTechnicalData = function (objfax) {
        if (objfax.infosFax.is(":visible")) {
            var meta = objfax.item.find('.meta span, .meta i, .meta .blue.small.label')
            meta.show()
            objfax.infosFax.hide()
        }
        else {
            var meta = objfax.item.find('.meta span, .meta i, .meta .blue.small.label')
            meta.hide()
            objfax.infosFax.css('display', 'inline-block')
            objfax.infosFax.show()
        }
    }

    /**
    * retourne true si le fax selectionné est selectionne
    */
    var isSelected = function (objfax) {
        return objfax.item.hasClass('selected')
    }

    // retourne true si le rapport d'emission existe
    var emitReportExist = function (objfax) {
        return objfax.statusProcess.find('div[data-status=EM]').hasClass('green')
    }

    // retourne true si l'archive existe
    var archiveExist = function (objfax) {
        return objfax.statusProcess.find('div[data-status=AR]').hasClass('green')
    }

    // verifie si un jobid est renseigné, l'id de l'utilisateur et que l'utilisateur n'est pas un user generique
    var canCancelFax = function (objfax) {
        return getInfosFax(objfax).jobid != "null" && getInfosFax(objfax).jobid != "undefined"
            && objfax.sender.attr('id-util') == hylaweb.getUserId()
            && hylaweb.userIsGeneric() == 0
            && getStatusFax(objfax) != "OK" && getStatusFax(objfax) != "ER" && getStatusFax(objfax) != "AN"
    }

    // Verifie si on peut renvoyer un fax
    var canSendBack = function (objfax) {
        return objfax.sender.attr('id-util') == hylaweb.getUserId()
            && hylaweb.userIsGeneric() == 0
            && archiveExist(objfax)
            && (getStatusFax(objfax) == "OK" || getStatusFax(objfax) == "ER")
    }

    // Affichage du fax 
    var displayFax = function (objfax) {
        var url = encodeURIComponent(api.urls['archive_file']
            .replace("#type_fax#", 'TX')
            .replace("#idFax#", objfax.item.attr('id-fax'))
            .replace("#format#", "pdf") + "?guid=" + hylaweb.user.guid_ad)
        window.open("../static/pdfjs/web/viewer.html?file=" + url, 'emissionFax');
    }

    // affichage du rapport d'emission
    var displayEmitReport = function (objfax) {
        var url = encodeURIComponent(api.urls['archive_file']
            .replace("#type_fax#", 'TX')
            .replace("#idFax#", objfax.item.attr('id-fax'))
            .replace("#format#", "pdf") + "?guid=" + hylaweb.user.guid_ad + "&type=rapport")
        window.open("../static/pdfjs/web/viewer.html?file=" + url, 'RapportEmission');
    }

    /**
    * retourne true si la valeur present dans l'item a etet tronqué (destinataire, expediteur, sujet de page de garde)
    */
    var isTooLong = function (item) {
        //verifie si l'item existe
        if (item.length != 0)
            return item.text().length < item.attr('data-content').length
        return false;
    }

    // fonction qui retourne les infos du fax
    var getInfosFax = function (objfax) {
        var info = {}
        $.each(objfax.infos.find('div[data][type]'), function () {
            info[$(this).attr('type')] = $(this).attr('data')
        })
        return info
    }

    // retourne le status du fax
    var getStatusFax = function (objfax) {
        return objfax.finalStatus.attr('data-status')
    }

    /** retourne les infos du fax en base en json a partir de son id */
    self.getFax = function (id) {
        var jsonfax
        var url_get_fax_tx = api.urls['get_fax_tx'].replace('#id_fax#', id)
        $.ajax({
            url: url_get_fax_tx,
            type: 'get',
            async: false,
        })
            .done(function (json) {
                // Si le fax est bien recuperé
                if (json.status == "OK") {
                    Logger.info("fax ayant l'id " + json.items.id + ": ", json.items)
                    jsonfax = json.items
                }
                else {
                    Logger.debug(json.description)
                }
            });
        return jsonfax
    }

    // appel a l'api pour annuler un fax
    var cancelFax = function (id) {
        var url = api.urls.cancel_fax_emit.replace('#id_fax#', id)
        $.ajax({
            url: url,
            type: 'POST',
        })
            .done(function (json) {
                // Si le fax est bien recuperé
                if (json.status == "OK") {
                    Logger.debug(json.description)
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }

    // appel api pour renvoyer un fax
    var sendBackFax = function (id) {
        var url = api.urls.send_back_fax.replace('#id_fax#', id)
        console.log(url)

        // appel send avec les donnes
        $.ajax({
            url: url,
            data: {
                guid: hylaweb.user.guid_ad,
            },
            type: 'POST',
        })
            .done(function (json) {
                // Si le fax est bien recuperé
                if (json.status == "OK") {
                    Logger.debug(json.description)
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }


    /**
    * Mise a jour des donnees du fax selectionner
    * @param {fax au format json} fax
    */
    self.updateFax = function (fax, transition) {
        var oldfax = $('#liste-fax .item[id-fax="' + fax.id + '"]')

        // on verifie si le fax est chargé
        if (fax.id >= hylaweb.emission.FaxList.getIdFax($('#liste-fax .fax.item:last'))) {
            var newfax = self.createItem(fax)
            // On initialise l'objet fax
            self.init(newfax)

            //Si l'ancien fax était selectionné, on selectionne le nouveau
            if (oldfax.hasClass("selected"))
                newfax.addClass("selected");

            oldfax.replaceWith(newfax)
            // animation pour l'update d'un fax
            if (transition)
                newfax.transition('glow');

            // transition sur l'icone si en cours d'envoi (Status = TR)
            console.log('1', newfax.find('.final-status[data-status=TR]'))
            console.log('2', newfax.find('.process > div.active[data-status=TR]'))
            newfax.find('.final-status[data-status=TR]')
                .transition('set looping')
                .transition('pulse', "1000ms");

            newfax.find('.process > div.active[data-status=TR]')
                .transition('set looping')
                .transition('pulse', "1200ms");
        }
    }

    // Construit le fax pour l'affichage
    self.createItem = function (fax) {
        $fax = $("<div id-fax=\"" + fax.id + "\"class=\"item fax\"></div>")

        // on creer le status courant
        $fax.append(createStatus(fax))
        $fax.append(createContent(fax))

        // on met a jour le status du process par rapport au statut final
        updateStatus($fax, fax.status)
        return $fax
    }

    var updateStatus = function ($fax, status) {
        $process = $fax.find('.process')
        // on recherche le status du fax a ciblé
        var $statusProcess = $process.find("div[data-status=\"" + status + "\"]")

        // si le status est different de null et qu'il n'existe pas il est indefini
        if (status != null && $statusProcess.length == 0)
            $statusProcess = $process.find("div[data-status=IND]")

        switch (status) {
            case "TR":
                $statusProcess.addClass("sprite download green").removeClass("grey")
                break;

            // envoi en différé
            case "DE":
                $statusProcess.addClass("sprite clock orange").removeClass("grey")
                break;

            case "OK":
                $statusProcess.addClass("sprite ok").removeClass("grey undefined")
                break;

            case "ER":
                $statusProcess.addClass("sprite delete").removeClass("grey undefined")
                break;

            default:
                $statusProcess.removeClass("circle loading")
        }
    }

    // recupere la couleur du status
    var getColorStatus = function (status) {
        switch (status) {
            // envoi en différé
            case "DE":
                return "orange"

            case "OK":
                return "green"

            case "ER":
                return "red"

            // cas TR, AN, null
            default:
                return "grey"
        }
    }

    // creation de la date du fax
    var createDate = function (fax) {
        var $labelDate = $("<span class=\"ui label date " + getColorStatus(fax.status) + "\"></span>")//</span>"

        // creer l'objet date
        switch (fax.status) {
            case "TR":
                $labelDate.text("Fax soumis le : " + getDateFaxWithSecond(fax.datetime))
                break;

            // envoi en différé
            case "DE":
                // on verifie si la date du procchain envoi est renseigné sinon on prend la date differe
                if (fax.date_next_send != null)
                    $labelDate.text("Prochain envoi : " + getDateFaxWithSecond(fax.date_next_send))
                else
                    $labelDate.text("Prochain envoi : " + getDateFaxWithSecond(fax.datetime_dif))
                break;
            case "OK":
                $labelDate.text("Envoyé le : " + getDateFaxWithSecond(fax.date_envoi))
                break;

            case "ER":
                $labelDate.text("Echec de l'envoi le : " + getDateFaxWithSecond(fax.date_envoi))
                break;

            // cas null
            default:
                $labelDate.text("Fax soumis le : " + getDateFaxWithSecond(fax.datetime))
                break;
        }
        return $labelDate
    }

    // on creer le status courant
    var createStatus = function (fax) {
        $status = $(" <div class=\"image\"></div>")

        // TODO remplacer par currentstatus
        $icon = $("<i class=\"final-status icon huge\"></i>")
        // Traitement du status du fax
        var icon = ""
        var status = ""
        var popupContent = ""
        var displayedDate = ""
        var popupTitle = ""
        var popupContent = ""
        var addClass = ""
        switch (fax.status) {
            case "TR":
                status = "TR"
                icon = "double angle right"
                addClass = "sprite download green"
                popupTitle = "Envoi en cours"
                popupContent = getSimplifyDateFax(fax.datetime)
                break;

            // envoi en différé
            case "DE":
                // on verifie si la date du procchain envoi est renseigné sinon on prend la date differe
                if (fax.date_next_send != null)
                    popupContent = getSimplifyDateFax(fax.date_current_send)

                else
                    popupContent = "Soumis " + getSimplifyDateFax(fax.datetime)

                status = "DE"
                icon = "outline clock"
                addClass = "sprite clock orange"
                popupTitle = "Envoi différé "
                break;

            case "OK":
                status = "OK"
                icon = "check"
                addClass = "sprite ok"
                popupContent = "le transfert a été effectué"
                popupTitle = "Succès de l'envoi"
                popupContent = getSimplifyDateFax(fax.date_envoi)
                break;

            case "ER":
                status = "ER"
                icon = "delete"
                addClass = "sprite delete"
                popupContent = "le transfert a échoué"
                popupTitle = "Echec de l'envoi "
                popupContent = getSimplifyDateFax(fax.date_envoi)
                break;

            // dans le cas d'une annulation de fax
            case "AN":
                status = "AN"
                icon = "help"
                popupTitle = "Annulation du fax "
                popupContent = getSimplifyDateFax(fax.datetime)
                break;

            default:
                status = "null"
                icon = "notched circle loading"
                popupTitle = "Soumission du fax "
                popupContent = getSimplifyDateFax(fax.datetime)
        }

        //Si dès le depart c'est un envoi differé on n'inscrit pas le nombre de tentatives, ou demande d'annulation du fax
        if ((fax.status != "DE" || fax.nb_envoi != 0) && fax.status != "AN") {
            var nb_envoi = fax.nb_envoi == 0 ? nb_envoi = 1 : nb_envoi = fax.nb_envoi
            var tentative = nb_envoi == 1 ? "essai " : "essais "
            tentative += nb_envoi + "/" + fax.dials
            popupTitle += " (" + tentative + ")"
        }
        // mise en valeur du status courant
        $icon.addClass("active " + icon + ' ' + getColorStatus(status))
            .attr('data-status', fax.status).attr('data-title', popupTitle).attr('data-content', popupContent)
        $status.append($icon)

        return $status
    }

    // creation du contenu
    var createContent = function (fax, color) {
        $content = $("<div class=\"top aligned content\"></div>")

        // si pas de nom de destinataire on met son numero
        var dest = fax.dest == null ? fax.numdest : fax.dest
        var sender = fax.sendername == null ? fax.sendername : fax.sendername

        $header = $("<div class=\"header\">"
            + "         <span num-dest=\"" + fax.numdest + "\" class=\"nom-dest\">" + dest + "</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            + "</div>"
            + "<span>de</span>&nbsp;<span id-util=\"" + fax.id_util + "\" class=\"nom-sender\">" + sender + "</span>"
        )
        $actions = $("<div class=\"ui right floated content action\"></div>")
            .append(createProcess(fax)).append(createDate(fax)).append("<br/><div class=\"actions-button\">"
            + " <i class=\"emit-fax file outline icon\" title=\"Visualiser le fax\"></i>"
            + " <i class=\"emit-report  file outline alternate icon\" title=\"Visualiser le rapport d'émission\"></i>"
            + " <i class=\"cancel-sending cancel icon\" title=\"Annuler l'envoi du fax \"></i>"
            + " <i class=\"send-back reply icon\" title=\"Renvoyer le fax\"></i>"
            + "</div>")

        var coverPage = ""
        // test si le sujet de la page de garde est renseigné
        if (fax.coversubject != null && fax.coversubject != "") {
            // on tronque le sujet de page de garde si trop long
            var coverobject = fax.coversubject.length > 25 ? fax.coversubject.substring(0, 22) + "..." : fax.coversubject
            coverPage = "<span coverpage=\"" + fax.coverpage + "\" faxname=\"" + fax.filename + "\""
                + " class=\"filefax ui grey label\">"
                + "    <i class=\"file icon\" data-content=\"" + fax.covernotes + "\"></i>"
                + "    <span class=\"coverobject\" data-content=\"" + fax.coversubject + "\">Sujet: " + coverobject + "</span>"
                + "</span></span>"
        }

        var tagList = ""
        // Si on a des tags on les ajoute
        if (fax.tag.length != 0) {
            for (var index_tag in fax.tag) {
                var tag = fax.tag[index_tag]
                // Si le tag n'est pas vide
                if (tag != "")
                    tagList += "<div class=\"ui blue small label\">" + tag + "</div>"
            }
        }

        var page = (fax.npages == null || fax.npages == 0) ? page = "" :
            fax.npages == 1 ? page = "1 page" : page = fax.npages + " pages"

        $meta = $("<div class=\"meta\">"
            + "<span class=page>" + page + "</span>&nbsp;&nbsp;&nbsp;&nbsp;"
            + "<i class=\"tags icon\"></i>" + tagList + coverPage
        )

        $content.append($header).append($actions).append($meta).append(createTechnicalData(fax))

        return $content
    }

    // on creer la liste des status
    var createProcess = function (fax) {

        // etape du processus d'envoi
        $process = $("<div class=\"process\">"
            + "  <div data-status=\"DE\" data-content=\"En attente d'émission\" class=\"clock grey sprite\"> </div> "
            + "  <div data-status=\"TR\" class=\"download grey sprite\"> </div> "
            + "  <div data-status=\"IND\" class=\"undefined\"> </div>"
            + "  <div data-status=\"EM\" class=\"sprite rapport grey\"></div>"
            + "  <div data-status=\"AR\" class=\"sprite archive grey\"></div>"
            + "</div>")

        // si le rapport d'emission existe 
        if (fax.ndoc_arc != null) {
            $process.find("div[data-status=AR]")
                .addClass("active green")
                .removeClass("grey")
                .attr('data-content', "Fax archivé")
        }

        // si le rapport d'archivage existe 
        if (fax.ndoc_rap != null) {
            $process.find("div[data-status=EM]")
                .addClass("active green")
                .removeClass("grey")
                .attr('data-content', "Rapport d'émission créé")
        }
        return $process
    }

    // Creation des infos technique pour le debuggage
    var createTechnicalData = function (fax) {
        $infos = $("<div class=\"data-infos ui label\">"
            + "         <div type=\"id\" data=\"" + fax.id + "\" class=\"data-fax ui small label \">ID: " + fax.id + " </div>"
            + "         <div type=\"commid\" data=\"" + fax.commid + "\" class=\"data-fax ui small label\">Commid: " + fax.commid + "</div>"
            + "         <div type=\"jobid\" data=\"" + fax.jobid + "\" class=\"data-fax ui small label\">Jobid: " + fax.jobid + "</div>"
            + "         <div type=\"jobtime\" data=\"" + fax.jobtime + "\" class=\"data-fax ui small label\">Jobtime: " + fax.jobtime + "</div>"
            + "         <div type=\"id-server\" data=\"" + fax.id_server + "\" class=\"data-fax ui small label\">ID serveur: " + fax.id_server + "</div>"
            + "         <div type=\"ndoc-arc\" data=\"" + fax.ndoc_arc + "\" class=\"data-fax ui small label\">doc archive: " + fax.ndoc_arc + "</div>"
            + "         <div type=\"ndoc-rap\" data=\"" + fax.ndoc_rap + "\" class=\"data-fax ui small label\">doc rapport EM: " + fax.ndoc_rap + "</div>"
            + "         <div type=\"modem\" data=\"" + fax.modem + "\" class=\"data-fax ui small label\">Transfert: " + fax.modem + "</div>"
            + "</div>")

        return $infos
    }

    return self;
})();