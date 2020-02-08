hylaweb = hylaweb || {};

// TODO ameliorer le formulaire manuel
// TODO si pas de resultat afficher pas de resultat dans l'annuaire
// TODO appel ajax si focus 
$(document).ready(function () {
    hylaweb.send.init();

    //Affichage du message lors d'un changement de version, Affichage uniquement si le cookie n'existe pas
    $('.cookie.nag').nag({
        key: 'hylasend-' + $('.cookie.nag').attr('version')
    });
})

// Partie Emission
hylaweb.send = (function () {
    var self = {};

    self.init = function () {
        addPopup()

        //Initialisation du repertoire
        self.AddressBook.init()

        //Initialisation du formulaire pour ajouter un nouveau contact
        self.AddNewContact.init()

        // Initialisation de l'envoi en differe
        self.DatePicker.init()

        //Initialisation de la page de garde
        self.CoverPage.init()

        //Initialisation de la liste des destinataires
        self.ReceiverList.init()

        //Initialisation des contacts recents
        self.RecentContact.init()

        //Initialisation des tags
        self.Tag.init()

        //Initialisation du bouton d'annulation
        self.CancelFax.init()

        //Initialisation du bouton d'attente
        self.WaitFax.init()

        //Initialisation des fax en attente
        self.ListWaitingFax.init()

        //Initialisation du bouton d'envoi
        self.SendFax.init()
    }

    // Ajout des differents popup
    var addPopup = function () {
        // Popup sur l'icone +
        $('#add-manual-dest').popup({
            content: 'Ajouter un nouveau destinataire',
            position: 'top center',
            delay: {
                show: 200,
            }
        });

        // Popup sur l'envoi en differe
        $('#deferred-date').popup({
            content: 'Envoi du fax à une date différée',
            position: 'top center',
            delay: {
                show: 200,
            }
        });

        // Popup sur l'exportation
        $('#export').popup({
            content: 'Exporter les destinataires de ce fax',
            position: 'top center',
            delay: {
                show: 200,
            }
        });

        // Popup sur l'importation
        $('#import').popup({
            content: 'Importer des destinataires depuis un fichier',
            position: 'top center',
            delay: {
                show: 200,
            }
        });

        $('#search-tag .add.icon').popup({
            content: 'Ajouter un nouveau tag',
            position: 'top right',
            delay: {
                show: 200,
            }
        });
    }

    /* retourne le nombre de fax qui vont être envoyé (le fax courant + le fax mis en attente) */
    self.nbFax = function () {
        return 1 + $('#liste-fax .fax.card').length
    }

    // renvoie true si le fax est une page de garde
    self.faxIsCoverPage = function () {
        var url = window.location.href.split('/')
        faxname = url[url.length - 1]
        // Si app/send/new alors on renvoie vide
        return "new" == faxname
    }

    // Retourne le nom du fax avec l'extension demandé
    self.getFaxname = function (extension) {
        //si l'extension n'est pas demande alors on n'en met pas
        if (extension == undefined)
            extension = ''
        else
            extension = "." + extension

        var url = window.location.href.split('/')
        fax_name = url[url.length - 1]
        // Si app/send/new alors on renvoie vide
        fax_name == 'new' ? fax_name = '' : fax_name = fax_name + extension
        return fax_name
    }

    /**
    * Notification des actions faites par l'utilisateur
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



// Gestion du carnet d'adresse
hylaweb.send.AddressBook = (function () {
    var self = {};

    var $repertoire = null

    self.init = function () {
        $repertoire = $('#recherche-rep')
        searchContact()
    }

    /**
    * Champ de recherche pour le repertoire 
    */
    var searchContact = function () {
        var url_search_dest = api.urls['search_destinataire'].replace('#guid#', hylaweb.session.guid);
        $repertoire.search({
            type: 'category',
            minCharacters: 3,
            transition: 'slide down',
            showNoResults: false,
            searchOnFocus: true,
            apiSettings: {
                onResponse: function (retour) {
                    var response = {
                        results: {}
                    };
                    $.each(retour.items, function (index, item) {
                        var nomservice = item.nomservice || '', maxResults = 4;
                        if (index >= maxResults) {
                            return false;
                        }

                        // create new service category
                        if (response.results[nomservice] === undefined) {
                            response.results[nomservice] = {
                                name: nomservice,
                                results: []
                            };
                        }
                        // add result to category
                        response.results[nomservice].results.push({
                            title: item.nom,
                            description: item.fax,
                        });
                    });
                    return response;
                },
                url: url_search_dest + '?search={query}'
            },

            // Click sur une valeur
            onSelect: function (result, response) {
                // Permet de remettre a 0 le champ
                setTimeout(function () {
                    $('.prompt').val('')
                }, 1);
                var nom = result.title
                var num = result.description
                hylaweb.send.ReceiverList.add(num, nom, num)
            },
        });
    }
    return self;
})();

