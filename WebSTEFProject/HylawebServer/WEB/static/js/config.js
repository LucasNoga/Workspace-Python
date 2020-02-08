/* API                                */
/* Define API endpoints once globally */
var hylaweb = hylaweb || {};

conf = (function () {
    var self = {};

    // true = config de dev
    //self.DEBUG = true;
    
    // limite du nombre de fax en attente pour envoyer un fax
    self.LIMIT_WAITING_FAX = 2

    // nombre de fax à affiché en reception
    self.LIMIT_RX_FAX = 15

    // nombre de fax à affiché en emission
    self.LIMIT_TX_FAX = 15

    // nombre de fax à affiché en archive
    self.LIMIT_ARCHIVE_FAX = 30

    self.init = function () {

        var consoleHandler = Logger.createDefaultHandler({
            formatter: function (messages, context) {
                messages.unshift(getLogTime(), " :: ", context.level.name + " ::")
            }
        });

        Logger.setHandler(function (messages, context) {
            consoleHandler(messages, context);
        });

        //niveau info par defaut
        Logger.setLevel(Logger.INFO);
        if (self.DEBUG) {
            Logger.setLevel(Logger.DEBUG);
        }
    }

    /** Retourne le temps courant pour les logs */
    var getLogTime = function () {
        return moment().format('YYYY-MM-DD HH:mm:ss')
    }

    self.Server = {
        API: {
            PROD: "http://10.253.254.74:8091/HylaWEB/",
            DEV: "http://10.253.255.33:5002/"
        },
        WEB: {
            PROD: "http://10.253.254.74/HylaWEB/",
            DEV: "http://10.253.255.33:5001/"
        },
        InfoAD: "http://10.253.254.74:8082/",
    }

    return self;
})();

// Objet permettant de se connecter à l'api
api = (function () {
    var self = {};
    self.init = function () {
        var serveurWEB = null
        var serveurAPI = null
        if (conf.DEBUG) {
            console.log('Config de dev')
            serveurWEB = conf.Server.WEB.DEV
            serveurAPI = conf.Server.API.DEV
        }
        else {
            console.log('Config de prod')
            serveurWEB = conf.Server.WEB.PROD
            serveurAPI = conf.Server.API.PROD
        }

        self.urls = {
            // Route pour acceder a hylasend en cas de transfert
            'hylasend': serveurWEB + "app/send/#faxname#",

            // Route pour acceder a l'AD
            'get_avatar': conf.Server.InfoAD + "InfoAD/avatar/#initial#.png?mail=#mail#&key=#key#",

            'user': serveurAPI + 'api/V1.0/user/#guid#',
            'visu_fax': serveurAPI + 'api/V1.0/rx/fax/#id_fax#/pdf?guid=#guid#',
            'check_hylanotify': serveurAPI + 'api/V1.0/user/HylaNotify/connected',
            'services': serveurAPI + 'api/V1.0/user/#guid#/services',

            // Hylafax, reception
            'rx_fax': serveurAPI + 'api/V1.0/rx/#id_serv#/fax',
            'get_fax': serveurAPI + 'api/V1.0/rx/fax/#id_fax#',
            'delete_fax': serveurAPI + 'api/rx/fax/#id_fax#/delete',
            'lock_fax': serveurAPI + 'api/rx/fax/#id_fax#/lock',
            'unlock_fax': serveurAPI + 'api/rx/fax/#id_fax#/unlock',
            'move_fax': serveurAPI + 'api/rx/fax/#id_fax#/move',
            'read_fax': serveurAPI + 'api/rx/fax/#id_fax#/read',
            'transfer_fax': serveurAPI + 'api/rx/fax/#id_fax#/transfer/#type_trf#',

            // Hylafax, emission
            'tx_fax': serveurAPI + 'api/V1.0/tx/#id_serv#/fax',
            'get_fax_tx': serveurAPI + 'api/V1.0/tx/fax/#id_fax#',
            'cancel_fax_emit': serveurAPI + 'api/V1.0/tx/fax/#id_fax#/cancel',
            'send_back_fax': serveurAPI + 'api/V1.0/tx/fax/#id_fax#/sendback',

            // Hylafax, archive
            'archive': serveurAPI + 'api/V1.0/archive/#type_fax#',
            'archive_file': serveurAPI + 'api/V1.0/#type_fax#/fax/#idFax#/archive/#format#',

            // HylaSend
            'search_destinataire': serveurAPI + 'api/V1.0/user/#guid#/dest',
            'envoi_fax': serveurAPI + 'api/V1.0/send/fax',
            'annuler_fax': serveurAPI + 'api/V1.0/wt/fax/#faxname#',
            'search_tag': serveurAPI + 'api/V1.0/user/#guid#/tags',
            'check_fax_ps_exist': serveurAPI + 'api/V1.0/wt/fax/#FAXNAME#',
            'import_contact': serveurAPI + 'api/V1.0/user/dest/import',
            'export_contact': serveurAPI + 'api/V1.0/user/dest/export',
            'standing_by': serveurAPI + 'api/V1.0/standby/fax',
            'thumbnails_fax': serveurAPI + 'api/V1.0/fax/jpeg',
        }
    }
    return self;
})();

// chargement de la config et de l'api
conf.init();
api.init()