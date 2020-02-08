#! /usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
# Query parameter : http://initd.org/psycopg/docs/usage.html#query-parameters
#
#############################################################################

import os
import datetime
import time
import tempfile
import ConfigParser
import ftplib
import base64
from hashlib import md5
from flask import Flask, jsonify, g, request, render_template, send_file
from flask_cors import CORS, cross_origin  #  pip install --proxy=http://10.253.255.100:3128 flask-cors
import requests
import json
import urllib
import shutil
import pika
import hashlib
import socket
import itertools
from operator import itemgetter
import re
import glob
import fnmatch
####### Traitement image pdf to img ########################################################
from pdf2image import convert_from_path
from PIL import Image
####### DB ########################################################
import psycopg2
import psycopg2.extras
####### Gestion du codage UTF8 dans la base POSTGRES ##############
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
###################################################################
from reverse_proxy import ReverseProxied
######################## DOC API ##################################
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder

app = Flask(__name__)
CORS(app)

# swagger
templateSwagger = {
    "basePath": "/",
    "swagger": "2.0",
    "info": {
        "description": "API to get data from Hylafax application",
        "title": "Hylafax API",
        "version": "1.0"
    },
    "swaggerUiPrefix": LazyString(lambda : request.environ.get('HTTP_X_SCRIPT_NAME', ''))
}

app.config['SWAGGER'] = {
    'uiversion': 3
}
app.json_encoder = LazyJSONEncoder
#swagger = Swagger(app, template=templateSwagger, template_file="doc/template.yml")
swagger = Swagger(app, template=templateSwagger)


# routes pour partage WSGI
app.wsgi_app = ReverseProxied(app.wsgi_app)

# Chargement fichier de conf
myhost = os.uname()[1]
if myhost == 'hylaweb':
    app.config.from_object('config.ProdConf')
    print 'Config prod'
else:
    app.config.from_object('config.DevConf')
    print 'config dev'

# Initialisation debug mode
debug_mode = app.config['DEBUG']

# Extensions autorisés pour upload
ALLOWED_EXTENSIONS = set(['ps', 'pdf'])

# Extensions autorisés pour upload
CACHE_ARCHIVE = "cacheArchive"

# autoriation d'activé le cache pour les photos d'archives
ACTIVE_CACHE_ARCHIVE = True

###########################################################################################
def connect_db(dbname):
    """Connects to the specific database."""
    if dbname == 'postgres_db':
        #Define our connection string
        conn_string = "host='"+app.config['PGSQL']['host']+"' dbname='"+app.config['PGSQL']['db']+"' user='"+app.config['PGSQL']['user']+"' password='"+app.config['PGSQL']['pass']+"'"
        # get a connection, if a connect cannot be made an exception will be raised here
        rv = psycopg2.connect(conn_string)
    return rv

def get_db(dbname):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, dbname):
        setattr(g,dbname,connect_db(dbname))
    return getattr(g,dbname)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'oracle_db'):
        g.oracle_db.close()
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()

# Upload un fichier en FTP
def upload(ftp, file, filedest):
    ftp.cwd(app.config['HYLAFTP']['fold'])
    ftp.storbinary("STOR " + filedest, open(file))

# Télecharge un fichier en FTP
def download(ftp, file):
    temp = None
    fileDownloaded = 'static/FaxND.pdf'  # default file
    print("**** download %s" %file)
    with tempfile.NamedTemporaryFile(delete = False) as temp:
        try:
            ftp.retrbinary('RETR ' + file, temp.write)
            fileDownloaded = temp.name
            
        except:
            print("*** ERREUR *** telechargement doc : %s" %file)
            pass
    return fileDownloaded

# Renvoie le numero du document d'un fax si le user a les droits
# en fonction de l'id du fax, du type (rapport ou fax) et du guid
def get_num_doc(type_fax, idFax, guid, file_type):

    if type_fax == "TX":
        table = "emission"
        select = "ndoc_arc, ndoc_rap"
        
    elif type_fax == "RX":
        table = "reception"
        select = "ndoc_arc"

    sql = """
        SELECT """ + select + """ FROM """ + table + """ as tab where tab.id=%(idFax)s
        and exists (select s.id FROM service s
                          INNER JOIN groupe_serv gs ON(s.id = gs.id_service)
                          INNER JOIN groupe g ON (gs.id_groupe = g.id)
                          INNER JOIN util_groupe ug ON (g.id = ug.id_groupe)
                          INNER JOIN (SELECT u.id FROM utilisateur u WHERE guid_ad=%(guid)s LIMIT 1) u
                                  ON (u.id = ug.id_util)
          where s.id= tab.id_service)          
        """
    
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'idFax': idFax, 'guid': guid})
    res = cursor.fetchone()
    cursor.close()

    # on recupere le document d'archivage
    if file_type == "fax" and res is not None:
        return res["ndoc_arc"]

    # on recupere le rapport d'emission
    elif file_type == "rapport" and res is not None:
        return res["ndoc_rap"]

    else:
        return None

## recupere les donnees d'un fax a partir du numero de document
def get_infos_archive(ndoc):
    sql = ''' SELECT jbox.ftpuser AS ftpuser, jbox.ftppass AS ftppass, jbox.host_name AS hostname, 
        base.repert_racine AS racine, face.nom_repert AS repert, doc.nom_fic AS nom, doc.vers AS version,
        doc.typ_fich AS type
        FROM doc
        INNER JOIN face ON doc.face = face.face
        INNER JOIN base ON face.base = base.base
        INNER JOIN jbox ON face.jbox = jbox.jbox
        WHERE doc.ndoc = %(NDOC)s
    '''

    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {"NDOC": ndoc})
    data = cursor.fetchone()
    cursor.close()
    
    # si la requete est valide
    if data is not None:
        return data
    else:
        print("Erreur impossible de recuperer les donnees pour le numero de doc: %s" %ndoc)
        return None

# Retourne les extensions possible pour un fichier
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



########################################################################
# type : API                                                           #
# desc :                                                               #
########################################################################
@app.route('/',methods=['GET'])
def API():
    data = {
        'title' : 'API Valide',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }
    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : POST: demande la mise a jour de l'utilisateur                 #
#        GET: recupere les infos sur l'utilisateur                     #
########################################################################
@app.route('/api/V1.0/user/<guid>',methods=['GET', 'POST'])
@swag_from('doc/user.get.yml', methods=['GET'])
@swag_from('doc/user.post.yml', methods=['POST'])
def user(guid=None):
    data = {
        'title' : '',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }

    if request.method == 'GET': #GET
        sql = """
            SELECT * FROM utilisateur WHERE guid_ad LIKE %(GUID)s
        """
        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'GUID' : guid})
        user = cursor.fetchone()
        cursor.close()

        data['title'] = 'Return info USER : ' + guid
        data['items'] = user
        statusCode = 200

    else:   #POST
        data['title'] = 'Update USER : ' + guid
        sql = """
            UPDATE utilisateur SET maj_grp='O' WHERE guid_ad LIKE %(GUID)s RETURNING id
        """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'GUID' : guid})
        rowcount = cursor.rowcount

        if rowcount == 0:
            # Pas de mise à jour donc nouveau User
            data['title'] = 'New USER : ' + guid
            sql = """
                INSERT INTO utilisateur (maj_grp, guid_ad) VALUES ('O', %(GUID)s) RETURNING id
            """
            cursor.execute(sql, {'GUID' : guid})

        db.commit()
        user = cursor.fetchone()
        cursor.close()
        statusCode = 201


    # Items return ID (POST) or INFO (GET)
    data['items'] = user
    return jsonify(data),statusCode

########################################################################
# type : API                                                           #
# desc : Afficher un fax, on recupere le fax au format pdf             #
########################################################################
@app.route('/api/V1.0/wt/fax/<filename>/pdf',methods=['GET'])
@swag_from('doc/getpdf_wtfax.yml')
def getpdf_wtfax(filename):
    #  TODO : Actuellement la conversion PDF se fait dans l'automate
    #         Voir si il ne faut pas la déplacer dans cet API
    file = os.path.join(app.config['FOLDER']['wait'], filename + '.pdf')
    try:
	    return send_file(file, mimetype='application/pdf', attachment_filename='fax.pdf')
    except Exception as e:
        return str(e)


########################################################################
# type : API                                                           #
# desc : GET: return OK if filename exist                              #
#        DELETE: Suppression d'un FAX en attente d'envoi               #
########################################################################
@app.route('/api/V1.0/wt/fax/<filename>',methods=['GET', 'DELETE'])
@swag_from('doc/exist_wtfax.yml', methods=['GET'])
@swag_from('doc/del_wtfax.yml', methods=['DELETE'])
def exist_wtfax(filename):
    data = {
        'title' : '',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }

    if request.method == 'GET':
        data['title'] = 'Exist Fax [%s]' %filename
        file = os.path.join(app.config['FOLDER']['wait'], filename)
        if not os.path.isfile(file):
            data['status'] = 'KO'
        

    elif request.method == 'DELETE':
        data['title'] = 'Send Fax (delete)'
         
        file = os.path.join(app.config['FOLDER']['wait'], filename)
        try:
            for ext in ['.ctl','.ps','.pdf']:
                fileSUPP = file.rsplit('.', 1)[0] + ext
                if os.path.isfile(fileSUPP):    os.remove(fileSUPP)
        except Exception as e:
            data['status'] = 'KO'
            data['description'] = 'Exception : ' + str(e)
    
    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : GET: Recuperation des fichiers en attente                     #
