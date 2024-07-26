
class gaa_config_parser_section:
    def __init__(self, config):
        self.name = 'self'
        self.config = config       

    def getConfig(self, param):
        return self.config.get(param)
