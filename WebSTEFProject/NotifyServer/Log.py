#!/usr/local/bin/python
# coding: latin-1

import sys,os
import logging
from logging.handlers import RotatingFileHandler

# disable propagation
logging.getLogger("pika").propagate = False

#Creation du log
logger = logging.getLogger()
#definition du niveua de log
logger.setLevel(logging.DEBUG)
#formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(message)s")
formatter = logging.Formatter('%(asctime)s :: %(levelname)-7s :: %(threadName)-10s -> %(message)s')

# creation d'un handler qui va rediriger une ecriture du log vers un fichier
main_file = os.path.realpath(sys.argv[0]) if sys.argv[0] else None
filepath, filename = os.path.split(main_file)
logFolder = os.path.join(filepath,"log")

if not os.path.exists(logFolder):
    # Creationdu du dossier log
    os.mkdir(logFolder)

logFile = os.path.join(filepath,"log",filename.rsplit('.',1)[0] + '.log')    
handler = RotatingFileHandler(logFile, 'a', maxBytes=10000000, backupCount=5)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG) # Laisse passer tout les log. Le niveau est géré par le niveau de logger
logger.addHandler(handler)

# creation d'un second handler qui va rediriger chaque ecriture de log sur la console
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG) # Laisse passer tout les log. Le niveau est géré par le niveau de logger
logger.addHandler(steam_handler)