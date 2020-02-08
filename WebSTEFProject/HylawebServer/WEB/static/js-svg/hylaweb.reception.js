
// Partie Reception
hylaweb = hylaweb || {}

hylaweb.reception = (function () {
    var self = {};

    self.hostRabbit = null

    var $list_agence = null

    var $service_default = null
    var $agence = null


    self.init = function () {
        $list_agence = $('#liste-agence');
        $service_default = $('#service-default')
        $agence = $('#agence')

        self.FaxList.init();
    }

    // Met a jour le libelle du service selectionné et les fax correspondant puis on affiche les fax correspondant a ce service
    self.updateService = function (service, id_service, agence) {
        $service_default.text(service)
        $service_default.attr('idService', id_service)
        $agence.text(agence)

        // On cache le pdf qui est affiché
        self.Pdf.hidePDF()

        // On affiche les fax correspondants au service par defaut de l'utilisateur
        self.FaxList.updateListFax(hylaweb.getIdServiceCurrent())

        // Mise a jour de la queue Rabbit
        hylaweb.Rabbit.subscribe(hylaweb.session.login, hylaweb.getIdServiceCurrent());
    }

    self.traitementMessageReception = function (message) {
        // verifie le type de message
        console.log('passage 1', message)
        if (message.type == "RX-NEW") {
            self.FaxList.AddPrependFax(message)
            //TODO animation
        }

        else if (message.type == "RX-UPD") {
            self.Fax.updateFax(message.id)
        }
    }

    return self;
})();

hylaweb.reception.Pdf = (function () {
    var self = {};

    /**
     * Enleve le pdf qui est affiché
     */
    self.hidePDF = function () {
        var $pdf = $('#pdf')
        $pdf.attr('src', '')
    }

    return self;
})();

/**
 * Représente la liste des fax
 */
hylaweb.reception.FaxList = (function () {
    var self = {};
    var liste_fax

    //TODO garder l'id du fax selectionner 
    self.init = function () {
        liste_fax = $('#fax')
    }

    self.updateListFax = function (id_service) {
        var url_rx_fax = hylaweb.api.urls['rx_fax'].replace("#id_serv#", id_service)
        $.ajax({
            url: url_rx_fax,
            type: 'get',
        })
            .done(function (json) {

                // remise a zero de la liste des fax
                reset()
                $.each(json.items, function (i, fax) {
                    self.AddAppendFax(fax)
                });
                selectFirstFax();
            });

    }

    /**
     * Ajoute un fax en début de liste
     */
    self.AddPrependFax = function (fax) {
        // On initialise l'objet fax puis on l'ajoute en tete de liste
        liste_fax.prepend(self.CreateFax(fax))
    }

    /**
     * Ajoute un fax en fin de liste
     */
    self.AddAppendFax = function (fax) {
        // On initialise l'objet fax puis on l'ajoute en tete de liste
        liste_fax.append(self.CreateFax(fax))
    }

    self.CreateFax = function (fax) {
        var baliseAvatar = ""
        var baliseTag = ""

        //Test si le proprietaire existe
        if (fax.proprietaire == "" || fax.proprietaire == undefined) {
            baliseAvatar = '<div class="ui circular image avatar"><img src="../static/images/lock.png"></div>'
        }
        else {
            var initial = fax.proprietaire.split(" ")[0].charAt(0) + fax.proprietaire.split(" ")[1].charAt(0)
            var mail = fax.proprietaire.split(" ")[2]
            var name = fax.proprietaire.split(" ")[1]
            var key = name
            var data_prop = fax.proprietaire.split(" ")[0] + " " + fax.proprietaire.split(" ")[1]
            if (mail != undefined) {
                mail = fax.proprietaire.split(" ")[2].replace('<', '').replace('>', '')
            }
            else {
                mail = ""
            }

            var url_get_avatar = hylaweb.api.urls['get_avatar'].replace("#initial#", initial).replace('#mail#', mail).replace('#key#', key)
            baliseAvatar = '<div data-prop="' + data_prop + '" class="ui circular image avatar locked"><img src="' + url_get_avatar + '"></div>'
        }

        // Si on a des tags on les ajoute
        if (fax.tag.length != 0) {
            for (var index_tag in fax.tag) {
                var tag = fax.tag[index_tag]
                // Si le tag n'est pas vide
                if (tag != "")
                    baliseTag += "<div class=\"ui blue small label\">" + tag + "</div>"
            }
        }

        $fax = $("<div id-fax=\"" + fax.id + "\"class=\"item\">"
            + "<div class=\"selector\"></div>"
            + baliseAvatar
            + "<div class=\"content\">"
            + "    <a class=\"header\">" + fax.sender + "</a>"
            + "    <div class=\"ui right floated content\">" + getDateFax(fax.datetime)
            + "    </div>"
            + "    <div class=\"meta\">"
            + "        <span>" + fax.npages + " Pages</span>&nbsp&nbsp&nbsp&nbsp"
            + "        <i class=\"tags icon\"></i>"
            + baliseTag
            + "        <i class=\"large plus square icon\"></i>"
            + "       <div class=\"ui right floated content action\">"
            + "           <i class=\"trash alternate outline icon\"></i>"
            + "       </div>"
            + "   </div>"
            + "</div></div>")


        // On initialise l'objet fax puis on l'ajoute en tete de liste
        hylaweb.reception.Fax.init($fax)
        return $fax
    }

    //TODO fusionner selectFirstFax et SelectFax
    /**
     * Selectionne le premier fax de la liste
     */
    var selectFirstFax = function () {
        if (existsFax()) {
            liste_fax.find('.item:first-child').trigger('click')
        }
    }

    self.selectFax = function ($item) {
        if (existsFax()) {
            liste_fax.find($item).trigger('click')
        }
    }

    /**
     * Retourne un booleen pour savoir si un fax existe dans la liste
     */

    // modifié par Philippe
    var existsFax = function () {
        return ($('#fax .item').length > 0)
    }

    //TODO reset de facon smooth la liste avec un fade voir sur internet
    /**
     * Vide la liste des fax
     */
    var reset = function () {
        liste_fax = $('#fax')
        $('#chargement').find('.loader').removeClass('active')
        liste_fax.empty()
    }

    return self;
})();


