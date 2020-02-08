
var hylaweb = hylaweb || {}
//TODO faire les popup sur le destinataire si trop long
//TODO detection si les fax existe ou pas
// Partie Emission
hylaweb.archive = (function () {
    var self = {};

    self.startDate = null
    self.endDate = null
    self.service = null
    self.type_fax = null
    self.tags = null

    self.init = function () {

        // On creer le menu des services et des agences
        self.MenuServices.CreateMenu();

        // Initialisation du formulaire
        initForm();

        // Initialisation du calendrier
        self.DatePicker.init()

        // Initialisation du type de fax
        self.TypeFax.init()

        // Initialisation des tags
        self.Tag.init()

        self.FaxList.init()
    }

    var initForm = function () {
        $search = $('#search')
        $search.form({
            fields: {
                date: "empty"
            },
        });

        $search.on("submit", function (event) {
            // on cancel le submit pour ne pas refresh la page
            event.preventDefault();
            search();
        });
    }

    self.getIdService = function () {
        return self.MenuServices.getIdService()
    }

    // demande a l'api les fax avec les donnees 
    var search = function () {
        self.startDate = self.DatePicker.getStartDate()
        self.endDate = self.DatePicker.getEndDate()
        self.service = self.getIdService()
        self.type_fax = self.TypeFax.getType()
        self.tags = self.Tag.getTags()

        var url_archive = api.urls['archive'].replace("#type_fax#", self.type_fax) + "/" + conf.LIMIT_ARCHIVE_FAX
        $.ajax({
            url: url_archive,
            type: 'get',
            data: {
                start_date: self.startDate,
                end_date: self.endDate,
                service: self.service,
                tag: self.tags
            }
        })
            .done(function (json) {
                self.FaxList.updateList(json)
            });
    }

    return self;
})();

