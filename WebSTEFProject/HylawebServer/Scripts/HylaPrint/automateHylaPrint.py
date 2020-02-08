#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import Queue
import signal
import glob
import time
import subprocess
import shlex

from threading import Thread, RLock, currentThread, enumerate

from lib.Log import logger
from lib.Config import Config
from lib.Spoolfax import Spoolfax
from lib.Message import RabbitMQ
from lib.User import User
from lib.ApiCall import sendfax

# config
main_file = os.path.realpath(sys.argv[0]) if sys.argv[0] else None
maconfig = Config(main_file.rsplit('.', 1)[0] + '.param')
#Threads
num_worker_threads = maconfig.threads['num_worker_threads']
# niveau de log
logger.setLevel(maconfig.log['level'])




def FileInUse(file):
  cmd = '/usr/bin/lsof ' + file
  if os.path.exists(file):
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (output,error) = p.communicate()
    if output=='':
      return False # file not in use
  return True # file in use ou not exist


# Process Principal des Thread 
def worker(FileQueue, verrou):
    t = currentThread()
    while not getattr(t, "stop", False):
        try:
            FileInQueue = FileQueue.get(True,0.1)
            logger.info('File %s Size : %s', FileInQueue, os.path.getsize(FileInQueue))
            fax = Spoolfax(maconfig, FileInQueue)
            user = User(maconfig, FileInQueue)
            if fax.isvalid:
                if user.getinfo():
                    mq = RabbitMQ(maconfig, fax, user)
                    if mq.checkQueue():
                        # La queue existe
                        if fax.fax_auto:
                            # CA -> Envoi en automatique
                            if sendfax(maconfig,fax,user):
                                logger.info('Le Fax a été correctement envoyé au serveur de Fax')
                            else:
                                logger.error('Le Fax n''a pas été correctement envoyé  correctement ar serveur de Fax')
                                #TODO : voir le traitement a effectuer
                            fax.remove()
                        else:
                            # Envoi message via rabbit MQ
                            fax.movewait()
                            mq.publish()
                    else:
                        # récupérer l'adresse mail de l'utilisateur
                        # envoyer un mail
                        # fax.remove()
                        fax.movewait()
                    del mq
                else:
                    logger.info('Le user n\'est pas valide... On supprime les fichiers')
                    fax.remove()    
            else:
                logger.info('Les fichiers FAX ne sont pas valides... On supprime les fichiers')
                fax.remove()    
            del fax
            del user
            FileQueue.task_done()
        # en cas de time out on repart sur un tour de boucle
        except Queue.Empty:
            pass
    logger.debug('Stop')           




#######################
# Programme principal #
#######################
def main():
  verrou = RLock()
  FileQueue = Queue.Queue()
  
  # Capture signal
  def handler_stop_signals(signal, frame):
    logger.info('*******************   SIGTERM  *****************************')
    sys.exit()

  signal.signal(signal.SIGINT, handler_stop_signals)
  signal.signal(signal.SIGTERM, handler_stop_signals)

  # demarrage des Thread

  for i in range(int(num_worker_threads)):
     t = Thread(target=worker, name = 'Thread ' + str(i),  args=(FileQueue, verrou))
     t.daemon = True
     t.start()

  try:
    # This would print all the files and directories
    Filemask = "*.ctl"
    inFolder = maconfig.folders['in']
    waitFolder = maconfig.folders['wait']
    path = os.path.join(inFolder,Filemask)
    logger.info('************************************************')
    logger.info('* Begin Job                                    *')
    logger.info('************************************************')
    logger.info('* Folder IN    : %s', path)
    logger.info('* Folder WAIT  : %s', waitFolder)
    logger.info('************************************************')
    logger.info('* Threads      : %s', num_worker_threads)
    logger.info('************************************************')


    if not os.path.exists(inFolder):
      logger.error('Folder %s does not exist', inFolder)
      sys.exit()
    if not os.path.exists(waitFolder):
      logger.error('Folder %s does not exist', waitFolder)
      sys.exit()

    stop = False
    while not stop:
      listing = glob.glob( path )
      listing.sort(key=os.path.getmtime)
      for file in listing: 
        if FileInUse(file):
          logger.warning('File %s is in use !!', file)
          continue
        FileQueue.put(file)


      FileQueue.join()       # block until all tasks are done
      time.sleep(0.1)
      #stop = True

  except SystemExit:
    pass
  finally:
    # si la boucle while s'arrête d'une manière ou d'une autre
    # on attend que les autres processus s'arrêtent avant de quitter
    # En vrai on mettrait beaucoup plus de code que ça, une file
    # de controle, peut être un handler de SIGTERM, etc
    # là on va à l'essentiel 
    main_thread = currentThread()
    for t in enumerate():
      if t is main_thread:
          continue
      logger.debug('joining %s', t.getName())
      t.stop = True
      t.join()
    print "Fin des haricots"   


# Lancement prg main
if __name__ == '__main__':
  main()


sys.exit()
# code pas pris en compte

