#! /usr/bin/python

class Config(object):

    VERSION = "1.4"

# API PROD
    API_PROD = "http://10.253.254.74:8091/"

# API DEV
    API_DEV = "http://10.253.255.33:5002/"

    URL_API = {
        ###   #FAXNAME# = nom du fichier fax
        ###   #GUID# = GUID de l'utilisateur
        "get_user": API_PROD + 'HylaWEB/api/V1.0/user/#GUID#',
        "check_fax": API_PROD + 'HylaWEB/api/V1.0/wt/fax/#FAXNAME#.pdf',
        "get_fax": API_PROD + 'HylaWEB/api/V1.0/wt/fax/#FAXNAME#/pdf',
        "dest_recent": API_PROD + 'HylaWEB/api/V1.0/user/#GUID#/dest/recent',
        "get_default_service": API_PROD + 'HylaWEB/api/V1.0/user/#GUID#/service',
        "get_list_standby_fax": API_PROD + 'HylaWEB/api/V1.0/standby/fax'
    }

class DevConf(Config):
    DEBUG = True

class ProdConf(Config):
    DEBUG = False
