#!/usr/local/bin/python
# coding: latin-1

from Database import GestionBD
from Message import RabbitMQ
import time
from Config import Config
from Log import logger
import os
import sys

if __name__ == "__main__":
    logger.info("###########################")
    logger.info("# Demarrage de l'automate #")
    logger.info("###########################")
    myhost = os.uname()[1]
    logger.info("Hostname : %s", myhost)

    # config
    main_file = os.path.realpath(sys.argv[0]) if sys.argv[0] else None
    maconfig = Config(main_file.rsplit('.', 1)[0] + '.param')
    # niveau de log
    logger.setLevel(maconfig.log['level'])
    
    # Création de l'objet-interface avec la base de données :
    bd = GestionBD(maconfig)
    if bd.echec:
        sys.exit()

    # Initialisation de l'etat des FAX
    bd.maj_rx("")
    bd.maj_tx("")

    # Creation de l'objet RabbitMQ
    mq = RabbitMQ(maconfig)

    try:
        ok = True
        while ok:
            ############ Reception ############
            list_fax = bd.check_rx()
            if len(list_fax)<>0:
                logger.debug("-- Debut traitement RX --")
                logger.info("Nombre de fax RX a traiter : %s", str(len(list_fax)))
                for fax in list_fax:
                    mq.publish(fax) # envoie les fax en json a la queue abo RabbitMQ
                    bd.maj_rx(fax)
                logger.debug("-- Fin   traitement RX --")
            ############ Emission #############
            list_fax = bd.check_tx()
            # list_fax=[]                     # a supprimer pour la mise en production
            if len(list_fax)<>0:
                logger.debug("-- Debut traitement TX --")
                logger.info("Nombre de fax TX a traiter : %s", str(len(list_fax)))
                for fax in list_fax:
                    mq.publish(fax) # envoie les fax en json a la queue abo RabbitMQ
                    bd.maj_tx(fax)
                logger.debug("-- Fin   traitement TX --")
            time.sleep(3) # Temps d'attente avant relance de la requete
    except KeyboardInterrupt:
        pass
    finally:
        print "Fin des haricots"
