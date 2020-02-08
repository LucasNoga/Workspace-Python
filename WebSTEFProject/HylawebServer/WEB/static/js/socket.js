// https://stomp-js.github.io/stomp-websocket/
// https://github.com/stomp-js/stomp-websocket

var hylaweb = hylaweb || {};

hylaweb.Rabbit = (function () {
    var self = {};
    var stompcfg = {
        default_host: '10.253.254.74',
        host: '',
        port: 15674,
        heartbeat: 30000,
        exchange: 'hyla.abonnement',
        user: 'guest',
        pass: 'guest',
        vhost: 'HYLAFAX',
        debug: false, //debug: true,
    }

    var client = {};
    var subscription = {};
    var userAD = {};
    var idService = {};
    var uid = {};

    self.connect = function (host, user, service) {
        //get unique ID
        uid = ID();

        //si Pas d'host on recupere celui par defaut
        if (host == '' || host == null || host == undefined) {
            Logger.debug('utilisation de l\'adresse par defaut pour stomp ' + stompcfg.default_host)
            stompcfg.host = stompcfg.default_host
        }
        else {
            Logger.debug('utilisation de l\'adresse pour stomp ' + host)
            stompcfg.host = host
        }

        userAD = user.toUpperCase();
        idService = service;
        var headers = {
            login: stompcfg.user,
            passcode: stompcfg.pass,
            // additional header
            'client-id': 'my-client-id',
            host: stompcfg.vhost
        }
        var ws = new WebSocket('ws://' + stompcfg.host + ':' + stompcfg.port + '/ws');
        client = Stomp.over(ws);
        client.connect(headers, onconnect, onerror, '/');
        client.heartbeat.outgoing = stompcfg.heartbeat; // client will send heartbeats every 30000ms
        client.heartbeat.incoming = stompcfg.heartbeat;

        //mode debug
        if (!stompcfg.debug) {
            client.debug = function (str) { };
        };
        Logger.debug("Connexion a Rabbit a l'adresse " + 'ws://' + stompcfg.host + ':' + stompcfg.port + '/ws')
    }

    self.disconnect = function () {
        client.disconnect(ondisconnect);
    }

    var onconnect = function () {
        subscribe()
    };

    var subscribe = function () {
        if (!isEmpty(subscription)) {

            if (subscription.tx != undefined) {
                subscription.tx.unsubscribe();
            }

            else if (subscription.rx != undefined) {
                subscription.rx.unsubscribe();
            }
        }
        var queueName = userAD + "_WEB_" + uid

        var destination = '/exchange/' + stompcfg.exchange + '/RX' + idService;
        subscription.rx = client.subscribe(destination, onmessage, { 'x-queue-name': queueName });

        var destination = '/exchange/' + stompcfg.exchange + '/TX' + idService;
        subscription.tx = client.subscribe(destination, onmessage, { 'x-queue-name': queueName });


    }

    self.subscribe = function (user, service) {
        userAD = user.toUpperCase();
        idService = service;
        subscribe()
    }

    var ondisconnect = function () {
        subscription.rx = undefined
        subscription.tx = undefined
        subscription.sys = undefined
    }

    var onerror = function () {
        console.log('error');
    };

    // TODO reecrire le onMessage en emission et en reception
    // called when the client receives a STOMP message from the server
    var onmessage = function (message) {
        //Traitement du message recu
        if (message.body) {
            var json = JSON.parse(message.body)
            if (json.type.substring(0, 2) == "RX" && hylaweb.reception != undefined) {
                Logger.debug('Message rabbit RX : ', message)
                hylaweb.reception.traitementMessageWebSocket(json);
            }
            else if (json.type.substring(0, 2) == "TX" && hylaweb.emission != undefined) {
                Logger.debug('Message rabbit TX : ', message)
                hylaweb.emission.traitementMessageWebSocket(json)
            }

        } else {
            console.log("got empty message");
        }
    };

    var ID = function () {
        // Math.random should be unique because of its seeding algorithm.
        // Convert it to base 36 (numbers + letters), and grab the first 9 characters
        // after the decimal.
        return Math.random().toString(36).substr(2, 9).toUpperCase();
    };


    /**
     * Retourne true si les queues sont non definies
     * @param {*} myObject 
     */
    var isEmpty = function (myObject) {
        return subscription.rx == undefined && subscription.tx == undefined
    }

    return self;
})();


