#! /usr/bin/python
# -*- coding: utf-8 -*-


import os,sys
from lib.Spoolfax import Spoolfax
from lib.Config import Config
from lib.User import User
from lib.ApiCall import sendfax

# config
maconfig = Config('cafax.param')

#file = '/home/ftpHylaprint/SAMPLES/2CA.ctl'
file = '/home/ftpHylaprint/SAMPLES/1CA.ctl'
#file = '/home/ftpHylaprint/SAMPLES/AUTRE.ctl'
#file = '/home/ftpHylaprint/IN/allouis.f.116.ctl'


# Lancement prg main
if __name__ == '__main__':
    user = User(maconfig,file)
    if user.getinfo():
        print user.guid
        print user.mail
    fax = Spoolfax(maconfig, file)
    if fax.fax_auto:
        print "Envoi en automatique : "
        print "Destinataire : %s" % fax.fax_dest
        print "Numéro : %s" % fax.fax_num
        print "Ref : %s" % fax.fax_ref
        print "Age : %s" % fax.fax_age
    #sendfax(maconfig,fax,user)
    print "############# avant MOVE #############"
    print "fichier PS  : %s" % fax.filePS
    print "fichier PDF : %s" % fax.filePDF
    print "file        : %s" % fax.file
    fax.movewait()
    print "############# apres MOVE #############"
    print "fichier PS  : %s" % fax.filePS
    print "fichier PDF : %s" % fax.filePDF
    print "file        : %s" % fax.file

    del fax

 
    
sys.exit()
# code pas pris en compte
