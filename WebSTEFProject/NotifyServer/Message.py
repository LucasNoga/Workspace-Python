#!/usr/local/bin/python
# coding: latin-1

import pika
from Log import logger


# RabbitMQ
# Partie Abonnement
class RabbitMQ(object):
    def __init__(self, config):
        #https://stackoverflow.com/questions/35193335/how-to-reconnect-to-rabbitmq
        """self._params = pika.connection.ConnectionParameters(
            host=config.rabbit['host'],
            virtual_host=config.rabbit['vhost'],
            credentials=pika.credentials.PlainCredentials(username, password))"""
        self._exchange = config.rabbit['exchange']
        self._params = pika.connection.ConnectionParameters(
            host=config.rabbit['host'],
            virtual_host=config.rabbit['vhost'])
        self._conn = None
        self._channel = None
        self.connect()

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()
            self._channel.exchange_declare(exchange=self._exchange,
                                           exchange_type='direct')        

    def check(self):
        """Publish msg, reconnecting if necessary."""
        try:
            self._channel.exchange_declare(exchange=self._exchange,
                                           exchange_type='direct')        
        except pika.exceptions.ConnectionClosed:
            logger.warning('reconnecting to queue')
            self.connect()

    def publish(self,fax):
        # pour chaque fax de la liste
        self.check()
        routing = fax.type[:2] + fax.idService # on recupere l'id du service pour le routage
        fax_json = fax.convertJson() # on convertit le fax en JSON
        logger.debug("message: routing %s body %s", routing, fax_json)
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing, 
            body=fax_json
        )