#        POST: Mise en attente d'un fax                                #
########################################################################
@app.route('/api/V1.0/standby/fax', methods=['GET', 'POST', 'DELETE'])
@swag_from('doc/get_standby_fax.yml', methods=['GET'])
@swag_from('doc/post_standby_fax.yml', methods=['POST'])
@swag_from('doc/delete_standby_fax.yml', methods=['DELETE'])
def get_fax_standed_by():
    data = {
        'title' : 'Fax mis en attente',
        'items' : [],
        'status': 'OK',
        'description' : ''
    }
   
    login = request.args.get('login', '')
    filename = request.form.get('filename', '')

    # Recuperation des fichiers en attente (ex: joannes.c.115.2206201812023004.pdf) 
    if request.method == 'GET':
        if login != '':
            data['description'] = 'Recuperation des fichier mis en attente par le user %s' %login
            Filemask = login + ".*.pdf"
            # on recupere les fichiers en ignorant la casse
            rule = re.compile(fnmatch.translate(Filemask), re.IGNORECASE)
            files = [name for name in os.listdir(app.config['FOLDER']['standby']) if rule.match(name)]

            # trie le fichier
            # on creer les masques
            listing = []
            for file in files:
                listing.extend(glob.glob(os.path.join(app.config['FOLDER']['standby'], file)))
            listing.sort(key=os.path.getmtime)
            # on recupere dans l'ordre du plus récent au plus vieux
            listing.reverse()

            # on limite le nombre de fax à recuperer
            listing = listing[:app.config.get('LIMIT_FAX_ATTENTE')]

            # On recupere que le basename  plus le dossier relatif STANDBY sans l'extension
            data["items"] = ['STANDBY/' + os.path.basename(os.path.splitext(filename)[0]) for filename in listing]
        else:
            data['status'] = 'KO'
            data['description'] = 'Pas de login'

    # Recuperation des fichiers en attente  
    elif request.method == 'POST':
        # si le fichier est renseigné
        if filename != '':
            print(filename)
            data['description'] = 'Mis en attente du fichier %s' %filename
            # pour le fichier ctl, pdf et ps s'il existe on les deplace
            extension = ['.ctl','.ps','.pdf']
            for ext in extension:
                file = filename + ext
                if os.path.isfile(os.path.join(app.config['FOLDER']['wait'], file)):
                    shutil.move(os.path.join(app.config['FOLDER']['wait'], file), os.path.join(app.config['FOLDER']['standby'], file))
                    data["description"] = "le fichier a été déplacé"
                
                # on verifie que le fichier pdf s'est bien deplacer existe bien
                else: 
                    if ext == '.pdf':
                        data['status'] = 'KO'
                        data["description"] = "le fichier: %s n'existe pas" %os.path.join(app.config['FOLDER']['wait'], file)
        else: 
            data['status'] = 'KO'
            data['description'] = 'Le fichier n\'est pas renseigné'

    # suppression d'un fax
    elif request.method == 'DELETE':
        if filename != '':
            data['description'] = 'Suppression du fax %s' %filename
            filename = os.path.join(app.config['FOLDER']['wait'], filename)
            try:
                for ext in ['.ctl','.ps','.pdf']:
                    fileSUPP = filename + ext
                    if os.path.isfile(fileSUPP):
                        os.remove(fileSUPP)
            except Exception as e:
                data['status'] = 'KO'
                data['description'] = 'Exception : ' + str(e)
            
           
            # pour le fichier ctl, pdf et ps s'il existe on les deplace
        else:
            data['status'] = 'KO'
            data['description'] = 'Le fichier n\'est pas renseigné'
       
    return jsonify(data)

########################################################################
# type : API                                                           #
# desc : Affiche la premiere page d'un fax                             #
########################################################################
@app.route('/api/V1.0/fax/<format>', methods=['GET'])
@swag_from('doc/get_file_standby_fax.yml', methods=['GET'])
def get_file_fax(format=None):
    data = {
        'title' : 'Recuperation image fax',
        'items' : [],
        'status': 'OK',
        'description' : ''
    }

    filename = request.args.get('file', '')
    if filename != '':
        filename = os.path.join(app.config['FOLDER']['wait'], filename)
        if format == 'jpeg':
            if os.path.isfile(filename):
                file = open(os.path.join(app.config['FOLDER']['wait'], filename), 'r')
                with tempfile.NamedTemporaryFile(delete = True) as temp:
                    pages = convert_from_path(filename, dpi=200, first_page=1, last_page=1, thread_count=2)
                    size = 200, 400
                    image = pages[0]
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(temp, 'JPEG', optimize=True) 
                        
                    resp = send_file(temp.name, mimetype='image/jpeg')
                return resp

    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : retourne le PDF du fax recu                                   #
########################################################################
@app.route('/api/V1.0/rx/fax/<int:idFax>/pdf',methods=['GET'])
@swag_from('doc/getpdf_rxfax.yml')
def getpdf_rxfax(idFax):
    faxND  ='static/FaxND.pdf'  # default file
    guid = request.args.get('guid', '-')
    sql ="""
        SELECT faxname FROM reception R where id=%(idFax)s
          and exists (select s.id FROM service s
                          INNER JOIN groupe_serv gs ON(s.id = gs.id_service)
                          INNER JOIN groupe g ON (gs.id_groupe = g.id)
                          INNER JOIN util_groupe ug ON (g.id = ug.id_groupe)
                          INNER JOIN (SELECT u.id FROM utilisateur u WHERE guid_ad=%(guid)s LIMIT 1) u
                                  ON (u.id = ug.id_util)
          where s.id= R.id_service)          
    """
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'idFax': idFax, 'guid': guid})
    fax = cursor.fetchone()
    cursor.close()
    if fax != None:

        filename=fax['faxname'].rsplit('.',1)[0]
        file = os.path.join(app.config['FOLDER']['rx'], filename + '.pdf')
        print file
        if not(os.path.isfile(file)):
            file = faxND
    else:
        file = faxND

    return send_file(file, mimetype='application/pdf', attachment_filename='fax.pdf')


########################################################################
# type : API                                                           #
# desc : retourne les infos sur le fax                                 #
########################################################################
@app.route('/api/V1.0/rx/fax/<int:idFax>',methods=['GET'])
@swag_from('doc/get_rxfax.yml')
def get_rxfax(idFax):
    data = {
        'title' : '',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }

    guid = request.args.get('guid','')

    # Verification idfax
    if idFax==None:
        data['title'] = "ID de fax n'est pas defini"
        data['status'] = 'KO'
        return jsonify(data)

    sql ="""
        SELECT COALESCE(CAST(FU.id_util AS VARCHAR(8)),'') AS lu,
               COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag,
               etatnew, faxname,
               COALESCE(CAST(R.ndoc_arc AS VARCHAR(15)),'') AS ndoc_arc,
               CASE WHEN (annu_inverse IS NOT NULL) THEN annu_inverse ELSE sender END AS sender,
               TO_CHAR(datetime, 'YYYY-MM-DD HH24:MI:SS') AS datetime, npages,
               CAST(commid AS VARCHAR(100)) AS commid,
               COALESCE(proprietaire,'') AS proprietaire, R.id AS id,
               affichable, id_service
        FROM reception R LEFT OUTER JOIN
                (fax_util FU INNER JOIN (SELECT id FROM utilisateur WHERE guid_ad=%(GUID)s LIMIT 1) U ON (U.id = FU.id_util))
                ON (R.id = FU.id_fax)
        WHERE R.id = %(ID_FAX)s;
    """
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'ID_FAX': idFax, 'GUID': guid})
    fax = cursor.fetchone()
    cursor.close()

    data['title'] = 'Info fax en reception num %s' %idFax
    if fax != None:
        data['items'] = fax
        data['status'] = 'OK'
    else:
        data['description'] = 'aucune info recuperee'
        data['status'] = 'KO'

    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Retourne une liste de fax en reception d'un service           #
#        On peut passer en parametre le guid du user pour savoir       #
#        s'il a lu chaque fax                                          #
########################################################################
@app.route('/api/V1.0/rx/<id_serv>/fax', methods=['GET'])
@app.route('/api/V1.0/rx/<id_serv>/fax/<nbfax_aff>', methods=['GET'])
@app.route('/api/V1.0/rx/<id_serv>/fax/<nbfax_aff>/<int:dernier_id_aff>', methods=['GET'])
@swag_from('doc/list_rxfax.yml')
def get_list_fax_RX_serv(id_serv=None, nbfax_aff='1000', dernier_id_aff=999999999):
    data = {
        'title' : 'Liste fax reception',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }
    # recup guid user connecte pour securisation acces liste
    guid = request.args.get('guid','')
    # recup proprietaire pour filtrage des FAX
    proprietaire = request.args.get('proprietaire','')
    
    # Verification id service
    if id_serv=="" or id_serv==None:
        data['description'] = "ID de service n'est pas defini"
        data['status'] = 'KO'
        return jsonify(data)

    sql = """
        SELECT COALESCE(CAST(FU.id_util AS VARCHAR(8)),'') AS lu,
               COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag,
               etat, etatnew, faxname,
               COALESCE(CAST(R.ndoc_arc AS VARCHAR(15)),'') AS ndoc_arc,
               CASE WHEN (annu_inverse IS NOT NULL) THEN annu_inverse ELSE sender END AS sender,
               TO_CHAR(datetime, 'YYYY-MM-DD HH24:MI:SS') AS datetime, npages,
               CAST(commid AS VARCHAR(100)) AS commid,
               COALESCE(proprietaire,'') AS proprietaire, R.id AS id
        FROM reception R LEFT OUTER JOIN
                 (fax_util FU INNER JOIN (SELECT id FROM utilisateur WHERE guid_ad=%(GUID)s LIMIT 1) U ON (U.id = FU.id_util))
                 ON (R.id = FU.id_fax)
        WHERE R.id_service = %(ID_SERV)s
        AND R.etat & 1 > 0
        AND datetime > now() - interval '7 days'
        AND R.affichable = 1
        AND R.id < %(DERNIER_ID)s
        AND ((proprietaire is null) OR
             (proprietaire like 'EMB reco%%') OR
             (CASE WHEN (%(PROPRIETAIRE)s <> '') THEN (proprietaire = %(PROPRIETAIRE)s)
                                                 ELSE (proprietaire is not null) END))
        ORDER BY R.datetime DESC
        LIMIT %(NBFAX)s;
    """
    
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'GUID': guid, 'ID_SERV': id_serv, 'NBFAX': nbfax_aff, 'DERNIER_ID': dernier_id_aff, 'PROPRIETAIRE': proprietaire})
    fax_rx = cursor.fetchall()
    cursor.close()

    data['description'] = 'Liste des fax en reception pour le service %s' %id_serv
    data['items'] = fax_rx

    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Retourne une liste de fax en emission d'un service            #
