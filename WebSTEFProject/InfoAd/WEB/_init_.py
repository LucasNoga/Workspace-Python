#! /usr/bin/python
# -*- coding: utf-8 -*-

###############################################
# https://github.com/maethor/avatar-generator #
###############################################

import os
import ldap
from flask import Flask, request, make_response
from flask_caching import Cache
from avatar_generator import Avatar
from reverse_proxy import ReverseProxied
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder


app = Flask(__name__)

# swagger

templateSwagger = {
    "info": {
        "title": "Active Directory API",        
        "description": "API to get data from active directory",
        "version": "1.0"
    },
    "basePath": "/",  # base bash for blueprint registration
    "swaggerUiPrefix": LazyString(lambda : request.environ.get('HTTP_X_SCRIPT_NAME', ''))
}

app.config['SWAGGER'] = {
    'uiversion': 3
}

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, template=templateSwagger)


# routes pour partage WSGI
app.wsgi_app = ReverseProxied(app.wsgi_app)

# paramétrage du cache
cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR' : './FlaskCache'
})

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

# 10h de cache
@app.route('/avatar/<text>.png',methods=['GET'])
@cache.cached(timeout=36000,query_string=True)
@swag_from('doc/avatar.yml')
def photo(text):
    """
    jkjkjk
    """
    LDAP_SERVER = app.config['LDAP']['server']
    LDAP_BASE   = app.config['LDAP']['base']
    LDAP_USER   = app.config['LDAP']['user']
    LDAP_PWD    = app.config['LDAP']['pwd']    

    size_avatar = 40
    headers = { 'Content-Type': 'image/png' }
    mail_user = request.args.get("mail","")
    key = request.args.get("key",text)
    if mail_user == "":
        avatar = Avatar.generate(size_avatar, text, key, "PNG")
        return make_response(avatar, 200, headers)
    key = request.args.get("key",mail_user)
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, 10)
    sess_ldap = ldap.initialize(LDAP_SERVER)
    sess_ldap.protocol_version = ldap.VERSION3
    sess_ldap.set_option(ldap.OPT_REFERRALS, 0) # referrals = 0
    sess_ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    sess_ldap.simple_bind_s(LDAP_USER, LDAP_PWD)

    searchScope = ldap.SCOPE_SUBTREE
    #recherche du user
    searchFilter= '(&(objectClass=user)(mail='+mail_user+'))'
    result = sess_ldap.search_s(LDAP_BASE, searchScope, searchFilter,['thumbnailPhoto'])[0]
    sess_ldap.unbind_s()
    if result[0] == None:
        # cas ou le user n'existe pas dans AD
        avatar = Avatar.generate(size_avatar, text, key, "PNG")
        return make_response(avatar, 200, headers)
    result = result[1]
    if result.has_key('thumbnailPhoto'):
        return make_response(result['thumbnailPhoto'][0], 200, headers)
    else:
        avatar = Avatar.generate(size_avatar, text, key, "PNG")
        return make_response(avatar, 200, headers)
        

if __name__ == '__main__':
    app.run(port=int("5005"), debug=debug_mode, host='0.0.0.0')
