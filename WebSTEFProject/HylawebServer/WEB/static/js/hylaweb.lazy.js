// fichier div-manager.js

var hylaweb = hylaweb || {}

// on peut créer le module enfant
hylaweb.lazy = (function () {
    /* ... */
    var self = {};
    var loading = false;
    var endfax = false;
    var liste = undefined;
    self.type = undefined

    self.init = function (el, type) {
        liste = el;
        liste.on('scroll', function () {
            //console.log('scroll : ' + ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight))
            //console.log('scrolltop:' + $(this).scrollTop() + ' innerHeight:' + $(this).innerHeight() + ' scrollHeight:' + $(this)[0].scrollHeight )
            if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight && $(this).scrollTop() > 0) {
                if (type == "rx"){
                    self.loadNewContentRX();//call function to load content when scroll reachs DIV bottom
                }
                else if (type == "tx"){
                    self.loadNewContentTX();//call function to load content when scroll reachs DIV bottom       
                }
                else if (type == "arc"){
                    self.loadNewContentArchive();//call function to load content when scroll reachs DIV bottom       
                }
                             
            };
        });
    };

    // stop l'affichage des fax de maniere dynamique utilisé lors du filtering des fax
    self.stop = function () {
        liste.off('scroll')
        self.reset()
    }

    // reinitialisation lors du changement de service
    self.reset = function () {
        liste.scrollTop(0)
        loading = false;
        endfax = false;
    }

    // appeler cette fonction lors de la suppression d'un fax si le nb de fax < valeur
    self.loadNewContentRX = function () {
        if (!loading && !endfax) {
            var dataGet = {
                guid: hylaweb.session.guid,
            }
            
            // Filtre les fax pour l'utilisateur
            if ($('#filter-fax').checkbox('is checked')) {
                dataGet.proprietaire = hylaweb.user.prenom + " " + hylaweb.user.nom + " <" + hylaweb.user.mail + ">";
            }

            loading = true;
            // affichage du loader
            var loader = $('<div class="lazy ui inline centered active text loader">Chargement...</div>').appendTo("#liste-fax");
            // récupération du dernier FAX
            // pour répurer le dernier ID du fax et la dernière date (jour) du FAX
            var lastIdfax = $("#liste-fax .fax.item:last").attr('id-fax')
            var id_service = hylaweb.getIdServiceCurrent()
            // faire appel AJAX à l'API ici pour récupérer les fax suivant
            // Faire test du retour de l'ajax (nb de fax retourné)
            var url_rx_fax = hylaweb.api.urls['rx_fax'].replace("#id_serv#", id_service) + "/" + conf.LIMIT_RX_FAX + "/" + lastIdfax
            $.ajax({
                url: url_rx_fax,
                type: 'get',
                data: dataGet
            })
                .done(function (json) {
                    //console.log(json.items.length)
                    if (json.items.length == 0) {
                        // plus de fax a charger
                        endfax = true;
                        $('<div class="ui separator grey attached center aligned inverted segment">Fin de la liste</div>').appendTo('#liste-fax');
                    } else {
                        $.each(json.items, function (i, fax) {
                            hylaweb.reception.FaxList.AddAppendFax(fax)
                        });
                    }
                    // TODO ajout des separateurs
                    //hylaweb.reception.FaxList.insertSeparator()
                    loader.remove()
                    loading = false
                });
        }
    }

    /**  lazy en emission */
    self.loadNewContentTX = function () {
        if (!loading && !endfax) {
            loading = true;
            // affichage du loader
            var loader = $('<div class="lazy ui inline centered active text loader">Chargement...</div>').appendTo("#liste-fax");
            // récupération du dernier FAX
            // pour répurer le dernier ID du fax et la dernière date (jour) du FAX
            var lastIdfax = $("#liste-fax .fax.item:last").attr('id-fax')
            var id_service = hylaweb.emission.getIdDefaultService();
            // faire appel AJAX à l'API ici pour récupérer les fax suivant
            // Faire test du retour de l'ajax (nb de fax retourné)
            var url_tx_fax = hylaweb.api.urls['tx_fax'].replace("#id_serv#", id_service) + "/" + conf.LIMIT_TX_FAX + "/" + lastIdfax
            $.ajax({
                url: url_tx_fax,
                type: 'get',
            })
                .done(function (json) {
                    //console.log(json.items.length)
                    if (json.items.length == 0) {
                        // plus de fax a charger
                        endfax = true;
                        $('<div class="ui separator grey attached center aligned inverted segment">Fin de la liste</div>').appendTo('#liste-fax');
                    } else {
                        $.each(json.items, function (i, fax) {
                            hylaweb.emission.FaxList.AddAppendFax(fax)
                        });
                    }
                    loader.remove()
                    loading = false
                });
        }
    }

     /**  lazy en archive */
     self.loadNewContentArchive = function () {
        if (!loading && !endfax) {
            loading = true;
            // affichage du loader
            var loader = $('<div class="lazy ui inline centered active text loader">Récupération des archives</div>').appendTo("#liste-fax");
            // récupération du dernier FAX
            // pour répurer le dernier ID du fax et la dernière date (jour) du FAX
            // Recuperation du type emission ou reception
            var lastIdfax = $("#liste-fax .fax.card:last").attr('id')
    
            var url_archive_fax = api.urls['archive'].replace("#type_fax#", hylaweb.archive.type_fax) + "/" + conf.LIMIT_ARCHIVE_FAX + "/" + lastIdfax
            $.ajax({
                url: url_archive_fax,
                type: 'get',
                data:{
                    start_date: hylaweb.archive.startDate,
                    end_date: hylaweb.archive.endDate ,
                    service: hylaweb.archive.service,
                    tag: hylaweb.archive.tags
                }
            })
                .done(function (json) {
                    if (json.items.length == 0) {
                        // plus de fax a charger
                        endfax = true;
                        $('<div class="ui separator grey attached center aligned inverted segment">Fin de la liste</div>').appendTo('#liste-fax');
                    } else {
                        $.each(json.items.fax, function (i, fax) {
                            hylaweb.archive.FaxList.AddAppendFax(fax, json.items.type)
                        });
                    }
                    loader.remove()
                    loading = false
                });
        }
    }

    return self
})();


