var hylaweb = hylaweb || {};

$(document).ready(function () {
    //TODO faire en sorte que mes items soit des modules en y implementant leur fonction
    //faire un logger custom

    // Activation du dropdown pour ajouter les champs de texte 
    dropdown_destinataire();

    //gestion des forumlaires
    gestion_formulaires();

    // Mise en place des champs de recherches
    search_repertoire();
    search_tag()

    // Ajout des listener
    add_listener()

    // Gestion des popups
    activation_popup()

    // Gestion du nag
    gestion_nag();
});

/**
 * Affichage du message lors d'un changement de version,
 * Affichage uniquement si le cookie n'existe pas
 */
function gestion_nag() {
    $('.cookie.nag').nag({
        key: 'nag' + $('.cookie.nag').attr('version'),
    });
}

// Ajout des differents popup
function activation_popup() {
    // Popup sur l'icone +
    $('#add-manual-dest').popup({
        content: 'Ajouter un nouveau destinataire',
        position: 'top right',
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

/**
 * Gere le dropdown pour l'ajout des destinataires
 */
function dropdown_destinataire() {
    $('#add-manual-dest').dropdown({
        onShow: function () {
            $('#add-manual-dest').popup('hide');
        }
    });
    // Desactivation de l'item qui permet de quitter le dropdown
    $('.item.fluid').css('display', 'none')
}

/**
 * Gestion des formulaires et des erreurs
 */
function gestion_formulaires() {
    // Formulaire pour l'ajout d'un nouveau destinataire
    $('#form-dest').form({
        on: 'blur',
        fields: {
            nom: {
                identifier: 'nom',
                rules: [
                    {
                        type: 'minLength[4]',
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

    //Formulaire pour la page de garde
    $('#form-garde').form({
        on: 'change',
        fields: {
            sujet: {
                identifier: 'sujet',
                rules: [
                    {
                        type: 'minLength[4]',
                        prompt: 'Veuillez entrer un nom valide'
                    }
                ]
            },
        }
    });
}

/**
 * Lors de l'ajout manuel d'un destinataire verifie si le champs sont valide
 */
function check_ajout_valide() {
    var isFormValid = $('#form-dest').form('is valid')

    if (isFormValid)
        $("#form-dest .button").removeClass("disabled")
    else
        $("#form-dest .button").addClass("disabled")
}

/**
 * Fonction qui determine si oui ou non l'envoi est possible
 */
function check_envoi_possible() {
    if (list_destinataires_valide() && page_de_garde_valide()) {
        $("#envoie-fax").removeClass("disabled")
    }
    else {
        $("#envoie-fax").addClass("disabled")
    }
}

/**
 * Active l'envoi si la liste n'est pas vide
 */
function list_destinataires_valide() {
    // si on demande de check alors
    var nb_dest = $('#list-dest > div.sup').length
    var div_error = $('#list-dest > div.warning')
    console.log("nombre de destinataire: " + nb_dest)
    if (nb_dest == 0) {
        div_error.show()
        return false
    }
    else {
        div_error.hide()
        return true;
    }
}

/**
 * Verifie si le sujet de la page de garde est rempli
 */
function page_de_garde_valide() {
    // si page de garde affiché on check si le form est valide
    if ($("#page-garde").checkbox('is checked')) {
        var isFormValid = $('#form-garde').form('is valid')

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
 * ajout d'un item dans la list des destinataires recent 
 * @param {les données du destinataire} destinataire 
 */
function add_destinataire_recent(destinataire) {
    var $list = $('#list-destinataire-recent')
    var id = destinataire.numdest
    var $item = $("<div identifiant=\"" + id + "\" class=\"ui blue label ajout\">"
        + "<span class=\"nom-dest\">" + destinataire.dest + "</span>"
        + "</br>"
        + "<span class=\"num-dest\">" + destinataire.numdest + "</span></div>")

    //ajout de la popup dans l'item
    $item.popup({
        html: destinataire.dest + " <br/> " + destinataire.numdest,
        position: 'top center',
        delay: {
            show: 2000,
            hide: 500,
        }
    });
    //Ajout de l'item dans la liste
    $list.append($item)
}

/**
 * Champ de recherche pour le repertoire 
 */
function search_repertoire() {
    var $repertoire = $('#recherche-rep')
    var url_search_dest = hylaweb.api.urls['search_destinataire'].replace('#guid#', guid); 
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
            add_destinataire(num, nom, num)
        },
    });
}

/**
 * Champ de recherche pour les tags
 */
function search_tag() {
    var $tags = $('#search-tag')
    var url_search_tag = hylaweb.api.urls['search_tag'].replace('#guid#', guid);
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

        //TODO a voir
        /*  // Click sur une valeur
         onSelect: function (result, response) {
             // Permet de remettre a 0 le champ
             setTimeout(function () {
                 $('.prompt').val('')
             }, 1);
 
             add_tag(result.tag)
         } */
    });
}

/**
 * Retourne le nom du fax avec l'extension ps
 */
function get_ps_fax_name() {
    var url = window.location.href.split('/')
    fax_name = url[url.length - 1]
    // Si app/send/new alors on renvoie vide
    fax_name == 'new' ? fax_name = '' : fax_name = fax_name + '.ps';
    return fax_name
}

/**
 * Retourne le nom du fax avec l'extension pdf
 */
function get_pdf_fax_name() {
    var url = window.location.href.split('/')
    fax_name = url[url.length - 1]
    fax_name == 'new' ? fax_name = '' : fax_name = fax_name + '.pdf';
    return fax_name
}

/**
 * Recupere les données des destinataires (nom et numero de fax)
 */
function get_destinataires() {
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

/**
 * Retourne le sujet de la page de garde si elle est activé
 */
function get_subject() {
    if ($('#page-garde').checkbox('is checked')) {
        return "" + $("#garde input[name=sujet]").val()
    }
    else
        return ""
}

/**
 * Retourne les notes de la page de garde si elle est activé
 */
function get_notes() {
    if ($('#page-garde').checkbox('is checked')) {
        return "" + $("#garde textarea[name=notes]").val()
    }
    else
        return ""
}

/** 
 * Retourne les tags saisi par l'utilisateur 
 */
function get_tags() {
    var tags = []
    $('#search-tag > a[data-value]').each(function (i) {
        /* tags[i] = $(this).find('span.nom-tag').text() */
        tags[i] = $(this).attr('data-value')
    });
    tags = tags.join(',');
    return tags
}

/** Envoi du fax a l'api avec les destinataires et le nom du fax */
function envoyer_fax() {
    var url_envoie_fax = hylaweb.api.urls['envoi_fax']; 
    var fax_name = get_ps_fax_name();
    var destinataires = get_destinataires();
    var nom_destinataires = destinataires.noms
    var num_destinataires = destinataires.nums
    var coverSubject = get_subject();
    var coverNotes = get_notes();
    var tags = get_tags()
    console.log('guid: ' + guid)
    console.log('fax_name: ' + fax_name)
    console.log('destinataire nom: ' + nom_destinataires)
    console.log('destinataire num: ' + num_destinataires)
    console.log('sujet: ' + coverSubject)
    console.log('notes: ' + coverNotes)
    console.log('tags: ' + tags)
    console.log(url_envoie_fax)
    console.log('envoie du fax ' + getTime())
    if (nom_destinataires == "" || num_destinataires == "") {
        afficherNotif("delete", "Vous n'avez pas saisi de destinataires", "red", true)
    }

    //TODO faire l'envoi des tags
    else {
         $.ajax({
             url: url_envoie_fax,
             data: {
                 sender_guid: guid,
                 filename: fax_name,
                 fax_tag: tags,
                 dest_num: num_destinataires,
                 dest_name: nom_destinataires,
                 fax_coversubject: coverSubject,
                 fax_covernotes: coverNotes
             },
             type: 'post',
         })
             .done(function (json) {
                 // si l'envoi c'est bien passe
                 console.log(json)
                 if (json.status == 'OK') {
                     afficherNotif("check", "Fax envoyé, vous pouvez quitter la page", "green", false)
                 }
 
                 // sinon erreur dans l'envoi
                 else {
                     afficherNotif("delete", "Fax non envoyé, veuillez réessayer", "red", true)
                 }
                 Logger.debug('Statut de la reponse ' + json.status)
                 Logger.debug('Description de la reponse ' + json.description)
             })
             .fail(function () {
                 $('.ui.basic.modal.erreur').modal({
                     closable: false
                 }).modal('show')
                 afficherNotif("delete", "Fax non envoyé, Veuillez réessayer", "red", true)
             })
    }
}

/**
 * Envoi une requete de type delete pour supprimer le fax
 */
function annuler_fax() {
    var fax_name = get_pdf_fax_name()
    var url_annuler_fax = hylaweb.api.urls['annuler_fax'].replace("#faxname#", fax_name)

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
                afficherNotif('delete', "Le fax a été annulé.<br/>Vous pouvez quitter la page", "green", false)
            }
        })
        .fail(function () {
            afficherNotif('delete', "Erreur de connexion", "red", true)
        })
}

/**
 * Ajoute des destinataires dans la liste final 
 * @param {identifiant du destinatiare=le numero du destinataire} id 
 * @param {le nom du destinataire} nom 
 * @param {le numero du destinataire} num 
 */
function add_destinataire(id, nom, num) {
    var $list = $('#list-dest')

    // Si le destinataire n'a pas été ajouté on l'ajoute
    if (!destinataire_exists(id)) {
        var $item = $("<div identifiant=\"" + id + "\" class=\"ui green label sup\">"
            + "<span class=\"nom-dest\">" + nom + "</span>"
            + "<br><span class=\"num-dest\">" + num + "</span>"
            + "<i class=\"delete icon\"></i></div>")

        // Ajout de l'item dans la liste des destinataire
        $list.append($item)

        //on bloque les destinataires de meme id
        $('#list-destinataire-recent [identifiant="' + id + '"]').addClass("disabled")
    }

    // Sinon on re-affiche ou reaffiche à l'utilisateur le destinataire qu'il a deja selectionné
    $item = $('#list-dest > div[identifiant="' + id + '"]')

    $item.hide()
    $item.fadeIn(1000)

}

/**
 * Supprime l'item dans la liste final et reactive au besoin l'item dans la list des dest recents
 * @param {id du destinataire supprimé} id 
 */
function del_destinataire(id) {
    // Suppression de l'item dans la liste des destinataires
    var $itemToDelete = $('#list-dest').find("div[identifiant=\"" + id + "\"]")
    $itemToDelete.fadeOut("slow")

    // Laisse le temps a l'item de disparaitre
    setTimeout(function () {
        $itemToDelete.remove()

        // Reactivation de l'item dans la liste des dest recents
        var $item = $('#list-destinataire-recent').find("div[identifiant=\"" + id + "\"]")
        $item.removeClass('disabled');
    }, 500);
}

/**
 * Fonction qui verifie si le destinataire choisi est deja présent dans la liste des destinataire
 * @param {numéro du destinataire} num 
 */
function destinataire_exists(num) {
    //Pour chaque destinataire
    var exist;
    $('#list-dest > div').each(function () {
        var num_dest = $(this).attr('identifiant')
        if (num_dest == num) {
            exist = true
        }
    });
    return exist;
}

/**
 * Ajoute les tags dans la liste des tags
 * @param {Le tag a ajouter} tag 
 */
function add_tag(tag) {
    var $list = $('#list-tag')
    var $item = $("<div class=\"ui teal label tag\">"
        + "<span class=\"nom-tag\">" + tag + "</span>"
        + "<i class=\"delete icon\"></i></div>")

    //Ajout de l'item dans la liste
    $list.append($item)
}

/**
 * Notification des actoins faites par l'utilisateur
 * @param {Icone} icon 
 * @param {Message de la notif} msg  
 * @param {couleur de l'icone} color 
 * @param {true=closable, false=unclosable} type
 */
function afficherNotif(icone, msg, color, type) {
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

/** Ajout des ecouteurs pour les elements du DOM */
function add_listener() {
    add_key_listener()
    add_mouse_listener()
    add_change_listener()
}

/** Gestion des evenements claviers */
function add_key_listener() {
    // Verifie si le formulaire d'ajout destinataire est valide
    $("#garde input").on('keyup', function () {
        check_envoi_possible();
    });

    // Verifie si le formulaire d'ajout destinataire est valide
    $("#form-dest input").on('keyup', function () {
        check_ajout_valide();
    });

    $("#search-tag").on('keypress', function (event) {
        if (event.which == 13) {
            $("#search-tag .link.icon").trigger('click')
        }
    });
}

/** Gestion des évènements souris */
function add_mouse_listener() {
    $('#list-destinataire-recent').on('click', '.ajout', function () {
        var $item = $(this)
        if (!$item.hasClass('disabled')) {
            var id = $item.attr('identifiant')
            var nom = $item.find('span.nom-dest').text()
            var num = $item.find('span.num-dest').text()
            add_destinataire(id, nom, num)
        }
    });

    //Suppression des destinataires
    $('#list-dest').on('click', '.delete.icon', function () {
        var $item = $(this).parent()
        var id = $item.attr('identifiant')
        del_destinataire(id);
    });

    // Envoyer un fax
    $('#envoie-fax').on('click', function () {
        envoyer_fax()
    });

    // click sur l'ajout manuel
    $('#annuler-fax').on('click', function () {
        annuler_fax();
    });

    // Soumission de l'ajout manuel d'sun destinataire
    $("#form-dest").on("submit", function (event) {
        var nom = $('#form-dest input[name=\"nom\"]').val()
        var num = $('#form-dest input[name=\"num\"]').val()
        add_destinataire(num, nom, num)

        // On reset le formulaire
        $('#form-dest .button').addClass('disabled')
        $('#add-manual-dest').dropdown('toggle');
        $('#form-dest').form('clear')
        event.preventDefault();
    });

    // Ajout d'un tag
    $("#search-tag .link.icon").on('click', function () {
        var input_tag = $("#search-tag input")

        //si le tag n'est pas vide on peut l'ajouter
        if (input_tag.val()) {
            add_tag(input_tag.val())
            input_tag.val('')
        }
    });

    // Suppression d'un tag
    $('#list-tag').on('click', '.delete.icon', function () {
        var $item = $(this).parent()
        $item.remove()
    });
}

/** Gestion des evenements de detection */
function add_change_listener() {
    // Detecte lorsque la liste des destinataires est modifiée
    $('#list-dest').on("DOMSubtreeModified", function () {
        check_envoi_possible();
    });

    if ($("#page-garde").checkbox('is checked')) {
        $("#garde").css('display', 'block')
    }

    // Affichage de la page de garde
    $("#page-garde").checkbox({
        onChecked: function () {
            //TODO a mettre en slideDOWN une fois citrix enlever
            //$("#garde").slideDown(400)
            $("#garde").fadeIn(500)
        },
        onUnchecked: function () {
            //TODO a mettre en slideUP une fois citrix enlever
            //$("#garde").slideUp(400)
            $("#garde").fadeOut(500)
        },

        onChange: function () {
            check_envoi_possible();
        }
    });
}