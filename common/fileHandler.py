import os
import pandas as pd 
from pathlib import Path

class FileHandler:

    def __init__(self, config):
        self.name = 'self'
        self.config = config
        self.meta_file_temp_suffix = config.meta_file_temp_suffix


    def split_csv(self, csvFilePath, newDirPath):
        df = pd.read_csv(csvFilePath, header=None)
        
        group_count = 0
        for (n), group in df.groupby(df.columns[0]):
            group_count = group_count + 1
            group.to_csv(f'{newDirPath}\\{n}{self.meta_file_temp_suffix}.csv')

        self.remove_first_column(newDirPath)
        return group_count


    def sort_csv(self, fromFileName, toFileName, deleteFromFile=True):
        pd.read_csv(fromFileName, header=None).sort_values([0,1], ascending=[True, False]).to_csv(toFileName, index=False, header=None)

        if deleteFromFile:
            os.remove(fromFileName)


    def remove_first_column(self, dir_path):

        temp_files = []
        for p in Path(dir_path).glob(f'*{self.meta_file_temp_suffix}.csv'):
            file_name = "{0}\\{1}".format(dir_path, p.name)            
            temp_files.append(file_name)
            df = pd.read_csv(file_name, header=0)            
            df = df.drop(df.columns[0], axis=1) #first column, coming extra after grouping           
            df.to_csv(file_name.replace(self.meta_file_temp_suffix, ""), index=False, header=None)

        
        for temp_file in temp_files:
            os.remove(temp_file)
            