hylaweb.archive.Tag = (function () {
    var self = {}

    self.init = function () {
        addPopup()
        searchTag()

        $("#search-tag").on('keypress', function (event) {
            if (event.which == 13) {
                $("#search-tag .link.icon").trigger('click')
            }
        });

        // Suppression d'un tag
        $('#list-tag').on('click', '.delete.icon', function () {
            var $item = $(this).parent()
            $item.remove()
        });
    }

    var addPopup = function () {
        $('#search-tag .add.icon').popup({
            content: 'Ajouter un nouveau tag',
            position: 'top right',
            delay: {
                show: 200,
            }
        });
    }

    var searchTag = function () {
        var url_search_tag = api.urls['search_tag'].replace('#guid#', hylaweb.session.guid);
        $('#search-tag').dropdown({
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

    /*
    * Retourne les tags saisi par l'utilisateur 
    */
    self.getTags = function () {
        var tags = []
        $('#search-tag > a[data-value]').each(function (i) {
            tags[i] = $(this).attr('data-value')
        });
        tags = tags.join(',');
        return tags
    }

    return self;
})();

// Calendrier
hylaweb.archive.DatePicker = (function () {
    var self = {};

    var $input = null
    var $datepicker = null
    self.init = function () {
        $input = $('#dates input')
        $datepicker = $('#dates')

        moment.locale('fr');
        // par defaut on configure un intervalle de 1 semaines pour la date
        selectDate(moment().subtract(1, 'week'), moment())

        // initialisation du calendrier
        moment.locale('fr')
        $datepicker.daterangepicker({
            "minYear": 2000,
            "alwaysShowCalendars": true,
            "showDropdowns": true,
            "showWeekNumbers": true,
            "startDate": moment().subtract(1, 'week').format('DD/MM/YYYY'),
            "endDate": moment().format('DD/MM/YYYY'),
            "opens": "center",
            ranges: {
                'Aujourd\'hui': [moment(), moment()],
                'Hier': [moment().subtract(1, 'days'), moment()],
                'Les 7 derniers jours': [moment().subtract(6, 'days'), moment()],
                'Ce mois-ci': [moment().startOf('month'), moment().endOf('month')],
                'Le mois dernier': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
                'Cette année': [moment().startOf('year'), moment().endOf('year')],
                'L\'année dernière': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
            },
            "showCustomRangeLabel": false,
            "locale": {
                "format": "DD/MM/YYYY",
                "separator": " - ",
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

        }, function (start, end, label) {
            selectDate(start, end)
        });
    }

    self.getStartDate = function () {
        return $input.attr('date-deb')
    }

    self.getEndDate = function () {
        return $input.attr('date-fin')
    }

    var selectDate = function (start, end) {
        Logger.debug('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
        $('#dates input').val(start.format('D MMMM YYYY') + ' - ' + end.format('D MMMM YYYY'));
        $('#dates input').attr('date-deb', start.format('YYYY-MM-DD'))
        $('#dates input').attr('date-fin', end.format('YYYY-MM-DD'))
    }

    return self;
})();

hylaweb.archive.TypeFax = (function () {
    var self = {};

    var $type = null

    self.init = function () {
        $type = $('#type')
        $type.dropdown()
    }

    self.getType = function () {
        return $type.dropdown('get value')
    }

    return self;
})();

// Menu pour la liste des services
hylaweb.archive.MenuServices = (function () {
    var self = {};

    var $service_current = null
    var $agence = null

    self.CreateMenu = function (json) {

        $service_current = $('#service-current')
        $agence = $('#agence')

        var url_services = api.urls['services'].replace('#guid#', hylaweb.user.guid_ad)
        $.ajax({
            url: url_services,
            async: false,
            type: 'get'
        })
            .done(function (json) {
                var default_service = json.items.service_defaut

                var $list_agence = $('#liste-agence')

                self.updateService(default_service.service, default_service.serviceid, default_service.agence)

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
                        self.Service.init($service)
                    });
                });

                // Active le dropdown pour les services
                $('#dropdown-service').dropdown();
            })
    }

    self.updateService = function (service, id_service, agence) {
        $service_current.text(service).attr('idService', id_service)
        $agence.text(agence)
        $('#label-service').val(agence + " --- " + service)
    }

    self.getIdService = function () {
        return $service_current.attr('idService')
    }
    return self;
})()

hylaweb.archive.MenuServices.Service = (function () {
    var self = {};
    self.$service = null
    self.init = function ($service) {
        self.$service = $service

        self.$service.on('click', function () {
            hylaweb.archive.MenuServices.updateService($(this).text(), $(this).attr('idservice'), $(this).attr('agence'))
        })
    }
    return self;
})();


/**
* Représente la liste des fax
*/
hylaweb.archive.FaxList = (function () {
    var self = {};
    var liste_fax

    self.init = function () {
        liste_fax = $('#liste-fax')
    }

    // retourne la liste de fax
    self.getItems = function () {
        return liste_fax.find('.fax.card')
    }

    // retourne le fax selectionné
    self.getFaxSelected = function () {
        return liste_fax.find('.fax.card.selected')
    }

    // Met a jour la liste
    self.updateList = function (json) {
        reset()
        // on recupere les fax et le type RX ou TX
        $.each(json.items.fax, function (i, fax) {
            self.AddAppendFax(fax, json.items.type)
        });

        var div_error = $('div.warning')
        // si pas de resultat
        if (isEmpty()) {
            div_error.removeClass('hidden')
        }
        else {
            div_error.addClass('hidden')
        }
        hylaweb.lazy.reset();
    }

    /**
     * Ajoute un fax en fin de liste
     */
    self.AddAppendFax = function (fax, type) {
        $fax = CreateFax(fax, type)
        liste_fax.append($fax)
        hylaweb.archive.Fax.init($fax, type)
    }

    // Construit le fax pour l'affichage
    var CreateFax = function (fax, type) {
        Logger.debug(fax)

        // Pour un fax en reception
        if (type == "RX")
            card = hylaweb.archive.Fax.createCardRX(fax)

        // Pour un fax en emission
        else if (type == "TX")
            card = hylaweb.archive.Fax.createCardTX(fax)


        // On initialise l'objet fax
        $fax = $(card)

        return $fax
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
        $('#chargement').find('.loader').removeClass('active')
        liste_fax.empty()
    }

    // Recupere l'id du fax par rapport a l'item
    var getIdFax = function ($item) {
        return liste_fax.find($item).attr('id-fax')
    }
    return self;
})();


/**
 * Un fax
 */
hylaweb.archive.Fax = (function () {
    var self = {};

    self.init = function ($item, type) {
        var objfax = {}

        objfax.item = $item;
        objfax.image = objfax.item.find('.image.firstpage-fax')
        objfax.rapportEmitButton = objfax.item.find('i.file.outline')
        objfax.avatar = objfax.item.find('.avatar')
        objfax.type = type
        addListener(objfax);
        addPopup(objfax)
    }

    var addPopup = function (objfax) {
        // si le nom est plus grand que la carte
        if (objfax.item.find('.header').width() < objfax.item.find('.nom-sender').width()) {
            objfax.item.find('.header').popup({
                content: objfax.item.find('.nom-sender').text(),
                position: 'top center'
            })
        }

        //ajout des popup
        objfax.avatar.popup({
            content: objfax.avatar.attr('data-prop'),
            position: 'right center',
        });
    }

    var addListener = function (objfax) {
        // click sur l'image pour visualiser le fax
        objfax.image.on('click', function () {
            getPDF(objfax)
        })

        // bouton pour visualiser le rapport d'emission pour les fax en emission
        objfax.rapportEmitButton.on('click', function () {
            getRappEmission(objfax)
        })
    }

    // retourne l'element card commune au fax en emission et en reception
    var createCard = function (fax, type) {
        // ajout d'une partie de la source des images
        source = api.urls['archive_file']
            .replace("#type_fax#", type)
            .replace("#idFax#", fax.id)
            .replace("#format#", "jpeg") + "?guid=" + hylaweb.session.guid
            
        // Ajout de la page
        //moment.locale('fr');
        var page = (fax.npages == null || fax.npages == 0) ? page = "" :
            fax.npages == 1 ? page = "1 page&nbsp&nbsp&nbsp&nbsp" : page = fax.npages + " pages&nbsp&nbsp&nbsp&nbsp"
        var Page = "<span class=\"page\">" + page + "</span><br/>"
        $card = $("<div id=\"" + fax.id + "\" class=\"fax card\">"
            + "     <div class=\"image firstpage-fax\">"
            + "         <img src=\"" + source + "\">"
            + "     </div>"
            + "     <div class=\"content\">"
            + "         <div class=\"header\"><span class=nom-sender></span></div>"
            + "         <div class=\"meta\">"
            + "             <div class=\"date\">" + moment(fax.date).format("ddd DD MMM YYYY HH:mm") + "</div>"
            + "             <div><span class=\"page\">" + page + "</div>"
            + "         </div>"
            + "         <div class=\"description\">"
            + "         </div>"
            + "     </div>"
            + "     <div class=\"extra content\">"
            + "     </div>"
            + " </div>"
        )


        var Tag = ""
        // Si on a des tags on les ajoute
        if (fax.tag.length != 0 && fax.tag[0] != "") {
            Tag = "<i class=\"tag icon\"></i>"
            for (var index_tag in fax.tag) {
                var tag = fax.tag[index_tag]
                // Si le tag n'est pas vide
                if (tag != "")
                    //TODO ajouter
                    //Tag += "<div class=\"tag-label tag ui blue small label\">" + tag + "</div>"
                    Tag += "<div class=\"tag-label ui blue small label\">" + tag + "</div>"
            }
        }

        // ajout des tags et du nombre de page
        $card.find('.content .description').append(Tag)

        //ajoute la popup si le nom est trop long

        var sendername = ""
        if (fax.name == 0)
            // espace insecable
            sendername = "&#8239"

        // si le nom est bon
        else
            sendername = fax.name

        $card.find('.nom-sender').html(sendername)

        $header = $card.find('.header')
        $sender = $card.find('.nom-sender')


        return $card
    }

    // Creation d'une carte fax en reception
    self.createCardRX = function (fax) {
        $card = createCard(fax, 'RX')
        avatar = createAvatar(fax.proprietaire)

        // Ajout du contenu different pour le fax en reception
        $card.find('.extra.content').append(avatar)

        return $card
    }

    // Creation d'une carte fax en emission
    self.createCardTX = function (fax) {

        avatar = createAvatar(fax.proprietaire)
        $card = createCard(fax, 'TX')
        // Ajout du contenu different
        $card.find('.extra.content').append(avatar)
        $card.find('.extra.content').append("<span class=\"right floated\"><i class=\"file outline icon\" title=\"Visualiser rapport d'émission\"></i></span>")

        color = ''
        if (fax.status == "OK")
            color = " green"

        else if (fax.status == "ER")
            color = " red"

        else
            color = ""


        $card.addClass(color)

        return $card
    }

    // Creer le code html pour le proprietaire du fax
    var createAvatar = function (proprietaire) {
        var data_prop = ""
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

    /* Appel a l'api pour recuperer le fax */
    var getPDF = function (objfax) {
        var url = encodeURIComponent(api.urls['archive_file']
            .replace("#type_fax#", objfax.type)
            .replace("#idFax#", objfax.item.attr('id'))
            .replace("#format#", "pdf") + "?guid=" + hylaweb.session.guid)
        window.open("../static/pdfjs/web/viewer.html?file=" + url, 'archivePDF');
    }

    /* Appel a l'api pour recuperer le rapport d'emission du fax */
    var getRappEmission = function (objfax) {
        var url = encodeURIComponent(api.urls['archive_file']
            .replace("#type_fax#", objfax.type)
            .replace("#idFax#", objfax.item.attr('id'))
            .replace("#format#", "pdf") + "?guid=" + hylaweb.session.guid + "&type=rapport")
        window.open("../static/pdfjs/web/viewer.html?file=" + url, 'archivePDF');
    }


    return self;
})();


$(document).ready(function () {
    hylaweb.archive.init()

    // on recupere tous les fax
    hylaweb.lazy.init($('.column'), 'arc');
});