// Gestion des destinataires recents
hylaweb.send.RecentContact = (function () {
    var self = {};
    var $list = null

    self.init = function () {
        $list = $('#list-contact-recent')

        // si pas de contact recent on affiche le message
        if (isEmpty()) {
            $list.find('div.info').show()
        }

        // lorsqu'on ajoute un destintaire recent
        $list.on('click', '.ajout', function () {
            var $item = $(this)
            if (!$item.hasClass('disabled')) {
                var id = $item.attr('identifiant')
                var nom = $item.find('span.nom-dest').text()
                var num = $item.find('span.num-dest').text()
                hylaweb.send.ReceiverList.add(id, nom, num)
            }
        });
    }

    /**
    * Active l'envoi si la liste n'est pas vide
    */
    isEmpty = function () {
        // si on demande de check alors
        var nb_dest = $list.find('div.ajout').length
        Logger.debug(nb_dest + " contacts récents")
        if (nb_dest == 0)
            return true
        else
            return false;
    }

    return self;
})();

// Calendrier
hylaweb.send.DatePicker = (function () {
    var self = {};

    var $labelDate = null
    var $datepickerButton = null
    var datepicker = null

    self.init = function () {
        $labelDate = $('#label-date')
        $datepickerButton = $('#deferred-date')

        // Suppression de la date differe
        $labelDate.find('.delete.icon').on('click', function () {
            resetLabel()
            // remise du datepicker a la date du jour + 5min
            moment.locale('fr')
            datepicker.startDate = moment().add(5 - (moment().minute() % 5), "minutes")
            datepicker.endDate = moment().add(5 - (moment().minute() % 5), "minutes")
        });

        // Creation du datepicker
        moment.locale('fr')
        $datepickerButton.daterangepicker({
            "minYear": moment().format('YYYY'),
            // date du jour + 5min
            "minDate": moment().add(5 - (moment().minute() % 5), "minutes").format("DD/MM/YYYY, HH:mm"),
            "singleDatePicker": true,
            "showDropdowns": true,
            "showWeekNumbers": true,
            "timePicker": true,
            "timePicker24Hour": true,
            "opens": "center",
            "timePickerIncrement": 5,
            "locale": {
                "format": "DD/MM/YYYY HH:mm",
                "applyLabel": "Valider",
                "cancelLabel": "Annuler",
                "weekLabel": "S",
                "daysOfWeek": function () {
                    var defaultWeekdays = Array.apply(null, Array(7)).map(function (_, i) {
                        return moment(i, 'e').startOf('week').isoWeekday(i + 1).format('dddd');
                    })
                },
                "monthNames": moment.monthsShort(),
                "firstDay": 1
            }
        });

        // sauvegarde de l'objet datepicker
        $datepickerButton.on('show.daterangepicker', function (ev, picker) {
            datepicker = picker
        });

        // validation de la date
        $datepickerButton.on('apply.daterangepicker', function (ev, picker) {
            selectDeferedDate(picker.startDate)
        });
    }

    // Selection d'une date differe
    var selectDeferedDate = function (start) {
        resetLabel()
        $labelDate.prepend("<span>Date d'envoi: " + start.format('DD/MM/YYYY') + ' à ' + start.format('HH:mm') + "<span>").show();
        $labelDate.attr('date', start.format('YYYY-MM-DD HH:mm'))
    }

    // vide le label
    var resetLabel = function () {
        $labelDate.hide()
        $labelDate.find('span').empty()
        $labelDate.attr('date', '')

    }

    return self;
})();


