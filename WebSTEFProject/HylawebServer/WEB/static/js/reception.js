var hylaweb = hylaweb || {}

$(document).ready(function () {

    hylaweb.reception.init();

    // verifie si on a le focus de la fenetre
    hylaweb.focusReception();

    // on recupere tous les fax
    hylaweb.lazy.init($('.column.left'), 'rx');

    // Automatically shows on init if cookie isnt set
    $('.cookie.nag').nag({
        key: 'reception-' + $('.cookie.nag').attr('version')
    });
});


// Partie Reception des fax
hylaweb.reception = (function () {
    var self = {};

    var $service_current = null
    var $agence = null
    var filter = null
    var contentPopup = null

    self.init = function () {
        $service_current = $('#service-current')
        $agence = $('#agence')

        self.FaxList.init();

        // On creer le menu des services et des agences et on affiche le service par defaut du user
        hylaweb.MenuServices.CreateMenu();

        // On affiche ensuite le fax correspondant au service par defaut du user
        self.FaxList.updateListFax(hylaweb.getIdServiceCurrent())

        // Connexion a Rabbit
        hylaweb.Rabbit.connect(hylaweb.hostRabbit, hylaweb.session.login, hylaweb.getIdServiceCurrent())

        // Initialisation du filtre pour afficher "mes fax"
        self.Filter.init();

        // Initialisation du formulaire d'archivage
        self.ArchiveForm.init();
    }

    // Met a jour le libelle du service selectionné et les fax correspondant 
    // puis on affiche les fax correspondant a ce service
    self.updateService = function (service, id_service, agence) {
        $service_current.text(service)
        $service_current.attr('idService', id_service)
        $agence.text(agence)

        // On cache le pdf qui est affiché
        hylaweb.reception.Pdf.hidePDF()

        // On affiche les fax correspondants au service par defaut de l'utilisateur
        hylaweb.reception.FaxList.updateListFax(hylaweb.getIdServiceCurrent())

        // Mise a jour de la queue Rabbit
        hylaweb.Rabbit.subscribe(hylaweb.session.login, hylaweb.getIdServiceCurrent());
    }

    /** Gestion des messages stomp pour les fax */
    self.traitementMessageWebSocket = function (message) {
        Logger.info("message: " + message.type, message)
        if (message.type == "RX-NEW") {
            // TODO si l'id existe deja on fait un update
            Logger.info(message)
            self.FaxList.AddPrependFax(message)
        }

        else if (message.type == "RX-UPD") {
            Logger.info(message)
            self.FaxList.updateFax(message.id, true)
        }
    }

    return self;
})();

hylaweb.reception.Filter = (function () {
    var self = {};

    self.init = function () {

        //Popup pour le filtre du fax
        $('#filter-fax').popup({
            html: $(this).attr('data-content'),
            position: 'right center',
            delay: {
                show: 700,
            },
        })

        // Permet au user de voir les fax dont il a les droits (fax dont il est proprietaire et fax qui sont libres)
        $('#filter-fax').checkbox({
            onChecked: function () {
                $('#filter-fax').attr('data-content', "Afficher tous les fax");
            },

            // On reaffiche l'ensemble des fax
            onUnchecked: function () {
                $('#filter-fax').attr('data-content', "Afficher mes fax")
            },

            //on met a jour la popup et on raffraichit les fax
            onChange: function () {
                $('#filter-fax').popup({
                    html: $(this).attr('data-content'),
                }).popup('show');
                hylaweb.reception.FaxList.updateListFax(hylaweb.getIdServiceCurrent());
            }
        })
    }
    return self;
})();



hylaweb.reception.Pdf = (function () {
    var self = {};

    /**
     * Enleve le pdf qui est affiché
     */
    self.hidePDF = function () {
        $('#pdf').attr('src', '')
    }
    return self;
})();

/**
 * Représente la liste des fax
 */