########################################################################
@app.route('/api/V1.0/tx/<id_serv>/fax', methods=['GET'])
@app.route('/api/V1.0/tx/<id_serv>/fax/<nbfax_aff>', methods=['GET'])
@app.route('/api/V1.0/tx/<id_serv>/fax/<nbfax_aff>/<int:dernier_id_aff>', methods=['GET'])
@swag_from('doc/list_txfax.yml')
def get_list_fax_TX_serv(id_serv=None, nbfax_aff='1000', dernier_id_aff=999999999):
    data = {
        'title' : 'Liste fax emission',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }
    
    # Verification id service
    if id_serv=="" or id_serv==None:
        data['description'] = "ID de service n'est pas defini"
        data['status'] = 'KO'
        return jsonify(data)

    sql = """
        SELECT E.id, 
        TO_CHAR(E.datetime, 'YYYY-MM-DD HH24:MI:SS') AS datetime, 
        TO_CHAR(E.date_envoi, 'YYYY-MM-DD HH24:MI:SS') AS date_envoi, 
        TO_CHAR(E.datetime_dif, 'YYYY-MM-DD HH24:MI:SS') AS datetime_dif, 
        COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(E.tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag,
        E.coversubject, E.covernotes, E.coverpage, E.dest, E.numdest, E.sendername, E.numsender, E.rtimes, E.dials, 
        E.tries, E.npages, E.ndoc_arc, E.nb_envoi, E.status, E.ndoc_rap, E.id_service, E.cc_exp, E.numdest_dial,
        E.mail, E.id_util, E.maj, E.id_server, E.commid, E.jobid, E.modem,
        COALESCE(CAST(E.jobtime AS TEXT),'') AS jobtime,
        TO_CHAR(X.datetime, 'YYYY-MM-DD HH24:MI:SS') AS date_current_send,
        CASE WHEN E.status='DE'
        THEN TO_CHAR(X.datetime + cast('00:'||COALESCE(CAST(E.rtimes AS TEXT), '00')||':00' as interval), 'YYYY-MM-DD HH24:MI:SS') 
        END as date_next_send
        FROM emission E LEFT OUTER JOIN xferfaxlog X on (E.jobid=X.jobid AND E.id_server=X.server_id AND E.commid=X.commid)
        WHERE E.id_service = %(ID_SERV)s
        AND E.datetime > now() - interval '7 days'
        AND E.affichable = 1
        AND E.id < %(DERNIER_ID)s
        ORDER BY E.id DESC
        LIMIT %(NBFAX)s;
    """
    
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'ID_SERV': id_serv, 'NBFAX': nbfax_aff, 'DERNIER_ID': dernier_id_aff})
    fax_tx = cursor.fetchall()
    cursor.close()

    data['description'] = 'Liste des fax en emission pour le service %s' %id_serv
    data['items'] = fax_tx
    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : retourne les infos sur le fax en emission                     #
########################################################################
@app.route('/api/V1.0/tx/fax/<int:idFax>', methods=['GET'])
@swag_from('doc/get_txfax.yml')
def get_txfax(idFax=None):
    data = {
        'title' : 'Info fax en emission num %s' %idFax,
        'items' : '',
        'status': 'OK',
        'description' : ''
    }
    
    # Verification idfax
    if idFax==None:
        data['title'] = "ID de fax n'est pas defini"
        data['status'] = 'KO'
        return jsonify(data)

    sql = """
        SELECT E.id, E.id_server, 
        TO_CHAR(E.datetime, 'YYYY-MM-DD HH24:MI:SS') AS datetime, 
        TO_CHAR(E.date_envoi, 'YYYY-MM-DD HH24:MI:SS') AS date_envoi, 
        TO_CHAR(E.datetime_dif, 'YYYY-MM-DD HH24:MI:SS') AS datetime_dif, 
        COALESCE(CAST(E.jobtime AS TEXT),'') AS jobtime,
        COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(E.tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag,
        E.priority, E.coversubject, E.covernotes, E.papertype, E.resolution, 
        E.filename, E.coverpage, E.dest, E.numdest, E.company, E.sendername, E.numsender, E.telsender, E.location,
        E.typenotify, E.rtimes, E.dials, E.tries, E.jobid, E.commid, E.npages, E.affichable, E.ndoc_arc, E.nb_envoi, 
        E.status, E.ndoc_rap, E.id_service, E.modem, E.nref_ext, E.cc_exp, E.numdest_dial,
        E.mail, E.id_util, E.maj, X.reason,
        TO_CHAR(X.datetime, 'YYYY-MM-DD HH24:MI:SS') AS date_current_send,
        COALESCE(CAST(X.jobtime AS TEXT),'') AS xferjobtime,
        CASE WHEN E.status='DE' 
        THEN TO_CHAR(X.datetime + cast('00:'||COALESCE(CAST(E.rtimes AS TEXT), '00')||':00' as interval), 'YYYY-MM-DD HH24:MI:SS') 
        END as date_next_send
        FROM emission E LEFT OUTER JOIN xferfaxlog X on (E.jobid=X.jobid AND E.id_server=X.server_id AND E.commid=X.commid)
        WHERE E.id = %(ID_FAX)s
    """
     
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'ID_FAX': idFax})
    fax = cursor.fetchone()
    cursor.close()

    if fax != None:
        data['items'] = fax
        data['status'] = 'OK'
    else:
        data['description'] = 'aucune info recuperee'
        data['status'] = 'KO'

    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Annule un fax en cours d'emission                             #
########################################################################
@app.route('/api/V1.0/tx/fax/<int:idFax>/cancel', methods=['POST'])
#@swag_from('doc/cancel_fax.yml')
def cancel_fax(idFax=None):
    data = {
        'title' : 'Annulation du fax ayant l\'id: %s' %idFax,
        'items' : '',
        'status': 'OK',
        'description' : ''
    }

    if idFax is not None:
        sql = """
            UPDATE emission set status='AN', etatnew=etatnew|2 WHERE id=%(ID_FAX)s 
        """
        
        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_FAX': idFax})
        rowcount = cursor.rowcount

        if rowcount == 0:
            data["status"] = "KO"
            data["description"] = "Le fax n'a pas pu être annulé"
        else:
            data["status"] = "OK"
            data["description"] = "Le fax a été annulé"
            db.commit()
        
        cursor.close()
    else:
        data["status"] = "KO"
        data["description"] = "l'id du fax n'est pas valide"
    return jsonify(data)
    

########################################################################
# type : API                                                           #
# desc : Renvoi un fax                                                 #
########################################################################
@app.route('/api/V1.0/tx/fax/<int:idFax>/sendback', methods=['POST'])
#@swag_from('doc/send_back_fax.yml')
def send_back_fax(idFax=None):
    data = {
        'title' : 'Renvoi du fax ayant l\'id: %s' %idFax,
        'items' : '',
        'status': 'OK',
        'description' : ''
    }

    guid = request.form.get('guid', '')

    if idFax is not None:
        # On recupere les infos sur le fax en base
        if guid != '':
            sql = """
                SELECT E.dest, E.numdest, E.ndoc_arc,
                COALESCE(regexp_replace(regexp_replace(regexp_replace(CAST(E.tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), '\\' \\'', ',', 'g')) AS tag
                FROM emission E
                WHERE E.id = %(ID_FAX)s
            """

            db = get_db('postgres_db')
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, {'ID_FAX': idFax})
            fax = cursor.fetchone()
            cursor.close()

            # si le numero de doc est valide on va recuperer le fichier dans les archives
            if fax.get('ndoc_arc') is not None:
                data["items"] = fax
                infosFax = get_infos_archive(fax.get('ndoc_arc'))
                data["infosFax"] = infosFax
        
                file = infosFax["racine"] + "/" + infosFax["repert"] +  "/" + infosFax["nom"] + "." + str(infosFax["version"]) + "." + infosFax["type"]
                print('le fichier demande depuis les archives: %s' %file)            
                
                # si le fichier est vide on ne fait rien
                if file is None:
                    data["status"] = "KO"
                    data["description"] = "le chemin absolu pour acceder au fichier n'est pas valide"

                # sinon on le telecharge
                else:
                    # connexion en ftp
                    ftp = ftplib.FTP(infosFax["hostname"])
                    ftp.login(infosFax["ftpuser"], infosFax["ftppass"])

                    ext = file.rsplit('.', 1)[1].lower()

                    # telechargement de fichier
                    filename = download(ftp, file)
                    newFilename = filename + '.' + ext

                    # on renomme le fichier
                    shutil.move(filename, newFilename) 
                    filename = newFilename
                    
                    print(filename)
                    f = open(filename)
                    files = {'file': f}
                    values = {
                        'sender_guid' : guid,
                        'dest_num'    : fax.get('numdest'),
                        'dest_name'   : fax.get('dest'),
                        'fax_tag'     : fax.get('tag')
                    }

                    try:
                        r = requests.post(app.config.get("URLS").get("send_fax"), files=files, data=values)
                        if r.status_code <> requests.codes.ok:
                            data["status"] = "KO"
                            data["description"] = 'La requete POST a renvoye le code retour : %s' %r.status_code
                    
                        else:
                            retour = json.loads(r.text)
                            print('La requete POST a renvoye le json : %s' %retour)
                            if retour['status']<>'OK':
                                data["status"] = "KO"
                                data["description"] = "Erreur dans l\'execution de l\'API : %s" %retour['description']
                          
                    except Exception as e:
                        data["status"] = "KO"
                        data["description"] = 'Erreur dans l\'execution de la fonction sendfax : ' + str(e)
             
                    finally:
                        f.close()
                        # suppression du fichier
                        os.remove(filename)
                        print('> Fin de la fonction sendfax')
           
            else:
                data["status"] = "KO"
                data["description"] = "le numero de document pour l'archive est invalide"
 
        else:
            data["status"] = "KO"
            data["description"] = "le guid n'est pas valide"

    else:
        data["status"] = "KO"
        data["description"] = "l'id du fax n'est pas valide"
        
    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : renvoie un fax depuis les archives                            #
# en fonction de son identifiant                                       #
########################################################################
@app.route('/api/V1.0/<type_fax>/fax/<idFax>/archive/<format>', methods=['GET'])
def getpdf_archivefax(type_fax=None, idFax=None, format=None):
    data = {
        'title' : 'Fichier archive',
        'items' : '',
        'status': 'OK',
        'description' : 'Recuperation du fichier de type %s aynt l\'id %s au format %s' % (type_fax, idFax, format),
    }

    # recupere le numero d'archivage
    guid = request.args.get('guid', '-')
    file_type = request.args.get('type', 'fax')

    ndoc = get_num_doc(type_fax, idFax, guid, file_type)

    # si le numero de document n'est pas recuperé
    if ndoc is None:
        data["status"] = "KO"
        data["description"] = "le numero de document n'est pas renseigne"
    
    # si le numero de document est recuperé
    else:
        data = get_infos_archive(ndoc)
        
        file = data["racine"] + "/" + data["repert"] +  "/" + data["nom"] + "." + str(data["version"]) + "." + data["type"]
        print('le fichier demande depuis les archives: %s' %file)            

        # si le fichier est vide on ne fait rien
        if file is None:
            data["status"] = "KO"
            data["description"] = "le chemin absolu pour acceder au fichier n'est pas valide"

        # sinon on le telecharge
        else:
            # connexion en ftp
            ftp = ftplib.FTP(data["hostname"])
            ftp.login(data["ftpuser"], data["ftppass"])

            # telechargement de fichier
            filename = download(ftp, file)
            if filename == None:
                file = 'static/FaxND.pdf'
            else:
                file = filename

            if format == "jpeg":
                # test si le fax correspond au fax non disponible
                if file == 'static/FaxND.pdf':
                    fileOut = "static/FaxNDImg.jpg"
                else:
                    filename = idFax + file_type
                    fileOut = os.path.join(CACHE_ARCHIVE, type_fax, filename)
                    if not os.path.exists(fileOut) or ACTIVE_CACHE_ARCHIVE == False:
                        print("le fichier %s a ete genere" %fileOut)
                        pages = convert_from_path(file, dpi=200, first_page=1, last_page=1, thread_count=2)
                        size = 200, 400
                        image = pages[0]
                        image.thumbnail(size, Image.ANTIALIAS)
                        image.save(fileOut, 'JPEG', optimize=True) 
                    # on supprime le fichier une fois envoyé si ce n'est pas le fichier par defaut
                    os.remove(file)
                
                resp = send_file(fileOut, mimetype='image/jpeg')
                return resp
        
            # teste si le format est demandé en pdf
            elif format == "pdf":
                resp = send_file(file, mimetype='application/pdf', attachment_filename='fax.pdf')
                
                # on supprime le fichier une fois envoyé si ce n'est pas le fichier par defaut
                if file != 'static/FaxND.pdf':
                    os.remove(file)
                return resp

    # si rien n'est retourné on considere que la requete n'as pas abouti
    return jsonify(data)

