#!/usr/local/bin/python
# coding: latin-1

import psycopg2
import psycopg2.extras
from Fax import Fax
from Log import logger


class GestionBD(object):
    """Mise en place et interfaçage d'une base de données PostgreSQL"""
    def __init__(self, config):
        "Établissement de la connexion - Création du curseur"
        connection = "dbname='%(name)s' user='%(user)s' host='%(host)s' password='%(pass)s'" %config.db
        try:
            self.baseDonn =  psycopg2.connect(connection)
        except Exception as err:
            logger.error('La connexion avec la base de données a échoué !')
            logger.error('Erreur détectée : %s' % err)
            self.echec =1
        else:
            self.cursor = self.baseDonn.cursor(cursor_factory=psycopg2.extras.DictCursor)   # création du curseur
            self.echec =0

    """Retourne les fax a recevoir dans la BD les renvoi en JSON"""
    def check_rx(self):
        logger.debug("Verification des fax en reception")
        sql = """SELECT 'RX' as direction, id, sender, numsender, npages, id_service, etatnew, datetime,
                    COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag
                    FROM reception
                    WHERE datetime > current_date - interval '7 days'
                      AND (etatnew & 5 = 1 OR etatnew & 8 > 0) AND id_service IS NOT NULL;"""
        logger.debug("SQL : %s" %sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        faxs = [] # liste des faxs
        for row in res:
            fax = Fax(row) # nouveau fax
            faxs.append(fax)
        return faxs # on renvoie les faxs a recevoir

    # Mise a jour des statuts des fax en Reception 
    def maj_rx(self,fax = ""):
        # Mise a jour reception
        if(fax == ""): # pour le premier passage on met a jour tous les fax
            logger.debug("Initialisation des FAX recus")
            sql = """UPDATE reception set etatnew = (etatnew | 4) & 119 WHERE etatnew & 4 = 0 OR etatnew & 8 > 0;"""
            logger.debug("SQL : " + sql)
            self.cursor.execute(sql)
            self.commit()
        else:
            logger.debug("Mise a jour du fax : " + str(fax.id))
                # selection des nouveaux fax et ceux qui ont ete modifie
                # reinitialisation du bit 4 a 1 et du bit 8 a 0
            sql = """UPDATE reception set etatnew = (etatnew | 4) & 119 WHERE id=%(ID)s;"""
            logger.debug("SQL : " + sql, {'ID': fax.id})
            self.cursor.execute(sql, {'ID': fax.id})
            self.commit()


    #Retourne les fax a mettre a jour en emission
    def check_tx(self):
        logger.debug("Verification des fax en emission")
        sql = """SELECT 'TX' as direction, id, id_service, etatnew FROM emission 
                 WHERE datetime > current_date - interval '7 days'
                 AND etatnew > 0 AND id_service IS NOT NULL;"""

        logger.debug("SQL : %s" %sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        faxs = [] # liste des faxs
        for row in res:
            fax = Fax(row) # nouveau fax
            faxs.append(fax)
        return faxs # on renvoie les faxs a recevoir

    # Mise a jour des statuts des fax en Emission
    def maj_tx(self,fax = ""):
        # Mise a jour table emission
        if(fax == ""): # pour le premier passage on met a jour tous les fax
            logger.debug("Initialisation des FAX emis")
            sql = """UPDATE emission SET etatnew = etatnew & 0 WHERE etatnew > 0"""
            logger.debug("SQL : " + sql)
            self.cursor.execute(sql)
            self.commit()
        else:
            logger.debug("Mise a jour du fax : " + str(fax.id))
            sql = """UPDATE emission SET etatnew = etatnew & 0 WHERE id=%(ID)s;"""
            logger.debug("SQL : " + sql, {'ID': fax.id})
            self.cursor.execute(sql, {'ID': fax.id})
            self.commit()
            

    def commit(self):
        if self.baseDonn:
            self.baseDonn.commit()	 # transfert curseur -> disque
    
    def close(self):
        if self.baseDonn:
            self.baseDonn.close()
