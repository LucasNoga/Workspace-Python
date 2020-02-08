#!/usr/local/bin/python
# coding: latin-1
import os
import json
import pika
from Log import logger


# RabbitMQ
# Partie Abonnement
class RabbitMQ(object):
    def __init__(self, config, fax, user):
        #https://stackoverflow.com/questions/35193335/how-to-reconnect-to-rabbitmq
        """self._params = pika.connection.ConnectionParameters(
            host=config.rabbit['host'],
            virtual_host=config.rabbit['vhost'],
            credentials=pika.credentials.PlainCredentials(username, password))"""
        self._fax  = fax
        self._queue = user.hostname + '\\' + user.login + '\\HYL\\SYS'
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

    def checkQueue(self):
        """check if the queue exist."""
        self.connect()
        try:
            self._channel.queue_declare(queue=self._queue, auto_delete=True, passive=True)
        except pika.exceptions.ChannelClosed:
            logger.warning('la queue %s n''existe pas' %self._queue)
            return False
        return True

    def publish(self):
        """ Publish message via MQTT """
        self.connect()
        body ={
                'type': 'NEW_FAX_SEND',
                'items': {
                    'navigateur': 'chrome.exe',
                    'options_nav': '',
                    'url': 'http://10.253.254.74/HylaWEB/app/send/' + os.path.split(self._fax.file)[1]
                }
            }

        logger.debug("message: queue %s body %s", self._queue, body)
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue, 
            body=json.dumps(body)
        )