########################################################################
# type : API                                                           #
# desc : retourne les fax en archive du type Emission ou Reception     #
########################################################################
@app.route('/api/V1.0/archive/<type_fax>', methods=['GET'])
@app.route('/api/V1.0/archive/<type_fax>/<nbfax_aff>', methods=['GET'])
@app.route('/api/V1.0/archive/<type_fax>/<nbfax_aff>/<int:dernier_id_aff>', methods=['GET'])
def get_archive(type_fax=None, nbfax_aff='1000', dernier_id_aff=999999999):
    data = {
        'title' : 'Liste des archives',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }
    
    # recupere les tag
    tags = request.args.get('tag', '')
    sqlTag = ''
    if tags != '':
        tags = tags.split(',')
        sqlTag = 'AND $$' + ' & '.join(str('\'' + e + '\':*') for e in tags) + '$$ @@ tag'
    
    sql = None 
    if type_fax == "RX":
        sql = ''' SELECT id, TO_CHAR(datetime, 'YYYY-MM-DD HH24:MI:SS') AS date, sender AS name, 
        numsender AS numtel, ndoc_arc, npages, proprietaire,
        COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag
        FROM reception
        WHERE id_service = %(SERVICE_ID)s 
        AND ndoc_arc IS NOT NULL
        AND datetime >= to_date(%(START_DATE)s, 'YYYY-MM-DD') 
        AND datetime < to_date(%(END_DATE)s, 'YYYY-MM-DD') + interval '1 day '
        AND id < %(DERNIER_ID)s
        ''' + sqlTag  + ''' 
        ORDER BY date DESC
        LIMIT %(NBFAX)s; '''
   
    elif type_fax == "TX":
        sql = ''' SELECT id, etatnew, TO_CHAR(date_envoi, 'YYYY-MM-DD HH24:MI:SS') AS date, dest AS name, 
            numdest AS numtel, ndoc_arc, ndoc_rap, status, npages, sendername,
            (SELECT CAST(U.prenom || ' ' || U.nom || ' <' || U.mail || '>' AS VARCHAR(100))
                FROM utilisateur U 
                WHERE U.id = emission.id_util LIMIT 1) as proprietaire,
            COALESCE(regexp_split_to_array(regexp_replace(regexp_replace(CAST(tag AS VARCHAR(1000)),'^\\'',''),'\\'$',''), E'\\' \\''), '{}') AS tag
            FROM emission
            WHERE id_service = %(SERVICE_ID)s
            AND ndoc_arc IS NOT NULL
            AND ndoc_rap IS NOT NULL 
            AND date_envoi IS NOT NULL
            AND date_envoi >= to_date(%(START_DATE)s, 'YYYY-MM-DD') 
            AND date_envoi < to_date(%(END_DATE)s, 'YYYY-MM-DD') + interval '1 day '
            AND id < %(DERNIER_ID)s
            ''' + sqlTag  + ''' 
            ORDER BY date DESC
            LIMIT %(NBFAX)s; '''

    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    service = request.args.get('service', '')
    
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {
        "START_DATE": start_date, 
        "END_DATE": end_date,
        "SERVICE_ID": service,
        "NBFAX": nbfax_aff,
        "DERNIER_ID": dernier_id_aff
        })
    res = cursor.fetchall()
    cursor.close()

    data["items"] = {
        "fax": res,
        "type": type_fax
    }
    return jsonify(data)

########################################################################
# type : API                                                           #
# desc : Envoi d'un FAX via une requete POST                           #
########################################################################
@app.route('/api/V1.0/send/fax',methods=['POST'])
def send_fax():
    
    today = datetime.datetime.now()
    unique = md5(str(today)).hexdigest()   #generate md5 pour unicite du fichier

    guid = request.form.get('sender_guid','')
    filename = request.form.get('filename','')

    data = {
        'title' : 'Send Fax (POST)',
        'items' : '',
        'status': 'KO',
        'description' : ''
    }

    dest = {'Numdest'  : request.form.get('dest_num',''),
          'Dest' : request.form.get('dest_name','')
    }
    fax = {'Type'        : 'EM',
          'Priority'     : request.form.get('fax_priority','127'),
          'Resolution'   : request.form.get('fax_resolution','low'),
          'Papertype'    : request.form.get('fax_papertype','a4'),
          'Datetime'     : request.form.get('fax_datetime',today.strftime('%Y-%m-%d %H:%M')),
          'Datetime_dif' : request.form.get('fax_datetime_dif','NOW'),
          'Tag'          : request.form.get('fax_tag','').replace("\"","'"),
          'Coverpage'    : request.form.get('fax_coverpage',''),
          'Coversubject' : request.form.get('fax_coversubject','').replace("\"","'").replace("\n","\\\\n"),
          'Covernotes'   : request.form.get('fax_covernotes','').replace("\"","'").replace("\n","\\\\n"),
          'Filename'     : ''
    }
    # Verification du GUID
    if guid=='':
        data['description'] = 'Manque GUID utilisateur'
        return jsonify(data)
    # Verification du Numdest
    if dest['Numdest']=='':
        data['description'] = 'Manque num fax destinataire'
        return jsonify(data)
    elif len(dest['Numdest'].split(';'))>5:
        # Mise à jour de la prioité
        # Priorité basse si nb dest > 5
        fax['Priority'] = '200' 

    # Coverpage par defaut
    if (fax['Coversubject']<>'' or fax['Covernotes']<>'') and fax['Coverpage']=='':
        fax['Coverpage'] = '/opt/CoverPages/faxcover.ps'
    # verification des parametre de la coverpage
    if (fax['Coverpage']<>'' and fax['Coversubject'] == ''):
        data['description'] = 'Manque sujet pour la page de garde'
        return jsonify(data)

    if 'file' not in request.files and filename=='' and fax['Coverpage']=='':
        data['description'] = 'Manque fichier fax (PS) et nom du fichier fax est vide'
        return jsonify(data)
    elif filename<>'':
        fileList = []
        for f in filename.split(';'):
            fileList.append(os.path.join(app.config['FOLDER']['wait'], f))
        for f in fileList:
            if not os.path.isfile(f):
                data['description'] = 'le fichier %s n''existe pas' %f
                return jsonify(data)
            elif not allowed_file(f):
                data['description'] = 'Extension fichier non autorise'
                return jsonify(data)
    elif 'file' in request.files:
        files = request.files.getlist('file')
        for file in files:
            if not(file and allowed_file(file.filename)):
                data['description'] = 'Extension fichier non autorise'
                return jsonify(data)

    sql ="""
        SELECT CAST(service.id as CHARACTER VARYING) AS Idservice, CAST(utilisateur.id as CHARACTER VARYING) as Id,  prenom || ' ' || nom AS Sendername,
        utilisateur.tel AS Telsender, fax AS Numsender, mail AS Mail, agence.libelle AS Company,
        agence.localisation AS Location
        FROM utilisateur, service, agence WHERE guid_ad = %(guid)s
        AND service.id = utilisateur.id_serv_default AND agence.id = service.id_agence;
    """
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'guid': guid})
    sender = cursor.fetchone()
    cursor.close()

    if sender == None:
        data['description'] = 'le GUID %s n''est pas valide' %guid
        return jsonify(data)

    print sender
    # Login FTP
    ftp = ftplib.FTP(app.config['HYLAFTP']['host'])
    ftp.login(app.config['HYLAFTP']['user'], app.config['HYLAFTP']['pass'])

    faxListe=[]
    # Cas ou filename est fourni
    if filename<>'':
        i = 0
        for f in fileList:
            i+=1
            ext = f.rsplit('.', 1)[1].lower()
            faxListe.append('FAX'+ str(sender['id']) + '-' + unique + '-' + str(i) + '.' + ext)
            upload(ftp, f, faxListe[-1])
    # Cas ou le fichier est envoyé en Upload
    elif 'file' in request.files:
        # Upload PS file
        files = request.files.getlist('file')
        i = 0
        for file in files:
            ext = file.filename.rsplit('.', 1)[1].lower()
            with tempfile.NamedTemporaryFile(delete = True) as f:
                i+=1
                f.write(file.read())
                f.flush()
                faxListe.append('FAX'+ str(sender['id']) + '-' + unique + '-' + str(i) + '.' + ext)
                upload(ftp, f.name, faxListe[-1])
    #creation de la liste des FAX
    fax['Filename'] = ';'.join(faxListe)
    #ecriture du fichier ctl
    parser = ConfigParser.ConfigParser()
    parser.optionxform = lambda option: option  #pour préserver les majuscules
    parser.add_section('FAX')
    parser.add_section('SENDER')
    parser.add_section('DEST')

    for key in fax.keys():
        parser.set('FAX', key, '"%s"' %("" + fax[key]).encode('latin_1'))

    for key in sender.keys():
        parser.set('SENDER', key.title(), '"%s"' %("" + sender[key]).encode('latin_1')) #title : Mets la premiere lettre en majuscule

    for key in dest.keys():
        parser.set('DEST', key, '"%s"' %("" + dest[key]).encode('latin_1'))

    # Upload ctl file
    with tempfile.NamedTemporaryFile(delete = True) as f:
        parser.write(f)
        f.flush()
        upload(ftp, f.name, 'CTL' + str(sender['id']) + '-' + unique + '.ctl')
    data['status'] = 'OK'
    ftp.quit()
    # Si nom fichier et si envoi OK
    # Alors on supprime les fichiers
    if filename<>'':
        for f in fileList:
            for ext in ['.ctl','.ps','.pdf']:
                fileSUPP = f.rsplit('.', 1)[0] + ext
                if os.path.isfile(fileSUPP):    os.remove(fileSUPP)
    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Envoi d'un FAX via une requete POST                           #
