#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time
import os
import urllib
import re
import json
from functools import wraps
from flask import Flask, session, redirect, url_for, render_template, request, jsonify, g, send_file
import requests
from flask_session import Session
import ldap
# DB
import psycopg2
import psycopg2.extras
####### Gestion du codage UTF8 dans la base POSTGRES ##############
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
###################################################################
from reverse_proxy import ReverseProxied

project_root = os.path.dirname(__file__)

SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = os.path.join(project_root,'flask_session')
SESSION_PERMANENT = True

app = Flask(__name__)


# timestamp pour la version des scripts javascript
timestamp = str(int(time.time()))

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

app.config.from_object(__name__)
Session(app)

########################################################################################################################################
# Début jinja

def datetimeformat(value, format='%d-%m-%Y %H:%M'):
    if value == None:
      return '-'
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat

@app.context_processor
def name_app():
    """Retourne les variables globales"""
    return dict(APP_NAME='HylaWEB', HYLA_SEND='HylaSend', VERSION=app.config["VERSION"], VERSION_JS=timestamp)

# Fin jinja
########################################################################################################################################
# Debut Route
# TODO a mettre dans un decorator pour savoir quelle template lancé print(request.headers.getlist("Accept-Language"))
# Authentification de l'utilisateur
def login_required(f):
  @wraps(f)
  def wrapped(*args, **kwargs):
    #IdModule = '3200' 
    IdModule = ''
    auth = session.get('auth', 'not set')
    sid = session.sid
    chaine = 'http://ws-metz-01/auth-ad/auth.asp?sid=' + sid + '&idmodule=' + IdModule + '&url=' + urllib.quote(request.url)
    print("url ", chaine)
    print("id de session " + sid)
    now = datetime.datetime.now()  # on récupère la date actuelle
    timestamp = time.mktime(now.timetuple()) - session.get('timestamp', 0)  # on effectue la conversion
    if timestamp >= 300:  # si > 5 min on verifie authentification user
        print 'Session expired or no AD access : [' + str(timestamp) + '] => Login'
        return redirect ('http://ws-metz-01/auth-ad/auth.asp?sid=' + sid + '&idmodule=' + IdModule + '&url=' + urllib.quote(request.url)) #ne pas mettre stef-tfe.nt sinon pb de cookies
        return redirect(url_for('login'))
    return f(*args, **kwargs)
  return wrapped


