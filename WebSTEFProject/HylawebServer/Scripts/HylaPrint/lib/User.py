import ldap
import uuid
from ConfigParser import ConfigParser
from Log import logger

class User(object):

    @staticmethod
    def _split_into_chunks(string, chunk_length=2):
        chunks = []
        while len(string) > 0:
            chunks.append(string[:chunk_length])
            string = string[chunk_length:]
        return chunks
    
    @staticmethod
    def _to_oracle_raw16(string, strip_dashes=True, dashify_result=True):
        oracle_format_indices = [3,2,1,0,5,4,7,6,8,9,10,11,12,13,14,15]
        if strip_dashes:
            string = string.replace("-", "")
        parts = User._split_into_chunks(string)
        result = ""
        for index in oracle_format_indices:
            result = result + parts[index]
        if dashify_result:
            result = result[:8] + '-' + result[8:12] + '-' + result[12:16] + '-' + result[16:20] + '-' + result[20:]
        return result

    def __init__(self,config,file):
        self._login    = ''
        self._hostname = ''
        self._guid     = ''
        self._mail     = ''
        self._ldapserver = config.ldap['server']
        self._ldapuser = config.ldap['user']
        self._ldappass = config.ldap['pass']
        self._ldapbase = config.ldap['base']
        self._env(file)

    @property
    def login(self):
        return self._login

    @property
    def hostname(self):
        return self._hostname

    @property
    def mail(self):
        return self._mail
    
    @property
    def guid(self):
        return self._guid
    


    def getinfo(self):
        # Connexion avec l'AD pour les recherches
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, 10)
            sess_ldap = ldap.initialize(self._ldapserver)
        
            sess_ldap.protocol_version = ldap.VERSION3
            sess_ldap.set_option(ldap.OPT_REFERRALS, 0) # referrals = 0
            sess_ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            sess_ldap.simple_bind_s(self._ldapuser, self._ldappass)

            searchScope = ldap.SCOPE_SUBTREE

            #test que le login est un user et pas un computer
            criteria = "(&(!(objectClass=computer))(objectClass=user)(sAMAccountName=%s))" %self._login
            attributes = ['displayName', 'objectGUID', 'mail']
            result = sess_ldap.search_s(self._ldapbase, searchScope, criteria, attributes)
            results = [entry for dn, entry in result if isinstance(entry, dict)]
            if len(results)==0:
                logger.info("ldap : Impossible de trouver le user %s" %self._login)
            else:                
                object_guid = results[0]['objectGUID'][0]
                guid = uuid.UUID(bytes=object_guid)
                self._guid = User._to_oracle_raw16(str(guid))

                #test si le mail est bien present dans tab de retour (cas des comptes user generique sans mail)
                if results[0].has_key('mail'):
                    self._mail = results[0]['mail'][0]

        except ldap.LDAPError, e:
            logger.error('connexion AD impossible : {0}'.format(e.message['desc'] if 'desc' in e.message else str(e)))
        finally:
            sess_ldap.unbind_s()
        return self._guid<>''

    def _env(self,value):
        config = ConfigParser()
        config.read(value)
        self._login = config.get("ENV", "USER").upper()
        self._hostname = config.get("ENV", "MACHINE").upper()
        logger.debug('FILE : %s' %value)
        logger.debug('LOGIN : %s' %self._login)
        logger.debug('HOSTNAME : %s' %self._hostname)
        del config