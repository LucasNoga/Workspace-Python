#! /usr/bin/python
# -*- coding: utf-8 -*-

# En production avec WSGI le mode DEBUG n'est pas pris en compte
class Config(object):
    LDAP = {
        'server' : 'ldaps://crv-57a.stef-tfe.nt',
        'base'   : 'DC=stef-tfe,DC=nt',
        'user'   : 'CA_MAJWEB',
        'pwd'    : '&MAR99LI'    
    }

class DevConf(Config):
    DEBUG = True


class ProdConf(Config):
    DEBUG = True