# Test si le user a les droits d'acceder a la page en verifiant son id de service par défaut
def check_user(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        json = get_infos_user()
         # si les infos sont invalides ou pas de service par defaut
        if json is None or json["id_serv_default"] is None:
            return redirect(url_for('error', ERR='USER'))
        return f(*args, **kwargs)
    return wrapped

###################### HylaFax ##############################
# Recupere les infos du user
def get_infos_user():
    req = None
    print("Recuperation des infos de l'utilisateur avec le guid %s " %session['guid']) 
    url_get_user = app.config["URL_API"].get("get_user").replace("#GUID#", session["guid"])
    try:
        req = requests.get(url_get_user)
    except Exception as e:
        print str(e)
        print("Impossible d'acceder a l'adresse: " + url_get_user)
    if req is not None:
        return req.json()["items"]
    else:
        return None

# Affiche la reception des fax
@app.route('/app/rx')
@login_required
@check_user
def fax_receive():
    ### recupere les infos sur l'utilisateur
    user = get_infos_user()
    return render_template("pages/reception.html", user=user, login=session["login"])

# Affiche l'emission des fax
@app.route('/app/tx')
@login_required
@check_user
def fax_emit():
    ### recupere les infos sur l'utilisateur
    user = get_infos_user()
    return render_template("pages/emission.html", user=user, login=session["login"])

# Affiche la partie archive des fax
@app.route('/app/archive')
@login_required
def fax_archive():
    user = get_infos_user()
    return render_template("pages/archive.html", user=user)
    
# La page de présentation d'Hylafax
@app.route('/app/welcome')
def welcome():
    return redirect(url_for('static', filename='doc/PresHYLAFAX.pdf'))

###################### HylaSend ##############################
# Recupere les destinataires récents de l'utilisateur
def get_dests_recents():
    req = None
    url_dest_recent = app.config["URL_API"].get("dest_recent").replace("#GUID#", session["guid"])
    print(url_dest_recent)
    print("Recuperation des dest recents avec le guid %s ", session['guid']) 
    try:
        req = requests.get(url_dest_recent)
    except requests.exceptions.ConnectionError:
        print("Impossible d'acceder a l'adresse: " + url_dest_recent)
    if req is not None and req.status_code == requests.codes.ok:
        return req.json()
    else:
        return None

# Vérification de l'existence du fax
def check_fax(faxname):
    req = None
    url_check_fax = app.config["URL_API"].get("check_fax").replace("#FAXNAME#", faxname)
    print(url_check_fax)
    print("Verification de l'existance du PDF ", faxname)    
    try:
        req = requests.get(url_check_fax)
    except requests.exceptions.ConnectionError:
        print("Impossible d'acceder a l'adresse: " + url_check_fax)
    
    if req is not None and req.status_code == requests.codes.ok:
        return req.json()
    else:
        return None

# Recuperation des fichiers qui sont mis en attente
def get_standby_fax():
    req = None
    url_get_standBy_fax = app.config["URL_API"].get("get_list_standby_fax")
    print(url_get_standBy_fax)
    print("Verification du login de la personne ", session['login'])    
    try:
        req = requests.get(url_get_standBy_fax, {'login': session.get('login')})
    except requests.exceptions.ConnectionError:
        print("Impossible d'acceder a l'adresse: " + url_get_standBy_fax)
         # verifie si la liste est vide
    if req is not None and req.status_code == requests.codes.ok:
        if len(req.json()["items"]) != 0:
            return req.json()["items"]
        else:
            print("Pas de fax en attente")
            return None
    else:
        return None

# Emission d'un fax 
@app.route('/app/send/<faxname>')
@login_required
@check_user
def send_fax(faxname=None):
    user = get_infos_user()
    destRecents = {}
    destRecentsJSON = get_dests_recents()

    files = get_standby_fax()
    # si les infos sont valides 
    if destRecentsJSON != None:
        if destRecentsJSON['status'] == "OK":
            destRecents = destRecentsJSON['items']
    
        # si les infos sont invalides
        elif destRecentsJSON['status'] == "KO":
            return redirect(url_for('error', ERR='DEST-RECENT'))

    # Si pas de fax renseigné on lance la page sans la visualisation du fax
    if faxname=="new":
        return render_template('layout/hylasend.html', files=files, user=user, dest_recent=destRecents)
    
    # sinon on lance avec la visualisation en verifiant que le fax existe et valide
    else:
        # Si le nom du fax est renseigné
        if faxname is not None:
            # on verifie que le fax existe
            checkFaxJSON = check_fax(faxname)
            # si l'api nous renvoi quelque chose on considere que le fax existe
            if checkFaxJSON is not None:
                # print('json fax', json)
                if checkFaxJSON['status']=='OK':
                    # url qui recupere le fax
                    url_fax = app.config["URL_API"].get("get_fax").replace("#FAXNAME#", faxname)
                    return render_template('pages/hylasend_with_fax.html', url_fax=url_fax, files=files, user=user, dest_recent=destRecents)
                elif checkFaxJSON['status']=='KO':
                    return redirect(url_for('error', ERR='PDF'))
        # Si aucun nom de fax est renseigné
        else: 
            return redirect(url_for('error', ERR='PDF')) # TODO changer le message d'erreur

# Message Erreur
@app.route('/app/error')
@app.route('/app/error/')
@app.route('/app/error/<ERR>')
def error(ERR=None):
    if ERR=='mail':
        message="Votre email n'est pas renseigné dans votre compte AD"
    elif ERR=='PDF':
        message="Le fax demandé n'existe pas !"
    elif ERR=='DEST-RECENT':
        message="Vous ne disposez pas des droits nécessaires pour accéder aux destinataires récents !"
    elif ERR=='USER':
        message="Vous ne disposez pas des droits nécessaires pour accéder à cette fonctionnalité !"
    else:
        message="Erreur..."
    return render_template("pages/error.html", message=message)

@app.route('/login', methods=['POST'])
def login():
    sid=request.form.get('sid','')
    auth=request.form.get('auth','')
    nom=request.form.get('nom','')
    prenom=request.form.get('prenom','')
    mail=request.form.get('mail','')
    ag=request.form.get('ag','')
    guid=request.form.get('guid','')
    login=request.form.get('login','')

    if sid=='':
        print 'sid vide'
        #Authentification KO
        return "KO;error"

    if auth != 'OK':
        print 'auth KO'
        return "KO;error/ad"

    if mail == '':
        print 'mail vide'
        return "KO;error/mail"

    #on arrive ici avec la session du user
    agt=session.get('agt','not set')
    now = datetime.datetime.now()  # on récupère la date actuelle
    timestamp = time.mktime(now.timetuple())  # on effectue la convertion

    session['auth'] = 'OK'
    session['nom'] = nom
    session['prenom'] = prenom
    session['ag'] = str(ag)
    session['mail'] = mail
    session['timestamp'] = timestamp
    session['guid'] = guid
    session['login'] = login

    if (agt == 'not set' or ag.find(agt)==-1):
        agt= ag.split('|')[0]
        session['agt'] = agt

    print '******************************** Authentification OK ********************************'
    print 'session          : ' + sid
    print 'authentification : ' + auth
    print 'ag               : ' + ag
    print 'guid             : ' + guid
    print 'agt              : ' + agt
    print 'mail             : ' + mail
    print 'login            : ' + login
    # print 'droits           : ' + droit
    print 'timestamp        : ' + str(timestamp)
    print '*************************************************************************************'

    #Authentification OK
    return "OK;Authentification OK"

if __name__ == '__main__':
    app.run(port=int("5001"), debug=debug_mode, host="0.0.0.0", threaded=True)
