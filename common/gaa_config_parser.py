import os, sys, shutil, pathlib
import configparser
from .gaa_config_parser_section import gaa_config_parser_section 

class gaa_config_parser:
    def __init__(self, cwd, env="prod"):
        self.name = 'self'
        self.cwd = cwd
        

        if os.environ.get('EYEDIA_TECH_ENV') == "dev_local":
            #print("Working in development environment.")
            env = "dev_local"

        configParser = configparser.ConfigParser()
        full_path = os.path.join(self.cwd, 'config.ini')
        configParser.read(full_path)
        if configParser.has_section(env):           
            self.config_section = gaa_config_parser_section(configParser[env])
        else:
            raise ValueError(f'config {env} not found! Please update config.ini file and try again.')
        

        self.ensureEnvironment()

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def ensureEnvironment(self):
        self.app_data_dir = os.path.join(pathlib.Path(os.getenv('APPDATA')), "GAutoAlbumizer")
        self.app_data_local_dir = os.path.join(pathlib.Path(os.getenv('LOCALAPPDATA')), "GAutoAlbumizer")

        self.meta_file = os.path.join(self.app_data_dir, self.config_section.getConfig("meta_file"))
        self.meta_file_temp =  os.path.join(self.app_data_dir, self.config_section.getConfig("meta_file_temp"))
        self.meta_file_temp_suffix = self.config_section.getConfig("meta_file_temp_suffix")
        self.meta_album_dir = os.path.join(self.app_data_dir, self.config_section.getConfig("meta_album_dir"))
        self.sample_album_dir = os.path.join(self.app_data_dir, self.config_section.getConfig("meta_file_temp"))
        self.log_dir = os.path.join(self.app_data_dir, self.config_section.getConfig("log_dir"))
        self.auth_token_file = os.path.join(self.app_data_local_dir, self.config_section.getConfig("auth_token_file"))        
        self.client_secrets_file = os.path.join(self.cwd, "client_secrets.json")

        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)

        if not os.path.exists(self.meta_album_dir):
            os.makedirs(self.meta_album_dir)

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        if not os.path.exists(self.app_data_local_dir):
            os.makedirs(self.app_data_local_dir)

        if not os.path.exists(os.path.dirname(self.auth_token_file)):
            os.makedirs(os.path.dirname(self.auth_token_file))
        
       


        # if config.getConfig("local") == "false" and not os.path.exists("sample_albums") and os.path.exists(self.resource_path(config.getConfig("sample_album_dir"))):
        #     print("extracing sample albums...")
        #     shutil.copytree(self.resource_path(config.getConfig("sample_album_dir")), "./sample_albums")

    
    @property
    def thingy(self):
        return self.config_section.getConfig("meta_file_temp")