// Liste des destinataires
hylaweb.send.ReceiverList = (function () {
    var self = {};
    var $list = null
    var $holder = null

    self.init = function () {
        $list = $('#list-dest')
        $holder = $('#holder')
        addListener()
    }

    var addListener = function () {
        // Suppression des destinataires
        $list.on('click', '.delete.icon', function () {
            var $item = $(this).parent()
            var id = $item.attr('identifiant')
            remove(id);
        });

        // Detecte lorsque la liste des destinataires est modifiée
        $list.on("DOMSubtreeModified", function () {
            hylaweb.send.SendFax.sendingIsPossible()
        });

        $('#import').on('click', function () {
            $('#modal-import').modal('show')
        });

        $('#export').on('click', function () {
            // on autorise l'export s'il y a des destinataires
            if (!$(this).hasClass('locked'))
                exportContact();
        });

        $holder.on('drop', function (e) {
            var file = e.originalEvent.dataTransfer.files[0]
            importContact(file)
            e.preventDefault();
        });

        $holder.on('dragover', function (e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).addClass('hover');
        });

        $holder.on('dragleave', function (e) {
            e.preventDefault();
            $(this).removeClass('hover');
        });
    }

    var exportContact = function () {
        // si on a au moins un destinataires 
        if (!self.isEmpty()) {

            // on force le telechargement du fichier en creeant un iframe caché
            $iframe = $("<iframe src='" + api.urls['export_contact']
                + "?contacts=" + encodeURIComponent(JSON.stringify(self.getReceivers())) + "' style='display: none;' ></iframe>")
            $("body").append($iframe);

            // On supprime l'iframe
            setTimeout(function () {
                $iframe.remove()
            }, 1000);
        }
    }

    var importContact = function (file) {
        var formData = new FormData()
        formData.append('file', file);
        var url_import_contact = api.urls['import_contact'];
        $.ajax({
            url: url_import_contact,
            data: formData,
            type: 'POST',
            contentType: false,
            processData: false,
        })
            .done(function (json) {
                // le fichier est bon
                if (json.status == "OK") {
                    $.each(json.items, function (index, contact) {
                        self.add(contact.fax, contact.nom, contact.fax)
                    });
                    $('#modal-import').modal('hide')
                }

                $('#holder').removeClass('hover')
            })
            .fail(function (json) {
                console.log('L\'importation ne s\'est pas effectué')
                $('#holder').removeClass('hover')
            });
    }

    /**
     * Recupere les données des destinataires (nom et numero de fax)
     */
    self.getReceivers = function () {
        var noms = [], nums = []
        //parcourt les elements ayant un identifiant
        $('#list-dest > div[identifiant]').each(function (i) {
            noms[i] = $(this).find('span.nom-dest').text()
            nums[i] = $(this).find('span.num-dest').text()
        });

        noms = noms.join(';')
        nums = nums.join(';')
        var dests = {
            "noms": noms,
            "nums": nums
        }
        return dests
    }

    var createReceiver = function (receiver) {
        // Si le destinataire n'a pas été ajouté on l'ajoute
        var $item = $("<div identifiant=\"" + receiver.id + "\" class=\"ui green label dest\">"
            + "<span class=\"nom-dest\">" + receiver.nom + "</span>"
            + "<br><span class=\"num-dest\">" + receiver.num + "</span>"
            + "<i class=\"delete icon\"></i></div>")

        //on bloque les destinataires de meme id
        $('#list-contact-recent [identifiant="' + receiver.id + '"]').addClass("disabled")

        // Sinon on re-affiche ou reaffiche à l'utilisateur le destinataire qu'il a deja selectionné
        $('#list-dest > div[identifiant="' + receiver.id + '"]').hide().fadeIn(1000)

        return $item
    }

    //Supprime l'item dans la liste final et reactive au besoin l'item dans la list des dest recents
    var remove = function (id) {
        // Suppression de l'item dans la liste des destinataires
        var $itemToDelete = $('#list-dest').find("div[identifiant=\"" + id + "\"]")
        $itemToDelete.fadeOut("slow")

        // Laisse le temps a l'item de disparaitre
        setTimeout(function () {
            $itemToDelete.remove()

            // Reactivation de l'item dans la liste des dest recents
            var $item = $('#list-contact-recent').find("div[identifiant=\"" + id + "\"]")
            $item.removeClass('disabled');
        }, 500);
    }

    //Ajoute des destinataires dans la liste final 
    self.add = function (id, nom, num) {
        receiver = {
            "id": id,
            "nom": nom,
            "num": formatNum(num)
        }

        // on verifie que le numero n'est pas dans la liste et qu'il est valide
        if (!isReceiverExist(receiver) && isReceiverValid(receiver)) {
            $list.append(createReceiver(receiver))
        }
        else {
            if (isReceiverExist(receiver)) {
                Logger.info(receiver, " se trouve deja dans la liste")
            }

            else if (!isReceiverValid(receiver)) {
                Logger.info(receiver, " n'est pas valide")
            }
        }
    }

    // on echappe les espace, les points et les virgules
    var formatNum = function (num) {
        return num.replace(new RegExp(' ', 'g'), '').replace(new RegExp('\\.', 'g'), '').replace(new RegExp(',', 'g'), '')
    }

    // Verifie si le destinataire choisi est deja présent dans la liste des destinataire
    var isReceiverExist = function (receiver) {
        // Pour chaque destinataire
        var exist = null
        $('#list-dest > div.dest').each(function () {
            if ($(this).attr('identifiant') === receiver.id) {
                exist = true;
            }
        });
        if (exist == true)
            return true

        else
            return false;
    }

    // Verifie si le destinataire est valide
    // nom d'au moins 3 caractere
    // numero de fax valide espace accepté
    var isReceiverValid = function (receiver) {
        var regex = new RegExp(/^(\+|0)?[0-9]{8,}/);
        //var regex = new RegExp(/^(\+|00)?[0-9]\ {8,}/);
        return receiver.nom.length >= 3 && regex.test(receiver.num)
    }

    /**
    * Active l'envoi si la liste n'est pas vide
    */
    self.isEmpty = function () {
        // si on demande de check alors
        var nb_dest = $('#list-dest > div.dest').length
        var div_error = $('#list-dest > div.warning')
        if (nb_dest == 0) {
            $("#export").addClass("locked")
            div_error.show()
            return true;
        }
        else {
            $("#export").removeClass("locked")
            div_error.hide()
            return false;
        }
    }

    return self;
})();

