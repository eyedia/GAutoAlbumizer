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
        self.image_extensions = (".jpg", ".jpeg") 
        self.fileHandler = FileHandler(config)
        self.count_dirs = 0
        self.count_files = 0

    def list_files_recursive(self, dir, root_dir):
          
        global file_content
        for entry in os.listdir(dir):        
            full_path = os.path.join(dir, entry)
            if os.path.isdir(full_path):
                self.count_dirs = self.count_dirs + 1
                self.list_files_recursive(full_path, root_dir)
            else:
                if full_path.endswith(self.image_extensions):
                    self.count_files = self.count_files + 1
                    album_name = self.getAlbumName(full_path, root_dir)
                    self.file_content += ("{0},{1},{2},False\n".format(album_name, full_path, datetime.datetime.fromtimestamp(os.path.getmtime(full_path))))
       

    def parse_directory(self, dir, root_dir):
        self.dir = dir
        self.list_files_recursive(dir, root_dir)
        f = open(self.config.meta_file_temp, "w")
        f.write(self.file_content)
        f.close()

        self.fileHandler.sort_csv(self.config.meta_file_temp, self.config.meta_file)        
        split_count = self.fileHandler.split_csv(self.config.meta_file, self.config.meta_album_dir)
        return (self.count_dirs, self.count_files, split_count)

    
    def getAlbumName(self, full_path, root_dir_name):        
        album_name = "default"
        try:
            album_name = full_path.split(f"{root_dir_name}\\")[1].split("\\")[0]
        
        except:
            pass

        if(album_name.endswith(self.image_extensions)):
            album_name = os.path.basename(os.path.dirname(full_path))
        
        return album_name