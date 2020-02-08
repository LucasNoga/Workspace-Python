from ConfigParser import ConfigParser

class Config(object):
    def __init__(self, file):
        # Load config File
        config = ConfigParser()
        config.read(file)

        #self.db = config._sections['DATABASE']
        self.rabbit  = config._sections['RABBITMQ']
        self.threads = config._sections['THREADS']
        self.folders = config._sections['FOLDERS']
        self.ldap    = config._sections['LDAP']
        self.api     = config._sections['API']
        self.log     = config._sections['LOG']
        self.ifs     = config._sections['IFS']
        
        del config