//TODO a tester/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Ajout d'un nouveau contact
hylaweb.send.AddNewContact = (function () {
    var self = {};

    var $form = null
    var $dropdown = null
    var $buttonValidation = null

    // TODO faire comme en reception pour la facturation avec un keyup et un change
    self.init = function () {

        $form = $("#form-dest")
        $dropdown = $('#add-manual-dest')
        $buttonValidation = $("#form-dest").find('.button.submit')
        $dropdown.dropdown({
            onShow: function () {
                $dropdown.popup('hide');
            }
        });

        // Desactivation de l'item qui permet de quitter le dropdown
        //TODO a voir ca
        $('.item.fluid').css('display', 'none')

        addListener()
    }

    // affiche le formulaire pour saisir un nouveau contact
    var addListener = function () {

        // Verifie si le formulaire d'ajout destinataire est valide
        //TODO modifier avec le get fields
        $("#form-dest input").on('keyup', function () {
            contactIsValid();
        });

        // Soumission de l'ajout manuel d'sun destinataire
        $form.on("submit", function (event) {
            //TODO recuperer les valeurs d'une meilleur maniere et dans une autre fonction
            var nom = $('#form-dest input[name=\"nom\"]').val()
            var num = $('#form-dest input[name=\"num\"]').val()
            hylaweb.send.ReceiverList.add(num, nom, num)

            // On reset le formulaire
            $buttonValidation.addClass('disabled')
            $('#add-manual-dest').dropdown('toggle');
            $form.form('clear')
            event.preventDefault();
        });

        setRule()
    }

    // regle pour valider le formulaire
    var setRule = function () {
        // Formulaire pour l'ajout d'un nouveau destinataire
        $form.form({
            on: 'blur',
            fields: {
                nom: {
                    identifier: 'nom',
                    rules: [
                        {
                            type: 'minLength[3]',
                            prompt: 'Veuillez entrer un nom valide'
                        }
                    ]
                },
                num: {
                    identifier: 'num',
                    rules: [
                        {
                            type: "regExp",
                            value: /^(\+|00)?[0-9]{8,}/,
                            prompt: 'Veuillez entrez un numéro valide'
                        }
                    ]
                },
            }
        });
    }

    /**
    * Lors de l'ajout manuel d'un destinataire verifie si le champs sont valide
    */
    var contactIsValid = function () {
        $form.form('validate form')
        var isFormValid = $form.form('is valid')

        if (isFormValid)
            $("#form-dest .button").removeClass("disabled")
        else
            $("#form-dest .button").addClass("disabled")
    }

    return self;
})();

