/* API                                */
/* Define API endpoints once globally */
var hylaweb = hylaweb || {};

/* // Serveur prod
var server = "http://10.253.254.74:8091/"

//Serveur Dev
var server2 = "http://10.253.255.33:5002/"

$.fn.api.url = {
    // HylaSend
    'search_destinataire': server + 'HylaWEB/api/V1.0/user/' + guid + '/dest',
    'destinataire_recent': server + 'HylaWEB/api/V1.0/user/' + guid + '/dest/recent',
    'envoi_fax': server + 'HylaWEB/api/V1.0/send/fax',
    'get_fax': server + 'HylaWEB/api/V1.0/wt/fax/#faxname#/pdf',
    'annuler_fax': server + 'HylaWEB/api/V1.0/wt/fax/#faxname#',
    'search_tag': server + 'HylaWEB/api/V1.0/user/' + guid + '/tags',
}; */

//Objet permettant de se connecter à l'api
hylaweb.api = (function () {
    var self = {};
    self.resultat = null

    // Serveur prod
    var server_prod = "http://10.253.254.74:8091/"

    var serverInfoAD = "http://10.253.254.74:8082" 
    

    // Serveur Dev
    var server_dev = "http://10.253.255.33:5002/"

    self.urls = {
        'user': server_prod + 'HylaWEB/api/V1.0/user/#guid#',
        'visu_fax': server_prod + 'HylaWEB/api/V1.0/rx/fax/#id_fax#/pdf?guid=#guid#',
        'check_hylanotify': server_prod + 'HylaWEB/api/V1.0/user/HylaNotify/connected',
        'services': server_prod + 'HylaWEB/api/V1.0/user/#guid#/services',
        'get_avatar': serverInfoAD + "/InfoAD/avatar/#initial#.png?mail=#mail#&key=#key#",
        
        // Hylafax, reception
        'rx_fax': server_prod + 'HylaWEB/api/V1.0/rx/#id_serv#/fax',
        'get_fax': server_prod + 'HylaWEB/api/V1.0/rx/fax/#id_fax#',
        'delete_fax': server_prod + 'HylaWEB/api/rx/fax/#id_fax#/delete',
        'lock_fax': server_prod + 'HylaWEB/api/rx/fax/#id_fax#/lock',
        'unlock_fax': server_prod + 'HylaWEB/api/rx/fax/#id_fax#/unlock',
        
/*
        'rx_fax': server_dev + 'api/V1.0/rx/#id_serv#/fax', 
        'get_fax': server_dev + 'api/V1.0/rx/fax/#id_fax#',
        'delete_fax': server_dev + 'api/rx/fax/#id_fax#/delete',
        'lock_fax': server_dev + 'api/rx/fax/#id_fax#/lock',
        'unlock_fax': server_dev + 'api/rx/fax/#id_fax#/unlock',
*/        
        // HylaSend
        'search_destinataire': server_prod + 'HylaWEB/api/V1.0/user/#guid#/dest',
        'envoi_fax': server_prod + 'HylaWEB/api/V1.0/send/fax',
        'annuler_fax': server_prod + 'HylaWEB/api/V1.0/wt/fax/#faxname#',
        'search_tag': server_prod + 'HylaWEB/api/V1.0/user/#guid#/tags',


    }
    return self;
})();
