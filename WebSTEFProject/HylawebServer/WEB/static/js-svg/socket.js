// https://stomp-js.github.io/stomp-websocket/
// https://github.com/stomp-js/stomp-websocket

var hylaweb = hylaweb || {};

hylaweb.Rabbit = (function(){
    var self = {};
    var stompcfg = {
        host: '10.253.254.74',// TODO A enlever en brut
        //host: hylaweb.reception.hostRabbit,
        port: 15674,
        heartbeat: 30000,
        exchange: 'hyla.abonnement',
        user: 'guest',
        pass: 'guest',
        vhost: 'HYLAFAX',
        //debug: true,
        debug: false
    }

    var client = {};
    var subscription = {};
    var userAD = {};
    var idService = {};
    var uid = {};

    self.connect = function(host, user, Service){
        //get unique ID
        uid = ID();
        //stompcfg.host = host
        userAD = user.toUpperCase();
        idService = Service;
        var headers = {
            login: stompcfg.user,
            passcode: stompcfg.pass,
            // additional header
            'client-id': 'my-client-id',
            host: stompcfg.vhost
        }
        var ws = new WebSocket('ws://' + stompcfg.host + ':' + stompcfg.port +'/ws');
        client = Stomp.over(ws);
        client.connect(headers, onconnect, onerror, '/');
        client.heartbeat.outgoing = stompcfg.heartbeat; // client will send heartbeats every 30000ms
        client.heartbeat.incoming = stompcfg.heartbeat;
        
        //mode debug
        if (!stompcfg.debug) {
            client.debug = function(str) {};
        };
    }

    self.disconnect = function(){
        client.disconnect(ondisconnect);
    }

    var onconnect = function () {
        subscribe()
    };

    var subscribe = function(){
        if (!isEmpty(subscription)) {
            subscription.tx.unsubscribe();
            subscription.rx.unsubscribe();
        }

        var queueName = userAD + "_WEB_" +  uid
        // reception
        var destination = '/exchange/' + stompcfg.exchange + '/RX' + idService;
        subscription.rx = client.subscribe(destination, onmessage,{ 'x-queue-name': queueName });
        // emmission
        var destination = '/exchange/' + stompcfg.exchange + '/TX' + idService;
        subscription.tx = client.subscribe(destination, onmessage,{ 'x-queue-name': queueName });            
    }

    self.subscribe  = function(user, Service){
        userAD = user.toUpperCase();
        idService = Service;
        subscribe()
    }

    var ondisconnect = function (){
        subscription.rx = undefined
        subscription.tx = undefined
    }

    var onerror = function () {
        console.log('error');
    };
 
   // called when the client receives a STOMP message from the server
    var onmessage = function (message) {
        //Traitement du message recu
        if (message.body) {
            var json = JSON.parse(message.body)
            hylaweb.reception.traitementMessageReception(json);
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


    var isEmpty = function (myObject) {
        return subscription.rx == undefined && subscription.tx == undefined
    }
       
        
        /* for(var key in myObject) {
            console.log('isEmpty', myObject)
            console.log('isEmpty', myObject.rx)
            if (myObject.hasOwnProperty(key)) {
                return false;
            }
        }
        return true;
    }
 */
    return self;
})();