//Gestion de la page de garde
hylaweb.send.CoverPage = (function () {
    var self = {};

    var $form = null
    var salut = null

    self.init = function () {
        $form = $('#form-garde')
        $checkbox = $("#page-garde")
        addListener()
        setRule()
    }

    var addListener = function () {
        // Verifie si le formulaire d'ajout destinataire est valide
        $form.form('get field', 'sujet').on('keyup', function () {
            $form.form('validate form')
            hylaweb.send.SendFax.sendingIsPossible()
        });

        // Affichage de la page de garde
        $checkbox.checkbox({
            onChange: function () {
                $form.fadeToggle(500)
                // TODO a remplacer par $formulaire.slideToggle(500)
                hylaweb.send.SendFax.sendingIsPossible();
            },

            // on rreset le formulaire s'il est caché
            onUnchecked: function () {
                $form.form('clear')
            }
        });
    }

    var setRule = function () {
        //Formulaire pour la page de garde
        $form.form({
            on: 'change',
            fields: {
                sujet: {
                     identifier: 'sujet',
                    rules: [
                        {
                            type: 'minLength[4]',
                            prompt: 'Veuillez entrer un sujet valide (au moins 4 caractères)'
                        }
                    ]
                },
            }
        });
    }

    // retourne true si la page de garde est affiche
    self.isRequested = function () {
        return $form.is(':visible')
    }

    /**
    * Verifie si le sujet de la page de garde est rempli
    */
    self.isValid = function () {
        // si page de garde affiché on check si le form est valide
        if ($checkbox.checkbox('is checked')) {
            var isFormValid = $form.form('is valid')

            if (isFormValid)
                return true;
            else
                return false;
        }

        // si pas de page de garde on valide
        else {
            return true
        }
    }

    /**
    * Retourne le sujet de la page de garde si elle est activé
    */
    self.getObject = function () {
        if ($checkbox.checkbox('is checked')) {
            return "" + $form.form('get value', 'sujet')
            //return "" + $("#garde input[name=sujet]").val()
        }
        else
            return ""
    }

    /**
     * Retourne les notes de la page de garde si elle est activé
     */
    self.getNotes = function () {
        if ($('#page-garde').checkbox('is checked')) {
            return "" + $form.form('get value', 'notes')
            //return "" + $("#garde textarea[name=notes]").val()
        }
        else
            return ""
    }

    return self;
})();

// Envoi du fax
hylaweb.send.SendFax = (function () {
    var self = {};

    sendFaxButton = null

    self.init = function () {
        sendFaxButton = $('#send-fax')
        addListener()
        addPopup()
    }

    // TODO juste changer le contenu de la popup
    var addPopup = function () {
        // si la liste des destinatiaires est vide
        if (hylaweb.send.ReceiverList.isEmpty()) {
            sendFaxButton.popup({
                preserve: true,
                content: 'Veuillez ajouter des destinataires',
                position: 'top center',
                delay: {
                    show: 50,
                },
            });
        }

        // si la page de garde n'est pas valide
        else if (!hylaweb.send.CoverPage.isValid()) {
            sendFaxButton.popup({
                preserve: true,
                content: 'Veuillez ajouter une page de garde',
                position: 'top center',
                delay: {
                    show: 50,
                },
            });
        }

        //si il y a trop de fax en attente
        else if (hylaweb.send.ListWaitingFax.tooMuchFax()) {
            sendFaxButton.popup({
                preserve: true,
                content: 'Vous disposez de trop de fax en attente',
                position: 'top center',
                delay: {
                    show: 50,
                },
            });
        }

        // sinon suppression de la popup
        else {
            sendFaxButton.popup('destroy');
        }
    }

    var addListener = function () {
        sendFaxButton.on('click', function () {
            // si le bouton est debloquer
            if (!$(this).hasClass('locked')) {

                // si pas de fax en attente pas de modal
                if (hylaweb.send.ListWaitingFax.isEmpty()) {
                    sendFax()
                }
                else {
                    $('#modal-envoi .contenu span').text(hylaweb.send.nbFax() == 1 ? text = "1 fichier" : hylaweb.send.nbFax() + " fichiers")
                    $('#modal-envoi').modal({
                        onApprove: function ($element) {
                            // Laisse le temps au modal de s'enlever
                            setTimeout(function () {
                                sendFax()
                            }, 300);
                        }
                    }).modal('show');
                }
            }
        });
    }

    // renvoi la date differe si demande
    var getDateDiff = function () {
        return $('#label-date').attr('date')
    }

    /** Recupere le nom du fax courant avec l'extension */
    var getFilename = function () {
        var filename

        var url_check_fax_ps_exist = api.urls['check_fax_ps_exist'].replace('#FAXNAME#', hylaweb.send.getFaxname('ps'));
        $.ajax({
            async: false,
            url: url_check_fax_ps_exist,
            type: 'GET',
        })
            .done(function (json) {
                //si le fichier .ps existe on le recupere
                if (json.status == "OK")
                    filename = hylaweb.send.getFaxname('ps')
                else
                    //sinon on recupere en pdf
                    filename = hylaweb.send.getFaxname('pdf')
            })
            .fail(function (json) {
                console.log(json)
            });
        return filename
    }

    /** Envoi du fax a l'api avec les destinataires et le nom du fax */
    var sendFax = function () {
        var url_envoie_fax = api.urls['envoi_fax'];

        var dataPOST = {
            sender_guid: hylaweb.session.guid,
            fax_tag: hylaweb.send.Tag.getTags(),
            dest_num: hylaweb.send.ReceiverList.getReceivers().nums,
            dest_name: hylaweb.send.ReceiverList.getReceivers().noms,
            fax_coversubject: hylaweb.send.CoverPage.getObject(),
            fax_covernotes: hylaweb.send.CoverPage.getNotes(),
            //filewait: hylaweb.send.ListWaitingFax.getFileWait()
        }

        // si le fax est different d'une page de garde
        if (window.location.href.split('/').pop() != "new")
            dataPOST.filename = getFilename() + ";" + hylaweb.send.ListWaitingFax.getFileWait()

        // TODO temporaire pour differencier l'envoi d'une page de garde avec fichier joints
        // Si page de garde + envoi de ficher joint
        //else if (window.location.href.split('/').pop() == "new" && hylaweb.send.ListWaitingFax.getFileWait() != "")
            //dataPOST.filename = "new" + ";" + hylaweb.send.ListWaitingFax.getFileWait()

        // si une date différé est demandé
        if ($('#label-date').is(':visible'))
            dataPOST.fax_datetime_dif = getDateDiff()

        // si pas de destinataires
        if (dataPOST.dest_num == "" || dataPOST.dest_name == "")
            hylaweb.send.afficherNotif("delete", "Vous n'avez pas saisi de destinataires", "red", true)

        else {
            Logger.debug(dataPOST)
            $.ajax({
                url: url_envoie_fax,
                data: dataPOST,
                type: 'post',
            })
                .done(function (json) {
                    // si l'envoi c'est bien passe
                    console.log(json)
                    if (json.status == 'OK') {
                        hylaweb.send.afficherNotif("check", "Fax envoyé, vous pouvez quitter la page", "green", false)
                    }

                    // sinon erreur dans l'envoi
                    else {
                        hylaweb.send.afficherNotif("delete", "Fax non envoyé: " + json.description + " , veuillez réessayer ultérieurement", "red", true)
                    }
                })
                .fail(function () {
                    $('.ui.basic.modal.erreur').modal({
                        closable: false
                    }).modal('show')
                    hylaweb.send.afficherNotif("delete", "Fax non envoyé, Veuillez réessayer", "red", true)
                })
        }
    }

    /**
    * Fonction qui determine si oui ou non l'envoi est possible
    */
    self.sendingIsPossible = function () {
        // test si au moins un destinataires et rensigné && et lorsque la page de garde est necessaire elle doit etre valide
        // && si la liste de fax en attente n'excede pas la limite des fax
        if (!hylaweb.send.ReceiverList.isEmpty() && hylaweb.send.CoverPage.isValid() && hylaweb.send.ListWaitingFax.isValid()) {
            sendFaxButton.removeClass('locked')
        }
        else {
            // on bloque le bouton d'envoi et l'export
            sendFaxButton.addClass('locked')
        }
        // modifie la popup
        addPopup()
    }

    return self;
})();

