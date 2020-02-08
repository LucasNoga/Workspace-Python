#! /usr/bin/python
# -*- coding: utf-8 -*-

class Config(object):
    LIMIT_DESTINATAIRE_RECENT = 20
    LIMIT_FAX_ATTENTE = 9
    PGSQL = {
        'host'  : '10.253.255.41',
        'db'    : 'bd_hylafax',
        'user'  : 'hylafaxadmin',
        'pass'  : 'hyladmin99li'
    }
    FOLDER = {
        'wait' : '/home/ftpHylaprint/WAIT',
        'standby' : '/home/ftpHylaprint/WAIT/STANDBY',
        'rx'   : '/home/ftpHylafaxDoc/RX'
    }
    HYLAFTP = {
        'host' :'10.253.255.40',
        'user' : 'hylafax_client',
        'pass' : 'hylafax_client-pwd',
        'fold' : '/em'
    }
    """ URL_RABBIT = {
        'host_valide': "http://guest:guest@#SERVER_RABBIT#:15672/api/vhosts/HYLAFAX",
        'queue_name':  "http://guest:guest@#SERVER_RABBIT#:15672/api/queues/HYLAFAX",
    }
    URL_ANIWEB = {
		'archive-eTrack':  "http://10.253.255.36:8091/Anilan/api/V1.0/recoLdv",
    } """
    URLS = {
        'host_valide': "http://guest:guest@#SERVER_RABBIT#:15672/api/vhosts/HYLAFAX",
        'queue_name':  "http://guest:guest@#SERVER_RABBIT#:15672/api/queues/HYLAFAX",
        'archive_ETrack':  "http://10.253.255.36:8091/Anilan/api/V1.0/recoLdv",
        'send_fax': "http://10.253.254.74:8091/HylaWEB/api/V1.0/send/fax"
    }


class DevConf(Config):
    DEBUG = True

    PGSQL = {
        'host'  : '10.253.255.23',
        'db'    : 'bd_hylafaxdev',
        'user'  : 'hylafaxadmindev',
        'pass'  : 'hylafaxpwd01'
    }

class ProdConf(Config):
    DEBUG = False

