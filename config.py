import json
import os.path

class Config(object):
    def __init__(self):
        configPath = "appsettings.json"
        self.__cfgValues = {
            # application database
            'dbPath': 'readings.db', 
            # refresh interval in seconds
            'interval': 20, 
            # azure storage upload enabled
            'azure': True,
            # azure storage account name
            'account': 'myStorageAccount',
            # azure storage key
            'key': 'myStorageKey',
            # DHT22 GPIO pin (BCM)
            'pin': 4, 
        }
        # default values
        if(not os.path.exists(configPath)):
            # create default config file
            self.__WriteConfig(configPath, self.__cfgValues)
        else:
            self.__cfgValues = self.__ReadConfig(configPath)

    @property
    def DbPath(self):
        return self.__cfgValues['dbPath']
    
    @property
    def Interval(self):
        return self.__cfgValues['interval']

    @property
    def Azure(self):
        return self.__cfgValues['azure']

    @property
    def Account(self):
        return self.__cfgValues['account']

    @property
    def Key(self):
        return self.__cfgValues['key']

    @property
    def Pin(self):
        return self.__cfgValues['pin']

    def __WriteConfig(self, path, config):
        cfgStr = json.dumps(config, indent=4, separators=(',', ': '))
        cfg = open(path, 'w')
        cfg.write(cfgStr)
        cfg.close()

    def __ReadConfig(self, path):
        cfg = open(path)
        result = json.load(cfg)
        cfg.close()
        return result