/**
 * Un fax
 */
hylaweb.reception.Fax = (function () {
    var self = {};

    self.init = function ($item) {
        self.fax = $item;
        self.avatar = self.fax.find('.avatar.image');

        //TODO a rename
        self.deletebutton = self.fax.find('.icon.trash')
        self.bouton2 = self.fax.find('.undo.button')
        self.bouton3 = self.fax.find('.copy.button')
        add_listener();
        // Ajout de la popup pour l'avatar
        addPopupOwner()
    }

    /** 
     * fonction pour gerer le click sur un icon 
     */
    var add_listener = function () {
        self.avatar.on('click', function (event) {
            self.fax = $(this).parents('.item')
            self.avatar = $(this)
            event.stopPropagation();
            // Si le user est proprietaire
            if (isOwner())
                unlockFax()

            // Verifie si le fax n'a pas de proprietaire
            else if (!hasOwner()) {
                //demande d'appropriation du fax
                lockFax()
            }
        });

        //suppression fax
        self.deletebutton.on('click', function (event) {
            self.fax = $(this).parents('.item')
            event.stopPropagation();
            // Si le user est proprietaire
            if (isOwner())
                self.supprimerFax()

            // Verifie si le fax n'a pas de proprietaire
            else if (!hasOwner()) {
                self.supprimerFax()
            }
        });

        self.fax.hover(
            function () {
                var icons = $(this).find('.action .icon, .large.plus.square.icon')
                icons.css('color', 'black');
            }, function () {
                var icons = $(this).find('.action .icon, .large.plus.square.icon')
                icons.removeAttr('style');
            }
        );

        // Click sur le fax
        self.fax.click(function () {
            $("#fax .item").removeClass("selected")
            $(this).addClass("selected");
            var $pdf = $('#pdf');
            var url_fax_pdf = encodeURIComponent(hylaweb.api.urls['visu_fax'].replace("#id_fax#", $(this).attr('id-fax')).replace("#guid#", hylaweb.user.guid_ad));
            $pdf.attr('src', "../static/pdfjs/web/viewer.html?file=" + url_fax_pdf)
        });
    };

    /**
     * Ajoute le popup pour le proprietaire
     */
    var addPopupOwner = function () {
        self.avatar.popup({
            content: self.avatar.attr('data-prop'),
            position: 'bottom center',
            delay: {
                show: 200,
            }
        });
    }

    /**
     * retourne true si le fax selectionné possède déjà un proprietaire
     */
    var hasOwner = function () {
        var avatar = self.fax.find('.avatar.image.locked');
        return avatar.length
    }

    /**
     * Retourne true si l'utilisateur est proprietaire de ce fax
     */
    var isOwner = function () {
        var avatar = self.fax.find('.avatar.image.locked');
        var dataprop = avatar.attr('data-prop')
        if (dataprop == hylaweb.user.prenom + " " + hylaweb.user.nom) {
            return true
        }
        else {
            return false
        }
    }

    /**
     * S'approprie le fax si pas de proprietaire
     */
    lockFax = function () {
        var url_lock_fax = hylaweb.api.urls['lock_fax'].replace("#id_fax#", self.fax.attr('id-fax'))
        // Si pas de proprio on se met proprietaire
        $.ajax({
            url: url_lock_fax,
            type: 'post',
            data: {
                proprietaire: hylaweb.user.prenom + " " + hylaweb.user.nom + " <" + hylaweb.user.mail + ">",
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    self.avatar.transition({
                        animation: 'scale',
                        onComplete: function () {


                            var mail = hylaweb.user.mail
                            var name = hylaweb.user.nom
                            var key = name
                            var data_prop = hylaweb.user.prenom + " " + hylaweb.user.nom

                            /*     var url_get_avatar = hylaweb.api.urls['get_avatar'].replace("#initial#", initial).replace('#mail#', mail).replace('#key#', key)
                                baliseAvatar = '<div data-prop="' + data_prop + '" class="ui circular image avatar locked"><img src="' + url_get_avatar + '"></div>'
     */

                            var initial = hylaweb.user.prenom.charAt(0) + hylaweb.user.nom.charAt(0)
                            var url_get_avatar = hylaweb.api.urls['get_avatar'].replace("#initial#", initial).replace('#key#', key).replace('#mail#', mail)
                            contentAvatar = $('<img src="' + url_get_avatar + '">')
                            self.avatar.attr('data-prop', data_prop)
                            self.avatar.addClass("locked")
                            self.avatar.html(contentAvatar);
                        }
                    });
                    self.avatar.transition('scale');
                }
                else {
                    //TODO message a afficher a l'utilisateur
                    console.log(json.description)
                }
            });
    }

    /**
     * Se desapproprie le fax si l'utilisateur est le proprietaire
     */
    unlockFax = function () {
        var url_unlock_fax = hylaweb.api.urls['unlock_fax'].replace("#id_fax#", self.fax.attr('id-fax'))
        // Si pas de proprio on se met proprietaire
        $.ajax({
            url: url_unlock_fax,
            type: 'post',
            data: {
                guid: hylaweb.user.guid_ad,
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    if (self.avatar.hasClass('locked')) {
                        avatar = $('<img src="../static/images/lock.png">')
                    }
                    self.avatar.transition({
                        animation: 'scale',
                        onComplete: function () {
                            var contentAvatar = $('<img src="../static/images/lock.png">')
                            self.avatar.removeAttr('data-prop')
                            self.avatar.removeClass("locked")
                            self.avatar.html(contentAvatar);
                        }
                    });
                    self.avatar.transition('scale');
                }
                else {
                    //TODO message a afficher a l'utilisateur
                    console.log(json.description)
                }
            });
    }

    /**
     * Suppression des fax
     */

    // Modifié par Philippe
    
    self.supprimerFax = function () {
        var url_delete_fax = hylaweb.api.urls['delete_fax'].replace('#id_fax#', self.fax.attr('id-fax'))
        console.log('supprimerfax')
        $.ajax({
            url: url_delete_fax,
            type: 'DELETE',
            data: {
                guid: hylaweb.user.guid_ad,
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    //$self.item.fadeOut('fast')
                    self.fax.transition({
                        animation: 'fade',
                        onComplete: function () {
                            // TODO Traiter le cas ou il n'y a plus de FAX
                            // Si un fax succede celui qui est supprimé on le selectionne
                            if (self.fax.hasClass("selected")){
                                if (self.fax.next('.item').length != 0) {
                                    console.log('suivant')
                                    hylaweb.reception.FaxList.selectFax(self.fax.next('.item'))
                                }

                                // Sinon si un fax precede celui qui est supprimé on le selectionne
                                else if (self.fax.prev('.item').length != 0) {
                                    hylaweb.reception.FaxList.selectFax(self.fax.prev('.item'))
                                }
                            }
                            //On supprime le fax
                            self.fax.remove();
                        }
                    });
                }
                else {
                    //TODO message a afficher a l'utilisateur
                    console.log(json.description)
                }
            });
    }

    /**f
     * Mise a jour des donnees du fax selectionner
     * @param {l'id du fax} id_fax 
     */

    // Modifié par Philippe

    self.updateFax = function (id_fax) {
        var oldfax = $('#fax .item[id-fax="' + id_fax + '"]')
        if (!oldfax.length)
            return;

        var url_get_fax = hylaweb.api.urls['get_fax'].replace('#id_fax#', id_fax)
        $.ajax({
            url: url_get_fax,
            type: 'get',
        })
            .done(function (json) {
                // Si le fax est bien recuperer
                if (json.status == "OK") {
                    var jsonfax = json.items
                    if (jsonfax.affichable != 0) {
                        var newfax = hylaweb.reception.FaxList.CreateFax(jsonfax)
                        if (oldfax.hasClass("selected")) newfax.addClass("selected");
                        oldfax.replaceWith(newfax)
                        // animation pour l'update d'un fax
                        newfax.css('animation', 'glow 2s');
                    }
                    else {
                        oldfax.transition({
                            animation: 'fade',
                            onComplete: function () {
                                // TODO Traiter le cas ou il n'y a plus de FAX
                                // Si un fax succede celui qui est supprimé on le selectionne
                                if (oldfax.hasClass("selected")){
                                    if (oldfax.next('.item').length != 0) {
                                        hylaweb.reception.FaxList.selectFax(oldfax.next('.item'))
                                    }
        
                                    // Sinon si un fax precede celui qui est supprimé on le selectionne
                                    else if (oldfax.prev('.item').length != 0) {
                                        hylaweb.reception.FaxList.selectFax(oldfax.prev('.item'))
                                    }    
                                }
                                //On supprime le fax
                                oldfax.remove();
                            }
                        });
                        
                    }
                }
                else {
                    //TODO message a afficher a l'utilisateur
                    console.log(json.description)
                }
            });
    }
    return self;
})();