########## version avec envoi de fichiers en attente (STANDBY)         #
########################################################################
@app.route('/api/V2.0/send/fax',methods=['POST'])
def send_fax_V2():
    
    today = datetime.datetime.now()
    unique = md5(str(today)).hexdigest()   #generate md5 pour unicite du fichier

    guid = request.form.get('sender_guid','')

    # dernier fax envoyé
    filename = request.form.get('filename','')
    #liste des fax en attente
    filewait = request.form.get('filewait','')

    data = {
        'title' : 'Send Fax (POST)',
        'items' : '',
        'status': 'KO',
        'description' : ''
    }

    dest = {'Numdest'  : request.form.get('dest_num',''),
          'Dest' : request.form.get('dest_name','')
    }
    fax = {'Type'        : 'EM',
          'Priority'     : request.form.get('fax_priority','127'),
          'Resolution'   : request.form.get('fax_resolution','low'),
          'Papertype'    : request.form.get('fax_papertype','a4'),
          'Datetime'     : request.form.get('fax_datetime',today.strftime('%Y-%m-%d %H:%M')),
          'Datetime_dif' : request.form.get('fax_datetime_dif','NOW'),
          'Tag'          : request.form.get('fax_tag','').replace("\"","'"),
          'Coverpage'    : request.form.get('fax_coverpage',''),
          'Coversubject' : request.form.get('fax_coversubject','').replace("\"","'").replace("\n","\\\\n"),
          'Covernotes'   : request.form.get('fax_covernotes','').replace("\"","'").replace("\n","\\\\n"),
          'Filename'     : ''
    }
    # Verification du GUID
    if guid=='':
        data['description'] = 'Manque GUID utilisateur'
        return jsonify(data)
    # Verification du Numdest
    if dest['Numdest']=='':
        data['description'] = 'Manque num fax destinataire'
        return jsonify(data)
    elif len(dest['Numdest'].split(';'))>5:
        # Mise à jour de la prioité
        # Priorité basse si nb dest > 5
        fax['Priority'] = '200' 

    # Coverpage par defaut
    if (fax['Coversubject'] <> '' or fax['Covernotes'] <> '') and fax['Coverpage'] == '':
        fax['Coverpage'] = '/opt/CoverPages/faxcover.ps'
    # verification des parametre de la coverpage
    if (fax['Coverpage']<>'' and fax['Coversubject'] == ''):
        data['description'] = 'Manque sujet pour la page de garde'
        return jsonify(data)

    # si le fichier n'existe pas et qu'il n'y pas de page de garde (ERREUR)
    if 'file' not in request.files and filename == '' and fax['Coverpage'] == '':
        data['description'] = 'Manque fichier fax (PS) et nom du fichier fax est vide'
        return jsonify(data)
    # si le nom du fax est renseigne, on prepare l'envoi (cas d'un fax normal via Hylasend)
    elif filename <> '':
        fileList = []
        if filename <> 'new':
            #on ajoute le fichier que si on n'est pas dans le cas d'une page de garde unique (<> new)
            fileList.append(os.path.join(app.config['FOLDER']['wait'], filename))
        # On ajoute a la liste d'envoi les fichiers en attente
        if filewait <> '':
            fileList.extend([os.path.join(app.config['FOLDER']['wait'], f) for f in filewait.split(';')])
        # Verif exitence + extension de chaque fichier a envoyer
        for f in fileList:
            if not os.path.isfile(f):
                print 'le fichier %s n\'existe pas' %f
                data['description'] = 'le fichier %s n\'existe pas' %f
                return jsonify(data)
            elif not allowed_file(f):
                data['description'] = 'Extension fichier non autorise pour le fichier %s' %f
                return jsonify(data)
    # si envoi automatique via HylaPrint (cas confirmation d'affret GTI)
    elif 'file' in request.files:
        files = request.files.getlist('file')
        for file in files:
            if not(file and allowed_file(file.filename)):
                data['description'] = 'Extension fichier non autorise'
                return jsonify(data)


    # Recuperation de l'expediteur
    sql ="""
        SELECT CAST(service.id as CHARACTER VARYING) AS Idservice, CAST(utilisateur.id as CHARACTER VARYING) as Id,  prenom || ' ' || nom AS Sendername,
        utilisateur.tel AS Telsender, fax AS Numsender, mail AS Mail, agence.libelle AS Company,
        agence.localisation AS Location
        FROM utilisateur, service, agence WHERE guid_ad = %(guid)s
        AND service.id = utilisateur.id_serv_default AND agence.id = service.id_agence;
    """
    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'guid': guid})
    sender = cursor.fetchone()
    cursor.close()

    if sender == None:
        data['description'] = 'le GUID %s n''est pas valide' %guid
        return jsonify(data)

    print sender
    # Login FTP
    ftp = ftplib.FTP(app.config['HYLAFTP']['host'])
    ftp.login(app.config['HYLAFTP']['user'], app.config['HYLAFTP']['pass'])

    # Preparation de la liste des fichiers pour l'upload en FTP
    faxListe=[]
    # Cas ou filename est fourni (cas d'un fax normal via Hylasend)
    if filename <> '':
        i = 0
        for f in fileList:
            i+=1
            ext = f.rsplit('.', 1)[1].lower()
            faxListe.append('FAX'+ str(sender['id']) + '-' + unique + '-' + str(i) + '.' + ext)
            print('fichier avant upload', faxListe[-1])
            upload(ftp, f, faxListe[-1])
    # Cas ou le fichier est envoyé en Upload
    elif 'file' in request.files:
        # Upload PS file
        files = request.files.getlist('file')
        i = 0
        for file in files:
            ext = file.filename.rsplit('.', 1)[1].lower()
            with tempfile.NamedTemporaryFile(delete = True) as f:
                i+=1
                f.write(file.read())
                f.flush()
                faxListe.append('FAX'+ str(sender['id']) + '-' + unique + '-' + str(i) + '.' + ext)
                upload(ftp, f.name, faxListe[-1])
    #creation de la liste des FAX
    fax['Filename'] = ';'.join(faxListe)
    #ecriture du fichier ctl
    parser = ConfigParser.ConfigParser()
    parser.optionxform = lambda option: option  #pour préserver les majuscules
    parser.add_section('FAX')
    parser.add_section('SENDER')
    parser.add_section('DEST')

    for key in fax.keys():
        parser.set('FAX', key, '"%s"' %("" + fax[key]).encode('latin_1'))

    for key in sender.keys():
        parser.set('SENDER', key.title(), '"%s"' %("" + sender[key]).encode('latin_1')) #title : Mets la premiere lettre en majuscule

    for key in dest.keys():
        parser.set('DEST', key, '"%s"' %("" + dest[key]).encode('latin_1'))

    # Upload ctl file
    with tempfile.NamedTemporaryFile(delete = True) as f:
        parser.write(f)
        f.flush()
        upload(ftp, f.name, 'CTL' + str(sender['id']) + '-' + unique + '.ctl')
    data['status'] = 'OK'
    ftp.quit()
    # Si nom fichier et si envoi OK
    # Alors on supprime les fichiers
    if filename<>'':
        for f in fileList:
            for ext in ['.ctl','.ps','.pdf']:
                fileSUPP = f.rsplit('.', 1)[0] + ext
                if os.path.isfile(fileSUPP):    os.remove(fileSUPP)
    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Retourne la configuration a l'utilisateur                     #
########################################################################
@app.route('/api/V1.0/HylaNotify/conf', defaults= {'ipClient': "", "template":"config.html"}, methods=['GET']) 
@app.route('/api/V2.0/HylaNotify/conf', defaults= {'ipClient': "", "template": "configwin10.html"}, methods=['GET']) 
@swag_from('doc/config.yml')
def conf(ipClient, template="config.html"):

    checksum_client = request.args.get('checksum')
    # adresse ip request.remote_adr

    #if request.headers.getlist("X-Forwarded-For"):
    #    ipClient = request.headers.getlist("X-Forwarded-For")[0]
    #else:
    #    ipClient = request.remote_addr

    if request.headers.getlist("X-Real-IP"):
        ipClient = request.headers.getlist("X-Real-IP")[0]
    else:
        ipClient = request.remote_addr


    #ipClient = request.remote_addr
    print(ipClient)
    sql = """
        SELECT get_list_server_second(%(IP_CLIENT)s)
    """

    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'IP_CLIENT' : ipClient})
    IpServers = cursor.fetchall()
    print(IpServers)

    req = None
    ipServerValide = ""
    for ipServer in IpServers:
        url_host_valide = app.config.get("URLS").get("host_valide").replace("#SERVER_RABBIT#", ipServer['get_list_server_second'])
        print("URL de verification du serveur rabbit " + url_host_valide)    
        try:
            req = requests.get(url_host_valide, timeout=0.5)
        except requests.exceptions.ConnectionError:
            print("Impossible de joindre l\'host rabbit: ConnectionError'")
            #data['description'] = 'Impossible de joindre l\'host rabbit: ConnectionError'
        except requests.exceptions.Timeout:
            print("Impossible de joindre l\'host rabbit: Timeout")
            #data['description'] = 'Impossible de joindre l\'host rabbit: Timeout'
        else:
            ipServerValide = ipServer['get_list_server_second']
            break  
    
    # JSON existant
    if req is not None:
        json = render_template(template, hostRabbit=ipServerValide, checksum=None).encode("UTF-8")
        ks = hashlib.md5(json)
        checksum = ks.hexdigest()

        # version du fichier de conf identique
        if checksum==checksum_client:
            data = {
                'title' : 'Configuration',
                'items' : '',
                'status': 'OKIDEM',
                'description' : 'Version identique a la version local pour l\'adresse ip: %s' %ipClient
            }
            return jsonify(data)
        
        # Version du fichier de conf different
        else:
            return render_template(template, hostRabbit=ipServerValide, checksum=checksum).encode("UTF-8")

    # Cas ou il n'y a pas de serveur Rabbit Valide en ligne
    data = {
        'title' : 'Configuration',
        'items' : '',
        'status': 'KO',
        'description' : 'Host Rabbit invalide: %s' %ipClient
    }
    return jsonify(data)
    

