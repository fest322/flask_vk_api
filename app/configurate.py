try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os


class Config(object):

    def __init__(self, cfgPath):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('app/passwd.ini')

    def getSetting(self, mark, setting):
        try:
            setting = self.cfg[mark][setting]
        except KeyError:
            setting = None
        return setting
