#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from Log import logger

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file


def sendfax(config, fax, user):
    logger.debug('> Debut de la fonction sendfax')
    sendfax = True
    url = "http://" + config.api['host'] + ":" + config.api['port'] + "/" + config.api['page']
    f = open(fax.filePS)
    files = {'file': f}
    values = {
        'sender_guid' : user.guid,
        'dest_num'    : fax.fax_num,
        'dest_name'   : fax.fax_dest,
        'fax_tag'     : fax.fax_ref
        }

    try:
        r = requests.post(url, files=files, data=values)
        if r.status_code <> requests.codes.ok:
            logger.error('La requete POST a renvoye le code retour : %s' %r.status_code)
            sendfax = False
        else:
            retour = json.loads(r.text)
            logger.debug('La requete POST a renvoye le json : %s' %retour)
            if retour['status']<>'OK':
                logger.error('Erreur dans l''execution de l''API : %s' %retour['description'])
                sendfax = False
    except Exception as e:
        logger.error('Erreur dans l''execution de la fonction sendfax : ' + str(e))
        sendfax = False
    finally:
        f.close()
        logger.debug('> Fin de la fonction sendfax')
        return sendfax


