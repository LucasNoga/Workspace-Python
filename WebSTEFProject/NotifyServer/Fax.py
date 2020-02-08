#!/usr/local/bin/python
# coding: latin-1


import json
"""Classe definissant un fax (RX ou TX)"""

class Fax():
    def __init__(self, row_fax):
        # FAX RX et TX
        self.direction = row_fax['direction']
        self.id = row_fax['id']


        
        # FAX RX a supprimer
        self.idService = str(row_fax['id_service'])
        self.numFax = row_fax.get('sender', '')
        self.nbPage = row_fax.get('npages',0)
        # FAX RX
        self.id_service = str(row_fax['id_service'])
        self.numsender = row_fax.get('numsender', '')
        self.sender = row_fax.get('sender', '')
        self.npages = row_fax.get('npages',0)
        self.datetime = str(row_fax.get('datetime',''))
        self.tag = row_fax.get('tag','')


        if self.direction == 'RX':
            #Fax en reception
            if row_fax['etatnew'] & 4 == 0:  # test si nouveau fax ou update
                self.type = "RX-NEW"
            else:
                self.type = "RX-UPD"
        else:        
            #Fax en emission
            if row_fax['etatnew'] & 1 == 1:  # test si nouveau fax ou update
                self.type = "TX-NEW"
            else:
                self.type = "TX-UPD"


    """ parsing de l'objet en JSON """
    def convertJson(self):
        if self.direction == 'RX':
            data = {
                'id'        : self.id,
                'datetime'  : self.datetime,
                'numsender' : self.numsender,
                'sender'    : self.sender,
                'npages'    : self.npages,
                'id_service': self.id_service,
                'tag'       : self.tag,
                'type'      : self.type
            }
        else:
            data = {
                'id'        : self.id,
                'numFax'    : self.numFax,
                'nbPage'    : self.nbPage,
                'idService' : self.idService,
                'type'      : self.type                
            }
        return json.dumps(data, sort_keys=True, indent=4)