#! /usr/bin/python
# -*- coding: utf-8 -*-

import os,shutil
import subprocess
import re
import shlex
from collections import Counter
from Log import logger
from ConfigParser import ConfigParser

class Spoolfax(object):
    def __init__(self,config,value):
        self._file     = {}         # tableau des fichiers
        self._fax_auto = False      # A true si envoi automatique 
        self._fax_num  = ''         # Le numéro de fax du destinataire
        self._fax_dest = ''         # Le nom du destinataire
        self._fax_ref  = ''         # La REF tms de la confirmation
        self._fax_age = ''              # Agence extrait du numéro de confirmation
        self._isvalid  = True       # True si les fichiers sont bien présent 
        self._waitfolder = config.folders['wait']     # le dossier WAIT
        self._listIFS  = config.ifs['age'].split(';') # tableau des agences IFS
        self._fileIFS = config.ifs['template']
        
        if value[-3:] == 'ctl':
            self._file['CTL']  =  value
            self._env(value)
            # Initialisation du nom du fichier sans extension
            file = self._file['CTL'].rsplit('.',1)[0]
            # Initialisation du nom du fichier postscript
            self._file['IFSCTL'] = file + '.ifs.ctl'
            self._file['PS'] = file + '.ps'
            self._file['IFSPS'] = file + '.ifs.ps'
            self._file['PDF'] = file + '.pdf'
            self._file['IFSPDF'] = file + '.ifs.pdf'
            # suppression des fichiers pdf ifs.pdf ifs.ps
            if os.path.isfile(self._file['IFSPS']): os.remove(self._file['IFSPS'])
            if os.path.isfile(self._file['IFSPDF']): os.remove(self._file['IFSPDF'])
            if os.path.isfile(self._file['PDF']): os.remove(self._file['PDF'])

            # Verification que le fichier Ps existe
            if os.path.isfile(self._file['PS']):
                # Verification si envoi en automatique
                self._analysefichier()
                # Ajout document IFS sur le PS
                self._addIFS()
                # creation du PDF
                self._makePDF(self._file['PS'], self._file['PDF'])
                self._makePDF(self._file['IFSPS'], self._file['IFSPDF'])
            else:
                self._isvalid  = False
                logger.error('Le fichier %s n''existe pas' %value)
        else:
            self._isvalid  = False
            logger.debug('Erreur l''extension du fichier ne correspond pas a *.ctl : %s' %value)


    @property
    def isvalid(self):
        return self._isvalid

    @property
    def file(self):
        if self._isIFS():
            return self._file['IFSPS'].rsplit('.',1)[0]        
        else:
            return self._file['PS'].rsplit('.',1)[0]

    @property
    def fileCTL(self):
        if os.path.isfile(self._file['IFSCTL']):
            return self._file['IFSCTL']        
        else:
            return self._file['CTL']

    @property
    def filePDF(self):
        if os.path.isfile(self._file['IFSPDF']):
            return self._file['IFSPDF']        
        else:
            return self._file['PDF']

    @property
    def filePS(self):
        if os.path.isfile(self._file['IFSPS']):
            return self._file['IFSPS']        
        else:
            return self._file['PS']

    @property
    def username(self):
        return self._username
    
    @property
    def hostname(self):
        return self._hostname

    @property
    def fax_auto(self):
        return self._fax_auto

    @property
    def fax_num(self):
        return self._fax_num

    @property
    def fax_dest(self):
        return self._fax_dest

    @property
    def fax_ref(self):
        return self._fax_ref

    @property
    def fax_age(self):
        return self._fax_age        

    def movewait(self):
        for type, file in self._file.iteritems():
            if os.path.isfile(file):
                filename = os.path.split(file)[1]
                logger.debug('> Déplacement de %s vers %s' %(file,self._waitfolder))
                shutil.move(file, os.path.join(self._waitfolder,filename))
                self._file[type] =  os.path.join(self._waitfolder,filename)
        if self._isIFS():
            if os.path.isfile(self._file['CTL']):   os.remove(self._file['CTL'])
            if os.path.isfile(self._file['PS']):   os.remove(self._file['PS'])
            if os.path.isfile(self._file['PDF']):   os.remove(self._file['PDF'])


    def remove(self):
        for type, file in self._file.iteritems():
            if os.path.isfile(file):
                logger.debug('> Suppression de %s' % file)
                os.remove(file)
                

    def _env(self,fileCTL):
        config = ConfigParser()
        config.read(fileCTL)
        del config

    def _isIFS(self):
        return (self._fax_age<>'' and self._fax_age in self._listIFS)

    def _addIFS(self):
        cmd = 'psmerge -o%s %s %s' %(self._file['IFSPS'], self._file['PS'], self._fileIFS)
        logger.debug('> Verification si Agence IFS')
        if self._isIFS():
            logger.debug('> Agence IFS')
            logger.debug('> Début join PS command : %s' %cmd)
            p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={'PATH': '/usr/bin'})
            out, err = p.communicate()
            logger.debug('Sortie Normal de la commande: %s' % out)
            logger.debug('Sortie Error  de la commande: %s' % err)
            
            logger.debug('creation fichier %s' % self._file['IFSCTL'])
            shutil.copy2(self._file['CTL'],self._file['IFSCTL'])
            logger.debug('> Fin join PS')

    def _makePDF(self, inPS, outPDF):
        # transformation du fichier ps en pdf
        if os.path.isfile(inPS):
            logger.debug('> Début transformation du document %s en PDF' % inPS)
            cmd = 'ps2pdf %s %s' %(inPS, outPDF)
            logger.debug('PDF command : %s' %cmd)
            p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={'PATH': '/usr/bin'})
            out, err = p.communicate()
            logger.debug('Sortie Normal de la commande: %s' % out)
            logger.debug('Sortie Error  de la commande: %s' % err)
            logger.debug('> Fin transformation PDF')

    def _analysefichier(self):
        logger.debug('Verification si le document est une CA')
        with open(self._file['PS'], "r") as fichier:
            filetext = fichier.read()
        # Verification du titre du document
        regex = re.compile(r'%%Title: ...-GTI-CA')
        matches = re.findall(regex, filetext)
        logger.debug('Recherche titre du document : %s' % matches)
        if len(matches) <> 1:
            self._fax_auto = False
            logger.debug('Le titre du document ne correspond pas ! ')
        else:
            logger.debug('Le titre du document correspond !')
            # recupération du champ caché
            regex = re.compile(r'#CA_FAX#(.*)@(.*)#(.*)#')
            matches = re.findall(regex, filetext)
            logger.debug('Recherche des mots clé : %s' % matches)
            if len(Counter(matches))==1 :
                logger.debug('La chaine de caractère est unique  !')
                self._fax_num  = matches[0][0]
                self._fax_dest = matches[0][1]
                self._fax_ref  = matches[0][2]
                self._fax_age = self._fax_ref[:3]
                if self._fax_num[:2]=='H:':
                    logger.debug('Detection du H: -> OK -> Envoi automatique  !')
                    self._fax_num  = self._fax_num[2:]
                    self._fax_auto = True
                else:
                    logger.debug('Detection du H: -> KO -> Envoi manuel  !')
                    self._fax_auto = False


            else:
                logger.debug('La chaine de caractère n''est pas unique ! Plusieurs documents detectés')
                self._fax_auto = False

        logger.debug('Fin verification')    

        