########################################################################
# type : API                                                           #
# desc : Recuperation liste des destinataires                          #
########################################################################
@app.route('/api/V1.0/user/<guid>/dest', methods=['GET'])
#@swag_from('doc/dest.yml')
def list_destinataire(guid=None):
    """Retourne le carnet d'adresse du user"""
    data = {
        'title' : 'Annuaire',
        'items' : '',
        'status': 'OK',
        'description' : ""
    }
    searchword = None
    searchword = request.args.get('search')
    print("mot de recherche ", searchword)
    
    # Pas d'id client valide
    if guid == "NULL" or guid == None:
        print("user ayant un id service par defaut a " + guid)
        data['status'] = 'KO'
        data['description'] = "le service par defaut de l'employe ayant l'id  %s n'est pas defini " %guid
        return jsonify(data) # serveur incapable de produire une réponse car id=null

    elif searchword == None or len(searchword) < 3:
        data['status'] = 'KO'
        data['description'] = "Mot de recherche non defini"
        return jsonify(data) # serveur incapable de produire une réponse car searchword inexploitable
    
    # id valide on fait la requete
    else:
        searchword = '%'+searchword+'%'
        sql = """
        SELECT aa.nom, CASE WHEN nomservice='<COMMUN>' THEN 'COMMUN' ELSE nomservice END nomservice, aa.fax
        FROM annu_adresse aa, agence a INNER JOIN service as s ON a.id = s.id_agence
                                       INNER JOIN utilisateur as u ON s.id = u.id_serv_default
        WHERE u.id=(SELECT u.id FROM utilisateur u WHERE guid_ad=%(GUID)s LIMIT 1)
          AND (aa.ag=a.code OR aa.ag='----')
          AND (LOWER(aa.nom) LIKE LOWER(%(CHAINE)s) OR aa.nomservice LIKE LOWER(%(CHAINE)s));
        """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'GUID': guid, 'CHAINE': searchword })
        annuaire = cursor.fetchall()
        #print (annuaire)
        data['items'] = annuaire
        data['description'] = "Annuaire de l'employe ayant l'id  %s " %guid

        # Si l'annuaire est vide
        if len(annuaire)==0:
            data['status'] = 'KO'
            data['description'] = "l'employe ayant l'id %s n'a pas de destinataire " %guid

        return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Recuperation liste des destinataires                          #
########################################################################
@app.route('/api/V1.0/user/dest/import', methods=['POST'])
def import_contact():
    """Ajoute les donnees d'un fichier de contact importé par un user"""
    data = {
        'title' : 'Importation des contacts',
        'items' : [],
        'status': 'OK',
        'description' : ""
    }
    file = request.files.get('file', '')

    #on verifie si le fichier existe
    if file != None:
        filename, ext = os.path.splitext(file.filename)
        if ext == '.txt':
            
            # pour chaque ligne du fichier
            for line in file:
                # si le debut de la chaine commence par 'Nom;' il s'agit de l'entete
                if line[:4] == "Nom;":
                    # on split l'entete
                    entete = line.replace('\r\n', '').split(';')

                    # on recupere l'index pour le nom et le fax
                    indexNom, indexFax = entete.index("Nom"), entete.index("Fax")
               
                # pour la partie contact 
                else:
                    # On supprime le retour chariot
                    line = line.replace('\r\n', '')
                    nom, fax = line.split(';')[indexNom], line.split(';')[indexFax]
                    # ajout des contacts
                    data['items'].append({
                        'nom':nom, 
                        'fax': fax
                    })        

        else:
            data['status'] = 'KO'
            data['description'] = "Fichier n'ayant pas l'extension .txt"
    
    else:
        data['status'] = 'KO'
        data['description'] = "Fichier introuvable"

    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Recuperation liste des destinataires                          #
########################################################################
@app.route('/api/V1.0/user/dest/export', methods=['GET'])
def export_contact():
    """Creer le fichier csv pour les contacts"""
    data = {
        'title' : 'Exportation des contacts',
        'items' : [],
        'status': 'OK',
        'description' : ""
    }
    
    contacts = request.args.get('contacts', '')
    
    #on verifie si des contacts sont exportés
    if contacts != None:
        contacts = json.loads(contacts)
        noms = contacts.get('noms').split(';')
        nums = contacts.get('nums').split(';')

        # on saisit l'entete du fichier
        #entete = "Nom;Fax\r\n"
        entete = "Nom;Fax\r\n"

        # les lignes des contacts
        contacts = [noms[i]+";"+nums[i] for i in range(len(noms))]

        with tempfile.NamedTemporaryFile(delete = True) as temp:
            try:
                fichier = open(temp.name, "w")
                fichier.write(entete)
                for contact in contacts:
                    fichier.write(contact)
                    fichier.write("\r\n")
                fichier.close()
                
                print("Fin d'ecriture du fichier")
                print("Envoi du fichier")
                ## Creation du fichier en python
                return send_file(temp.name, as_attachment=True, attachment_filename="Hylafax_export.txt")
            except:
                print("*** ERREUR *** Exportation des contacts : %s" %file)
                data["status"] = "KO"
                data['description'] = "L'exportation des contacts ne s'est pas effectue"

    return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Recuperation liste des destinataires recents                  #
########################################################################
@app.route('/api/V1.0/user/<guid>/dest/recent', methods=['GET'])
def list_destinataire_recent(guid=None):
    """Retourne la liste des destinataires recent"""
    data = {
        'title' : 'Destinataires recents',
        'items' : '',
        'status': 'OK',
        'description': ''
    }

    # Pas d'id client valide
    if guid=="NULL" or guid==None:
        print("user ayant un id service par defaut a " + guid)
        data["status"] = "KO"
        data['description'] = "le service par defaut de l'employe ayant l'id %s n'est pas defini " %guid
        return jsonify(data) # serveur incapable de produire une réponse car id=null
        
    # id valide on fait la requete
    else:
        sql = """
        SELECT MIN(upper(dest)) dest, numdest, max(id) id
        from emission
        where id_util=(SELECT u.id FROM utilisateur u WHERE guid_ad=%(GUID)s LIMIT 1)
        group by numdest
        order by id desc
        limit %(LIMIT_DEST)s
        """
        print(sql)
        
        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'GUID' : guid, 'LIMIT_DEST': app.config['LIMIT_DESTINATAIRE_RECENT']})
        dests_recents = cursor.fetchall()

        data['items'] = dests_recents
        data['description'] = "Destinataire recent de l'employe ayant l'id %s " %guid

        # Si pas de destinataires recents est vide
        if len(dests_recents)==0:
            data["status"] = "OK"
            data['description'] = "l'employe ayant l'id %s n'a pas de destinataires recent " %guid
        return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Recherche des TAGS                                            #
########################################################################
@app.route('/api/V1.0/user/<guid>/tags', methods=['GET'])
def list_tags(guid=None):
    """Retourne la liste des destinataires recent"""
    searchword = None
    searchword = request.args.get('search')
    print("mot de recherche ", searchword)

    # Pas d'id client valide
    if guid=="NULL" or guid==None:  
        data = {
            'title' : 'Tags',
            'items' : '',
            'status': 'KO',
            'description' : "le service par defaut de l'employe ayant l'id %s n'est pas defini " %guid
        }
        return jsonify(data) # serveur incapable de produire une réponse car id=null

    elif searchword==None:
        data = {
            'title' : 'Tags',
            'items' : '',
            'status': 'KO',
            'description' : "Mot de recherche non defini "
        }
        return jsonify(data) # serveur incapable de produire une réponse car searchword inexploitable

    # id valide on fait la requete
    else:
        searchword = searchword+'%'

        sql = """
        SELECT t.tag, t.datetime FROM tag_service t
        INNER JOIN utilisateur as u ON u.id_serv_default = t.id_service
        WHERE u.id = (SELECT u2.id FROM utilisateur u2 WHERE u2.guid_ad=%(GUID)s LIMIT 1)
        AND ( (LOWER(t.tag) LIKE LOWER(%(CHAINE)s)) OR (UPPER(t.tag) LIKE UPPER(%(CHAINE)s)) )
        ORDER BY t.tag;
        """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'GUID' : guid, 'CHAINE': searchword})
        tags = cursor.fetchall()

        data = {
            'title' : 'Tags',
            'items' : tags,
            'status': 'OK',
            'description' : "Tags de l'employe ayant l'id %s " %guid
        }

        # Si l'annuaire est vide
        if len(tags)==0:
            data = {
                'title' : 'Tags',
                'items' : '',
                'status': 'KO',
                'description' : "L'employe ayant l'id %s n'a pas de tags " %guid
            }

        return jsonify(data)


########################################################################
# type : API                                                           #
# desc : Verifie si HylaNotify est lance                               #
########################################################################
@app.route('/api/V1.0/user/HylaNotify/connected', methods=['GET'])
def check_hylanotify():
    if request.headers.getlist("X-Real-IP"):
        ipClient = request.headers.getlist("X-Real-IP")[0]
    else:
        ipClient = request.remote_addr
    print(ipClient)
    sql = """
        SELECT get_list_server_second(%(IP_CLIENT)s)
    """

    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'IP_CLIENT' : ipClient})
    IpServers = cursor.fetchall()

    data = {
        'title' : '',
        'items' : '',
        'status': 'KO',
        'description' : ''
    }
   
    req = None
    ipServerValide = ""
    # Verification du serveur Rabbit Valide
    for ipServer in IpServers:
        # API Rabbit pour verifier si le vhost HYLAFAX existe
        url_host_valide = app.config.get("URLS").get("host_valide").replace("#SERVER_RABBIT#", ipServer['get_list_server_second'])
        print("Url de verification du serveur rabbit " + url_host_valide )    
        data['title'] = 'Check existence host Rabbit'
        try:
            req = requests.get(url_host_valide, timeout=0.5)
        except requests.exceptions.ConnectionError:
            print("Impossible de joindre l\'host rabbit: ConnectionError'")
            data['description'] = 'Impossible de joindre l\'host rabbit: ConnectionError'
        except requests.exceptions.Timeout:
            print("Impossible de joindre l\'host rabbit: Timeout")
            data['description'] = 'Impossible de joindre l\'host rabbit: Timeout'
        else:
            ipServerValide = ipServer['get_list_server_second']
            break
    
    # JSON existant
    if ipServerValide == "":
        return jsonify(data)

    # print("ipServerValide ", ipServerValide)

    # Recuperation de l'host de la machine
    hostname = socket.gethostbyaddr(ipClient)[0].split(".")[0].upper()
    # recuperation du login de l'utilisateur
    login_ad = request.args.get('login_ad')

    # Fabrication de la queue rabbit
    queueRabbit = urllib.quote_plus(hostname + '\\' + login_ad + '\\HYL\\SYS')
    print(queueRabbit)

    # API Rabbit retournant la liste des queues
    url_queue_name = app.config.get("URLS").get("queue_name").replace("#SERVER_RABBIT#", ipServerValide) + "/" + queueRabbit
    print(url_queue_name)
    data['title'] = 'Check existence queue Rabbit'
    try:
        req = requests.get(url_queue_name, timeout=0.5)
    except requests.exceptions.ConnectionError:
        print("Impossible de recuperer la queue : ConnectionError")
        data['description'] = 'Impossible de recuperer la queue : ConnectionError'
        return jsonify(data)
    except requests.exceptions.Timeout:
        print("Impossible de recuperer la queue : Timeout")
        data['description'] = 'Impossible de recuperer la queue : Timeout'
        return jsonify(data)
    except requests.exceptions.InvalidURL:
        print("Impossible de recuperer la queue : InvalidURL")
        data['description'] = 'Impossible de recuperer la queue : InvalidURL'
        return jsonify(data)
    

    # JSON existant
    if req is not None:
        json = req.json()

        # on verifie si la queue system existe
        if json.has_key("error"):
            data = {
                'title' : 'Check Queue System',
                'items' : '',
                'status': 'KO',
                'description' : 'La queue '+ queueRabbit +' n\'existe pas: '
            }
        # si la queue existe
        else:
            data = {
                'title' : 'Check Queue System',
                'items' : {'HostRabbit': ipServerValide, 'QueueSystem': queueRabbit},
                'status': 'OK',
                'description' : 'La queue '+ queueRabbit + ' existe. '
            }
    return jsonify(data)