hylaweb.reception.FaxList = (function () {
    var self = {};
    var $list

    var datesSep = {}

    self.init = function () {
        $list = $('#liste-fax')
    }

    // retourne la liste des fax et des separators
    self.getItems = function () {
        return $list.find('.item-date')
    }

    // retourne la position d'un element a partir de sa date
    self.indexOfFax = function (datetime) {
        return $(".item.fax .date-label:contains(" + datetime + ")").parents('.item.fax').index()
    }

    // retourne la liste de fax
    self.getItemsFax = function () {
        return $list.find('.fax.item')
    }

    // retourne le fax selectionné
    self.getFaxSelected = function () {
        return $list.find('.fax.item.selected')
    }

    // suppression des separator
    var removeSeparator = function () {
        $list.find('.separator').remove()
    }

    /* // creation des dates pour les separateurs
    createDateSeparator = function () {
        moment.locale('fr')
        datesSep['Aujourd\'hui'] = moment().add(1, 'days').startOf('day')
        datesSep['Hier'] = moment().startOf('day')
        datesSep[moment().subtract(2, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(1, 'days').startOf('day')
        datesSep[moment().subtract(3, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(2, 'days').startOf('day')
        datesSep[moment().subtract(4, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(3, 'days').startOf('day')
        datesSep[moment().subtract(5, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(4, 'days').startOf('day')
        datesSep[moment().subtract(6, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(5, 'days').startOf('day')
        datesSep[moment().subtract(1, 'week').startOf('day').format('DD/MM/YYYY')] = moment().subtract(6, 'days').startOf('day')
    } */

    // creation des dates pour les separateurs
    createDateSeparator = function () {
        moment.locale('fr')
        datesSep['Aujourd\'hui'] = moment().startOf('day')
        datesSep['Hier'] = moment().subtract(1, 'days').startOf('day')
        datesSep[moment().subtract(2, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(2, 'days').startOf('day')
        datesSep[moment().subtract(3, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(3, 'days').startOf('day')
        datesSep[moment().subtract(4, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(4, 'days').startOf('day')
        datesSep[moment().subtract(5, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(5, 'days').startOf('day')
        datesSep[moment().subtract(6, 'day').startOf('day').format('DD/MM/YYYY')] = moment().subtract(6, 'days').startOf('day')
        datesSep[moment().subtract(1, 'week').startOf('day').format('DD/MM/YYYY')] = moment().subtract(1, 'week').startOf('day')
    }

    //insertion des separateur de temps pour les fax
    self.insertSeparator = function () {
        i = 0
        // pour chaque separateur on verifie ou on l'insere
        for (date in datesSep) {
            // on envoi juste une date avec un jour de
            var posSep = getSeparatorPosition(datesSep[date])
            // si on peut inserer le separateur
            if (posSep != null) {
                self.addAtPosition({ 'date': date, 'datetime': datesSep[date] }, 'SEP', posSep)
                // si le separateur est inseré on le supprime
                delete datesSep[date]
            }
            else {
                Logger.debug('separateur pas chargé')
            }
        }
    }

    /* // Retourne la position d'un separator a partir de sa date
    var getSeparatorPosition = function (datetimeSeparator) {
        // Conversion de la date en objet moment
        pos = null
        toInsert = false

        $.each(self.getItems(), function (position) {
            //console.log("fax: " + $(this).attr('id-fax'))
            var date = moment($(this).find(".date-label").text(), 'llll')
            //console.log("Comparaison d'insertion: " + datetimeSeparator.format('llll') + " ----- " + date.format('llll'))

            // dès qu'un des fax est plus ancien que la date du separateur on peut l'inserer en verifiant que le fax est bien issu le mem jour que le separateur
            //console.log("pour la date: " + datetimeSeparator.format('DD/MM/YYYY HH:mm'), '------', date.format('DD/MM/YYYY HH:mm'))
            if (datetimeSeparator.diff(date) >= 0) {
                //console.log("date plus ancienne")
                //console.log(datetimeSeparator.clone().subtract(1, 'minute').format('DD'), date.format('DD'))
                if (datetimeSeparator.clone().subtract(1, 'minute').format('DD') == date.format('DD')) {
                    //console.log("le meme jour")
                    //on verifie si l'element suivant correspond au jour du seprateur
                    pos = position
                    toInsert = true
                    return false
                }
                else {
                    //console.log("pas le meme jour")
                }
            }
        })

        if (toInsert) {
            //console.log("Ajout du separateur: " + datetimeSeparator.format('DD/MM/YYYY HH:mm'))
            return pos
        }

        else {
            //console.log("Imposibble d'ajouter le separateur: " + datetimeSeparator.format('DD/MM/YYYY HH:mm'))
            return null
        }


    } */

    // Retourne la position d'un separator a partir de sa date
    var getSeparatorPosition = function (datetimeSeparator) {
        // Conversion de la date en objet moment
        pos = null

        console.log(datetimeSeparator.format('ddd DD MMM'))

        console.log(self.getItemsFax().find(".date-label:contains('"+ datetimeSeparator.format('ddd DD MMM') + "')").first())
/* 
        console.log((self.getItemsFax()).first(self.getItemsFax().find(".date-label:contains('"+ datetimeSeparator.format('ddd DD MMM') + "')")).index)
        console.log(self.getItemsFax().find(".date-label:contains('"+ datetimeSeparator.format('ddd DD MMM') + "')").first().index(self.getItemsFax())) */
        
        //return pos
        // on recherche le premier element en dessous-de la date recherche qui a le meme jour
    }
    // pour les separateur restant
    /*  $.each(self.getDateSeparator(), function (position) {
         //console.log("fax: " + $(this).attr('id-fax'))
         var date = moment($(this).find(".date-label").text(), 'llll')
         //console.log("Comparaison d'insertion: " + datetimeSeparator.format('llll') + " ----- " + date.format('llll'))

         // dès qu'un des fax est plus ancien que la date du separateur on peut l'inserer en verifiant que le fax est bien issu le mem jour que le separateur
         //console.log("pour la date: " + datetimeSeparator.format('DD/MM/YYYY HH:mm'), '------', date.format('DD/MM/YYYY HH:mm'))
         if (datetimeSeparator.diff(date) >= 0) {
             //console.log("date plus ancienne")
             //console.log(datetimeSeparator.clone().subtract(1, 'minute').format('DD'), date.format('DD'))
             if (datetimeSeparator.clone().subtract(1, 'minute').format('DD') == date.format('DD')) {
                 //console.log("le meme jour")
                 //on verifie si l'element suivant correspond au jour du seprateur
                 pos = position
                 toInsert = true
                 return false
             }
             else {
                 //console.log("pas le meme jour")
             }
         }
     })

     if (toInsert) {
         //console.log("Ajout du separateur: " + datetimeSeparator.format('DD/MM/YYYY HH:mm'))
         return pos
     }
     else {
         //console.log("Imposibble d'ajouter le separateur: " + datetimeSeparator.format('DD/MM/YYYY HH:mm'))
         return null
     }
 } */

    // Retourne la position d'un nouveau fax ou d'un separator a partir de sa date de reception 
    self.getPosition = function (datetime) {
        // Conversion de la date en objet moment
        pos = null
        toInsert = false
        console.log(datetime, 'llll')
        moment.locale('fr')
        $.each(self.getItems(), function (position) {
            var date = null
            // si c'est un fax
            if ($(this).attr('id-fax') != null) {
                date = moment($(this).find(".date-label").text(), 'llll')
            }

            // si c'est un separateur
            else {
                console.log("sep:" + $(this).text())
                date = moment($(this).attr('date'))
                console.log("Comparaison d'insertion: " + datetime.format('llll') + " ----- " + date.format('llll'))
                console.log('dateSEP', date)
            }

            // dès qu'on a une date plus ancienne et que ca correspond au meme jour
            if (datetime.diff(date) >= 0) {
                pos = position
                toInsert = true
                return false
            }
        })
        if (toInsert)
            return pos
        else
            return null

    }

    // Met a jour la liste
    self.updateListFax = function (id_service) {
        var dataGet = {
            guid: hylaweb.user.guid_ad,
        }

        // verfie si on a filtrer les messages
        if ($('#filter-fax').checkbox('is checked')) {
            dataGet.proprietaire = hylaweb.user.prenom + " " + hylaweb.user.nom + " <" + hylaweb.user.mail + ">";
        }

        var url_rx_fax = api.urls['rx_fax'].replace("#id_serv#", id_service) + "/" + conf.LIMIT_RX_FAX
        $.ajax({
            url: url_rx_fax,
            type: 'get',
            data: dataGet
        })
            .done(function (json) {
                // on recupere l' id du fax selectionné
                id_fax_selected = self.getFaxSelected().attr('id-fax')
                // remise a zero de la liste des fax
                reset()
                $.each(json.items, function (i, fax) {
                    self.AddAppendFax(fax)
                });

                // ajout des séparateurs
                //createDateSeparator()
               // self.insertSeparator()

                var div_error = $('div.warning')
                if (isEmpty()) {
                    div_error.removeClass('hidden')
                }
                else {
                    div_error.addClass('hidden')
                }

                // On selectionne le fax qui était selectionné avant avec son id
                if (id_fax_selected != undefined) {
                    self.selectFax(id_fax_selected)
                }

                // Sinon On selectionne le premier fax
                else {
                    Logger.debug("selection du premier fax")
                    self.selectFax($list.find('.item.fax:first-child').attr('id-fax'))
                }
                hylaweb.lazy.reset();
            });
    }

    // Ajoute un fax ou un separateur a une position donnée
    self.addAtPosition = function (obj, type, position) {
        console.log("ADD", obj, position)
        // si on doit ajouter un fax
        if (type == "FAX") {
            $fax = CreateFax(obj)
            // TODO a voir

            console.log($list.find(".item-date").eq(position))
            for (i = 0; i < 15; i++) {
                console.log('t', i, $list.find(".item-date").eq(i))
            }
            //$list.find(".item.fax:eq(" + position + ")").after($fax);
            console.log(position)
            $list.find(".item-date").eq(position).before($fax);
            //$list.prepend($fax)
            // On initialise l'objet fax
            hylaweb.reception.Fax.init($fax)
        }

        // si on doit ajouter un separateur
        else if (type == "SEP") {
            $separator = $("<div date=\"" + obj.datetime + "\" class=\"item-date ui separator grey attached center aligned inverted segment\">"
                + obj.date
                + " </div >")

            /* $separator = $("<div date=\"" + obj.datetime + "\" class=\"item-date ui separator attached center segment\">"
                + obj.date
                + " </div >") */

            // ajout du separateur a la position souhaiter
            $list.find(".item-date:eq(" + position + ")").before($separator)
        }

    }

    /**
     * Ajoute un fax en début de liste
     */
    self.AddPrependFax = function (fax) {
        $fax = CreateFax(fax)
        // ajoute le fax juste apres le separateur d'aujourd'hui
        $list.find('.separator:first').after($fax)

        // On initialise l'objet fax
        hylaweb.reception.Fax.init($fax)
    }

    /**
     * Ajoute un fax en fin de liste
     */
    self.AddAppendFax = function (fax) {
        $fax = CreateFax(fax)
        $list.append($fax)
        // On initialise l'objet fax
        hylaweb.reception.Fax.init($fax)
    }

    // Construit le fax pour l'affichage
    var CreateFax = function (fax) {
        return $(hylaweb.reception.Fax.createItem(fax))
    }

    /**
    * Selectionne le fax de la liste a partir de son id
    */
    self.selectFax = function (id_fax) {
        Logger.debug('selection du fax ayant l\'id ' + id_fax);
        $list.find('.item.fax[id-fax="' + id_fax + '"]').trigger('click')
    }

    /**
     * Retourne un booleen pour savoir si un fax existe dans la liste
     */
    var isEmpty = function () {
        return (self.getItemsFax().length == 0)
    }

    /**
     * Vide la liste des fax
     */
    var reset = function () {
        $('#chargement').find('.loader').removeClass('active')
        $list.empty()
    }

    // Recupere l'id du fax par rapport a l'item
    var getIdFax = function ($item) {
        return $list.find($item).attr('id-fax')
    }

    /** 
    * Mise a jour des donnees du fax selectionner
    * @param {l'id du fax} id_fax 
    */
    self.updateFax = function (fax_id, transition) {
        //on recupere les donnees du fax en base
        var fax = null
        debugger
        var url_get_fax = api.urls['get_fax'].replace('#id_fax#', fax_id)
        console.log(url_get_fax)
        $.ajax({
            url: url_get_fax,
            type: 'get',
            async: false,
            data: {
                guid: hylaweb.user.guid_ad
            }
        }).done(function (json) {
            if (json.status == "OK") {
                fax = json.items
            }
            else {
                Logger.debug(json.description)
            }
        });

        if (fax != null) {
            var oldfax = $('#liste-fax .item[id-fax="' + fax.id + '"]')
            // on verifie si le fax est chargé
            if (fax.id >= getIdFax($('#liste-fax .fax.item:last'))) {
                 // On refresh la liste complete Si le fax a été deplacer dans un autre service ou si on selectionne uniquement "mes fax"
                 if ($('#filter-fax').checkbox('is checked') || !oldfax.length) {
                     hylaweb.reception.FaxList.updateListFax(hylaweb.getIdServiceCurrent())
                 }

                // On insere le fax a la bonne position si le fax a été deplacé dans un autre service ou si on selectionne uniquement "mes fax"
               /*  if ($('#filter-fax').checkbox('is checked') || !oldfax.length) {
                    hylaweb.reception.FaxList.addAtPosition(fax, "FAX", hylaweb.reception.FaxList.getPosition(moment(fax.datetime)))
                } */

                // sinon on update uniquement le fax en question
                else {
                    // si le service du fax et different du service courant alors 
                    // c'est un deplacement de fax dans un autre service
                    // donc on supprime l'objet
                    if (fax.id_service != $('#service-current').attr('idservice')) {
                        Logger.debug("Deplacement du fax: " + fax.id + " dans le service " + fax.id_service)
                        oldfax.transition({
                            animation: 'fade',
                            onComplete: function () {
                                // Si un fax succede celui qui est supprimé on le selectionne
                                if (oldfax.hasClass("selected")) {
                                    if (oldfax.next('.item').length != 0) {
                                        self.selectFax(oldfax.next('.item').attr('id-fax'))
                                    }

                                    // Sinon si un fax precede celui qui est supprimé on le selectionne
                                    else if (oldfax.prev('.item').length != 0) {
                                        self.selectFax(oldfax.prev('.item').attr('id-fax'))
                                    }
                                }
                                //On supprime le fax
                                oldfax.remove();
                            }
                        });
                    }

                    // Si c'est une suppresion de fax 
                    else if (fax.affichable == 0) {
                        Logger.debug("Suppression du fax: " + fax.id)
                        oldfax.transition({
                            animation: 'fade',
                            onComplete: function () {
                                // Si un fax succede celui qui est supprimé on le selectionne
                                if (oldfax.hasClass("selected")) {
                                    if (oldfax.next('.item').length != 0) {
                                        self.selectFax(oldfax.next('.item').attr('id-fax'))
                                    }

                                    // Sinon si un fax precede celui qui est supprimé on le selectionne
                                    else if (oldfax.prev('.item').length != 0) {
                                        self.selectFax(oldfax.next('.item').attr('id-fax'))
                                    }
                                }
                                //On supprime le fax
                                oldfax.remove();
                            }
                        });
                    }

                    // Sinon si c'est une mise a jour du fax qui n'est pas une suppression 
                    else {
                        var newfax = CreateFax(fax)
                        // on initialise le fax TODO a modifier la facon dont c'est initialiser
                        hylaweb.reception.Fax.init(newfax)
                        //Si l'ancien fax était selectionné, on selectionne le nouveau
                        if (oldfax.hasClass("selected"))
                            newfax.addClass("selected");

                        oldfax.replaceWith(newfax)
                        // animation pour l'update d'un fax
                        if (transition)
                            newfax.transition('glow');
                    }
                }
            }

            // si le fax n'est pas chargé , on ne refresh pas la liste
            else {
                Logger.debug("Fax non chargé, impossible d'atteindre la liste")
                return;
            }
        }
        else {
            Logger.info("impossible de recuperer les infos en base sur le fax " + fax_id)
        }


    }
    return self;
})();

/**
 * Archivage sur E-Track et SCOP
 */
hylaweb.reception.ArchiveForm = (function () {
    var self = {}

    var $form = null
    var $buttonOK = null
    var $cle = null

    // soit SCOP, soit FACT
    var type_transfer = null

    // service sur lequel le fax se trouve
    var service = null

    // fax a manipuler
    var fax = null

    // lettre de voiture saisi par le user
    var position = null

    self.init = function () {
        $form = $('#demande-archivage .form')
        $buttonOK = $('#demande-archivage .ok.button')
        $cle = $('div[name=checkCle]')
        // Ajout des evenements au formulaire
        addListener()
    }

    /**
    * Ajout des listener
    */
    var addListener = function () {
        $('#demande-archivage').on('keyup', function (e) {
            if (e.keyCode == 13 && $form.form('is valid')) {
                $buttonOK.trigger('click')
            }
        })

        // Ajoute une seule fois l'evenement
        $buttonOK.on('click', function () {
            // on envoie la position saisi
            archiveFax(position)

        })

        // Annulation de la soumission du formulaire
        $form.submit(function (event) {
            event.preventDefault();
        });

        // a chaque saisi de caractere on verifie si le form est valide
        $form.on('keyup', function (e) {
            $form.form('validate form')
        });

        // active le bouton checkbox
        $cle.state()
        $cle.on('click', function (e) {
            e.preventDefault()
            toogleCheckboxCle()
            $form.form('validate form')
        });
    }

    /**
    * Ouvre la boite de dialogue pour l'archivage
    * @param {type d'archivage} type 
    */
    self.open = function (objfax, type, idService) {
        type_transfer = type
        fax = objfax
        service = idService

        if (type == "SCOP") {
            $('#demande-archivage .titre').text('Envoyer vers SCOP')
        }
        else if (type == "FACT") {
            $('#demande-archivage .titre').text('Archiver pour la facturation')
        }

        $('#demande-archivage').modal({
            closable: false,
        }).modal('show');

        reset()

        addRule(14)
    }

    // On reset le formulaire
    var reset = function () {
        $form.form('clear')
        $form.find('.ui.error.message').empty()
        // on remet la taille a 14
        //$form.form('get field', 'position').attr('maxLength', 14)
        // on remet le checking cle a false
        $cle.removeClass('active')
        toogleCheckboxCle()
    }

    // ajoute les regles en fonction de la taille de la position 12 = sans clé + 14 sans cle
    var addRule = function (length) {
        // Création de la contrainte sur la cle de controle
        $.fn.form.settings.rules.cleControle = function (value) {
            return verifie_cle_controle_ASCII(value.toUpperCase())
        };

        $form.form({
            on: 'change',
            fields: {
                position: {
                    identifier: 'position',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'La lettre de voiture ne doit pas être vide.'
                        },
                        {
                            type: 'exactLength[' + length + ']',
                            prompt: 'Vous n\'avez pas saisi ' + length + ' caractères'
                        },
                        {
                            type: 'cleControle',
                            prompt: 'La clé de contrôle est invalide'
                        },
                    ]
                },
            },

            // Lorsque le formulaire est valide
            onSuccess: function (event, fields) {
                $buttonOK.removeClass('disabled')
                // recupere la position valide
                position = fields.position
            },

            // Lorsque le formulaire n'est pas valide
            onFailure: function (formErrors, fields) {
                $buttonOK.addClass('disabled')
            }
        });
    }

    // Gere le toggle button si on doit renseigner la cle ou non 
    var toogleCheckboxCle = function () {
        var $icon = $cle.find('i')
        var text = ''
        var length = 0

        if ($cle.hasClass('active')) {
            Logger.debug('cle pas demandé')
            $icon.removeClass('check').addClass('ban')
            text = 'La clé ne doit pas être saisie'
            length = 12
            addRule(length)
            // on supprime la regle sur la cle
            $form.form('remove rule', 'position', 'cleControle')
        }
        else {
            Logger.debug('cle demandé')
            $icon.removeClass('ban').addClass('check')
            text = 'La clé doit être saisie'
            length = 14
            addRule(length)
        }

        //on change la popup
        $cle.popup({
            content: text,
            position: 'left center'
        })

        // redonne le focus a l'input
        $form.form('get field', 'position').focus()
        // gestion de la taille
        $form.form('get field', 'position').attr('maxLength', length)
        $form.form('set value', 'position', $form.form('get value', 'position').substr(0, length))
    }

    // permet d'archiver un fax pour la facturation ou d'envoyer sur E-Track
    archiveFax = function (numLDV) {
        var url_transfer_fax = api.urls['transfer_fax'].replace('#id_fax#', fax.id).replace('#type_trf#', type_transfer)
        request_type = null
        if (type_transfer == "SCOP") {
            request_type = "GET"
        }

        else if (type_transfer == "FACT") {
            // TODO mettre en post
            request_type = "GET"
        }

        $.ajax({
            url: url_transfer_fax,
            type: 'GET',
            data: {
                service: service,
                NumLDV: numLDV.toUpperCase().substring(0, 12),
            }
        })
            .done(function (json) {
                if (json.status != "OK") {
                    hylaweb.afficherNotif('delete', json.description, 'red', true)
                }

                // si le transfert s'est bien deroulé
                else {
                    var $buttonArchive = $('#liste-fax .fax.item[id-fax=' + fax.id + '] .archive-fax[type=' + type_transfer + ']')
                    $buttonArchive.removeClass('basic grey').addClass('green')

                    // on ne bloque pas l'envoi vers SCOP, on ajoute locked aux autres type d'envoi (FACT)
                    if (type_transfer != "SCOP") {
                        buttonArchive.addClass('locked')
                    }

                    $buttonArchive.css('display', 'inline-block').css('visibility', 'visible');
                }
            });
    }
    return self;
})();

/**
 * Un fax
 */
hylaweb.reception.Fax = (function () {
    var self = {};

    self.init = function ($item) {
        var objfax = {}
        objfax.item = $item;
        objfax.id = objfax.item.attr('id-fax');
        objfax.ndoc_arc = objfax.item.attr('ndoc-arc');
        objfax.avatar = objfax.item.find('.avatar.image');
        objfax.tagButton = objfax.item.find('.add-tag')
        objfax.deleteButton = objfax.item.find('.icon.trash')
        objfax.moveFaxButton = objfax.item.find('.move-fax')
        objfax.archiveFaxButton = objfax.item.find('.archive-fax')
        objfax.transferFaxButton = objfax.item.find('.share.square.outline.icon')
        objfax.transferMailButton = objfax.item.find('.envelope.outline.icon')

        objfax.icons = objfax.item.find('.action .icon, .large.plus.square.icon')
        objfax.actionIcons = objfax.item.find('.action').children()

        addListener(objfax);

        // ajoute les listeners en vérifiant que le user peut effectué ces actions sur le fax
        authorizeActions(objfax);

        // Ajout des popup
        addPopup(objfax)
    }

    // Creer le code html pour le proprietaire du fax
    var createAvatar = function (proprietaire) {
        var avatar = null
        var initial = ""
        var mail = ""
        var key = ""
        var data_prop = ""
        var type_avatar = ""
        // Ajout du proprietaire
        if (proprietaire == "" || proprietaire == undefined) {
            avatar = '<div class="ui circular image avatar"><img src="../static/images/lock.png"></div>'
        }

        // le proprietaire n'est pas vide
        else {
            var type_avatar = "user"
            // si le proprietaire est valide
            if (proprietaire.split(" ").length >= 3) {
                // test si c'est un emballage
                if (proprietaire.split(" ")[0] == "EMB" && proprietaire.split(" ")[1] == "reco:") {
                    var statusEMB = proprietaire.split(" ")[2]
                    if (statusEMB == "VALIDE") {
                        initial = "VAL"
                        key = proprietaire.split(" ")[0] + "%3AVAL"
                        data_prop = "EMB VALIDE"
                    }

                    //Emballage indetermine
                    else {
                        initial = "IND"
                        key = proprietaire.split(" ")[0] + "%3AIND"
                        data_prop = "EMB INDETERMINE"
                    }
                    mail = ""
                    type_avatar = "automate"
                }

                // si le proprietaire est un utilisateur 
                else {
                    initial = proprietaire.split(" ")[0].charAt(0) + proprietaire.split(" ")[1].charAt(0)
                    mail = proprietaire.split(" ")[2]
                    var name = proprietaire.split(" ")[1]
                    key = name
                    data_prop = proprietaire.split(" ")[0] + " " + proprietaire.split(" ")[1]
                    if (mail != undefined) {
                        mail = proprietaire.split(" ")[2].replace('<', '').replace('>', '')
                    }
                    else {
                        mail = ""
                    }
                }
            }

            // si le proprietaire n'est pas valide
            else {
                erreur = "!!"
                initial = erreur
                mail = erreur
                name = erreur
                key = name
            }

            var url_get_avatar = api.urls['get_avatar'].replace("#initial#", initial).replace('#mail#', mail).replace('#key#', key)
            avatar = '<div data-prop="' + data_prop + '" class="ui circular ' + type_avatar + ' image avatar locked"><img src="' + url_get_avatar + '"></div>'
        }

        return avatar
    }

    // construit l'element fax
    self.createItem = function (fax) {
        avatar = createAvatar(fax.proprietaire)

        //Si le fax n'as pas été lu par cet utilisateur
        var read = ""
        if (fax.lu == user.id)
            read = "lu"
        else
            read = "non-lu"

        var $fax = $("<div id-fax=\"" + fax.id + "\"class=\"item fax item-date " + read + "\"></div>").append("<div class=\"selector\">")
        var $content = $("<div class=\"content\"><div>")
        var $meta = $("<div class=\"meta\"></div>")


        $fax.append(avatar)

        // Ajout de la page
        var page = fax.npages == 1 ? page = "page " : page = "pages"
        $meta.append("<span class=\"" + read + "\">" + fax.npages + " " + page + "</span>&nbsp&nbsp&nbsp&nbsp")

        // Ajouts des tags
        var tag = ""
        if (fax.tag.length != 0) {
            for (var index_tag in fax.tag) {
                var tagFax = fax.tag[index_tag]
                // Si le tag n'est pas vide
                if (tagFax != "")
                    tag += "<div class=\"ui blue small label\">" + tagFax + "</div>"
            }
        }
        $meta.append("<i class=\"tags icon\"></i>" + tag)

        // ajout du formulaire pour ajouter de nouveau tags
        $formAddTag = $("<div class=\"add-tag ui dropdown icon item\">"
            + "     <i class=\"large plus square icon\"></i>"
            + "     <div class=\"menu\"><div class=\"ui basic segment\" id=\"menu-add-dest\">"
            + "         <form id=\"form-dest\" class=\"ui form error\">"
            + "                 <div class=\"field\">"
            + "                     <div class=\"ui small left icon input\">"
            + "                         <input placeholder=\"Tag...\" maxlength=\"150\" name=\"tag\" type=\"text\">"
            + "                         <i class=\"tag icon\"></i>"
            + "                     </div>"
            + "                 </div>"
            + "             <div class=\"item fluid\"></div>"
            + "             <div class=\"ui error message\"></div>"
            + "         </form>"
            + "     </div>"
            + "</div>")
        $meta.append($formAddTag)

        // ajout des actions sur le fax
        var $action = $("<div class=\"ui right floated content action\">"
            + " <i class=\"stop-propagation envelope outline icon\" title=\"Faire suivre par mail\"></i>"
            + " <i class=\"stop-propagation share square outline icon\" title=\"Faire suivre par fax\"></i>"
            + " <div class=\"stop-propagation move-fax pointing right ui icon compact dropdown\" title=\"Déplacer dans un autre service\">"
            + "     <i class=\"folder open outline icon\"></i>"
            + " </div>"
            + " <i class=\"stop-propagation button trash alternate outline icon\" title=\"Supprimer\"></i>")

        // Ajout des actions d'archivage
        $scop = $("<div data-content=\"Envoyer vers SCOP\" class=\"archive-fax ui label circular mini button basic grey\" type=\"SCOP\">S</div>")
        $fact = $("<div data-content=\"Archiver pour la facturation\" class=\"archive-fax ui label circular mini button basic grey\" type=\"FACT\">F</div>")

        // Test si pas de numero d'archivage alors on ne peut archiver en factu
        if (fax.ndoc_arc == "" || fax.ndoc_arc == null) {
            $fact = null
        }

        // si deja archivé en factu
        if ((fax.etatnew & 16) == 16) {
            $fact.removeClass('grey basic').addClass('green locked')
        }

        // si deja archivé sur SCOP
        if ((fax.etatnew & 32) == 32) {
            $scop.removeClass('grey basic').addClass('green')
        }
        $action.append($scop).append($fact)
        $meta.append($action)


        $expediteur = $("<a class=\"header\"><span class=\"" + read + "\">" + fax.sender + "</span></a>")
        $date = $("<div class=\"ui right floated content\"><span class=\"date-label " + read + "\">" + getDateFax(fax.datetime) + "</span></div>")
        $content.append($expediteur).append($date).append($meta)

        $fax.append($content)
        return $fax
    }


    /** 
     * fonction pour gerer le click sur un icon 
     */
    var addListener = function (objfax) {
        // empeche le click sur le fax si on click sur les icones
        objfax.actionIcons.filter('.stop-propagation').on('click', function () {
            event.stopPropagation();
        });

        //Clique sur le transfere de fax sur HylaSend
        objfax.transferFaxButton.on('click', function () {
            transferFax(objfax);
        });

        // Survole d'un fax
        objfax.item.hover(function () {
            objfax.icons.css('color', 'black');
            objfax.archiveFaxButton.css('visibility', 'visible')

        }, function () {
            objfax.icons.removeAttr('style');
            objfax.archiveFaxButton.css('visibility', 'hidden')
            objfax.archiveFaxButton.filter('.locked').css('visibility', 'visible');
        });

        //TODO PARTIE TAG 
        objfax.tagButton.dropdown({
            direction: 'downward',
            delay: {
                hide: 300,
                show: 200,
                search: 50,
                touch: 50
            },
        });
         objfax.tagButton.on('click', function () {
            //event.stopPropagation();
        }); 

        // Click sur le fax
        objfax.item.click(function () {
            //si le fax n'est pas déjà selectionné
            if (!$(this).hasClass("selected")) {
                hylaweb.reception.FaxList.getItemsFax().removeClass("selected")
                objfax.item.addClass("selected");

                // Chargement du pdf
                var url_fax_pdf = encodeURIComponent(api.urls['visu_fax'].replace("#id_fax#", $(this).attr('id-fax')).replace("#guid#", hylaweb.user.guid_ad));
                $('#pdf').attr('src', "../static/pdfjs/web/viewer.html?file=" + url_fax_pdf)

                // si le fax n'as pas été lu par l'utilisateur on fait la requete pour certifier qu'il l'a lu
                if (!isRead(objfax))
                    readFax(objfax)
            }
        });
    };

    // Listener néecissitant d'avoir certains droits (suppression, appropriation et deplacement de fax)
    var authorizeActions = function (objfax) {

        // si l'utilisateur a les droits on active les evenements
        if (isOwner(objfax) || !hasOwner(objfax)) {

            // Deplacement du fax
            objfax.moveFaxButton.dropdown({
                direction: 'downward',
                delay: {
                    hide: 300,
                    show: 200,
                    search: 50,
                    touch: 50
                },

                values: hylaweb.getServicesDefault(),
                onShow: function () {
                    // On desactive le service courant de la liste
                    var service_current = $('#service-current').attr('idservice')
                    $(this).find('.item[data-value="' + service_current + '"]').addClass('disabled')
                },

                onChange: function (value) {
                    if (value != "")
                        moveFax(objfax, value)
                }
            })

            // Click sur la factu ou etrack
            objfax.archiveFaxButton.on('click', function () {
                if (!$(this).hasClass('locked'))
                    hylaweb.reception.ArchiveForm.open(objfax, $(this).attr('type'), hylaweb.getIdServiceCurrent())
            })

            objfax.avatar.on('click', function (event) {
                event.stopPropagation();
                // Si le user est proprietaire
                if (isOwner(objfax))
                    unlockFax(objfax)

                // Verifie si le fax n'a pas de proprietaire
                else if (!hasOwner(objfax)) {
                    //demande d'appropriation du fax
                    lockFax(objfax)
                }
            });

            //suppression fax
            objfax.deleteButton.on('click', function (event) {
                event.stopPropagation();
                // Demande a l'utilisateur de confirmer la suprresion du fax
                $('#demande-suppression').modal({
                    onApprove: function ($element) {
                        deleteFax(objfax)
                    }
                }).modal('show');
            });
        }

        // si l'utilisateur n'a pas les droits
        else {
            objfax.moveFaxButton.addClass('disabled')
            objfax.deleteButton.addClass('disabled')
            objfax.archiveFaxButton.addClass('disabled')
            objfax.archiveFaxButton.filter('.locked').removeClass('disabled')
        }

        // si l'utilisateur a hylanotify de lancé on lui ajoute de nouvelles actions
        if (hylaweb.isConnected()) {
            //Clique sur le transfere de fax par mail
            objfax.transferMailButton.on('click', function () {
                transferMail(objfax);
            });
        }

        // sinon on lui bloque
        else {
            objfax.transferMailButton.addClass('disabled')
        }
    }

    /**
    * Ajouts des popup
    */
    var addPopup = function (objfax) {
        // ajout de la popup pour le proprietaire
        objfax.avatar.popup({
            content: objfax.avatar.attr('data-prop'),
            position: 'bottom center',
            delay: {
                show: 200,
            }
        });

        // ajout de la popup pour l'archivage
        objfax.archiveFaxButton.popup({
            position: 'bottom center',
            delay: {
                show: 500,
            }
        });
    }

    /**
    * retourne true si le fax selectionné est selectionne
    */
    var isSelected = function (objfax) {
        return objfax.item.hasClass('selected')
    }

    /**
      * retourne true si le fax a été lu par l'utilisateur
      */
    var isRead = function (objfax) {
        return objfax.item.hasClass('lu')
    }

    /**
    * retourne true si le fax selectionné possède déjà un proprietaire
    */
    var hasOwner = function (objfax) {
        return objfax.avatar.hasClass('locked')
    }

    /**
     * Retourne true si l'utilisateur est proprietaire de ce fax
     */
    var isOwner = function (objfax) {
        var proprietaire = hylaweb.user.prenom + " " + hylaweb.user.nom
        return (hasOwner(objfax) && objfax.avatar.attr('data-prop') == proprietaire)
    }

    /**
     * Passe le fax en lu pour l'utilisateur
     */
    var readFax = function (objfax) {
        Logger.debug('fax non lu')
        var url_read_fax = api.urls['read_fax'].replace("#id_fax#", objfax.item.attr('id-fax'))
        $.ajax({
            url: url_read_fax,
            type: 'post',
            data: {
                guid: hylaweb.user.guid_ad
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    Logger.debug(json.description)
                    // On met le fax en lu pour l'utilisateur
                    objfax.item.removeClass('non-lu').addClass('lu')
                    objfax.item.find('*').removeClass('non-lu').addClass('lu')
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }

    /**
     * S'approprie le fax si pas de proprietaire
     */
    var lockFax = function (objfax) {
        var url_lock_fax = api.urls['lock_fax'].replace("#id_fax#", objfax.item.attr('id-fax'))
        $.ajax({
            url: url_lock_fax,
            type: 'post',
            data: {
                proprietaire: hylaweb.user.prenom + " " + hylaweb.user.nom + " <" + hylaweb.user.mail + ">",
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    objfax.avatar.transition({
                        animation: 'scale',
                        onComplete: function () {
                            var mail = hylaweb.user.mail
                            var name = hylaweb.user.nom
                            var key = name
                            var data_prop = hylaweb.user.prenom + " " + hylaweb.user.nom

                            var initial = hylaweb.user.prenom.charAt(0) + hylaweb.user.nom.charAt(0)
                            var url_get_avatar = hylaweb.api.urls['get_avatar'].replace("#initial#", initial).replace('#key#', key).replace('#mail#', mail)
                            contentAvatar = $('<img src="' + url_get_avatar + '">')
                            objfax.avatar.attr('data-prop', data_prop)
                            objfax.avatar.addClass("locked")
                            objfax.avatar.html(contentAvatar);
                        }
                    });
                    objfax.avatar.transition('scale');
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }

    /**
     * Se desapproprie le fax si l'utilisateur est le proprietaire
     */
    var unlockFax = function (objfax) {
        var url_unlock_fax = api.urls['unlock_fax'].replace("#id_fax#", objfax.item.attr('id-fax'))

        $.ajax({
            url: url_unlock_fax,
            type: 'post',
            data: {
                guid: hylaweb.user.guid_ad,
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    objfax.avatar.transition({
                        animation: 'scale',
                        onComplete: function () {
                            var contentAvatar = $('<img src="../static/images/lock.png">')
                            objfax.avatar.removeAttr('data-prop')
                            objfax.avatar.removeClass("locked")
                            objfax.avatar.html(contentAvatar);
                        }
                    });
                    objfax.avatar.transition('scale');
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }

    /**
     * Deplacement d'un fax dans un autre service
     */
    var moveFax = function (objfax, id_new_service) {
        var url_move_fax = api.urls['move_fax'].replace('#id_fax#', objfax.item.attr('id-fax'))
        // on recupere le service courant 
        id_old_service = $('#service-current').attr('idservice')
        Logger.debug('deplacement du fax: ', objfax)
        $.ajax({
            url: url_move_fax,
            type: 'POST',
            data: {
                'id_new_service': id_new_service,
                'id_old_service': id_old_service,
                'hostRabbit': hostRabbit,
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    Logger.debug(json)
                    objfax.item.transition({
                        animation: 'fade',
                        onComplete: function () {
                            // Si un fax succede celui qui est supprimé on le selectionne
                            if (objfax.item.hasClass("selected")) {
                                if (objfax.item.next('.item').length != 0) {
                                    hylaweb.reception.FaxList.selectFax(objfax.item.next('.item').attr('id-fax'))
                                }

                                // Sinon si un fax precede celui qui est supprimé on le selectionne
                                else if (objfax.item.prev('.item').length != 0) {
                                    hylaweb.reception.FaxList.selectFax(objfax.item.prev('.item').attr('id-fax'))
                                }
                            }
                            //On supprime le fax
                            objfax.item.remove();
                        }
                    });
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }

    /**
    * Transférer un fax par HylaSend
    */
    var transferFax = function (objfax) {
        var url_transfer_fax = api.urls['transfer_fax'].replace('#id_fax#', objfax.item.attr('id-fax'))
        url_transfer_fax = url_transfer_fax.replace('#type_trf#', 'FAX')
        Logger.debug('Transfert du fax: ', url_transfer_fax)
        $.ajax({
            url: url_transfer_fax,
            type: 'GET',
            data: {
                login_ad: hylaweb.session.login,
            }
        })
            .done(function (json) {
                // si ok ouverture de hylasend
                if (json.status == "OK") {
                    var url_hylasend = api.urls['hylasend'].replace('#faxname#', json.items.new_fax_name)
                    Logger.debug('ouverture de Hylasend avec l\'url ' + url_hylasend)
                    window.open(url_hylasend, '_blank')
                }
                else {
                    hylaweb.afficherNotif('ban', json.description, 'red', true)
                    Logger.debug(json.description)
                }
            });
    }

    /**
    * Envoi un message Rabbit dans la queue System pour transférer un fax par mail
    */
    var transferMail = function (objfax) {
        Logger.debug(hylaweb.hostRabbit)
        Logger.debug(hylaweb.queueSys)
        Logger.debug('Transfert du fax par mail: ', objfax.item.attr('id-fax'))
        var url_transfer_mail = api.urls['transfer_fax'].replace('#id_fax#', objfax.item.attr('id-fax')).replace('#type_trf#', 'MAIL')
        $.ajax({
            url: url_transfer_mail,
            type: 'GET',
            data: {
                hostRabbit: hylaweb.hostRabbit,
                queueSys: hylaweb.queueSys
            }
        })
            .done(function (json) {
                // si ok ouverture de outlook si hylanotify
                var content = $('#transfer-mail .content p')
                Logger.debug(json.description)
                if (json.status == "OK") {
                    content.html("Veuillez attendre quelques secondes l'ouverture de Outlook.")
                    // Affichage du message d'information
                    $('#transfer-mail').modal('show')
                }
                else {
                    hylaweb.afficherNotif('delete', json.description, "red", false)
                }
            });
    }

    /**
    * Suppression des fax
    */
    var deleteFax = function (objfax) {
        var url_delete_fax = api.urls['delete_fax'].replace('#id_fax#', objfax.item.attr('id-fax'))
        Logger.debug('suppression du fax: ', objfax)
        $.ajax({
            url: url_delete_fax,
            type: 'DELETE',
            data: {
                guid: hylaweb.user.guid_ad,
            }
        })
            .done(function (json) {
                if (json.status == "OK") {
                    objfax.item.transition({
                        animation: 'fade',
                        onComplete: function () {
                            // Si un fax succede celui qui est supprimé on le selectionne
                            if (objfax.item.hasClass("selected")) {
                                if (objfax.item.next('.item').length != 0) {
                                    hylaweb.reception.FaxList.selectFax(objfax.item.next('.item').attr('id-fax'))
                                }

                                // Sinon si un fax precede celui qui est supprimé on le selectionne
                                else if (objfax.item.prev('.item').length != 0) {
                                    hylaweb.reception.FaxList.selectFax(objfax.item.prev('.item').attr('id-fax'))
                                }
                            }
                            //On supprime le fax
                            objfax.item.remove();
                            //on verifie si on doit charger les fax suivants
                            if (hylaweb.reception.FaxList.getItemsFax().length == 14) {
                                hylaweb.lazy.loadNewContent();
                            }
                        }
                    });
                }
                else {
                    Logger.debug(json.description)
                }
            });
    }
    return self;
})();