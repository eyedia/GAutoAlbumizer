import os
import datetime
import sys

sys.path.append("..")
from common.fileHandler import FileHandler

class metaFileHandler:
    def __init__(self):
        self.name = 'self'
        self.dir =  ""
        self.file_content = ""
        self.output_file_temp = ".\\data\\album_data_temp.csv"
        self.output_file = ".\\data\\album_data.csv"
        self.fileHandler = FileHandler()

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
        print(self.file_content)
        f = open(self.output_file_temp, "w")
        f.write(self.file_content)
        f.close()

        self.fileHandler.sort_csv(self.output_file_temp, self.output_file)
        #pd.read_csv(self.output_file_temp, header=None).sort_values([0,1], ascending=[True, False]).to_csv(self.output_file, index=False, header=None)
        #os.remove(self.output_file_temp)


    def split_csv(self, csvFilePath, newDirPath):       
       self.fileHandler.split_csv(csvFilePath, newDirPath)