// Annulation du fax
hylaweb.send.CancelFax = (function () {
    var self = {};

    self.init = function () {
        // click sur l'annulation d'un fax
        $('#cancel-fax').on('click', function () {
            cancelFax();
        });
    }

    //Envoi une requete de type delete pour supprimer le fax
    var cancelFax = function () {
        var fax_name = hylaweb.send.getFaxname('pdf')
        // si ce n'est pas un nouveau fax
        if (fax_name != '') {
            var url_annuler_fax = api.urls['annuler_fax'].replace("#faxname#", fax_name)

            $.ajax({
                url: url_annuler_fax,
                type: 'delete'
            })
                .done(function (json) {
                    // si un probleme avec le fax
                    if (json.status != 'OK') {
                        $('.ui.basic.modal.notif').modal({
                            closable: true
                        }).modal('show');
                    }
                    else if (json.status == 'OK') {
                        hylaweb.send.afficherNotif('check', "Le fax a été annulé.<br/>Vous pouvez quitter la page", "green", false)
                    }
                })
                .fail(function () {
                    hylaweb.send.afficherNotif('delete', "Erreur de connexion", "red", true)
                })
        }
        else {
            hylaweb.send.afficherNotif('check', "Le fax a été annulé.<br/>Vous pouvez quitter la page", "green", false)
        }
    }
    return self;
})();

