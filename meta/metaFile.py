import os
import datetime
import sys
import pandas as pd 

sys.path.append("..")
from common.fileHandler import FileHandler

class metaFileHandler:
    def __init__(self, config):
        self.name = 'self'
        self.config = config
        self.dir =  ""
        self.file_content = ""        
        self.fileHandler = FileHandler(config)

    def list_files_recursive(self, path='.'):
        image_extensions = (".jpg", ".jpeg")   
        global file_content
        for entry in os.listdir(path):        
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):            	
                self.list_files_recursive(full_path)
            else:
                if full_path.endswith(image_extensions):
                    album_name = full_path.replace(self.dir + "\\", "").split("\\")[0]
                    if(album_name.endswith(image_extensions)):
                        album_name = os.path.basename(os.path.dirname(full_path))                
                    
                    self.file_content += ("{0},{1},{2},False\n".format(album_name, full_path, datetime.datetime.fromtimestamp(os.path.getmtime(full_path))))
       

    def parse_directory(self, dir):
        self.dir = dir
        self.list_files_recursive(dir)
        f = open(self.config.getConfig("meta_file_temp"), "w")
        f.write(self.file_content)
        f.close()

        self.fileHandler.sort_csv(self.config.getConfig("meta_file_temp"), self.config.getConfig("meta_file"))        
        self.fileHandler.split_csv(self.config.getConfig("meta_file"), self.config.getConfig("meta_album_dir"))