########################################################################
# type : API                                                           #
# desc : Recupere les services du user et le service par defaut        #
########################################################################
@app.route('/api/V1.0/user/<guid>/services', methods=['GET', 'POST'])
def get_services(guid=None):
  
    # Pas d'id client valide
    if guid=="NULL" or guid==None:
        data['title'] = "le service par defaut de l'employe ayant l'id n'est pas defini "
        data['status'] = 'KO'
        return jsonify(data) # serveur incapable de produire une réponse car id=null

    data = {
        'title' : '',
        'items' : '',
        'status': 'OK',
        'description' : ''
    }
    
    if request.method == 'GET': #GET
        # On recherche les services accessibles par l'utilisateur
            data['title'] = "Services accessibles par l'utilisateur"    
          
            sql = """
                SELECT DISTINCT a.libelle AS agence, a.id AS id, s.libelle AS service, s.id AS serviceId
                FROM agence a INNER JOIN service s ON (a.id = s.id_agence)
                            INNER JOIN groupe_serv gs ON(s.id = gs.id_service)
                            INNER JOIN groupe g ON (gs.id_groupe = g.id)
                            INNER JOIN util_groupe ug ON (g.id = ug.id_groupe)
                            INNER JOIN (SELECT u.id FROM utilisateur u WHERE guid_ad=%(GUID)s LIMIT 1) u ON (u.id = ug.id_util)
                ORDER BY a.id;
            """

            db = get_db('postgres_db')
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, {'GUID' : guid})
            services = cursor.fetchall()
            cursor.close()

            # recuperation du service par defaut du user
            sql = """
                SELECT u.id_serv_default
                FROM utilisateur u
                WHERE u.id = (SELECT u2.id FROM utilisateur u2 WHERE guid_ad=%(GUID)s)
            """

            db = get_db('postgres_db')
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, {'GUID' : guid})
            service_defaut = cursor.fetchone()
            cursor.close()

            id_service_default = service_defaut["id_serv_default"]
            service_defaut = None

            list_agence=[]
            sorted_data = sorted(services, key=itemgetter('id'))
            #for key, group in itertools.groupby(sorted_data, key=lambda x:x['id']):
            for key, group in itertools.groupby(sorted_data, key=itemgetter('id')):
                site={}
                service = {}
                grp = list(group)
                site['id'] = grp[0]['id']
                site['agence'] = grp[0]['agence']
                site['services'] = []
                for item in grp:
                    service['serviceid'] = item['serviceid']
                    service['service'] = item['service']
                    site['services'].append(service.copy())
                list_agence.append(site.copy())

            # On parcourt l'ensemble des services
            for service in services:
                id_agence = service['id']
                ### On stocke le service par défaut
                if service["serviceid"] == id_service_default:
                    service_defaut = service
  
            data['items'] = {"service_defaut": service_defaut, "agences": list_agence}
            return jsonify(data)

    # Changement du service par defaut du user
    elif request.method == 'POST':  #POST
        id_service = request.form.get('service_defaut', '-')
        data['title'] = "Changement de service par defaut du user nouveau service %s" %id_service    
            
        sql = """
           UPDATE utilisateur set id_serv_default = %(ID_SERVICE)s WHERE guid_ad = %(GUID)s;
        """
        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_SERVICE': id_service, 'GUID': guid})
        rowcount = cursor.rowcount

        if rowcount == 0:
            data["status"] = "KO"
            data["description"] = "le service par defaut de l'utilisateur n'a pas ete mis a jour"
        else:
            data["items"] = {'idService': id_service}
            data["status"] = "OK"
            data["description"] = "le service par defaut de l'utilisateur a ete mis a jour"

        db.commit()
        cursor.close()

        ##
        ## Envoi du message rabbit a hylanotify si l'appli est lancé
        ##
        ipServerValide =  request.form.get('hostRabbit', None)
        queueRabbit = request.form.get('queueSys', None)
        
        #print('host', ipServerValide)
        #print('queue', queueRabbit)

        # si les donnees pour rabbit sont non valide
        if ipServerValide == '' or queueRabbit == '':
            data["status"] = "KO"
            data["description"] = "impossible d'envoyer le message rabbit"
        # sinon on envoie le message
        else:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=ipServerValide, virtual_host="HYLAFAX"))
            channel = connection.channel()

            # envoi du message rabbit pour un mail a Hylanotify
            message = {
                "type": "SERVICE_CHANGE",
                "items": {
                    "idService": id_service
                }
            }

            channel.basic_publish(exchange='',
                                routing_key=queueRabbit,
                                body=json.dumps(message))
            print('envoi d\'un message')
            connection.close()
        return jsonify(data)

########################################################################
# type : API                                                           #
# desc : supprime le fax id_fax de l'affichage des fax recus           #
#        (suppression logique en base)                                 #
########################################################################
@app.route('/api/rx/fax/<id_fax>/delete', methods=['DELETE'])
def delete_fax(id_fax=None):
    print('delete fax : '+ id_fax)
    data = {
        'title' : 'Delete Fax %s' %id_fax,
        'items' : '',
        'status': 'OK',
        'description' : ''
    }

    if request.method == 'DELETE':
        guid = request.form.get('guid', '')

        if guid == "":
            data['status'] = "KO"
            data['description'] = 'Le guid: %s est invalide' %guid
        else:
            sql = """
                UPDATE reception
                SET proprietaire = (CASE WHEN (proprietaire = '' OR proprietaire IS NULL) 
                                      THEN (SELECT nom || ' ' || prenom || ' <' || "mail" || '>'
                                            FROM utilisateur
                                            WHERE guid_ad = %(GUID)s) 
                                      ELSE proprietaire END),
                    affichable = 0, etat = etat | 8
                WHERE id = %(ID_FAX)s;
            """

            db = get_db('postgres_db')
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, {'ID_FAX' : id_fax, 'GUID': guid})
            rowcount = cursor.rowcount
            cursor.close()

            if rowcount == 0:
                data["status"] = "KO"
                data["description"] = "le fax %s n'a pas ete supprime" %id_fax
            else:
                data["description"] = "le fax %s a ete supprime" %id_fax
                db.commit()

        return jsonify(data)     

########################################################################
# type : API                                                           #
# desc : s'approprie un fax recus                                      #
########################################################################
@app.route('/api/rx/fax/<id_fax>/lock', methods=['POST'])
def lock_fax(id_fax=None):
    data = {
        'title' : 'Update Fax',
        'items' : '',
        'status': 'OK',
        'description' : 'Appropriation du fax' + id_fax
    }
    
    if request.method == 'POST': #POST

        proprietaire = request.form.get('proprietaire', '-')

        sql = """
            UPDATE reception SET etat = etat | 8, proprietaire = %(PROPRIETAIRE)s
            WHERE id = %(ID_FAX)s;
            """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_FAX' : id_fax, 'PROPRIETAIRE': proprietaire})
        rowcount = cursor.rowcount

        if rowcount == 0:
            data["status"] = "KO"
            data["description"] = "le fax %s n'a pas ete mis a jour" %id_fax
        else:
            data["description"] = "le fax %s a ete mis a jour " %id_fax

        db.commit()
        cursor.close()
        return jsonify(data)

########################################################################
# type : API                                                           #
# desc : libere un fax recus (suppression du proprietaire en base)     #
########################################################################
@app.route('/api/rx/fax/<id_fax>/unlock', methods=['POST'])
def unlock_fax(id_fax=None):
    data = {
        'title' : 'Update Fax',
        'items' : '',
        'status': 'OK',
        'description' : 'Appropriation du fax' + id_fax
    }
    
    if request.method == 'POST': #POST   
        sql = """
            UPDATE reception SET etat = etat | 8, proprietaire = NULL WHERE id = %(ID_FAX)s;
        """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_FAX' : id_fax})
        rowcount = cursor.rowcount

        if rowcount == 0:
            data["status"] = "KO"
            data["description"] = "le fax %s n'a pas ete supprime" %id_fax
        else:
            data["description"] = "le fax %s a ete supprime " %id_fax

        db.commit()
        cursor.close()
        return jsonify(data)

########################################################################
# type : API                                                           #
# desc : Envoie d'un fax vers un autre service                         #
########################################################################
@app.route('/api/rx/fax/<id_fax>/move', methods=['POST'])
def move_fax(id_fax=None):
    ''' Déplacement d'un fax vers un nouveau service '''
    data = {
        'title' : 'Update Fax',
        'items' : '',
        'status': 'OK',
        'description' : 'Deplacement du fax' + id_fax
    }
    # on recupere l'ancien service
    id_old_service = request.form.get('id_old_service', '')
    
    # on recupere le nouveau service du fax
    id_new_service = request.form.get('id_new_service', '')

    # On recupere l'host Rabbit
    hostRabbit = request.form.get('hostRabbit', '')

    sql = """
        UPDATE reception SET etat = etat | 8, id_service = %(ID_NEW_SERVICE)s WHERE id = %(ID_FAX)s;
    """

    db = get_db('postgres_db')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql, {'ID_FAX' : id_fax, 'ID_NEW_SERVICE': id_new_service})
    rowcount = cursor.rowcount

    if rowcount == 0:
        data["status"] = "KO"
        data["description"] = "le fax %s n'a pas ete deplace " %id_fax
    else:
        data["description"] = "le fax %s a ete deplace " %id_fax

    db.commit()
    cursor.close()

    # on envoie un message rabbit pour notifier l'ancien service que le fax a été deplacer
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostRabbit, virtual_host="HYLAFAX"))
    channel = connection.channel()
    message = {
        "type": "RX-UPD",
        "id": id_fax,
    }

    channel.basic_publish(
        exchange='hyla.abonnement',
        routing_key='RX'+id_old_service,
        body=json.dumps(message))
    connection.close()

    return jsonify(data)