// Bouton de Mise en attente du fax
hylaweb.send.WaitFax = (function () {
    var self = {};

    var $wait = null
    self.init = function () {
        $wait = $('#waiting-fax')
        addPopup()
        addListener()
        // on desactive le bouton si ce n'est pas une page de garde ou si la limte en nombre de fax est atteinte
        if (hylaweb.send.faxIsCoverPage() || hylaweb.send.ListWaitingFax.tooMuchFax()) {
            $wait.addClass('locked')
        }
    }

    var addPopup = function () {
        // si le fax a envoye est une page de garde
        if (hylaweb.send.faxIsCoverPage()) {
            $wait.popup({
                preserve: true,
                content: 'Vous ne pouvez pas mettre une page de garde en attente',
                position: 'top center',
                delay: {
                    show: 50,
                }
            });
        }

        // si la limite du nombre de fax est atteinte 
        else if (hylaweb.send.ListWaitingFax.tooMuchFax()) {
            $wait.popup({
                preserve: true,
                content: 'Vous ne pouvez plus mettre en attente de fax',
                position: 'top center',
                delay: {
                    show: 50,
                },
            });
        }
    }

    var addListener = function () {
        // si ce n'est pas une page de garde, et qu'on n'a pas atteint la limit en terme de fax en attente alors on peut mettre en attente
        $wait.on('click', function () {
            if (!hylaweb.send.faxIsCoverPage() && !hylaweb.send.ListWaitingFax.tooMuchFax() && !$(this).hasClass('locked')) {
                waitFax();
            }
            else {
                console.log('yo')
            }
        });
    }

    self.activeButton = function () {
        $wait.removeClass('locked')
        $wait.parent().popup('destroy')
    }

    // Mise en attente du fax
    var waitFax = function () {
        var url_standing_by = api.urls['standing_by'];
        $.ajax({
            url: url_standing_by,
            data: {
                filename: hylaweb.send.getFaxname()
            },
            type: 'POST',
        })
            .done(function (json) {
                console.log(json)

                if (json.status == 'OK')
                    hylaweb.send.afficherNotif("clock outline", "Le fax a été mis en attente, vous pouvez quitter la page", "orange", false)
                else
                    hylaweb.send.afficherNotif("delete", "Erreur: " + json.description + ", veuillez réessayer", "red", true)
            })
            .fail(function (json) {
                hylaweb.send.afficherNotif("delete", "'La mise en attente ne s\'est pas faite', veuillez réessayer ultérieurement", "red", true)
            });
    }
    return self;
})();



// Liste des fax en attente
hylaweb.send.ListWaitingFax = (function () {
    var self = {};
    var $list

    self.init = function () {
        $list = $('#liste-fax')
        loadFax()
        addListener()

    }

    // charge la premiere page de chaque fax
    var loadFax = function () {
        $('#liste-fax > .fax.card').each(function () {
            hylaweb.send.WaitingFax.init($(this))
        });
    }

    var addListener = function () {
        // Detecte lorsque la liste des fax est modifiée
        $list.on("DOMSubtreeModified", function () {
            // on verifie si l'envoi est possible
            hylaweb.send.SendFax.sendingIsPossible()

            // s'il n'y a plus de fax on cache la side barre
            if (self.isEmpty()) {
                hideList()
            }

            // si le nombre de fax est inferieur a 9 on peut mettre en attente
            else if (!self.tooMuchFax()) {
                hylaweb.send.WaitFax.activeButton()
            }
        });
    }

    // cahce la liste si il n'y a plus de fax en attente
    var hideList = function () {
        $list.animate({
            left: '-500px', //on le sort de l'ecran
        }, 1000, function () {
            $list.remove()
        });
    }

    self.getFileWait = function () {
        files = []
        // si il y a des fax en attente on les ajoute dans la liste
        $('#liste-fax > .fax.card').each(function (i) {
            files.push($(this).attr('file'))
        });
        return files.join(';')
    }

    // retourne le nombre de fax a envoyer
    //TODO a modifier pour tester les fax requis + page de garde
    var getNBFax = function () {
        return $('#liste-fax .fax.card').length
    }


    // Retourne true si l'utilisateur a déjà le nombre maximal de fax en attente
    self.tooMuchFax = function () {
        return getNBFax() >= conf.LIMIT_WAITING_FAX
    }

    //retourne true si l'utilisateur peut envoyer les fax en attente
    self.isValid = function () {
        return getNBFax() <= conf.LIMIT_WAITING_FAX
    }

    // retourne true si il n'y aucun fax en attente
    self.isEmpty = function () {
        return getNBFax() == 0
    }

    return self;
})();

