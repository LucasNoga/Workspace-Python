from ConfigParser import ConfigParser

class Config(object):
    def __init__(self, file):
        # Load config File
        config = ConfigParser()
        config.read(file)

        self.db = config._sections['DATABASE']
        self.rabbit = config._sections['RABBITMQ']
        self.log = config._sections['LOG']
        del config