########################################################################
# type : API                                                           #
# desc : Notifie l'utilisateur que le fax a été lu                     #
########################################################################
@app.route('/api/rx/fax/<id_fax>/read', methods=['POST'])
def read_fax(id_fax=None):
    data = {
        'title' : 'Update Fax',
        'items' : '',
        'status': 'OK',
        'description' : 'Lecture du fax ' + id_fax
    }

    # on recupere le guid de l'utilisateur
    guid = request.form.get('guid', '-')
    
    if request.method == 'POST': #POST
        sql = """
                INSERT INTO fax_util VALUES ((SELECT u.id FROM utilisateur u WHERE guid_ad=%(GUID)s LIMIT 1), %(ID_FAX)s) 
            """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_FAX' : id_fax, 'GUID': guid})
        rowcount = cursor.rowcount

        if rowcount == 0:
            data["status"] = "KO"
            data["description"] = "Erreur UPDATE le user n'a pas lu le fax %s" %id_fax
        else:
            data["description"] = "UPDATE: le user a lu le fax %s" %id_fax

        db.commit()
        cursor.close()
        return jsonify(data)
       
########################################################################
# type : API                                                           #
# desc : transfere le fax                                              #
#       - Deplace le fax dans le wait                                  #
########################################################################
@app.route('/api/rx/fax/<id_fax>/transfer/<type_trf>', methods=['GET', 'POST'])
def transfer_fax(id_fax=None, type_trf=None):
    data = {
        'title' : 'Transfert du fax %s vers %s' %(id_fax, type_trf),
        'items' : '',
        'status': 'OK',
        'description' : '',
    }
    
    # recuperation du login de l'utilisateur
    login_ad = request.args.get('login_ad', '')
    queueRabbit = request.args.get('queueSys', '')
    hostRabbit = request.args.get('hostRabbit', '')

    ##
    ## Transfert par Hylasend
    ##
    if type_trf == "FAX":
        # besoin d'avoir le login_ad pour nommer le fichier
        if login_ad == '':
            data['status'] = "KO"
            data['description'] = "Le login AD n'est pas renseigne"

        else:
            sql = """
                SELECT R.faxname from reception R
                WHERE R.id = %(ID_FAX)s AND R.affichable = 1
            """

            db = get_db('postgres_db')
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, {'ID_FAX': id_fax})
            res = cursor.fetchone()
            cursor.close()
            
            # on convertit le fichier de .tif a .pdf
            faxname = res["faxname"].split('.', 1)[0]

            file_RX = os.path.join(app.config['FOLDER']['rx'], faxname + '.pdf')
            new_fax_name = None
            
            # Si le fichier existe on le copie dans le dossier de wait
            if os.path.isfile(file_RX): 
                # nom du fichier
                new_fax_name = login_ad.title() + "." + str(id_fax) +  "." + str(int(time.time()))

                # Retourne chemin absolu du nouveau de fax pour la copie du fichier dans le repertoire wait
                new_fax_name_path = os.path.join(app.config['FOLDER']['wait'], new_fax_name + ".pdf")

                # Copie du fichier dans le dossier wait
                shutil.copy(file_RX, new_fax_name_path)

            # le fichier n'existe pas
            else:
                data['status'] = 'KO'
                data['description'] = "Le fichier " + file_RX + " est inexistant : La copie du fax ne s'est pas effectué"
        
            data['items'] = {
                'new_fax_name': new_fax_name,
            }
    ##
    ## Transfert par mail
    ##
    elif type_trf == "MAIL":
        if queueRabbit == '' or hostRabbit == '':
            data['status'] = "KO"
            data['description'] = "La queue rabbit et/ou l'host rabbit n'est pas renseigne"

        else:
            # recuperation du fichier
            sql = """
                SELECT R.faxname, R.datetime from reception R
                WHERE R.id = %(ID_FAX)s AND R.affichable = 1
            """

            db = get_db('postgres_db')
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, {'ID_FAX': id_fax})
            res = cursor.fetchone()
            cursor.close()
            
            # reformate la date de reception du fax
            dateFax = str(res["datetime"])
            dateFax = datetime.datetime.strptime(dateFax, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y a %H:%M')

            # on convertit le fichier de .tif a .pdf
            faxname = res["faxname"].split('.', 1)[0]
            fileRX = os.path.join(app.config['FOLDER']['rx'], faxname + '.pdf')    

            # on verifie si le fichier existe dans le dossier RX
            if os.path.isfile(fileRX): 
                # encode le fichier en binaire
                dataFile = None
                dataFile = open(fileRX, 'rb').read()
            
                print('queue rabbit', queueRabbit)
                print('ipServerValide', hostRabbit)

                connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostRabbit, virtual_host="HYLAFAX"))
                channel = connection.channel()

                # envoi du message rabbit pour un mail a Hylanotify
                message = {
                    "type": "TRANSFER_MAIL",
                    "items": {
                        "subject": "Fax reçu le : " + dateFax,
                        "body": "",
                        "filename": os.path.basename(fileRX),
                        "dataFile": base64.b64encode(dataFile),   
                    }
                }

                channel.basic_publish(exchange='',
                                    routing_key=queueRabbit,
                                    body=json.dumps(message))
                connection.close()
            # le fichier n'existe pas dans le dossier RX
            else:
                data['status'] = 'KO'
                data['description'] = "Le fichier " + fileRX + " est inexistant : Le transfert par mail ne s'est pas effectué"

    ##
    ## Archivage pour la facturation
    ##
    elif type_trf == "FACT":
        numLDV = request.args.get('NumLDV', '')[:12]
        codeAG = request.args.get('codeAG', '')
        service = request.args.get('service', '')

        # Recuperation de l'agence pour l'archivage
        sql = """
                SELECT substr(A.code, 2, 3) as code FROM agence A 
                LEFT OUTER JOIN service S on A.id=S.id_agence
                WHERE S.id = %(SERVICE)s 
            """
        
        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'SERVICE': service})
        res = cursor.fetchone()
        cursor.close()

        agence = res["code"]

        # Recuperation du numero de document pour l'archivage
        sql = """
                SELECT R.ndoc_arc from reception R
                WHERE R.id = %(ID_FAX)s AND R.affichable = 1
            """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_FAX': id_fax})
        res = cursor.fetchone()
        cursor.close()

        ndoc_arc = res["ndoc_arc"]
        
        if agence == '' or ndoc_arc == None:
            data['status'] = "KO"
            data['description'] = "L'agence et/ou le numero de document n'est pas renseigne"
        
        else:
            try:
                # Inscription dans la base facturation
                sql = """
                    INSERT INTO archi_factu (ndoc_arc, ndoc_ext, agence) VALUES (%(NDOC_ARC)s, UPPER(%(NDOC_EXT)s), %(AGENCE)s)
                    """

                db = get_db('postgres_db')
                cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(sql, {'NDOC_ARC': ndoc_arc, 'NDOC_EXT': numLDV, 'AGENCE': agence})
                rowcount = cursor.rowcount
                cursor.close()

                # si pas d'insertion
                if rowcount == 0:
                    # Pas de mise à jour donc erreur
                    data['status'] = "KO"
                    data['description'] = "L'archivage vers la facturation ne s'est pas effectue"
                    
                # sinon on sauvegarde les changements
                else:
                    db.commit()

                # Mise a jour de l'etat du fax
                sql = """
                        UPDATE reception SET etatnew = etatnew | (16 + 8) WHERE id = %(ID_FAX)s;
                    """

                db = get_db('postgres_db')
                cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(sql, {'ID_FAX': id_fax})
                rowcount = cursor.rowcount
                cursor.close()
                
                 # si pas d'insertion
                if rowcount == 0:
                    # Pas de mise à jour donc erreur
                    data['status'] = "KO"
                    data['description'] = "La mise a jour du fax ne s'est pas effectue"
                    
                # sinon on sauvegarde les changements
                else:
                    db.commit()
            
            except psycopg2.IntegrityError:
                data["status"] = "KO"
                data["description"] = "Ce fax a déjà été archivé"
            except Exception as e:
                data["status"] = "KO"
                data["description"] = str(e)
               
            data["items"] = res

    ##
    ## Envoyer sur E-Track
    ##
    elif type_trf == "SCOP":

        service = request.args.get('service', '')

        # Recuperation de l'agence pour l'archivage
        sql = """
            SELECT substr(A.code, 2, 3) as code FROM agence A 
            LEFT OUTER JOIN service S on A.id=S.id_agence
            WHERE S.id = %(SERVICE)s 
        """
        
        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'SERVICE': service})
        res = cursor.fetchone()
        cursor.close()

        # code tiers sur 6 caracteres pour definir l'agence
        agence = "800" + res["code"]

        # recuperation du nom du fichier
        sql = """
            SELECT R.faxname from reception R
            WHERE R.id = %(ID_FAX)s AND R.affichable = 1
        """

        db = get_db('postgres_db')
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, {'ID_FAX': id_fax})
        res = cursor.fetchone()
        cursor.close()
        
        # on convertit le fichier de .tif a .pdf
        filename = os.path.join(app.config['FOLDER']['rx'], res["faxname"].split('.', 1)[0] + '.pdf')
        print(filename)
        
        # Si le fichier exist on appel la route aniweb pour archiver le fax
        if os.path.isfile(filename):
            values = {
                'NumLDV' : request.args.get('NumLDV', ''),
                'codeAG' : agence
            }

            # appel api aniweb
            url_archive_etrack = app.config.get("URLS").get("archive_ETrack")
            f = open(filename)
            files = {'file': f}
            print(url_archive_etrack)

            r = None
            try:
                r = requests.post(url_archive_etrack, files=files, data=values)
                if r.status_code <> requests.codes.ok:
                    data['status'] = "KO"
                    data['description'] = 'La requete POST a renvoye le code retour : %s' %r.status_code
                else:
                    # Mise a jour de l'etat du fax
                    sql = """
                            UPDATE reception SET etatnew = etatnew | (32 + 8) WHERE id = %(ID_FAX)s;
                        """

                    db = get_db('postgres_db')
                    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                    cursor.execute(sql, {'ID_FAX': id_fax})
                    rowcount = cursor.rowcount
                    cursor.close()
                    
                    # si pas d'insertion
                    if rowcount == 0:
                        # Pas de mise à jour donc erreur
                        data['status'] = "KO"
                        data['description'] = "La mise a jour du fax ne s'est pas effectue"
                        
                    # sinon on sauvegarde les changements
                    else:
                        db.commit()
                    
            except requests.exceptions.ConnectionError:
                print("Impossible de joindre l\'API AniWEB: ConnectionError'")
            except requests.exceptions.Timeout:
                print("Impossible de joindre l\'API AniWEB: Timeout")
            finally:
                f.close()
        
        # le fichier n'existe pas
        else:
            data['status'] = 'KO'
            data['description'] = "Le fichier " + filename + " est inexistant : L'envoi du fax sur E-Track ne s'est pas effectué"
    
    return jsonify(data)
    
                
if __name__ == '__main__':
    app.run(port=int("5002"), debug=debug_mode, host='0.0.0.0', threaded=True)