// represente un fax en attente
hylaweb.send.WaitingFax = (function () {
    var self = {};

    self.init = function ($fax) {
        var objfax = {}
        objfax.item = $fax;
        objfax.image = objfax.item.find('.image')
        objfax.img = objfax.item.find('.image img')
        objfax.deleteIcon = objfax.item.find('.image i.delete.icon')
        objfax.id = objfax.item.attr('id');
        objfax.file = objfax.item.attr('file');
        loadImg(objfax)
        setIconPosition(objfax)
        addListener(objfax)
    }

    // On charge l'image du fichier grace a une api
    var loadImg = function (objfax) {
        objfax.img.attr('src', api.urls['thumbnails_fax'] + '?file=' + objfax.file)
    }

    // positionnement de l'icone en fonction de la taille de l'image
    var setIconPosition = function (objfax) {
        // on verifie que le fax est chargé
        var interval = setInterval(function () {
            if (isLoaded(objfax.img)) {
                Logger.debug('le fax d\'id ' + objfax.id + ' est chargé')
                // si le fax est en mode paysage
                if (isLandScape(objfax.img)) {
                    Logger.debug("fax", objfax.item, "en mode paysage")
                    objfax.deleteIcon.css('margin-top', '-55%')
                }
                // si le fax est en mode portrait
                else {
                    Logger.debug("fax", objfax.item, "en mode portrait")
                    objfax.deleteIcon.css('margin-top', '-140%')
                }
                // affichage de l'icone
                objfax.deleteIcon.show()
                clearInterval(interval)
            }
        }, 1000)
    }

    var addListener = function (objfax) {
        // affichage du dimmer
        objfax.image.dimmer({ on: 'hover' })

        // affichage de la popup de confirmation
        objfax.deleteIcon.on('click', function () {
            $fax = $(this).parents('.fax.card')
            $('#modal-delete').modal({
                onApprove: function ($element) {
                    supprimerFax($fax)
                }
            }).modal('show');
        })
    }

    // verifie si l'image du fax est chargé
    var isLoaded = function (img) {
        return img.width() != 0 && img.height() != 0
    }

    // true si le fax est en mode paysage
    var isLandScape = function (img) {
        return img.width() > img.height()
    }

    // supprime un fax en attente
    var supprimerFax = function ($fax) {
        url_delete_fax = api.urls['standing_by'];
        $.ajax({
            url: url_delete_fax,
            data: {
                filename: $fax.attr('id')
            },
            type: 'DELETE',
        })
            .done(function (json) {
                console.log(json)

                if (json.status == 'OK') {
                    $fax.slideUp("slow")

                    // Laisse le temps a l'item de disparaitre
                    setTimeout(function () {
                        $fax.remove()
                    }, 500);
                }

                else
                    hylaweb.send.afficherNotif("delete", "Echec de la suppression, veuillez réessayer", "red", true)
            })
            .fail(function (json) {
                hylaweb.send.afficherNotif("delete", "Impossible de supprimer le fax", "red", true)
            });
    }

    return self;
})();


// Gestion des tags
// TODO utiliser la methode ajout tag dans la partie dropdown pour customiser le tag
hylaweb.send.Tag = (function () {
    var self = {};

    var $list = $('#list-tag')

    self.init = function () {
        $list = $('#list-tag')
        searchTag()
        addListener()
    }

    //Champ de recherche pour les tags
    var searchTag = function () {
        var $tags = $('#search-tag')
        var url_search_tag = api.urls['search_tag'].replace('#guid#', hylaweb.session.guid);
        $tags.dropdown({
            apiSettings: {
                url: url_search_tag + '?search={query}'
            },
            filterRemoteData: true,
            allowAdditions: true,
            minCharacters: 3,
            fields: {
                remoteValues: 'items',
                name: 'tag',
                value: 'tag',
            },
        });
    }

    var addListener = function () {
        // si la touche entree est saisi on entre le tag
        $("#search-tag").on('keypress', function (event) {
            if (event.which == 13) {
                $("#search-tag .link.icon").trigger('click')
            }
        });

        // Ajout d'un tag
        $("#search-tag .link.icon").on('click', function () {
            var input_tag = $("#search-tag input")

            //si le tag n'est pas vide on peut l'ajouter
            if (input_tag.val()) {
                addTag(input_tag.val())
                input_tag.val('')
            }
        });

        // Suppression d'un tag
        $('#list-tag').on('click', '.delete.icon', function () {
            var $item = $(this).parent()
            $item.remove()
        });
    }

    // Creation de la balise tag
    var createTag = function (tag) {
        var $item = $("<div class=\"ui teal label tag\">"
            + "<span class=\"nom-tag\">" + tag + "</span>"
            + "<i class=\"delete icon\"></i></div>")

        return $item
    }

    //Ajout de l'item dans la liste
    var addTag = function (tag) {
        $list.append(createTag($item))
    }

    /** 
     * Retourne les tags saisi par l'utilisateur 
     */
    self.getTags = function () {
        var tags = []
        $('#search-tag > a[data-value]').each(function (i) {
            tags[i] = $(this).attr('data-value')
        });
        tags = tags.join(',');
        console.log(tags)
        return tags
    }

    return self;
})();