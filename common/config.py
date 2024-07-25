
class galbumizer_config:
    def __init__(self, config):
        self.name = 'self'
        self.config = config       

    def getConfig(self, param):
        return self.config.get(param)
